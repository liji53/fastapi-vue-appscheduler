use super::schemas::{FormData, FormItem, Log, Notice, NoticeItem, RunAppPayload};

use chrono::{DateTime, Local};
use ini::Ini;
use rand::Rng;
use serde_json::Value;
use sha1::{Digest, Sha1};
use std::collections::HashMap;
use std::path::Path;
use std::process::Command;
use std::{env, fs, thread};
use tauri::Window;

// 版本管理工具命令 接口
pub trait RepoCommand {
    fn local_path(&self) -> &String;

    /// 使用版本管理工具，导出python项目
    fn checkout(&self) -> Result<(), String>;

    /// 读取本地仓库中指定文件的内容
    fn cat(&self, file_path: &str) -> Result<String, String> {
        let file = Path::new(self.local_path()).join(file_path);
        if !file.exists() {
            return Err("readme.md文件不存在".to_string());
        }
        fs::read_to_string(file.to_string_lossy().to_string())
            .map_err(|e| format!("readme.md文件读取失败: {}", e))
    }

    /// 删除本地仓库
    fn delete(&self) -> Result<(), String> {
        println!("delete dir: {}", self.local_path());
        fs::remove_dir_all(self.local_path()).map_err(|e| format!("删除本地应用失败: {}", e))
    }

    /// 安装python项目中的依赖库，pip install -r requirements.txt
    fn install_requirements(&self) -> Result<(), String> {
        let requirement_path = Path::new(self.local_path()).join("requirements.txt");
        if !requirement_path.exists() {
            eprintln!("requirements.txt文件不存在");
            return Ok(());
        }
        let output = Command::new("pip")
            .arg("install")
            .arg("-r")
            .arg(format!("{}", requirement_path.to_string_lossy()))
            .output()
            .map_err(|e| format!("执行pip install失败: {}", e))?;
        if output.status.success() {
            Ok(())
        } else {
            eprintln!(
                "pip install 失败：{}",
                String::from_utf8_lossy(&output.stderr)
            );
            Err("执行pip install失败".to_string())
        }
    }

    /// 执行应用程序，python main.py
    fn run_app(&self, window: Window, task_name: String, task_id: u32) -> Result<(), String> {
        let repo_path = self.local_path().clone();
        let path = Path::new(&repo_path).join("main.py");
        if !path.exists() {
            return Err("项目中不存在main.py".to_string());
        }
        thread::spawn(move || {
            let _ = env::set_current_dir(repo_path);
            let output = Command::new("python")
                .arg("main.py")
                .output()
                .map_err(|e| format!("执行Command报错: {}", e));

            let mut success = false;
            let description: String;
            let log_content: String;
            match output {
                Ok(ret) => {
                    if ret.status.success() {
                        success = true;
                        description = "任务执行成功".to_string();
                        log_content = String::from_utf8_lossy(&ret.stdout).to_string();
                    } else {
                        description = "任务脚本执行报错".to_string();
                        log_content = String::from_utf8_lossy(&ret.stderr).to_string();
                    }
                }
                Err(e) => {
                    description = e.clone();
                    log_content = e;
                }
            }

            let now: DateTime<Local> = Local::now();
            let formatted_time = now.format("%m-%d %H:%M:%S").to_string();
            window
                .emit(
                    "run_app_result",
                    RunAppPayload {
                        notice: Notice{
                            name: "任务结果".to_string(),
                            list: vec![NoticeItem {
                                title: task_name,
                                avatar: "https://gw.alipayobjects.com/zos/rmsportal/ThXAXghbEsBCCSDihZxY.png".to_string(),
                                datetime: formatted_time,
                                r#type: "1".to_string(),
                                description,
                                status: if success {"success".to_string()} else {"danger".to_string()},
                                extra: if success {"成功".to_string()} else {"失败".to_string()},
                            }],
                        },
                        log: Log{
                            status: success,
                            execute_type: "手动".to_string(),
                            content: log_content,
                            task_id
                        }
                    },
                )
                .unwrap();
        });

        Ok(())
    }

    /// 获取当前任务的配置(注：配置的section会忽略，不能存在相同的key，如有相同的key最后的生效)
    /// todo: 需要考虑：多section、应用升级的情况
    fn getconfig_app(&self, app_form: String, task_id: u32) -> Result<String, String> {
        // 如果有设置过配置，则用该任务的配置，没有则用默认配置
        let mut config_path = Path::new(self.local_path()).join(format!("conf_{}.ini", task_id));
        if !config_path.exists() {
            config_path = Path::new(self.local_path()).join("config.ini");
        }

        let mut config = HashMap::new();
        let i = Ini::load_from_file(config_path).map_err(|_| "配置文件解析失败!".to_string())?;
        for (_section, prop) in i.iter() {
            for (k, v) in prop.iter() {
                config.insert(k.to_string(), v.to_string());
            }
        }

        println!("app表单: {}", app_form);
        // println!("应用配置: {:?}", config);

        if app_form == "[]" {
            default_config_form(&config)
        } else {
            task_config_form(&config, app_form)
        }
    }

    /// 设置当前任务的配置
    /// todo: 需要考虑：多section、应用升级的情况
    fn setconfig_app(&self, config_in: String, task_id: u32) -> Result<(), String> {
        let config_in: Value = serde_json::from_str(&config_in).map_err(|_| "配置转json失败!")?;
        let config_in = config_in.as_object().unwrap();
        let task_config_path = Path::new(self.local_path()).join(format!("conf_{task_id}.ini"));
        let mut config_path = task_config_path.clone();
        if !config_path.exists() {
            config_path = Path::new(self.local_path()).join("config.ini");
            if !config_path.exists() {
                return Err("该应用不存在配置，无需设置!".to_string());
            }
        }

        let mut cur_config =
            Ini::load_from_file(config_path).map_err(|_| "配置文件解析失败!".to_string())?;
        for (_section, prop) in cur_config.iter_mut() {
            for (key, _value) in config_in.iter() {
                if prop.contains_key(key) {
                    prop.insert(key, config_in[key].as_str().unwrap());
                }
            }
        }
        cur_config
            .write_to_file(task_config_path)
            .map_err(|e| format!("保存配置失败：{e}"))
    }
}

// 生成默认配置表单
fn default_config_form(config: &HashMap<String, String>) -> Result<String, String> {
    let mut config_form: Vec<FormItem> = Vec::new();
    for (key, value) in config.iter() {
        let random = rand::thread_rng().gen_range(1..=10000);
        config_form.push(FormItem {
            control_type: "Text".to_string(),
            name_cn: "文本框".to_string(),
            layout: false,
            id: random.to_string(),
            data: FormData {
                field_name: key.to_string(),
                label: key.to_string(),
                tip: "".to_string(),
                placeholder: "".to_string(),
                show_rule: "{}".to_string(),
                required: false,
                rule: "[]".to_string(),
                default: value.to_string(),
                csslist: "[]".to_string(),
            },
        })
    }
    let ret =
        serde_json::to_string(&config_form).map_err(|_| "struct转json str失败!".to_string())?;
    Ok(ret)
}

// 基于应用配置表单生成 表单
fn task_config_form(
    config: &HashMap<String, String>,
    app_form_str: String,
) -> Result<String, String> {
    // 存在应用的配置表单
    let app_form_array: Result<Value, serde_json::Error> = serde_json::from_str(&app_form_str);
    match app_form_array {
        Ok(mut app_form) => {
            let forms_val = app_form.as_array_mut();
            match forms_val {
                Some(forms) => {
                    for form in forms {
                        let field_name = form["data"]["fieldName"].as_str().unwrap();
                        if !config.contains_key(field_name) {
                            continue;
                        }
                        // 将当前配置的值更新到应用配置表单中
                        let config_val = &config[field_name];
                        if form["data"].get("itemConfig").is_none() {
                            let tmp = form["data"].as_object_mut().unwrap();
                            tmp.insert(
                                "default".to_string(),
                                Value::String(config_val.to_string()),
                            );
                        } else {
                            let tmp = form["data"]["itemConfig"].as_object_mut().unwrap();
                            tmp.insert("value".to_string(), Value::String(config_val.to_string()));
                        }
                    }
                }
                None => return default_config_form(&config),
            }
            let ret = serde_json::to_string(&app_form)
                .map_err(|_| "app_form转json str失败!".to_string())?;
            Ok(ret)
        }
        Err(e) => {
            println!("app表单str转json失败：{}", e);
            default_config_form(config)
        }
    }
}

/// 将python项目地址转化为本地安装路径，在windows中项目位于C:\USERS\XXX\.appscheduler 目录下
pub fn url_to_local_path(url: &String) -> String {
    let mut hasher = Sha1::new();
    hasher.update(url.as_bytes());
    let result = hasher.finalize();

    let mut user_path = ".".to_string(); // 默认当前路径
    if let Ok(user_profile) = env::var("USERPROFILE") {
        user_path = user_profile;
    }
    let path = Path::new(user_path.as_str())
        .join(".appscheduler")
        .join(format!("{:x}", result));
    return path.to_string_lossy().to_string();
}

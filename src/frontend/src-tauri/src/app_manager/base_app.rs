use chrono::{DateTime, Local};
use sha1::{Digest, Sha1};
use std::path::Path;
use std::process::Command;
use std::thread;
use std::{env, fs};
use tauri::Window;

#[derive(Clone, serde::Serialize)]
struct ListItem {
    avatar: String,
    title: String,
    datetime: String,
    r#type: String,
    description: String,
    status: String,
    extra: String,
}
#[derive(Clone, serde::Serialize)]
struct RunAppPayload {
    name: String,
    list: Vec<ListItem>,
}

// 版本管理工具命令 接口
pub trait RepoCommand {
    fn local_path(&self) -> &String;
    /// 使用版本管理工具，导出python项目
    fn checkout(&self) -> bool;
    /// 读取本地仓库中指定文件的内容
    fn cat(&self, file_path: &str) -> Result<String, std::io::Error> {
        let file = Path::new(self.local_path()).join(file_path);
        fs::read_to_string(file.to_string_lossy().to_string())
    }
    /// 删除本地仓库
    fn delete(&self) -> Result<(), std::io::Error> {
        println!("delete dir: {}", self.local_path());
        fs::remove_dir_all(self.local_path())?;
        Ok(())
    }

    /// 安装python项目中的依赖库，pip install -r requirements.txt
    fn install_requirements(&self) -> bool {
        let requirement_path = Path::new(self.local_path()).join("requirements.txt");
        let output: std::process::Output = Command::new("pip")
            .arg("install")
            .arg("-r")
            .arg(format!("{}", requirement_path.to_string_lossy()))
            .output()
            .expect(&format!("执行pip install失败"));
        if output.status.success() {
            return true;
        }
        false
    }
    /// 执行应用程序，python main.py
    fn run_app(&self, window: Window, task_name: String) -> Result<(), String> {
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
                .map_err(|e| format!("{}", e));

            let mut success = false;
            let err_msg: String;

            match output {
                Ok(ret) => {
                    if ret.status.success() {
                        success = true;
                        err_msg = "任务执行成功".to_string();
                    } else {
                        err_msg = "任务脚本执行报错".to_string();
                    }
                }
                Err(e) => {
                    err_msg = e;
                }
            }

            let now: DateTime<Local> = Local::now();
            let formatted_time = now.format("%m-%d %H:%M:%S").to_string();
            window
                .emit(
                    "run_app_result",
                    RunAppPayload {
                        name: "任务结果".to_string(),
                        list: vec![ListItem {
                            title: task_name,
                            avatar: "https://gw.alipayobjects.com/zos/rmsportal/ThXAXghbEsBCCSDihZxY.png".to_string(),
                            datetime: formatted_time,
                            r#type: "1".to_string(),
                            description: err_msg,
                            status: if success {"success".to_string()} else {"danger".to_string()},
                            extra: if success {"成功".to_string()} else {"失败".to_string()},
                        }],
                    },
                )
                .unwrap();
        });

        Ok(())
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

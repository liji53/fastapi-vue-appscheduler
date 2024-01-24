use sha1::{Digest, Sha1};
use std::fs;
use std::path::Path;
use std::process::Command;

// 版本管理工具命令 接口
pub trait RepoCommand {
    fn local_path(&self) -> &String;
    // 使用版本管理工具，导出python项目
    fn checkout(&self) -> bool;
    fn cat(&self, file_path: &str) -> Result<String, std::io::Error> {
        let file = Path::new(self.local_path()).join(file_path);
        fs::read_to_string(file.to_string_lossy().to_string())
    }
    // 删除本地仓库
    fn delete(&self) -> Result<(), std::io::Error> {
        println!("delete dir: {}", self.local_path());
        fs::remove_dir_all(self.local_path())?;
        Ok(())
    }

    // 安装python项目中的依赖库，pip install -r requirements.txt
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
    // 执行应用程序，python main.py
    fn run_app(&self) -> bool {
        true
    }
}

pub fn url_to_local_path(url: &String) -> String {
    let mut hasher = Sha1::new();
    hasher.update(url.as_bytes());
    let result = hasher.finalize();
    let path = Path::new("..").join(format!("{:x}", result));
    return path.to_string_lossy().to_string();
}

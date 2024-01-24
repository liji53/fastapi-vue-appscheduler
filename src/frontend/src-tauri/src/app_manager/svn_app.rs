use super::base_app::{url_to_local_path, RepoCommand};
use std::process::Command;

pub struct SvnRepo {
    url: String,        // 远程仓库地址
    local_path: String, // 本地仓库路径
}
impl SvnRepo {
    pub fn new(url: String) -> SvnRepo {
        return SvnRepo {
            local_path: url_to_local_path(&url),
            url,
        };
    }
}
impl RepoCommand for SvnRepo {
    fn local_path(&self) -> &String {
        &self.local_path
    }

    fn checkout(&self) -> bool {
        /* 默认使用本地svn的账号 */
        let output = Command::new("svn")
            .arg("checkout")
            .arg(&self.url)
            .arg(&self.local_path)
            .arg("--non-interactive")
            .arg("--trust-server-cert")
            .output()
            .expect(&format!("执行svn checkout {}失败", self.url));
        if output.status.success() {
            true
        } else {
            let stderr = String::from_utf8_lossy(&output.stderr);
            eprintln!("pip install failed: {}", stderr);
            false
        }
    }
}

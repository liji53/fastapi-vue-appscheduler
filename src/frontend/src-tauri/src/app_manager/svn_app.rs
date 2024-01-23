use sha1::{Digest, Sha1};
use std::path::Path;
use std::process::Command;

#[tauri::command]
pub fn install_svn_app(repo_url: &str) -> bool {
    let mut hasher = Sha1::new();
    hasher.update(repo_url.as_bytes());
    let result = hasher.finalize();
    let repo_folder = format!("{:x}", result);
    println!("svn导出目录：{}", repo_folder);

    let output = Command::new("svn")
        .arg("checkout")
        .arg(&repo_url)
        .arg(&repo_folder)
        .output()
        .expect(&format!("执行svn checkout {}失败", repo_url));

    if output.status.success() {
        println!("SVN checkout successful");
        println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
        let requirement_path = Path::new(&repo_folder).join("requirements.txt");
        let output: std::process::Output = Command::new("pip")
            .arg("install")
            .arg("-r")
            .arg(format!("{}", requirement_path.to_string_lossy()))
            .output()
            .expect(&format!("执行pip install {}失败", repo_url));
        if output.status.success() {
            println!("pip install successful");
            true
        } else {
            let stderr = String::from_utf8_lossy(&output.stderr);
            println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
            eprintln!("pip install failed: {}", stderr);
            false
        }
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr);
        eprintln!("SVN checkout failed: {}", stderr);
        false
    }
}

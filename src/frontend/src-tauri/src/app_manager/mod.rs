mod base_app;
mod svn_app;
use self::base_app::RepoCommand;
use serde::Serialize;
use svn_app::SvnRepo;
use tauri::Window;

#[tauri::command]
pub fn install_app(repo_url: &str) -> bool {
    if repo_url.ends_with(".git") {
        return false;
    }
    let svn_repo = SvnRepo::new(repo_url.to_string());
    let ret = svn_repo.checkout();
    if !ret {
        return false;
    }
    svn_repo.install_requirements()
}

#[tauri::command]
pub fn uninstall_app(repo_url: &str) -> bool {
    let svn_repo = SvnRepo::new(repo_url.to_string());
    if let Ok(_) = svn_repo.delete() {
        true
    } else {
        false
    }
}

#[derive(Serialize)]
pub struct Readme {
    success: bool,
    content: String,
}

#[tauri::command]
pub fn readme_app(repo_url: &str) -> Readme {
    let svn_repo: SvnRepo = SvnRepo::new(repo_url.to_string());
    if let Ok(content) = svn_repo.cat("readme.md") {
        Readme {
            success: true,
            content,
        }
    } else {
        Readme {
            success: false,
            content: "".to_string(),
        }
    }
}

#[tauri::command]
pub fn run_app(
    window: Window,
    repo_url: String,
    task_name: String,
    task_id: u32,
) -> Result<(), String> {
    let svn_repo: SvnRepo = SvnRepo::new(repo_url);
    svn_repo.run_app(window, task_name, task_id)
}

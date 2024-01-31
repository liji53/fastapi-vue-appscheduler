mod base_app;
mod schemas;
mod svn_app;
use self::base_app::RepoCommand;
use svn_app::SvnRepo;
use tauri::Window;

#[tauri::command]
pub fn install_app(repo_url: String) -> Result<(), String> {
    if repo_url.ends_with(".git") {
        return Err("不支持安装git应用".to_string());
    }
    let svn_repo = SvnRepo::new(repo_url);
    svn_repo.checkout()?;
    svn_repo.install_requirements()
}

#[tauri::command]
pub fn uninstall_app(repo_url: &str) -> Result<(), String> {
    let svn_repo = SvnRepo::new(repo_url.to_string());
    svn_repo.delete()
}

#[tauri::command]
pub fn readme_app(repo_url: &str) -> Result<String, String> {
    let svn_repo: SvnRepo = SvnRepo::new(repo_url.to_string());
    svn_repo.cat("readme.md")
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

#[tauri::command]
pub fn getconfig_app(repo_url: String, app_form: String, task_id: u32) -> Result<String, String> {
    let svn_repo: SvnRepo = SvnRepo::new(repo_url);
    svn_repo.getconfig_app(app_form, task_id)
}

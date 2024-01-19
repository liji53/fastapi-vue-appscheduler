// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
mod sys_resource {
    pub mod sys_info;
}
use sys_resource::sys_info::get_sys_info;

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_sys_info])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

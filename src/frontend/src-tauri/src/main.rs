// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_sys_info])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

use serde::Serialize;
use sysinfo::{CpuRefreshKind, Disks, MemoryRefreshKind, RefreshKind, System};

#[derive(Serialize)]
struct SysResource {
    cpu: f32,
    memory: f32,
    disk: u64,
    full_disk: u64,
}

#[tauri::command]
fn get_sys_info() -> SysResource {
    let mut s =
        System::new_with_specifics(RefreshKind::new().with_cpu(CpuRefreshKind::everything()));

    // Wait a bit because CPU usage is based on diff.
    std::thread::sleep(sysinfo::MINIMUM_CPU_UPDATE_INTERVAL);
    // Refresh CPUs again.
    s.refresh_cpu();
    // 计算平均CPU使用率
    let cpu_usages: Vec<f32> = s.cpus().iter().map(|x| x.cpu_usage()).collect();
    let cpu_avg = cpu_usages.iter().sum::<f32>() / cpu_usages.len() as f32;

    // 计算磁盘使用情况
    let disks: Disks = Disks::new_with_refreshed_list();
    let mut full_disk = 0;
    let mut usage_disk = 0;
    for disk in disks.list() {
        full_disk += disk.total_space();
        usage_disk += disk.total_space() - disk.available_space();
    }
    // 计算内存使用率
    s.refresh_memory_specifics(MemoryRefreshKind::new().with_ram());
    let memory_usage = (s.total_memory() - s.free_memory()) as f32 / s.total_memory() as f32;

    SysResource {
        cpu: cpu_avg,
        memory: memory_usage * 100.0,
        disk: usage_disk / (1024 * 1024 * 1024),
        full_disk: full_disk / (1024 * 1024 * 1024),
    }
}

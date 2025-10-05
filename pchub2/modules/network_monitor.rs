// network_monitor.rs
use std::process::Command;
use std::net::IpAddr;
use std::collections::HashMap;

#[no_mangle]
pub extern "C" fn monitor_network() {
    println!("[Rust Stub] Network Monitoring Started...");

    // List network interfaces (Windows/Mac/Linux compatible)
    ifcfg::IfCfg::get().unwrap().iter().for_each(|iface| {
        println!("Interface: {}", iface.name);
        if let Some(ip) = iface.address {
            println!("  IP: {}", ip);
        }
        if let Some(netmask) = iface.netmask {
            println!("  Netmask: {}", netmask);
        }
        println!("  Up: {}", iface.is_up);
    });

    // Simple ping test (example)
    let ping_target = "8.8.8.8";
    println!("Pinging {}...", ping_target);
    let output = if cfg!(target_os = "windows") {
        Command::new("ping").args(&["-n", "1", ping_target]).output().unwrap()
    } else {
        Command::new("ping").args(&["-c", "1", ping_target]).output().unwrap()
    };

    println!("Ping Result:\n{}", String::from_utf8_lossy(&output.stdout));
}

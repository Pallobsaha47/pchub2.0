Ultimate PC Hub – Project Description

Ultimate PC Hub is an advanced, all-in-one system monitoring and management tool for Windows PCs, designed to provide real-time insights into system performance, processes, network activity, and file changes. Built primarily with Python and a modular architecture, this project leverages multiple languages and technologies to deliver a powerful, interactive, and extensible platform for PC monitoring and control.

Key Features

System Monitoring

Live CPU and RAM usage graphs with per-core details.

Real-time disk usage statistics.

Display of top processes based on CPU and memory consumption.

Process Management

Interactive process table for viewing active processes.

(Future modules) Ability to terminate or snapshot specific processes.

Provides insight into resource-hogging or suspicious processes.

Network Information

Lists all network interfaces with their IP addresses.

Detects active Wi-Fi SSID (Windows only).

Can be extended for advanced network monitoring or packet capture.

File Monitoring & Security

Monitors key folders (Desktop, Downloads) for file creation, deletion, or modification.

Computes SHA-256 hashes of monitored files for integrity and security checks.

Logs all file events to an SQLite database for persistent records.

Hardware Sensors

Reads CPU and GPU temperatures.

Fan speed and power usage monitoring (Windows hardware sensors; extendable via C++ or Rust modules).

Provides a foundation for advanced hardware control.

Database & Reporting

Maintains an SQLite database for snapshots and file events.

Can export reports in CSV, JSON, or text formats.

Stores historical system performance and activity logs.

Modular & Extensible Architecture

Core implemented in Python with PyQt6 GUI and pyqtgraph visualizations.

Optional modules in C++ for fan/power control and Rust for high-performance network monitoring.

Web dashboard capabilities via HTML/CSS/JavaScript for remote monitoring.

Configurable via JSON for monitoring intervals and folder selection.

Technologies Used

Python: Core logic, GUI, monitoring, database.

PyQt6 & pyqtgraph: Interactive GUI and live graphs.

psutil & watchdog: System and file monitoring.

wmi & pynvml (optional): Hardware sensor integration.

SQLite: Persistent storage for snapshots and logs.

C++/Rust (optional): Advanced fan control, power management, network analysis.

HTML/CSS/JavaScript (optional): Web-based monitoring dashboard.

Project Goals

Provide a centralized hub for PC performance monitoring and process management.

Offer security awareness through real-time file monitoring and integrity checks.

Build a modular framework that allows integration of advanced features like fan control, GPU monitoring, and network analytics.

Enable future extensions such as automated alerts, remote dashboards, and system optimization tools.

Future Enhancements

Fully functional process control (terminate, prioritize, snapshot).

Real-time GPU and fan speed control using C++/Rust modules.

Interactive network monitoring with live ping, packet capture, and alerts.

Exportable, detailed performance and security reports.

Web-based dashboard for remote monitoring.

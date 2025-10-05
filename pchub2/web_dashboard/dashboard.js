// dashboard.js
// This script will connect to the Python backend (via HTTP or WebSocket) to fetch live data
// For now, we will simulate data to test the dashboard

console.log("Web dashboard loaded.");

// Function to simulate CPU/RAM/Disk graphs
function updateGraphs() {
    document.getElementById("cpu-graph").innerText = `CPU Usage: ${Math.floor(Math.random()*100)} %`;
    document.getElementById("ram-graph").innerText = `RAM Usage: ${Math.floor(Math.random()*100)} %`;
    document.getElementById("disk-graph").innerText = `Disk Usage: ${Math.floor(Math.random()*100)} %`;
}

// Function to simulate top processes
function updateProcesses() {
    const tbody = document.getElementById("process-table").getElementsByTagName("tbody")[0];
    tbody.innerHTML = ""; // Clear old rows

    for (let i = 0; i < 5; i++) {
        const row = tbody.insertRow();
        row.insertCell(0).innerText = 1000 + i; // PID
        row.insertCell(1).innerText = `Process_${i}`; // Name
        row.insertCell(2).innerText = Math.floor(Math.random()*50); // CPU %
        row.insertCell(3).innerText = Math.floor(Math.random()*30); // RAM %
    }
}

// Function to simulate network info
function updateNetwork() {
    const netDiv = document.getElementById("network-details");
    netDiv.innerText = `IP: 192.168.1.${Math.floor(Math.random()*255)}, Status: UP, WiFi SSID: MyNetwork`;
}

// Function to simulate hardware sensors
function updateHardware() {
    document.getElementById("cpu-temp").innerText = `CPU Temp: ${40 + Math.floor(Math.random()*40)} °C`;
    document.getElementById("gpu-temp").innerText = `GPU Temp: ${35 + Math.floor(Math.random()*45)} °C`;
    document.getElementById("fan-speed").innerText = `Fan Speed: ${1000 + Math.floor(Math.random()*3000)} RPM`;
    document.getElementById("power-usage").innerText = `Power Usage: ${50 + Math.floor(Math.random()*150)} W`;
}

// Function to simulate file monitor events
function updateFiles() {
    const tbody = document.getElementById("file-table").getElementsByTagName("tbody")[0];
    tbody.innerHTML = ""; // Clear old rows

    for (let i = 0; i < 3; i++) {
        const row = tbody.insertRow();
        row.insertCell(0).innerText = new Date().toLocaleTimeString(); // Timestamp
        row.insertCell(1).innerText = ["created", "deleted"][Math.floor(Math.random()*2)]; // Event
        row.insertCell(2).innerText = `C:/Users/User/Desktop/File${i}.txt`; // Path
        row.insertCell(3).innerText = Math.random().toString(36).substring(2, 10); // Fake SHA256
    }
}

// Update dashboard every 2 seconds
setInterval(() => {
    updateGraphs();
    updateProcesses();
    updateNetwork();
    updateHardware();
    updateFiles();
}, 2000);

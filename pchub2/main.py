import os, sys, psutil, hashlib, sqlite3, platform, socket, subprocess
from datetime import datetime
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------------- OPTIONAL MODULES ----------------
try:
    import wmi
    WINDOWS = True
except ImportError:
    WINDOWS = False

try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False

# ---------------- CONFIG ----------------
MONITOR_FOLDERS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads")
]
DB_FILE = "database.db"
QUARANTINE_FOLDER = os.path.expanduser("~/Quarantine")
os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

# ---------------- SIGNAL RGB ----------------
SIGNAL_RGB_PATH = r"C:\Users\pallo\AppData\Local\Programs\SignalRGB\SignalRGB.exe"

def launch_signalrgb():
    try:
        subprocess.Popen([SIGNAL_RGB_PATH])
    except Exception as e:
        print(f"Failed to launch SignalRGB: {e}")

def set_rgb_color(color_name):
    try:
        subprocess.run([SIGNAL_RGB_PATH, "--set-color", color_name])
    except Exception as e:
        print(f"Failed to set RGB color: {e}")

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS file_event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        event TEXT,
        path TEXT,
        sha256 TEXT
    )""")
    conn.commit()
    conn.close()

def log_file_event(event, path, sha):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO file_event (timestamp,event,path,sha256) VALUES (?,?,?,?)",
              (datetime.now().isoformat(), event, path, sha))
    conn.commit()
    conn.close()

# ---------------- FILE MONITOR ----------------
class FileMonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        sha = hash_file(event.src_path)
        log_file_event("created", event.src_path, sha)
    def on_deleted(self, event):
        if event.is_directory: return
        log_file_event("deleted", event.src_path, None)

def hash_file(path):
    try:
        h = hashlib.sha256()
        with open(path,"rb") as f:
            for chunk in iter(lambda: f.read(8192),b""):
                h.update(chunk)
        return h.hexdigest()
    except: return None

# ---------------- NETWORK ----------------
def get_network_info():
    info = {}
    try:
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for iface, addr_list in addrs.items():
            ips = [a.address for a in addr_list if getattr(a,'family',None) in [2, getattr(socket,'AF_INET',2)]]
            info[iface] = {'ips': ips, 'up': stats[iface].isup if iface in stats else None}
        if WINDOWS:
            try:
                out = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
                for line in out.splitlines():
                    if "SSID" in line and "BSSID" not in line:
                        info['WiFi SSID'] = line.split(":",1)[1].strip()
                        break
            except: info['WiFi SSID']=None
    except Exception as e:
        info["Error"] = str(e)
    return info

# ---------------- SNAPSHOT ----------------
def take_snapshot():
    cpu = psutil.cpu_percent()
    cpu_per_core = psutil.cpu_percent(percpu=True)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    procs = list(psutil.process_iter(['pid','name','cpu_percent','memory_percent']))
    top_cpu = sorted(procs,key=lambda x:x.info['cpu_percent'],reverse=True)[:5]
    top_mem = sorted(procs,key=lambda x:x.info['memory_percent'],reverse=True)[:5]
    net = get_network_info()
    return {'cpu':cpu,'cpu_per_core':cpu_per_core,'mem':mem,'disk':disk,'top_cpu':top_cpu,'top_mem':top_mem,'network':net}

# ---------------- GUI ----------------
class HubGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PCHub2 - Ultimate PC Control")
        self.resize(1200,800)
        self.init_ui()
        self.start_file_monitor()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)
        self.add_rgb_tab()  # RGB Tab

    def init_ui(self):
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        # --- System Overview ---
        self.overview_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.overview_tab.setLayout(layout)

        self.cpu_plot = pg.PlotWidget(title="CPU Usage %")
        self.cpu_curve = self.cpu_plot.plot(pen='r')
        self.mem_plot = pg.PlotWidget(title="RAM Usage %")
        self.mem_curve = self.mem_plot.plot(pen='g')
        layout.addWidget(self.cpu_plot)
        layout.addWidget(self.mem_plot)

        # --- Process Table ---
        self.proc_table = QtWidgets.QTableWidget()
        self.proc_table.setColumnCount(4)
        self.proc_table.setHorizontalHeaderLabels(["PID","Name","CPU %","MEM %"])
        self.proc_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.proc_table)

        self.tabs.addTab(self.overview_tab,"System Overview")

    # --- File Monitor ---
    def start_file_monitor(self):
        self.observer = Observer()
        handler = FileMonitorHandler()
        for folder in MONITOR_FOLDERS:
            os.makedirs(folder, exist_ok=True)
            self.observer.schedule(handler, folder, recursive=False)
        self.observer.start()

    # --- Update Stats ---
    def update_stats(self):
        snap = take_snapshot()
        # CPU
        if not hasattr(self,'cpu_data'): self.cpu_data=[]
        self.cpu_data.append(snap['cpu'])
        self.cpu_data=self.cpu_data[-50:]
        self.cpu_curve.setData(self.cpu_data)
        # MEM
        if not hasattr(self,'mem_data'): self.mem_data=[]
        self.mem_data.append(snap['mem'].percent)
        self.mem_data=self.mem_data[-50:]
        self.mem_curve.setData(self.mem_data)
        # Processes
        self.proc_table.setRowCount(len(snap['top_cpu']))
        for row,proc in enumerate(snap['top_cpu']):
            self.proc_table.setItem(row,0,QtWidgets.QTableWidgetItem(str(proc.info['pid'])))
            self.proc_table.setItem(row,1,QtWidgets.QTableWidgetItem(proc.info['name']))
            self.proc_table.setItem(row,2,QtWidgets.QTableWidgetItem(str(proc.info['cpu_percent'])))
            self.proc_table.setItem(row,3,QtWidgets.QTableWidgetItem(str(round(proc.info['memory_percent'],2))))

    # --- RGB Tab ---
    def add_rgb_tab(self):
        self.rgb_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.rgb_tab.setLayout(layout)

        launch_btn = QtWidgets.QPushButton("Launch SignalRGB")
        launch_btn.clicked.connect(launch_signalrgb)
        layout.addWidget(launch_btn)

        colors = ["Red","Green","Blue","White","Rainbow"]
        for color in colors:
            btn = QtWidgets.QPushButton(color)
            btn.clicked.connect(lambda _, c=color.lower(): set_rgb_color(c))
            layout.addWidget(btn)

        self.tabs.addTab(self.rgb_tab,"RGB Control")

    def closeEvent(self,event):
        self.observer.stop()
        self.observer.join()
        event.accept()

# ---------------- MAIN ----------------
if __name__=="__main__":
    try:
        init_db()
        app = QtWidgets.QApplication(sys.argv)
        hub = HubGUI()
        hub.show()
        sys.exit(app.exec())
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")





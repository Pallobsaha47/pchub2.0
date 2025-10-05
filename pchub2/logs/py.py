import subprocess

SIGNAL_RGB_PATH = r"C:\Full\Path\To\SignalRGB.exe"

# Launch SignalRGB (optional: in background)
subprocess.Popen([SIGNAL_RGB_PATH])

# Example: if SignalRGB supports CLI args, you could do:
# subprocess.run([SIGNAL_RGB_PATH, "--set-color", "red"])

import os, subprocess, time, psutil
from obswebsocket import obsws
from config import OBS_EXE, OBS_ARGS, OBS_EXE_DIR, OBS_WS_PORT, OBS_WS_PASSWORD

def is_obs_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'obs64.exe' in proc.info['name']:
            return True
    return False

def launch_obs():
    if is_obs_running():
        print("⚠️ OBS is already running. Skipping launch.")
        return True
    if not os.path.exists(OBS_EXE):
        print("❌ OBS not found at:", OBS_EXE)
        return False
    print("🚀 Launching OBS...")
    subprocess.Popen([OBS_EXE] + OBS_ARGS, cwd=OBS_EXE_DIR)
    return True

def connect_ws(retries=10):
    print("🔌 Connecting to OBS WebSocket...")
    for i in range(retries):
        try:
            ws = obsws("localhost", OBS_WS_PORT, OBS_WS_PASSWORD)
            ws.connect()
            print("✅ Connected to OBS WebSocket")
            return ws
        except Exception:
            print(f"⏳ Retry {i + 1}/{retries}...")
            time.sleep(1)
    print("❌ Failed to connect to OBS WebSocket")
    return None

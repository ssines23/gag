import os
import time
import subprocess
from obswebsocket import obsws, requests
from pynput import keyboard

# === CONFIG ===
OBS_ROOT = os.path.abspath("obs-portable")
OBS_EXE_DIR = os.path.join(OBS_ROOT, "bin", "64bit")
OBS_EXE = os.path.join(OBS_EXE_DIR, "obs64.exe")
OBS_ARGS = ["--startreplaybuffer", "--minimize-to-tray"]
OBS_WS_PORT = 4455
OBS_WS_PASSWORD = "clip123"
CLIP_PATH = "C:\\RocketClips"
# ==============

def ensure_clip_folder():
    os.makedirs(CLIP_PATH, exist_ok=True)

def launch_obs():
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

def main():
    ensure_clip_folder()
    launch_obs()
    ws = connect_ws()
    if not ws:
        return

    def on_press(key):
        try:
            if key == keyboard.Key.f8:
                print("🎬 F8 pressed — saving replay...")
                ws.call(requests.SaveReplayBuffer())
                print("✅ Replay saved successfully!")
            elif key == keyboard.Key.f10:
                print("🛑 F10 pressed — exiting...")
                ws.disconnect()
                return False
        except Exception as e:
            print(f"⚠️ Error handling key press: {e}")

    print(f"🟢 Ready! Clips will be saved to:\n{CLIP_PATH}")
    print("Press F8 to save a 20s clip. Press F10 to quit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()

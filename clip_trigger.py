import os
import time
import subprocess
from obswebsocket import obsws, requests
from pynput import keyboard
import psutil
import sys
import pygame
import time
import traceback

last_save_time = 0

# === CONFIG ===
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.abspath(".")

OBS_ROOT = os.path.join(BASE_DIR, "obs-portable")
OBS_EXE_DIR = os.path.join(OBS_ROOT, "bin", "64bit")
OBS_EXE = os.path.join(OBS_EXE_DIR, "obs64.exe")
OBS_ARGS = ["--startreplaybuffer", "--minimize-to-tray"]
OBS_WS_PORT = 4455
OBS_WS_PASSWORD = "clip123"
CLIP_PATH = "C:\\RocketClips"
# ==============

def play_sound():
    try:
        pygame.mixer.init()
        sound_path = os.path.join(BASE_DIR, "f8_sound.wav")  # Use BASE_DIR!
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"⚠️ Failed to play sound: {e}")


def ensure_clip_folder():
    os.makedirs(CLIP_PATH, exist_ok=True)

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


def safe_obs_call(call_fn):
    try:
        return call_fn()
    except Exception as e:
        print("⚠️ OBS WebSocket call failed:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        traceback.print_exc()
        return None

def main():
    ensure_clip_folder()
    launch_obs()
    ws = connect_ws()
    if not ws:
        return

    def on_press(key):
        global last_save_time
        try:
            if key == keyboard.Key.f8:
                now = time.time()
                if now - last_save_time < 5:
                    print("⏳ Save cooldown active. Try again shortly.")
                    return
                print("🎬 F8 pressed — saving replay...")
                last_save_time = now
                play_sound()
                safe_obs_call(lambda: ws.call(requests.SaveReplayBuffer()))
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
    try:
        main()
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        traceback.print_exc()


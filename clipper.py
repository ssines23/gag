# clipper.py

import time
from pynput import keyboard
from obswebsocket import requests
from sound import play_sound
from utils import ensure_clip_folder
from config import CLIP_PATH
from obs_controller import launch_obs, connect_ws

last_save_time = 0
ws = None  # global connection reference

def safe_obs_call(fn):
    try:
        return fn()
    except Exception as e:
        print(f"⚠️ OBS call error: {e}")

def save_clip():
    print("🎬 Saving replay...")
    play_sound()
    safe_obs_call(lambda: ws.call(requests.SaveReplayBuffer()))

def disconnect_obs():
    global ws
    if ws:
        ws.disconnect()
        print("🛑 OBS disconnected.")

def run_clipper():
    global ws, last_save_time
    ensure_clip_folder()
    launch_obs()
    ws = connect_ws()
    if not ws:
        return

    def on_press(key):
        try:
            if key == keyboard.Key.f8:
                now = time.time()
                if now - last_save_time < 5:
                    print("⏳ Cooldown active.")
                    return
                last_save_time = now
                save_clip()
            elif key == keyboard.Key.f10:
                print("🛑 Exiting...")
                disconnect_obs()
                return False
        except Exception as e:
            print(f"⚠️ Key press error: {e}")

    print(f"🟢 Clips saved to {CLIP_PATH}")
    print("Press F8 to clip. Press F10 to quit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

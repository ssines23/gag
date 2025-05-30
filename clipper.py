import time
from pynput import keyboard
from obswebsocket import requests
from sound import play_sound
from utils import ensure_clip_folder
from config import CLIP_PATH
from obs_controller import launch_obs, connect_ws

last_save_time = 0

def run_clipper():
    ensure_clip_folder()
    launch_obs()
    ws = connect_ws()
    if not ws:
        return

    def safe_obs_call(fn):
        try:
            return fn()
        except Exception as e:
            print(f"⚠️ OBS call error: {e}")

    def on_press(key):
        global last_save_time
        try:
            if key == keyboard.Key.f8:
                now = time.time()
                if now - last_save_time < 5:
                    print("⏳ Cooldown active.")
                    return
                print("🎬 Saving replay...")
                last_save_time = now
                play_sound()
                safe_obs_call(lambda: ws.call(requests.SaveReplayBuffer()))
            elif key == keyboard.Key.f10:
                print("🛑 Exiting...")
                ws.disconnect()
                return False
        except Exception as e:
            print(f"⚠️ Key press error: {e}")

    print(f"🟢 Clips saved to {CLIP_PATH}")
    print("Press F8 to clip. Press F10 to quit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

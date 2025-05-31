# clipper.py

import time
from pynput import keyboard
from obswebsocket import requests
from sound import play_sound
from utils import ensure_clip_folder
from config import CLIP_PATH
from obs_controller import launch_obs, connect_ws

class Clipper:
    def __init__(self):
        self.ws = None
        self.last_save_time = 0

    def safe_obs_call(self, fn):
        try:
            return fn()
        except Exception as e:
            print(f"⚠️ OBS call error: {e}")

    def save_clip(self):
        print("🎬 Saving replay...")
        play_sound()
        self.safe_obs_call(lambda: self.ws.call(requests.SaveReplayBuffer()))

    def disconnect(self):
        if self.ws:
            self.ws.disconnect()
            print("🛑 OBS disconnected.")

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f8:
                now = time.time()
                if now - self.last_save_time < 5:
                    print("⏳ Cooldown active.")
                    return
                self.last_save_time = now
                self.save_clip()
            elif key == keyboard.Key.f10:
                print("🛑 Exiting...")
                self.disconnect()
                return False
        except Exception as e:
            print(f"⚠️ Key press error: {e}")

    def run(self):
        ensure_clip_folder()
        launch_obs()
        self.ws = connect_ws()
        if not self.ws:
            return

        print(f"🟢 Clips saved to {CLIP_PATH}")
        print("Press F8 to clip. Press F10 to quit.")
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

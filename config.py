import os
import sys

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
SOUND_FILE = os.path.join(BASE_DIR, "f8_sound.wav")

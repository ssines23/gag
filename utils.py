import os
from config import CLIP_PATH

def ensure_clip_folder():
    os.makedirs(CLIP_PATH, exist_ok=True)

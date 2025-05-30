import pygame
from config import SOUND_FILE

def play_sound():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"⚠️ Failed to play sound: {e}")

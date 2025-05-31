# ui.py

import tkinter as tk
from clipper import Clipper
import threading

class GagUI:
    def __init__(self):
        self.clipper = Clipper()  # instantiate once
        self.root = tk.Tk()
        self.root.title("GaG")
        self.root.geometry("300x200")
        self.create_widgets()
        threading.Thread(target=self.clipper.run, daemon=True).start()

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="Ready", fg="green")
        self.status_label.pack(pady=10)

        self.clip_button = tk.Button(self.root, text="Save Clip (F8)", command=self.on_clip)
        self.clip_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit (F10)", command=self.on_quit)
        self.quit_button.pack(pady=5)

    def on_clip(self):
        self.clipper.save_clip()
        self.status_label.config(text="Clip Saved!", fg="blue")

    def on_quit(self):
        self.clipper.disconnect()
        self.root.quit()

    def run(self):
        self.root.mainloop()

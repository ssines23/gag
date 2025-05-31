# gag.py

from ui import GagUI
import threading
from clipper import run_clipper  # Ensure this is defined in your clipper.py

if __name__ == "__main__":
    threading.Thread(target=run_clipper, daemon=True).start()
    ui = GagUI()
    ui.run()

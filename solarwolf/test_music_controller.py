# test_slider.py
import time
import threading
import tkinter as tk
from tkinter import ttk
from scamp import instruments
from music_controller import MusicController

class MusicGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Intensity Controller")

        # Controller initialisieren
        self.controller = MusicController()

        # Start SCAMP in separatem Thread
        self.scamp_thread = threading.Thread(target=self.controller.run_scamp)
        self.scamp_thread.start()

        # Intensitätsskala
        self.intensity_scale = tk.Scale(root, from_=1.0, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,
                                        label="Intensity", length=300, command=self.on_intensity_change)
        self.intensity_scale.set(self.controller.current_intensity_level)
        self.intensity_scale.pack(pady=20)

        # Stop-Button, um die Musik zu beenden
        self.stop_button = ttk.Button(root, text="Stop Music", command=self.stop_music)
        self.stop_button.pack(pady=20)

        # Instrumente auflisten (optional)
        instruments.print_soundfont_presets()

    def on_intensity_change(self, value):
        # Wird aufgerufen, wenn der Slider bewegt wird
        # Konvertiere den Wert in float
        intensity = float(value)
        self.controller.update_music(intensity)
        print(f"[GUI] Intensity updated to {intensity}")

    def stop_music(self):
        print("[GUI] Stopping music now...")
        self.controller.stop_flag = True
        self.scamp_thread.join()
        print("[GUI] Process finished cleanly.")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicGUI(root)
    root.mainloop()

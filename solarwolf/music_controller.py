from scamp import Session
import threading
import random

class MusicController:
    def __init__(self):
        self.session = Session(tempo=120)
        self.instrument = self.session.new_part("piano")
        self.current_tempo = 120

        # Starten der Scamp-Session in einem separaten Thread
        self.scamp_thread = threading.Thread(target=self.session.wait_for_children_to_finish)
        self.scamp_thread.start()

        # Starten der Musik
        self.play_music()
        print("[DEBUG] Musikcontroller initialisiert und Musik gestartet.")

    def update_music(self, intensity):
        # Passen Sie das Tempo basierend auf der Intensität an
        new_tempo = 60 + (intensity * 100)  # Beispiel: Tempo zwischen 60 und 160
        if abs(new_tempo - self.current_tempo) > 5:
            print(f"[DEBUG] Aktualisiere Tempo von {self.current_tempo} auf {new_tempo}")
            self.current_tempo = new_tempo
            self.session.tempo = self.current_tempo

    def play_music(self):
        # Starten Sie eine Endlosschleife, um Musik zu spielen
        def music_loop():
            while True:
                self.instrument.play_note(
                    pitch=random.randint(60, 72),
                    length=0.5,
                    volume=0.8
                )
        self.session.fork(music_loop)
        print("[DEBUG] Musik-Loop gestartet.")

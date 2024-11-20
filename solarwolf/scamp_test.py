import time
from music_controller import MusicController

music_controller = MusicController()

# Simulieren von Intensitätsänderungen
for intensity in range(1, 5):
    music_controller.update_music(intensity)
    time.sleep(5)  # 5 Sekunden warten

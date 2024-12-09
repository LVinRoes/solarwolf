# test_script.py
from scamp import *
from music_controller import MusicController
import time

def main():
    # Controller initialisieren
    controller = MusicController()
    instruments.print_soundfont_presets()

    # Musik starten
    # run_scamp ist blockierend, da es auf wait_for_children_to_finish wartet.
    # Daher führen wir es in einem separaten Thread aus, um parallel Aktionen durchführen zu können.
    import threading
    scamp_thread = threading.Thread(target=controller.run_scamp)
    scamp_thread.start()

    # Einige Sekunden warten, um etwas Musik zu hören
    time.sleep(5)

    # Intensitätslevel aktualisieren
    controller.update_music(2)
    print("[TEST] Intensity level updated to 2")

    # Noch ein paar Sekunden warten
    time.sleep(5)

    controller.update_music(4)

    time.sleep(5)

    controller.update_music(1)

    time.sleep(5)

    controller.update_music(5)

    time.sleep(5)
    # Jetzt den Prozess stoppen
    print("[TEST] Stopping music now...")
    controller.stop_flag = True

    # Warten, bis alle Kinderprozesse beendet sind
    scamp_thread.join()

    print("[TEST] Process finished cleanly.")

if __name__ == "__main__":
    main()

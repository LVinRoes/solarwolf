import numpy as np
import time
import pygame

class ScreenProcessor:
    def __init__(self):
        self.previous_frame = None
        self.last_capture_time = 0
        self.capture_interval = 0.5  # in Sekunden

    def process_screen(self):
        current_time = time.time()
        if current_time - self.last_capture_time >= self.capture_interval:
            self.last_capture_time = current_time

            # Holen Sie sich das aktuelle Display-Surface
            screen_surface = pygame.display.get_surface()

            # Konvertieren Sie das Surface in ein Array
            screen_array = pygame.surfarray.array3d(screen_surface)

            # Transponieren Sie das Array, um die Achsen zu korrigieren
            screen_array = np.transpose(screen_array, (1, 0, 2))

            # Reduzieren Sie die Auflösung
            small_array = screen_array[::4, ::4]

            # Konvertieren Sie in Graustufen
            current_gray = np.dot(small_array[...,:3], [0.2989, 0.5870, 0.1140])

            # Normieren Sie die Werte
            current_gray = current_gray / 255.0

            if self.previous_frame is not None:
                # Berechnen der absoluten Differenz zwischen den Bildern
                frame_diff = np.abs(current_gray - self.previous_frame)

                # Berechnen Sie die durchschnittliche Änderung
                average_change = np.mean(frame_diff)

                # Skalierungsfaktor anwenden
                scaling_factor = 50.0  # Erhöhen Sie diesen Wert
                average_change *= scaling_factor
                average_change = min(average_change, 1.0)

                # Speichern Sie das aktuelle Bild
                self.previous_frame = current_gray

                # Debugging-Ausgabe
                #print(f"[DEBUG] Durchschnittliche Bildänderung (skaliert): {average_change}")

                return average_change
            else:
                self.previous_frame = current_gray
                return None
        else:
            return None



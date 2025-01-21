import numpy as np
import time
import pygame

class ScreenProcessor:
    def __init__(self):
        self.previous_frame = None
        self.last_capture_time = 0
        self.capture_interval = 0.5  # in Sekunden
        self.last_intensity = 0.0
        #print("image processor initialized")

    def process_screen(self):
        current_time = time.time()
        # Debug-Statement: Ausgeben, wann die Methode aufgerufen wurde
        #print(f"[DEBUG] process_screen() aufgerufen. current_time={current_time}")

        if current_time - self.last_capture_time >= self.capture_interval:
            self.last_capture_time = current_time
            #print(f"[DEBUG] Neue Aufnahme wird gemacht (>= {self.capture_interval} s vergangen).")

            screen_surface = pygame.display.get_surface()
            if screen_surface is None:
                #print("[ERROR] screen_surface ist None. pygame.display wurde evtl. nicht korrekt initialisiert?")
                return None

            screen_array = pygame.surfarray.array3d(screen_surface)
            screen_array = np.transpose(screen_array, (1, 0, 2))
            small_array = screen_array[::4, ::4]

            current_gray = np.dot(small_array[..., :3], [0.2989, 0.5870, 0.1140])
            current_gray /= 255.0
            #print(f"[DEBUG] Aktuelles Graustufen-Array erstellt. Shape={current_gray.shape}")

            if self.previous_frame is not None:
                frame_diff = np.abs(current_gray - self.previous_frame)
                average_change = np.mean(frame_diff)
                # Skalierungsfaktor
                average_change *= 200.0
                # Begrenzen auf [0,1]
                average_change = min(max(average_change, 0.0), 1.0)
                self.last_intensity = average_change
                result = average_change

                #print(f"[DEBUG] Frame-Differenz berechnet. average_change={average_change:.4f}")
            else:
                #print("[DEBUG] Kein previous_frame vorhanden; Differenz kann nicht berechnet werden.")
                result = self.last_intensity

            self.previous_frame = current_gray
            return result
        else:
            #print("[DEBUG] Noch nicht genug Zeit vergangen - kein neuer Screenshot.")
            return None

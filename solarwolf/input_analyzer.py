import pygame
import time

class InputAnalyzer:
    def __init__(self):
        self.key_counts = {}
        self.last_reset_time = time.time()
        self.reset_interval = 1.0  # in Sekunden
        self.smoothed_intensity = 0.0  # Neuer geglätteter Intensitätswert
        self.alpha = 0.5  # Glättungsfaktor (zwischen 0 und 1)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            self.key_counts[key_name] = self.key_counts.get(key_name, 0) + 1
            print(f"[DEBUG] Verarbeitete Taste: {key_name}")
            
    def get_input_intensity(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_reset_time
        if elapsed_time >= self.reset_interval:
            # Berechnen der aktuellen Eingabeintensität
            total_keys_pressed = sum(self.key_counts.values())
            current_intensity = total_keys_pressed / elapsed_time

            # Normalisieren der aktuellen Intensität (optional, je nach Skala)
            max_possible_keys = 10  # Schätzen Sie die maximale Anzahl von Tastendrücken pro Intervall
            current_intensity = min(current_intensity / max_possible_keys, 1.0)

            # Anwenden der exponentiellen Glättung
            self.smoothed_intensity = (
                self.alpha * current_intensity
                + (1 - self.alpha) * self.smoothed_intensity
            )

            # Reset
            self.key_counts = {}
            self.last_reset_time = current_time

            return self.smoothed_intensity
        else:
            return None


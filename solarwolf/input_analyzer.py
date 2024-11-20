import pygame
import time

class InputAnalyzer:
    def __init__(self):
        self.key_counts = {}
        self.last_reset_time = time.time()
        self.reset_interval = 0.5  # Erhöhtes Intervall für langsamere Aktualisierung
        self.smoothed_intensity = 0.0
        self.alpha = 0.5  # Niedrigerer Glättungsfaktor für stärkere Glättung
        self.intensity_history = []  # Liste zur Speicherung der letzten Intensitätswerte
        self.history_length = 5  # Anzahl der Werte im gleitenden Durchschnitt

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            self.key_counts[key_name] = self.key_counts.get(key_name, 0) + 1
            #print(f"[DEBUG] Verarbeitete Taste: {key_name}")

    def get_input_intensity(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_reset_time
        if elapsed_time >= self.reset_interval:
            # Berechnen der aktuellen Eingabeintensität
            total_keys_pressed = sum(self.key_counts.values())
            current_intensity = total_keys_pressed / elapsed_time

            # Normalisieren der aktuellen Intensität
            max_possible_keys = 5  # Anpassen je nach erwarteter maximaler Eingabe
            current_intensity = min(current_intensity / max_possible_keys, 1.0)

            # Anwenden des gleitenden Durchschnitts
            self.intensity_history.append(current_intensity)
            if len(self.intensity_history) > self.history_length:
                self.intensity_history.pop(0)
            average_intensity = sum(self.intensity_history) / len(self.intensity_history)

            # Exponentielle Glättung
            self.smoothed_intensity = (
                self.alpha * average_intensity
                + (1 - self.alpha) * self.smoothed_intensity
            )

            # Reset
            self.key_counts = {}
            self.last_reset_time = current_time

            # Debugging-Ausgabe
            #print(f"[DEBUG] Geglättete Eingabeintensität: {self.smoothed_intensity}")

            return self.smoothed_intensity
        else:
            return None

import pygame
import time

class InputAnalyzer:
    def __init__(self):
        self.key_counts = {}
        self.last_reset_time = time.time()
        self.reset_interval = 1.0  # in Sekunden

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            self.key_counts[key_name] = self.key_counts.get(key_name, 0) + 1
            print(f"[DEBUG] Verarbeitete Taste: {key_name}")
            
    def get_input_intensity(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_reset_time
        if elapsed_time >= self.reset_interval:
            # Berechnen der Eingabeintensität
            total_keys_pressed = sum(self.key_counts.values())
            intensity = total_keys_pressed / elapsed_time
            print(f"[DEBUG] Berechnete Eingabeintensität: {intensity}")

            # Reset
            self.key_counts = {}
            self.last_reset_time = current_time

            return intensity
        else:
            return None

from pynput import keyboard
import time

class GlobalInputAnalyzer:
    def __init__(self, reset_interval=0.5):
        self.key_counts = {}
        self.reset_interval = reset_interval
        self.last_reset_time = time.time()
        self.intensity_history = []
        self.history_length = 5
        self.last_intensity = 0.0
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        print("GlobalInputAnalyzer initialized")

    def on_press(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key)
        self.key_counts[key_name] = self.key_counts.get(key_name, 0) + 1
        print(f"[DEBUG] Taste gedrückt: {key_name} (Gesamt: {self.key_counts[key_name]})")

    def process_event(self, event):
        # Globale Eingaben werden über pynput erfasst – diese Methode bleibt leer.
        pass

    def get_input_intensity(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_reset_time
        if elapsed_time >= self.reset_interval:
            total_keys_pressed = sum(self.key_counts.values())
            if total_keys_pressed == 0:
                current_intensity = 0.0
            else:
                current_intensity = total_keys_pressed / elapsed_time

            current_intensity = min(current_intensity / max_possible_intensity, 1.0)
            
            if total_keys_pressed == 0:
                decay_factor = 0.5  # Abklingfaktor; kann angepasst werden
                current_intensity = self.last_intensity * (1 - decay_factor)
            
            # Gleitender Mittelwert (ohne exponentielles Smoothing)
            self.intensity_history.append(current_intensity)
            if len(self.intensity_history) > self.history_length:
                self.intensity_history.pop(0)
            average_intensity = sum(self.intensity_history) / len(self.intensity_history)

            self.key_counts = {}
            self.last_reset_time = current_time
            self.last_intensity = average_intensity
            print(f"[DEBUG] Durchschnittliche Intensität: {average_intensity}")
            return self.last_intensity
        else:
            return self.last_intensity

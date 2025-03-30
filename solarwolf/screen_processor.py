import numpy as np
import time
import pygame
import os
import matplotlib.pyplot as plt

class ScreenProcessor:
    def __init__(self):
        self.previous_frame = None
        self.last_capture_time = 0
        self.capture_interval = 0.5  # in Sekunden
        self.last_intensity = 0.0

        # Attribute für den Demo-Capture-Zustandsautomaten
        self.demo_interval = 10  # Zyklus alle 10 Sekunden
        self.last_demo_time = time.time()
        self.demo_cycle = 0
        self.demo_output_dir = "screenshots"
        if not os.path.exists(self.demo_output_dir):
            os.makedirs(self.demo_output_dir)
        self.demo_state = 'idle'  # mögliche Zustände: 'idle', 'waiting_for_B'
        self.screenshot_A = None
        self.screenshot_A_time = 0

    def process_screen(self):
        current_time = time.time()
        if current_time - self.last_capture_time >= self.capture_interval:
            self.last_capture_time = current_time

            screen_surface = pygame.display.get_surface()
            if screen_surface is None:
                return None

            screen_array = pygame.surfarray.array3d(screen_surface)
            screen_array = np.transpose(screen_array, (1, 0, 2))
            small_array = screen_array[::4, ::4]

            current_gray = np.dot(small_array[..., :3], [0.2989, 0.5870, 0.1140])
            current_gray /= 255.0

            if self.previous_frame is not None:
                frame_diff = np.abs(current_gray - self.previous_frame)
                average_change = np.mean(frame_diff)
                average_change *= 200.0
                average_change = min(max(average_change, 0.0), 1.0)
                self.last_intensity = average_change
                result = average_change
            else:
                result = self.last_intensity

            self.previous_frame = current_gray
            return result
        else:
            return None

    def capture_current_screen(self):
        """Erfasst den aktuellen Bildschirm und gibt ihn als NumPy-Array zurück."""
        screen_surface = pygame.display.get_surface()
        if screen_surface is None:
            return None
        screen_array = pygame.surfarray.array3d(screen_surface)
        screen_array = np.transpose(screen_array, (1, 0, 2))
        return screen_array

    def downscale_and_grayscale(self, array):
        """Downscaled das Bild (jede 4. Zeile/Spalte) und wandelt es in Graustufen um."""
        small_array = array[::4, ::4]
        gray = np.dot(small_array[..., :3], [0.2989, 0.5870, 0.1140])
        gray = gray / 255.0
        return gray

    def save_image(self, array, filename, cmap=None):
        """Speichert ein NumPy-Array als Bild mithilfe von Matplotlib."""
        plt.imsave(filename, array, cmap=cmap)

    def update_demo_capture(self):
        
        current_time = time.time()
        if self.demo_state == 'idle':
            if current_time - self.last_demo_time >= self.demo_interval:
                # Screenshot A aufnehmen
                screenshot_A = self.capture_current_screen()
                if screenshot_A is not None:
                    self.screenshot_A = screenshot_A
                    gray_A = self.downscale_and_grayscale(screenshot_A)
                    filename_A = os.path.join(self.demo_output_dir, f"screenshotA_cycle{self.demo_cycle}.png")
                    filename_A_gray = os.path.join(self.demo_output_dir, f"screenshotA_gray_cycle{self.demo_cycle}.png")
                    self.save_image(screenshot_A, filename_A)
                    self.save_image(gray_A, filename_A_gray, cmap="gray")
                    self.screenshot_A_time = current_time
                    self.demo_state = 'waiting_for_B'
        elif self.demo_state == 'waiting_for_B':
            if current_time - self.screenshot_A_time >= 0.5:
                # Screenshot B aufnehmen
                screenshot_B = self.capture_current_screen()
                if screenshot_B is not None:
                    gray_B = self.downscale_and_grayscale(screenshot_B)
                    filename_B = os.path.join(self.demo_output_dir, f"screenshotB_cycle{self.demo_cycle}.png")
                    filename_B_gray = os.path.join(self.demo_output_dir, f"screenshotB_gray_cycle{self.demo_cycle}.png")
                    self.save_image(screenshot_B, filename_B)
                    self.save_image(gray_B, filename_B_gray, cmap="gray")
                    # Differenz berechnen
                    gray_A = self.downscale_and_grayscale(self.screenshot_A)
                    frame_diff = np.abs(gray_B - gray_A)
                    diff_scaled = np.clip(frame_diff * 200.0, 0.0, 1.0)
                    filename_diff = os.path.join(self.demo_output_dir, f"screenshot_diff_cycle{self.demo_cycle}.png")
                    self.save_image(diff_scaled, filename_diff, cmap="gray")
                    print(f"Demo-Zyklus {self.demo_cycle} abgeschlossen.")
                    self.demo_cycle += 1
                    self.last_demo_time = current_time
                    self.demo_state = 'idle'

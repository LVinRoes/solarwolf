# intensity_calculator.py
class IntensityCalculator:
    def __init__(self, image_weight=0.4, input_weight=0.6, alpha=1):
        self.image_weight = image_weight
        self.input_weight = input_weight
        self.alpha = alpha
        self.smoothed_intensity = None  # Merkt sich die geglättete Gesamtintensität
        print("intensity calc initialized")

    def calculate_total_intensity(self, image_intensity, input_intensity):
        # Setze fehlende Intensitäten auf 0
        if image_intensity is None:
            image_intensity = 0.0
        if input_intensity is None:
            input_intensity = 0.0

        # Stelle sicher, dass die Einzel-Intensitäten im Bereich [0,1] liegen
        image_intensity = min(max(image_intensity, 0.0), 1.0)
        input_intensity = min(max(input_intensity, 0.0), 1.0)

        # Berechne die gewichtete Gesamtintensität
        raw_intensity = (self.image_weight * image_intensity) + (self.input_weight * input_intensity)
        raw_intensity = min(max(raw_intensity, 0.0), 1.0)

        # Exponentielle Glättung ERST HIER auf dem Gesamtwert
        # Falls noch keine Vorwerte da sind, nimm den aktuellen als Start
        if self.smoothed_intensity is None:
            self.smoothed_intensity = raw_intensity
        else:
            self.smoothed_intensity = (
                self.alpha * raw_intensity
                + (1 - self.alpha) * self.smoothed_intensity
            )

        return self.smoothed_intensity

    def get_intensity_level(self, intensity, previous_intensity_level):
        """
        intensity = bereits geglättete Gesamtintensität
        """
        # Hier z. B. die Schwellwerte definieren.
        # Du könntest optional nochmal clampen, falls du auf Nummer sicher gehen willst.
        smoothed_intensity = min(max(intensity, 0.0), 1.0)

        if smoothed_intensity < 0.1:
            current_level = 1
        elif smoothed_intensity < 0.2:
            current_level = 2
        elif smoothed_intensity < 0.3:
            current_level = 3
        elif smoothed_intensity < 0.4:
            current_level = 4
        else:
            current_level = 5

        # Optional: Begrenzung der Sprünge
        # if previous_intensity_level is not None:
        #     if current_level > previous_intensity_level + 1:
        #         current_level = previous_intensity_level + 1
        #     elif current_level < previous_intensity_level - 1:
        #         current_level = previous_intensity_level - 1

        return current_level

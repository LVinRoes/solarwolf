class IntensityCalculator:
    def __init__(self, image_weight=0.4, input_weight=0.6,
                 alpha_up=0.1, alpha_down=0.5):
        """
        image_weight, input_weight: Gewichte für die eingehende Intensität (Bild / Input).
        alpha_up:   Glättungsfaktor, wenn Wert steigen soll (slow rise).
        alpha_down: Glättungsfaktor, wenn Wert fallen soll (fast fall).
        """
        self.image_weight = image_weight
        self.input_weight = input_weight

        # Glättungsfaktoren für Anstieg und Abfall
        self.alpha_up = alpha_up
        self.alpha_down = alpha_down

        self.smoothed_intensity = None

        print("IntensityCalculator initialized (mit getrennten alpha_up/down)")

    def calculate_total_intensity(self, image_intensity, input_intensity):
        # Fallback auf 0.0, wenn None
        if image_intensity is None:
            image_intensity = 0.0
        if input_intensity is None:
            input_intensity = 0.0

        # Clamping (0.0 bis 1.0)
        image_intensity = min(max(image_intensity, 0.0), 1.0)
        input_intensity = min(max(input_intensity, 0.0), 1.0)

        # 1) Rohwert berechnen (gewichtetes Mittel)
        raw_intensity = (self.image_weight * image_intensity) + \
                        (self.input_weight * input_intensity)
        raw_intensity = min(max(raw_intensity, 0.0), 1.0)

        # 2) Single Exponential Smoothing mit unterschiedlichen Faktoren
        if self.smoothed_intensity is None:
            # Beim ersten Durchlauf direkt übernehmen
            self.smoothed_intensity = raw_intensity
        else:
            if raw_intensity > self.smoothed_intensity:
                # Slow rise
                alpha = self.alpha_up
            else:
                # Fast fall
                alpha = self.alpha_down

            # Smoothing-Formel
            self.smoothed_intensity = alpha * raw_intensity + (1 - alpha) * self.smoothed_intensity

        return self.smoothed_intensity

    def get_intensity_level(self, intensity):
        """
        ... unverändert, oder leicht angepasst ...
        """
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

        return current_level

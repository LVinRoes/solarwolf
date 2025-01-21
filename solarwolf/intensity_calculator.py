# intensity_calculator.py
class IntensityCalculator:
    def __init__(self, image_weight=0.4, input_weight=0.6, alpha=0.3, beta=0.3):
        """
        image_weight, input_weight: Gewichte für die jeweils eingehende Intensität (Bild / Input).
        alpha, beta: Gewichte für exponentielle Glättung. Die Summe alpha + beta sollte <= 1 sein,
                     damit (1 - alpha - beta) nicht negativ wird.
        """
        self.image_weight = image_weight
        self.input_weight = input_weight

        # Damit nicht der dritte Faktor für den "zweiten Vorwert" negativ wird.
        if alpha + beta > 1:
            raise ValueError("alpha + beta sollte <= 1 sein, damit die Glättungsanteile Sinn ergeben.")
        self.alpha = alpha
        self.beta = beta

        # Anfangswerte für die geglättete Intensität
        self.smoothed_intensity = None
        self.smoothed_intensity_prev = None

        print("IntensityCalculator initialized")

    def calculate_total_intensity(self, image_intensity, input_intensity):
        # Fallback auf 0.0, wenn None
        if image_intensity is None:
            image_intensity = 0.0
        if input_intensity is None:
            input_intensity = 0.0

        # Clamping (0.0 bis 1.0)
        image_intensity = min(max(image_intensity, 0.0), 1.0)
        input_intensity = min(max(input_intensity, 0.0), 1.0)

        # Gewichtetes Mittel
        raw_intensity = (self.image_weight * image_intensity) + \
                        (self.input_weight * input_intensity)
        raw_intensity = min(max(raw_intensity, 0.0), 1.0)

        # Exponentielle Glättung mit Berücksichtigung der letzten beiden Werte
        if self.smoothed_intensity is None:
            # Beim ersten Durchlauf einfach direkt übernehmen
            self.smoothed_intensity = raw_intensity
            self.smoothed_intensity_prev = raw_intensity
        else:
            # Formel: smoothed_n = alpha*raw + beta*smoothed_(n-1) + (1 - alpha - beta)*smoothed_(n-2)
            new_smoothed_intensity = (
                self.alpha * raw_intensity +
                self.beta * self.smoothed_intensity +
                (1 - self.alpha - self.beta) * self.smoothed_intensity_prev
            )
            # Update der vorherigen Werte
            self.smoothed_intensity_prev = self.smoothed_intensity
            self.smoothed_intensity = new_smoothed_intensity

        return self.smoothed_intensity

    def get_intensity_level(self, intensity, previous_intensity_level=None):
        """
        intensity: bereits geglättete Gesamtintensität.
        previous_intensity_level: optionaler letzter Level,
                                  um Sprünge zu begrenzen (wenn gewünscht).
        """
        # Clamping (0.0 bis 1.0)
        smoothed_intensity = min(max(intensity, 0.0), 1.0)

        # Einfache Schwellenwerteinteilung
        if smoothed_intensity < 0.1:
            current_level = 1
        elif smoothed_intensity < 0.25:
            current_level = 2
        elif smoothed_intensity < 0.4:
            current_level = 3
        elif smoothed_intensity < 0.5:
            current_level = 4
        else:
            current_level = 5

        # Optional: Begrenzung der Sprünge (auskommentiert)
        # if previous_intensity_level is not None:
        #     # Beispiel: darf sich nur um 1 Level pro Schritt ändern
        #     if current_level > previous_intensity_level + 1:
        #         current_level = previous_intensity_level + 1
        #     elif current_level < previous_intensity_level - 1:
        #         current_level = previous_intensity_level - 1

        return current_level

# intensity_calculator.py
class IntensityCalculator:
    def __init__(self, image_weight=0.5, input_weight=0.5, alpha=0.7):
        self.image_weight = image_weight
        self.input_weight = input_weight
        self.alpha = alpha
        self.smoothed_intensity = None
        print("intensity calc initialized")

    def calculate_total_intensity(self, image_intensity, input_intensity):
        # Setze fehlende Intensitäten auf 0
        if image_intensity is None:
            image_intensity = 0.0
        if input_intensity is None:
            input_intensity = 0.0

        # Stelle sicher, dass die Intensitäten im Bereich [0,1] liegen
        image_intensity = min(max(image_intensity, 0.0), 1.0)
        input_intensity = min(max(input_intensity, 0.0), 1.0)

        # Berechne die gewichtete Gesamtintensität
        total_intensity = (self.image_weight * image_intensity) + (self.input_weight * input_intensity)

        # Da die Gewichte sich zu 1 summieren, sollte total_intensity im Bereich [0,1] liegen
        total_intensity = min(max(total_intensity, 0.0), 1.0)

        return total_intensity

    def get_intensity_level(self, intensity, previous_intensity_level):
        # Exponentielle Glättung
        self.smoothed_intensity = intensity
        

        smoothed_intensity = self.smoothed_intensity

        # Definiere die Schwellenwerte für Intensitätsstufen
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

        # Begrenze die Änderung der Intensitätsstufe
        # if previous_intensity_level is not None:
        #     if current_level > previous_intensity_level + 1:
        #         current_level = previous_intensity_level + 1
        #     elif current_level < previous_intensity_level - 1:
        #         current_level = previous_intensity_level - 1

        return current_level

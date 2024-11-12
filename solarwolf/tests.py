import unittest
from input_analyzer import InputAnalyzer
from main import calculate_intensity, get_intensity_level

class TestIntensityFunctions(unittest.TestCase):
    def test_calculate_intensity(self):
        # Testfall 1: Beide Intensitäten in der Mitte
        image_intensity = 0.5
        input_intensity = 0.5
        expected_total_intensity = 0.5
        total_intensity = calculate_intensity(image_intensity, input_intensity)
        self.assertAlmostEqual(total_intensity, expected_total_intensity)

        # Testfall 2: Maximale Intensitäten
        image_intensity = 1.0
        input_intensity = 1.0
        expected_total_intensity = 1.0
        total_intensity = calculate_intensity(image_intensity, input_intensity)
        self.assertAlmostEqual(total_intensity, expected_total_intensity)

        # Testfall 3: Minimale Intensitäten
        image_intensity = 0.0
        input_intensity = 0.0
        expected_total_intensity = 0.0
        total_intensity = calculate_intensity(image_intensity, input_intensity)
        self.assertAlmostEqual(total_intensity, expected_total_intensity)

    def test_get_intensity_level(self):
        # Testfall 1: Intensität 0.1 -> Stufe 1
        intensity = 0.1
        expected_level = 1
        level = get_intensity_level(intensity)
        self.assertEqual(level, expected_level)

        # Testfall 2: Intensität 0.35 -> Stufe 2
        intensity = 0.35
        expected_level = 2
        level = get_intensity_level(intensity)
        self.assertEqual(level, expected_level)

        # Testfall 3: Intensität 0.55 -> Stufe 3
        intensity = 0.55
        expected_level = 3
        level = get_intensity_level(intensity)
        self.assertEqual(level, expected_level)

        # Testfall 4: Intensität 0.75 -> Stufe 4
        intensity = 0.75
        expected_level = 4
        level = get_intensity_level(intensity)
        self.assertEqual(level, expected_level)

        # Testfall 5: Intensität 0.85 -> Stufe 5
        intensity = 0.85
        expected_level = 5
        level = get_intensity_level(intensity)
        self.assertEqual(level, expected_level)

if __name__ == '__main__':
    unittest.main()

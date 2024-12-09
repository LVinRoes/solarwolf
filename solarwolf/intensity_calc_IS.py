import game

class Intensity_calc_IS:
    def __init__(self, gameplay, max_intensity=100.0):
        """
        Initialisiert den Intensitäts-Rechner mit einer Referenz auf das aktuelle Gameplay-Objekt.
        
        Parameter:
        gameplay: Instanz der GamePlay-Klasse, aus welcher die aktuellen Spielzustände ausgelesen werden.
        max_intensity: Wert zur Normierung der berechneten Intensität auf [0,1].
        """
        self.gameplay = gameplay
        self.max_intensity = max_intensity
        self.smoothed_intensity = None  # Wird hier nicht exponentiell geglättet, aber für Interface-Kompatibilität vorgehalten

    def calculate_intensity(self):
        # Beispielhafte Gewichtungen:
        weight_shots = 1.5       # Jeder gegnerische Schuss erhöht die Intensität
        weight_guards = 2.0      # Jeder aktive Gegner ist relativ stark gewichtet
        weight_asteroids = 1.0   # Asteroiden erhöhen etwas die Intensität
        weight_powerups = -0.5   # Powerups verringern ggf. die gefühlte Intensität
        weight_time = -0.01      # Viel verbleibende Zeit senkt etwas die Intensität
        weight_turbo = 1.0       # Spieler im Turbo-Modus -> intensivere Situation
        weight_lives = -0.5      # Mehr Leben => geringere Intensität, daher negatives Gewicht pro Leben
        weight_shield = -2.0     # Ein aktiver Schild verringert stark die Intensität

        # Anzahl gegnerischer Schüsse
        num_shots = len(self.gameplay.shotobjs)
        # Aktive Gegner (Guards)
        num_guards = sum(1 for g in self.gameplay.guardobjs if not g.dead and g.killed == 0)
        # Asteroiden
        num_asteroids = len(self.gameplay.asteroidobjs)
        # Powerups
        num_powerups = len(self.gameplay.powerupobjs)
        # Verbleibende Zeit
        time_left = game.timeleft if hasattr(game, 'timeleft') else 500.0
        # Spieler-Turbo aktiv?
        turbo_active = 1 if self.gameplay.player.turbo else 0
        # Verbleibende Leben
        lives_left = self.gameplay.lives_left
        # Schild aktiv?
        shield_active = 1 if self.gameplay.player.shield else 0

        # Berechnung des Intensitätsscores:
        intensity_score = (num_shots * weight_shots +
                           num_guards * weight_guards +
                           num_asteroids * weight_asteroids +
                           num_powerups * weight_powerups +
                           time_left * weight_time +
                           turbo_active * weight_turbo +
                           lives_left * weight_lives +
                           shield_active * weight_shield)

        # Intensität soll nicht negativ werden:
        if intensity_score < 0:
            intensity_score = 0

        return intensity_score

    def calculate_total_intensity(self, image_intensity=None, input_intensity=None):
        """
        Berechnet die Gesamtintensität analog zu IntensityCalculator.
        Hier werden image_intensity und input_intensity ignoriert, da die Intensität aus internen Werten berechnet wird.
        """

        raw_intensity = self.calculate_intensity()

        # Normiere Intensität auf [0,1]
        normalized_intensity = raw_intensity / self.max_intensity
        if normalized_intensity > 1.0:
            normalized_intensity = 1.0
        if normalized_intensity < 0.0:
            normalized_intensity = 0.0

        return normalized_intensity

    def get_intensity_level(self, intensity, previous_intensity_level):
        # Diese Methode wird analog zum bestehenden IntensityCalculator gestaltet.
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

        return current_level

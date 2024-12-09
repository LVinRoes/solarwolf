import game

class Intensity_calc_IS:
    def __init__(self, gameplay):
        """
        Initialisiert den Intensitäts-Rechner mit einer Referenz auf das aktuelle Gameplay-Objekt.
        
        Parameter:
        gameplay: Instanz der GamePlay-Klasse, aus welcher die aktuellen Spielzustände ausgelesen werden.
        """
        self.gameplay = gameplay

    def calculate_intensity(self):
        # Beispielhafte Gewichtungen:
        weight_shots = 1.5       # Jeder gegnerische Schuss erhöht die Intensität
        weight_guards = 2.0      # Jeder aktive Gegner ist relativ stark gewichtet
        weight_asteroids = 1.0   # Asteroiden erhöhen etwas die Intensität
        weight_powerups = -0.5   # Powerups verringern ggf. die gefühlte Intensität (negatives Gewicht)
        weight_time = -0.01      # Viel verbleibende Zeit senkt etwas die Intensität
        weight_turbo = 1.0       # Spieler im Turbo-Modus -> intensivere Situation
        weight_lives = -0.5      # Wenige Leben -> höhere Intensität, daher negatives Gewicht für mehr Leben
        weight_shield = -2.0     # Ein aktiver Schild verringert stark die Intensität

        # Anzahl gegnerischer Schüsse
        num_shots = len(self.gameplay.shotobjs)
        # Aktive Gegner (Guards, die nicht getötet/entfernt wurden)
        num_guards = sum(1 for g in self.gameplay.guardobjs if not g.dead and g.killed == 0)
        # Asteroiden
        num_asteroids = len(self.gameplay.asteroidobjs)
        # Powerups
        num_powerups = len(self.gameplay.powerupobjs)
        # Verbleibende Zeit (je weniger, desto stressiger)
        time_left = game.timeleft if hasattr(game, 'timeleft') else 500.0  # Falls timeleft nicht gesetzt ist, Default
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

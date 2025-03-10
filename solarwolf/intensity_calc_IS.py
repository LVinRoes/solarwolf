import game
import math

class Intensity_calc_IS:
    def __init__(self, gameplay, max_intensity=100.0):
        self.gameplay = gameplay
        self.max_intensity = max_intensity
        self.smoothed_intensity = None

        self.num_shots = 0
        self.num_guards = 0
        self.num_asteroids = 0
        self.num_powerups = 0
        self.time_left = 0
        self.turbo_active = 0
        self.lives_left = 0
        self.shield_active = 0
        self.distance_to_nearest_projectile = 0
        self.distance_score = 0
        self.intensity_score = 0
        self.normalized_intensity = 0

    def calculate_intensity(self):
        weight_shots = 1.5
        weight_guards = 2.0
        weight_asteroids = 1.0
        weight_powerups = -0.5
        weight_time = -0.01
        weight_turbo = 1.0
        weight_lives = -0.5
        weight_shield = -2.0

        # Anzahl gegnerischer Schüsse
        self.num_shots = len(self.gameplay.shotobjs)
        # Aktive Gegner (Guards)
        self.num_guards = sum(1 for g in self.gameplay.guardobjs if not g.dead and g.killed == 0)
        # Asteroiden
        self.num_asteroids = len(self.gameplay.asteroidobjs)
        # Powerups
        self.num_powerups = len(self.gameplay.powerupobjs)
        # Verbleibende Zeit
        self.time_left = game.timeleft if hasattr(game, 'timeleft') else 500.0
        # Spieler-Turbo aktiv?
        self.turbo_active = 1 if self.gameplay.player.turbo else 0
        # Verbleibende Leben
        self.lives_left = self.gameplay.lives_left
        # Schild aktiv?
        self.shield_active = 1 if self.gameplay.player.shield else 0

        distance_to_nearest_projectile = float('inf')
        player_center = self.gameplay.player.rect.center

        for shot in self.gameplay.shotobjs:
            shot_center = shot.rect.center
            dx = shot_center[0] - player_center[0]
            dy = shot_center[1] - player_center[1]
            dist = math.hypot(dx, dy)
            if dist < distance_to_nearest_projectile:
                distance_to_nearest_projectile = dist

        if distance_to_nearest_projectile == float('inf'):
            distance_to_nearest_projectile = 9999.0

        intensity_score = (self.num_shots * weight_shots +
                           self.num_guards * weight_guards +
                           self.num_asteroids * weight_asteroids +
                           self.num_powerups * weight_powerups +
                           self.time_left * weight_time +
                           self.turbo_active * weight_turbo +
                           self.lives_left * weight_lives +
                           self.shield_active * weight_shield)

        if intensity_score < 0:
            intensity_score = 0

        max_relevant_distance = 300.0
        distance_factor = max(0, max_relevant_distance - distance_to_nearest_projectile) / max_relevant_distance
        weight_distance = 2.0
        distance_score = distance_factor * weight_distance

        #print(f"Distance Score: {distance_score}")
        # Gesamtscore erweitern
        intensity_score += distance_score



        #print(f"Intensity Score: {intensity_score}")
        return intensity_score

    def calculate_total_intensity(self, image_intensity=None, input_intensity=None):
        raw_intensity = self.calculate_intensity()

        normalized_intensity = raw_intensity / self.max_intensity
        if normalized_intensity > 1.0:
            normalized_intensity = 1.0
        if normalized_intensity < 0.0:
            normalized_intensity = 0.0

        #print(f"Normalized Intensity: {normalized_intensity}")
        return normalized_intensity

    def get_intensity_level(self, intensity, previous_intensity_level):
        self.smoothed_intensity = intensity
        smoothed_intensity = self.smoothed_intensity

        # Schwellenwerte
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

       #print(f"Current Intensity Level: {current_level}")
        return current_level

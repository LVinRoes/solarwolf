import random

class MelodyAgent:
    def __init__(self):
        # A-Moll-Pentatonik: A (69), C (72), D (74), E (76), G (79)
        self.scale = [69, 72, 74, 76, 79]

        # Vordefinierte Grundthemen für jede Intensität (8.0 Sekunden total)
        # Jede Melodie wird in vier Abschnitte (Maße) à 2.0 Sekunden aufgeteilt,
        # um gezielter einzelne Takte randomisieren zu können.
        self.intensity_melodies = {
            1: [
                (69, 2.0), (72, 2.0), (69, 2.0), (72, 2.0) # Sehr ruhig
            ],
            2: [
                (69,1.0),(72,1.0),(74,2.0),(72,1.0),(69,1.0),(74,2.0) # Etwas mehr Bewegung
            ],
            3: [
                (69,1.0),(72,0.5),(74,0.5),(76,1.0),(79,1.0),(76,1.0),(74,1.0),(72,2.0)
            ],
            4: [
                # 2x (A-C-D-E-G-E-D-C) mit je 4s
                (69,0.5),(72,0.5),(74,0.5),(76,0.5),(79,0.5),(76,0.5),(74,0.5),(72,0.5),
                (69,0.5),(72,0.5),(74,0.5),(76,0.5),(79,0.5),(76,0.5),(74,0.5),(72,0.5)
            ],
            5: [
                # Sehr lebhaftes Muster (A-C-D-E-G-G-E-D-C-A-C-D-E-G-E-C), alle 0.5s
                (69,0.5),(72,0.5),(74,0.5),(76,0.5),(79,0.5),(79,0.5),(76,0.5),(74,0.5),
                (72,0.5),(69,0.5),(72,0.5),(74,0.5),(76,0.5),(79,0.5),(76,0.5),(72,0.5)
            ]
        }

    def _split_into_measures(self, pattern, measure_length=2.0):
        """Teilt ein gegebenes Pattern (Liste aus (pitch, duration)) in Takte von measure_length Sek."""
        measures = []
        current_measure = []
        current_sum = 0.0
        for p, d in pattern:
            if current_sum + d == measure_length:
                current_measure.append((p, d))
                measures.append(current_measure)
                current_measure = []
                current_sum = 0.0
            elif current_sum + d < measure_length:
                current_measure.append((p, d))
                current_sum += d
            else:
                # Falls ein Event länger ist als noch im Takt übrig, splitten wir die Note (selten)
                # Um es einfach zu halten, vermeiden wir solche Fälle in vordefinierten Patterns.
                pass

        # Falls noch etwas übrig wäre (sollte nicht passieren, da die Patterns sauber aufgehen)
        if current_measure:
            measures.append(current_measure)

        return measures

    def _recombine_measures(self, measures):
        """Setzt die Takte wieder zu einem Pattern zusammen."""
        combined = []
        for m in measures:
            combined.extend(m)
        return combined

    def _randomize_measure(self, measure_length=2.0):
        """Erzeugt einen zufälligen Takt nur aus Pentatonik-Noten."""
        # Wir füllen measure_length mit zufälligen Noten und zufälligen Dauern,
        # sodass die Summe der Dauern genau measure_length beträgt.
        # Dauerwerte: 0.25, 0.5, 1.0 stehen zur Wahl.
        durations = [0.25, 0.5, 1.0]
        current_sum = 0.0
        measure = []
        while current_sum < measure_length - 0.25:  # wir brauchen mind. 0.25 Reserve
            d = random.choice(durations)
            if current_sum + d <= measure_length:
                p = random.choice(self.scale)
                measure.append((p, d))
                current_sum += d
        # Falls noch etwas Rest übrig ist, füge eine letzte Note mit der Restdauer hinzu
        rest = measure_length - current_sum
        if rest > 0:
            p = random.choice(self.scale)
            measure.append((p, rest))
        return measure

    def _slight_variation(self, measures, intensity_level):
        """Wendet kleine Abweichungen an den existierenden Takte an:
        - Mit einer gewissen Wahrscheinlichkeit werden einzelne Noten leicht in Pitch verändert.
        - Bei höherer Intensität: mehr Variationen.
        """
        variation_chance = 0.05 * intensity_level  # z.B. bei Intensität 5 -> 25% Chance pro Note
        for m in measures:
            for i, (p, d) in enumerate(m):
                if random.random() < variation_chance:
                    # Leichte pitch variation innerhalb der Scale
                    # Wir nehmen den ursprünglichen Pitch und suchen den nächsten oder vorherigen Skalenton
                    # um subtil die Tonhöhe zu verändern.
                    neighbors = [note for note in self.scale if abs(note - p) <= 5 and note != p]
                    if neighbors:
                        p_new = random.choice(neighbors)
                        m[i] = (p_new, d)
        return measures

    def generate_melody(self, intensity_level=3, total_duration=8.0, num_notes=16):
        # Hole das Grundpattern für diese Intensität
        base_pattern = self.intensity_melodies.get(intensity_level, self.intensity_melodies[3])

        # Teile die Melodie in 4 Takte à 2 Sekunden auf (8s total)
        measures = self._split_into_measures(base_pattern, measure_length=2.0)

        # Wahrscheinlichkeit, einen kompletten Takt zu randomisieren,
        # steigt mit der Intensität
        # z.B. Intensität 1: kaum Randomisierung
        # Intensität 5: etwa 50% Chance pro Takt
        randomize_chance = 0.1 * intensity_level  # Intensität 5 -> 0.5 = 50%

        for i, measure in enumerate(measures):
            if random.random() < randomize_chance:
                # Ersetze diesen Takt komplett durch random Noten
                measures[i] = self._randomize_measure(2.0)

        # Zusätzlich kleine Pitch-Variationen an den restlichen Takten
        measures = self._slight_variation(measures, intensity_level)

        final_pattern = self._recombine_measures(measures)

        pitches = [p for (p,d) in final_pattern]
        durations = [d for (p,d) in final_pattern]

        print("generate melody aufgerufen für Intensität:", intensity_level, "mit Randomisierung")
        return pitches, durations

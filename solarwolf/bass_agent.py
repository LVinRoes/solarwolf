import random

class BassAgent:
    def __init__(self):
        # A-Moll-Pentatonik in tiefen Lagen (A2 = 45, C3 = 48, D3 = 50, E3 = 52, G3 = 55)
        # Wir bewegen uns um A2 herum für den Grundton (A), um einen authentischen Bassbereich zu erzeugen.
        self.scale = [45, 48, 50, 52, 55]  # A, C, D, E, G in tiefen Lagen

        # Mappt unsere Akkordnamen auf deren Grundtöne im Bassbereich
        # Wir nehmen die Grundtöne etwa zwei Oktaven unterhalb der Drohne:
        # A=69 -> A-24=45, D=62 -> 62-24=38 (entspricht D2), F=65 -> 65-24=41 (F2), E=64-24=40 (E2), C=60-24=36 (C2)
        self.chord_roots = {
            "Am7": 45,    # A
            "Dm7": 38,    # D
            "Em7": 40,    # E
            "Fmaj7": 41,  # F
            "Cmaj7": 36   # C
        }

    def generate_bass_line(self, total_duration=8.0, intensity_level=3, current_chord="Am7"):
        # Bestimme den Grundton basierend auf dem aktuellen Akkord
        root = self.chord_roots.get(current_chord, 45)  # Fallback auf A, falls unbekannter Akkord

        # Anzahl der Noten abhängig von der Intensität
        # Weniger intensiv: weniger Noten, mehr Ruhe
        # Höher intensiv: mehr Noten, evtl. Fills
        # Beispiel: Bei Intensität 1 nur 2 Noten, bei Intensität 3 etwa 6 Noten, bei Intensität 5 etwa 10 Noten
        num_notes = int(2 * intensity_level)

        pitches = []
        durations = []

        remaining_duration = total_duration
        # Erlaubte Dauern: eher gleichmäßig oder leichte Variation
        duration_values = [0.5, 1.0] if intensity_level < 3 else [0.25, 0.5, 1.0]

        # Definiere Fills: bei höherer Intensität manchmal Quinte (E), Oktave (root+12), oder andere Pentatonik-Töne
        # Root = z.B. A2 = 45
        # Quinte über A = E, in tief = 45 + 7 HT = 52 (E3)
        # Oktave = root + 12 Halbtöne
        octave = root + 12

        # Weitere Skalentöne um kurze Läufe zu machen:
        # Da root in self.scale steckt, können wir benachbarte Skalentöne für Fills nutzen.
        # Filtere Töne der scale, die in der Nähe liegen:
        available_fills = [n for n in self.scale if abs(n - root) <= 10]

        for i in range(num_notes):
            if remaining_duration <= 0:
                break

            # Entscheide, ob wir Grundton oder Fill spielen:
            # Bei niedriger Intensität hauptsächlich Grundton
            # Bei mittlerer/höherer Intensität gelegentlich Fill
            if intensity_level <= 2:
                pitch = root
            else:
                # Bei höherer Intensität gelegentlich (z.B. 1/3 Chance) ein Fill anstatt Grundton
                if random.random() < 0.3:
                    # Wähle einen Fill-Ton aus den verfügbaren Skalentönen:
                    # Oder nimm Quinte/ Oktave zur Variation
                    fill_choices = [root, octave, 52] + available_fills
                    pitch = random.choice(fill_choices)
                else:
                    pitch = root

            # Dauer wählen, die noch reinpasst
            possible_durations = [d for d in duration_values if d <= remaining_duration]
            if not possible_durations:
                break
            duration = random.choice(possible_durations)

            pitches.append(pitch)
            durations.append(duration)

            remaining_duration -= duration

        # Falls noch Restdauer übrig ist, verlängere die letzte Note
        if remaining_duration > 0 and durations:
            durations[-1] += remaining_duration

        return pitches, durations

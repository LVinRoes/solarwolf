import random
from typing import List, Tuple

class RhythmAgent:
    def __init__(self):
        # MIDI-Notennummern für die jeweiligen Drums
        self.kick = 36         # Bass Drum
        self.snare = 38        # Snare Drum
        self.closed_hihat = 42
        self.open_hihat = 46
        self.ride = 51
        self.tom_low = 45
        self.tom_mid = 47
        self.tom_high = 50
        self.crash = 49

        # Definiert Drum-Pattern als Listen von Tupeln (Instrumente, Dauer) für verschiedene Intensitätsstufen.
        # Jedes Pattern summiert sich zu insgesamt 8 Beats.
        self.pattern_library: dict[int, List[List[Tuple[List[int], float]]]] = {
            1: [
                # Intensitätsstufe 1: Einfache, ruhige Patterns (8 Viertelnoten à 1 Beat)
                [([self.closed_hihat], 1.0) for _ in range(8)]
            ],
            2: [
                # Intensitätsstufe 2: Pattern mit Kick und Snare abwechselnd (8 Viertelnoten à 1 Beat)
                [
                    ([self.kick, self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([ self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0)   
                ]
            ],
            3: [
                # Intensitätsstufe 3: Achtelnoten-Pattern (16 Events à 0.5 Beat, insgesamt 8 Beats)
                [
                    ([self.closed_hihat, self.kick], 0.5),  # Down-Event: Closed Hi‑Hat + Kick
                    ([self.closed_hihat], 0.5),             # Off-Event: Closed Hi‑Hat
                    # Beat 2 (Beat 1, beat_in_measure = 1):
                    ([self.closed_hihat], 0.5),             # Down-Event: Closed Hi‑Hat
                    ([self.closed_hihat], 0.5),             # Off-Event: Closed Hi‑Hat
                    # Beat 3 (Beat 2, beat_in_measure = 2):
                    ([self.closed_hihat, self.kick], 0.5),  # Down-Event: Closed Hi‑Hat + Kick
                    ([self.closed_hihat], 0.5),             # Off-Event: Closed Hi‑Hat
                    # Beat 4 (Beat 3, beat_in_measure = 3):
                    ([self.closed_hihat], 0.5),             # Down-Event: Closed Hi‑Hat
                    ([self.closed_hihat], 0.5),             # Off-Event: Closed Hi‑Hat
                    # Beat 5 (Beat 4, beat_in_measure = 0):
                    ([self.closed_hihat, self.kick], 0.5),  # Down-Event: Closed Hi‑Hat + Kick
                    ([self.closed_hihat], 0.5),             # Off-Event: Closed Hi‑Hat
                    # Beat 6 (Beat 5, beat_in_measure = 1):
                    ([self.closed_hihat], 0.5),             # Down-Event: Closed Hi‑Hat
                    ([self.closed_hihat], 0.5),             # Off-Event: Closed Hi‑Hat
                    # Beat 7 (Beat 6, beat_in_measure = 2):
                    ([self.closed_hihat, self.kick], 0.5),  # Down-Event: Closed Hi‑Hat + Kick
                    ([self.closed_hihat], 0.5),             # Off-Event: Closed Hi‑Hat
                    # Beat 8 (Beat 7, beat_in_measure = 3):
                    ([self.closed_hihat], 0.5),             # Down-Event: Closed Hi‑Hat
                    ([self.closed_hihat], 0.5)              # Off-Event: Closed Hi‑Hat    
                ]
            ],
            4: [
                [
                ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),  # Down-Event: Closed Hi‑Hat + Kick + Extra Hi‑Hat
                ([self.closed_hihat], 0.5),                                # Off-Event: Closed Hi‑Hat
                # Beat 2 (Beat 1, beat_in_measure = 1):
                ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),   # Down-Event: Closed Hi‑Hat + Snare + Extra Hi‑Hat
                ([self.closed_hihat], 0.5),                                # Off-Event: Closed Hi‑Hat
                # Beat 3 (Beat 2, beat_in_measure = 2):
                ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),  # Down-Event: Closed Hi‑Hat + Kick + Extra Hi‑Hat
                ([self.closed_hihat], 0.5),                                # Off-Event: Closed Hi‑Hat
                # Beat 4 (Beat 3, beat_in_measure = 3):
                ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),   # Down-Event: Closed Hi‑Hat + Snare + Extra Hi‑Hat
                ([self.closed_hihat], 0.5),                                # Off-Event: Closed Hi‑Hat
                # Beat 5 (Beat 4, beat_in_measure = 0):
                ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),  # Down-Event: Closed Hi‑Hat + Kick + Extra Hi‑Hat
                ([self.closed_hihat], 0.5),                                # Off-Event: Closed Hi‑Hat
                # Beat 6 (Beat 5, beat_in_measure = 1):
                ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),   # Down-Event: Closed Hi‑Hat + Snare + Extra Hi‑Hat
                ([self.closed_hihat], 0.5),                                # Off-Event: Closed Hi‑Hat
                # Beat 7 (Beat 6, beat_in_measure = 2):
                ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),  # Down-Event: Closed Hi‑Hat + Kick + Extra Hi‑Hat
                ([self.closed_hihat], 0.5),                                # Off-Event: Closed Hi‑Hat
                # Beat 8 (Beat 7, beat_in_measure = 3):
                ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),   # Down-Event: Closed Hi‑Hat + Snare + Extra Hi‑Hat
                ([self.closed_hihat], 0.5)        
                ]                         # Off-Event: Closed Hi‑Hat
            ],
# Summe: 16 Events à 0.5 = 8 Beats.

            5: [
                # Intensitätsstufe 5: Sehr energiereiches Pattern mit zusätzlichen Variationen.
                # Auch hier wird das 4-Beat-Pattern verdoppelt.
                (
                    [
                        ([self.closed_hihat, self.kick, self.closed_hihat], 0.25),  # Sub 0: Down-Event
                        ([self.closed_hihat], 0.25),                                 # Sub 1
                        ([self.closed_hihat], 0.5),                                  # Sub 3
                        # Beat 2 (Beat 1, beat_in_measure = 1):
                        ([self.closed_hihat, self.snare, self.closed_hihat], 0.25),  # Sub 0: Down-Event
                        ([self.closed_hihat], 0.25),                                 # Sub 1
                        ([self.closed_hihat], 0.5),                                   # Sub 3
                        # Beat 3 (Beat 2, beat_in_measure = 2):
                        ([self.closed_hihat, self.kick, self.closed_hihat], 0.25),  # Sub 0: Down-Event
                        ([self.closed_hihat], 0.25),                                 # Sub 1
                        ([self.closed_hihat], 0.5),                                  # Sub 3
                        # Beat 4 (Beat 3, beat_in_measure = 3):
                        ([self.closed_hihat, self.snare, self.closed_hihat], 0.25),  # Sub 0: Down-Event
                        ([self.closed_hihat], 0.25),                                 # Sub 1
                        ([self.closed_hihat], 0.5),                                   # Sub 3
                        # Beat 5 (Beat 4, beat_in_measure = 0):
                        ([self.closed_hihat, self.kick, self.closed_hihat], 0.25),  # Sub 0: Down-Event
                        ([self.closed_hihat], 0.25),                                 # Sub 1
                        ([self.closed_hihat], 0.5),                                   # Sub 3
                        # Beat 6 (Beat 5, beat_in_measure = 1):
                        ([self.closed_hihat, self.snare, self.closed_hihat], 0.25),  # Sub 0: Down-Event
                        ([self.closed_hihat], 0.25),                                 # Sub 1
                        ([self.closed_hihat], 0.5),                                  # Sub 3
                        # Beat 7 (Beat 6, beat_in_measure = 2):
                        ([self.closed_hihat, self.kick, self.closed_hihat], 0.25),  # Sub 0: Down-Event
                        ([self.closed_hihat], 0.25),                                 # Sub 1
                        ([self.closed_hihat], 0.5),                                  # Sub 3
                        # Beat 8 (Beat 7, beat_in_measure = 3):
                        ([self.closed_hihat, self.snare, self.closed_hihat, self.crash], 0.25),  # Sub 0: Down-Event (Crash hinzu)
                        ([self.closed_hihat], 0.25),                                             # Sub 1
                        ([self.closed_hihat], 0.5),     
                    ]   # Verdopple das Pattern für 8 Beats
                )
            ]
        }

    def _slight_variation(self, pattern: List[Tuple[List[int], float]], intensity_level: int) -> List[Tuple[List[int], float]]:
        """
        Fügt dem Pattern leichte Variationen hinzu, z. B. den Austausch eines geschlossenen Hi‑Hat
        gegen einen offenen Hi‑Hat mit einer gewissen Wahrscheinlichkeit.
        """
        variation_chance = 0.01 * intensity_level
        new_pattern = []
        for instruments, duration in pattern:
            new_instruments = instruments.copy()
            if self.closed_hihat in new_instruments and random.random() < variation_chance:
                new_instruments = [self.open_hihat if inst == self.closed_hihat else inst for inst in new_instruments]
            new_pattern.append((new_instruments, duration))
        return new_pattern

    def generate_pattern(self, intensity_level: float) -> Tuple[float, List[Tuple[List[int], float]]]:
        """
        Wählt ein Drum-Pattern aus der Bibliothek basierend auf der Intensitätsstufe,
        wendet leichte Variationen an und gibt das Pattern als Liste von Tupeln (Instrumente, Dauer) zurück.
        Das resultierende Pattern summiert sich stets zu 8 Beats.
        """
        level = int(round(intensity_level))
        if level < 1:
            level = 1
        elif level > 5:
            level = 5

        if level not in self.pattern_library:
            level = 3

        pattern_candidates = self.pattern_library[level]
        pattern = random.choice(pattern_candidates)
        pattern = self._slight_variation(pattern, level)
        return intensity_level, pattern

# Beispielhafte Verwendung:
if __name__ == "__main__":
    agent = RhythmAgent()
    intensity = 3
    intensity, pattern = agent.generate_pattern(intensity)
    print("Intensity:", intensity)
    print("Pattern (insgesamt 8 Beats):")
    total_beats = sum(duration for (_, duration) in pattern)
    for instruments, duration in pattern:
        print("Instruments:", instruments, "Duration:", duration)
    print("Total Beats:", total_beats)

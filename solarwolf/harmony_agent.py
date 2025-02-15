import random
from typing import Dict, List, Tuple

class HarmonyAgent:
    def __init__(self) -> None:
        # Feste Akkordprogressionen pro Intensitätsstufe.
        # Jede Progression ist eine Liste von Akkorden (Name, Pitches, Dauer) mit insgesamt 8 Beats.
        self.intensity_chords: Dict[int, List[List[Tuple[str, List[int], float]]]] = {
            1: [
                [("Am", [65, 69, 72, 76], 4.0), ("Am7", [69, 72, 76, 79], 4.0)],
                [("Am7", [69, 72, 76, 79], 4.0), ("Am", [65, 72, 76], 4.0)]
            ],
            2: [
                [("Am7", [69, 72, 76], 4.0), ("Dm7", [62, 65, 69, 72], 4.0)],
                [("Dm7", [62, 65, 69, 72], 4.0), ("Am7", [69, 72, 76], 4.0)]
            ],
            3: [
                [("Fmaj7", [65, 69, 72, 76], 4.0), ("Dm7", [62, 65, 69, 72], 4.0)],
                [("Dm7", [62, 65, 69, 72], 4.0), ("Fmaj7", [65, 69, 72, 76], 4.0)],
                [("Fmaj7", [65, 69, 72, 76], 2.0), ("Dm7", [62, 65, 69, 72], 2.0), ("Em7", [57, 60, 64, 67], 4.0)]
            ],
            4: [
                [("Am7", [69, 72, 76], 3.0), ("Dm7", [64, 65, 69, 74], 1.0), ("Dm7", [62, 65, 69, 72], 4.0)],
                [("Dm7", [64, 65, 69, 74], 1.0), ("Am7", [69, 72, 76], 3.0), ("Dm7", [62, 65, 69, 72], 4.0)],
                [("Am7", [69, 72, 76], 2.0), ("Fmaj7", [65, 69, 72, 76], 2.0), ("Em7", [57, 60, 64, 67], 4.0)]
            ],
            5: [
                [("Am7", [57, 69, 72, 76], 3.0), ("Dm7", [64, 69, 74, 67], 1.0),
                 ("Dm7", [62, 65, 69, 72], 3.0), ("Em7", [57, 60, 64, 67], 1.0)],
                [("Em7", [57, 60, 64, 67], 1.0), ("Dm7", [64, 65, 69, 74], 1.0),
                 ("Am7", [57, 69, 72, 76], 3.0), ("Dm7", [62, 65, 69, 72], 3.0)],
                [("Am7", [57, 69, 72, 76], 2.0), ("Dm7", [64, 65, 69, 74], 2.0),
                 ("Fmaj7", [65, 69, 72, 76], 2.0), ("Em7", [57, 60, 64, 67], 2.0)]
            ]
        }

    def generate_progression(self, intensity: int, total_beats: float = 8.0) -> List[Tuple[str, List[int], float]]:
        """
        Gibt eine zufällig gewählte Akkordprogression zurück, die exakt total_beats (standardmäßig 8 Beats)
        dauert. Es werden ausschließlich feste Progressionen verwendet, die in self.intensity_chords definiert sind.
        """
        # Hole alle Progressionen für die gegebene Intensität – falls nicht vorhanden, nutze Intensität 1.
        progressions = self.intensity_chords.get(intensity, self.intensity_chords[1])
        progression = random.choice(progressions)
        
        # Überprüfe, ob die Progression exakt 8 Beats hat:
        total_duration = sum(chord[2] for chord in progression)
        if total_duration != total_beats:
            raise ValueError(f"Die gewählte Progression hat {total_duration} Beats, erwartet werden {total_beats} Beats.")
        
        return progression

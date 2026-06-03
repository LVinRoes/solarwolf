import random
from typing import Dict, List, Tuple

class HarmonyAgent:
    def __init__(self) -> None:
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
                [("Fmaj7", [69, 72], 4.0), ("Dm7", [ 65, 69], 4.0)],
                [("Dm7", [65, 69], 4.0), ("Fmaj7", [ 69, 72], 4.0)],
                [("Am", [65, 69], 4.0), ("Am7", [69, 72], 4.0)],
                [("Fmaj7", [ 69, 72], 2.0), ("Dm7", [ 65, 69], 2.0), ("Em7", [57, 60, 64, 67], 4.0)]
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
        Returns a randomly chosen chord progression that lasts exactly total_beats (default 8 beats).
        Only fixed progressions defined in self.intensity_chords are used.
        """
        
        progressions = self.intensity_chords.get(intensity, self.intensity_chords[1])
        progression = random.choice(progressions)
        
        # Check whether the progression has exactly 8 beats:
        total_duration = sum(chord[2] for chord in progression)
        if total_duration != total_beats:
            raise ValueError(f"The chosen progression has {total_duration} beats, expected {total_beats} beats.")
        
        return progression

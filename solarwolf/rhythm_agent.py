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
        self.cowbell = 56
        self.clap = 39
        self.woodblock = 75
        self.tambourine = 54
        self.tambourine2 = 55

        self.shaker = 70
        self.shaker2 = 69
        self.shaker3 = 74

        self.stick = 37

        self.pattern_library: dict[int, List[List[Tuple[List[int], float]]]] = {
            1: [
                [([self.closed_hihat], 1.0) for _ in range(8)]
            ],
            2: [
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
                [
                    ([self.kick, self.open_hihat], 1),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([self.kick, self.closed_hihat], 1),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat], 1.0),
                    ([self.closed_hihat, self.tom_mid], 1.0)   
                ]
            ],
            4: [
                [
                ([self.open_hihat, self.kick, self.closed_hihat], 0.5),   
                ([self.shaker], 0.5),   
                ([self.closed_hihat, self.closed_hihat], 0.5),   
                ([self.tambourine], 0.5),   
                
                ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),    
               
                ([self.shaker], 0.5),   
                ([self.closed_hihat, self.closed_hihat], 0.5),   
                ([self.tambourine], 0.5),   
                                            
                
                ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),       
               
                ([self.shaker], 0.5),  
                ([self.closed_hihat, self.closed_hihat], 0.5),   
                ([self.tambourine], 0.5),    
                                         
                
                ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),  
                ([self.shaker], 0.5),   
                ([self.closed_hihat, self.closed_hihat], 0.5),  
                
                ([self.tom_low ,self.shaker3],0.5)    
                       
                ]                         
            ],

            5: [
                (
                    [
                        ([self.open_hihat, self.kick, self.closed_hihat], 0.5), 
                                                       
                        ([self.closed_hihat], 0.5),              
                        ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),  
                                                      
                        ([self.closed_hihat], 0.5),                
                        ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),  
                                                       
                        ([self.closed_hihat], 0.5),               
                        ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),  
                        ([self.closed_hihat], 0.5),                   
                        ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),  
                        ([self.closed_hihat], 0.5),                         
                        ([self.closed_hihat, self.snare, self.closed_hihat], 0.5),  
                        ([self.closed_hihat], 0.5),                                
                        ([self.closed_hihat, self.kick, self.closed_hihat], 0.5),  
                        ([self.closed_hihat], 0.5),                                
                        ([self.closed_hihat, self.snare, self.closed_hihat, self.crash], 0.5),  
                                                                   
                        ([self.closed_hihat], 0.5),     
                    ]   
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

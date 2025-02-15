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

    def random_hihat(self) -> int:
        """
        Liefert mit 10% Wahrscheinlichkeit einen offenen Hi‑Hat zurück,
        ansonsten den geschlossenen Hi‑Hat – für subtile Variationen.
        """
        #return self.open_hihat if random.random() < 0.1 else self.closed_hihat
        return self.closed_hihat

    def generate_pattern(self, intensity_level: float) -> Tuple[float, Tuple[List[List[int]], List[float]]]:
        """
        Generiert ein Drum-Pattern für 2 Takte (8 Beats in 4/4) ...
        """
        # NEU: Falls die Intensität 1 oder kleiner ist, gib ein leeres Pattern zurück.
        
        beats_per_measure = 4
        total_measures = 2
        total_beats = beats_per_measure * total_measures  # 8 Beats insgesamt

        # Berechne den linearen Faktor f (0 bis 1)
        f = max(0.0, min(1.0, (intensity_level - 2) / 3.0))

        # Wähle die Unterteilung in Abhängigkeit vom intensity_level:
        if intensity_level <= 2.0:
            subdivision = 1.0   # Viertelnoten
            spb = 1             # Subdivisions per beat
        elif intensity_level <= 4.0:
            subdivision = 0.5   # Achtelnoten
            spb = 2
        else:
            subdivision = 0.25  # Sechzehntelnoten
            spb = 4

        pattern_pitches: List[List[int]] = []
        pattern_durations: List[float] = []

        # (Der restliche Code bleibt unverändert ...)
        if spb == 1:
            # Viertelnoten-Modus
            for beat in range(total_beats):
                beat_in_measure = beat % beats_per_measure
                instruments = [self.random_hihat()]
                if beat_in_measure in (0, 2) and f >= 0.33:
                    instruments.append(self.kick)
                    if random.random() < 0.1:
                        instruments.append(self.tom_low)
                if beat_in_measure in (1, 3) and f >= 0.5:
                    instruments.append(self.snare)
                    if random.random() < 0.1:
                        instruments.append(self.tom_mid)
                if f >= 0.66:
                    instruments.append(self.random_hihat())
                if beat == total_beats - 1 and f >= 0.8:
                    instruments.append(self.crash)
                if random.random() < 0.05:
                    instruments.append(self.random_hihat())
                pattern_pitches.append(instruments)
                pattern_durations.append(subdivision)
        elif spb == 2:
            # Achtelnoten-Modus
            for beat in range(total_beats):
                beat_in_measure = beat % beats_per_measure
                instruments_down = [self.random_hihat()]
                if beat_in_measure in (0, 2) and f >= 0.33:
                    instruments_down.append(self.kick)
                    if random.random() < 0.1:
                        instruments_down.append(self.tom_low)
                if beat_in_measure in (1, 3) and f >= 0.5:
                    instruments_down.append(self.snare)
                    if random.random() < 0.1:
                        instruments_down.append(self.tom_mid)
                if f >= 0.66:
                    instruments_down.append(self.random_hihat())
                if beat == total_beats - 1 and f >= 0.8:
                    instruments_down.append(self.crash)
                if random.random() < 0.05:
                    instruments_down.append(self.random_hihat())
                pattern_pitches.append(instruments_down)
                pattern_durations.append(subdivision)

                instruments_off = [self.random_hihat()]
                if random.random() < 0.15:
                    instruments_off = [self.open_hihat]
                if f >= 0.5 and random.random() < 0.1:
                    instruments_off.append(self.random_hihat())
                pattern_pitches.append(instruments_off)
                pattern_durations.append(subdivision)
        else:
            # Sechzehntelnoten-Modus
            for beat in range(total_beats):
                beat_in_measure = beat % beats_per_measure
                for sub in range(4):
                    instruments = []
                    if sub == 0:
                        instruments.append(self.random_hihat())
                        if beat_in_measure in (0, 2) and f >= 0.33:
                            instruments.append(self.kick)
                            if random.random() < 0.1:
                                instruments.append(self.tom_low)
                        if beat_in_measure in (1, 3) and f >= 0.5:
                            instruments.append(self.snare)
                            if random.random() < 0.1:
                                instruments.append(self.tom_mid)
                        if f >= 0.66:
                            instruments.append(self.random_hihat())
                        if beat == total_beats - 1 and f >= 0.8:
                            instruments.append(self.crash)
                    else:
                        instruments.append(self.random_hihat())
                        if random.random() < 0.05:
                            instruments.append(self.tom_high)
                    pattern_pitches.append(instruments)
                    pattern_durations.append(subdivision)

        return intensity_level, (pattern_pitches, pattern_durations)

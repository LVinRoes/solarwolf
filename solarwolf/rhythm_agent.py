import random

class RhythmAgent:
    def __init__(self):
        self.kick = 36  # Bass Drum
        self.snare = 38  # Snare Drum
        self.closed_hihat = 42  # Closed Hi-hat
        self.open_hihat = 46  # Open Hi-hat
        self.ride = 51  # Ride Cymbal
        self.tom_low = 45  # Low Tom
        self.tom_mid = 47  # Mid Tom
        self.tom_high = 50  # High Tom

        self.crash = 49  # Crash Cymbal

    def generate_pattern(self, intensity_level):
        """
        Generiert immer 2 Takte (8 Schläge bei 4/4), basierend auf dem Intensitätslevel.
        Nutzt ggf. Füller-Events, sodass die Gesamtdauer immer 8 beträgt.
        :param intensity_level: Wert zwischen 1 und 5
        :return: Tuple aus Listen von pitches und durations, wobei pitches jetzt Listen von MIDI-Noten
                 darstellen (für einen Akkord). Falls kein Instrument erklingt, wird eine leere Liste
                 eingefügt. durations enthält für jede Subdivision genau eine Dauer, sodass die Summe der
                 durations immer 8.0 ergibt.
        """
        pattern_pitches = []
        pattern_durations = []

        beats_per_measure = 4
        total_measures = 2
        total_duration = beats_per_measure * total_measures  

        if intensity_level <= 1:
            subdivision = 1.0  # Viertelnoten
        elif intensity_level <= 2 and intensity_level > 1:
            subdivision = 0.5  # Achtelnoten
        elif intensity_level <= 3 and intensity_level > 2:
            subdivision = 0.5  # Achtelnoten, aber mit mehr Instrumenten
        elif intensity_level <= 4 and intensity_level > 3:
            subdivision = 0.25 # Sechzehntelnoten
        elif intensity_level <= 5 and intensity_level > 4:
            subdivision = 0.25 # Sechzehntelnoten mit mehr Instrumenten
        else:
            subdivision = 1.0  # Standardmäßig Viertelnoten

        # Berechne die Anzahl der Subdivisions
        num_subdivisions = int(total_duration / subdivision)

        for i in range(num_subdivisions):
            instruments = []

            # Logik zur Generierung des Patterns basierend auf dem Intensitätslevel
            if intensity_level <= 1:
                # Kick auf jeder Viertelnote
                current_beat = (i * subdivision) % beats_per_measure
                if current_beat == 0.0:
                    instruments.append(self.kick)
                elif current_beat == 4.0:
                    instruments.append(self.snare)

            elif intensity_level <= 2 and intensity_level > 1:
                # Kick auf Beat 1 (current_beat=0.0) und Snare auf Beat 3 (current_beat=2.0)
                current_beat = (i * subdivision) % beats_per_measure
                if current_beat == 0.0:
                    instruments.append(self.kick)
                elif current_beat == 2.0:
                    instruments.append(self.snare)

            elif intensity_level <= 3 and intensity_level > 2:
                # Hi-Hat auf jedem Achtel, Kick auf Beat 1, Snare auf Beat 3
                current_beat = (i * subdivision) % beats_per_measure
                instruments.append(self.closed_hihat)
                if current_beat == 0.0:
                    instruments.append(self.kick)
                elif current_beat == 2.0:
                    instruments.append(self.snare)

            elif intensity_level <= 4 and intensity_level > 3:
                # Hi-Hat auf jeder 16tel, Kick alle 4 (1 Beat), Snare auf dem Offbeat (i % 8 == 4)
                instruments.append(self.closed_hihat)
                if i % 4 == 0:
                    instruments.append(self.kick)
                if i % 8 == 4:
                    instruments.append(self.snare)

            elif intensity_level <= 5 and intensity_level > 4:
                # Wechselnde Hi-Hats, Kick und Snare wie oben, plus Tom und Crash
                if i % 3 == 0:
                    instruments.append(self.closed_hihat)
                else:
                    instruments.append(self.open_hihat)
                if i % 8 == 0:
                    instruments.append(self.kick)
                if i % 8 == 4:
                    instruments.append(self.snare)
                if i % 16 == 8:
                    instruments.append(self.tom_mid)
                if i == 0:
                    instruments.append(self.crash)
            pattern_pitches.append(instruments) 
            pattern_durations.append(subdivision)

        return pattern_pitches, pattern_durations

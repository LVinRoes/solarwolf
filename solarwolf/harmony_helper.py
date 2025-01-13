class HarmonyHelper:
    def __init__(self):
        
        self.a_minor_full_range = []
        a_minor_pitch_classes = {0, 2, 4, 5, 7, 9, 11}  

        for note in range(21, 109):  
            if note % 12 in a_minor_pitch_classes:
                self.a_minor_full_range.append(note)


    def get_chord(self, chord_name):
        return self.chords.get(chord_name, [])

    def transpose(self, pitches, semitones):
        return [p + semitones for p in pitches]

    def get_third_above_in_scale(self, pitch):
        
        nearest_pitch = min(self.a_minor_full_range, key=lambda p: abs(p - pitch))
        
        idx = self.a_minor_full_range.index(nearest_pitch)
        
        new_idx = idx + 2
        if new_idx >= len(self.a_minor_full_range):
            new_idx = len(self.a_minor_full_range) - 1
        
        return self.a_minor_full_range[new_idx]

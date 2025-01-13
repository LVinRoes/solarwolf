class HarmonyHelper:
    """
    Diese Klasse verwaltet grundlegende Skalen, Akkorde und Transpositionsfunktionen
    für eine bestimmte Tonart.
    """
    def __init__(self):
        
        self.a_minor_scale = [69, 71, 72, 74, 76, 77, 79]  
        
        self.chords = {
            "Am":   [69, 72, 76],       # A, C, E
            "Am7":  [69, 72, 76, 79],   # A, C, E, G
            "Cmaj": [60, 64, 67],       # C, E, G 
            "E7":   [64, 68, 71, 76],   # E, G#, B, D
            "Dm":   [62, 65, 69],       # D, F, A 
            
        }

    def get_chord(self, chord_name):
        """Liefert die MIDI-Pitches zu einem Akkordnamen, wenn vorhanden."""
        return self.chords.get(chord_name, [])

    def transpose(self, pitches, semitones):
        """
        Transponiert eine Liste von MIDI-Pitches um einen
        bestimmten Wert in Halbtönen.
        """
        return [p + semitones for p in pitches]

    def get_third_above_in_scale(self, pitch):
        """
        Beispiel-Funktion, die einen Ton `pitch` in A-Moll um 'eine Terz oben' 
        transponiert, aber nur in der Skala bleibt. (Sehr einfach gehalten.)
        """
        if pitch not in self.a_minor_scale:
            
            nearest_pitch = min(self.a_minor_scale, key=lambda p: abs(p - pitch))
            idx = self.a_minor_scale.index(nearest_pitch)
        else:
            idx = self.a_minor_scale.index(pitch)
        
        idx_third = (idx + 2) % len(self.a_minor_scale) 
        pitch_third = self.a_minor_scale[idx_third]
        return pitch_third

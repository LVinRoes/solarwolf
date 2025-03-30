import random

class BassAgent:
    def __init__(self):
        # Definierte Skala (Grundtöne: A, C, D, E, G)
        self.scale = [45, 48, 50, 52, 55]
        # Zuordnung von Akkordnamen zu ihren Grundtönen
        self.chord_roots = {
            "Am7":   45,  # A2
            "Dm7":   38,  # D2
            "Em7":   40,  # E2
            "Fmaj7": 41,  # F2
            "Cmaj7": 36   # C2
        }

    def generate_bass_line_for_progression(self, progression, intensity_level=3):
        """
        Erzeugt eine Basslinie für eine Akkord-Progression.
        
        Jedes Element in 'progression' ist ein Tupel:
            (chord_name, chord_pitches, chord_len)
        
        Bei niedriger Intensität oder kurzen Akkorden wird nur der Grundton gespielt.
        Bei höherer Intensität wird der Akkordabschnitt in zwei Phasen geteilt:
            1. Eine längere Phase, in der der Grundton gehalten wird.
            2. Eine kurze Phase, in der ein passender Ton aus der Skala als
               "Passing Tone" in Richtung der nächsten Akkordwurzel gespielt wird.
        """
        all_pitches = []
        all_durations = []
        
        for i, (chord_name, chord_pitches, chord_len) in enumerate(progression):
            current_root = self.chord_roots.get(chord_name, 45)
            
            # Bei niedriger Intensität oder wenn der Akkord zu kurz ist, wird nur der Grundton gespielt.
            if intensity_level <= 2 or chord_len < 1.0:
                all_pitches.append(current_root)
                all_durations.append(chord_len)
            else:
                # Unterteile den Akkordabschnitt in zwei Teile:
                first_duration = chord_len * 0.75  # längere Phase mit Grundton
                second_duration = chord_len - first_duration  # kurze Phase als Übergang
                
                all_pitches.append(current_root)
                all_durations.append(first_duration)
                
                # Bestimme den Zielgrundton des nächsten Akkords (falls vorhanden)
                if i < len(progression) - 1:
                    next_chord = progression[i+1]
                    next_root = self.chord_roots.get(next_chord[0], current_root)
                    passing_tone = self._choose_passing_tone(current_root, next_root)
                else:
                    passing_tone = current_root
                
                all_pitches.append(passing_tone)
                all_durations.append(second_duration)
        
        return all_pitches, all_durations

    def _choose_passing_tone(self, current, next_root):
        """
        Wählt einen passenden "Passing Tone" aus der definierten Skala.
        - Ist next_root größer als current, wird der nächsthöhere Ton in der Skala gewählt.
        - Ist next_root kleiner, der nächsttiefere.
        - Bei gleicher Wurzel oder fehlender Option wird current zurückgegeben.
        """
        sorted_scale = sorted(self.scale)
        if current not in sorted_scale:
            return current
        idx = sorted_scale.index(current)
        if next_root > current:
            if idx < len(sorted_scale) - 1:
                return sorted_scale[idx + 1]
        elif next_root < current:
            if idx > 0:
                return sorted_scale[idx - 1]
        return current

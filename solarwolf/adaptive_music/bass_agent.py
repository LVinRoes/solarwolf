import random

class BassAgent:
    def __init__(self):
        # Defined scale (root notes: A, C, D, E, G)
        self.scale = [45, 48, 50, 52, 55]
        # Mapping of chord names to their root notes
        self.chord_roots = {
            "Am7":   45,  # A2
            "Dm7":   38,  # D2
            "Em7":   40,  # E2
            "Fmaj7": 41,  # F2
            "Cmaj7": 36   # C2
        }

    def generate_bass_line_for_progression(self, progression, intensity_level=3):
        """
        Generates a bass line for a chord progression.
        
        Each element in 'progression' is a tuple:
            (chord_name, chord_pitches, chord_len)
        
        At low intensity or for short chords, only the root note is played.
        At higher intensity, the chord section is split into two phases:
            1. A longer phase where the root note is held.
            2. A short phase where a matching note from the scale is played as
               a passing tone toward the next chord root.
        """
        all_pitches = []
        all_durations = []
        
        for i, (chord_name, chord_pitches, chord_len) in enumerate(progression):
            current_root = self.chord_roots.get(chord_name, 45)
            
            # At low intensity or if the chord is too short, only the root note is played.
            if intensity_level <= 2 or chord_len < 1.0:
                all_pitches.append(current_root)
                all_durations.append(chord_len)
            else:
                # Split the chord section into two parts:
                first_duration = chord_len * 0.75  # longer phase with root note
                second_duration = chord_len - first_duration  # short transition phase
                
                all_pitches.append(current_root)
                all_durations.append(first_duration)
                
                # Determine the target root note of the next chord (if available)
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
        Selects a suitable passing tone from the defined scale.
        - If next_root is greater than current, the next higher note in the scale is chosen.
        - If next_root is smaller, the next lower note is chosen.
        - If the roots are equal or no option is available, current is returned.
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

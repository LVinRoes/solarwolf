import random

class BassAgent:
    def __init__(self):
        
        self.scale = [45, 48, 50, 52, 55]  # A, C, D, E, G

        
        self.chord_roots = {
            "Am7":   45,    # A2
            "Dm7":   38,    # D2
            "Em7":   40,    # E2
            "Fmaj7": 41,    # F2
            "Cmaj7": 36     # C2
        }

    def generate_bass_line_for_progression(
        self, 
        progression,       
        intensity_level=3
    ):
        """
        Nimmt eine komplette Akkord-Progression entgegen (z.B. 8s mit mehreren Akkorden)
        und erstellt eine EINZIGE Bass-Linie als (pitches, durations).
        
        Jeder Akkord hat: (chord_name, chord_pitches, chord_len)
          - chord_name: z.B. "Am7"
          - chord_pitches: unused here, aber existiert
          - chord_len: z.B. 3.0 (Sekunden)
        
        Innerhalb eines Akkord-Abschnitts wenden wir wahlweise die Pedal-Note-Logik an 
        oder erzeugen "normale" Bass-Passagen. Zwischen den Akkorden fügen wir 
        Passing Tones ein, um zum nächsten Root zu leiten.
        """
        all_pitches = []
        all_durations = []
        
        
        for i, (chord_name, chord_pitches, chord_len) in enumerate(progression):
            
            root_current = self.chord_roots.get(chord_name, 45)
            
            
            if i < len(progression) - 1:
                next_chord_name = progression[i + 1][0]
                root_next = self.chord_roots.get(next_chord_name, root_current)
            else:
                
                next_chord_name = chord_name
                root_next = root_current

            
            pedal_chance = 0.20
            if random.random() < pedal_chance and chord_len >= 2.0:
                
                all_pitches.append(root_current)
                all_durations.append(chord_len)
            else:
                
                sub_pitches, sub_durations = self._generate_bass_fragment(
                    total_duration=chord_len,
                    intensity_level=intensity_level,
                    root_current=root_current,
                    root_next=root_next
                )
                all_pitches.extend(sub_pitches)
                all_durations.extend(sub_durations)

        return (all_pitches, all_durations)

    def _generate_bass_fragment(
        self,
        total_duration,
        intensity_level,
        root_current,
        root_next
    ):
        """
        Erzeugt einen "normalen" Bass-Abschnitt (ohne Pedal) für 'total_duration' Sekunden
        und versucht am Ende ggf. Passing Tones Richtung 'root_next'.
        
        Ähnlich wie deine vorherige _generate_bass_fragment(), 
        nur ohne 'num_notes' fest. Wir bauen es eher 'zeitlich' auf.
        """
        
        if intensity_level < 3:
            duration_values = [0.5, 1.0]
            num_notes = int(2 * intensity_level)  
        else:
            duration_values = [0.25, 0.5, 1.0]
            num_notes = int(2 * intensity_level)  

        pitches = []
        durations = []
        remaining_duration = total_duration

        def get_passing_tones(start_note, end_note):
            passing_sequence = []
            step = 1 if end_note > start_note else -1
            current = start_note
            while current != end_note:
                current += step
                if current in self.scale:
                    passing_sequence.append(current)
                if abs(current - end_note) <= 1:
                    break
            return passing_sequence

        for i in range(num_notes):
            if remaining_duration <= 0:
                break

            if i == num_notes - 2:
                passing_seq = get_passing_tones(root_current, root_next)
                if passing_seq:
                    pitch = random.choice(passing_seq)
                else:
                    pitch = root_current
            elif i == num_notes - 1:
                
                pitch = root_next
            else:
                if intensity_level <= 2:
                    pitch = root_current
                else:
                    if random.random() < 0.3:
                        fill_choices = [root_current, root_current+12, 52]
                        pitch = random.choice(fill_choices)
                    else:
                        pitch = root_current

           
            possible_durations = [d for d in duration_values if d <= remaining_duration]
            if not possible_durations:
                break
            chosen_duration = random.choice(possible_durations)

            pitches.append(pitch)
            durations.append(chosen_duration)
            remaining_duration -= chosen_duration
        
        if remaining_duration > 0 and len(durations) > 0:
            durations[-1] += remaining_duration

        return pitches, durations

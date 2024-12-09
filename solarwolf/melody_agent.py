import random

class MelodyAgent:
    def __init__(self):
        # Definiere die A-Moll-Pentatonik in MIDI-Notennummern (Mittleres C = 60)
        self.scale = self._create_scale()

    def _create_scale(self):
        # Intervalle der A-Moll-Pentatonik: 0, 3, 5, 7, 10 Halbtöne über Grundton A
        intervals = [0, 3, 5, 7, 10]
        scale_notes = []
        # Verwende Oktaven von A3 bis A5
        for octave in range(3, 6):
            base_note = 57 + 12 * (octave - 3)  # A3 hat die MIDI-Nummer 57
            for interval in intervals:
                note = base_note + interval
                scale_notes.append(note)
        return scale_notes

    def generate_melody(self, total_duration=8.0, num_notes=16):
        pitches = []
        durations = []
        duration_values = [0.25, 0.5, 1.0, 2.0]
        remaining_duration = total_duration
        for _ in range(num_notes):
            pitch = random.choice(self.scale)
            # Wähle mögliche Dauern, die in die verbleibende Dauer passen
            possible_durations = [d for d in duration_values if d <= remaining_duration]
            if not possible_durations:
                break
            duration = random.choice(possible_durations)
            pitches.append(pitch)
            durations.append(duration)
            remaining_duration -= duration
            if remaining_duration <= 0:
                break
        # Falls noch Restdauer übrig ist, passe die letzte Note an
        if remaining_duration > 0 and durations:
            durations[-1] += remaining_duration
        print("generate melody aufgerufen")
        return pitches, durations

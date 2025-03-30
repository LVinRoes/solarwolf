from music21 import stream, note

def create_score_from_melody(pitches, durations):
    """
    Erstellt einen music21-Stream aus den übergebenen Listen von MIDI-Pitches und Dauern.
    """
    s = stream.Stream()
    for p, d in zip(pitches, durations):
        n = note.Note()         # Erzeuge ein leeres Note-Objekt
        n.pitch.midi = p        # Setze den MIDI-Wert (z.B. 69 entspricht A4)
        n.quarterLength = d     # Setze die Notendauer (angenommen: 1.0 = Viertelnote)
        s.append(n)
    return s

# Beispielhafte Melodiedaten, die z.B. vom MelodyAgent zurückgegeben werden
pitches = [69, 72, 69, 67, 69, 72, 74, 76]
durations = [1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0]

# Erstelle die Partitur
score = create_score_from_melody(pitches, durations)

# Speichere die Partitur als PNG-Datei; dies nutzt LilyPond zur Renderung
score.write('lily.png', fp='melody_score.png')

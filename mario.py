from scamp import Session

def play_melody(pitches, durations):
    for pitch, duration in zip(pitches, durations):
        oboe.play_note(pitch, 1, duration)

def play_bass():
    bass.play_note(40, 2, 1)

def play_tetris_theme():
    play_melody(tetris_pitches, tetris_durations)

s = Session(tempo=80)

tetris_pitches = [67, 66, 64, 62, 64, 64]
tetris_durations = [1, 1, 1, 1, 0.5, 0.5]

oboe = s.new_part("Oboe")
bass = s.new_part("bass")

# Übergib die Funktionen direkt, da sie keine Parameter haben
s.fork(play_bass)
s.fork(play_tetris_theme)

# Warte 10 Sekunden, damit alle Noten gespielt werden
s.wait_for_children_to_finish()
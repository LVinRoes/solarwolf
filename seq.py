import matplotlib.pyplot as plt
import numpy as np

# Beispiel-Daten, wie bei dir im Code
# Key = Intensität (z.B. 5 oder 2),
# Value = Liste von Patterns,
#         wo ein Pattern eine Liste von Steps ist,
#         und jeder Step ist ([Instrumente], Dauer).
drum_patterns = {
    5: [  # Hier nur 1 Pattern
        (
            [
                (["open_hihat", "kick"], 0.5), 
                (["closed_hihat"], 0.5), 
                (["closed_hihat", "snare"], 0.5),
                (["closed_hihat"], 0.5),
                (["closed_hihat", "kick"], 0.5),
                (["closed_hihat"], 0.5),
                (["closed_hihat", "snare"], 0.5),
                (["closed_hihat"], 0.5),
                (["closed_hihat", "kick"], 0.5),
                (["closed_hihat"], 0.5),
                (["closed_hihat", "snare"], 0.5),
                (["closed_hihat"], 0.5),
                (["closed_hihat", "kick"], 0.5),
                (["closed_hihat"], 0.5),
                (["closed_hihat", "snare", "crash"], 0.5),
                (["closed_hihat"], 0.5),
            ]
        )
    ],
    2: [  # Hier nur 1 Pattern
        [
            (["kick", "closed_hihat"], 1.0),
            (["closed_hihat"], 1.0),
            (["closed_hihat"], 1.0),
            (["closed_hihat"], 1.0),
            (["closed_hihat"], 1.0),
            (["closed_hihat"], 1.0),
            (["closed_hihat"], 1.0),
            (["closed_hihat"], 1.0),
        ]
    ]
}

def visualize_drum_pattern(drum_patterns, intensity):
    """
    Zeigt das erste Pattern für die gegebene Intensität
    als Grid an (Zeilen=Instrumente, Spalten=Steps).
    """
    if intensity not in drum_patterns:
        print(f"Keine Patterns für Intensität {intensity} gefunden.")
        return

    # Hole das erste Pattern
    pattern = drum_patterns[intensity][0]
    
    # pattern kann entweder eine Liste von Steps ODER ein einzelnes Tupel sein.
    # Du hast teils "(" und teils "[" in deinen Beispielen verwendet.
    # Wir normalisieren das hier mal:
    if isinstance(pattern, tuple):
        # Falls pattern ein einziges Tupel ist: pattern = ( [ (instruments, dur), ... ] )
        steps = pattern[0]
    else:
        # Falls pattern direkt die Liste von Steps ist
        steps = pattern

    # Sammle alle Instrument-Namen
    instrument_set = set()
    for (instr_list, dur) in steps:
        for instr in instr_list:
            instrument_set.add(instr)
    instrument_list = sorted(list(instrument_set))

    # Wir erstellen eine Liste der Step-Längen (z.B. 0.5 oder 1.0)
    # und wandeln sie in "Spalten" um.
    # In diesem Beispiel addieren wir einfach die Dauer auf, um die Spaltenindexe zu bekommen.
    time_positions = []
    current_time = 0.0
    for (instr_list, dur) in steps:
        time_positions.append((current_time, instr_list, dur))
        current_time += dur

    # Wir bauen eine 2D-Matrix: rows = len(instrument_list), cols = anzahl steps (nach Summation)
    # Hier ist es etwas tricky, weil du variable Dauer hast (0.5 oder 1.0).
    # Für eine einfache Darstellung tun wir so, als wäre 0.5 = 1 Takt-Einheit, 1.0 = 2 Takt-Einheiten usw.
    
    # 1. Finde die Gesamtanzahl an Takt-Einheiten
    total_units = 0
    for (instr_list, dur) in steps:
        # z.B. 0.5 => 1 Einheit, 1.0 => 2 Einheiten
        total_units += int(dur / 0.5)

    # Leere Matrix anlegen: 0 = kein Schlag, 1 = Schlag
    matrix = np.zeros((len(instrument_list), total_units))

    # Fülle die Matrix
    col_index = 0
    for (instr_list, dur) in steps:
        # Wandle dur in Step-Einheiten um
        step_units = int(dur / 0.5)
        for u in range(step_units):
            for instr in instr_list:
                row = instrument_list.index(instr)
                matrix[row, col_index + u] = 1
        col_index += step_units

    # Visualisierung mit Matplotlib
    fig, ax = plt.subplots(figsize=(8, 3))
    cax = ax.imshow(matrix, aspect="auto", cmap="Greys", origin="lower")
    # Y-Achse = Instrumente
    ax.set_yticks(range(len(instrument_list)))
    ax.set_yticklabels(instrument_list)
    # X-Achse = Step-Einheiten
    ax.set_xticks(range(total_units))
    ax.set_xlabel("Step-Einheiten (0.5 pro Schritt)")
    ax.set_ylabel("Instrument")
    ax.set_title(f"Drum Pattern (Intensity = {intensity})")

    # Optional: Legende 0/1
    fig.colorbar(cax, label="Schlag (0=nein, 1=ja)")
    plt.tight_layout()
    plt.show()

# Beispiel: Visualisiere Intensität 5
visualize_drum_pattern(drum_patterns, intensity=5)

# Und Intensität 2
visualize_drum_pattern(drum_patterns, intensity=2)

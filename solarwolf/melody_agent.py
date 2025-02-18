import random

class MelodyAgent:
    def __init__(self):
        # Ursprüngliche Skala (A‑Moll-Kontext, z. B. A, C, D, E, G)
        self.scale = [57, 60, 62, 64, 67]

        self.phrase_library = {
            1: [
                [(69, 1), (72, 1)],            
                [(72, 2.0)],                      
                [(69, 2.0)],
                [(76, 2.0)],
                [(69, 1.0), (67, 1.0)],
            ],
            2: [
                # Stufe 2
                [(67, 0.5), (69, 0.5), (72, 1.0)],
                [(72, 0.5), (69, 0.5), (76, 1.0)],
                [(69, 2)],
                [(72, 2.0)],
            ],
            3: [
                [(69, 0.5), (72, 0.5), (74, 0.5), (76, 0.5)],
                [(76, 1.0), (72, 0.5), (74, 0.5)],
                [(69, 0.5), (71, 0.5), (72, 0.5), (74, 0.5)],
                [(76, 2)], 
                [(69, 0.5), (72, 0.5), (74, 1.0)],
                [(69, 0.5), (69, 0.5), (74, 1.0)],
                [(76, 0.5), (72, 0.5), (74, 1.0)],
            ],
            4: [
                [(69, 0.5), (72, 0.5), (74, 1.0)],
                [(69, 0.5), (69, 0.5), (74, 1.0)],
                [(72, 0.5), (72, 0.5) ,(74, 0.5), (76, 0.5)],
                [(69, 0.5), (72, 1.0), (79, 0.5)],
                [(76, 2)],
                [(76, 0.5), (72, 0.5), (74, 1.0)],
                [(72, 0.5), (74, 0.5), (72, 0.5), (69, 0.5)],
                [(74, 0.5), (69, 0.5), (72, 1)],
                [(69, 2)]
            ],
            5: [
                [(69, 0.25),(69, 0.25), (72, 0.5), (74, 1.0)],
                [(76, 0.25),(76, 0.25), (72, 0.5), (74, 1.0)],
                [(74, 1), (69, 0.25), (69, 0.25), (74, 0.5)],
                [(74, 0.25),(74, 0.25), (69, 0.5), (72, 1)],
                [(69, 2)],
                [(69, 1), (72, 1)],
                [(69, 1.0), (67, 1.0)],
                [(69, 0.5), (69, 0.5), (72, 0.5), (69, 0.5)],
            ]
        }

    def _split_into_measures(self, pattern, measure_length=2.0):
        measures = []
        current_measure = []
        current_sum = 0.0
        for p, d in pattern:
            if current_sum + d == measure_length:
                current_measure.append((p, d))
                measures.append(current_measure)
                current_measure = []
                current_sum = 0.0
            elif current_sum + d < measure_length:
                current_measure.append((p, d))
                current_sum += d
            else:
                pass
        if current_measure:
            measures.append(current_measure)
        return measures

    def _recombine_measures(self, measures):
        combined = []
        for m in measures:
            combined.extend(m)
        return combined

    def _get_phrase_pattern(self, intensity_level=3):
        """
        Wählt eine Phrase aus der Bibliothek, wendet evtl. eine Transposition oder leichte Variation an,
        und konvertiert sie anschließend von A‑Moll zu C‑Dur.
        """
        if intensity_level not in self.phrase_library:
            intensity_level = 3  # fallback

        phrase_candidates = self.phrase_library[intensity_level]
        phrase = random.choice(phrase_candidates)
        r = random.random()
        if r < 0.1:
            phrase = [(p - 12, d) for (p, d) in phrase]
        elif r < 0.3:
            phrase = [(p + 12, d) for (p, d) in phrase]

        if random.random() < 0.2 and len(phrase) > 2:
            i = random.randint(0, len(phrase) - 2)
            p, d = phrase[i]
            p_next, d_next = phrase[i + 1]
            if d > 0.25:
                delta = 0.25
                phrase[i] = (p, d - delta)
                phrase[i + 1] = (p_next, d_next + delta)

        #phrase = [(p + 12, d) for (p, d) in phrase]
        return phrase

    def _fit_to_measure(self, phrase, measure_length=2.0):
        total = sum(d for (_, d) in phrase)
        if abs(total - measure_length) < 0.01:
            return phrase  
        elif total < measure_length:
            rest = measure_length - total
            if len(phrase) > 0:
                last_pitch = phrase[-1][0]
            else:
                last_pitch = random.choice(self.scale)
            new_phrase = phrase + [(last_pitch, rest)]
            return new_phrase
        else:
            result = []
            running = 0.0
            for p, d in phrase:
                if running + d <= measure_length:
                    result.append((p, d))
                    running += d
                else:
                    delta = measure_length - running
                    if delta > 0:
                        result.append((p, delta))
                    break
            return result

    def _slight_variation(self, pattern, intensity_level):
        variation_chance = 0.05 * intensity_level
        new_pattern = []
        for (p, d) in pattern:
            if random.random() < variation_chance:
                possible_notes = [note for note in self.scale if abs(note - p) <= 5]
                if possible_notes:
                    p_new = random.choice(possible_notes)
                else:
                    p_new = p
                new_pattern.append((p_new, d))
            else:
                new_pattern.append((p, d))
        return new_pattern

    def _assemble_4bar_phrase(self, intensity_level=3):
        """
        Erzeugt eine 4-Takt-Phrase mit zufälliger Struktur:
         - A–A–B–A (ursprüngliches Muster)
         - A–B–A–C
         - A–B–C–D
        Jeder Buchstabe repräsentiert eine Phrase, wobei bei gleichem Buchstaben die Phrase wiederholt wird.
        """
        # Wähle zufällig ein Phrasenmuster aus
        pattern_choice = random.choice(["A-A-B-A", "A-B-A-C", "A-B-C-D"])
        print(f"[DEBUG] Ausgewähltes Phrasenmuster: {pattern_choice}")

        if pattern_choice == "A-A-B-A":
            phraseA = self._get_phrase_pattern(intensity_level)
            phraseB = self._get_phrase_pattern(intensity_level)
            measureA = self._fit_to_measure(phraseA, 2.0)
            measureB = self._fit_to_measure(phraseB, 2.0)
            big_pattern = measureA + measureA + measureB + measureA
        elif pattern_choice == "A-B-A-C":
            phraseA = self._get_phrase_pattern(intensity_level)
            phraseB = self._get_phrase_pattern(intensity_level)
            phraseC = self._get_phrase_pattern(intensity_level)
            measureA = self._fit_to_measure(phraseA, 2.0)
            measureB = self._fit_to_measure(phraseB, 2.0)
            measureC = self._fit_to_measure(phraseC, 2.0)
            big_pattern = measureA + measureB + measureA + measureC
        elif pattern_choice == "A-B-C-D":
            phraseA = self._get_phrase_pattern(intensity_level)
            phraseB = self._get_phrase_pattern(intensity_level)
            phraseC = self._get_phrase_pattern(intensity_level)
            phraseD = self._get_phrase_pattern(intensity_level)
            measureA = self._fit_to_measure(phraseA, 2.0)
            measureB = self._fit_to_measure(phraseB, 2.0)
            measureC = self._fit_to_measure(phraseC, 2.0)
            measureD = self._fit_to_measure(phraseD, 2.0)
            big_pattern = measureA + measureB + measureC + measureD

        return big_pattern

    def generate_melody(self, intensity_level=3, total_duration=8.0, num_notes=16):
        big_pattern = self._assemble_4bar_phrase(intensity_level)
        big_pattern = self._slight_variation(big_pattern, intensity_level)
        pitches = [p for (p, d) in big_pattern]
        durations = [d for (p, d) in big_pattern]
        print("[DEBUG] generate_melody (phrasing) für Intensität:", intensity_level)
        print("Pitches:", pitches)
        print("Durations:", durations)
        return pitches, durations

# Beispielhafte Verwendung:
if __name__ == "__main__":
    agent = MelodyAgent()
    pitches, durations = agent.generate_melody(intensity_level=3)
    print("Pitches:", pitches)
    print("Durations:", durations)

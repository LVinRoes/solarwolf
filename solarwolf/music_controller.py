# music_controller.py
from scamp import *
from melody_agent import MelodyAgent
from rhythm_agent import RhythmAgent
from bass_agent import BassAgent

def intensity_to_dynamic(intensity_level):
    # Ein einfaches Mapping von Intensitätsstufe zu Dynamik
    if intensity_level == 1:
        return "pp"
    elif intensity_level == 2:
        return "p"
    elif intensity_level == 3:
        return "mf"
    elif intensity_level == 4:
        return "f"
    elif intensity_level == 5:
        return "ff"
    else:
        return "mf"  # Standardfallback

class MusicController:
    def __init__(self):
        self.session = Session(tempo=120)
        self.current_intensity_level = 3
        self.stop_flag = False  # Flag, um den Prozess zu beenden

        # self.drone_instrument = self.session.new_part("Slow Strings SP 2")
        # self.drum_instrument = self.session.new_part("Standard 2")
        # self.melody_instrument = self.session.new_part("Pan Flute 2")
        # self.melody_layer_instrument = self.session.new_part("DistortionGuitar 2")
        # self.extra_instrument = self.session.new_part("Soundtrack 2")
        # self.bass_instrument = self.session.new_part("Synth Bass")
        # self.bass_layer_instrument = self.session.new_part("Slap Bass 1")

        self.drone_instrument = self.session.new_part("Square Wave")
        self.drum_instrument = self.session.new_part("TR 808")
        self.melody_instrument = self.session.new_part("Bass & Lead")
        self.melody_layer_instrument = self.session.new_part("DistortionGuitar 2")
        self.extra_instrument = self.session.new_part("Soundtrack 2")
        self.bass_instrument = self.session.new_part("Synth Bass")
        self.bass_layer_instrument = self.session.new_part("Slap Bass 1")

        self.layer_volumes = {
            "drone": 1.0,
            "drums": 1.0,
            "melody": 1.0,
            "extra": 1.0,
            "bass": 1.0
        }

        # Hier fügen wir ein neues Attribut ein, um den aktuellen Akkord zu speichern.
        self.current_chord = None

        self.update_music(self.current_intensity_level)
        print("[DEBUG] MusicController initialized and music layers generated.")

    def run_scamp(self):
        print("[DEBUG] Starting musical processes")
        self.session.fork(self.play_drone)
        self.session.fork(self.play_drums)
        self.session.fork(self.play_melody)
        self.session.fork(self.play_extra)
        self.session.fork(self.play_bass)
        print("[DEBUG] All musical processes forked.")
        self.session.wait_for_children_to_finish()
        print("[DEBUG] All musical processes finished.")

    def update_music(self, intensity_level):
        print(f"[DEBUG] Updating music for intensity level {intensity_level}")
        self.current_intensity_level = intensity_level
        self.layer_volumes["drums"] = intensity_level/5
        self.layer_volumes["drone"] = intensity_level/8
        self.layer_volumes["melody"] = intensity_level/5
        self.layer_volumes["extra"] = intensity_level/5
        self.layer_volumes["bass"] = intensity_level/5


    def play_bass(self):
        bass_agent = BassAgent()
        while not self.stop_flag:
            print("play bass wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["bass"]
            total_duration = 8.0

            # Aktuellen Akkord aus der Drohne holen, falls keiner gesetzt ist, fallback auf "Am7"
            current_chord = self.current_chord if self.current_chord else "Am7"

            pitches, durations = bass_agent.generate_bass_line(total_duration=total_duration, 
                                                            intensity_level=intensity_level, 
                                                            current_chord=current_chord)
            dynamic = intensity_to_dynamic(intensity_level)

            for pitch, duration in zip(pitches, durations):
                if self.stop_flag:
                    break
                volume = self.layer_volumes["bass"]
                self.bass_instrument.play_note(pitch=pitch, length=duration, volume=volume, properties=dynamic)
                self.bass_layer_instrument.play_note(pitch=pitch, length=duration, volume=volume, properties=dynamic)


    def play_drone(self):
        # Akkordprogressionen für verschiedene Intensitätsstufen:
        # Jede Progression ist eine Liste von Tupeln: (Akkordname, [Tonhöhen], Länge)
        # Jede Progression ist eine Liste von Tupeln: (Akkordname, [Tonhöhen], Länge)
        intensity_chords = {
            1: [
                ("Am7", [69, 72, 76, 79], 4.0),  # reine Tonika mehrmals
                ("Am7", [69, 72, 76, 79], 4.0),
                ("Am7", [69, 72, 76, 79], 4.0),
                ("Am7", [69, 72, 76, 79], 4.0)
            ],
            2: [
                # Wechsel zwischen Tonika (Am7) und Subdominante (Dm7) zur leichten Steigerung
                ("Am7", [69, 72, 76, 79], 4.0),
                ("Dm7", [62, 65, 69, 72], 4.0),
                ("Am7", [69, 72, 76, 79], 4.0),
                ("Dm7", [62, 65, 69, 72], 4.0)
            ],
            3: [
                # Ursprüngliche diatonische Progression in A-Moll: VI - iv - VI/ v - i
                ("Fmaj7", [65, 69, 72, 76], 4.0),   # VImaj7
                ("Dm7",   [62, 65, 69, 72], 4.0),   # ivm7
                ("Fmaj7", [65, 69, 72, 76], 2.0),   # VImaj7 (halber Takt)
                ("Em7",   [64, 67, 71, 74], 2.0),   # vm7 (halber Takt)
                ("Am7",   [69, 72, 76, 79], 4.0)    # im7
            ],
            4: [
                # Statt E7 nun Em7, um die Spannung zu reduzieren, aber dennoch Bewegung zu schaffen
                ("Fmaj7", [65, 69, 72, 76], 4.0),
                ("Dm7",   [62, 65, 69, 72], 4.0),
                ("Em7",   [64, 67, 71, 74], 2.0),  # vorher E7, jetzt Em7
                ("Em7",   [64, 67, 71, 74], 2.0),  # bleibt bei Em7 statt Dominante
                ("Am7",   [69, 72, 76, 79], 4.0)
            ],
            5: [
                # Statt bIImaj7 und E7#9 nutzen wir nur weitere diatonische Akkorde aus A-Moll:
                # Fmaj7 (VI), Cmaj7 (III), Em7 (v), Dm7 (iv), Am7 (i)
                ("Fmaj7", [65, 69, 72, 76], 2.0),    # VImaj7
                ("Cmaj7", [60, 64, 67, 72], 2.0),    # IIImaj7
                ("Em7",   [64, 67, 71, 74], 2.0),    # vm7
                ("Dm7",   [62, 65, 69, 72], 2.0),    # ivm7
                ("Am7",   [69, 72, 76, 79], 4.0)     # im7
            ]
        }


        while not self.stop_flag:
            print("play drone wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["drone"]
            dynamic = intensity_to_dynamic(intensity_level)

            # Hole die entsprechende Progression abhängig von der Intensität
            progression = intensity_chords.get(intensity_level, intensity_chords[3])  # Fallback zu Intensität 3

            # Durchlaufe die Akkordfolge und spiele sie
            for chord_name, chord_pitches, chord_length in progression:
                if self.stop_flag:
                    break
                volume = self.layer_volumes["drone"]
                self.current_chord = chord_name  # Aktuellen Akkord speichern
                self.drone_instrument.play_chord(chord_pitches, length=chord_length, volume=volume, properties=dynamic)


    def play_drums(self):
        rhythm_agent = RhythmAgent()
        while not self.stop_flag:
            print("play drums wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["drums"]
            dynamic = intensity_to_dynamic(intensity_level)

            drum_notes, drum_durations = rhythm_agent.generate_pattern(intensity_level=intensity_level)
            
            for pitches, duration in zip(drum_notes, drum_durations):
                if self.stop_flag:
                    break
                volume = self.layer_volumes["drums"]
                if len(pitches) > 0:
                    self.drum_instrument.play_chord(pitches, length=duration, volume=volume, properties=dynamic)
                else:
                    self.drum_instrument.play_chord([32,31], length=duration, volume=0)


    def play_melody(self):
        melody_agent = MelodyAgent() 
        while not self.stop_flag:
            print("play melody wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["melody"]
            dynamic = intensity_to_dynamic(intensity_level)

            # Wir übergeben nun auch den intensity_level an generate_melody
            pitches, durations = melody_agent.generate_melody(intensity_level=intensity_level)
            
            for pitch, duration in zip(pitches, durations):
                if self.stop_flag:
                    break
                # Hauptmelodie
                volume = self.layer_volumes["melody"]
                self.melody_instrument.play_note(pitch=pitch, length=duration, volume=volume, properties=dynamic)


    def play_extra(self):
        while not self.stop_flag:
            print("play extra wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["extra"]
            dynamic = intensity_to_dynamic(intensity_level)
            self.extra_instrument.play_note(pitch=72, volume=max(volume-0.4,0), length=8.0, properties=dynamic)

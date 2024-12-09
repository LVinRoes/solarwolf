# music_controller.py
from scamp import *
from melody_agent import MelodyAgent
from rhythm_agent import RhythmAgent
def intensity_to_dynamic(intensity_level):
    # Ein einfaches Mapping von Intensitätsstufe zu Dynamik
    # Dies kann nach Belieben angepasst werden.
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

        self.drone_instrument = self.session.new_part("Slow Strings SP 2")
        self.drum_instrument = self.session.new_part("TR 808")
        self.melody_instrument = self.session.new_part("Baritone Sax 2")
        self.melody_layer_instrument = self.session.new_part("Ocarina 2")
        self.extra_instrument = self.session.new_part("violin")
        self.bass_instrument = self.session.new_part("Synth Bass")
        self.bass_layer_instrument = self.session.new_part("Acoustic Bass 2")

        self.layer_volumes = {
            "drone": 1.0,
            "drums": 1.0,
            "melody": 1.0,
            "extra": 1.0,
            "bass": 1.0
        }

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
        
        if intensity_level == 1:
            self.layer_volumes["drone"] = 0.2
            self.layer_volumes["drums"] = 0.2
            self.layer_volumes["melody"] = 0.2
            self.layer_volumes["extra"] = 0.2
            self.layer_volumes["bass"] = 0.2
        elif intensity_level == 2:
            self.layer_volumes["drone"] = 0.4
            self.layer_volumes["drums"] = 0.4
            self.layer_volumes["melody"] = 0.4
            self.layer_volumes["extra"] = 0.4
            self.layer_volumes["bass"] = 0.4
        elif intensity_level == 3:
            self.layer_volumes["drone"] = 0.7
            self.layer_volumes["drums"] = 0.7
            self.layer_volumes["melody"] = 0.7
            self.layer_volumes["extra"] = 0.7
            self.layer_volumes["bass"] = 0.7
        elif intensity_level == 4:
            self.layer_volumes["drone"] = 0.9
            self.layer_volumes["drums"] = 0.9
            self.layer_volumes["melody"] = 0.9
            self.layer_volumes["extra"] = 0.9
            self.layer_volumes["bass"] = 0.9
        elif intensity_level == 5:
            self.layer_volumes["drone"] = 1.0
            self.layer_volumes["drums"] = 1.0
            self.layer_volumes["melody"] = 1.0
            self.layer_volumes["extra"] = 1.0
            self.layer_volumes["bass"] = 1.0

    def play_bass(self):
        melody_agent = MelodyAgent()
        while not self.stop_flag:
            print("play bass wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["bass"]
            num_notes = 2 * intensity_level
            total_duration = 8.0
            pitches, durations = melody_agent.generate_melody(total_duration=total_duration, num_notes=num_notes)
            pitches = [p - 24 for p in pitches]

            dynamic = intensity_to_dynamic(intensity_level)

            for pitch, duration in zip(pitches, durations):
                if self.stop_flag:
                    break
                # Hier ebenfalls Dynamiken setzen
                self.bass_instrument.play_note(pitch=pitch, length=duration, volume=volume, properties=dynamic)
                self.bass_layer_instrument.play_note(pitch=pitch, length=duration, volume=volume, properties=dynamic)

    def play_drone(self):
        while not self.stop_flag:
            print("play drone wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["drone"]
            dynamic = intensity_to_dynamic(intensity_level)
            self.drone_instrument.play_chord(pitches=[48, 60, 52], length=8.0, volume=volume, properties=dynamic)

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
                
                if len(pitches) > 0:
                    # Akkord spielen mit Dynamik
                    self.drum_instrument.play_chord(pitches, length=duration, volume=volume, properties=dynamic)
                else:
                    # Stiller Akkord, wir bleiben bei volume=0 und brauchen keine Dynamik
                    self.drum_instrument.play_chord([32,31], length=duration, volume=0)

    def play_melody(self):
        melody_agent = MelodyAgent()
        while not self.stop_flag:
            print("play melody wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["melody"]
            dynamic = intensity_to_dynamic(intensity_level)

            num_notes = 4 * intensity_level
            total_duration = 8.0
            pitches, durations = melody_agent.generate_melody(total_duration=total_duration, num_notes=num_notes)
            for pitch, duration in zip(pitches, durations):
                if self.stop_flag:
                    break
                # Dynamik angeben
                self.melody_instrument.play_note(pitch=pitch, length=duration, volume=volume, properties=dynamic)

    def play_extra(self):
        while not self.stop_flag:
            print("play extra wurde nun neu aufgerufen")
            intensity_level = self.current_intensity_level
            volume = self.layer_volumes["extra"]
            dynamic = intensity_to_dynamic(intensity_level)
            # Hier eventuell leiser machen, daher max(volume - 0.4,0) beibehalten
            self.extra_instrument.play_note(pitch=72, volume=max(volume-0.4,0), length=8.0, properties=dynamic)

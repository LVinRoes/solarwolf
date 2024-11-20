from scamp import *

class MusicController:
    def __init__(self):
        self.session = Session(tempo=120)
        self.current_intensity_level = 4

        self.drone_instrument = self.session.new_part("pad_synth")
        self.drum_instrument = self.session.new_part("TR 808")
        self.melody_instrument = self.session.new_part("piano")
        self.extra_instrument = self.session.new_part("violin")

        self.layer_volumes = {
            "drone": 1.0,
            "drums": 1.0,
            "melody": 1.0,
            "extra": 1.0
        }

        self.update_music(self.current_intensity_level)

        print("[DEBUG] MusicController initialized and music layers generated.")

    def run_scamp(self):
        print("[DEBUG] Starting musical processes")
        self.session.fork(self.play_drone)
        self.session.fork(self.play_drums)
        self.session.fork(self.play_melody)
        self.session.fork(self.play_extra)
        print("[DEBUG] All musical processes forked.")
        self.session.wait_for_children_to_finish()
        print("[DEBUG] All musical processes finished.")

    def update_music(self, intensity_level):
        print(f"[DEBUG] Updating music for intensity level {intensity_level}")
        self.current_intensity_level = intensity_level
        
        if intensity_level == 1:
            self.layer_volumes["drone"] = 0.2
            self.layer_volumes["drums"] = 0.0  # Drums aus
            self.layer_volumes["melody"] = 0.0  # Melodie aus
            self.layer_volumes["extra"] = 0.0  # Extra-Schicht aus
        elif intensity_level == 2:
            self.layer_volumes["drone"] = 0.4
            self.layer_volumes["drums"] = 0.2
            self.layer_volumes["melody"] = 0.0
            self.layer_volumes["extra"] = 0.0
        elif intensity_level == 3:
            self.layer_volumes["drone"] = 0.6
            self.layer_volumes["drums"] = 0.4
            self.layer_volumes["melody"] = 0.3
            self.layer_volumes["extra"] = 0.0
        elif intensity_level == 4:
            self.layer_volumes["drone"] = 0.8
            self.layer_volumes["drums"] = 0.6
            self.layer_volumes["melody"] = 0.5
            self.layer_volumes["extra"] = 0.3
        elif intensity_level == 5:
            self.layer_volumes["drone"] = 1.0
            self.layer_volumes["drums"] = 0.8
            self.layer_volumes["melody"] = 0.7
            self.layer_volumes["extra"] = 0.5


    def play_drone(self):
        
        
        while True:
            volume = self.layer_volumes["drone"]
            self.drone_instrument.play_chord(
                pitches=[48, 60, 52],
                length=3.0,
                volume=volume
            )
        print("[DEBUG] play_drone finished.")

    def play_drums(self):
        drum_notes = [36, 42, 36, 42, 38, 42, 36, 42]
        drum_durations = [0.25] * 8
        try:
            
            while True:
                volume = self.layer_volumes["drums"]
                for pitch, duration in zip(drum_notes, drum_durations):
                    self.drum_instrument.play_note(
                        pitch=pitch,
                        length=duration,
                        volume=volume
                    )
            print("[DEBUG] play_drums finished.")
        except Exception as e:
            print(f"[ERROR] Exception in play_drums: {e}")
            raise

    def play_melody(self):
        melody_notes = [60, 62, 64, 65, 67, 69, 71]
        melody_durations = [0.5] * 7
        try:
            
            while True:
                volume = self.layer_volumes["melody"]
                for pitch, duration in zip(melody_notes, melody_durations):
                    self.melody_instrument.play_note(
                        pitch=pitch,
                        length=duration,
                        volume=volume
                    )
                print("[DEBUG] play_melody finished.")
                wait(0.5)
        except Exception as e:
            print(f"[ERROR] Exception in play_melody: {e}")
            raise

    def play_extra(self):
        
        while True:
            volume = self.layer_volumes["extra"]
            self.extra_instrument.play_note(
                pitch=74,
                volume=volume,
                length=2.0
            )
        print("[DEBUG] play_extra finished.")

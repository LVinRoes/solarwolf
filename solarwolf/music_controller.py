from scamp import Session
import threading
import time
import random
from collections import defaultdict
from queue import Queue

from melody_agent import MelodyAgent
from rhythm_agent import RhythmAgent
from bass_agent import BassAgent
from harmony_helper import HarmonyHelper

def intensity_to_dynamic(intensity_level):
    """
    Ein einfaches Mapping von Intensitätsstufe zu Dynamik (z. B. "mf").
    """
    if intensity_level <= 1:
        return "pp"
    elif intensity_level == 2:
        return "p"
    elif intensity_level == 3:
        return "mf"
    elif intensity_level == 4:
        return "f"
    elif intensity_level >= 5:
        return "ff"
    return "mf"


class MusicBuffer:
    """
    Verwaltet vor-generierte Musikdaten in Queues pro (Intensität, Instrument).
    """
    def __init__(self, buffer_size=2):
        self.buffer = defaultdict(Queue)  
        self.buffer_size = buffer_size

    def add_music(self, intensity_level, instrument_type, music_data):
        key = f"{intensity_level}_{instrument_type}"
        self.buffer[key].put(music_data)
        print(f"[DEBUG] [MusicBuffer] Added music for key='{key}'. "
              f"New queue size: {self.buffer[key].qsize()}")

    def get_music(self, intensity_level, instrument_type):
        key = f"{intensity_level}_{instrument_type}"
        if not self.buffer[key].empty():
            music_data = self.buffer[key].get()
            print(f"[DEBUG] [MusicBuffer] Got music for key='{key}'. "
                  f"Remaining queue size: {self.buffer[key].qsize()}")
            return music_data
        else:
            print(f"[DEBUG] [MusicBuffer] No music available for key='{key}'.")
            return None

    def debug_dump_precomputed_data(self):
        print("[DEBUG] DUMPING ALL PRECOMPUTED DATA:")
        for level in range(1, 6):
            for instr_type in ["bass", "melody", "drums", "drone", "extra"]:
                key = f"{level}_{instr_type}"
                items_in_queue = list(self.buffer[key].queue)
                print(f"  -> key={key} hat {len(items_in_queue)} Einträge:")
                for i, data in enumerate(items_in_queue, start=1):
                    print(f"       #{i}: {data}")
        print("[DEBUG] END DUMP")


class MusicController:
    def __init__(self):
        self.session = Session(tempo=130)
        self.stop_flag = False

        self.current_intensity_level = 1

        
        self.high_intensity_start_time_harmony = None
        self.high_intensity_start_time_transposition = None
        self.skip_melody_until_next_chunk = False


        self.key_offset = 0  
        self.transposition_chance = 0.2
        self.transposed = False  
        self.tonart_switch_just_happened = False

        # --- Volume & Layers ---
        self.layer_volumes = {
            "drone": 1.0,
            "drums": 1.0,
            "melody": 1.0,
            "extra": 1.0,
            "bass": 1.0
        }

        # --- Chords & Helpers ---
        self.intensity_chords = {
            1: [
                ("Am", [65, 72, 76], 4.0),
                ("Am7", [69, 72, 76, 79], 4.0)
            ],
            2: [
                ("Am7", [69, 72, 76], 4.0),
                ("Dm7", [62, 65, 69, 72], 4.0)
            ],
            3: [
                ("Am7", [69, 72, 76], 3.0),
                ("Dm7", [64, 65, 69, 74], 1.0),
                ("Dm7", [62, 65, 69, 72], 3.0),
                ("Em7", [57, 60, 64, 67], 1.0)
            ],
            4: [
                ("Fmaj7", [65, 69, 72, 76], 4.0),
                ("Dm7",   [62, 65, 69, 72], 4.0)
            ],
            5: [
                ("Am7", [69, 72, 76], 2.0),
                ("Cmaj7", [60, 64, 67, 72], 2.0),
                ("Fmaj7", [65, 69, 72, 76], 2.0),
                ("Cmaj7", [60, 64, 67, 72], 2.0)
            ]
        }
        
        self.harmony_helper = HarmonyHelper()
        self.current_chord = None

        self.setup_instruments()
        self.music_buffer = MusicBuffer(buffer_size=2)
        self.buffer_threads = []

        self.update_music(self.current_intensity_level)
        print("[DEBUG] MusicController initialized.")

        # Start Buffer Generation (Threads)
        self.start_buffer_generation()

    def setup_instruments(self):
        """
        Initialisiert die SCAMP-Instrumente, die später abgespielt werden.
        """
        self.drone_instrument = self.session.new_part("English Horn")

        self.drone2_instrument = self.session.new_part("Piano Merlin")

        self.drum_instrument = self.session.new_part("Power 2")

        self.melody_instrument = self.session.new_part("Marimba")
        self.melody_layer_instrument = self.session.new_part("Synth Calliope")
        self.octave_layer_instrument = self.session.new_part("Guitar 2")

        self.extra_instrument = self.session.new_part("Sweep Pad")
        self.bass_instrument = self.session.new_part("Synth Bass")
        self.bass_layer_instrument = self.session.new_part("Slap Bass 1")

    def start_buffer_generation(self):
        """
        Startet pro Intensitätslevel einen Thread, der kontinuierlich 
        neue Musikdaten (Bass, Melody, Drums, Drone, Extra) generiert 
        und im Buffer ablegt.
        """
        print("[DEBUG] Starting buffer generation threads...")
        for level in range(1, 6):
            thread = threading.Thread(
                target=self.generate_buffer_for_level,
                args=(level,),
                daemon=True
            )
            thread.start()
            self.buffer_threads.append(thread)

    def generate_buffer_for_level(self, level):
        """
        Läuft in einem eigenen Thread; generiert fortlaufend 
        Bass-/Melody-/Drum-/Drone-/Extra-Daten für das gegebene Intensitätslevel
        und packt es in self.music_buffer.
        """
        bass_agent = BassAgent()
        melody_agent = MelodyAgent()
        rhythm_agent = RhythmAgent()

        while not self.stop_flag:
            self._maybe_generate_bass(level, bass_agent)
            self._maybe_generate_melody(level, melody_agent)
            self._maybe_generate_drums(level, rhythm_agent)
            self._maybe_generate_drone(level)
            self._maybe_generate_extra(level)
            time.sleep(0.1)

    def _maybe_generate_bass(self, level, bass_agent):
        key_bass = f"{level}_bass"
        if self.music_buffer.buffer[key_bass].qsize() < self.music_buffer.buffer_size:
            progression = self.intensity_chords.get(level, self.intensity_chords[3])
            bass_data = bass_agent.generate_bass_line_for_progression(
                progression=progression,
                intensity_level=level
            )
            self.music_buffer.add_music(level, "bass", bass_data)

    def _maybe_generate_melody(self, level, melody_agent):
        key_melody = f"{level}_melody"
        if self.music_buffer.buffer[key_melody].qsize() < self.music_buffer.buffer_size:
            melody_data = melody_agent.generate_melody(intensity_level=level)
            self.music_buffer.add_music(level, "melody", melody_data)

    def _maybe_generate_drums(self, level, rhythm_agent):
        key_drums = f"{level}_drums"
        if self.music_buffer.buffer[key_drums].qsize() < self.music_buffer.buffer_size:
            drum_data = rhythm_agent.generate_pattern(intensity_level=level)
            self.music_buffer.add_music(level, "drums", drum_data)

    def _maybe_generate_drone(self, level):
        key_drone = f"{level}_drone"
        if self.music_buffer.buffer[key_drone].qsize() < self.music_buffer.buffer_size:
            progression = self.intensity_chords.get(level, self.intensity_chords[3])
            self.music_buffer.add_music(level, "drone", progression)

    def _maybe_generate_extra(self, level):
        key_extra = f"{level}_extra"
        if self.music_buffer.buffer[key_extra].qsize() < self.music_buffer.buffer_size:
            self.music_buffer.add_music(level, "extra", ([72], [8.0]))


    def check_for_transposition(self):
        level = self.current_intensity_level
        if level < 4:
            self.high_intensity_start_time_transposition = None
            return

        if self.high_intensity_start_time_transposition is None:
            self.high_intensity_start_time_transposition = self.session.beat()

        time_in_high = self.session.beat() - self.high_intensity_start_time_transposition

        if time_in_high >= 16:
            print(f"[DEBUG] 4 Takte in Intensity {level} erreicht.")
            if random.random() < self.transposition_chance:
                self._toggle_transposition()
                self.transposition_chance = 0.1
            else:
                self.transposition_chance = min(1.0, self.transposition_chance + 0.1)
                print(f"self.transposition_chance = {self.transposition_chance}")
            self.high_intensity_start_time_transposition = self.session.beat()


    def _toggle_transposition(self):
        """
        Wechselt zwischen Originaltonart (0) und +2 Halbtöne.
        """
        if not self.transposed:
            self.key_offset = 2  
            self.transposed = True
        else:
            self.key_offset = 0  
            self.transposed = False

        self.skip_melody_until_next_chunk = True
        self.tonart_switch_just_happened = True 


    def run_scamp(self):
        """
        Startet die SCAMP-Forks für die einzelnen Layer und wartet,
        bis sie beendet werden.
        """
        print("[DEBUG] Starting musical processes")
        self.session.fork(self.play_drone)
        self.session.fork(self.play_drums)
        self.session.fork(self.play_melody)
        self.session.fork(self.play_extra)
        self.session.fork(self.play_bass)
        print("[DEBUG] All musical processes forked.")

        self.session.wait_for_children_to_finish()
        print("[DEBUG] All musical processes finished.")

    def play_bass(self):
        while not self.stop_flag:
            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            bass_data = self.music_buffer.get_music(level, "bass")

            if bass_data:
                pitches, durations = bass_data
                print(f"[DEBUG] [Playback] BASS level={level}, notes={len(pitches)}")

                for p, d in zip(pitches, durations):
                    if self.stop_flag:
                        break

                    transposed_pitch = p + self.key_offset
                    vol = self.layer_volumes["bass"]

                    # Falls Intensität < 3: Nur den Basston spielen
                    if level < 3:
                        self.bass_instrument.play_note(
                            pitch=transposed_pitch,
                            length=d,
                            volume=vol,
                            properties=dynamic
                        )
                    else:
                        # Ab Intensität >= 3: Bass + Oktave drüber gleichzeitig
                        chord = [transposed_pitch, transposed_pitch + 12]
                        self.bass_instrument.play_chord(
                            chord,
                            length=d,
                            volume=vol,
                            properties=dynamic
                        )


    def play_drone(self):
        while not self.stop_flag:
            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            progression = self.music_buffer.get_music(level, "drone")

            if progression:
                print(f"[DEBUG] [Playback] DRONE level={level}, chords={len(progression)}")
                for chord_name, chord_pitches, chord_len in progression:
                    if self.stop_flag:
                        break
                    vol = self.layer_volumes["drone"]
                    instrument = (self.drone_instrument if level >= 3
                                else self.drone2_instrument)
                    chord_pitches_transposed = [p + self.key_offset for p in chord_pitches]
                    self.current_chord = chord_name
                    instrument.play_chord(
                        chord_pitches_transposed, length=chord_len, volume=vol, properties=dynamic
                    )

    def play_drums(self):
        while not self.stop_flag:
            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            drum_data = self.music_buffer.get_music(level, "drums")

            if drum_data:
                pitches_list, durations_list = drum_data
                print(f"[DEBUG] [Playback] DRUMS level={level}, notes={len(pitches_list)}")
                for pitches, dur in zip(pitches_list, durations_list):
                    if self.stop_flag:
                        break
                    vol = self.layer_volumes["drums"]
                    
                    if pitches and level >= 2:
                        self.drum_instrument.play_chord(
                            pitches, length=dur, volume=vol, properties=dynamic
                        )
                    else:
                        self.drum_instrument.play_chord([32, 31], length=dur, volume=0)

    def play_melody(self):
        while not self.stop_flag:
            self.check_for_transposition()

            if self.skip_melody_until_next_chunk:
                self.skip_melody_until_next_chunk = False
                self.music_buffer.get_music(self.current_intensity_level, "melody")
                time.sleep(0.1)
                continue

            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            melody_data = self.music_buffer.get_music(level, "melody")

            do_harmony = False
            if level < 4:
                self.high_intensity_start_time_harmony = None
            else:
                if self.high_intensity_start_time_harmony is None:
                    self.high_intensity_start_time_harmony = self.session.beat()
                time_in_high = self.session.beat() - self.high_intensity_start_time_harmony
                if time_in_high >= 16:
                    do_harmony = (random.random() < 0.5)
                    if do_harmony:
                        print("[DEBUG] >>> Harmonien (Terzen) werden gespielt.")
                    else:
                        print("[DEBUG] >>> Keine Harmonien diesmal.")
                    self.high_intensity_start_time_harmony = self.session.beat()

            if self.tonart_switch_just_happened:
                do_harmony = False

            if melody_data:
                pitches, durations = melody_data
                print(f"[DEBUG] [Playback] MELODY level={level}, notes={len(pitches)}")

                for pitch, dur in zip(pitches, durations):
                    if self.stop_flag:
                        break

                    # --------------------------
                    # Vorbereitung der Akkord-/Notenliste
                    # --------------------------
                    vol = self.layer_volumes["melody"]
                    transposed_pitch = pitch + self.key_offset

                    # Wir fügen immer die Oktave tiefer hinzu: (pitch - 12)
                    chord = [transposed_pitch, transposed_pitch - 12]

                    if do_harmony:
                        # Füge Terz + Terz eine Oktave tiefer hinzu
                        third = self.harmony_helper.get_third_above_in_scale(pitch) + self.key_offset
                        chord.append(third)
                        chord.append(third - 12)

                    # --------------------------
                    # Instrument wählen
                    # --------------------------
                    instrument = (
                        self.melody_layer_instrument 
                        if level >= 4 else self.melody_instrument
                    )

                    # --------------------------
                    # Jetzt alles GLEICHZEITIG spielen
                    # (ein einziger play_chord-Aufruf)
                    # --------------------------
                    instrument.play_chord(chord, length=dur, volume=vol, properties=dynamic)

                if self.tonart_switch_just_happened:
                    self.tonart_switch_just_happened = False





    def play_extra(self):
        while not self.stop_flag:
            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            extra_data = self.music_buffer.get_music(level, "extra")

            if extra_data:
                pitches, durations = extra_data
                print(f"[DEBUG] [Playback] EXTRA level={level}, notes={len(pitches)}")
                for pitch, dur in zip(pitches, durations):
                    if self.stop_flag:
                        break
                    vol = self.layer_volumes["extra"]
                    transposed_pitch = pitch + self.key_offset
                    # Ab Intensität 4: Tremolo
                    properties = [dynamic, "tremolo"] if level >= 4 else dynamic
                    if level > 1:
                        self.extra_instrument.play_note(
                            pitch=transposed_pitch, length=dur, volume=vol, properties=properties
                        )
                    else:
                        self.extra_instrument.play_note(
                            pitch=transposed_pitch, length=dur, volume=0, properties=properties
                        )

    def update_music(self, intensity_level):
        """
        Aktualisiert Intensität, setzt Volume und Tempo,
        und prüft, ob wir in "High Intensity" wechseln (>=4).
        """
        intensity = max(1, min(5, int(round(intensity_level))))
        if intensity >= 4 and self.high_intensity_start_time is None:
            self.high_intensity_start_time = self.session.beat()
            print(f"[DEBUG] High INTENSITY start time = {self.high_intensity_start_time}")

        if intensity < 4:
            self.high_intensity_start_time = None

        # Volume anpassen
        self._update_volumes(intensity)
        # Tempo
        self._update_tempo_for_intensity(intensity)

        self.current_intensity_level = intensity
        print(f"[DEBUG] Updating music for intensity level {intensity}")

        

    def _update_volumes(self, intensity):
        """
        Passt die Layer-Volumes basierend auf Intensität an.
        """
        new_min = 0.7
        new_max = 1
        def scale_vol(factor):
            return (new_min + factor) * (new_max - new_min)

        self.layer_volumes["drums"]  = scale_vol(intensity / 5)
        self.layer_volumes["drone"]  = scale_vol(intensity / 10)
        self.layer_volumes["melody"] = scale_vol(intensity / 10)
        self.layer_volumes["extra"]  = scale_vol(intensity / 4)
        self.layer_volumes["bass"]   = scale_vol(intensity / 6)

    def _update_tempo_for_intensity(self, new_intensity, beats_for_transition=8.0):
        """
        Setzt das Tempo auf den zur Intensität passenden BPM-Wert 
        und überblendet innerhalb von 'beats_for_transition' Beats linear.
        """
        old_bpm = self.session.tempo
        base_bpm = 126
        increment = 2
        new_bpm = base_bpm + (new_intensity - 1) * increment

        print(f"[DEBUG] Linearer Tempo-Übergang von {old_bpm:.1f} auf {new_bpm:.1f} BPM in {beats_for_transition} Beats.")
        self.session.set_tempo_target(
            tempo_target=new_bpm,
            duration=beats_for_transition,
            curve_shape=0,          
            duration_units='beats',
            truncate=True
        )

    def debug_dump_precomputed_data(self):
        self.music_buffer.debug_dump_precomputed_data()

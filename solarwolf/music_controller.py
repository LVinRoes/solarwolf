import logging
import random
import threading
import time
from collections import defaultdict
from queue import Queue
from typing import Any, Dict, List, Optional, Tuple

from scamp import Session
from melody_agent import MelodyAgent
from rhythm_agent import RhythmAgent
from bass_agent import BassAgent
from harmony_helper import HarmonyHelper
from harmony_agent import HarmonyAgent

# Logging konfigurieren
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def intensity_to_dynamic(intensity_level: int) -> str:
    """
    Mapped eine Intensitätsstufe zu einer dynamischen Markierung.
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
    def __init__(self, buffer_size: int = 2) -> None:
        self.buffer: Dict[str, Queue] = defaultdict(Queue)
        self.buffer_size = buffer_size

    def _get_key(self, intensity_level: int, instrument_type: str) -> str:
        return f"{intensity_level}_{instrument_type}"

    def add_music(self, intensity_level: int, instrument_type: str, music_data: Any) -> None:
        key = self._get_key(intensity_level, instrument_type)
        self.buffer[key].put(music_data)
        logger.debug(f"[MusicBuffer] Added music for key='{key}'. "
                     f"New queue size: {self.buffer[key].qsize()}")

    def get_music(self, intensity_level: int, instrument_type: str) -> Optional[Any]:
        key = self._get_key(intensity_level, instrument_type)
        if not self.buffer[key].empty():
            music_data = self.buffer[key].get()
            logger.debug(f"[MusicBuffer] Got music for key='{key}'. "
                         f"Remaining queue size: {self.buffer[key].qsize()}")
            return music_data
        else:
            logger.debug(f"[MusicBuffer] No music available for key='{key}'.")
            return None

    def debug_dump_precomputed_data(self) -> None:
        logger.debug("DUMPING ALL PRECOMPUTED DATA:")
        for level in range(1, 6):
            for instr_type in ["bass", "melody", "drums", "drone", "extra"]:
                key = self._get_key(level, instr_type)
                items_in_queue = list(self.buffer[key].queue)
                logger.debug(f"  -> key={key} hat {len(items_in_queue)} Einträge:")
                for i, data in enumerate(items_in_queue, start=1):
                    logger.debug(f"       #{i}: {data}")
        logger.debug("END DUMP")


class MusicController:
    def __init__(self) -> None:
        self.session = Session(tempo=130)
        self.stop_flag = False
        self.current_intensity_level: int = 1
        self.counter: int = 0

        self.high_intensity_start_time_harmony: Optional[float] = None
        self.high_intensity_start_time_transposition: Optional[float] = None
        self.skip_melody_until_next_chunk = False

        self.bass_agent = BassAgent()
        self.melody_agent = MelodyAgent()
        self.rhythm_agent = RhythmAgent()
        self.harmony_agent = HarmonyAgent()

        # self.current_progression entfällt jetzt

        self.key_offset = 0  
        self.transposition_chance = 0.2
        self.transposed = False  
        self.tonart_switch_just_happened = False

        # Layer Volumes
        self.layer_volumes: Dict[str, float] = {
            "drone": 1.0,
            "drums": 1.0,
            "melody": 1.0,
            "extra": 1.0,
            "bass": 1.0
        }

        # Die vordefinierten Akkordfolgen bleiben hier zur Notfall-/Fallback-Nutzung,
        # werden aber beim neuen Ansatz über den HarmonyAgent nicht mehr direkt genutzt.
        self.intensity_chords: Dict[int, List[Tuple[str, List[int], float]]] = {
           1: [
                ("Am", [65, 72, 76], 4.0),
                ("Am7", [69, 72, 76, 79], 4.0)
            ],
            2: [
                ("Am7", [69, 72, 76], 4.0),
                ("Dm7", [62, 65, 69, 72], 4.0)
            ],
            5: [
                ("Am7", [69, 72, 76], 3.0),
                ("Dm7", [64, 65, 69, 74], 1.0),
                ("Dm7", [62, 65, 69, 72], 3.0),
                ("Em7", [57, 60, 64, 67], 1.0)
            ],
            3: [
                ("Fmaj7", [65, 69, 72, 76], 4.0),
                ("Dm7",   [62, 65, 69, 72], 4.0)
            ],
            4: [
                ("Am7", [69, 72, 76], 3.0),
                ("Dm7", [64, 65, 69, 74], 1.0),
                ("Dm7", [62, 65, 69, 72], 4.0)
            ]
        } 
        
        self.harmony_helper = HarmonyHelper()
        self.current_chord: Optional[str] = None

        self.setup_instruments()
        self.music_buffer = MusicBuffer(buffer_size=2)
        self.buffer_threads: List[threading.Thread] = []

        self.update_music(self.current_intensity_level)
        logger.debug("MusicController initialized.")

        # Starte Buffer-Generierung in separaten Threads
        self.start_buffer_generation()

    def setup_instruments(self) -> None:
        """
        Initialisiert die SCAMP-Instrumente.
        """
        self.drone_instrument = self.session.new_part("English Horn")
        self.drone2_instrument = self.session.new_part("Piano Merlin")
        self.drum_instrument = self.session.new_part("Power 2")
        self.melody_instrument = self.session.new_part("Marimba")
        self.melody_layer_instrument = self.session.new_part("Poly Synth")
        self.octave_layer_instrument = self.session.new_part("Guitar 2")
        self.extra_instrument = self.session.new_part("Sweep Pad")
        self.bass_instrument = self.session.new_part("Synth Bass")
        self.bass_layer_instrument = self.session.new_part("Slap Bass 1")

    def start_buffer_generation(self) -> None:
        """
        Startet pro Intensitätslevel einen Thread, der kontinuierlich neue Musikdaten
        generiert und in den Buffer legt.
        """
        logger.debug("Starting buffer generation threads...")
        for level in range(1, 6):
            thread = threading.Thread(
                target=self.generate_buffer_for_level,
                args=(level,),
                daemon=True
            )
            thread.start()
            self.buffer_threads.append(thread)

    def generate_buffer_for_level(self, level: int) -> None:
        """
        Generiert fortlaufend Musikdaten für das gegebene Intensitätslevel.
        """
        while not self.stop_flag:
            # Generiere eine Progression und füge sie gleichzeitig in beide Queues ein:
            self._maybe_generate_progression(level)
            self._maybe_generate_melody(level)
            self._maybe_generate_drums(level)
            self._maybe_generate_extra(level)
            time.sleep(0.1)

    def _maybe_generate_progression(self, level: int) -> None:
        """
        Generiert eine neue Progression (über den HarmonyAgent) und legt
        sie in die Buffer-Queues für Drone und Bass, falls dort weniger als
        die gewünschte Anzahl an Einträgen vorhanden ist.
        """
        key_drone = f"{level}_drone"
        key_bass = f"{level}_bass"
        if (self.music_buffer.buffer[key_drone].qsize() < self.music_buffer.buffer_size or 
            self.music_buffer.buffer[key_bass].qsize() < self.music_buffer.buffer_size):
            progression = self.harmony_agent.generate_progression(level)
            if self.music_buffer.buffer[key_drone].qsize() < self.music_buffer.buffer_size:
                self.music_buffer.add_music(level, "drone", progression)
            if self.music_buffer.buffer[key_bass].qsize() < self.music_buffer.buffer_size:
                bass_data = self.bass_agent.generate_bass_line_for_progression(
                    progression, intensity_level=level
                )
                self.music_buffer.add_music(level, "bass", bass_data)

    def _maybe_generate_melody(self, level: int) -> None:
        key = f"{level}_melody"
        if self.music_buffer.buffer[key].qsize() < self.music_buffer.buffer_size:
            melody_data = self.melody_agent.generate_melody(intensity_level=level)
            self.music_buffer.add_music(level, "melody", melody_data)

    def _maybe_generate_drums(self, level: int) -> None:
        key = f"{level}_drums"
        if self.music_buffer.buffer[key].qsize() < self.music_buffer.buffer_size:
            drum_data = self.rhythm_agent.generate_pattern(intensity_level=level)
            self.music_buffer.add_music(level, "drums", drum_data)

    def _maybe_generate_extra(self, level: int) -> None:
        key = f"{level}_extra"
        if self.music_buffer.buffer[key].qsize() < self.music_buffer.buffer_size:
            self.music_buffer.add_music(level, "extra", ([72], [8.0]))

    def check_for_transposition(self) -> None:
        level = self.current_intensity_level
        if level < 4:
            self.high_intensity_start_time_transposition = None
            return

        if self.high_intensity_start_time_transposition is None:
            self.high_intensity_start_time_transposition = self.session.beat()

        time_in_high = self.session.beat() - self.high_intensity_start_time_transposition
        if time_in_high >= 16:
            logger.debug(f"4 Takte in Intensity {level} erreicht.")
            if random.random() < self.transposition_chance:
                self._toggle_transposition()
                self.transposition_chance = 0.1
            else:
                self.transposition_chance = min(1.0, self.transposition_chance + 0.1)
                logger.debug(f"transposition_chance = {self.transposition_chance}")
            self.high_intensity_start_time_transposition = self.session.beat()

    def _toggle_transposition(self) -> None:
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

    def run_scamp(self) -> None:
        """
        Startet die SCAMP-Forks für die einzelnen Layer und wartet, bis sie beendet werden.
        """
        logger.debug("Starting musical processes")
        self.session.fork(self.play_drone)
        self.session.fork(self.play_drums)
        self.session.fork(self.play_melody)
        self.session.fork(self.play_extra)
        self.session.fork(self.play_bass)
        logger.debug("All musical processes forked.")

        self.session.wait_for_children_to_finish()
        logger.debug("All musical processes finished.")

    def play_bass(self) -> None:
        while not self.stop_flag:
            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            bass_data = self.music_buffer.get_music(level, "bass")
            self.counter += 1
            logger.debug(f"Bass counter: {self.counter}")

            if bass_data:
                pitches, durations = bass_data
                logger.debug(f"[Playback] BASS level={level}, notes={len(pitches)}")
                for p, d in zip(pitches, durations):
                    if self.stop_flag:
                        break
                    transposed_pitch = p + self.key_offset
                    vol = self.layer_volumes["bass"]
                    if level < 3:
                        self.bass_instrument.play_note(
                            pitch=transposed_pitch,
                            length=d,
                            volume=vol,
                            properties=dynamic
                        )
                    else:
                        chord = [transposed_pitch, transposed_pitch + 12]
                        self.bass_instrument.play_chord(
                            chord,
                            length=d,
                            volume=vol,
                            properties=dynamic
                        )

    def play_drone(self) -> None:
        while not self.stop_flag:
            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            progression = self.music_buffer.get_music(level, "drone")
            if progression:
                logger.debug(f"[Playback] DRONE level={level}, chords={len(progression)}")
                for chord_name, chord_pitches, chord_len in progression:
                    if self.stop_flag:
                        break
                    vol = self.layer_volumes["drone"]
                    instrument = self.drone_instrument if level >= 3 else self.drone2_instrument
                    transposed_chord = [p + self.key_offset for p in chord_pitches]


                    self.current_chord = chord_name
                    instrument.play_chord(
                        transposed_chord,
                        length=chord_len,
                        volume=vol-0.3,
                        properties=dynamic
                    )

    def play_drums(self) -> None:
        while not self.stop_flag:
            current_intensity = self.current_intensity_level
            dynamic = intensity_to_dynamic(current_intensity)
            drum_data = self.music_buffer.get_music(current_intensity, "drums")
            if drum_data:
                # Entpacke drum_data als (generated_intensity, pattern)
                generated_intensity, pattern = drum_data
                # Zerlege pattern (Liste von Tupeln (instruments, duration)) in zwei separate Listen:
                if pattern:
                    pattern_pitches, pattern_durations = zip(*pattern)
                    pattern_pitches = list(pattern_pitches)
                    pattern_durations = list(pattern_durations)
                else:
                    pattern_pitches, pattern_durations = [], []
                
                num_subdivisions = len(pattern_durations)
                # Erzeuge zusätzlich ein neues Pattern aus dem RhythmAgent (falls benötigt)
                _, new_pattern = self.rhythm_agent.generate_pattern(current_intensity)
                vol = self.layer_volumes["drums"]
                if current_intensity == 1:
                    vol = 0
                for index, (old_instruments, dur) in enumerate(zip(pattern_pitches, pattern_durations)):
                    if self.stop_flag:
                        break

                    print(f"Generated intensity: {generated_intensity}, current intensity: {self.current_intensity_level}")

                    # Prüfe, ob wir in der zweiten Hälfte des Taktes sind
                    if index >= num_subdivisions / 2:
                        intensity_diff = self.current_intensity_level - generated_intensity
                        if abs(intensity_diff) > 0.5:
                            f = (index - (num_subdivisions / 2)) / (num_subdivisions / 2)
                            # Bei einem Wechsel von niedrig nach hoch (intensity_diff > 0) den Fill-Faktor anpassen
                            if intensity_diff > 0:
                                reduced_factor = f * 0.3 * abs(intensity_diff)
                            else:
                                reduced_factor = f * 0.3
                            print(f"Fill-Faktor: {f}, intensity_diff: {intensity_diff}, reduced_factor: {reduced_factor}")
                            result_instruments = list(old_instruments)
                            if random.random() < reduced_factor:
                                result_instruments.append(self.rhythm_agent.crash)
                            if random.random() < reduced_factor:
                                print("Adding tom to fill")
                                result_instruments.append(random.choice([
                                    self.rhythm_agent.tom_low,
                                    self.rhythm_agent.tom_mid,
                                    self.rhythm_agent.tom_high
                                ]))
                        else:
                            result_instruments = old_instruments
                    else:
                        result_instruments = old_instruments

                    if result_instruments and self.current_intensity_level >= 1:
                        self.drum_instrument.play_chord(
                            result_instruments,
                            length=dur,
                            volume=vol-0.1,
                            properties=dynamic
                        )
                    else:
                        self.drum_instrument.play_chord([32, 31], length=dur, volume=0)



    def play_melody(self) -> None:
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
                    do_harmony = random.random() < 0.5
                    logger.debug(">>> Harmonien (Terzen) werden gespielt." if do_harmony else ">>> Keine Harmonien diesmal.")
                    self.high_intensity_start_time_harmony = self.session.beat()

            if self.tonart_switch_just_happened:
                do_harmony = False

            if melody_data:
                pitches, durations = melody_data
                logger.debug(f"[Playback] MELODY level={level}, notes={len(pitches)}")
                for pitch, dur in zip(pitches, durations):
                    if self.stop_flag:
                        break
                    vol = self.layer_volumes["melody"]
                    
                    transposed_pitch = pitch + self.key_offset
                    chord = [transposed_pitch, transposed_pitch - 12]
                    if do_harmony:
                        third = self.harmony_helper.get_third_above_in_scale(pitch) + self.key_offset
                        chord.extend([third, third - 12])
                    instrument = self.melody_layer_instrument if level >= 4 else self.melody_instrument
                    instrument.play_chord(chord, length=dur, volume=vol-0.2, properties=dynamic)
                if self.tonart_switch_just_happened:
                    self.tonart_switch_just_happened = False

    def play_extra(self) -> None:
        while not self.stop_flag:
            level = self.current_intensity_level
            dynamic = intensity_to_dynamic(level)
            extra_data = self.music_buffer.get_music(level, "extra")
            if extra_data:
                pitches, durations = extra_data
                logger.debug(f"[Playback] EXTRA level={level}, notes={len(pitches)}")
                for pitch, dur in zip(pitches, durations):
                    if self.stop_flag:
                        break
                    vol = self.layer_volumes["extra"]
                    transposed_pitch = pitch + self.key_offset
                    properties = [dynamic, "tremolo"] if level >= 4 else dynamic
                    if level > 1:
                        self.extra_instrument.play_note(
                            pitch=transposed_pitch,
                            length=dur,
                            volume=vol,
                            properties=properties
                        )
                    else:
                        self.extra_instrument.play_note(
                            pitch=transposed_pitch,
                            length=dur,
                            volume=0,
                            properties=properties
                        )

    def update_music(self, intensity_level: float) -> None:
        """
        Aktualisiert Intensität, passt Volumes und Tempo an.
        """
        intensity = max(1, min(5, int(round(intensity_level))))
        if intensity >= 4 and not hasattr(self, "high_intensity_start_time"):
            self.high_intensity_start_time = self.session.beat()
            logger.debug(f"High INTENSITY start time = {self.high_intensity_start_time}")
        if intensity < 4 and hasattr(self, "high_intensity_start_time"):
            del self.high_intensity_start_time

        self._update_volumes(intensity)
        self._update_tempo_for_intensity(intensity)
        self.current_intensity_level = intensity
        logger.debug(f"Updating music for intensity level {intensity}")

    def _update_volumes(self, intensity: int) -> None:
        new_min = 0.7
        new_max = 1.0

        def scale_vol(factor: float) -> float:
            return new_min + factor * (new_max - new_min)

        self.layer_volumes["drums"]  = scale_vol(intensity / 5)
        self.layer_volumes["drone"]  = scale_vol(intensity / 20)
        self.layer_volumes["melody"] = scale_vol(intensity / 10)
        self.layer_volumes["extra"]  = scale_vol(intensity / 4)
        self.layer_volumes["bass"]   = scale_vol(intensity / 6)

    def _update_tempo_for_intensity(self, new_intensity: int, beats_for_transition: float = 8.0) -> None:
        old_bpm = self.session.tempo
        base_bpm = 124
        increment = 1
        new_bpm = base_bpm + (new_intensity - 1) * increment
        logger.debug(f"Linearer Tempo-Übergang von {old_bpm:.1f} auf {new_bpm:.1f} BPM in {beats_for_transition} Beats.")
        self.session.set_tempo_target(
            tempo_target=new_bpm,
            duration=beats_for_transition,
            curve_shape=0,
            duration_units='beats',
            truncate=True
        )

    def debug_dump_precomputed_data(self) -> None:
        self.music_buffer.debug_dump_precomputed_data()


if __name__ == "__main__":
    controller = MusicController()
    try:
        controller.run_scamp()
    except KeyboardInterrupt:
        controller.stop_flag = True
        logger.debug("Musik gestoppt durch KeyboardInterrupt.")

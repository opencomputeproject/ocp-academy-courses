"""Signal regressions for pause-resistant narration level checks."""
import math
import random
import struct
import tempfile
import unittest
import wave
from pathlib import Path

from audio_tail_report import analyze


class AudioLevelTests(unittest.TestCase):
    def clip(self, sections, trailing=0):
        rate = 1000
        rng = random.Random(7)
        values = []
        for seconds, db, duty in sections:
            amplitude = 32768 * 10 ** (db / 20) * math.sqrt(3)
            for index in range(int(seconds * rate)):
                values.append(int(rng.uniform(-amplitude, amplitude)) if (index % rate) / rate < duty else 0)
        values.extend([0] * int(trailing * rate))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.wav"
            with wave.open(str(path), "wb") as writer:
                writer.setparams((1, 2, rate, 0, "NONE", "not compressed"))
                writer.writeframes(struct.pack("<" + "h" * len(values), *values))
            return analyze(path)

    def test_quiet_ending_above_old_absolute_threshold_is_flagged(self):
        result = self.clip([(15, -22, .7), (15, -23, .7), (15, -24, .7), (15, -27, .7)])
        self.assertGreater(result["tail_db"], -30)
        self.assertGreater(result["spoken_fade_db"], 4.8)
        self.assertTrue(any("spoken-level decline" in flag for flag in result["flags"]))

    def test_more_pauses_do_not_count_as_quieter_speech(self):
        result = self.clip([(30, -24, .9), (30, -24, .4)])
        self.assertLess(abs(result["spoken_fade_db"]), .3)
        self.assertFalse(result["flags"])

    def test_trailing_silence_does_not_count_as_speech_fade(self):
        result = self.clip([(60, -24, .7)], trailing=20)
        self.assertLess(abs(result["spoken_fade_db"]), .3)
        self.assertFalse(result["flags"])

    def test_sustained_middle_drop_is_detected_even_if_ending_recovers(self):
        result = self.clip([(30, -22, .7), (15, -27, .7), (15, -22, .7)])
        self.assertIsNotNone(result["spoken_drop_onset_seconds"])
        self.assertLess(result["spoken_fade_db"], .3)

    def test_borderline_drop_is_a_review_prompt(self):
        result = self.clip([(45, -24, .7), (15, -26.7, .7)])
        self.assertTrue(any("borderline" in flag for flag in result["flags"]))

    def test_uniform_quiet_narration_is_not_a_relative_decline(self):
        result = self.clip([(60, -36, .7)])
        self.assertFalse(result["flags"])

    def test_silence_and_short_clips_do_not_produce_comparison_flags(self):
        self.assertFalse(self.clip([(40, -120, 0)])["flags"])
        self.assertIsNone(self.clip([(10, -22, .7), (10, -28, .7)])["spoken_fade_db"])


if __name__ == "__main__":
    unittest.main()

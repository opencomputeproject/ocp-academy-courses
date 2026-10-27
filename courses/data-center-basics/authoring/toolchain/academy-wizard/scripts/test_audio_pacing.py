"""Behavior checks for v4 pacing, request parameters and module isolation."""

import array
import io
import json
import math
import os
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import Mock, patch

import audio_pacing
import gen_audio
from elevenlabs_model_support import should_send_language_code, validate_voice_model


def write_tone(path, seconds=6, frequency=440):
    samples = array.array("h", (int(6000 * math.sin(2 * math.pi * frequency * i / 22050))
                               for i in range(round(seconds * 22050))))
    with wave.open(str(path), "wb") as writer:
        writer.setparams((1, 2, 22050, 0, "NONE", "not compressed"))
        writer.writeframes(samples.tobytes())


class PacingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_tempo_matches_duration_without_changing_pitch(self):
        native, final = self.root / "native.wav", self.root / "final.wav"
        write_tone(native)
        receipt = audio_pacing.match_wav_duration(native, final, 5)
        self.assertLessEqual(abs(receipt["final_seconds"] - 5), .05)
        with wave.open(str(final)) as reader:
            self.assertEqual((reader.getnchannels(), reader.getsampwidth(), reader.getframerate()), (1, 2, 22050))
            samples = array.array("h", reader.readframes(reader.getnframes()))
        middle = samples[22050:-22050]
        crossings = sum(a <= 0 < b for a, b in zip(middle, middle[1:]))
        self.assertAlmostEqual(crossings / (len(middle) / 22050), 440, delta=2)

    def test_processing_failure_preserves_existing_output(self):
        native, final = self.root / "native.wav", self.root / "final.wav"
        write_tone(native)
        final.write_bytes(b"approved existing recording")
        with patch("audio_pacing.subprocess.run", return_value=Mock(returncode=1, stderr="encoder failed")):
            with self.assertRaisesRegex(RuntimeError, "encoder failed"):
                audio_pacing.match_wav_duration(native, final, 5, ffmpeg="ffmpeg")
        self.assertEqual(final.read_bytes(), b"approved existing recording")

    def test_missing_processor_blocks_both_billable_callbacks(self):
        native, reference = Mock(), Mock()
        with patch("audio_pacing.find_ffmpeg", side_effect=RuntimeError("missing ffmpeg")):
            with self.assertRaisesRegex(RuntimeError, "missing ffmpeg"):
                audio_pacing.synth_duration_matched("text", self.root / "output.wav", work_dir=self.root / "work",
                    identity={}, synth_native=native, synth_reference=reference)
        native.assert_not_called()
        reference.assert_not_called()

    def test_cache_reuses_reference_but_force_generates_fresh_native(self):
        reference = Mock(side_effect=lambda text, path: write_tone(path, 5))
        native = Mock(side_effect=lambda text, path: write_tone(path, 6))
        kwargs = dict(work_dir=self.root / "work", identity={"reference_speed": 1.18},
                      synth_native=native, synth_reference=reference)
        for _ in range(2):
            receipt = audio_pacing.synth_duration_matched("unchanged script", self.root / "output.wav", **kwargs)
        self.assertEqual(reference.call_count, 1)
        self.assertEqual(native.call_count, 2)
        self.assertTrue(Path(receipt["native_master"]).is_file())
        audio_pacing.synth_duration_matched("revised script", self.root / "output.wav", **kwargs)
        self.assertEqual(reference.call_count, 2)

    def test_reference_requires_matching_spoken_script(self):
        (self.root / "script.txt").write_text("Different approved text")
        write_tone(self.root / "reference.wav", 5)
        with self.assertRaisesRegex(ValueError, "differs"):
            audio_pacing.reference_files(self.root, "script.txt", "reference.wav", "New text")
        (self.root / "script.txt").write_text("# pronunciation: hints\nNew text")
        self.assertEqual(audio_pacing.reference_files(self.root, "script.txt", "reference.wav", "New text"), (self.root / "reference.wav").resolve())

    def test_v4_request_omits_speed_and_enforces_english(self):
        requests = []
        def respond(request, **kwargs):
            requests.append(json.loads(request.data))
            return io.BytesIO(b"\0\0" * 22050)
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-key"}), patch("urllib.request.urlopen", side_effect=respond):
            for model in ["eleven_v4", "eleven_v4_turbo", "eleven_multilingual_v2"]:
                gen_audio.synth_elevenlabs("Text", self.root / "output.wav", "voice", model, "en", 1.18)
        for request in requests[:2]:
            self.assertNotIn("speed", request["voice_settings"])
            self.assertEqual(request["language_code"], "en")
        self.assertEqual(requests[2]["voice_settings"]["speed"], 1.18)
        self.assertNotIn("language_code", requests[2])

    def test_v4_accepts_professional_clone_without_v4_fine_tune(self):
        metadata = {"voice_id": "Leo", "category": "professional", "high_quality_base_model_ids": ["eleven_multilingual_v2"]}
        self.assertIn("v4", validate_voice_model("eleven_v4", "Leo", voice_metadata=metadata))
        with self.assertRaisesRegex(RuntimeError, "Professional Voice Clone"):
            validate_voice_model("eleven_v3", "Leo", voice_metadata=metadata)

    def test_failed_native_synthesis_preserves_existing_recording(self):
        output = self.root / "output.wav"
        write_tone(output, 5)
        original = output.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "provider failed"):
            audio_pacing.synth_duration_matched("script", output, work_dir=self.root / "work", identity={},
                synth_native=Mock(side_effect=RuntimeError("provider failed")),
                synth_reference=lambda text, path: write_tone(path, 5))
        self.assertEqual(output.read_bytes(), original)

    def course_fixture(self):
        course = {"language": "en-US", "narration": {"engine": "elevenlabs", "voice_id": "Leo", "model_id": "eleven_multilingual_v2", "speed": 1.18}, "modules": []}
        baseline = self.root / "baseline"
        baseline.mkdir()
        for number in [1, 9]:
            audio = {"script_file": f"audio/module{number}/slide.txt", "wav_file": f"audio/module{number}/slide.wav"}
            mod = {"id": number, "slides": [{"id": 1, "type": "content", "audio": audio}]}
            course["modules"].append(mod)
            for root in [self.root, baseline]:
                script = root / audio["script_file"]
                script.parent.mkdir(parents=True, exist_ok=True)
                script.write_text("Complete approved teaching script.")
                write_tone(root / audio["wav_file"], 5)
        (baseline / "course.json").write_text(json.dumps(course))
        course["modules"][1]["narration"] = {"model_id": "eleven_v4"}
        (self.root / "course.json").write_text(json.dumps(course))
        return baseline

    def run_course(self, extra):
        calls = []
        def synth(text, path, voice, model, language, speed):
            calls.append((model, speed))
            write_tone(path, 6 if model == "eleven_v4" else 5)
        args = ["gen_audio.py", str(self.root / "course.json"), "--force", *extra]
        with patch.object(gen_audio.sys, "argv", args), patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-key"}), \
             patch.object(gen_audio, "validate_model_language", return_value="verified"), \
             patch.object(gen_audio, "validate_voice_model", return_value="verified"), \
             patch.object(gen_audio, "synth_elevenlabs", side_effect=synth):
            gen_audio.main()
        return calls

    def test_module_nine_does_not_touch_other_audio_or_course_json(self):
        baseline = self.course_fixture()
        untouched = (self.root / "audio/module1/slide.wav").read_bytes()
        metadata = (self.root / "course.json").read_bytes()
        calls = self.run_course(["--module", "9", "--pacing-reference-root", str(baseline)])
        self.assertEqual(calls, [("eleven_v4", 1.18)])
        self.assertEqual((self.root / "audio/module1/slide.wav").read_bytes(), untouched)
        self.assertEqual((self.root / "course.json").read_bytes(), metadata)
        self.assertAlmostEqual(audio_pacing.wav_duration(self.root / "audio/module9/slide.wav"), 5, delta=.05)

    def test_full_build_respects_module_specific_model(self):
        baseline = self.course_fixture()
        calls = self.run_course(["--pacing-reference-root", str(baseline)])
        self.assertEqual(calls, [("eleven_multilingual_v2", 1.18), ("eleven_v4", 1.18)])

    def test_mismatched_reference_is_blocked_before_any_synthesis(self):
        baseline = self.course_fixture()
        (baseline / "audio/module9/slide.txt").write_text("An obsolete script")
        with self.assertRaisesRegex(SystemExit, "differs"):
            self.run_course(["--pacing-reference-root", str(baseline)])

    def test_reference_profile_must_match_recorded_speed(self):
        baseline = self.course_fixture()
        path = baseline / "course.json"
        metadata = json.loads(path.read_text())
        metadata["narration"]["speed"] = 1.0
        path.write_text(json.dumps(metadata))
        with self.assertRaisesRegex(SystemExit, "timing reference must record"):
            self.run_course(["--module", "9", "--pacing-reference-root", str(baseline)])

    def test_existing_module_audio_blocks_local_quiz_fallback_in_another_module(self):
        self.course_fixture()
        path = self.root / "course.json"
        course = json.loads(path.read_text())
        course["modules"][1]["slides"][0]["type"] = "knowledge_check"
        path.write_text(json.dumps(course))
        (self.root / "audio/module9/slide.wav").unlink()
        args = ["gen_audio.py", str(path), "--engine", "say"]
        with patch.object(gen_audio.sys, "argv", args), patch.object(gen_audio, "synth_say") as synth:
            with self.assertRaisesRegex(SystemExit, "refusing local"):
                gen_audio.main()
            synth.assert_not_called()

    def test_chunked_v4_is_paced_after_assembly(self):
        baseline = self.course_fixture()
        path = self.root / "course.json"
        course = json.loads(path.read_text())
        course["modules"][1]["slides"][0]["audio"]["synthesis_chunks"] = ["Complete approved", "teaching script."]
        path.write_text(json.dumps(course))
        calls = self.run_course(["--module", "9", "--pacing-reference-root", str(baseline)])
        self.assertEqual(calls, [("eleven_v4", 1.18), ("eleven_v4", 1.18)])
        self.assertAlmostEqual(audio_pacing.wav_duration(self.root / "audio/module9/slide.wav"), 5, delta=.05)


if __name__ == "__main__":
    unittest.main()

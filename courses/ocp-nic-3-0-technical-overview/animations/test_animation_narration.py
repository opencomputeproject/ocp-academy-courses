import base64
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("narration", Path(__file__).with_name("synthesize_animation_narration.py"))
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class NarrationTests(unittest.TestCase):
    def setUp(self):
        self.config = {"voice_id": "test-voice", "model_id": "eleven_multilingual_v2", "speed": 1.18, "stability": .55, "similarity_boost": .75}
        self.alignment = {"characters": ["H", "i"], "character_start_times_seconds": [0, .2], "character_end_times_seconds": [.2, .4]}

    def test_comments_are_not_spoken(self):
        self.assertEqual(helper.spoken_body("# pronunciation: Rose\nHello\n # status: draft\nworld"), "Hello\nworld")

    def test_provenance_covers_voice_and_settings(self):
        a = helper.provenance("Hello", self.config)
        self.assertEqual(a["voice_settings"]["speed"], 1.18)
        self.assertNotEqual(a, helper.provenance("Hello again", self.config))
        self.assertNotEqual(a, helper.provenance("Hello", {**self.config, "voice_id": "another"}))

    def test_valid_alignment(self):
        helper.validate_alignment({"alignment": self.alignment}, 1)

    def test_invalid_lengths_rejected(self):
        with self.assertRaises(ValueError):
            helper.validate_alignment({"alignment": {**self.alignment, "characters": ["H"]}}, 1)

    def test_outside_audio_rejected(self):
        with self.assertRaises(ValueError):
            helper.validate_alignment({"alignment": self.alignment}, .1)

    def test_nonmonotonic_starts_rejected(self):
        with self.assertRaises(ValueError):
            helper.validate_alignment({"alignment": {**self.alignment, "character_start_times_seconds": [.3, .2]}}, 1)

    def test_timestamp_request_keeps_settings(self):
        response = {"audio_base64": base64.b64encode(b"\0" * 44100).decode(), "alignment": self.alignment}
        stream = io.BytesIO(json.dumps(response).encode())
        with patch.object(helper.urllib.request, "urlopen", return_value=stream) as network:
            pcm, alignment = helper.generate("Hi", self.config, "secret-not-saved")
        request = network.call_args.args[0]
        self.assertTrue(request.full_url.endswith("/with-timestamps?output_format=pcm_22050"))
        payload = json.loads(request.data)
        self.assertEqual(payload["voice_settings"]["speed"], 1.18)
        self.assertNotIn("language_code", payload)
        self.assertNotIn("audio_base64", alignment)
        self.assertEqual(len(pcm), 44100)

    def test_sha_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            wav = Path(temp) / "clip.wav"
            align = Path(temp) / "clip.alignment.json"
            wav.write_bytes(b"a")
            expected = helper.provenance("Hi", self.config)
            align.write_text(json.dumps({**expected, "wav_sha256": helper.digest(b"a")}))
            self.assertTrue(helper.current(wav, align, expected))
            wav.write_bytes(b"b")
            self.assertFalse(helper.current(wav, align, expected))

    def test_changed_approved_script_blocks(self):
        plan = {"scripts_approved": True, "new_single_pass_mode_approved": True, "approved_script_sha256": {"a.txt": "old"}}
        with self.assertRaises(RuntimeError):
            helper.approve(plan, {"a.txt": "new"})


if __name__ == "__main__":
    unittest.main()

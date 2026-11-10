"""Offline tests for explicit same-text cloud narration chunk plans."""
import struct
import tempfile
import unittest
import wave
from pathlib import Path

from gen_audio import approved_chunks, synth_chunks


class ChunkTests(unittest.TestCase):
    def test_no_plan_preserves_default(self):
        self.assertIsNone(approved_chunks("One. Two.", {}))

    def test_plan_preserves_text_and_allows_whitespace(self):
        chunks = ["One.", "Two.\nThree."]
        self.assertEqual(approved_chunks("One.\n\nTwo. Three.", {"synthesis_chunks": chunks}), chunks)

    def test_missing_reordered_empty_and_nonstring_plans_are_rejected(self):
        for chunks in (["One."], ["Two.", "One."], ["One.", ""], ["One.", None], "One. Two."):
            with self.subTest(chunks=chunks), self.assertRaises(ValueError):
                approved_chunks("One. Two.", {"synthesis_chunks": chunks})

    def test_native_pcm_is_joined_exactly(self):
        calls = []
        payloads = [struct.pack('<hhh', 0, 100, 0), struct.pack('<hhh', 0, -200, 0)]
        def synth(text, path):
            calls.append(text)
            with wave.open(str(path), 'wb') as writer:
                writer.setparams((1, 2, 22050, 0, 'NONE', 'not compressed'))
                writer.writeframes(payloads[len(calls) - 1])
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'final.wav'
            synth_chunks(['One.', 'Two.'], target, synth)
            with wave.open(str(target), 'rb') as reader:
                self.assertEqual(reader.readframes(reader.getnframes()), b''.join(payloads))
            self.assertEqual(calls, ['One.', 'Two.'])
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_request_failure_preserves_previous_output(self):
        def synth(text, path):
            raise RuntimeError('request failed')
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'final.wav'
            target.write_bytes(b'previous output')
            with self.assertRaises(RuntimeError):
                synth_chunks(['One.', 'Two.'], target, synth)
            self.assertEqual(target.read_bytes(), b'previous output')


if __name__ == '__main__':
    unittest.main()

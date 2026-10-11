import importlib.util
import json
import tempfile
import unittest
import wave
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('build_resources', Path(__file__).parents[1] / 'scripts/build_resources.py')
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


class SynchronizationGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'animations/sequence').mkdir(parents=True)
        self.audio = self.root / 'speech.wav'
        self.write_audio(8000)
        self.course = {'modules': [{'id': 1, 'slides': [{'id': 1,
            'audio': {'wav_file': 'speech.wav'}, 'figure': {
                'animation_source': 'animations/sequence/master.json', 'sync_to_narration': True}}]}]}
        self.master = {'duration': 1, 'fps': 30, 'audio_provenance': {'wav_sha256': sha256(self.audio.read_bytes()).hexdigest()}}
        (self.root / 'animations/plan.json').write_text(json.dumps({'videos': [{'module': 1, 'slide': 1, 'id': 'sequence'}]}))
        self.original_source = patch.object(hook, 'SOURCE', self.root)
        self.original_source.start()
        self.addCleanup(self.original_source.stop)

    def write_audio(self, frames, value=0):
        with wave.open(str(self.audio), 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(8000)
            wav.writeframes(value.to_bytes(2, 'little', signed=True) * frames)

    def validate(self):
        (self.root / 'course.json').write_text(json.dumps(self.course))
        (self.root / 'animations/sequence/master.json').write_text(json.dumps(self.master))
        hook.validate(self.root / 'course.json')

    def test_exact_recording_passes(self):
        self.validate()

    def test_same_duration_different_recording_is_rejected(self):
        self.write_audio(8000, 1200)
        with self.assertRaisesRegex(SystemExit, 'differs from the reviewed video timing'):
            self.validate()

    def test_duration_mismatch_is_rejected(self):
        self.write_audio(4000)
        self.master['audio_provenance']['wav_sha256'] = sha256(self.audio.read_bytes()).hexdigest()
        with self.assertRaisesRegex(SystemExit, 'duration mismatch'):
            self.validate()

    def test_missing_audio_is_rejected(self):
        self.audio.unlink()
        with self.assertRaisesRegex(SystemExit, 'Missing synchronized narration'):
            self.validate()

    def test_sync_opt_in_is_required(self):
        self.course['modules'][0]['slides'][0]['figure']['sync_to_narration'] = False
        with self.assertRaisesRegex(SystemExit, 'not enabled'):
            self.validate()


if __name__ == '__main__':
    unittest.main()

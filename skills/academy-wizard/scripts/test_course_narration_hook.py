"""Caption-timed recordings must never fall through to untimed TTS."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

class CourseNarrationHookTests(unittest.TestCase):
    def run_generation(self, with_master):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'script.txt').write_text('A timed demonstration.')
            course = {'style':'Slides', 'narration':{'engine':'elevenlabs',
                'model_id':'eleven_v4','voice_id':'test-approved-voice','speed':1.18,
                'delivery':{'format':'mp3','approved':True,'bitrate_kbps':96,
                    'sample_rate_hz':44100,'channels':1,'bitrate_mode':'CBR'}},
                'modules':[{'id':1,'slides':[{'id':6,'type':'content_diagram',
                    'audio':{'script_file':'script.txt','wav_file':'timed.wav',
                        'delivery_file':'timed.mp3','generation_hook':'scripts/generate_demo_narration.py'}}]}]}
            source = root / 'course.json';source.write_text(json.dumps(course))
            master = root / 'timed.wav'
            if with_master:
                master.write_bytes(b'Existing hook-owned master must remain untouched.')
            before = hashlib.sha256(master.read_bytes()).hexdigest() if master.exists() else None
            environment = dict(os.environ)
            environment.pop('ELEVENLABS_API_KEY', None)
            process = subprocess.run([sys.executable, str(Path(__file__).with_name('gen_audio.py')),
                str(source), '--force'], capture_output=True, text=True, env=environment)
            after = hashlib.sha256(master.read_bytes()).hexdigest() if master.exists() else None
            return process, before, after

    def test_missing_timed_master_fails_before_any_provider_request(self):
        process, before, after = self.run_generation(False)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('requires its course narration hook', process.stdout + process.stderr)
        self.assertEqual(before, after)

    def test_force_does_not_replace_a_hook_owned_master(self):
        process, before, after = self.run_generation(True)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertIn('skipped (already present): 1', process.stdout)
        self.assertEqual(before, after)

if __name__ == '__main__':
    unittest.main()

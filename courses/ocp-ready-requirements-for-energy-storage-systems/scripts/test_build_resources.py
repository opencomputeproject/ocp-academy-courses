import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReviewedMediaTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        source = root/'source'
        self.build = root/'build'
        self.hook = source/'scripts/build_resources.py'
        self.hook.parent.mkdir(parents=True)
        shutil.copy2(Path(__file__).with_name('build_resources.py'), self.hook)
        timing_file = source/'animations/full-v4/timings.final.json'
        timing_file.parent.mkdir(parents=True)
        self.build.mkdir()
        (self.build/'figures').mkdir()
        (self.build/'audio').mkdir()
        modules = []
        timings = {}
        for number in range(1, 5):
            media = self.build/f'figures/m{number}.mp4'
            media.write_bytes(f'reviewed video {number}'.encode())
            figure = {'media_type':'video','path':media.relative_to(self.build).as_posix(),
                      'text_inventory':{'sha256':digest(media)},'sync_to_narration':number < 4}
            slide = {'id':1,'figure':figure}
            if number < 4:
                audio = self.build/f'audio/m{number}.wav'
                with wave.open(str(audio),'wb') as writer:
                    writer.setparams((1,2,22050,0,'NONE','not compressed'))
                    writer.writeframes(b'\0\0'*22050)
                script = self.build/f'audio/m{number}.txt'
                script.write_text('Reviewed narration.\n',encoding='utf-8')
                slide['audio'] = {'wav_file':audio.relative_to(self.build).as_posix(),
                                  'script_file':script.relative_to(self.build).as_posix()}
                figure['narration_script_sha256'] = hashlib.sha256(b'Reviewed narration.').hexdigest()
                timings[f'M{number}S1'] = {'cues_reviewed':True,'duration_ms':1000,
                    'narration_sha256':digest(audio)}
            modules.append({'id':number,'slides':[slide]})
        self.course_path = self.build/'course.json'
        self.course_path.write_text(json.dumps({'language':'en-US','modules':modules}),encoding='utf-8')
        timing_file.write_text(json.dumps({'editions':{'en-US':timings}}),encoding='utf-8')

    def run_hook(self):
        return subprocess.run([sys.executable,str(self.hook),str(self.course_path)],capture_output=True,text=True)

    def test_matching_reviewed_assets_pass(self):
        result = self.run_hook()
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_changed_script_is_rejected(self):
        (self.build/'audio/m1.txt').write_text('Changed technical teaching.\n',encoding='utf-8')
        result = self.run_hook()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('script differs',result.stderr)

    def test_changed_recording_is_rejected(self):
        with (self.build/'audio/m2.wav').open('ab') as writer:
            writer.write(b'changed')
        result = self.run_hook()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('narration no longer matches',result.stderr)

    def test_changed_video_is_rejected(self):
        (self.build/'figures/m3.mp4').write_bytes(b'unreviewed replacement')
        result = self.run_hook()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('changed after visual review',result.stderr)


if __name__ == '__main__':
    unittest.main()

"""A new locale retains delivery/media but cannot reuse approved English speech."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

class TranslationRetainedMediaTests(unittest.TestCase):
    def test_native_voice_applies_without_losing_delivery_or_recordings(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'english';source.mkdir()
            for folder in ('resources/videos','scripts','poster-assets','audio/module1'):
                (source / folder).mkdir(parents=True)
            (source / 'resources/videos/demo.mp4').write_bytes(b'retained original video')
            (source / 'scripts/generate_demo_narration.py').write_text('# editable cue generator\n')
            (source / 'scripts/narration-cue-plan.json').write_text(json.dumps({'approved':True,'voice_id':'english-voice','model_id':'eleven_v4','clips':[]}))
            (source / 'poster.html').write_text('<html>Editable poster</html>')
            (source / 'thumbnail.png').write_bytes(b'poster bytes')
            (source / 'audio/module1/demo.wav').write_bytes(b'English audio must not be copied')
            course={'style':'Slides','course_slug':'demo','course_title':'Demo','language':'en-US',
                'narration':{'engine':'elevenlabs','voice_id':'english-voice','model_id':'eleven_v4',
                    'speed':1.18,'delivery':{'format':'mp3','approved':True,'bitrate_kbps':96},
                    'teaching_video_mode':'narration-synchronized'},
                'lms_catalog':{'approved':True},'modules':[{'id':1,'slides':[{'id':1,
                    'audio':{'approved':True,'wav_file':'audio/module1/demo.wav'}}]}]}
            original=source/'course.json';original.write_text(json.dumps(course))
            digest=hashlib.sha256(original.read_bytes()).hexdigest()
            process=subprocess.run([sys.executable,str(Path(__file__).with_name('scaffold_slides_translation.py')),
                str(original),'ko-KR'],capture_output=True,text=True)
            self.assertEqual(process.returncode,0,process.stdout+process.stderr)
            target=source/'locales/ko-KR';translated=json.loads((target/'course.json').read_text())
            self.assertEqual(translated['narration']['voice_id'],'PDoCXqBQFGsvfO0hNkEs')
            for key in ('speed','delivery','teaching_video_mode'):
                self.assertEqual(translated['narration'][key],course['narration'][key])
            self.assertEqual(translated['narration']['model_id'],'eleven_v4')
            self.assertFalse(translated['modules'][0]['slides'][0]['audio']['approved'])
            self.assertFalse(translated['lms_catalog']['approved'])
            self.assertFalse((target/'audio/module1/demo.wav').exists())
            self.assertEqual((target/'resources/videos/demo.mp4').read_bytes(),b'retained original video')
            self.assertTrue((target/'scripts/generate_demo_narration.py').exists())
            self.assertTrue((target/'poster.html').exists())
            cue=json.loads((target/'scripts/narration-cue-plan.json').read_text())
            self.assertFalse(cue['approved']);self.assertTrue(cue['localization_required'])
            self.assertEqual(cue['voice_id'],translated['narration']['voice_id'])
            self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),digest)

if __name__=='__main__':unittest.main()

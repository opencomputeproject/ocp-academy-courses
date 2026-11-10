"""MP3 defaults, original-media exclusions and real codec integrity."""
import copy, json, tempfile, unittest, wave, array, math, subprocess, sys
from pathlib import Path
from audio_delivery_defaults import apply_delivery_defaults, MP3_DELIVERY
from encode_delivery_audio import encode
from audio_pacing import find_ffmpeg, synth_paced

class MP3DefaultTests(unittest.TestCase):
    def course(self):
        return {'modules':[{'slides':[{'audio':{'wav_file':'audio/a.wav'}},
            {'figure':{'role':'original_video'},'audio':None}]}]}
    def test_defaults_and_original_exclusion(self):
        c={'modules':[]};self.assertTrue(apply_delivery_defaults(c))
        c['modules']=self.course()['modules'];self.assertTrue(apply_delivery_defaults(c))
        self.assertEqual(c['modules'][0]['slides'][0]['audio']['delivery_file'],'audio/a.mp3')
        self.assertIsNone(c['modules'][0]['slides'][1]['audio'])
        self.assertFalse(apply_delivery_defaults(c))
    def test_overrides_and_scrolling(self):
        for c in [{'style':'Scrolling'},dict(self.course(),narration={'delivery':{'format':'wav','migration_decision':'keep-wav'}}),dict(self.course(),narration={'delivery':dict(MP3_DELIVERY,bitrate_kbps=128)})]:
            if c.get('narration',{}).get('delivery',{}).get('format')=='mp3':
                c['modules'][0]['slides'][0]['audio']['delivery_file']='audio/a.mp3'
            before=copy.deepcopy(c);apply_delivery_defaults(c);self.assertEqual(before,c)
    def test_legacy_wav_requires_consent_without_mutation(self):
        for c in [self.course(),dict(self.course(),narration={'delivery':{'format':'wav','approved':True}})]:
            before=copy.deepcopy(c)
            with self.assertRaisesRegex(ValueError,'Ask the user'):
                apply_delivery_defaults(c)
            self.assertEqual(c,before)
    def test_approved_migration_and_decline_are_persisted(self):
        for choice,expected in [('mp3','mp3'),('keep-wav','wav')]:
            c=self.course();apply_delivery_defaults(c,choice)
            self.assertEqual(c['narration']['delivery']['format'],expected)
            self.assertEqual(c['narration']['delivery']['migration_decision'],choice)
            self.assertEqual('delivery_file' in c['modules'][0]['slides'][0]['audio'],choice=='mp3')
            self.assertFalse(apply_delivery_defaults(c))
    def test_cli_stops_before_creating_output_then_accepts_explicit_choice(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);c=self.course();c['modules'][0]['id']=1
            p=root/'course.json';p.write_text(json.dumps(c));before=p.read_bytes();out=root/'build'
            cmd=[sys.executable,str(Path(__file__).with_name('new_course.py')),str(out),str(p)]
            result=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(result.returncode,2);self.assertIn('Ask the user',result.stderr)
            self.assertFalse(out.exists());self.assertEqual(p.read_bytes(),before)
            subprocess.run(cmd+['--audio-delivery-choice','mp3'],check=True,capture_output=True)
            self.assertEqual(json.loads((out/'course.json').read_text())['narration']['delivery']['migration_decision'],'mp3')
    def test_synthesis_cli_requires_decision_before_api_or_file_changes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'course.json';p.write_text(json.dumps(self.course()));before=p.read_bytes()
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('gen_audio.py')),str(p)],capture_output=True,text=True)
            self.assertEqual(result.returncode,2);self.assertIn('Ask the user',result.stderr)
            self.assertEqual(p.read_bytes(),before)
    def test_scaffold_records_defaults_when_source_is_in_output_directory(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            c=self.course();c['modules'][0]['id']=1;c['narration']={'delivery':dict(MP3_DELIVERY)}
            p=root/'course.json';p.write_text(json.dumps(c))
            subprocess.run([sys.executable,str(Path(__file__).with_name('new_course.py')),str(root),str(p)],check=True,capture_output=True)
            actual=json.loads(p.read_text())
            self.assertEqual(actual['narration']['delivery']['bitrate_kbps'],96)
            self.assertEqual(actual['modules'][0]['slides'][0]['audio']['delivery_file'],'audio/a.mp3')
    def test_real_encode_preserves_master_and_decoded_duration(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'audio').mkdir();wav=root/'audio/a.wav'
            with wave.open(str(wav),'wb') as w:
                w.setparams((1,2,22050,0,'NONE','not compressed'))
                w.writeframes(array.array('h',[int(6000*math.sin(2*math.pi*440*i/22050)) for i in range(44100)]).tobytes())
            original=wav.read_bytes();(root/'course.json').write_text(json.dumps(self.course()))
            with self.assertRaisesRegex(ValueError,'Ask the user'):
                encode(root/'course.json',ffmpeg=find_ffmpeg())
            self.assertFalse((root/'audio/a.mp3').exists())
            r=encode(root/'course.json',ffmpeg=find_ffmpeg(),migration_choice='mp3')
            self.assertEqual(r['api_calls'],0);self.assertEqual(wav.read_bytes(),original)
            self.assertLess(r['clips'][0]['decoded_duration_difference_ms'],5)
            self.assertLess((root/'audio/a.mp3').stat().st_size,len(original))
    def test_provider_master_and_receipt_retained(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            def provider(text,p):
                with wave.open(str(p),'wb') as w:
                    w.setparams((1,2,22050,0,'NONE','not compressed'));w.writeframes(b'\0\0'*44100)
                p.with_suffix('.provider.mp3').write_bytes(b'provider bytes')
            r=synth_paced('text',root/'paced.wav',work_dir=root/'masters',identity={'model_id':'eleven_v4'},synth_native=provider)
            self.assertEqual(Path(r['provider_master']).read_bytes(),b'provider bytes')
            self.assertIn('not a lossless',r['wav_provenance'])

if __name__=='__main__':unittest.main()

"""Behavior checks for required full-v4 narration, pacing and module isolation."""
import array,io,json,math,os,tempfile,unittest,wave
from pathlib import Path
from unittest.mock import Mock,patch
import audio_pacing,gen_audio
from elevenlabs_model_support import default_model_for_language,validate_voice_model

def write_tone(path,seconds=6):
    samples=array.array('h',(int(6000*math.sin(2*math.pi*440*i/22050)) for i in range(round(seconds*22050))))
    with wave.open(str(path),'wb') as w:w.setparams((1,2,22050,0,'NONE','not compressed'));w.writeframes(samples.tobytes())

class PacingTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
    def test_defaults_and_policy_aliases_always_choose_full_model(self):
        with patch.dict(os.environ,{},clear=True):
            self.assertEqual(gen_audio.pick_engine(None,{}),'elevenlabs')
            self.assertEqual(gen_audio.pick_model_id({},'elevenlabs'),'eleven_v4')
            for language in ['en-US','vi','ko','ja','zh-TW']:
                for policy in ['stable','expressive','balanced']:
                    self.assertEqual(default_model_for_language(language,policy),'eleven_v4')
    def test_other_model_or_engine_blocks_before_generation(self):
        with self.assertRaises(ValueError):gen_audio.pick_model_id({'narration':{'model_id':'retired'}},'elevenlabs')
        with patch.dict(os.environ,{'ELEVENLABS_MODEL':'retired'}):
            with self.assertRaises(ValueError):gen_audio.pick_model_id({},'elevenlabs')
        with self.assertRaises(ValueError):gen_audio.pick_engine('say',{})
        with patch('urllib.request.urlopen') as request:
            with patch.dict(os.environ,{'ELEVENLABS_API_KEY':'test-key'}):
                with self.assertRaises(ValueError):gen_audio.synth_elevenlabs('Text',self.root/'out.wav','Leo','retired','en',1.18)
            request.assert_not_called()
    def test_request_uses_full_model_and_no_api_speed(self):
        calls=[]
        def respond(request,**kwargs):calls.append(json.loads(request.data));return io.BytesIO(b'\0\0'*22050)
        with patch.dict(os.environ,{'ELEVENLABS_API_KEY':'test-key'}),patch('urllib.request.urlopen',side_effect=respond):
            gen_audio.synth_elevenlabs('Text',self.root/'out.wav','Leo','eleven_v4','en',1.18)
        self.assertEqual(len(calls),1);self.assertEqual(calls[0]['model_id'],'eleven_v4')
        self.assertEqual(calls[0]['language_code'],'en');self.assertNotIn('speed',calls[0]['voice_settings'])
    def test_native_pacing_preserves_pitch_and_records_one_synthesis(self):
        native=Mock(side_effect=lambda text,p:write_tone(p,6))
        receipt=audio_pacing.synth_paced('approved script',self.root/'out.wav',work_dir=self.root/'work',identity={'model_id':'eleven_v4'},synth_native=native,speed=1.18)
        native.assert_called_once();self.assertAlmostEqual(receipt['final_seconds'],6/1.18,delta=.05)
        self.assertTrue(Path(receipt['native_master']).is_file())
        with wave.open(str(self.root/'out.wav')) as w:samples=array.array('h',w.readframes(w.getnframes()))
        middle=samples[22050:-22050];crossings=sum(a<=0<b for a,b in zip(middle,middle[1:]))
        self.assertAlmostEqual(crossings/(len(middle)/22050),440,delta=2)
    def test_failed_processing_keeps_previous_output(self):
        native=self.root/'native.wav';out=self.root/'out.wav';write_tone(native);out.write_bytes(b'previous recording')
        with patch('audio_pacing.subprocess.run',return_value=Mock(returncode=1,stderr='failed')):
            with self.assertRaises(RuntimeError):audio_pacing.match_wav_duration(native,out,5,ffmpeg='ffmpeg')
        self.assertEqual(out.read_bytes(),b'previous recording')
    def test_missing_processor_or_failed_provider_preserves_output(self):
        out=self.root/'out.wav';out.write_bytes(b'previous recording');native=Mock()
        with patch('audio_pacing.find_ffmpeg',side_effect=RuntimeError('missing')):
            with self.assertRaises(RuntimeError):audio_pacing.synth_paced('text',out,work_dir=self.root/'work',identity={'model_id':'eleven_v4'},synth_native=native)
        native.assert_not_called()
        with self.assertRaises(RuntimeError):audio_pacing.synth_paced('text',out,work_dir=self.root/'work',identity={'model_id':'eleven_v4'},synth_native=Mock(side_effect=RuntimeError('provider failed')))
        self.assertEqual(out.read_bytes(),b'previous recording')
    def fixture(self,chunks=False,missing_quiz=False):
        c={'language':'en-US','narration':{'engine':'elevenlabs','voice_id':'Leo','model_id':'eleven_v4','speed':1.18},'modules':[]}
        for n in [1,2]:
            a={'script_file':f'audio/module{n}/slide.txt','wav_file':f'audio/module{n}/slide.wav'}
            p=self.root/a['script_file'];p.parent.mkdir(parents=True);p.write_text('Complete approved script.')
            write_tone(self.root/a['wav_file'],5)
            if chunks and n==1:a['synthesis_chunks']=['Complete approved','script.']
            s={'id':1,'type':'knowledge_check' if missing_quiz else 'content','audio':a}
            if missing_quiz and n==1:s.pop('audio')
            c['modules'].append({'id':n,'slides':[s]})
        (self.root/'course.json').write_text(json.dumps(c))
    def run_course(self):
        calls=[]
        def synth(text,path,voice,model,language,speed):calls.append(model);write_tone(path,6)
        args=['gen_audio.py',str(self.root/'course.json'),'--module','1','--force']
        with patch.object(gen_audio.sys,'argv',args),patch.dict(os.environ,{'ELEVENLABS_API_KEY':'test-key'}),patch.object(gen_audio,'validate_model_language',return_value='verified'),patch.object(gen_audio,'validate_voice_model',return_value='verified'),patch.object(gen_audio,'synth_elevenlabs',side_effect=synth):gen_audio.main()
        return calls
    def test_module_selection_preserves_other_audio_and_metadata(self):
        self.fixture();other=(self.root/'audio/module2/slide.wav').read_bytes();meta=(self.root/'course.json').read_bytes()
        self.assertEqual(self.run_course(),['eleven_v4'])
        self.assertEqual((self.root/'audio/module2/slide.wav').read_bytes(),other);self.assertEqual((self.root/'course.json').read_bytes(),meta)
    def test_paragraphs_are_paced_after_complete_assembly(self):
        self.fixture(chunks=True);self.assertEqual(self.run_course(),['eleven_v4','eleven_v4'])
        self.assertAlmostEqual(audio_pacing.wav_duration(self.root/'audio/module1/slide.wav'),12/1.18,delta=.05)
    def test_missing_knowledge_check_stops_before_paid_text(self):
        self.fixture(missing_quiz=True)
        with self.assertRaisesRegex(SystemExit,'missing audio'):self.run_course()
    def test_professional_voice_identity_is_verified(self):
        self.assertIn('full v4',validate_voice_model('eleven_v4','Leo',voice_metadata={'voice_id':'Leo','category':'professional'}))
        with self.assertRaises(RuntimeError):validate_voice_model('eleven_v4','Leo',voice_metadata={'voice_id':'wrong'})

if __name__=='__main__':unittest.main()

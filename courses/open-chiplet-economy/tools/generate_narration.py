"""Prompt securely for a key; never save it in the course or command arguments."""
import getpass,os,pathlib,runpy,sys
root=pathlib.Path(__file__).resolve().parents[1]
if not os.environ.get('ELEVENLABS_API_KEY'):
 os.environ['ELEVENLABS_API_KEY']=getpass.getpass('ElevenLabs API key (hidden): ')
sys.path.insert(0,str(root/'tools/academy_wizard/scripts'))
sys.argv=[str(root/'tools/academy_wizard/scripts/gen_audio.py'),str(root/'course.json'),*sys.argv[1:]]
runpy.run_path(sys.argv[0],run_name='__main__')

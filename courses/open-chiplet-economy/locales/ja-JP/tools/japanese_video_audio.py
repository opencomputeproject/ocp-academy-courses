"""Prepare Japanese voice masters, timed captions and narration/music video mixes.

Requires generated v4 masters and their pacing receipts. Keys come from the
process environment or a hidden prompt; no credentials are persisted.
"""
from pathlib import Path
import argparse,concurrent.futures,difflib,getpass,hashlib,json,os,re,subprocess,sys,tempfile,wave
import requests
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'_narration_work'
SOURCE=ROOT.parents[1]
SHARED=Path(os.environ.get('ACADEMY_WIZARD_SKILL_DIR',ROOT.parents[3]/'skills/academy-wizard'))
sys.path.insert(0,str(ROOT/'tools/academy_wizard/scripts'))
from audio_pacing import match_wav_duration


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def run(args):return subprocess.run(list(map(str,args)),check=True,capture_output=True,text=True)
def ffmpeg():
    from shutil import which
    value=os.environ.get('FFMPEG') or which('ffmpeg')
    if not value:raise RuntimeError('FFmpeg is required on PATH or through FFMPEG')
    return value

def duration(path):
    result=subprocess.run([ffmpeg(),'-hide_banner','-i',str(path)],capture_output=True,text=True)
    match=re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)',result.stderr)
    if not match:raise RuntimeError('Cannot read media duration: '+str(path))
    return int(match[1])*3600+int(match[2])*60+float(match[3])


def synthesize():
    """Recreate reproducible paid recording jobs from approved source scripts."""
    course=json.loads((ROOT/'course.json').read_text());jobs=[];slides=[]
    for module in course['modules']:
        for slide in module['slides']:
            figure=slide.get('figure',{})
            if figure.get('playback_mode')!='recorded':continue
            name=f'm{module["id"]}s{slide["id"]}'
            script=f'video_source/narration/{name}.ja.txt'
            transcript=(ROOT/script).read_text().strip()
            wav=f'_narration_work/dubbing/{name}.wav'
            jobs.append({'name':name,'module':module['id'],'slide':slide['id'],
                         'source_video':figure['path'],'voice_wav':wav,'transcript':transcript})
            slides.append({'id':len(slides)+1,'type':'content_diagram','audio':{
                'script_file':script,'wav_file':wav,'approved':True,
                'synthesis_chunks':[p for p in transcript.split('\n\n') if p.strip()]}})
    destination=WORK/'dubbing';destination.mkdir(parents=True,exist_ok=True)
    (destination/'jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2)+'\n')
    job_course={'language':'ja-JP','course_slug':'chiplet_ja_video_dubbing',
                'narration':course['narration'],'modules':[{'id':10,'slides':slides}]}
    target=ROOT/'_dub-course.json';target.write_text(json.dumps(job_course,ensure_ascii=False,indent=2)+'\n')
    key=os.environ.get('ELEVENLABS_API_KEY') or getpass.getpass('ElevenLabs API key (hidden): ')
    environment={**os.environ,'ELEVENLABS_API_KEY':key}
    try:
        subprocess.run([sys.executable,str(ROOT/'tools/academy_wizard/scripts/gen_audio.py'),
                        str(target),'--module','10','--audio-work-dir',str(WORK/'pacing')],
                       env=environment,check=True)
    finally:environment.pop('ELEVENLABS_API_KEY',None);key=None


def prepare():
    jobs=json.loads((WORK/'dubbing/jobs.json').read_text())
    receipts={}
    for file in (WORK/'pacing').glob('*/receipt.json'):
        item=json.loads(file.read_text());receipts[item['output']]=item
    music=sorted([{'path':str(p),'name':p.name,'duration':duration(p),'sha256':digest(p)}
                  for p in (SHARED/'assets/background-music').glob('*.mp3')],key=lambda x:x['duration'],reverse=True)
    if len(music)!=3:raise ValueError('The maintained three-track music library is required')
    for job in jobs:job['duration']=duration(SOURCE/job['source_video'])
    ordered=sorted(jobs,key=lambda j:j['duration'],reverse=True)
    # Balanced counts 5/5/4; longest assets accompany the longest recordings.
    allocation=[music[0]]*5+[music[1]]*5+[music[2]]*4
    for job,track in zip(ordered,allocation):job['music']=track
    output=[]
    for job in jobs:
        name=job['name'];raw=ROOT/job['voice_wav'];receipt=receipts[str(raw.resolve())]
        native=Path(receipt['native_master']);target=job['duration']-1.2
        master=WORK/f'voice-only/{name}.wav';matched=WORK/f'voice-only/{name}.matched.wav'
        master.parent.mkdir(parents=True,exist_ok=True)
        pacing=match_wav_duration(native,matched,target,ffmpeg=ffmpeg())
        run([ffmpeg(),'-hide_banner','-loglevel','error','-y','-i',matched,
             '-af',f'adelay=600:all=1,apad=whole_dur={job["duration"]},atrim=duration={job["duration"]}',
             '-ar','22050','-ac','1','-c:a','pcm_s16le',master])
        script=ROOT/f'video_source/narration/{name}.ja.txt';script.parent.mkdir(parents=True,exist_ok=True)
        script.write_text(job['transcript']+'\n')
        output.append({**job,'source_video_sha256':digest(SOURCE/job['source_video']),
                       'script_file':str(script.relative_to(ROOT)),'voice_master':str(master.relative_to(ROOT)),
                       'voice_master_sha256':digest(master),'native_v4_sha256':digest(native),
                       'alignment_pacing':pacing,'music_repeated':job['music']['duration']+.05<job['duration']})
    (WORK/'dubbing/prepared.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print('Prepared fourteen complete voice masters; music usage 5/5/4.',flush=True)


def transcribe(name,path,key):
    cache=WORK/'alignments'/f'{name}.json';sha=digest(path)
    if cache.exists():
        data=json.loads(cache.read_text())
        if data['source_sha256']==sha:return name,data['transcription']
    with tempfile.TemporaryDirectory(prefix='academy-ja-asr-') as temp:
        mono=Path(temp)/'audio.wav'
        run([ffmpeg(),'-hide_banner','-loglevel','error','-y','-i',path,'-ac','1','-ar','16000','-c:a','pcm_s16le',mono])
        with mono.open('rb') as stream:
            response=requests.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':key},
                data={'model_id':'scribe_v2','language_code':'jpn','timestamps_granularity':'word',
                      'diarize':'false','tag_audio_events':'false'},
                files={'file':('audio.wav',stream,'audio/wav')},timeout=(30,300))
        if not response.ok:raise RuntimeError(f'{name}: ASR HTTP {response.status_code}')
        payload=response.json()
    if not payload.get('words') or not payload.get('text'):raise ValueError(name+': empty Japanese ASR result')
    cache.parent.mkdir(parents=True,exist_ok=True)
    cache.write_text(json.dumps({'provider':'ElevenLabs','model':'scribe_v2','language':'ja',
        'source_sha256':sha,'transcription':payload},ensure_ascii=False,indent=2)+'\n')
    print(name+': Japanese speech timing saved',flush=True)
    return name,payload


def align():
    c=json.loads((ROOT/'course.json').read_text());jobs=[]
    selected={(2,3),(3,4),(6,5),(7,3),(8,4),(1,3),(1,4),(1,10),(3,7),(3,10),(4,2),(4,3),(4,7),(5,3),(5,4),(5,8),(5,9),(6,4),(7,5),(7,6),(7,8),(9,6),(9,13)}
    for module in c['modules']:
        for slide in module['slides']:
            if (module['id'],slide['id']) in selected:
                jobs.append((f'narration-m{module["id"]}s{slide["id"]}',ROOT/slide['audio']['wav_file']))
    for job in json.loads((WORK/'dubbing/prepared.json').read_text()):jobs.append((job['name'],ROOT/job['voice_master']))
    key=os.environ.get('ELEVENLABS_API_KEY') or getpass.getpass('ElevenLabs API key (hidden): ')
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures=[pool.submit(transcribe,name,path,key) for name,path in jobs]
            for future in concurrent.futures.as_completed(futures):future.result()
    finally:key=None
    print('Japanese speech verification and timing complete.',flush=True)


def timestamp(seconds):
    ms=round(seconds*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'

def approved_timing(payload,approved):
    """Use approved orthography with actual word times; retain raw ASR in audit."""
    heard=[];times=[]
    for word in payload['words']:
        if word.get('type') in ['spacing','audio_event']:continue
        token=''.join(c for c in word.get('text','') if not c.isspace())
        if not token:continue
        start=float(word['start']);end=float(word['end'])
        for index,char in enumerate(token):
            heard.append(char);times.append((start+(end-start)*index/len(token),start+(end-start)*(index+1)/len(token)))
    target=''.join(c for c in approved if not c.isspace())
    matcher=difflib.SequenceMatcher(None,''.join(heard),target,autojunk=False)
    aligned=[None]*len(target)
    for action,a,b,x,y in matcher.get_opcodes():
        if x==y:continue
        if action=='equal':
            aligned[x:y]=times[a:b]
        else:
            left=times[a][0] if a<len(times) else times[-1][1]
            right=times[b-1][1] if b>a else left
            for index in range(x,y):aligned[index]=(left+(right-left)*(index-x)/(y-x),left+(right-left)*(index-x+1)/(y-x))
    words=[];index=0
    for char in approved.replace('\n',''):
        if char.isspace():
            previous=words[-1]['end'] if words else 0
            words.append({'text':' ','start':previous,'end':previous,'type':'word'});continue
        start,end=aligned[index];index+=1
        words.append({'text':char,'start':start,'end':end,'type':'word'})
    return {'text':approved,'words':words,'recognition_similarity':matcher.ratio()}


def caption_cues(payload,end):
    # Japanese captions use short two-line phrases and the actual voice timing.
    words=[w for w in payload['words'] if w.get('type') not in ['spacing','audio_event'] and str(w.get('text',''))!='']
    groups=[];text='';start=None;finish=0
    for w in words:
        token=w['text'];a=float(w['start']);b=float(w['end'])
        if text and (len(text+token)>36 or b-start>5 or a-finish>.75):
            groups.append([start,finish,text]);text='';start=None
        if start is None:start=a
        text+=token;finish=b
        if text and text[-1] in '\u3002\uff01\uff1f!?':groups.append([start,finish,text]);text='';start=None
    if text:groups.append([start,finish,text])
    cues=[]
    for i,(a,b,value) in enumerate(groups):
        next_start=groups[i+1][0] if i+1<len(groups) else end
        b=min(end,next_start-.04,max(b,min(a+1.3,next_start-.04)))
        a=max(0,a);b=max(a+.1,b)
        value=value.strip();lines=[value[j:j+18].strip() for j in range(0,len(value),18)]
        if len(lines)>2:raise ValueError('Caption phrase exceeds the two-line budget')
        cues.append({'start':a,'end':b,'text':'\n'.join(lines)})
    return cues


def captions():
    course_path=ROOT/'course.json';c=json.loads(course_path.read_text());count=0
    for job in json.loads((WORK/'dubbing/prepared.json').read_text()):
        data=json.loads((WORK/f'alignments/{job["name"]}.json').read_text())['transcription']
        data=approved_timing(data,job['transcript'])
        if data['recognition_similarity']<.8:raise ValueError(job['name']+': Japanese ASR mismatch needs review')
        print(job['name']+': approved-text alignment '+str(round(data['recognition_similarity'],3)),flush=True)
        cues=caption_cues(data,job['duration'])
        if cues and cues[0]['start']>=.5:cues.insert(0,{'start':0,'end':cues[0]['start']-.04,'text':'[\u97f3\u697d]'})
        if cues and job['duration']-cues[-1]['end']>=.5:cues.append({'start':cues[-1]['end']+.04,'end':job['duration'],'text':'[\u97f3\u697d]'})
        target=ROOT/f'captions/{job["name"]}.ja.vtt';target.parent.mkdir(exist_ok=True)
        target.write_text('WEBVTT\n\n'+'\n\n'.join(f'{i}\n{timestamp(q["start"])} --> {timestamp(q["end"])}\n{q["text"]}' for i,q in enumerate(cues,1))+'\n')
        slide=next(s for m in c['modules'] if m['id']==job['module'] for s in m['slides'] if s['id']==job['slide'])
        slide['figure']['captions']=[{'path':str(target.relative_to(ROOT)),'language':'ja-JP','label':'\u65e5\u672c\u8a9e','default':False}]
        count+=len(cues)
    course_path.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    print('Fourteen Japanese caption tracks:',count,'cues',flush=True)


def mix():
    records=[]
    for job in json.loads((WORK/'dubbing/prepared.json').read_text()):
        report=WORK/f'dubbing/{job["name"]}.mix.json'
        args=[sys.executable,str(ROOT/'tools/academy_wizard/scripts/mix_localized_video.py'),
              '--video',str(SOURCE/job['source_video']),'--voice',str(ROOT/job['voice_master']),
              '--music',job['music']['path'],'--output',str(ROOT/job['source_video']),
              '--language-tag','jpn','--audio-title','Japanese narration with background music',
              '--report-json',str(report)]
        subprocess.run(args,check=True,env={**os.environ,'FFMPEG':ffmpeg()})
        record={k:v for k,v in job.items() if k!='transcript'}
        record['music']={k:v for k,v in record['music'].items() if k!='path'}
        record['voice']={'model_id':'eleven_v4','voice_id':'b34JylakFZPlGS0BnwyY','language':'ja-JP'}
        record['output_sha256']=digest(ROOT/job['source_video']);record['source_audio_mapped']=False
        records.append(record)
    (ROOT/'video_source/dubbing-ja-production.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    print('Fourteen localized recordings mixed; source audio was never mapped.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['synthesize','prepare','align','captions','mix']);args=parser.parse_args()
    globals()[args.action]()

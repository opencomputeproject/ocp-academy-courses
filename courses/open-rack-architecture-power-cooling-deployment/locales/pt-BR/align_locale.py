"""Refresh a locale's spoken visual cues after deliberately regenerating its narration.

Usage from a locale source folder: python align_locale.py m2s4
ELEVENLABS_API_KEY is read only from the caller's environment. Alignment does not synthesize audio.
"""
import argparse, hashlib, json, os, re, subprocess, sys, unicodedata, urllib.request, uuid, wave
from pathlib import Path
def read(p):return json.loads(p.read_text('utf-8'))
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n','utf-8')
def norm(s):return ''.join(ch for ch in unicodedata.normalize('NFKC',s).casefold() if ch.isalnum())
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('slide');arg=parser.parse_args()
    key=arg.slide;m,s=map(int,re.fullmatch(r'm(\d+)s(\d+)',key).groups());r=Path(__file__).resolve().parent
    cp=r/'course.json';c=read(cp);sl=c['modules'][m-1]['slides'][s-1];a=sl['audio']
    ap=r/a['wav_file'];audio=ap.read_bytes();tx='\n'.join(x for x in (r/a['script_file']).read_text().splitlines() if not x.startswith('#')).strip();h=hashlib.sha256(audio).hexdigest()
    with wave.open(str(ap)) as w:duration=w.getnframes()/w.getframerate()
    mp=r/'localization/media.json';man=read(mp);cues=read(r/'localization/cues.json')[key]
    boundary=uuid.uuid4().hex;pre=f'--{boundary}\r\nContent-Disposition: form-data; name="text"\r\n\r\n{tx}\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="narration.wav"\r\nContent-Type: audio/wav\r\n\r\n'
    req=urllib.request.Request('https://api.elevenlabs.io/v1/forced-alignment',data=pre.encode()+audio+f'\r\n--{boundary}--\r\n'.encode(),headers={'xi-api-key':os.environ['ELEVENLABS_API_KEY'],'Content-Type':f'multipart/form-data; boundary={boundary}'})
    with urllib.request.urlopen(req,timeout=180) as res:data=json.load(res)
    units=data.get('characters') or data['words'];text='';times=[]
    for u in units:
        part=norm(u['text']);text+=part;times.extend([u['start']]*len(part))
    cursor=0;frames=[0]
    for cue in cues:
        phrase=norm(cue);idx=text.find(phrase,cursor)
        if idx<0:raise ValueError(f'Cue no longer matches recording: {cue}')
        frames.append(round(times[idx]*24));cursor=idx+len(phrase)
    frames.append(round(duration*24));assert all(x<y for x,y in zip(frames,frames[1:]))
    if key=='m1s4':
        track=sl['timed_points'];assert len(track['points'])==len(frames)-1
        for p,n in zip(track['points'],frames):p['at']=round(n/24,4)
        track['master_sha256']=h
    else:
        man['scenes'][key].update(frames=frames,duration=duration,narration_sha256=h,cue_phrases=cues)
        save(mp,man);subprocess.run([sys.executable,str(r/'render_localized.py'),key],check=True)
        review=read(r/'localization/media-qa'/(key+'.json'));sl['figure'].update(duration_seconds=review['duration_seconds'],text_inventory=review['text_inventory'])
        sl['figure']['localized_timing']['audio_sha256']=h
    save(cp,c)
if __name__=='__main__':main()

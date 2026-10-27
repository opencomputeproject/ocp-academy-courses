"""Sample or export exactly one measured narration pass per FCSA sequence."""
from pathlib import Path
import importlib,json,argparse,math
ROOT=Path(__file__).resolve().parents[2];WORK=ROOT/'_video_work/synced-pilots';AUDIT=ROOT/'audit/synced-video-production';FPS=30
KEYS={'m1':'M1S3','m2':'M2S3','m3':'M3S5','m4':'M4S4','m5':'M5S3'}
def item(name):
 d=json.loads((ROOT/'video_source/video-timing.json').read_text())[KEYS[name]]
 return {'id':KEYS[name],'duration':d['duration'],'boundaries':d['scene_starts']+[d['duration']],'poster_seconds':d['duration']-1,'stem':name+'-teaching-sequence','events':[]}
ITEMS={n:item(n) for n in KEYS if KEYS[n] in json.loads((ROOT/'video_source/video-timing.json').read_text())}
def times(v):
 d=v['duration'];b=v['boundaries'];ts=[0,d*.25,d*.5,d*.75,d-1/FPS]
 for a,z in zip(b,b[1:]):
  ts += [a,(a+z)/2,z-1/FPS]
  for f in [.1,.15,.25,.35,.5,.65,.7,.75,.85,.9,.95]:ts += [a+(z-a)*f-1/FPS,a+(z-a)*f,a+(z-a)*f+1/FPS]
 for t in b[1:-1]:ts += [t-1/FPS,t,t+1/FPS]
 return sorted(set(round(max(0,min(d-1/FPS,t)),5) for t in ts))
def main():
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['samples','encode']);p.add_argument('--only',choices=KEYS);a=p.parse_args();WORK.mkdir(parents=True,exist_ok=True);AUDIT.mkdir(parents=True,exist_ok=True)
 for name in ([a.only] if a.only else ITEMS):
  v=item(name);m=importlib.import_module('tools.synced_video.'+name)
  if a.mode=='samples':
   out=AUDIT/'native-svgs'/name;out.mkdir(parents=True,exist_ok=True)
   for f in out.glob('*.svg'):f.unlink()
   inv={}
   for i,t in enumerate(times(v)):
    f=out/f'{i:03d}-{t:08.3f}.svg';f.write_text(m.render(t));inv[f.name]=t
   (out/'times.json').write_text(json.dumps(inv,indent=2));(out/f'poster-{v["poster_seconds"]:.3f}.svg').write_text(m.render(round(v['poster_seconds']*FPS)/FPS));print(name,len(inv),'source samples',flush=True)
  else:
   count=round(v['duration']*FPS)
   with (WORK/f'{name}-frames.jsonl').open('w') as f:
    for i in range(count):f.write(json.dumps({'frame':i,'svg':m.render(i/FPS)})+'\n')
   print(name,count,'lossless source frames',flush=True)
if __name__=='__main__':main()

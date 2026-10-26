"""Lossless deterministic vector sampling and exactly-one-pass media production.

Run from the course root: python3 -m tools.synced_video.produce samples|encode.
The encoded assets are staged under _video_work until explicitly integrated.
"""
import argparse, importlib, json, math, pathlib, subprocess

ROOT=pathlib.Path(__file__).resolve().parents[2]
WORK=ROOT/'_video_work/synced-pilots'
AUDIT=ROOT/'audit/synced-video-production'
FPS=30
ITEMS={
 'm1':{'id':'M1S3','duration':43.748662131519275,'stem':'m1-the-project-connects-three-kinds-of-work','poster_seconds':42.8,
       'boundaries':[0,7.86,10.50,13.78,16.76,19.60,24.22,30.56,33.78,39.32,43.748662131519275],
       'events':[4.44,6.68,8.32,9.60,11.74,12.84,14.34,15.02,17.72,18.65,20.38,21.44,22.26,23.40,25.62,26.88,27.84,28.94,35.0,35.95,36.42,37.25,37.72,38.60]},
 'm4':{'id':'M4S3','duration':39.52285714285714,'stem':'m4-a-transaction-crosses-three-agreements','poster_seconds':39.1,
       'boundaries':[0,4.84,9.04,12.26,16.94,19.80,24.56,29.16,33.06,39.52285714285714],
       'events':[2.84,4.10,5.48,6.22,7.04,7.94,9.72,10.08,11.40,14.16,14.78,15.84,22.04,25.80,26.72,27.36,27.52,28.14,30.62,31.60,34.24,37.8,38.96]},
 'm5':{'id':'M5S3','duration':41.65963718820862,'stem':'m5-test-what-exists-at-each-stage','poster_seconds':40.5,
       'boundaries':[0,4.54,8.02,12.20,15.76,19.36,23.28,28,32.82,34.78,37.66,41.65963718820862],
       'events':[.35,1.1,1.5,2.3,2.9,3.2,3.74,8.1,9.5,14.04,20.34,21.24,28.10,29.4,30,31.26,39.84]},
 'm9':{'id':'M9S6','duration':42.67954648526077,'stem':'m9-from-a-catalog-to-an-evaluable-system','poster_seconds':42.3,
       'boundaries':[0,3.24,9.38,17.08,19.76,27.42,33.24,38.34,42.67954648526077],
       'events':[5.86,10.2,11.74,11.86,13.38,21.38,23.18,41.36]}}

from .japanese_timing import TIMING,japanese_time
for _name,_item in ITEMS.items():
    _item['duration']=TIMING[_name]['duration_seconds']
    _item['poster_seconds']=_item['duration']-.4
    _item['boundaries']=[japanese_time(_name,t) for t in _item['boundaries']]
    _item['events']=[japanese_time(_name,t) for t in _item['events']]

def times(item):
    b=item['boundaries'];d=item['duration']
    ts=[0,d-1/FPS,d*.25,d*.5,d*.75]
    for a,z in zip(b,b[1:]):ts += [a,(a+z)/2,z-1/FPS]
    for t in item['events']+b[1:-1]:ts += [t-1/FPS,t,t+1/FPS]
    return sorted(set(round(max(0,min(d-1/FPS,t)),5) for t in ts))

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['samples','encode']);p.add_argument('--only',choices=ITEMS)
    args=p.parse_args();WORK.mkdir(parents=True,exist_ok=True);AUDIT.mkdir(parents=True,exist_ok=True)
    selected=[args.only] if args.only else list(ITEMS)
    for name in selected:
        item=ITEMS[name];mod=importlib.import_module(f'tools.synced_video.{name}')
        if args.mode=='samples':
            out=AUDIT/'native-svgs'/name;out.mkdir(parents=True,exist_ok=True)
            # This directory contains only regenerable samples from this source.
            for old in out.glob('*.svg'):old.unlink()
            inventory={}
            for i,t in enumerate(times(item)):
                f=out/f'{i:03d}-{t:08.3f}.svg';f.write_text(mod.render(t));inventory[f.name]=t
            (out/'times.json').write_text(json.dumps(inventory,indent=2)+'\n')
            poster=item['poster_seconds']
            (out/f'poster-{poster:.3f}.svg').write_text(mod.render(round(poster*FPS)/FPS))
            print(name,len(inventory),'native vector samples',flush=True)
        else:
            frames=round(item['duration']*FPS)
            f=WORK/f'{name}-frames.jsonl'
            with f.open('w') as stream:
                for i in range(frames):stream.write(json.dumps({'frame':i,'svg':mod.render(i/FPS)})+'\n')
            print(name,frames,'lossless source frames exported',flush=True)

if __name__=='__main__':main()

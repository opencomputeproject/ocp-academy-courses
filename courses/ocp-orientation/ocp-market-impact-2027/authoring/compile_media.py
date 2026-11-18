"""Prepare deterministic vector frames on the timed narration and encode one pass."""
import argparse
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from artwork import artwork, CUES
from record import HERE, COURSE, find_ffmpeg

FPS=24
def prepare(n,folder):
    folder.mkdir(parents=True,exist_ok=True)
    recording=HERE/'Recordings'/f'slide_{n:02}'
    alignment=json.loads((recording/'timing.json').read_text())
    receipt=json.loads((recording/'receipt.json').read_text())
    words=''.join(alignment['characters'])
    starts=alignment['character_start_times_seconds']
    ends=alignment['character_end_times_seconds']
    phrases=CUES[n]
    cues=[starts[words.lower().index(phrase.lower())]/receipt['tempo_factor'] for phrase in phrases]
    duration=receipt['final_seconds']
    data={'fps':FPS,'duration':duration,'cues':dict(zip(phrases,cues))}
    if n==3:
        last=words.index('Make your guess.')+len('Make your guess.')-1
        data['prediction_pause']=ends[last]/receipt['tempo_factor']
    path=HERE/'Scenes';path.mkdir(exist_ok=True)
    (path/f'slide_{n:02}.json').write_text(json.dumps(data,indent=2))
    frames=round(duration*FPS)
    order=[];old=None;captions=OrderedDict()
    for i in range(frames):
        svg=artwork(n,i/FPS,cues)
        if svg!=old:
            name=f'f{len(order):04d}'
            (folder/(name+'.svg')).write_text(svg)
            order.append([name,1])
            for item in ET.fromstring(svg).iter('{http://www.w3.org/2000/svg}text'):
                captions.setdefault(item.text,i/FPS)
            old=svg
        else:order[-1][1]+=1
    (folder/'timeline.json').write_text(json.dumps(order))
    (path/f'slide_{n:02}_labels.json').write_text(json.dumps([{'text':k,'at_seconds':v} for k,v in captions.items() if k],ensure_ascii=False))
    (path/f'slide_{n:02}_end.svg').write_text(old)
    print(f'Slide {n}: {len(order)} distinct states / {frames} frames',flush=True)

def encode(n,folder):
    order=json.loads((folder/'timeline.json').read_text())
    subprocess.run(['node',str(HERE/'raster.cjs'),str(folder)],check=True)
    lines=['ffconcat version 1.0']
    for name,count in order:
        lines+=["file '"+name+".png'",'option framerate 24',f'duration {count/FPS:.8f}']
    lines+=["file '"+order[-1][0]+".png'",'option framerate 24']
    (folder/'frames.ffconcat').write_text('\n'.join(lines)+'\n')
    out=COURSE/'figures'/f'scene_{n:02}.mp4'
    temporary=out.with_name(out.stem+'.new.mp4')
    subprocess.run([find_ffmpeg(),'-nostdin','-loglevel','error','-y','-f','concat','-safe','0','-i',str(folder/'frames.ffconcat'),'-an','-vf','fps=24,scale=out_color_matrix=bt709','-frames:v',str(sum(x[1] for x in order)),'-c:v','libx264','-preset','veryfast','-crf','9','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-threads','3',str(temporary)],check=True)
    temporary.replace(out)
    poster_name=order[-1][0]
    if n==3:
        wait=json.loads((HERE/'Scenes/slide_03.json').read_text())['prediction_pause']
        elapsed=0
        for name,count in order:
            elapsed+=count
            if elapsed/FPS>=wait-0.5:
                poster_name=name
                break
    (out.with_suffix('.png')).write_bytes((folder/(poster_name+'.png')).read_bytes())
    print(f'Slide {n}: encoded {out.stat().st_size:,} bytes',flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=['prepare','encode'])
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('slides',type=int,nargs='*')
    args=ap.parse_intermixed_args()
    def run(n):
        folder=args.work/f'slide_{n:02}'
        (prepare if args.mode=='prepare' else encode)(n,folder)
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,args.slides or CUES))

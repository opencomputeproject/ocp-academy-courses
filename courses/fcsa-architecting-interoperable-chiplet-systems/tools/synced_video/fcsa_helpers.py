"""FCSA-only scene/timing helpers; no course, audio or runtime side effects."""
from .primitives import *
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
_STORY = json.loads((ROOT/'video_source/storyboards/fcsa_video_storyboards.json').read_text())
_PLANS = {s['slide_id']:s for s in _STORY['sequences']}
_cache_stamp = None
_cache = {}


def timing(key):
    """Pick up alignment even if the file appears after this module is imported."""
    global _cache_stamp, _cache
    file = ROOT/'video_source/video-timing.json'
    stamp = file.stat().st_mtime_ns if file.exists() else None
    if stamp != _cache_stamp:
        data = json.loads(file.read_text()) if stamp is not None else {}
        _cache, _cache_stamp = data, stamp
    if key in _cache:
        v = _cache[key]
        starts, ends = v['scene_starts'], v['scene_ends']
        if len(starts) != len(_PLANS[key]['scenes']) or len(ends) != len(starts):
            raise ValueError(f'{key}: aligned scene count differs from storyboard')
        return float(v['duration']), list(map(float, starts)), list(map(float, ends))
    s = _PLANS[key]
    return float(s['duration_seconds_provisional']), [v['start'] for v in s['scenes']], [v['end'] for v in s['scenes']]


def scene(t, key):
    duration, starts, ends = timing(key)
    t = max(0.0, min(float(t), duration))
    i = max(i for i, start in enumerate(starts) if t >= start)
    end = ends[i]
    if i == len(starts)-1:
        end = max(starts[i]+.1, min(end, duration-2))
    p = max(0.0, min(1.0, (t-starts[i])/max(.1,end-starts[i])))
    return i, p


def phase(p, start=.15, end=.7):
    return smooth(p, start, end)


def title(label, sub=''):
    return [text(960,120,label,60), *([text(960,215,sub,48)] if sub else [])]


def centered(x, y, label, size=48, color=INK, weight=600):
    return text(x,y+size*.27-(len(label.split('\n'))-1)*size*.625,label,size,color,weight)


def unit(x,y,w,h,label,accent=False):
    return chip(x,y,w,h,'',accent)+centered(x+w/2,y+h/2,label,50)


def paper(x,y,w,h,label='',accent=False,size=48):
    fold=26
    col=GREEN if accent else GRAY
    return (path(f'M{x} {y} H{x+w-fold} L{x+w} {y+fold} V{y+h} H{x} Z',col,5,WHITE)
            +path(f'M{x+w-fold} {y} V{y+fold} H{x+w}',col,4)
            +(centered(x+w/2,y+h/2,label,size) if label else ''))


def open_scope(x1,x2,y,label):
    return path(f'M{x1} {y-22} V{y} H{x2} V{y-22}',GRAY,5)+text((x1+x2)/2,y+78,label,50)


def tag(x,y,label,w=400,h=150,accent=False):
    return rect(x,y,w,h,WHITE,GREEN if accent else GRAY,5,16)+centered(x+w/2,y+h/2,label,48)


def pulse(x1,y1,x2,y2,p):
    """One emphasis mark along an existing relation; never an approval."""
    if not 0 <= p <= 1:return ''
    x,y=lerp(x1,x2,p),lerp(y1,y2,p)
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="13" fill="{GREEN}"/>'


def nvm(x,y,label='NVM',w=420,h=145):
    return rect(x,y,w,h,WHITE,GRAY,5,7)+line(x+25,y+26,x+w-25,y+26,GRAY,4)+centered(x+w/2,y+h/2+12,label,48)


def role(x,y,label,active=False):
    # The small open disc marks a function; text sits to its right, uncontained.
    return (f'<circle cx="{x}" cy="{y-15}" r="15" fill="{GREEN if active else WHITE}" stroke="{GRAY}" stroke-width="4"/>'
            +text(x+42,y,label,48,anchor='start'))

"""Bidirectional interpolation over reviewed Japanese narration landmarks."""
from pathlib import Path
import bisect,json
ROOT=Path(__file__).resolve().parents[2]
TIMING=json.loads((ROOT/'video_source/timing-ja.json').read_text())
def convert(name,value,source,target):
    rows=TIMING[name]['anchors'];x=[r[source] for r in rows];y=[r[target] for r in rows]
    if value<=x[0]:return y[0]
    if value>=x[-1]:return y[-1]
    i=bisect.bisect_right(x,value)-1
    return y[i]+(y[i+1]-y[i])*(value-x[i])/(x[i+1]-x[i])
def english_time(name,seconds):return convert(name,seconds,'japanese_seconds','english_seconds')
def japanese_time(name,seconds):return convert(name,seconds,'english_seconds','japanese_seconds')

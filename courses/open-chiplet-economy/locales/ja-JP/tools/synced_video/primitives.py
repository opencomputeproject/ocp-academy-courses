"""Shared SVG geometry. Coordinates are native 1920 × 1080 pixels."""
from html import escape
import math
import json
from functools import lru_cache
from pathlib import Path
from tools.japanese_media import translate,layout

INK = '#5F6062'
GRAY = '#9CA3AF'
GREEN = '#8DC63F'
PALE = '#F3F6EF'
WHITE = '#FFFFFF'

def svg(parts):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="1080" fill="white"/>'+''.join(parts)+'</svg>'

def text(x, y, value, size=52, color=INK, weight=600, anchor='middle'):
    value,size=layout(value,size,weight)
    lines=str(value).split('\n')
    content=''.join(f'<tspan x="{x:.3f}" dy="{0 if i==0 else size*1.25:.3f}">{escape(s)}</tspan>' for i,s in enumerate(lines))
    return f'<text x="{x:.3f}" y="{y:.3f}" text-anchor="{anchor}" font-family="Noto Sans JP,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{content}</text>'

def rect(x,y,w,h,fill=PALE,stroke=GRAY,width=4,rx=20):
    return f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'

def line(x1,y1,x2,y2,color=INK,width=6,dash=None):
    return f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'

@lru_cache(maxsize=64)
def _phrase_bounds(full,phrase,size,weight):
    """Use the same bundled variable font and weight as SVG rasterization."""
    full=translate(full);phrase=translate(phrase)
    measured=Path(__file__).with_name('font_metrics.json')
    if measured.exists():
        key=json.dumps([full,phrase,size,weight],ensure_ascii=False,separators=(',',':'))
        bounds=json.loads(measured.read_text())['bounds']
        if key in bounds:return tuple(bounds[key])
    from PIL import ImageFont
    font=ImageFont.truetype(str(Path(__file__).resolve().parents[2]/'fonts/NotoSansJP[wght].ttf'),size)
    font.set_variation_by_axes([weight])
    index=full.index(phrase)
    origin=-font.getlength(full)/2+font.getlength(full[:index])
    ink=font.getbbox(phrase,anchor='ls')
    return origin+ink[0],origin+ink[2]

def underline_phrase(x,baseline,full,phrase,size=48,weight=600,gap=11,color=GREEN,width=5):
    """Align the line to the phrase's actual ink, rather than estimated pixels."""
    left,right=_phrase_bounds(full,phrase,size,weight)
    return line(x+left,baseline+gap,x+right,baseline+gap,color,width).replace('<line ',f'<line data-underline="{escape(translate(phrase))}" ',1)

def path(d,color=GRAY,width=5,fill='none',dash=None):
    return f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill}" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'

def arrow(x1,y1,x2,y2,color=GREEN,width=7,head=22):
    distance=math.hypot(x2-x1,y2-y1)
    if distance<1:return ''
    ux,uy=(x2-x1)/distance,(y2-y1)/distance
    bx,by=x2-head*ux,y2-head*uy
    px,py=-uy*head*.5,ux*head*.5
    return line(x1,y1,bx,by,color,width)+f'<polygon class="arrowhead" points="{bx+px:.3f},{by+py:.3f} {bx-px:.3f},{by-py:.3f} {x2:.3f},{y2:.3f}" fill="{color}"/>'

def chip(x,y,w,h,label='',accent=False):
    cut=min(32,w*.1)
    d=f'M{x} {y} H{x+w-cut} L{x+w} {y+cut} V{y+h} H{x} Z'
    result=path(d,GREEN if accent else GRAY,6,PALE if accent else '#F0F2F4')
    # A notch keeps the die identity visible through a move and a reframing.
    result+=line(x+28,y+h-32,x+64,y+h-32,GRAY,5)
    if label:result+=text(x+w/2,y+h/2+18-(len(label.split('\n'))-1)*32.5,label,52)
    return result

def token(x,y,label='',w=310,h=140,accent=True):
    return rect(x,y,w,h,WHITE,GREEN if accent else GRAY,6,18)+text(x+w/2,y+h/2+18,label,50)

def bracket(x1,x2,y,label='',color=GRAY,direction='down'):
    dy=24 if direction=='down' else -24
    result=path(f'M{x1} {y+dy} V{y} H{x2} V{y+dy}',color,5)
    if label:result+=text((x1+x2)/2,y-26 if dy>0 else y+70,label,48)
    return result

def smooth(t,start,end):
    if end<=start:return float(t>=end)
    p=max(0.0,min(1.0,(t-start)/(end-start)))
    return p*p*(3-2*p)

def lerp(a,b,p):return a+(b-a)*p

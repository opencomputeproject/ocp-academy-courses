"""Source-derived Japanese labels and measured font layout for teaching media."""
from pathlib import Path
import json,math,re,xml.etree.ElementTree as ET
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1]
LABELS=json.loads((ROOT/'video_source/labels.ja.json').read_text())
FONT=ROOT/'fonts/NotoSansJP[wght].ttf'
SOURCE_FONT=ROOT/'fonts/OpenSans[wdth,wght].ttf'
ET.register_namespace('','http://www.w3.org/2000/svg')

def translate(value):
    key=' '.join(str(value).split())
    if not key:return str(value)
    if key not in LABELS:raise KeyError('Untranslated media label: '+key)
    return LABELS[key]

def font(size,weight=400,japanese=True):
    f=ImageFont.truetype(str(FONT if japanese else SOURCE_FONT),max(1,round(size)))
    f.set_variation_by_axes([weight] if japanese else [weight,100])
    return f

def wrap(value,f,width):
    rows=[];line=''
    for char in re.findall(r'[A-Za-z0-9./+_-]+|[^A-Za-z0-9./+_-]',value):
        if char=='\n':rows.append(line);line='';continue
        if line and f.getlength(line+char)>width:rows.append(line);line=char
        else:line+=char
    if line:rows.append(line)
    if len(rows)>1 and len(rows[-1])<3 and len(rows[-2])>5:
        needed=3-len(rows[-1]);rows[-1]=rows[-2][-needed:]+rows[-1];rows[-2]=rows[-2][:-needed]
    return rows or ['']

def layout(value,size,weight=400,width=None):
    old=str(value).split('\n');translated=translate(value)
    width=width or max(max(font(size,weight,False).getlength(x) for x in old)+4,size*9)
    actual=size
    while True:
        rows=wrap(translated,font(actual,weight),width)
        if len(rows)<=len(old) or actual<=size*.72:break
        actual*=.95
    return '\n'.join(rows),actual

def localize_svg(text):
    root=ET.fromstring(text)
    for node in list(root.iter()):
        if node.tag.rsplit('}',1)[-1]!='text':continue
        spans=[x for x in node if x.tag.rsplit('}',1)[-1]=='tspan']
        original='\n'.join(''.join(s.itertext()) for s in spans) if spans else ''.join(node.itertext())
        if not original.strip():continue
        size=float(node.get('font-size','25'));weight=node.get('font-weight','400')
        weight=int(weight) if str(weight).isdigit() else (700 if weight=='bold' else 400)
        x=node.get('x','0');y=float(node.get('y','0'));cx=float(x)
        rectangles=[]
        for candidate in root.iter():
            if candidate.tag.rsplit('}',1)[-1]!='rect':continue
            rx=float(candidate.get('x','0'));ry=float(candidate.get('y','0'));rw=float(candidate.get('width','0'));rh=float(candidate.get('height','0'))
            if rx<=cx<=rx+rw and ry<=y<=ry+rh:rectangles.append((rw*rh,rw))
        budget=max(40,min(rectangles)[1]-40) if rectangles else None
        value,adjusted=layout(original,size,weight,budget)
        for child in list(node):node.remove(child)
        node.text=None;node.set('font-family','Noto Sans JP,sans-serif');node.set('font-size',f'{adjusted:.3f}')
        for index,line in enumerate(value.split('\n')):
            part=ET.SubElement(node,'{http://www.w3.org/2000/svg}tspan',{'x':x,'dy':'0' if index==0 else f'{adjusted*1.25:.3f}'})
            part.text=line
    return ET.tostring(root,encoding='unicode')

from pathlib import Path
import importlib,json,re,xml.etree.ElementTree as ET
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[3]
fontfile=ROOT/'fonts/OpenSans[wdth,wght].ttf'
fonts={}
def font(size,weight):
 key=(size,weight)
 if key not in fonts:
  f=ImageFont.truetype(str(fontfile),int(size));f.set_variation_by_axes([weight,100]);fonts[key]=f
 return fonts[key]
def inspect(svg):
 root=ET.fromstring(svg);shapes=[];labels=[];flags=[]
 for e in root:
  tag=e.tag.split('}')[-1]
  if tag=='rect' and e.get('width')!='1920':
   x,y,w,h=[float(e.get(k,0)) for k in ('x','y','width','height')];shapes.append((x,y,x+w,y+h))
  elif tag=='path' and e.get('fill','none')!='none':
   d=e.get('d','');m=re.match(r'M([\d.]+) ([\d.]+) H([\d.]+) L([\d.]+) ([\d.]+) V([\d.]+) H',d)
   if m:
    x,y,_,xx,_,yy=map(float,m.groups());shapes.append((x,y,xx,yy))
  elif tag=='text':
   size=float(e.get('font-size'));weight=float(e.get('font-weight'));f=font(size,weight);base=float(e.get('y'));x=float(e.get('x'));anchor=e.get('text-anchor');label=[]
   for n,node in enumerate(e):
    base+=float(node.get('dy','0'));v=node.text or '';label.append(v);b=f.getbbox(v,anchor='ls');adv=f.getlength(v);offset=adv/2 if anchor=='middle' else adv if anchor=='end' else 0
    box=(x-offset+b[0],base+b[1],x-offset+b[2],base+b[3]);labels.append((v,box,size))
    if box[0]<60 or box[1]<50 or box[2]>1860 or box[3]>1030:flags.append(('safe-area',v,box))
    containers=[s for s in shapes if s[0]<=x<=s[2] and s[1]<=base<=s[3]]
    if containers:
     c=containers[-1];pad=min(box[0]-c[0],box[1]-c[1],c[2]-box[2],c[3]-box[3]);
     if pad<size*.75-.5:flags.append(('padding',v,round(pad,2),size*.75,c))
 return flags,labels
if __name__=='__main__':
 from tools.synced_video.fcsa_helpers import timing
 summary={};unique={};samples=Path(__file__).parent
 for k in range(1,6):
  m=importlib.import_module(f'tools.synced_video.m{k}');dur,ss,ee=timing(m.KEY);texts=set();fl=[]
  times=sorted(set([n/30 for n in range(int(dur*30)+1)]+[dur]+[max(0,t-.01) for t in ss]+ss))
  for t in times:
   svg=m.render(t);f,ls=inspect(svg)
   for v,_,_ in ls:texts.add(v)
   for v in f:
    key=str(v)
    if key not in unique:unique[key]={'module':k,'time':t,'flag':v}
   fl+=f
  summary[m.KEY]={'duration':dur,'sample_count':len(times),'text_inventory':sorted(texts),'fixed_final_two_seconds':m.render(dur-2)==m.render(dur),'flag_count':len(fl)}
  for i,(a,b) in enumerate(zip(ss,ee)):
   for u in [.15,.5,.85]:
    (samples/f'm{k}-s{i+1}-{int(u*100):02d}.svg').write_text(m.render(a+(b-a)*u))
 (samples/'source-checks.json').write_text(json.dumps({'modules':summary,'unique_flags':list(unique.values())},indent=2))
 print(json.dumps({'modules':{k:{a:b for a,b in v.items() if a!='text_inventory'} for k,v in summary.items()},'unique_flags':list(unique.values())[:35]},indent=2))

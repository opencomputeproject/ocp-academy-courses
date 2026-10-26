"""Create editable vector teaching diagrams and finite animation sources."""
import json,pathlib,html,textwrap,shutil
R=pathlib.Path(__file__).resolve().parents[1]; c=json.loads((R/'course.json').read_text());A=R/'animation_sources';A.mkdir(exist_ok=True)
esc=lambda x:html.escape(str(x))
GREEN='#8DC63F';GRAY='#5F6062';INDIGO='#343895'
def text(x,y,value,size=25,color=GRAY,weight=400,width=28):
 lines=textwrap.wrap(value,width=width,break_long_words=False)
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.35}">{esc(l)}</tspan>' for i,l in enumerate(lines))+'</text>'
def rect(x,y,w,h,fill='#F4F6F1',stroke='#CCD3C7',rx=12):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def arrow(x1,y,x2,color=GREEN):
 return f'<line x1="{x1}" y1="{y}" x2="{x2-14}" y2="{y}" stroke="{color}" stroke-width="4"/><polygon class="arrowhead" points="{x2-14},{y-7} {x2-14},{y+7} {x2},{y}" fill="{color}"/>'
def row(labels,motion=False):
 result=[]
 y,h=(100,400) if motion else (155,270)
 for i,(a,b) in enumerate(labels):
  x=40+i*390
  result += [f'<g class="stage stage{i}">',rect(x,y,340,h),rect(x,y,340,8,GREEN,GREEN,0),text(x+170,180 if motion else 225,a,38 if motion else 28,INDIGO,700,13 if motion else 16),text(x+170,280 if motion else 315,b,34 if motion else 24,width=14 if motion else 22),'</g>']
  if i<2:result.append(f'<g class="route route{i}">'+arrow(x+340,300 if motion else 290,x+390)+'</g>')
 return ''.join(result)
def layer(labels):
 z=''
 for i,(a,b) in enumerate(labels):
  y=20+i*195;z+=f'<g class="stage stage{i}">'+rect(135,y,930,150,'#F4F6F1')+text(360,y+85,a,36,INDIGO,700,24)+text(800,y+62,b,34,width=24)+'</g>'
 return z

def yield_diagram():
 z=text(280,75,'One large die',30,INDIGO,700)+text(900,75,'Smaller screened dies',30,INDIGO,700)
 z+=rect(95,130,370,330,'#ECEFF4')
 for x,y in [(175,225),(330,355)]:z+=f'<path d="M{x-14} {y-14}L{x+14} {y+14} M{x+14} {y-14}L{x-14} {y+14}" stroke="#5F6062" stroke-width="6"/>'
 for j in range(3):
  for k in range(3):
   x=725+k*115;y=130+j*115;bad=(j,k) in [(0,1),(2,0)];z+=rect(x,y,100,100,'#ECEFF4' if bad else '#EDF7DF',GRAY if bad else GREEN)
   if bad:z+=f'<path d="M{x+40} {y+40}l20 20 m0 -20l-20 20" stroke="{GRAY}" stroke-width="5"/>'
 z+=text(600,535,'Illustration of defect exposure, not measured yield data',23,width=70)
 return z

def package_diagram(title):
 z=''
 if 'Hybrid' in title:
  z+=rect(220,80,760,150,'#ECEFF4')+text(600,145,'Upper die',30,INDIGO,700)
  z+=rect(220,350,760,150,'#ECEFF4')+text(600,430,'Lower die',30,INDIGO,700)
  z+=rect(220,250,760,80,'#EDF7DF',GREEN)+text(600,530,'Dielectric + direct metal bond',27,width=40)
  for x in range(250,960,70):z+=rect(x,220,22,140,GREEN,GREEN,0)
 elif 'Bridges' in title:
  for o,label in [(0,'Local bridge'),(600,'Broad interposer')]:
   z+=text(o+300,70,label,29,INDIGO,700)
   z+=rect(o+60,370,480,100,'#ECEFF4')+text(o+300,430,'Package substrate',23)
   for x in [o+80,o+330]:z+=rect(x,140,210,130,'#EDF7DF',GREEN)+text(x+105,215,'Chiplet',25,INDIGO,700)
   if o==0:z+=rect(o+220,290,160,35,GREEN,GREEN,0)
   else:z+=rect(o+65,290,470,45,GREEN,GREEN,0)
 else:
  z+=rect(70,390,1060,100,'#ECEFF4')+text(600,454,'Larger package substrate',29,INDIGO,700)
  z+=rect(155,300,890,55,GREEN,GREEN,0)+text(600,530,'Redistribution beyond the die outlines',26,width=52)
  for x in [260,700]:z+=rect(x,75,240,145,'#EDF7DF',GREEN)+text(x+120,160,'Chiplet',30,INDIGO,700)
  for x1,x2 in [(310,195),(430,550),(750,650),(880,1005)]:z+=f'<path d="M{x1} 220 V305 H{x2} V390" fill="none" stroke="{INDIGO}" stroke-width="4"/>'
 z+=text(600,575,'Conceptual cross-section · not to scale',23,width=65)
 return z

def artwork(s,m):
 f=s['figure'];labels=f['diagram']['labels'];title=s['title'];kind=f['diagram']['kind']
 if 'Smaller dies' in title:return yield_diagram()
 if any(x in title for x in ['Fan-out','Bridges and','Hybrid bonding']):return package_diagram(title)
 if kind=='layers':return layer(labels)
 return row(labels,f.get('media_type')=='video')
for m in c['modules']:
 for s in m['slides']:
  f=s.get('figure') or {}
  if not f.get('diagram'):continue
  # These figures have their own deterministic vector source and measured WAV
  # timeline. Never replace an approved single-pass sequence with a generic loop.
  if f['diagram'].get('kind')=='narration_synced':continue
  if f['diagram'].get('kind')=='3dk':
   from create_3dk_figure import build_svg
   (R/f['path']).write_text(build_svg())
   continue
  body=artwork(s,m);svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600"><rect width="1200" height="600" fill="white"/>{body}</svg>'
  if f.get('media_type')!='video':
   if not any(k in s['title'] for k in ['Smaller dies','Fan-out','Bridges and','Hybrid bonding']): svg=svg.replace('viewBox="0 0 1200 600" width="1200" height="600"','viewBox="0 110 1200 350" width="1200" height="350"')
   (R/f['path']).write_text(svg)
  else:
   # A finite timeline reveals the relationship in stages, then holds the full comparison.
   # No quantity reverses within the clip. The replay reset is the loop boundary.
   css='''body{margin:0;width:1920px;height:1080px;background:white;display:grid;place-items:center;overflow:hidden}svg{width:1800px;height:900px}.stage{opacity:.16}.stage0{animation:a 8000ms linear both}.stage1{animation:b 8000ms linear both}.stage2{animation:c 8000ms linear both}.route{opacity:.12}.route0{animation:b 8000ms linear both}.route1{animation:c 8000ms linear both}@keyframes a{0%,100%{opacity:1}}@keyframes b{0%,24%{opacity:.16}31%,100%{opacity:1}}@keyframes c{0%,49%{opacity:.16}56%,100%{opacity:1}}'''
   p=A/(pathlib.Path(f['path']).stem+'.html');p.write_text(f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(s["title"])}</title><style>{css}</style></head><body data-duration-ms="8000" data-poster-ms="6500">{svg}</body></html>')
# Course mark is an authored schematic, not an OCP logo modification.
(R/'chiplet-mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240"><rect x="8" y="8" width="224" height="224" rx="34" fill="#343895"/><g fill="#8DC63F"><rect x="40" y="40" width="65" height="65" rx="7"/><rect x="135" y="40" width="65" height="65" rx="7"/><rect x="40" y="135" width="65" height="65" rx="7"/><rect x="135" y="135" width="65" height="65" rx="7"/></g><path d="M105 72H135 M105 168H135 M72 105V135 M168 105V135" stroke="white" stroke-width="8"/></svg>')
shutil.copy2(R/'tools/academy_wizard/assets/ocp_academy_white.svg',R/'ocp_academy_white.svg')
print('Created',len(list(A.glob('*.html'))),'animation sources and',len(list((R/'figures').glob('*.svg'))),'editable static diagrams.')

"""Build code-native course figures, course mark, and editable LMS poster."""
from pathlib import Path
import re,html,base64,sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT;FIG=OUT/'figures';FIG.mkdir(exist_ok=True)
GREEN='#8DC63F';BLUE='#343895';INK='#283246';GRAY='#5F6062'
STYLE='''<style>text{font-family:"Open Sans",Arial,sans-serif;fill:#283246;font-size:28px} .small{font-size:22px;fill:#5F6062}.em{font-weight:700}.box{fill:#f5f7f1;stroke:#8DC63F;stroke-width:2}.neutral{fill:#f5f6fa;stroke:#cbd1dc;stroke-width:2}</style>'''
def svg(w,h,body):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">{STYLE}<rect width="{w}" height="{h}" fill="white"/>{body}</svg>'
def txt(x,y,lines,cl='em',size=28):
    if isinstance(lines,str):lines=[lines]
    return f'<text x="{x}" y="{y}" text-anchor="middle" class="{cl}" style="font-size:{size}px">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.35}">{html.escape(t)}</tspan>' for i,t in enumerate(lines))+'</text>'
def box(x,y,w,h,lines,accent=True,size=28):
    if isinstance(lines,str):lines=[lines]
    yy=y+h/2-(len(lines)-1)*size*1.35/2+size*.35
    return f'<rect class="{"box" if accent else "neutral"}" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>'+txt(x+w/2,yy,lines,size=size)
def arrow(x1,y1,x2,y2,color=GRAY):
    # Arrow points stop on the target edge; shaft meets the flat-back midpoint.
    import math
    dx=x2-x1;dy=y2-y1;L=math.hypot(dx,dy);ux=dx/L;uy=dy/L;bx=x2-14*ux;by=y2-14*uy
    a=(bx-7*uy,by+7*ux);b=(bx+7*uy,by-7*ux)
    return f'<path d="M{x1} {y1} L{bx} {by}" fill="none" stroke="{color}" stroke-width="3"/><polygon class="arrowhead" points="{a[0]},{a[1]} {b[0]},{b[1]} {x2},{y2}" fill="{color}"/>'
def save(name,w,h,body):
    p=FIG/(name+'.svg');art=svg(w,h,body)
    if name in {'firmware_boundary','publication_path','requirements_evidence'}:
        art=art.replace(f'height="{h}" viewBox="0 0 {w} {h}"',f'height="240" viewBox="0 50 {w} 240"',1)
    p.write_text(art);return p

if '--poster-only' not in sys.argv:
    save('firmware_boundary',790,310,
     box(25,75,205,120,['Authorized','update'],False)+box(290,75,205,120,['Firmware','and config'])+box(555,75,210,120,['Data and','device keys'],False)+arrow(230,135,290,135)+arrow(495,135,555,135)+txt(395,260,'Security decisions cross trust boundaries',cl='small',size=23))
    save('scope_examples',760,380,
     ''.join(box(25,25+i*115,265,88,[a],False)+box(320,25+i*115,410,88,[b])+arrow(290,69+i*115,320,69+i*115) for i,(a,b) in enumerate([('Code','Command parser'),('Isolation','Security boundary'),('Physical attack','Long-lived secret')])) )
    save('evidence_boundary',720,340,
     '<rect x="18" y="18" width="684" height="304" rx="20" fill="#fff" stroke="#343895" stroke-width="3"/>'+box(42,42,300,104,['Product identity'])+box(378,42,300,104,['Firmware state'])+box(42,190,300,104,['Review scope'],False)+box(378,190,300,104,['Limitations'],False))
    save('boundary_depth',790,350,
     box(25,30,225,100,['Whole device'],size=24)+box(282,30,225,100,['Component'],size=24)+box(540,30,225,100,['Agreed changes'],size=24)+txt(395,190,'ASSESSMENT BOUNDARY',cl='small',size=23)+
     '<path d="M25 220H765" stroke="#cbd1dc" stroke-width="2"/>'+box(25,250,740,75,['Review depth: applicable Scopes 1, 2, and 3'],False,size=27))
    save('publication_path',790,300,
     box(25,75,205,120,['Provider','evidence'],False)+box(290,75,205,120,['Vendor','submission'])+box(555,75,210,120,['Published','review result'],False,size=27)+arrow(230,135,290,135)+arrow(495,135,555,135)+txt(395,262,'Review changed firmware against an agreed baseline',cl='small',size=23))
    save('requirements_evidence',790,310,
     box(25,75,205,125,['Applicable','requirements'],size=25)+box(290,75,205,125,['Vendor','evidence'],False)+box(555,75,210,125,['Independent','review'])+arrow(230,138,290,138)+arrow(495,138,555,138)+txt(395,267,'One connected S.A.F.E. review process',cl='small',size=24))

    mark='''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240"><path d="M120 18 202 50v66c0 50-36 84-82 106-46-22-82-56-82-106V50Z" fill="#343895"/><path d="M120 40 182 64v51c0 37-25 66-62 86-37-20-62-49-62-86V64Z" fill="white"/><rect x="80" y="77" width="80" height="76" rx="12" fill="#8DC63F"/><path d="m94 115 18 18 35-39" fill="none" stroke="white" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><g stroke="#343895" stroke-width="6" stroke-linecap="round"><path d="M71 92H62M71 115H62M71 138H62M178 92h-9M178 115h-9M178 138h-9"/></g></svg>'''
    (OUT/'safe_mark.svg').write_text(mark)

academy=((ROOT.parents[1]/'skills/academy-wizard/assets/ocp_academy_white.svg')).read_text()
academy=re.sub(r'<\?xml[^>]*>','',academy).strip()
academy=re.sub(r'<svg\b([^>]*)>',lambda m: '<svg x="42" y="27" width="215" height="58"'+re.sub(r'\s(?:width|height|x|y)="[^"]*"','',m[1])+'>',academy,count=1)
# A nested SVG keeps the authoritative Academy logo geometry intact.
logo_data=(ROOT/'authoring/ocp_safe_official_tm.svg').read_bytes()
logo_viewbox=[float(x) for x in ET.fromstring(logo_data).attrib['viewBox'].split()]
logo_width=240
logo_height=logo_width*logo_viewbox[3]/logo_viewbox[2]
logo_encoded=base64.b64encode(logo_data).decode()
poster=f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400"><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#141a45"/><stop offset=".55" stop-color="#252a6b"/><stop offset="1" stop-color="#343a86"/></linearGradient><linearGradient id="rail"><stop stop-color="#8dc63f"/><stop offset="1" stop-color="#addb61"/></linearGradient><radialGradient id="face"><stop stop-color="white"/><stop offset="1" stop-color="#e8edf5"/></radialGradient></defs><rect width="800" height="400" fill="url(#bg)"/>{academy}<path d="M614 0h186v400H716Z" fill="url(#rail)"/><path d="M550 0h70L723 400h-48Z" fill="#747ac0" opacity=".18"/><g fill="none" stroke="#9da3dc" opacity=".25"><circle cx="635" cy="215" r="155"/><circle cx="635" cy="215" r="170" stroke-dasharray="48 22"/><path d="M456 105h70l22 22M483 331h50l28-24"/></g><circle cx="635" cy="218" r="123" fill="url(#face)" stroke="#343895" stroke-width="6"/><image x="{635-logo_width/2}" y="{218-logo_height/2}" width="{logo_width}" height="{logo_height}" href="data:image/svg+xml;base64,{logo_encoded}"/><rect x="43" y="105" width="138" height="28" rx="5" fill="#8dc63f"/><g font-family="Open Sans,Arial,sans-serif"><text x="57" y="125" font-size="16" font-weight="800" fill="#1d2258">OCP S.A.F.E.</text><text x="42" y="186" font-size="38" font-weight="800" fill="white">PRODUCT SECURITY</text><text x="42" y="232" font-size="38" font-weight="800" fill="white">REVIEWS</text><text x="44" y="270" font-size="21" font-weight="600" fill="white">WITH S.O.L.I.D. REQUIREMENTS</text><rect x="44" y="306" width="48" height="5" fill="#8dc63f"/><text x="44" y="342" font-size="17" fill="white">Understand the evidence. Ask better questions.</text></g></svg>'''
(ROOT/'authoring/thumbnail.svg').write_text(poster)
print('Built editable poster source with the supplied official OCP S.A.F.E. trademark SVG; course mark preserved.')

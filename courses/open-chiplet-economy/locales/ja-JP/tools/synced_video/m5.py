"""M5S3: test the physical object that exists, against final narration.

Die identities persist through dicing and assembly. The package substrate is a
separate input. A full inter-die path appears only after assembly; the final
comparison comprises snapshots, rather than a reversal of manufacturing.
"""
from .primitives import *

DURATION = 41.65963718820862

def wafer(cx,cy,r,selected=True):
    out=[f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHITE}" stroke="{GRAY}" stroke-width="5"/>']
    scale=r/300
    for row in range(3):
        for col in range(3):
            if not selected and row==1 and col in (1,2):continue
            x=cx+(-230+col*180)*scale;y=cy+(-200+row*150)*scale
            w=150*scale;h=130*scale
            # The selected pair is rendered separately so it can leave the wafer.
            if row==1 and col in (1,2):continue
            # Only dice contained in the circular usable area are drawn.
            corners=[(x,y),(x+w,y),(x,y+h),(x+w,y+h)]
            if max((a-cx)**2+(b-cy)**2 for a,b in corners)>r*r*.94:continue
            out.append(rect(x,y,w,h,WHITE,GRAY,3,0))
    return out

def early(t):
    p=smooth(t,8.10,9.5)
    cx,cy,r=lerp(650,300,p),lerp(500,310,p),lerp(300,165,p)
    parts=wafer(cx,cy,r,False)
    a=(lerp(600,740,p),lerp(450,290,p),lerp(150,240,p),lerp(130,210,p))
    b=(lerp(780,1120,p),lerp(450,290,p),lerp(150,240,p),lerp(130,210,p))
    parts += [chip(*a,'A'),chip(*b,'B')]
    parts += [text(cx,cy+r+80,'Silicon wafer',52)]
    if t<4.54:
        # One stylized probe needle tests A then B without dicing the wafer.
        q=smooth(t,1.5,2.3);px=lerp(675,855,q)
        contact=(smooth(t,.35,1.1)-smooth(t,1.1,1.5)+
                 smooth(t,2.3,2.9)-smooth(t,3.2,3.74))
        tip=lerp(325,450,contact)
        parts += [path(f'M{px-95} 145 H{px+80} V230 H{px} V{tip}',INK,8),
                  text(1390,480,'Probe each die',56)]
    elif t<8.02:
        parts += [path('M590 430 H580 V600 H590',GRAY,5),
                  text(1390,455,'Function +\nelectrical behavior',56),
                  text(1390,620,'Die-level scope',48),
                  text(1390,720,'At this stage',50)]
    else:
        parts += [text(1040,145,'Individual dies',58)]
        if t>=9.5:
            parts += [path('M710 270 H690 V520 H710',GREEN,6),
                      text(1050,600,'Screening, as appropriate',50)]
    return parts

def package(parts,dy=0,highlight=False):
    parts += [rect(650,700+dy,900,140,WHITE,GRAY,6,5),
              chip(740,490+dy,240,210,'A'),chip(1120,490+dy,240,210,'B')]
    parts += [path(f'M860 {700+dy} V{770+dy} H1240 V{700+dy}',GREEN if highlight else INK,9)]

def comparison(t):
    parts=[text(360,220,'Before assembly',54),text(960,220,'After assembly',54),
           text(1560,220,'System',54)]
    # The identical notched A and B die identities repeat in labelled snapshots.
    parts += [chip(170,400,164,140,'A',t>=37.66),chip(390,400,164,140,'B',t>=37.66)]
    parts += [rect(730,600,460,100,WHITE,GRAY,5,4),
              chip(780,450,160,150,'A'),chip(1010,450,160,150,'B'),
              path('M860 600 V650 H1090 V600',GREEN if t>=34.78 else INK,8)]
    # A distinct branch enters the substrate, never emerges from the wafer.
    parts += [path('M650 790 V650 H708',GRAY,6),arrow(708,650,730,650,GRAY,6,18),
              text(490,730,'Substrate',46)]
    parts += [rect(1320,300,500,400,WHITE,GRAY,5,12),
              rect(1360,540,420,100,WHITE,GRAY,5,4),
              chip(1390,390,160,150,'A'),chip(1580,390,160,150,'B'),
              path('M1470 540 V590 H1660 V540',INK,8)]
    parts += [text(360,810,'Early screening',48),text(960,810,'New paths',48),
              text(1560,810,'Integrated behavior',48),
              bracket(90,1830,930,'Complementary evidence')]
    if t>=37.66:parts += [text(960,1000,'Early screening still matters',50)]
    return parts

def render(t:float)->str:
    t=max(0,min(float(t),DURATION))
    if t<12.20:return svg(early(t))
    if t<19.36:
        parts=wafer(300,310,165,False)
        parts += [text(300,555,'Silicon wafer',50),chip(740,290,240,210,'A'),
                  chip(1120,290,240,210,'B'),text(1050,150,'Separate incoming flows',58)]
        p=smooth(t,12.20,14.04)
        bx,by=lerp(840,650,p),lerp(780,700,p)
        parts += [rect(bx,by,900,140,WHITE,GRAY,6,5),text(bx+450,by+230,'Package substrate',52)]
        if t>=15.76:
            parts += [bracket(690,1460,590,'Not assembled',GRAY,'up')]
        return svg(parts)
    if t<23.28:
        parts=[text(960,150,'Assembly',60),rect(650,700,900,140,WHITE,GRAY,6,5)]
        q=smooth(t,19.36,20.34);y=lerp(290,490,q)
        parts += [chip(740,y,240,210,'A'),chip(1120,y,240,210,'B')]
        if t>=20.34:
            q=smooth(t,20.34,21.24)
            # Reveal the newly created complete path only after the dies seat.
            parts += [path('M860 700 V770 H1240 V700',INK,8),
                      f'<path d="M860 700 V770 H1240 V700" fill="none" stroke="{GREEN}" stroke-width="10" stroke-dasharray="{520*q} 520"/>',
                      text(1100,970,'New connections exist after assembly',52)]
        return svg(parts)
    if t<28:
        parts=[text(960,150,'Package testing',60)]
        package(parts,highlight=True)
        parts += [bracket(625,1575,930,'New paths + accessible functions')]
        return svg(parts)
    if t<32.82:
        parts=[text(960,130,'System testing',60),rect(300,190,1330,650,WHITE,GRAY,5,14)]
        package(parts,dy=-80,highlight=True)
        q=smooth(t,28.10,29.40)
        x=lerp(90,360,q)
        parts += [line(170,300,600,300,GRAY,6),token(x,230,'Stimulus',300,140,False)]
        q=smooth(t,30.0,31.26);x=lerp(1260,1500,q)
        if t>=30:parts += [line(1320,300,1805,300,GRAY,6),token(x,230,'Behavior',300,140,False)]
        parts += [text(960,940,'Integrated behavior',54),text(960,1000,'Relevant operating conditions',48)]
        return svg(parts)
    return svg(comparison(t))

# Retain approved scene logic and use measured Japanese narration time.
from .japanese_timing import english_time
_source_render=render
def render(t):
    return _source_render(english_time('m5',float(t)))

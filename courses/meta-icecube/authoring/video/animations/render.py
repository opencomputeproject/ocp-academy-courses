"""Rebuild the three silent masters with Pillow and ffmpeg.
Run: FFMPEG=/path/to/ffmpeg python3 render.py [signal-path|hybrid-cooling|slow-fan]
Source figures live in the course figures directory. All positions use a 960 × 540 design grid.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from functools import lru_cache
import io, json, os, math, subprocess, sys
ROOT=Path(__file__).resolve().parent
FIG=ROOT.parents[2]/'figures'
W,H=1920,1080
INK='#182B39'; MUT='#4C6371'; TEAL='#006D69'; BLUE='#1555A0'; AMBER='#934615'; LIGHT='#D9E3E5'; WHITE='white'
def scale(box): return tuple(round(v*2) for v in box)
@lru_cache(None)
def font(sz,bold):
    name='Arial Bold.ttf' if bold else 'Arial.ttf'
    for path in [Path('/System/Library/Fonts/Supplemental')/name,Path('/usr/share/fonts/truetype/liberation2')/('LiberationSans-Bold.ttf' if bold else 'LiberationSans-Regular.ttf')]:
        if path.exists(): return ImageFont.truetype(str(path),round(2*sz))
    return ImageFont.truetype('DejaVuSans.ttf',round(2*sz))
def txt(x,y,s,sz=22,c=INK,b=False,anchor='la'):
    d.text(scale((x,y)),s,font=font(sz,b),fill=c,anchor=anchor)
def box(bounds,c=TEAL,w=3,fill=None,r=6):
    d.rounded_rectangle(scale(bounds),radius=r*2,outline=c,width=w*2,fill=fill)
def line(points,c,w=4):
    d.line([scale(p) for p in points],fill=c,width=w*2,joint='curve')
def dot(x,y,c,r=4): d.ellipse(scale((x-r,y-r,x+r,y+r)),fill=c)
def arrow(x,y,ex,ey,c,t=1):
    t=max(0,min(1,t));xx=x+(ex-x)*t;yy=y+(ey-y)*t
    if t<.02:return
    a=math.atan2(ey-y,ex-x); ln=min(10,math.hypot(xx-x,yy-y));tip=(xx,yy)
    base=(xx-ln*math.cos(a),yy-ln*math.sin(a))
    line([(x,y),base],c,3)
    d.polygon([scale(tip),scale((base[0]-4*math.sin(a),base[1]+4*math.cos(a))),scale((base[0]+4*math.sin(a),base[1]-4*math.cos(a)))],fill=c)
def progress(t,start,span=1.4): return min(1,max(0,(t-start)/span))
@lru_cache(None)
def source(n):
    im=Image.open(next(FIG.glob(f'figure-{n}-*'))).convert('RGB')
    # Tight front/rear hardware crops. Top and isometric retain source callouts.
    if n==3:im=im.crop((175,246,1266,444))
    if n==4:im=im.crop((25,148,1398,392))
    return im
@lru_cache(maxsize=90)
def asset(n,w,h):return source(n).resize((w*2,h*2),Image.Resampling.LANCZOS)
def photo(n,x,y,w,h):
    im.paste(asset(n,round(w),round(h)),scale((x,y)))
def heading(s): txt(40,32,s,31,INK,True)
def sub(s):txt(40,80,s,18,MUT)
def front():photo(3,55,178,850,154)
def rear():photo(4,55,180,850,151)
def banks():box((150,196,473,318));box((486,196,806,318))
def row(y,s,c=INK):txt(65,y,s,25,c,True)
def chip(x,y,s,c,w):box((x,y,x+w,y+39),c,1,'#F5F9F9');txt(x+w/2,y+19,s,18,c,True,'mm')
def signal(t):
    if t<12:
        heading('How can 64 connectors deliver 128 interfaces?');sub('Front panel');front()
        if t>1:banks()
        row(374,'64 physical OSFP connectors',TEAL)
        if t>=5:txt(65,430,'Two physical interface cards carry 32 connectors each.',20,MUT)
    elif t<35:
        heading('Follow one transmit signal');sub('Internal top view  ·  Simplified signal path')
        photo(1,32,154,541,304)
        beats=[(12,'ASIC / SerDes'),(16,'RF flyover cables'),(20,'PIC / OSFP'),(25,'Pluggable optical module'),(30,'Fiber')]
        for i,(at,s) in enumerate(beats):
            if t>=at:
                y=120+i*77
                chip(621,y,s,TEAL if i<4 else BLUE,298)
                if 0<i<4:arrow(770,y-34,770,y-4,TEAL,progress(t,at,.8))
                if i==4:
                    for yy in [y-34,y-24]:line([(770,yy),(770,yy+5)],BLUE,3)
                    arrow(770,y-16,770,y-4,BLUE,progress(t,at,.8))
        boxes=[(239,276,313,341),(202,199,346,230),(147,223,190,413)]
        i=0 if t<16 else 1 if t<20 else 2
        box(boxes[i],AMBER,3)
        if t>=30:
            txt(638,484,'Electrical → optical',18,BLUE,True)
    elif t<58:
        heading('One connector carries two 800GbE interfaces')
        if t<48:
            sub('One populated OSFP opening  ·  Simplified view')
            # Animate a pull-in on the physical opening, followed by the module diagram.
            p=progress(t,35,2)
            sw=int(318+65*p); sh=int(sw*.31)
            opening=source(3).crop((139,27,192,54)).resize((sw*2,sh*2),Image.Resampling.LANCZOS)
            im.paste(opening,scale((46,205)));box((46,205,46+sw,205+sh),TEAL,2)
            if t>=38:
                box((53,211,423,315),TEAL,2,'#E6F1F1',4)
                txt(238,262,'Dual-800G module',25,TEAL,True,'mm')
            txt(48,350,'One OSFP connector',22,TEAL,True)
            for i in range(2):
                at=38+i*3
                if t>=at:
                    yy=180+i*115
                    line([(437,268),(485,268),(485,yy+20)],TEAL,3)
                    arrow(485,yy+20,563,yy+20,TEAL,progress(t,at))
                    chip(570,yy,f'800GbE interface {i+1}',TEAL,322)
        else:
            sub('Front panel  ·  64 physical connectors');front();banks()
            row(386,'64 × 2 × 800 Gb/s = 102.4 Tb/s',TEAL)
            txt(65,446,'128 logical 800GbE interfaces',21,MUT)
    else:
        heading('Two ways to express system capacity');sub('Front panel  ·  64 physical connectors');front();banks()
        row(370,'64 × 2 × 800 Gb/s = 102.4 Tb/s',TEAL)
        if t>=59.5:row(432,'512 × 200 Gb/s = 102.4 Tb/s',BLUE)
def cooling(t):
    if t<15:
        heading('IceCube in the Open Rack v3 High Power Rack')
        # Rack rails are schematic; the Figure 2 chassis is pictured inside them.
        for x in (63,556):
            box((x,110,x+15,469),'#6B7E86',1,'#C7D1D4',2)
            for y in range(125,460,24):dot(x+7.5,y,WHITE,2)
        photo(2,84,123,464,317)
        for x in (80,550):line([(x,343),(x,401)],TEAL,6)
        txt(605,189,'Canister adapter',26,TEAL,True)
        txt(605,239,'Mounts the 2OU chassis',19);txt(605,266,'in the rack.',19)
        line([(594,219),(582,219),(582,373),(558,373)],TEAL,2)
        txt(82,480,'Rack outline and mounting interface are schematic.',16,MUT)
    elif t<40:
        heading('Liquid and air remove heat from different parts')
        sub('Internal top view  ·  Simplified airflow')
        photo(1,38,150,584,328)
        box((264,285,343,355),TEAL,3)
        txt(644,145,'Cold plates',24,TEAL,True);txt(644,187,'Switch ASIC',19)
        if t>=19:
            box((162,197,213,421),TEAL,3);txt(644,220,'Populated OSFP optics',19)
        if t>=24:
            txt(644,283,'Front-to-back air',24,AMBER,True)
            txt(644,330,'Microserver and RunBMC',17);txt(644,359,'Power stages and SSD',17);txt(644,388,'QSFP28 and board devices',17)
            for i in range(2):
                yy=237+i*72
                line([(384,yy),(515,yy)],WHITE,8)
                arrow(384,yy,515,yy,AMBER,progress(t,24+i,.9))
            txt(63,492,'Front',17,MUT);txt(521,492,'Rear',17,MUT)
    elif t<60:
        heading('Locate the rack-side connections');sub('Rear view  ·  As seen from the back of the rack');rear()
        for at,x,s in [(40,850,'Coolant supply'),(46,109,'Coolant return'),(51,481,'51 V DC power')]:
            if t>=at:
                if x==481:box((442,232,517,306),INK);c=INK
                else:
                    c=BLUE if x>500 else TEAL;box((x-28,185,x+30,246),c)
                if x==850:arrow(x,153,x,180,c,progress(t,at));txt(x,122,'Supply in',17,c,True,'mm')
                if x==109:arrow(x,180,x,150,c,progress(t,at));txt(x,122,'Return out',17,c,True,'mm')
                txt(x,385,s,21,c,True,'mm')
    else:
        heading('Which front-panel optics use cold plates?');sub('Front view');front()
        if t>=64:
            banks();txt(213,380,'OSFP banks',23,TEAL,True);txt(213,421,'Liquid-cooled',19)
        if t>=68:
            box((833,262,884,291),AMBER,3);txt(728,380,'QSFP28',23,AMBER,True);txt(728,421,'Air-cooled',19)
def fan(t):
    if t<15:
        heading('How does IceCube detect a slow fan?');sub('Rear view  ·  Four fan trays');rear()
        box((163,197,280,323),AMBER,3)
        txt(163,379,'One fan slows',26,AMBER,True)
        if t>=6:txt(163,426,'Its speed falls below the RPM threshold.',20)
    elif t<35:
        heading('From fan speed to a control decision');sub('Simplified monitoring and control signals')
        xs=[48,350,650]; names=['Fan tray','Fan control logic','Microserver']
        for i,(x,s) in enumerate(zip(xs,names)):
            if t>=15+i*3:chip(x,241,s,TEAL if i<2 else BLUE,248)
        for i,(at,s) in enumerate([(18,'Fan speed feedback'),(21,'Low-RPM warning')]):
            if t>=at:
                xx=xs[i]+124; ex=xs[i+1]+124
                line([(xx,239),(xx,199),(ex,199)],TEAL,3)
                arrow(ex,199,ex,235,TEAL,progress(t,at))
                txt((xx+ex)/2,172,s,17,TEAL,True,'mm')
        if t>=25:
            txt(775,365,'Temperature sensors',18,BLUE,True,'mm');arrow(775,345,775,285,BLUE,progress(t,25))
        if t>=29:
            # Separate return route below the sensor input.
            line([(877,285),(877,435),(510,435)],AMBER,3)
            arrow(510,435,510,285,AMBER,progress(t,29))
            line([(440,285),(440,388),(172,388)],AMBER,3)
            arrow(172,388,172,285,AMBER,progress(t,29))
            txt(690,463,'Fan speed command',19,AMBER,True,'mm')
    elif t<50:
        heading('Two controllers have different responsibilities');sub('BMC-lite management')
        for x,s,c in [(55,'Microserver',BLUE),(501,'BMC',TEAL)]:
            box((x,151,x+400,432),LIGHT,1,'#F6F9F9');txt(x+25,179,s,28,c,True)
        txt(80,248,'Reads sensors',22);txt(80,305,'Runs the fan-speed',22);txt(80,338,'control algorithm',22)
        if t>=36:
            for i,s in enumerate(['Power-on','Failure recovery','System event logging']):txt(526,248+53*i,s,22)
    else:
        if t<56:
            heading('Find the same fan tray in both views')
            photo(4,42,187,407,72);box((94,195,148,254),AMBER,3)
            photo(1,478,133,435,245);box((819,314,853,346),AMBER,3)
            txt(45,332,'Rear view',19,MUT,True);txt(495,398,'Internal top view',19,MUT,True)
        else:
            heading('Find the front-accessible E1.S SSD');sub('Front view  ·  Field-replaceable storage');front()
            box((839,290,897,322),AMBER,3)
            if t<61:txt(710,381,'E1.S SSD',24,AMBER,True)
            else:row(386,'Who runs the fan-speed control algorithm?',BLUE)
CLIPS={'signal-path':(signal,75),'hybrid-cooling':(cooling,75),'slow-fan':(fan,65)}
def frame(draw,t):
    global im,d
    im=Image.new('RGB',(W,H),WHITE);d=ImageDraw.Draw(im);draw(t);return im
def render(name):
    draw,duration=CLIPS[name]; fps=24
    source_frames = range(duration * fps)
    if name == 'signal-path':
        timing = json.loads((ROOT.parent / 'signal-path-timing.json').read_text())
        if timing['frames_per_second'] != fps:
            raise ValueError('Signal-path trim ranges must use the encoder frame rate')
        removed = {
            frame_number
            for start, end in timing['removed_frame_ranges']
            for frame_number in range(start, end)
        }
        source_frames = [j for j in range(timing['source_frame_count']) if j not in removed]
    frame(draw,3).save(ROOT/(name+'-poster.png'))
    cmd=[os.environ.get('FFMPEG','ffmpeg'),'-v','error','-y','-f','image2pipe','-framerate',str(fps),'-vcodec','png','-i','-','-an','-c:v','libx264','-threads','3','-preset','veryfast','-crf','14','-pix_fmt','yuv420p','-r','24','-movflags','+faststart',str(ROOT/(name+'-silent.mp4'))]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    moving={'signal-path':[(16,17),(20,21),(25,26),(30,31),(35,37),(38,40),(41,43)],'hybrid-cooling':[(24,26),(40,42),(46,48)],'slow-fan':[(18,20),(21,23),(25,27),(29,31)]}[name]
    last=None
    for j in source_frames:
        t=j/fps
        # Reuse lossless frames during stationary holds.
        key=t if any(a<=t<b for a,b in moving) else int(t*2)/2
        if last!=key:
            buf=io.BytesIO();frame(draw,key).save(buf,format='PNG',compress_level=1);data=buf.getvalue();last=key
        proc.stdin.write(data)
    proc.stdin.close()
    if proc.wait():raise RuntimeError('Encoder failed')
if __name__=='__main__':
    for name in sys.argv[1:] or CLIPS:render(name)

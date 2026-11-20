"""Editable vector-primitive scenes. See README.md for rendering instructions."""
import argparse, json, math, os, re, subprocess, tempfile, shutil, sys, hashlib
import mounting_kits
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parent
FIG=ROOT.parent/'figures'
NAVY='#162e40'; INK='#203b4a'; BLUE='#0b678a'; CYAN='#a5dce4'; TEAL='#00796e'; GREEN='#d4efe6'; RED='#ac4536'; CREAM='#fff0df'; GRAY='#576c77'; LIGHT='#e3ebec'; WHITE='#ffffff'
SCENES={
'm1s3':('Front support and rear power','RACK MECHANICS',['pick one rail','as it moves in','turn the rack around','at several heights','back around to the front']),
'm2s5':('Can you release the middle plug?','SERVICE ACCESS',['one plug in the middle','populate the ports','crosses right over','a sharp turn','separate side guides','drawing it straight out']),
'm3s4':('What remains after one supply is lost?','POWER DELIVERY',['six installed power supplies','seventy two kilowatts','sixty kilowatts of output','set one block aside','power monitoring module','a buffer answers','once spent']),
}
SCENES['m2s4']=('Google mounting options','EQUIPMENT FIT',mounting_kits.CUES)

@lru_cache(None)
def font(n,b):
    path='/System/Library/Fonts/Supplemental/Arial'+(' Bold' if b else '')+'.ttf'
    return ImageFont.truetype(path if Path(path).exists() else ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'),n)
def xy(points):return [(round(960+(x-cx)*zoom*2),round(540+(y-cy)*zoom*2)) for x,y in points]
def line(p,c=INK,w=2):d.line(xy(p),fill=c,width=round(2*w*zoom),joint='curve')
def box(x,y,w,h,fill=WHITE,stroke=None,r=4):
    d.rounded_rectangle(xy([(x,y),(x+w,y+h)]),radius=round(2*r*zoom),fill=fill,outline=stroke,width=3)
def txt(x,y,s,n=17,c=INK,b=False):d.text(xy([(x,y)])[0],s,font=font(round(2*n*zoom),b),fill=c,anchor='lt')
def poly(p,c,stroke=None):
    d.polygon(xy(p),fill=c)
    if stroke:line(p+[p[0]],stroke)
def bez(p,c,w):
    points=[]
    for i in range(61):
        t=i/60;q=1-t
        points.append(tuple(sum(k*v[j] for k,v in zip([q**3,3*q*q*t,3*q*t*t,t**3],p)) for j in (0,1)))
    line(points,c,w)
def label(x,y,s):txt(x,y,s,13,GRAY,True)
def note(y,s):txt(48,y,s,17,INK)
def rack(x,y,angle,seat,rail,back,second,sc):
    # Meta ORv3 frame rev 1.3 §6.1 (mm). Keep one physical scale in all three axes.
    W,D,H=600,1068,2286
    rad=math.radians(angle); elev=math.radians(16)
    def away(a,c):return -(a-W/2)*math.sin(rad)+(c-D/2)*math.cos(rad)
    def P(a,b,c):
        return (x+sc*((a-W/2)*math.cos(rad)+(c-D/2)*math.sin(rad)),
                y+sc*((b-H/2)*math.cos(elev)-away(a,c)*math.sin(elev)))
    draw=[]
    def part(pts,col,w=0,edge=None):
        # Back-to-front painting keeps the front handle behind the tray on the return view.
        depth=sum(away(a,c)*math.cos(elev)-(b-H/2)*math.sin(elev) for a,b,c in pts)/len(pts)
        draw.append((depth,pts,col,w,edge))
    steel='#78858a';far='#adb6b9';bus='#45484b'
    for c in (0,D):
        for a in (0,W):
            part([(a,0,c),(a,H,c)],steel if away(a,c)<0 else far,4)
        for b in (0,H):
            part([(0,b,c),(W,b,c)],steel,4)
    for a in (0,W):
        for b in (0,H,1220):
            part([(a,b,0),(a,b,D)],TEAL if rail and b==1220 else steel,4)
    # The diagram shows the whole rear busbar assembly, not its individual conductors.
    # Contacts are integral to the same assembly, not a second adjacent column.
    part([(W*.45,48,D),(W*.45,H-48,D)],bus,11)
    bus_depth=draw[-1][0]
    if back:
        for b in ([1160,860,1460] if second else [1160]):
            part([(W*.45-30,b,D+9),(W*.45+30,b,D+9)],'#e3e4e2',3)
            # Paint markings on their parent surface, regardless of their height.
            draw[-1]=(bus_depth-.01, *draw[-1][1:])
    z=-390+seat*426;end=z+D-36;xt,xb=13,W-13;top,bot=1126,1206
    def face(p,col):part(p,col,edge='#406170')
    face([(xt,top,z),(xb,top,z),(xb,top,end),(xt,top,end)],'#cfdee1')
    face([(xb,top,z),(xb,top,end),(xb,bot,end),(xb,bot,z)],'#90abb4')
    face([(xt,top,z),(xb,top,z),(xb,bot,z),(xt,bot,z)],BLUE)
    face([(xt,top,end),(xb,top,end),(xb,bot,end),(xt,bot,end)],'#839ba4')
    if math.cos(rad)>0:
        part([(W*.32,1164,z-3),(W*.68,1164,z-3)],WHITE,2)
    for _,pts,col,w,edge in sorted(draw,key=lambda d:-d[0]):
        p=[P(*v) for v in pts]
        if w:line(p,col,w)
        else:poly(p,col,edge)
def m1(k,f):
    if k<5:
        rack(302,268, 44 if k<3 else 44+92*(f if k==3 else 1), (0 if k<2 else f if k==2 else 1),k>=1,k>=3,k>=4,.163)
        label(580,169,'REAR VIEW' if k>=3 else 'FRONT VIEW')
        txt(580,210,['Open frame','Paired support rails','Tray travels on rails','Busbar assembly','Multiple contact heights'][k],21,BLUE,True)
        if k>=3:
            box(580,264,8,31,'#45484b',r=0)
            txt(604,263,'Rear power busbar',17)
            txt(580,315,'One assembly carries both',16)
            txt(580,342,'supply and return paths.',16)
        else:txt(580,260,'Steel frame carries the load.',16)
    else:
        rack(285,249,44,1,True,False,False,.145);rack(680,249,136,1,False,True,True,.145)
        label(208,449,'FRONT   /   TRAY HANDLE');label(597,449,'REAR   /   POWER BUSBAR')
    return 'The rails carry the tray; the rear contacts carry current.'
def m2(k,f):
    label(52,129,'ILLUSTRATIVE SWITCH FACE   /   OBLIQUE SERVICE VIEW')
    box(113,188,726,140,'#d4e0e4',GRAY,8)
    box(151,273,650,38,NAVY)
    for i in range(51):line([(158+i*12,279),(152+i*12,304)],GRAY,2)
    for i in range(7):
        x=213+87*i;box(x-25,198,50,33,NAVY)
    # Shade a straight approach lane, distinct from horizontal ventilation.
    if k>=5:poly([(448,231),(500,231),(507,271),(441,271)],GREEN)
    for i in range(7):
        if i!=3 and k<2:continue
        x=213+87*i;y=214+(40*f if i==3 and k==6 else 0)
        box(x-18,y-8,36,22,BLUE if i==3 else GRAY);box(x-7,y-10,14,5,'#ffbd58')
    for i in range(7):
        if i!=3 and k<2:continue
        x=213+i*87;y=228+(40*f if i==3 and k==6 else 0)
        if k==3:bez([(x,y),(x+2,202),(472,187),(87,232+i*3)],GRAY,8)
        elif k==4 and i==3:line([(x,y),(x,243),(x-70,243)],RED,7)
        elif i==3:bez([(x,y),(x,y+12),(x+4,y+16),(x+5,y+28)],BLUE,7)
        else:
            side=1 if i>3 else -1
            end=x+side*(42 if k<5 else (abs(x-(858 if side==1 else 98))))
            bez([(x,y),(x,y+29),(x+side*36,y+25),(end,249+(i%3)*4)],TEAL,6)
    if k>=5:
        for x in (90,849):box(x,242,17,27,None,BLUE)
    note(365,['Center latch and vent','Center latch visible','Adjacent ports populated','Crossing bundle hides the center latch','Rejected: a corner is not a supported bend','Broad curves keep the center approach clear','Center plug withdrawn; neighbors remain seated'][k])
    label(53,411,'BLUE   CENTER PLUG');label(285,411,'AMBER   RELEASE LATCH');label(579,411,'DARK SLOTS   AIR OPENING')
    return 'A useful cable route preserves both the hand path and the air path.'
def m3(k,f):
    label(49,136,'AC INPUT');label(181,136,'PHYSICAL SHELF   /   SIX INSTALLED POSITIONS');label(771,136,'DC OUTPUT')
    box(154,167,563,104,LIGHT,GRAY)
    for i in range(6):
        x=174+76*i;box(x,183,65,70,WHITE,BLUE);txt(x+17,195,str(i+1),15,GRAY);txt(x+5,226,'12 kW',15,BLUE,True)
    box(639,183,64,70,GREEN if k>=5 else WHITE,TEAL);txt(646,208,'PMM',16,TEAL,True)
    for i in range(2):line([(50,194+i*40),(152,194+i*40)],BLUE,5)
    line([(612,262),(758,262),(758,216),(866,216)],TEAL,5);poly([(864,208),(882,216),(864,224)],TEAL)
    label(50,291,'CAPACITY CALCULATION   /   NOT A LOAD-SHARING DIAGRAM')
    for i in range(6):
        x=50+i*67;box(x,318,58,40,LIGHT if k>=4 and i==5 else BLUE)
        txt(x+7,330,'12 kW',14,GRAY if k>=4 and i==5 else WHITE,True)
    if k>=2:txt(488,316,'72 kW   installed sum',20,BLUE,True)
    if k>=3:txt(488,353,'60 kW   redundant output',20,TEAL,True)
    if k>=6:
        txt(50,387,'Energy buffer',15,INK,True);box(50,412,188,15,LIGHT,GRAY)
        ratio=1 if k==6 else max(0,1-f)
        if ratio>.01:box(52,414,184*ratio,11,'#d88937')
        txt(257,407,'Stored energy is finite.',15)
    return 'Specified dual-cord configuration: installed ratings and sustained output answer different questions.'
def m4(k,f):
    # Source states 3–6 belong exclusively to the Supermicro comparison.
    assert 3 <= k <= 6
    label(48,132,'SUPERMICRO   /   LIQUID-COOLED ARM SERVER CHASSIS')
    # Actual aspect: OU = 48 mm, widths in inches; same pixel/mm scale.
    for x,w,h,title in [(58,240,43.2,'21-inch  /  2 OU'),(394,480,21.6,'42-inch  /  1 OU')]:
        if x>100 and k<4:continue
        box(x,265-h,w,h,CYAN,BLUE,1);txt(x,282,title,18,INK,True)
        if k>=5:
            for i in range(4):
                box(x+i*50,328,44,28,GREEN,TEAL)
                for j in range(2):box(x+7+i*50+j*18,335,12,12,TEAL)
    line([(47,266),(895,266)],GRAY)
    if k>=5:label(50,372,'COUNTS ONLY   /   FOUR NODES × TWO PROCESSORS IN EACH CHASSIS')
    if k>=6:box(48,401,841,31,LIGHT);txt(60,409,'Same four nodes and eight processors; the wider chassis saves 1 OU.',16,BLUE,True)
    return 'Four dual-processor nodes occupy less height in the wider chassis.'

def frame(slide,k,f):
    global d,cx,cy,zoom
    if slide=='helios_bay':
        from helios_bay import draw
        cx,cy,zoom=480,270,1
        im=Image.new('RGB',(1920,1080),WHITE);d=ImageDraw.Draw(im)
        draw(sys.modules[__name__],k,f)
        return im
    if slide=='m2s4':
        cx,cy,zoom=480,270,1
        im=Image.new('RGB',(1920,1080),WHITE);d=ImageDraw.Draw(im)
        mounting_kits.draw(sys.modules[__name__],im,k,f)
        return im
    cx,cy,zoom={'m1s3':(477,273,1.13),'m2s5':(465,275,1.09),'m3s4':(465,278,1.08),'m4s5':(472,278,1.075)}[slide]
    im=Image.new('RGB',(1920,1080),WHITE);d=ImageDraw.Draw(im)
    globals()['m'+slide[1]](k,f)
    return im
def norm(s):return re.findall(r'[a-z0-9]+',s.lower())
def gettimes(slide,data):
    if 'cues' in data:return data['cues']
    words=[]
    for item in data['words']:
        words.extend((w,item['start']) for w in norm(item['word']))
    tokens=[w for w,t in words];out=[]
    for cue in SCENES[slide][2]:
        key=norm(cue)
        starts=[i for i in range(len(tokens)) if tokens[i:i+len(key)]==key]
        if not starts:raise ValueError('Unmatched phrase: '+cue+'; provide explicit cue times if needed')
        out.append(words[starts[0]][1])
    return out
def render(slide,data):
    if slide=='m2s4':
        assert hashlib.sha256(next((ROOT.parent/'audio/module2').glob('slide_04*.wav')).read_bytes()).hexdigest()==data['wav_sha256']
    times=[0]+gettimes(slide,data);duration=data['duration']
    assert len(times)==len(SCENES[slide][2])+1 and times==sorted(times) and times[-1]<duration
    FIG.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);seq=[]
        for k,start in enumerate(times):
            end=(times+[duration])[k+1];span=end-start
            if span<=0:continue
            # Geometric movement for seating, rotating, withdrawal and discharge;
            # other states cut on their spoken cue with no idle motion.
            animated=(slide,k) in [('m1s3',2),('m1s3',3),('m2s4',10),('m2s5',6),('m3s4',7)]
            trans=min(1.4,span/2) if animated else 0
            steps=max(1,round(trans*24))
            for j in range(steps):
                f=1 if steps==1 else j/(steps-1);f=f*f*(3-2*f)
                name=f'{k:02}-{j:03}.png';frame(slide,k,f).save(tmp/name,compress_level=1)
                seq.extend([f"file '{name}'",f'duration {(trans/steps if j<steps-1 else span-trans*(steps-1)/steps):.8f}'])
        seq.append(f"file '{name}'");(tmp/'frames.ffconcat').write_text('\n'.join(seq)+'\n')
        mp4=FIG/(slide+'.mp4');tmpmp=tmp/'render.mp4'
        binary=os.environ.get('FFMPEG_BIN') or shutil.which('ffmpeg') or imageio_ffmpeg.get_ffmpeg_exe()
        subprocess.run([binary,'-loglevel','error','-f','concat','-safe','0','-i',str(tmp/'frames.ffconcat'),'-t',str(duration),'-vf','fps=24','-c:v','libx264','-threads','3','-preset','veryfast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(tmpmp)],check=True)
        shutil.copyfile(tmpmp,mp4);poster(binary,mp4)
def poster(binary,mp4):
    # Decode the actual last presented picture, including H.264 color conversion.
    subprocess.run([binary,'-y','-loglevel','error','-sseof','-1','-i',str(mp4),'-update','1',str(mp4.with_name(mp4.stem+'-poster.png'))],check=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description='Modules 2–4 use fresh/motion.py.');p.add_argument('slides',nargs='*',default=['m1s3']);p.add_argument('--preview',action='store_true');a=p.parse_args()
    if a.slides!=['m1s3']:p.error('Use fresh/motion.py for Modules 2–4.')
    for s in a.slides:
        if a.preview:
            states=[frame(s,k,1).resize((480,270),Image.Resampling.LANCZOS) for k in range(len(SCENES[s][2])+1)]
            im=Image.new('RGB',(960,270*((len(states)+1)//2)),WHITE)
            for i,state in enumerate(states):im.paste(state,(i%2*480,i//2*270))
            (ROOT/'previews').mkdir(exist_ok=True);im.save(ROOT/'previews'/(s+'.png'))
        else:render(s,json.loads((ROOT/'timing'/(s+'.json')).read_text()))

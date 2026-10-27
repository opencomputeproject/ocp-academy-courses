"""Deterministic, source-derived teaching media. One finite master pass per asset.

Frames are RGB lossless PNG at 1920x1080. Native STEP geometry was rendered
with VTK; source drawing crops retain their original proportions. Display
separation, schematic depth cases, and arithmetic do not assert simulation.
"""
from pathlib import Path
import sys, json, wave, math, io, subprocess, functools, os, shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
def find_ffmpeg():
    executable = os.environ.get('FFMPEG_BIN') or shutil.which('ffmpeg')
    if executable:
        return executable
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise RuntimeError('Install FFmpeg or set FFMPEG_BIN.') from exc

FFMPEG = find_ffmpeg()
OUT = ROOT / 'figures'
QA = ROOT / '_analysis/video_review'
QA.mkdir(parents=True, exist_ok=True)
W,H,FPS = 1920,1080,30
GREEN,NAVY,INK,GRAY = '#8DC63F','#343895','#27323B','#5F6062'

@functools.lru_cache(maxsize=40)
def font(size,bold=False):
    return ImageFont.truetype(str(ROOT/'assets/fonts'/f'open-sans-{700 if bold else 400}.ttf'),size)
@functools.lru_cache(maxsize=300)
def pic(path):
    return Image.open(ROOT/path).convert('RGB')
def blank(): return Image.new('RGB',(W,H),'white')
def text(im,xy,s,size=36,bold=False,color=INK):
    ImageDraw.Draw(im).text(xy,s,font=font(size,bold),fill=color)
def wrap(im,xy,s,width,size=36,bold=False,color=INK,lineheight=None):
    d=ImageDraw.Draw(im);lines=[];line=''
    for word in s.split():
        trial=(line+' '+word).strip()
        if d.textlength(trial,font=font(size,bold))>width and line:lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    for i,line in enumerate(lines):text(im,(xy[0],xy[1]+i*(lineheight or size*1.4)),line,size,bold,color)
    return len(lines)*(lineheight or size*1.4)
def card(im,box,title,lines,active=False):
    x,y,w,h=box;d=ImageDraw.Draw(im)
    d.rounded_rectangle((x,y,x+w,y+h),radius=18,fill='#E7F2D8' if active else '#F2F4F7',outline=GREEN if active else '#D8DDE3',width=3)
    yy=y+30;yy+=wrap(im,(x+34,yy),title,w-68,38,True,NAVY)+24
    for line in lines:yy+=wrap(im,(x+34,yy),line,w-68,30)+18
    assert yy<y+h-16,(title,yy,y+h)
def fit(im,path,box):
    x,y,w,h=box;p=pic(path).copy();p.thumbnail((w,h),Image.Resampling.LANCZOS);im.paste(p,(int(x+(w-p.width)/2),int(y+(h-p.height)/2)))
def note(im,s):wrap(im,(90,980),s,1740,29,color=GRAY)
def strip(im,labels,active,y=890):
    d=ImageDraw.Draw(im);width=(1740-24*(len(labels)-1))/len(labels)
    for i,label in enumerate(labels):
        x=90+i*(width+24);d.rounded_rectangle((x,y,x+width,y+66),radius=12,fill=GREEN if i<=active else '#E9EDF1')
        tw=d.textlength(label,font=font(27,True));assert tw<width-42
        text(im,(x+(width-tw)/2,y+14),label,27,True,NAVY)

def rack(t,D):
    im=blank();f=t/D
    phase=0 if f<.28 else 1 if f<.48 else 2 if f<.68 else 3 if f<.82 else 4
    imgs=['animations/assets/rack_frame_exploded.png','figures/rack_stage2.png','figures/rack_stage3.png','figures/rack_stage3.png','figures/rack_stage3.png']
    fit(im,imgs[phase],(760,55,1070,800))
    data=[('Base structure',['ORV3-derived rack','19-inch EIA equipment','1RU pitch']),('Optional rear extender',['Increases depth to 1200 mm','Protects rear components','Preserves rear hole pattern']),('Interface supports',['Manifold locations','Interconnect cartridge volume','Supports and stiffeners']),('Rack-level payload',['Up to 4000 lb IT payload','Separate evidence for slides,','brackets, and connector supports']),('Controlled reference chain',['Frame to mounting features','Supports to mating interfaces','Installed tray and actual loads'])]
    title,lines=data[phase];card(im,(90,235,620,540),title,lines,True)
    strip(im,['Base frame','Extender option','Supports','Mating interfaces'],min(phase,3))
    note(im,'Feature reveal follows the reference chain; it is not a rack assembly procedure.')
    return im

def hpm(t,D):
    im=blank();f=t/D
    if f<.25:
        fit(im,'animations/assets/fanless_dual.png',(740,65,1100,775))
        card(im,(90,235,620,540),'Dual-HPM example',['Discrete cooling / I/O zone','Manifold and midplane','Distribution between modules'],True)
        label='Dual HPM: discrete distribution zone'
    elif f<.46:
        fit(im,'animations/assets/fanless_full.png',(740,65,1100,775))
        card(im,(90,235,620,540),'Full-size HPM example',['T-pin chassis installation','Coplanar bay connections','Liquid distribution in HPM'],True)
        label='Full-size HPM: integrated distribution'
    else:
        # Eight seconds of real source-geometry separation at 30 fps, then hold.
        start=.46*D;pose=max(0,min(240,round((t-start)/8*240)))
        fit(im,f'animations/assets/hpm/hpm_pose_{pose:03}.png',(650,0,1270,910))
        card(im,(70,190,555,640),'Supplied STEP geometry',['Full-size fanless HPM','Geometric layers separated','Display positions expanded','Review interface ownership'],True)
        label='Source geometry retained; separation is illustrative'
    strip(im,['Dual HPM','Full-size HPM','Geometry separation'],0 if f<.25 else 1 if f<.46 else 2)
    note(im,label+'. No verified actuation or disassembly sequence is asserted.')
    return im

def depth(t,D):
    im=blank();case=min(3,int(t/(D/4)));p=(t%(D/4))/(D/4)
    titles=['Short module in a short location','Short module in a long location','Long module in a short location','Type C CRPS-optimized short option']
    text(im,(90,80),titles[case],48,True,NAVY)
    loc=132.8 if case in [0,2] else 318 if case==1 else 185
    mod=318 if case==2 else 185 if case==3 else 132.8
    scale=4.5;x,y=250,300;d=ImageDraw.Draw(im)
    # Side silhouette: location and module are separate horizontal rows, same scale.
    d.rounded_rectangle((x,y,x+loc*scale,y+155),radius=8,fill='#EEF0FA',outline=NAVY,width=4)
    text(im,(x,y-75),f'Location envelope: {loc:g} mm',36,True,NAVY)
    end=x+mod*scale;d.rounded_rectangle((x,y+285,end,y+400),radius=8,fill=GREEN if case!=2 else '#C6CBD3')
    text(im,(x,y+430),f'Module depth: {mod:g} mm',36,True)
    if p>.3:
        card(im,(90,845,1740,120),'',[]) if False else None
        msg=['Allowed depth class','Short can occupy a permitted long location','Long cannot replace a short module','Separately specified 185 mm Type C case'][case]
        d.rounded_rectangle((90,835,1830,940),radius=18,fill='#E7F2D8' if case!=2 else '#EEF0FA')
        text(im,(130,858),msg,37,True,NAVY)
    note(im,'Depth comparison is schematic. Each visible case reset changes the configuration being compared.')
    return im

def busbar(t,D):
    im=blank();phase=min(3,int(t/(D/4)))
    fit(im,'figures/busbar_layers.png',(730,70,1100,770))
    # Outline the orange thermal-contact rings in the source section.
    # This is annotation, not calculated thermal transport.
    d=ImageDraw.Draw(im)
    if phase==1:
        d.ellipse((1080,382,1224,526),outline=GREEN,width=4)
        d.ellipse((1382,382,1526,526),outline=GREEN,width=4)
    labels=[('Insulating layer',['GTS 348151 HTS','Electrical isolation','Black in the source section']),('Thermal layer',['TGP3500: 1.5 mm','Compressed to 1.0 mm','Orange in the source section']),('Separate temperature limits',['Outer touch region','Internal clip region','Check applicable test conditions']),('Liquid-cooled implementation',['Layer stack + compression','Selected cooling path','Isolation and thermal evidence'])]
    title,lines=labels[phase];card(im,(90,215,610,600),title,lines,True)
    strip(im,['Insulation','Thermal contact','Touch / clip regions','Evidence'],phase)
    note(im,'Source section retained. Emphasis identifies requirements; no quantitative heat-flow simulation is shown.')
    return im

def float_mate(t,D):
    im=blank();f=t/D;phase=0 if f<.25 else 1 if f<.44 else 2 if f<.63 else 3 if f<.82 else 4
    paths=['figures/uqdfloat_overview.png','figures/uqdfloat_overview.png','figures/uqdfloat_nominal.png','figures/uqdfloat_loading.png','figures/uqdfloat_nominal.png']
    fit(im,paths[phase],(730,80,1100,740))
    entries=[('Gather and engage',['Tray insert + hose adaptor','Spring and washer capture','Rack socket + lead-in cap']),('Controlled float',['Radial and rotational motion','Permitted misalignment','Reference surfaces still matter']),('Axial states',['Nominal: 0.5 mm overmate','Allowed overdrive: 3 mm','Different labeled positions']),('Illustrated spring loading',['Initial preload: 55 lb','Estimated at overdrive: 82 lb','Not total tray insertion force']),('Engagement review',['Nominal versus overdrive','Rack and tray alignment','Actual interface / load evidence'])]
    title,lines=entries[phase];card(im,(90,200,605,630),title,lines,True)
    # Simplified alignment silhouettes below the source section. Display travel
    # is expanded and has no dimensional or force interpretation.
    d=ImageDraw.Draw(im);q=max(0,min(1,f/.25));x=850+400*q
    dy=0 if phase!=1 else 18*math.sin(((f-.25)/.19)*math.pi)*math.sin(((f-.25)/.19)*4*math.pi)
    if phase>=3:x=1280
    d.line((780,769,1780,769),fill='#C6CBD3',width=2)
    d.rounded_rectangle((1400,730,1750,808),radius=10,fill='#D8DDE3',outline=NAVY,width=3)
    d.rounded_rectangle((x,742+dy,x+150,796+dy),radius=8,fill=GREEN,outline=NAVY,width=3)
    text(im,(780,839),'Schematic alignment; display travel expanded',25,color=GRAY)
    strip(im,['Gather','Float','Nominal position','Overdrive'],min(phase,3))
    note(im,'Source sectional views explain permitted movement. Expanded display states are not a verified actuation model.')
    return im

def force(t,D):
    im=blank();f=t/D;stage=0 if f<.23 else 1 if f<.37 else 2 if f<.49 else 3 if f<.59 else 4
    fit(im,'figures/load27_switch.png',(915,95,935,770))
    text(im,(80,65),'27RU switch · maximum mating · lb',39,True,NAVY)
    amounts=[164,409.2,22.5];labels=['2 × 82 = 164 lb (UQD)','4 × 102.3 = 409.2 lb (interconnect)','22.5 lb (busbar)']
    d=ImageDraw.Draw(im)
    for i,(v,label) in enumerate(zip(amounts,labels)):
        y=220+i*175;text(im,(90,y),label,33,True)
        d.rounded_rectangle((90,y+65,810,y+123),radius=7,fill='#E9EDF1')
        if stage>=i+1:
            # Continuous accumulation within each reveal; no backward jump.
            starts=[.23,.37,.49];q=min(1,max(0,(f-starts[i])/.035))
            d.rounded_rectangle((90,y+65,90+v/409.2*720*q,y+123),radius=7,fill=GREEN)
    if stage>=4:card(im,(85,775,740,160),'Derived subtotal: 595.7 lb',[],True)
    note(im,'Illustrative simultaneous maxima. Derived arithmetic is separate from measured force and structural qualification.')
    return im

FUNCTIONS={'rack_build_up':(rack,1,4),'hpm_exploded':(hpm,2,4),'bay_depth_cases':(depth,3,5),'busbar_layers':(busbar,4,7),'blind_mate_float':(float_mate,5,6),'force_budget':(force,6,3)}
def config(name):
    c=json.loads((ROOT/'course.json').read_text());fun,m,s=FUNCTIONS[name];sl=next(slide for slide in c['modules'][m-1]['slides'] if Path(slide.get('figure',{}).get('path','')).stem==name)
    if sl['figure'].get('sync_to_narration'):
        audio = ROOT/sl['audio']['wav_file']
        if audio.exists():
            with wave.open(str(audio)) as wav:
                duration = wav.getnframes()/wav.getframerate()
        else:
            # Preserve the approved master when generated narration is absent.
            reviewed = json.loads((ROOT/'animations/reviewed_timing.json').read_text())
            duration = reviewed[name]['master_duration']
    else:duration=20.0
    return fun,sl,duration
def encode(name):
    fun,slide,D=config(name);count=round(D*FPS);dest=ROOT/slide['figure']['path'];log=QA/(name+'_encode.log')
    cmd=[str(FFMPEG),'-y','-loglevel','warning','-f','image2pipe','-vcodec','png','-framerate',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','slow','-crf','8','-pix_fmt','yuv420p','-frames:v',str(count),'-movflags','+faststart',str(dest)]
    with log.open('wb') as err:
        process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=err)
        prev=None;buf=None
        for n in range(count):
            t=n/FPS;im=fun(t,D)
            # All input frames are lossless PNG, including cached hold states.
            raw=im.tobytes()
            if raw!=prev:
                stream=io.BytesIO();im.save(stream,format='PNG',compress_level=1);buf=stream.getvalue();prev=raw
            process.stdin.write(buf)
            if n%(FPS*20)==0:print(name,round(t,1),'/',round(D,2),flush=True)
        process.stdin.close();rc=process.wait()
    if rc:raise RuntimeError(log.read_text())
    poster=fun(D*.72,D);poster.save(ROOT/slide['figure']['poster'])
    # Review five required positions and transition-adjacent positions, in native resolution.
    positions=sorted(set([0,D*.25,D*.5,D*.75,(count-1)/FPS]+[D*f+d for f in [.23,.25,.28,.37,.44,.46,.48,.49,.59,.63,.68,.82] for d in [-1/FPS,1/FPS] if 0<D*f+d<D]))
    for i,t in enumerate(positions):fun(t,D).save(QA/f'{name}_{i:02}.png')
    record={'name':name,'module':FUNCTIONS[name][1],'slide':slide['id'],'master_duration':D,'encoded_duration':count/FPS,'frame_count':count,'fps':FPS,'resolution':[W,H],'sync_to_narration':bool(slide['figure'].get('sync_to_narration')),'timeline_method':'Measured final WAV; scene landmarks weighted to narration paragraphs, held conclusion','lossless_source_review_seconds':positions,'codec':'libx264 CRF 8, slow, yuv420p'}
    (QA/(name+'_timeline.json')).write_text(json.dumps(record,indent=2))
    print('Completed',name,flush=True)

if __name__=='__main__':
    names=sys.argv[1:] or list(FUNCTIONS)
    if names==['--preview']:
        for name in FUNCTIONS:
            fun,s,D=config(name)
            for i,f in enumerate([0,.25,.5,.75,.999]):fun(D*f,D).save(QA/f'{name}_preview_{i}.png')
    else:
        for name in names:encode(name)

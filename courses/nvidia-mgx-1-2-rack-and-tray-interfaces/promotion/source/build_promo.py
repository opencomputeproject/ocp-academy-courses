"""Finite 30-second LinkedIn course teaser, made from reviewed course footage.

Actual MP4 excerpts are decoded to lossless PNG. UI shots come from the course
home; geometry is not altered. Promo framing uses a 1080-square feed canvas.
"""
from pathlib import Path
import sys,json,math,io,subprocess,functools,os
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'promotion';WORK=ROOT/'_analysis/promo_frames';QA=OUT/'source/review';QA.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'animations'))
from build_media import find_ffmpeg
FF=find_ffmpeg()
FPS=30;DURATION=30;W=H=1080
GREEN='#8DC63F';WHITE='#FFFFFF';INK='#1D2258'
SKILL=Path(os.environ.get('ACADEMY_WIZARD_SKILL_DIR',str(ROOT.parents[1]/'skills/academy-wizard')))
MUSIC=Path(os.environ.get('PROMO_MUSIC_FILE',str(SKILL/'assets/background-music/viacheslavstarostin-educational-presentation-tutorial-music-357862.mp3')))
VIDEO=OUT/'MGX_1.2_LinkedIn_Promo.mp4'
SCENES=[(0,3,'intro'),(3,10,'cad'),(10,14,'float'),(14,18,'busbar'),(18,22,'force'),(22,26,'overview'),(26,30,'cta')]
HEADLINES={'intro':['NVIDIA MGX 1.2','RACK & TRAY INTERFACES'],
 'cad':['SEE THE DESIGN','IN 3D.'],
 'float':['BLIND MATING,','MADE VISIBLE.'],
 'busbar':['POWER AND COOLING.','ONE INTERFACE SYSTEM.'],
 'force':['MAKE ASSUMPTIONS','VISIBLE.'],
 'overview':['SIX MODULES.','DEEP TECHNICAL.']}
CAPTIONS={'intro':'New on OCP Academy',
 'cad':'Supplied HPM geometry | illustrative separation',
 'float':'Float | gathering | engagement',
 'busbar':'Electrical isolation | thermal contact',
 'force':'Illustrative force budget | simultaneous maxima',
 'overview':'Racks | trays | bays | power | cooling | review'}
CLIPS={name:sorted((WORK/name).glob('*.png')) for name in ['cad','float','busbar','force']}
assert all(CLIPS.values()),'Prepare actual course-video excerpts first.'
INDEX=Image.open(OUT/'source/assets/index_home.png').convert('RGB')
INDEX_HEADER=INDEX.crop((220,128,1230,475))
INDEX_MODULES=INDEX.crop((325,255,1115,927))
LOGO=Image.open(OUT/'source/academy_logo.png').convert('RGBA');LOGO.thumbnail((208,104),Image.Resampling.LANCZOS)

@functools.lru_cache(maxsize=30)
def font(size,bold=False):return ImageFont.truetype(str(ROOT/'assets/fonts'/f'open-sans-{800 if bold else 400}.ttf'),size)
@functools.lru_cache(maxsize=500)
def clip_image(name,n):return Image.open(CLIPS[name][min(n,len(CLIPS[name])-1)]).convert('RGB')
def text(im,xy,s,size=40,bold=False,color=WHITE):
 d=ImageDraw.Draw(im);width=d.textlength(s,font=font(size,bold));assert xy[0]+width<=W-45,(s,width)
 d.text(xy,s,font=font(size,bold),fill=color)
def bg():
 im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
 for y in range(H):
  q=y/(H-1);d.line((0,y,W,y),fill=(round(29+18*q),round(34+21*q),round(88+37*q)))
 d.polygon([(1010,0),(1080,0),(1080,1080),(940,1080)],fill='#435095')
 d.polygon([(1066,0),(1080,0),(1080,1080),(1040,1080)],fill=GREEN)
 d.arc((760,-280,1440,400),90,290,fill='#4A559C',width=2)
 d.arc((-280,850,500,1580),205,350,fill='#455096',width=2)
 return im
BACKGROUND=bg()
def fit_panel(im,pic,box,progress=0):
 x,y,w,h=box;d=ImageDraw.Draw(im)
 d.rounded_rectangle((x+6,y+9,x+w+6,y+h+9),radius=24,fill='#202759')
 d.rounded_rectangle((x,y,x+w,y+h),radius=24,fill=WHITE)
 # Pan/scale the paper inside a clipping mask; no source geometry distortion.
 p=pic.copy();p.thumbnail((w-42,h-38),Image.Resampling.LANCZOS)
 scale=1+.025*max(0,min(1,progress));p=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS)
 card=Image.new('RGB',(w,h),'white');card.paste(p,((w-p.width)//2,(h-p.height)//2))
 mask=Image.new('L',(w,h),0);ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=24,fill=255)
 im.paste(card,(x,y),mask)
def brand(im):
 im.paste(LOGO,(58,40),LOGO)
 d=ImageDraw.Draw(im);d.rounded_rectangle((768,70,1020,133),radius=12,fill=GREEN)
 text(im,(799,85),'MGX 1.2',30,True,INK)
def scene(name,u):
 im=BACKGROUND.copy();brand(im)
 if name=='cta':
  text(im,(60,218),'FROM THE MGX WALL',61,True)
  text(im,(60,303),'TO YOUR NEXT',66,True)
  text(im,(60,393),'DESIGN REVIEW.',66,True,GREEN)
  text(im,(60,523),'NVIDIA MGX 1.2',41,True)
  text(im,(60,585),'Rack and Tray Interfaces',39)
  d=ImageDraw.Draw(im);d.rounded_rectangle((60,691,1018,799),radius=18,fill=GREEN)
  label='EXPLORE ON OCP ACADEMY';tw=d.textlength(label,font=font(38,True))
  text(im,((W-tw)/2,719),label,38,True,INK)
  text(im,(60,833),'Course link in the post',34)
  text(im,(60,932),'2026 OCP Global Summit',28)
  text(im,(60,978),'NVIDIA Reception @ MGX Wall',28,False,GREEN)
  return im
 # Two bold lines remain legible without sound in a mobile feed.
 size=61 if name in ['intro','busbar'] else 70
 for i,line in enumerate(HEADLINES[name]):text(im,(60,206+i*91),line,size,True,GREEN if name=='intro' and i else WHITE)
 if name=='intro':
  fit_panel(im,INDEX_HEADER,(52,427,976,423),u)
  text(im,(60,899),'Real drawings. Real CAD. Practical review.',34)
  text(im,(60,982),CAPTIONS[name],32,True,GREEN)
 elif name=='overview':
  fit_panel(im,INDEX_MODULES,(52,400,976,552),u)
  text(im,(60,985),CAPTIONS[name],29,False,GREEN)
 else:
  # Force comparison builds over 2.5 sec, then holds the derived subtotal.
  n=round(u*(2.5*FPS-1)) if name=='force' and u<1 else 0
  if name=='force':n=min(len(CLIPS[name])-1,round(u*4*FPS))
  else:n=round(u*(len(CLIPS[name])-1))
  frame=clip_image(name,n)
  fit_panel(im,frame,(52,405,976,539),u)
  text(im,(60,979),CAPTIONS[name],30,False,GREEN)
 return im
def frame_at(t):
 which=next((x for x in SCENES if x[0]<=t<x[1]),SCENES[-1]);start,end,name=which;u=(t-start)/(end-start)
 im=scene(name,u)
 # Short cross-dissolves between complete finite scenes; no repeated loops.
 if start>0 and t-start<.20:
  prior=SCENES[SCENES.index(which)-1];before=scene(prior[2],1)
  q=(t-start)/.2;q=q*q*(3-2*q);im=Image.blend(before,im,q)
 d=ImageDraw.Draw(im);d.rectangle((0,H-8,round(W*min(t/(DURATION-1/FPS),1)),H),fill=GREEN)
 return im
def preview():
 times=[0,.5,1.8,3.3,5,7.5,9.8,10.3,12.5,13.8,14.3,16,17.8,18.3,20,21.7,22.3,24,25.8,26.3,28.5,29.9667]
 for i,t in enumerate(times):frame_at(t).save(QA/f'preview_{i:02}.png')
 sheet=Image.new('RGB',(1440,math.ceil(len(times)/4)*390),'#dde0e6');d=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  pic=frame_at(t);pic.thumbnail((354,354));x=(i%4)*360;y=(i//4)*390;sheet.paste(pic,(x,y+30));d.text((x+8,y+8),f'{t:.2f}s',fill='black')
 sheet.save(QA/'contact.png');(QA/'review_times.json').write_text(json.dumps(times))
def encode():
 cmd=[str(FF),'-y','-loglevel','warning','-f','image2pipe','-vcodec','png','-framerate',str(FPS),'-i','pipe:0','-i',str(MUSIC),'-filter_complex','[1:a]atrim=0:30,asetpts=PTS-STARTPTS,volume=0.45,afade=t=in:d=0.7,afade=t=out:st=28.7:d=1.3[a]',
 '-map','0:v','-map','[a]','-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p','-frames:v','900','-c:a','aac','-b:a','192k','-ar','48000','-t','30','-movflags','+faststart',str(VIDEO)]
 with (QA/'encode.log').open('wb') as err:
  p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=err)
  for n in range(900):
   stream=io.BytesIO();frame_at(n/FPS).save(stream,format='PNG',compress_level=1);p.stdin.write(stream.getvalue())
   if n%150==0:print('Rendered',n/FPS,'of 30 seconds',flush=True)
  p.stdin.close();rc=p.wait()
  if rc:raise RuntimeError((QA/'encode.log').read_text())
 frame_at(1.8).save(OUT/'MGX_1.2_LinkedIn_Cover.png')
 subprocess.run([str(FF),'-y','-loglevel','error','-i',str(VIDEO),'-map','0:v','-c:v','copy','-an','-movflags','+faststart',str(OUT/'MGX_1.2_LinkedIn_Promo_Silent.mp4')],check=True)
 print('Completed 30-second music and silent promo files',flush=True)

if __name__=='__main__':
 preview()
 if '--preview' not in sys.argv:encode()

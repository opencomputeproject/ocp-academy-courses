from pathlib import Path
import sys,json,subprocess,re
sys.path.insert(0,str(Path(__file__).parent))
from build_promo import ROOT,OUT,QA,FF,VIDEO,FPS,frame_at
from PIL import Image,ImageDraw
times=sorted(set([0,1.8,2.9667,3.2,7.5,9.9667,10.2,12,13.9667,14.2,15,17.9667,18.2,20,21.9667,22.2,22.5,24,25.9667,26.2,29,29.9667]))
frames=[]
for i,t in enumerate(times):
 t=round(t*FPS)/FPS
 dest=QA/f'encoded_{i:02}.png'
 subprocess.run([str(FF),'-y','-loglevel','error','-ss',str(t),'-i',str(VIDEO),'-frames:v','1',str(dest)],check=True);frames.append(dest)
quality=[]
for t in [1.8,7.5,12,16,21,24,29]:
 src=QA/f'lossless_{t}.png';frame_at(t).save(src);metrics={}
 for metric in ['ssim','psnr']:
  filt=f'[0:v]format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[a];[1:v]format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[b];[a][b]{metric}'
  p=subprocess.run([str(FF),'-i',str(src),'-ss',str(t),'-i',str(VIDEO),'-filter_complex',filt,'-frames:v','1','-f','null','-'],capture_output=True,text=True,check=True)
  line=next(x for x in p.stderr.splitlines() if 'Parsed_'+metric in x and ('All:' in x or 'average:' in x));metrics[metric]=line
  val=float(re.search(r'All:([\d.]+)' if metric=='ssim' else r'average:([\d.]+)',line).group(1));assert val>=(.995 if metric=='ssim' else 45),(t,metric,val)
 quality.append({'seconds':t,'metrics':metrics});print('Fidelity pass at',t,'seconds',flush=True)
for p in [VIDEO,OUT/'MGX_1.2_LinkedIn_Promo_Silent.mp4']:
 subprocess.run([str(FF),'-v','error','-i',str(p),'-f','null','-'],capture_output=True,check=True)
sheet=Image.new('RGB',(1440,((len(frames)+3)//4)*390),'#dde0e6');draw=ImageDraw.Draw(sheet)
for i,(p,t) in enumerate(zip(frames,times)):
 im=Image.open(p);im.thumbnail((354,354));x=(i%4)*360;y=(i//4)*390;sheet.paste(im,(x,y+30));draw.text((x+8,y+8),f'{t:.2f}s',fill='black')
sheet.save(QA/'encoded_contact.png')
(QA/'quality.json').write_text(json.dumps({'representative_quality':quality,'decoded_review_seconds':times,'all_frames_decode':'pass'},indent=2))
print('Both complete files decode without error')

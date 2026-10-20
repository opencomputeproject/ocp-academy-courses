"""Verify the retained Summit animation against native source frames."""
from pathlib import Path
import json
import re
import subprocess
from PIL import Image, ImageDraw
from build_summit_media import ROOT, REVIEW, ffmpeg, path_frame

video=ROOT/'figures/summit_power_path.mp4'
times=[0,2,5,9,13,17,599/30]
results=[]
for index,t in enumerate(times):
    reference=REVIEW/f'fidelity_source_{index:02}.png'
    decoded=REVIEW/f'encoded_{index:02}.png'
    path_frame(t).save(reference)
    subprocess.run([ffmpeg(),'-y','-loglevel','error','-ss',str(t),'-i',str(video),
                    '-frames:v','1',str(decoded)],check=True)
    metrics={}
    for metric in ['ssim','psnr']:
        filtergraph=f'[0:v]format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[a];[1:v]format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[b];[a][b]{metric}'
        result=subprocess.run([ffmpeg(),'-i',str(reference),'-ss',str(t),'-i',str(video),
            '-filter_complex',filtergraph,'-frames:v','1','-f','null','-'],capture_output=True,text=True,check=True)
        pattern=r'All:([\d.]+)' if metric=='ssim' else r'average:([\d.]+)'
        value=float(re.search(pattern,result.stderr).group(1))
        assert value >= (.995 if metric=='ssim' else 45),(t,metric,value)
        metrics[metric]=value
    results.append({'seconds':t,**metrics})
    print('Fidelity pass:',t,flush=True)
subprocess.run([ffmpeg(),'-v','error','-i',str(video),'-f','null','-'],check=True)
sheet=Image.new('RGB',(1440,780),'#E0E4EB');draw=ImageDraw.Draw(sheet)
for index,t in enumerate(times):
    im=Image.open(REVIEW/f'encoded_{index:02}.png');im.thumbnail((352,340))
    x=(index%4)*360;y=(index//4)*390
    sheet.paste(im,(x,y+45));draw.text((x+8,y+15),f'{t:.3f}s',fill='black')
sheet.save(REVIEW/'encoded_contact.png')
(REVIEW/'verification.json').write_text(json.dumps({
    'video':'figures/summit_power_path.mp4','duration_seconds':20,
    'fps':30,'frame_count':600,'resolution':[1920,1080],
    'all_frames_decode':'pass','representative_quality':results,
},indent=2)+'\n')
print('All 600 frames decode; seven representative fidelity checks pass.')

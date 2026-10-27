"""Editable source-derived Summit figures and a default 20-second silent loop."""
from pathlib import Path
import functools
import io
import json
import math
import os
import shutil
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures'
REVIEW = ROOT / '_analysis/summit_media'
REVIEW.mkdir(parents=True, exist_ok=True)
W, H, FPS, DURATION = 1920, 1080, 30, 20
NAVY, GREEN, GRAY = '#343895', '#8DC63F', '#5F6062'
TEXT, BORDER = '#27323B', '#D1D7E0'
TRANSCRIPTION = set()

def ffmpeg():
    binary = os.environ.get('FFMPEG_BIN') or shutil.which('ffmpeg')
    if binary:
        return binary
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

@functools.lru_cache(maxsize=60)
def font(size, bold=False):
    return ImageFont.truetype(str(ROOT / 'assets/fonts' / f'open-sans-{700 if bold else 400}.ttf'), size)

def text(im, xy, value, size=32, bold=False, color=TEXT, center=False):
    TRANSCRIPTION.add(value)
    draw = ImageDraw.Draw(im)
    if center:
        xy = (xy[0] - draw.textlength(value, font=font(size, bold))/2, xy[1])
    draw.text(xy, value, font=font(size, bold), fill=color)

def wrap(im, xy, value, width, size=32, bold=False, color=TEXT):
    draw = ImageDraw.Draw(im)
    line, rows = '', []
    for word in value.split():
        candidate = (line + ' ' + word).strip()
        if line and draw.textlength(candidate, font=font(size, bold)) > width:
            rows.append(line)
            line = word
        else:
            line = candidate
    if line:
        rows.append(line)
    for index, row in enumerate(rows):
        text(im, (xy[0], xy[1]+index*size*1.4), row, size, bold, color)

def card(im, box, lines, active=False, size=32):
    x, y, width, height = box
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((x,y,x+width,y+height), radius=12,
        fill='#E8F3D9' if active else '#FFFFFF',
        outline=GREEN if active else NAVY, width=5 if active else 3)
    row_height = size*1.4
    top = y + (height-len(lines)*row_height)/2
    for index, line in enumerate(lines):
        assert draw.textlength(line, font=font(size,True)) < width-30, line
        text(im, (x+width/2, top+index*row_height), line, size, True, NAVY, True)

def arrow(im, x, top, bottom, active=False, t=0):
    draw = ImageDraw.Draw(im)
    color = GREEN if active else GRAY
    draw.line((x,top,x,bottom-14),fill=color,width=6 if active else 4)
    draw.polygon([(x-12,bottom-16),(x+12,bottom-16),(x,bottom)], fill=color)
    if active and bottom-top > 45:
        y = top+18+(bottom-top-43)*(t % 1)
        draw.ellipse((x-8,y-8,x+8,y+8),fill=NAVY)

def zone(im, box, label):
    x,y,width,height=box
    ImageDraw.Draw(im).rounded_rectangle((x,y,x+width,y+height),radius=18,
        fill='#F4F6FA',outline=BORDER,width=2)
    text(im,(x+18,y+12),label,28,True,GRAY)

def path_frame(t):
    im=Image.new('RGB',(W,H),'white')
    stage=min(4,int(t/4))
    pulse=(t % 4)/2
    text(im,(420,25),'Common bus',44,True,NAVY,True)
    text(im,(1330,25),'Point-to-point',44,True,NAVY,True)
    text(im,(420,92),'AC input',32,True,GRAY,True)
    text(im,(1330,92),'AC input to each string',32,True,GRAY,True)

    zone(im,(65,155,710,445),'Power rack')
    zone(im,(65,725,710,305),'Compute rack')
    card(im,(170,220,500,62),['AC PDU'],stage==0)
    card(im,(170,324,500,84),['AC/DC power shelf'],stage==1)
    card(im,(170,502,500,62),['DC PDU'],stage==2)
    arrow(im,420,137,220,stage==0,pulse)
    arrow(im,420,282,324,stage==1,pulse)
    arrow(im,420,408,502,stage==2,pulse)
    text(im,(590,437),'800 VDC busbar',27,False,GRAY,True)
    arrow(im,420,564,784,stage==2,pulse)
    text(im,(575,647),'800 VDC',32,True,NAVY,True)
    text(im,(575,688),'125 A link',29,False,GRAY,True)
    card(im,(170,784,500,70),['DC/DC power shelf'],stage==3)
    arrow(im,420,854,947,stage==4,pulse)
    text(im,(590,883),'54 VDC busbar',27,False,NAVY,True)
    card(im,(170,947,500,62),['Tray'],stage==4)

    zone(im,(825,155,1030,445),'Power rack')
    zone(im,(825,725,1030,305),'Compute rack')
    for x in [1080,1600]:
        card(im,(x-215,270,430,104),['AC/DC','power shelf'],stage==1,32)
        arrow(im,x,137,270,stage==0,pulse)
        arrow(im,x,374,784,stage==2,pulse)
        text(im,(x+115,503),'800 VDC',29,True,NAVY,True)
        text(im,(x+115,544),'125 A link',27,False,GRAY,True)
        card(im,(x-215,784,430,70),['DC/DC power shelf'],stage==3,30)
        arrow(im,x,854,905,stage==4,pulse)
    # Repeated high-voltage strings feed the shared low-voltage rack busbar.
    ImageDraw.Draw(im).line((1080,905,1600,905),fill=GREEN if stage==4 else NAVY,width=7)
    text(im,(1340,860),'54 VDC busbar',27,False,NAVY,True)
    arrow(im,1340,905,947,stage==4,pulse)
    card(im,(1125,947,430,62),['Tray'],stage==4)
    text(im,(1330,646),'Repeating conversion strings',30,True,GRAY,True)
    return im

def fit(im, path, box):
    x,y,width,height=box
    picture=Image.open(path).convert('RGB')
    picture.thumbnail((width,height),Image.Resampling.LANCZOS)
    im.paste(picture,(int(x+(width-picture.width)/2),int(y+(height-picture.height)/2)))

def cooling_figure():
    im=Image.new('RGB',(W,H),'white')
    text(im,(70,45),'Power-shelf interfaces',42,True,NAVY)
    text(im,(1190,45),'Contact cooling',42,True,NAVY)
    fit(im,ROOT/'animations/assets/summit/power_shelf_views.png',(45,150,1080,475))
    fit(im,ROOT/'animations/assets/summit/contact_cutaway.png',(1155,130,715,650))
    draw=ImageDraw.Draw(im)
    draw.rounded_rectangle((65,690,1115,990),radius=18,fill='#F2F5F9',outline=BORDER,width=2)
    text(im,(100,722),'Separate the interfaces',36,True,NAVY)
    wrap(im,(100,785),'Electrical input / output, management, and liquid couplings each need applicable evidence.',970,32)
    wrap(im,(100,893),'TBD input and management labels are retained.',970,30,False,GRAY)
    draw.rounded_rectangle((1190,805,1855,990),radius=18,fill='#E8F3D9',outline=GREEN,width=3)
    text(im,(1225,835),'2036 A clip example',36,True,NAVY)
    wrap(im,(1225,898),'Component rating; qualify the installed contact.',590,30)
    return im

def preview():
    times=[0,2,5,9,13,17,19.9667]
    for index,t in enumerate(times):
        path_frame(t).save(REVIEW/f'path_source_{index:02}.png')
    cooling_figure().save(OUT/'summit_power_contact_cooling.png')
    sheet=Image.new('RGB',(1440,390*2),'#E0E4EB')
    draw=ImageDraw.Draw(sheet)
    for index,t in enumerate(times):
        picture=path_frame(t);picture.thumbnail((352,340))
        x=(index%4)*360;y=(index//4)*390
        sheet.paste(picture,(x,y+45));draw.text((x+8,y+15),f'{t:.2f}s',fill='black')
    sheet.save(REVIEW/'source_contact.png')
    (REVIEW/'text_transcription.json').write_text(json.dumps(sorted(TRANSCRIPTION),indent=2)+'\n')

def encode():
    target=OUT/'summit_power_path.mp4'
    command=[ffmpeg(),'-y','-loglevel','warning','-f','image2pipe','-vcodec','png',
        '-framerate',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','slow',
        '-crf','8','-pix_fmt','yuv420p','-frames:v','600','-movflags','+faststart',str(target)]
    with (REVIEW/'encode.log').open('wb') as log:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
        for index in range(600):
            stream=io.BytesIO()
            path_frame(index/FPS).save(stream,format='PNG',compress_level=1)
            process.stdin.write(stream.getvalue())
        process.stdin.close()
        if process.wait():
            raise RuntimeError((REVIEW/'encode.log').read_text())
    path_frame(9).save(OUT/'summit_power_path_poster.png')
    print('Encoded 20-second, 1920x1080 silent power-path loop.',flush=True)

if __name__=='__main__':
    preview()
    if '--preview' not in sys.argv:
        encode()

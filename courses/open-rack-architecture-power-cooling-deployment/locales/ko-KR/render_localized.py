"""Rebuild a translated single-pass lesson from approved Open Rack scenes and local voice cue frames.

Place this file at the locale root. Requires Pillow, FontTools with Brotli, imageio-ffmpeg and ffmpeg.
The localized JSON scene track keeps geometry identical to the approved English sequence.
"""
from pathlib import Path
import argparse, functools, hashlib, io, json, os, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'animations'))
import render as r
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(slide,manifest):
    cfg=manifest['scenes'][slide]; mp=manifest['labels']; frames=cfg['frames']; states=cfg['states'];source=cfg['geometry'];labeltimes={}; fit={}
    assert len(frames)==len(states)+1 and all(x<y for x,y in zip(frames,frames[1:])) and frames[0]==0
    out=ROOT/cfg['path']; out.parent.mkdir(exist_ok=True)
    ft=TTFont(ROOT/'fonts/locale.woff2');ft.flavor=None; fb=io.BytesIO();ft.save(fb);tt=fb.getvalue()
    ff=os.getenv('FFMPEG_BIN') or r.imageio_ffmpeg.get_ffmpeg_exe()
    @functools.lru_cache(None)
    def font(size,b):
        f=ImageFont.truetype(io.BytesIO(tt),size)
        try:f.set_variation_by_name('Bold' if b else 'Regular')
        except (OSError,ValueError):pass
        return f
    rawtxt=r.txt
    def txt(x,y,s,n=17,c=r.INK,b=False):
        s=str(s);translated=mp[s]
        labeltimes.setdefault(translated,round(start/24,3))
        px,py=r.xy([(x,y)])[0];size=round(2*n*r.zoom);f=font(size,b)
        # Fit to the space allocated to this callout by the English illustration.
        # Short originals get a little extra room so compact acronym labels stay legible.
        maxw=max(36,min(1920-px-12,r.font(size,b).getlength(s)*1.12+4))
        w=f.getlength(translated)
        if w>maxw:
            newsize=max(round(size*.82),round(size*maxw/w));f=font(newsize,b)
        w=max(1,round(f.getlength(translated)))
        if w<=maxw:r.d.text((px,py),translated,font=f,fill=c,anchor='lt');return
        layer=Image.new('RGBA',(w+4,round(size*1.75)),(0,0,0,0));di=ImageDraw.Draw(layer)
        di.text((0,0),translated,font=f,fill=c,anchor='lt')
        layer=layer.resize((max(1,round(maxw)),layer.height),Image.Resampling.LANCZOS)
        r.d._image.paste(layer,(px,py),layer);fit[s]=round(maxw/w,3)
    with tempfile.TemporaryDirectory() as temp:
        tmp=Path(temp);seq=['ffconcat version 1.0'];r.txt=txt
        try:
            for k,start,end in zip(states,frames,frames[1:]):
                length=end-start
                animate=(source,k) in {('m1s3',2),('m1s3',3),('m2s4',10),('m2s5',6),('m3s4',7),('helios_bay',2)}
                steps=min(34,max(2,length//2)) if animate and length>=2 else 1
                for j in range(steps):
                    f=j/(steps-1) if steps>1 else 1;im=r.frame(source,k,f*f*(3-2*f))
                    name=f'frame-{k}-{j}.png';im.save(tmp/name,compress_level=1)
                    hold=(length-steps+1 if j==steps-1 else 1)/24
                    seq+=["file '"+name+"'","option framerate 24",f'duration {hold:.9f}']
        finally:r.txt=rawtxt
        seq+=["file '"+name+"'","option framerate 24"]
        (tmp/'frames.txt').write_text('\n'.join(seq)+'\n')
        dst=tmp/'review.mp4'
        subprocess.run([ff,'-nostdin','-v','error','-f','concat','-safe','0','-i',str(tmp/'frames.txt'),'-vf','fps=24,tpad=stop_mode=clone:stop_duration=0.2','-frames:v',str(frames[-1]),'-c:v','libx264','-threads','3','-preset','veryfast','-crf','13','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(dst)],check=True)
        info=subprocess.run([ff,'-nostdin','-i',str(dst),'-map','0:v','-c','copy','-f','null','-'],capture_output=True,text=True,check=True).stderr
        assert 'Audio:' not in info and '1920x1080' in info and int(re.findall(r'frame=\s*(\d+)',info)[-1])==frames[-1]
        import shutil
        shutil.copyfile(dst,out);r.poster(ff,out)
    return {'duration_seconds':frames[-1]/24,'duration_error_seconds':frames[-1]/24-cfg['duration'],'text_inventory':{'sha256':sha(out),'entries':[{'text':s,'at_seconds':t} for s,t in labeltimes.items()]},'compressed_labels':fit,'narration_sha256':cfg['narration_sha256'],'poster_sha256':sha(ROOT/cfg['poster']),'frames':frames}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('slide');args=parser.parse_args()
    manifest=json.loads((ROOT/'localization/media.json').read_text()); result=build(args.slide,manifest)
    dest=ROOT/'localization/media-qa';dest.mkdir(parents=True,exist_ok=True)
    (dest/(args.slide+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

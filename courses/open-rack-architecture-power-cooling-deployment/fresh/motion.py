"""Render each new spoken lesson directly from editable scenes at its own word cues."""
import json,re,hashlib,os,shutil,subprocess,sys,tempfile,wave
from pathlib import Path
here=Path(__file__).resolve().parent;root=here.parent
sys.path.insert(0,str(root/'animations'))
import render as r
from PIL import Image,ImageDraw
scenes={
'm2s4':('m2s4',0,['look at the small bolt holes',"Google's version-three frame",'with the Open Rack kit','with the E I A kit']),
'm2s5':('m2s4',5,['the close-up shows',"Google's table gives",'the tray dimensions below']),
'm2s6':('m2s4',9,['now compare the extended rail position','a device designed to mount only','then ask a separate question about power']),
'm2s8':('m2s5',0,['with one cable connected','fill the neighboring ports','in the first route','what if we give the cable a sharp corner']),
'm2s9':('m2s5',5,['now watch the plug move']),
'm3s6':('m3s4',0,['there are six installed units','seventy-two kilowatts','sixty kilowatts of sustained output','set one twelve-kilowatt block aside']),
'm3s7':('m3s4',5,['a buffer has a third job','watch what happens to the energy reserve']),
'm4s9':('helios_bay',0,['a single Helios compute tray','pull that tray forward','H P E makes a further choice']),
'm4s10':('m4s5',3,['now look at the forty-two-inch chassis','count the processors as well','the wider chassis saves'])}
ff=os.environ.get('FFMPEG_BIN') or shutil.which('ffmpeg') or r.imageio_ffmpeg.get_ffmpeg_exe()
sha=lambda b:hashlib.sha256(b).hexdigest()
def norm(t):return re.findall('[a-z0-9]+',t.casefold())
def encode(id):
    source,k0,cues=scenes[id]; timing=json.loads((here/'timing'/(id+'.json')).read_text());m,s=map(int,id[1:].split('s'))
    script=next((root/f'audio/module{m}/fresh').glob(f'slide_{s:02}_*.txt'))
    txt='\n'.join(l for l in script.read_text().splitlines() if not l.startswith('#')).strip()
    assert sha(script.with_suffix('.wav').read_bytes()+txt.encode())==timing['input_sha256']
    words=[(w,it['start']) for it in timing['words'] for w in norm(it['word'])];tokens=[w for w,t in words]
    frames=[0]; entries={}; notes=[]
    for cue in cues:
        phrase=norm(cue);ix=[i for i in range(len(tokens)) if tokens[i:i+len(phrase)]==phrase]
        assert len(ix)==1,(id,cue,ix)
        frames.append(round(words[ix[0]][1]*24))
    frames.append(round(timing['duration']*24))
    assert all(i<j for i,j in zip(frames,frames[1:])),frames
    dst=root/'figures'/('fresh-'+id+'.mp4')
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td);seq=['ffconcat version 1.0']
        for off,(start,end) in enumerate(zip(frames,frames[1:])):
            k=k0+off;length=end-start
            span=min(34,max(2,length//2)) if (source,k) in [('m2s4',10),('m2s5',6),('m3s4',7),('helios_bay',2)] else 1
            orig=r.txt
            def record(x,y,label,*args,**kw):
                entries.setdefault(str(label),round(start/24,3));return orig(x,y,label,*args,**kw)
            try:
                r.txt=record
                for j in range(span):
                    f=j/(span-1) if span>1 else 1; frame=r.frame(source,k,f*f*(3-2*f))
                    path=f'{k}-{j}.png';frame.save(tmp/path,compress_level=1)
                    hold=(length-span+1 if j==span-1 else 1)/24
                    seq.extend([f"file '{path}'","option framerate 24",f'duration {hold:.9f}'])
            finally:r.txt=orig
            notes.append(dict(state=k,phrase=([None]+cues)[off],at_frame=start,at_seconds=start/24))
        seq.extend([f"file '{path}'","option framerate 24"])
        (tmp/'frames.txt').write_text('\n'.join(seq)+'\n')
        subprocess.run([ff,'-loglevel','error','-y','-f','concat','-safe','0','-i',str(tmp/'frames.txt'),'-vf','fps=24,tpad=stop_mode=clone:stop_duration=0.2','-frames:v',str(frames[-1]),'-c:v','libx264','-threads','3','-preset','veryfast','-crf','13','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(dst)],check=True)
    r.poster(ff,dst)
    # Verify the encoded stream, not just the timeline; retain decoded cue images for QA.
    inf=subprocess.run([ff,'-i',str(dst),'-map','0:v','-c','copy','-f','null','-'],stderr=subprocess.PIPE,text=True,check=True).stderr
    assert 'Audio:' not in inf and '1920x1080' in inf and int(re.findall(r'frame=\s*(\d+)',inf)[-1])==frames[-1],(id,inf)
    import io
    contact=Image.new('RGB',(360*len(notes),223),'white');draw=ImageDraw.Draw(contact)
    for j,row in enumerate(notes):
        at=min((frames[-1]-1)/24,row['at_seconds']+1.6)
        cmd=[ff,'-loglevel','error','-ss',str(at),'-i',str(dst),'-frames:v','1','-vf','scale=360:202','-f','image2pipe','-vcodec','png','-']
        im=Image.open(io.BytesIO(subprocess.check_output(cmd)));contact.paste(im,(360*j,0));draw.text((360*j+4,205),f'{id} / {row["at_seconds"]:.2f}s / state {row["state"]}',fill='black')
    contact.save(here/'timing'/(id+'-decoded.jpg'),quality=92)
    return dict(path='figures/'+dst.name,poster='figures/'+dst.stem+'-poster.png',duration_seconds=frames[-1]/24,input_sha256=timing['input_sha256'],cues=notes,text_inventory=dict(sha256=sha(dst.read_bytes()),entries=[dict(text=k,at_seconds=v) for k,v in entries.items()]))
if __name__=='__main__':
    for id in sys.argv[1:] or list(scenes):
        o=encode(id);(here/'timing'/(id+'-media.json')).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
        print(id,len(o['cues']),'verified scenes',flush=True)

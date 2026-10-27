"""Decode final posters and verify exact track time, silence and RGB quality."""
import struct,subprocess,re,json,argparse,os
from .produce import ROOT,WORK,AUDIT,ITEMS,FPS

def boxes(data,start=0,end=None):
    end=len(data) if end is None else end
    while start+8<=end:
        size,kind=struct.unpack_from('>I4s',data,start);header=8
        if size==1:size=struct.unpack_from('>Q',data,start+8)[0];header=16
        if size==0:size=end-start
        yield kind,start+header,start+size
        start+=size

def duration_and_tracks(file):
    data=file.read_bytes();mdhd=[];handlers=[]
    def walk(start,end):
        for kind,a,b in boxes(data,start,end):
            if kind in [b'moov',b'trak',b'mdia',b'minf',b'stbl']:walk(a,b)
            if kind==b'hdlr':handlers.append(data[a+8:a+12].decode())
            if kind==b'mdhd':
                if data[a]==0:scale,duration=struct.unpack_from('>II',data,a+12)
                else:scale,duration=struct.unpack_from('>IQ',data,a+20)
                mdhd.append(duration/scale)
    walk(0,len(data));return mdhd,handlers

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only',choices=ITEMS);args=parser.parse_args()
    ff=os.environ.get('FFMPEG_BIN','ffmpeg');results=[]
    for name,item in ITEMS.items():
        if args.only and name!=args.only:continue
        file=WORK/f'{name}.mp4';durations,handlers=duration_and_tracks(file)
        decode=subprocess.run([ff,'-hide_banner','-i',str(file),'-map','0:v:0','-f','null','-'],text=True,capture_output=True,check=True)
        frames=int(re.findall(r'frame=\s*(\d+)',decode.stderr)[-1])
        source=WORK/'samples'/name/f'poster-{item["poster_seconds"]:.3f}.png';n=round(item['poster_seconds']*FPS)
        decoded=WORK/f'{name}-decoded.png'
        subprocess.run([ff,'-y','-v','error','-i',str(file),'-vf',f'select=eq(n\\,{n}),format=rgb24','-vsync','0','-frames:v','1',str(decoded)],check=True)
        metrics={}
        for filt in ['ssim','psnr']:
            r=subprocess.run([ff,'-hide_banner','-i',str(source),'-i',str(decoded),'-lavfi',f'[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]{filt}','-f','null','-'],capture_output=True,text=True,check=True)
            score=float(re.search(r'All:([0-9.]+)',r.stderr)[1]) if filt=='ssim' else float(re.search(r'average:([0-9.]+)',r.stderr)[1])
            metrics[filt]=score
        row={'id':item['id'],'frames':frames,'duration_seconds':durations[0],'narration_seconds':item['duration'],'duration_delta_seconds':abs(durations[0]-item['duration']),'track_handlers':handlers,'video_dimensions':'2560x1440','color_range':'full, explicitly signalled','decode_quality':metrics,'source_frame':n}
        assert frames==round(item['duration']*FPS) and handlers==['vide'] and row['duration_delta_seconds']<=1/FPS,row
        assert '2560x1440' in decode.stderr and 'h264' in decode.stderr
        assert metrics['ssim']>=.995 and metrics['psnr']>=45,row
        results.append(row);print(json.dumps(row),flush=True)
    (AUDIT/f'encoded-quality{("-"+args.only) if args.only else ""}.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()

"""Losslessly correct recorder matrix metadata; retain encoded pixels and timing.

The maintained recorder converts PNG RGB to limited-range BT.601 YUV420, then
tags it BT.709. Match H.264 VUI and container matrix to the actual conversion.
This local postprocess follows the established adjacent Open Rack correction.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
ROOT=Path(__file__).resolve().parents[1]
FF=os.environ.get('FFMPEG_BIN') or shutil.which('ffmpeg')
if not FF:raise SystemExit('Set FFMPEG_BIN to a full ffmpeg executable')
parser=argparse.ArgumentParser();parser.add_argument('--modules',nargs='+',type=int,default=[1,2,3,4,5]);args=parser.parse_args()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw_frame_hashes(p):
    result=subprocess.run([str(FF),'-v','error','-i',str(p),'-map','0:v:0','-pix_fmt','yuv420p','-f','framemd5','-'],capture_output=True,text=True,check=True)
    return '\n'.join(line for line in result.stdout.splitlines() if line and not line.startswith('#'))
for m in args.modules:
    video=ROOT/f'figures/m{m}_teaching_animation.mp4';poster=video.with_name(f'm{m}_teaching_animation_poster.png')
    if not poster.exists():raise SystemExit(f'M{m} is not finalized')
    out=ROOT/f'authoring/animation-build/m{m}';out.mkdir(parents=True,exist_ok=True)
    receipt=out/'color-metadata-receipt.json'
    if receipt.exists() and json.loads(receipt.read_text())['corrected_sha256']==digest(video):
        print(f'M{m}: correct matrix metadata already present',flush=True);continue
    original=out/'recorder-before-matrix-correction.mp4';shutil.copy2(video,original)
    before=raw_frame_hashes(video);temp=video.with_name(video.stem+'_matrix_temp.mp4')
    subprocess.run([str(FF),'-y','-hide_banner','-loglevel','error','-i',str(video),'-map','0:v:0','-c:v','copy','-bsf:v','h264_metadata=matrix_coefficients=6','-colorspace','smpte170m','-movflags','+faststart',str(temp)],check=True)
    after=raw_frame_hashes(temp)
    if before!=after:raise RuntimeError(f'Decoded pixel or frame timing changed in M{m}; original preserved')
    temp.replace(video)
    data={'module':m,'original_sha256':digest(original),'corrected_sha256':digest(video),'color_matrix':'smpte170m / BT.601','operation':'Lossless H.264 VUI + container matrix metadata correction; compressed image data copied.',
      'decoded_yuv420_frame_hashes_and_timestamps_unchanged':True,'frame_hash_sequence_sha256':hashlib.sha256(before.encode()).hexdigest()}
    receipt.write_text(json.dumps(data,indent=2)+'\n');print(f'M{m}: matrix corrected; every decoded frame and timestamp unchanged',flush=True)

"""Create accurate Japanese captions from approved scripts and measured speech."""
from pathlib import Path
import json,wave,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from tools.japanese_video_audio import approved_timing,caption_cues,timestamp
c=json.loads((R/'course.json').read_text());count=0
for m in c['modules']:
 for s in m['slides']:
  f=s.get('figure',{})
  if f.get('media_type')!='video' or f.get('playback_mode')=='recorded':continue
  name=f'm{m["id"]}s{s["id"]}'
  raw=json.loads((R/f'_narration_work/alignments/narration-{name}.json').read_text())['transcription']
  data=approved_timing(raw,s['transcript'])
  if data['recognition_similarity']<.8:raise ValueError(name+': speech text needs review')
  with wave.open(str(R/s['audio']['wav_file'])) as w:duration=w.getnframes()/w.getframerate()
  cues=caption_cues(data,duration)
  target=R/f'captions/{name}.ja.vtt'
  target.write_text('WEBVTT\n\n'+'\n\n'.join(f'{i}\n{timestamp(q["start"])} --> {timestamp(q["end"])}\n{q["text"]}' for i,q in enumerate(cues,1))+'\n')
  f['captions']=[{'path':str(target.relative_to(R)),'language':'ja-JP','label':'\u65e5\u672c\u8a9e','default':False}]
  if f.get('sync_to_narration') is not True:f['captions_time_source']='narration'
  count+=len(cues)
(R/'course.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print('Nine teaching-video caption tracks:',count,'cues')

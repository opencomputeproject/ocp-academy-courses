"""Retime finite HTML video sources from matching built-course WAVs and TXT anchors.
Usage: python3 scripts/retime_videos.py /path/to/built-course
Writes only this course's animation sources and authoring/video-plan.json.
Re-encode and review changed animations before replacing published media.
"""
from pathlib import Path
import argparse,json,re,wave,hashlib
p=argparse.ArgumentParser();p.add_argument('built_course',type=Path);a=p.parse_args()
source=Path(__file__).resolve().parents[1];runtime=a.built_course.resolve();course=json.loads((source/'course.json').read_text());plan_path=source/'authoring/video-plan.json';plan=json.loads(plan_path.read_text());anchors=json.loads((source/'authoring/cue-map.json').read_text());slides={s['planning_id']:s for m in course['modules'] for s in m['slides']};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for v in plan['videos']:
 tag=v['id'];s=slides[tag];txt=source/s['audio']['script_file'];wav=runtime/s['audio']['wav_file'];spoken=' '.join(l for l in txt.read_text().splitlines() if not l.startswith('#')).strip()
 with wave.open(str(wav)) as w:
  pcm={'frames':w.getnframes(),'sample_rate':w.getframerate(),'channels':w.getnchannels(),'sample_width_bytes':w.getsampwidth()};duration=pcm['frames']/pcm['sample_rate']
 tokens=list(re.finditer(r'\S+',spoken));cues={};details=[];ms=round(duration*1000,6)
 for cue,phrase in anchors[tag].items():
  at=spoken.lower().find(phrase.lower())
  if at<0:raise ValueError(f'{tag}: missing phrase: {phrase}')
  count=sum(t.start()<at for t in tokens);time=round(min(max(0,ms-4800),count/len(tokens)*ms),3);cues[cue]=time;details.append({'cue':cue,'phrase':phrase,'estimated_seconds':time/1000,'spoken_word_offset':count,'spoken_word_fraction':count/len(tokens),'method':'editorial word-position estimate, not forced alignment'})
 html=source/'animations'/f'{tag}.html';text=html.read_text();text=re.sub(r'data-duration-ms="[^"]+"',f'data-duration-ms="{ms}"',text);text=re.sub(r'data-poster-ms="[^"]+"',f'data-poster-ms="{ms}"',text);text=re.sub(r'window.teachingCues=\{[^;]+;',f'window.teachingCues={json.dumps(cues)};',text);html.write_text(text)
 v.update(duration_ms=ms,poster_ms=ms,narration_anchors=details,sequence=[item['phrase'] for item in details])
 v['timing'].update(duration_method='measured PCM WAV duration',pcm=pcm,word_count=len(tokens),spoken_script=s['audio']['script_file'],audio=s['audio']['wav_file'],alignment='Editorial spoken-word estimates, not forced alignment; review against narration.',completed_picture_hold_seconds=round((ms-max(cues.values())-1800)/1000,3))
 v['hashes'].update(spoken_txt=sha(txt),audio_wav=sha(wav),animation_html=sha(html),cue_map=sha(source/'authoring/cue-map.json'))
 v['source']=f'animations/{tag}.html'
 print(tag,f'{duration:.3f}s; re-encode and review before delivery')
plan['status']='Retimed from measured WAVs; encoding and cue listening review required.';plan_path.write_text(json.dumps(plan,indent=2)+'\n')

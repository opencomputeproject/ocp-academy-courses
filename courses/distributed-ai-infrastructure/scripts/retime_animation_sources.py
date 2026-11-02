"""Bind editable deterministic animation sources to the current final narration WAVs.

Only owns the five new animation HTML/config files. Does not modify course.json.
"""
import argparse
import hashlib
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
import wave

ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT
OUT=ROOT/'animations'
parser=argparse.ArgumentParser()
parser.add_argument('--modules',nargs='+',type=int,default=[1,2,3,4,5])
parser.add_argument('--require-audio',action='store_true')
parser.add_argument('--runtime',type=Path,default=ROOT,help='Built course folder containing generated WAVs')
args=parser.parse_args()
COURSE=args.runtime.resolve()
course=json.loads((ROOT/'course.json').read_text())
fallback={1:70,2:80,3:90,4:95,5:90}
OUT.mkdir(exist_ok=True)
report={}
for number in args.modules:
    slide=course['modules'][number-1]['slides'][4]
    audio=COURSE/slide['audio']['wav_file']
    actual=audio.exists()
    if args.require_audio and not actual:
        raise SystemExit(f'Final narration not available: {audio}')
    if actual:
        with wave.open(str(audio)) as wav:
            duration=wav.getnframes()/wav.getframerate()
    else:
        duration=fallback[number]
    paragraphs=slide['transcript'].split('\n\n')
    counts=[len(p.split()) for p in paragraphs]
    total=sum(counts)
    # Initial proportional cues are editable and are retained for reproducibility.
    # Last 1.5% of measured audio holds the conclusion; all earlier scene boundaries
    # follow canonical spoken paragraph word positions.
    cursor=0
    cue=[]
    for i,(p,count) in enumerate(zip(paragraphs,counts)):
        start=cursor/total*duration*1000*.985
        cursor+=count
        end=cursor/total*duration*1000*.985 if i<len(counts)-1 else duration*1000
        cue.append({'paragraph':i,'start':round(start,3),'end':round(end,3),'text':p,'words':count})
    alignment_file=ROOT/f'authoring/alignment/M{number}S5.json'
    events={}
    if actual and alignment_file.exists():
        alignment=json.loads(alignment_file.read_text())
        if alignment['wav_sha256']!=hashlib.sha256(audio.read_bytes()).hexdigest():
            raise SystemExit(f'Alignment hash does not match final audio: {alignment_file}')
        def normalize(s):return re.sub(r'[^a-z0-9]','',s.lower())
        words=alignment['words']
        normalized=[normalize(w['text']) for w in words]
        last=0
        for i,p in enumerate(paragraphs):
            if i==0:cue[i]['start']=0;continue
            target=[normalize(w) for w in p.split()[:4]]
            matches=[j for j in range(last,len(words)-len(target)+1) if normalized[j:j+len(target)]==target]
            if matches:j=matches[0];score=1
            else:
                candidates=[(SequenceMatcher(None,target,normalized[j:j+len(target)]).ratio(),j) for j in range(last,len(words)-len(target)+1)]
                score,j=max(candidates,key=lambda v:(v[0],-v[1]))
            if score<.75:raise SystemExit(f'Paragraph alignment uncertain: M{number} P{i} ({score})')
            cue[i]['start']=round(words[j]['start']*1000,3);cue[i]['alignment_match']=score;last=j+len(target)
        for i in range(len(cue)-1):cue[i]['end']=cue[i+1]['start']
        cue[-1]['end']=duration*1000
        event_phrases={
          1:{'serving_start':('three requests finish','start'),'serving_early':('100 milliseconds','end'),'serving_late':('the fourth takes 140','end'),'training_start':('three participants are ready','start'),'training_early':('after 100 milliseconds','end'),'training_late':('the fourth needs another 40','end')},
          2:{'gradients':('the local gradients','start'),'mean':('averaged gradient five','end'),'updated':('all reach 9 .5','end')},
          3:{'second_case':('in the second','start')},
          4:{'supply_drop':('supply then falls','start'),'buffer_6':('buffer holds six','end'),'buffer_4':('it holds four','end'),'buffer_2':('it holds two','end'),'buffer_0':('after the fourth second','end'),'supply_limited':('during the following second','start')},
          5:{'failure':('loses a participant','end')}
        }
        for name,(phrase,which) in event_phrases[number].items():
            target=[normalize(w) for w in phrase.split()]
            matches=[j for j in range(len(words)-len(target)+1) if normalized[j:j+len(target)]==target]
            if not matches:raise SystemExit(f'Event anchor not found: M{number} {phrase}')
            j=matches[0];idx=j if which=='start' else j+len(target)-1
            events[name]=round(words[idx][which]*1000,3)
    config={'module':number,'durationMs':round(duration*1000,6),'posterMs':round(duration*1000*.985,3),'audio_path':str(audio.relative_to(COURSE)),
            'audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest() if actual else None,'measured_audio':actual,
            'timing_basis':('Local ASR word timestamps matched to approved paragraph openings and key quantities; remaining within-paragraph cues are proportional. Not forced alignment or human listening approval.' if events else 'Proportional canonical transcript paragraph word positions, pending audiovisual listening confirmation.'),
            'alignment_file':str(alignment_file.relative_to(ROOT)) if events else None,'events':events,
            'paragraphs':cue,'final_hold_ms':round(duration*1000-cue[-1]['start'],3)}
    (OUT/f'm{number}_timing.json').write_text(json.dumps(config,indent=2)+'\n')
    html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Technical teaching animation</title>
<style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#fff}svg{display:block;width:100%;height:100%;font-family:Arial,Helvetica,sans-serif}*{box-sizing:border-box}</style>
</head><body data-duration-ms="__DURATION__" data-poster-ms="__POSTER__"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" role="img" aria-label="__ALT__"></svg>
<script>window.TEACHING_CONFIG=__CONFIG__;</script><script src="teaching.js"></script></body></html>'''
    html=html.replace('__DURATION__',str(config['durationMs'])).replace('__POSTER__',str(config['posterMs'])).replace('__ALT__',slide['title']).replace('__CONFIG__',json.dumps(config))
    (OUT/f'm{number}_teaching_animation.html').write_text(html)
    report[f'M{number}S5']={'duration_seconds':duration,'audio_exists':actual,'source':str(OUT/f'm{number}_teaching_animation.html'),'paragraph_cues':len(cue)}
print(json.dumps(report,indent=2))

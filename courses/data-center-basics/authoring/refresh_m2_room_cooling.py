"""Refresh current content records after reviewed M2 room-cooling edits."""
from pathlib import Path
import json,sys,hashlib,wave,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parents[1];Q=P/'authoring/qa/m2-room-cooling';sys.path.insert(0,str(P/'authoring/toolchain/academy-wizard/scripts'))
from glossary_audit import slide_sources,match_term,glossary_exclusion_reason,audit_glossary
c=json.loads((P/'course.json').read_text());newids=set()
for s in c['modules'][1]['slides'][8:10]:
 f=s['figure'];entries=[{'text':' '.join(e.itertext())} for e in ET.parse(P/f['path']).iter() if e.tag.endswith('}text') and ''.join(e.itertext()).strip()];f['text_inventory']={'sha256':hashlib.sha256((P/f['path']).read_bytes()).hexdigest(),'entries':entries,'reviewed_on':'2026-10-27','review_method':'Native rendered SVG review; label clearance, clipping and arrow geometry checks.'}
s=c['modules'][1]['slides'][10];f=s['figure'];record=json.loads((Q/'source-build-records.json').read_text())[0]
f['text_inventory']={'sha256':hashlib.sha256((P/f['path']).read_bytes()).hexdigest(),'entries':[{'text':x,'at_seconds':0} for x in record['text'] if x.strip()],'reviewed_on':'2026-10-27','review_method':'Reviewed native full-size frames, transition states and decoded samples; Scribe v2 word timestamps from the final delivered WAV; measured complete muted course playback.'}
for m in c['modules']:
 for s in m['slides']:s['term_refs']=[t for t in s.get('term_refs',[]) if t not in newids]
 for term in [t for t in c['term_glossary'] if t['id'] in newids]:
  for index,s in enumerate(m['slides']):
   if glossary_exclusion_reason(s,index,len(m['slides'])):continue
   sources,errs=slide_sources(s,c,m,P)
   if errs:raise ValueError(errs)
   if any(match_term(term,x['text']) for x in sources):s.setdefault('term_refs',[]).append(term['id']);break
errors,evidence=audit_glossary(c,P);assert not errors,errors
(Q/'glossary-placement.json').write_text(json.dumps({'definitions':len(c['term_glossary']),'placements':len(evidence),'errors':errors,'evidence':evidence},indent=2)+'\n')
meta=json.loads((P/'lms-metadata.json').read_text());modules=[]
for m in c['modules']:
 sec=0
 for s in m['slides']:
  if s.get('audio'):
   with wave.open(str(P/s['audio']['wav_file'])) as w:sec+=w.getnframes()/w.getframerate()
 old=meta['modules'][m['id']-1];modules.append(dict(old,narration_seconds=round(sec,3),sequential_media_seconds=round(sec+old['original_video_seconds'],3),seat_minutes_estimate=c['lms_catalog']['modules'][m['id']-1]['duration_minutes'],summary=c['lms_catalog']['modules'][m['id']-1]['summary']))
ns=round(sum(x['narration_seconds'] for x in modules),3);seq=round(ns+meta['measured_original_video_seconds'],3)
meta.update(estimated_seat_minutes=c['lms_catalog']['duration_minutes'],measured_narration_seconds=ns,measured_sequential_media_seconds=seq,glossary_terms=len(c['term_glossary']),retained_source_knowledge_checks=10,replaced_source_knowledge_checks=['M2-KC2','M3-KC2'],new_knowledge_checks=3,modules=modules)
(P/'lms-metadata.json').write_text(json.dumps(meta,indent=2)+'\n');c['duration_plan'].update(narration_seconds=ns,total_sequential_media_seconds=seq,timing_status='Measured narration and original recordings; estimated 95-minute seat time including reading/reflection/checks; optional retries/references vary.');c['m2_room_cooling_revision'].update(measured_narration_seconds=ns,measured_sequential_media_seconds=seq)
(P/'course.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
lines=['# Course glossary','','Definitions at verified substantive use. Black space is explicitly project-specific.','','| Term | Definition | Source |','|---|---|---|']
for t in c['term_glossary']:lines.append(f"| {t['term']} | {t['tooltip']} | [Source]({t['url']}) |")
(P/'authoring/Glossary.md').write_text('\n'.join(lines)+'\n')
for m in c['modules']:
 lines=[f"# Module {m['id']} · {m['title']}",'']
 for s in m['slides']:
  lines+=[f"## M{m['id']}S{s['id']} · {s.get('title',s['type'])}",'',json.dumps({k:v for k,v in s.items() if k not in ['audio','figure','video_transcript','transcript']},ensure_ascii=False,indent=2),'']
  if s.get('audio'):lines+=['Narration:',(P/s['audio']['script_file']).read_text()]
  if s.get('video_transcript'):lines+=['Imported transcript:',s['video_transcript']]
  if s.get('figure'):lines+=['Media:',json.dumps(s['figure'],ensure_ascii=False,indent=2)]
 (Q/f'Module_{m["id"]}_Current_Content.md').write_text('\n'.join(lines)+'\n')
print(len(c['term_glossary']),'terms;',len(evidence),'placements;',ns,'narration seconds;',seq,'sequential seconds')

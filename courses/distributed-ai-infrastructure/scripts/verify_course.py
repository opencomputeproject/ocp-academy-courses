"""Verify a built course against its reviewed source, media, audio and captions."""
from pathlib import Path
import hashlib,json,re,sys,wave,xml.etree.ElementTree as ET

SOURCE=Path(__file__).resolve().parents[1]
root=Path(sys.argv[1]).resolve()
course=json.loads((root/'course.json').read_text())
integrity=json.loads((SOURCE/'authoring/media-integrity.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for entry in integrity['files']:
    assert sha(root/entry['path'])==entry['sha256'],entry['path']
for entry in integrity['generated_audio']:
    audio=root/entry['path'];assert sha(audio)==entry['sha256'],entry['path']
    with wave.open(str(audio)) as w:duration=w.getnframes()/w.getframerate()
    assert abs(duration-entry['duration_seconds'])<.001,entry['path']
assert len(course['modules'])==5 and sum(len(m['slides']) for m in course['modules'])==57
assert sum(len(s.get('questions',[])) for m in course['modules'] for s in m['slides'])==10
assert [(m['id'],s['id']) for m in course['modules'] for s in m['slides'] if s.get('show_context_note') is True]==[(1,4)]
payloads=[];recordings=animations=0
for m in course['modules']:
    html=(root/f"module{m['id']}.html").read_text()
    assert html.count('class="slide-subtitle slide-context-note animate-in"')==(1 if m['id']==1 else 0)
    for s in m['slides']:
        f=s.get('figure') or {}
        if f.get('role')=='original_video':
            recordings+=1;assert s['audio'] is None and s['narration_enabled'] is False
            assert f.get('captions') and all(t.get('language')=='en-US' and t.get('label')=='English (US)' for t in f['captions'])
            expected='With Ankur Sharma' if (m['id'],s['id']) in [(1,4),(5,8)] else 'By Ankur Sharma'
            assert s['section_label']==expected
        if f.get('sync_to_narration'):
            animations+=1;assert f['loop'] is False and f['autoplay'] is False and f['muted'] is True
    payloads.extend(json.loads(p) for p in re.findall(r'<script class="academy-video__caption-data" type="application/json">(.*?)</script>',html,re.S))
assert recordings==8 and animations==5 and len(payloads)==8
assert all(t['language']=='en-US' and t['label']=='English (US)' for p in payloads for t in p['tracks'])
assert sum(len(t['cues']) for p in payloads for t in p['tracks'])==390
caption_text=' '.join(c['text'] for p in payloads for t in p['tracks'] for c in t['cues'])
for old,new in [('destination note','destination node'),('GPUs 12,','GPUs 1, 2,'),('distributed air','distributed AI'),('Guard rule','Guardrail')]:
    assert old not in caption_text and new in caption_text
manifest=ET.parse(root/'imsmanifest.xml')
scos=[e for e in manifest.iter() if e.get('{http://www.adlnet.org/xsd/adlcp_rootv1p2}scormtype')=='sco']
assert len(scos)==6 and {e.get('href') for e in scos}=={'index.html',*[f'module{n}.html' for n in range(1,6)]}
namespace=manifest.getroot().tag.split('}')[0].lstrip('{')
resources={e.get('identifier'):e.get('href') for e in manifest.iter(f'{{{namespace}}}resource')}
organization=manifest.find(f'.//{{{namespace}}}organization')
assert [resources[e.get('identifierref')] for e in organization.findall(f'{{{namespace}}}item')]==['index.html',*[f'module{n}.html' for n in range(1,6)]]
print('PASS: reviewed asset/audio hashes, 57 slides, 6 Home-first SCOs, 8 recordings, 5 animations, 10 questions and 390 caption cues.')

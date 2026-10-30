"""Verify the built runtime against deliberately reviewed media and script hashes."""
from pathlib import Path
import sys,json,hashlib,wave,xml.etree.ElementTree as ET
source=Path(__file__).resolve().parents[1];root=Path(sys.argv[1]).resolve();c=json.loads((root/'course.json').read_text());inventory=json.loads((source/'authoring/media-integrity.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=0
for entry in inventory['files']:
 p=root/entry['path'];assert p.is_file(),p
 assert sha(p)==entry['sha256'],f'Reviewed hash changed: {p}';checks+=1
assert len(c['modules'])==4;checks+=1
assert sum(len(m['slides']) for m in c['modules'])==45;checks+=1
videos=[];audio=0
for m in c['modules']:
 for s in m['slides']:
  a=s['audio'];assert a['model_id']=='eleven_v4';audio+=1;checks+=1
  with wave.open(str(root/a['wav_file'])) as w:seconds=w.getnframes()/w.getframerate()
  assert abs(seconds-a['duration_seconds'])<.001;checks+=1
  if s.get('figure',{}).get('sync_to_narration'):
   f=s['figure'];assert f['loop'] is False and f['autoplay'] is False and f['muted'] is True;videos.append(s['planning_id']);checks+=1
assert audio==45 and len(videos)==5;checks+=1
manifest=ET.parse(root/'imsmanifest.xml');ns={'s':'http://www.imsproject.org/xsd/imscp_rootv1p1p2','a':'http://www.adlnet.org/xsd/adlcp_rootv1p2'};sco=[e for e in manifest.iter() if e.get('{http://www.adlnet.org/xsd/adlcp_rootv1p2}scormtype')=='sco'];assert len(sco)==5;checks+=1
for name in ['index.html','module1.html','module2.html','module3.html','module4.html']:assert (root/name).is_file();checks+=1
print(f'PASS: {checks} reviewed script/media, narration, timing and five-SCO structure checks.')

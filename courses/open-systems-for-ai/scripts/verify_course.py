"""Verify editable media/scripts and, when supplied, the rebuilt six-SCO package.

Usage: python3 scripts/verify_course.py [built-course-folder]
"""
from pathlib import Path
import hashlib
import json
import sys
import wave
import zipfile
from xml.etree import ElementTree as ET
source = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else source
course = json.loads((root / 'course.json').read_text())
index = json.loads((source / 'authoring/media-integrity.json').read_text())
checks = 0

def check(condition, message):
    global checks
    if not condition:
        raise AssertionError(message)
    checks += 1

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

check(len(course['modules']) == 6, 'Six modules required')
check(sum(len(m['slides']) for m in course['modules']) == 72, '72 slides required')
check(course['scorm'] == {'version': '1.2', 'organization': 'multi-sco', 'include_home_sco': False}, 'Six-SCO architecture')
check(course['narration']['model_id'] == 'eleven_v4' and course['narration']['speed'] == 1.18, 'Full-v4 pacing')
recordings = videos = narration = 0
for module in course['modules']:
    questions = [q for s in module['slides'] for q in s.get('questions', [])]
    check(len(questions) == 2, f'Module {module["id"]}: two assessments')
    for slide in module['slides']:
        figure = slide.get('figure') or {}
        if slide.get('audio'):
            narration += 1
        if figure.get('role') == 'original_video':
            recordings += 1
            check(slide.get('audio') is None and slide.get('narration_enabled') is False, 'Recording owns audio')
            check(bool(figure.get('captions')) and bool(figure.get('caption_cues')), 'Recording captions and local fallback')
        elif figure.get('media_type') == 'video':
            videos += 1
            check(all(figure.get(k) is v for k, v in {'sync_to_narration': True, 'autoplay': False, 'loop': False, 'muted': True}.items()), 'Single-pass teaching video')
check((recordings, videos, narration) == (6, 8, 66), 'Media counts')
for relative, expected in index['source_files'].items():
    p = (source if relative.startswith('animations/') else root) / relative
    check(p.is_file() and digest(p) == expected, f'Media changed: {relative}; review and update integrity inventory')
for item in index['narration']:
    check(digest(root / item['script']) == item['script_sha256'], f'Script changed: {item["script"]}; regenerate/review audio and update inventory')
    if root != source:
        wav = root / item['wav']
        check(digest(wav) == item['wav_sha256'], f'Audio differs: {item["wav"]}')
        with wave.open(str(wav)) as audio:
            check(abs(audio.getnframes() / audio.getframerate() - item['seconds']) < .02, 'Narration duration')
if root != source:
    ns = {'i': 'http://www.imsproject.org/xsd/imscp_rootv1p1p2'}
    adl = '{http://www.adlnet.org/xsd/adlcp_rootv1p2}'
    manifest = ET.parse(root / 'imsmanifest.xml')
    resources = manifest.findall('.//i:resource', ns)
    check([r.get('href') for r in resources if r.get(adl + 'scormtype') == 'sco'] == [f'module{i}.html' for i in range(1, 7)], 'Exactly six module SCOs')
    check(len(manifest.findall('.//i:item', ns)) == 6, 'Six syllabus items')
    check(next(r for r in resources if r.get('href') == 'index.html').get(adl + 'scormtype') == 'asset', 'Untracked Home')
    home = (root / 'index.html').read_text()
    check(all(x not in home for x in ['SCORM.init()', 'SCORM.setCompleted()', 'SCORM.finish()']), 'Home cannot write LMS completion')
    archive = root.with_suffix('.zip')
    if archive.is_file():
        declared = {e.get('href') for e in manifest.findall('.//i:file', ns)} | {'imsmanifest.xml'}
        with zipfile.ZipFile(archive) as z:
            check(z.testzip() is None, 'Archive CRC')
            check(set(z.namelist()) == declared, 'Exact manifest archive set')
            for relative in declared:
                check(hashlib.sha256(z.read(relative)).hexdigest() == digest(root / relative), f'Stale archive entry: {relative}')
print(f'Passed {checks} source/media/package checks.')

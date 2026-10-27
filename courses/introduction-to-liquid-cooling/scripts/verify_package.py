"""Check five SCO launches and the reviewed course/media contracts after building."""
from pathlib import Path
import json
import sys
import zipfile
from scorm_contract import validate_home_and_modules

output = Path(sys.argv[1]).resolve()
course = json.loads((output / 'course.json').read_text())
validate_home_and_modules((output / 'imsmanifest.xml').read_bytes(), course)
assert sum(len(module['slides']) for module in course['modules']) == 52
assert len(list((output / 'audio').rglob('*.wav'))) == 48
assert course['modules'][-1]['slides'][-1]['summary_items'] == []
for module in course['modules']:
    recording = module['slides'][8]
    assert recording['figure']['role'] == 'original_video'
    assert recording['audio'] is None and recording['narration_enabled'] is False
home = (output / 'index.html').read_text()
assert 'const inLMS = !reviewMode && SCORM.init();' in home
assert 'if (!reviewMode) SCORM.setCompleted();' in home
with zipfile.ZipFile(output.with_suffix('.zip')) as archive:
    assert archive.testzip() is None
    validate_home_and_modules(archive.read('imsmanifest.xml'), course)
    assert all(archive.read(name) == (output / name).read_bytes() for name in archive.namelist())
print('PASS: Course Home plus four module SCOs, 52 slides, 48 narration clips, recording audio ownership and archive parity.')

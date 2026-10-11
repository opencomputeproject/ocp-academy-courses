#!/usr/bin/env python3
"""Reject a build whose narration no longer matches its synchronized media."""

import hashlib
import json
import sys
import wave
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]


def validate(course_file):
    package = course_file.parent
    course = json.loads(course_file.read_text())
    plan = json.loads((SOURCE / 'animations/plan.json').read_text())
    for video in plan['videos']:
        slide = next(s for m in course['modules'] if m['id'] == video['module']
                     for s in m['slides'] if s['id'] == video['slide'])
        master = json.loads((SOURCE / slide['figure']['animation_source']).read_text())
        audio = package / slide['audio']['wav_file']
        if not audio.is_file():
            raise SystemExit(f'Missing synchronized narration: {audio}')
        sha = hashlib.sha256(audio.read_bytes()).hexdigest()
        if sha != master['audio_provenance']['wav_sha256']:
            raise SystemExit(f'M{video["module"]}S{video["slide"]}: narration differs from the reviewed video timing. Regenerate with timestamps, re-render and visually review the animation before packaging; see the course README.')
        with wave.open(str(audio)) as wav:
            duration = wav.getnframes() / wav.getframerate()
        if abs(duration - master['duration']) > 1 / master['fps']:
            raise SystemExit(f'Video/narration duration mismatch: {video["id"]}')
        if slide['figure'].get('sync_to_narration') is not True:
            raise SystemExit(f'Synchronized playback is not enabled: {video["id"]}')
    print('Verified all six synchronized videos against their exact narration recordings.')


if __name__ == '__main__':
    validate(Path(sys.argv[1]).resolve())

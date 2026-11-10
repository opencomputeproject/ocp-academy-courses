"""Fail closed when reviewed teaching media no longer matches the narration."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import wave


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit('Usage: build_resources.py <staged-course.json>')
    course_path = Path(sys.argv[1]).resolve()
    course = json.loads(course_path.read_text(encoding='utf-8'))
    root = course_path.parent
    source_root = Path(__file__).resolve().parents[1]
    timing_path = source_root / 'animations/full-v4/timings.final.json'
    timings = json.loads(timing_path.read_text(encoding='utf-8'))
    locale = course.get('language') or 'en-US'
    edition = timings.get('editions', {}).get(locale, {})
    checked = 0
    for module in course['modules']:
        for slide in module['slides']:
            figure = slide.get('figure') or {}
            if figure.get('media_type') != 'video':
                continue
            label = f"{locale} M{module['id']}S{slide['id']}"
            media = root / figure['path']
            inventory = figure.get('text_inventory') or {}
            if not media.is_file() or sha256(media) != inventory.get('sha256'):
                raise SystemExit(f'{label}: teaching video is missing or changed after visual review.')
            if not figure.get('sync_to_narration'):
                continue
            timing = edition.get(f"M{module['id']}S{slide['id']}") or {}
            audio = root / slide['audio']['wav_file']
            script = root / slide['audio']['script_file']
            spoken = '\n'.join(line for line in script.read_text(encoding='utf-8').splitlines()
                               if not line.startswith('#')).strip()
            if hashlib.sha256(spoken.encode()).hexdigest() != figure.get('narration_script_sha256'):
                raise SystemExit(f'{label}: narration script differs from the reviewed recording/video pairing.')
            if not timing.get('cues_reviewed') or not audio.is_file() or sha256(audio) != timing.get('narration_sha256'):
                raise SystemExit(
                    f'{label}: narration no longer matches the reviewed animation cues. '
                    'Review the new recording and retime/re-encode its teaching video before packaging. '
                    'See animations/full-v4/README.md; do not relabel an old recording as a new one.'
                )
            with wave.open(str(audio), 'rb') as reader:
                seconds = reader.getnframes() / reader.getframerate()
            if abs(seconds * 1000 - timing['duration_ms']) > 1000 / 30 + 5:
                raise SystemExit(f'{label}: reviewed timing duration differs from its narration.')
            checked += 1
    if checked != 3:
        raise SystemExit(f'{locale}: expected three narration-synchronized teaching videos, found {checked}.')
    print(f'{locale}: reviewed video hashes and all three narration/cue pairings verified.')


if __name__ == '__main__':
    main()

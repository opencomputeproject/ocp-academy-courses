#!/usr/bin/env python3
"""Encode default MP3 narration delivery; preserve WAV masters and overrides."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import wave
from audio_delivery_defaults import apply_delivery_defaults


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(course_file, ffmpeg=None, report_path=None, migration_choice=None):
    course_file = Path(course_file).resolve()
    course = json.loads(course_file.read_text(encoding='utf-8'))
    if apply_delivery_defaults(course, migration_choice):
        course_file.write_text(json.dumps(course, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    config = (course.get('narration') or {}).get('delivery') or {}
    selected = [s for m in course.get('modules', []) for s in m.get('slides', [])
                if (s.get('audio') or {}).get('delivery_file')
                and s.get('narration_enabled', True)
                and (s.get('figure') or {}).get('role') != 'original_video']
    if not selected:
        return {'clips': [], 'status': 'WAV delivery unchanged'}
    if config.get('format') != 'mp3' or config.get('approved') is not True:
        raise ValueError('MP3 delivery requires approved narration.delivery metadata')
    rate = config.get('sample_rate_hz', 44100)
    bitrate = config.get('bitrate_kbps', 96)
    if rate != 44100 or bitrate not in (32, 64, 96, 128, 192) or config.get('channels', 1) != 1 or config.get('bitrate_mode', 'CBR') != 'CBR':
        raise ValueError('Supported delivery: 44.1 kHz mono CBR MP3, 32/64/96/128/192 kbps')
    binary = ffmpeg or os.environ.get('FFMPEG_BIN') or shutil.which('ffmpeg')
    if not binary:
        raise ValueError('MP3 delivery needs ffmpeg; set FFMPEG_BIN or use --ffmpeg')
    root = course_file.parent

    def local(value):
        rel = Path(value)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Narration paths must be course-relative')
        result = (root / rel).resolve()
        result.relative_to(root)
        return result

    def run(args):
        p = subprocess.run([str(binary), '-nostdin', '-v', 'error', *args], capture_output=True)
        if p.returncode:
            raise ValueError(p.stderr.decode(errors='replace'))
        return p.stdout

    clips = []
    for slide in selected:
        audio = slide['audio']
        master = local(audio['wav_file'])
        target = local(audio['delivery_file'])
        if master.suffix.lower() != '.wav' or target.suffix.lower() != '.mp3':
            raise ValueError('Keep wav_file as WAV and delivery_file as MP3')
        master_hash = sha(master)
        with wave.open(str(master)) as w:
            frames, source_rate = w.getnframes(), w.getframerate()
        target.parent.mkdir(parents=True, exist_ok=True)
        handle = tempfile.NamedTemporaryFile(dir=target.parent, suffix='.mp3', delete=False)
        temporary = Path(handle.name)
        handle.close()
        try:
            run(['-y', '-i', str(master), '-map_metadata', '-1', '-ar', str(rate),
                 '-ac', '1', '-c:a', 'libmp3lame', '-b:a', str(bitrate)+'k',
                 '-write_xing', '1', str(temporary)])
            decoded = run(['-i', str(temporary), '-ar', str(source_rate), '-ac', '1',
                           '-f', 'f32le', 'pipe:1'])
            difference = abs(len(decoded)/4 - frames)/source_rate
            if difference > .005:
                raise ValueError('Decoded duration differs by over 5 ms: '+str(target))
            if sha(master) != master_hash:
                raise ValueError('WAV master changed during delivery encode')
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
        clips.append({'master': audio['wav_file'], 'delivery': audio['delivery_file'],
                      'master_sha256': master_hash, 'delivery_sha256': sha(target),
                      'master_bytes': master.stat().st_size, 'delivery_bytes': target.stat().st_size,
                      'decoded_duration_difference_ms': difference*1000})
    report = {'status': 'encoded', 'settings': config, 'api_calls': 0, 'clips': clips}
    if report_path:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('course_json', type=Path)
    p.add_argument('--ffmpeg')
    p.add_argument('--report', type=Path, help='Authoring receipt outside the runtime manifest')
    p.add_argument('--audio-delivery-choice', choices=['mp3', 'keep-wav'],
                   help='Explicit user decision for a legacy WAV course')
    args = p.parse_args()
    try:
        report = encode(args.course_json, args.ffmpeg, args.report, args.audio_delivery_choice)
    except (OSError, ValueError, wave.Error) as error:
        p.exit(1, 'Audio delivery error: '+str(error)+'\n')
    print(report['status']+': '+str(len(report['clips']))+' MP3 delivery clips; no TTS calls')


if __name__ == '__main__':
    main()

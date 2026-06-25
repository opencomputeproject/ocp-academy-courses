#!/usr/bin/env python3
"""
audio_tail_report.py - scan generated narration WAV files for likely tail issues.

Usage:
    python audio_tail_report.py course.json [--module N] [--fail-on-flags]

The report is intentionally conservative. It flags clips whose last 15 seconds
are much quieter than the body, and clips that contain a short non-silent burst
after a quiet gap near the end. Listen to flagged clips before editing.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import struct
import sys
import wave
from pathlib import Path


def read_wav_mono(path: Path) -> tuple[int, list[float]]:
    with wave.open(str(path), "rb") as w:
        channels = w.getnchannels()
        sampwidth = w.getsampwidth()
        rate = w.getframerate()
        frames = w.getnframes()
        raw = w.readframes(frames)
    if sampwidth != 2:
        raise ValueError(f"{path}: expected 16-bit PCM WAV, got sample width {sampwidth}")
    values = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    if channels > 1:
        mono = [
            sum(values[i : i + channels]) / channels
            for i in range(0, len(values), channels)
        ]
    else:
        mono = list(values)
    return rate, mono


def rms_db(samples: list[float]) -> float:
    if not samples:
        return -120.0
    rms = math.sqrt(sum(x * x for x in samples) / len(samples))
    return 20 * math.log10(rms / 32768) if rms > 0 else -120.0


def window_levels(samples: list[float], rate: int, seconds: float) -> list[tuple[float, float, float]]:
    win = max(1, int(rate * seconds))
    levels = []
    for start in range(0, len(samples), win):
        end = min(len(samples), start + win)
        levels.append((start / rate, end / rate, rms_db(samples[start:end])))
    return levels


def analyze(path: Path) -> dict:
    rate, samples = read_wav_mono(path)
    duration = len(samples) / rate
    five_sec = window_levels(samples, rate, 5.0)
    body_levels = [db for start, end, db in five_sec if end <= max(duration - 15, duration * 0.75)]
    tail_levels = [db for start, end, db in five_sec if start >= max(0, duration - 15)]
    body_ref = statistics.median(body_levels) if body_levels else statistics.median(db for _, _, db in five_sec)
    audible_tail = [db for db in tail_levels if db > -55]
    tail_ref = statistics.mean(audible_tail) if audible_tail else (tail_levels[-1] if tail_levels else -120.0)
    fade_db = body_ref - tail_ref

    burst_after_gap = False
    tail_start_seconds = max(0, duration - 2)
    small = window_levels(samples[int(tail_start_seconds * rate) :], rate, 0.025)
    audible = [i for i, (_, _, db) in enumerate(small) if db > -45]
    if audible:
        groups: list[tuple[int, int]] = []
        start = prev = audible[0]
        for idx in audible[1:]:
            if idx == prev + 1:
                prev = idx
            else:
                groups.append((start, prev))
                start = prev = idx
        groups.append((start, prev))
        for start_i, end_i in groups:
            group_start = tail_start_seconds + small[start_i][0]
            group_end = tail_start_seconds + small[end_i][1]
            group_len = group_end - group_start
            quiet_before = start_i >= 8 and all(small[j][2] < -70 for j in range(start_i - 8, start_i))
            quiet_after = end_i <= len(small) - 3 and all(small[j][2] < -70 for j in range(end_i + 1, min(len(small), end_i + 4)))
            near_file_end = group_start >= duration - 0.75
            if near_file_end and quiet_before and quiet_after and group_len <= 0.20:
                burst_after_gap = True
                break

    flags = []
    if duration >= 35 and fade_db >= 5.0 and tail_ref < -30:
        flags.append(f"tail fade ({fade_db:.1f} dB lower than body)")
    if burst_after_gap:
        flags.append("non-silent burst after quiet gap")

    return {
        "duration": duration,
        "body_db": body_ref,
        "tail_db": tail_ref,
        "fade_db": fade_db,
        "flags": flags,
    }


def iter_audio(course: dict, root: Path, module_filter: int | None):
    for mod in course.get("modules", []):
        if module_filter and mod.get("id") != module_filter:
            continue
        for slide in mod.get("slides", []):
            wav = (slide.get("audio") or {}).get("wav_file")
            if not wav:
                continue
            path = root / wav
            yield mod.get("id"), slide.get("id"), wav, path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_json", type=Path)
    parser.add_argument("--module", type=int)
    parser.add_argument("--fail-on-flags", action="store_true")
    args = parser.parse_args()

    course_json = args.course_json.resolve()
    root = course_json.parent
    course = json.loads(course_json.read_text(encoding="utf-8"))

    flagged = 0
    checked = 0
    for mod_id, slide_id, wav, path in iter_audio(course, root, args.module):
        checked += 1
        if not path.exists():
            print(f"MISS M{mod_id}S{slide_id}: {wav}")
            flagged += 1
            continue
        try:
            result = analyze(path)
        except Exception as exc:
            print(f"ERROR M{mod_id}S{slide_id}: {wav}: {exc}")
            flagged += 1
            continue
        flag_text = "; ".join(result["flags"]) if result["flags"] else "ok"
        if result["flags"]:
            flagged += 1
        print(
            f"M{mod_id}S{slide_id} {wav}: {result['duration']:.1f}s, "
            f"body {result['body_db']:.1f} dBFS, tail {result['tail_db']:.1f} dBFS - {flag_text}"
        )

    print(f"\nchecked: {checked}; flagged: {flagged}")
    return 1 if flagged and args.fail_on_flags else 0


if __name__ == "__main__":
    sys.exit(main())

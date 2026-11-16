#!/usr/bin/env python3
"""
audio_tail_report.py - scan generated narration WAV files for likely level and tail issues.

Usage:
    python audio_tail_report.py course.json [--module N] [--fail-on-flags]

The report flags sustained volume drops that
begin anywhere in the latter half of a clip, clips whose last 15 seconds are
much quieter than the body, and clips that contain a short non-silent burst
after a quiet gap near the end. Speech-active frames are also compared with the
opening so pauses, gradual drift, and absolute-level thresholds cannot hide a
quieter ending. Flags are review prompts, not proof of a synthesis defect.
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


def sustained_drop(
    levels: list[tuple[float, float, float]],
    duration: float,
    body_ref: float,
) -> tuple[float, float] | None:
    """Find a two-window level drop that begins before the conventional tail.

    A long TTS clip can lose projection around 50 seconds and stay quiet without
    making only its final 15 seconds look anomalous. Ignore partial end windows
    and near-silence, then compare two consecutive full windows with the stable
    body reference. The result is an onset time and average drop in dB.
    """
    if duration < 35:
        return None

    full_audible = [
        (start, end, db)
        for start, end, db in levels
        if end - start >= 4.5 and db > -50
    ]
    scan_from = max(20.0, duration * 0.45)
    for index in range(len(full_audible) - 1):
        first = full_audible[index]
        second = full_audible[index + 1]
        if first[0] < scan_from:
            continue
        if second[0] - first[1] > 0.5:
            continue
        pair_levels = [first[2], second[2]]
        average_drop = body_ref - statistics.mean(pair_levels)
        if average_drop >= 5.0 and all(body_ref - db >= 4.5 for db in pair_levels):
            return first[0], average_drop
    return None


def energy_db(levels: list[float]) -> float | None:
    """Mean frame energy in dBFS, rather than the mean of logarithmic levels."""
    if not levels:
        return None
    return 10 * math.log10(statistics.fmean(10 ** (db / 10) for db in levels))


def spoken_level_report(samples: list[float], rate: int) -> dict:
    """Compare likely speech frames with the opening, independently of pauses.

    This is an energy gate, not a linguistic speech recognizer. Use one fixed
    gate for the whole clip so quieter words are not selectively discarded.
    Exclude silence after the last active frame from the final-section bounds.
    Require enough active audio before drawing a level comparison.
    """
    frames = [x for x in window_levels(samples, rate, 0.05) if x[1] - x[0] >= 0.025]
    ordered = sorted(db for _, _, db in frames)
    gate = max(-50.0, ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))] - 25.0) if ordered else -50.0
    active = [(start, end, db) for start, end, db in frames if db > gate]
    result = {
        "speech_gate_db": gate, "spoken_head_db": None, "spoken_tail_db": None,
        "spoken_fade_db": None, "spoken_drop_onset_seconds": None,
        "spoken_sustained_drop_db": None, "spoken_head_active_seconds": 0.0,
        "spoken_tail_active_seconds": 0.0,
    }
    if not active:
        return result
    start, finish = active[0][0], active[-1][1]
    head = [x for x in active if x[0] < start + 15.0]
    tail = [x for x in active if x[1] > finish - 15.0]
    for name, group in (("head", head), ("tail", tail)):
        result[f"spoken_{name}_active_seconds"] = sum(end - begin for begin, end, _ in group)
        if result[f"spoken_{name}_active_seconds"] >= 2.0:
            result[f"spoken_{name}_db"] = energy_db([db for _, _, db in group])
    head_db, tail_db = result["spoken_head_db"], result["spoken_tail_db"]
    if finish - start < 35.0 or head_db is None or tail_db is None:
        return result
    result["spoken_fade_db"] = head_db - tail_db
    buckets: dict[int, list[tuple[float, float, float]]] = {}
    for frame in active:
        buckets.setdefault(int(frame[0] // 5.0), []).append(frame)
    levels = {}
    for index, group in buckets.items():
        if sum(end - begin for begin, end, _ in group) >= 2.0 and (index + 1) * 5 <= finish + 0.05:
            levels[index] = energy_db([db for _, _, db in group])
    for index, db in sorted(levels.items()):
        following = levels.get(index + 1)
        if index * 5 < max(start + 20.0, finish * 0.45) or following is None:
            continue
        drops = [head_db - db, head_db - following]
        if statistics.fmean(drops) >= 3.5 and min(drops) >= 3.0:
            result["spoken_drop_onset_seconds"] = index * 5.0
            result["spoken_sustained_drop_db"] = statistics.fmean(drops)
            break
    return result


def analyze(path: Path) -> dict:
    rate, samples = read_wav_mono(path)
    duration = len(samples) / rate
    five_sec = window_levels(samples, rate, 5.0)
    body_levels = [db for start, end, db in five_sec if end <= max(duration - 15, duration * 0.75)]
    # Window centers avoid excluding an entire tail window for a few extra samples.
    tail_levels = [db for start, end, db in five_sec if (start + end) / 2 >= max(0, duration - 15)]
    body_ref = statistics.median(body_levels) if body_levels else statistics.median(db for _, _, db in five_sec)
    audible_tail = [db for db in tail_levels if db > -55]
    tail_ref = statistics.mean(audible_tail) if audible_tail else (tail_levels[-1] if tail_levels else -120.0)
    fade_db = body_ref - tail_ref
    volume_drop = sustained_drop(five_sec, duration, body_ref)
    spoken = spoken_level_report(samples, rate)

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
    if volume_drop:
        onset, drop_db = volume_drop
        flags.append(f"sustained volume drop from ~{onset:.0f}s ({drop_db:.1f} dB lower than body)")
    if audible_tail and duration >= 35 and fade_db >= 5.0 and tail_ref < -30:
        flags.append(f"tail fade ({fade_db:.1f} dB lower than body)")
    spoken_fade = spoken["spoken_fade_db"]
    if spoken_fade is not None and spoken_fade >= 2.5:
        severity = "spoken-level decline" if spoken_fade >= 3.0 else "borderline spoken-level decline; review"
        flags.append(f"{severity} ({spoken_fade:.1f} dB lower than opening speech)")
    if spoken["spoken_drop_onset_seconds"] is not None:
        flags.append(
            f"sustained spoken-level drop from ~{spoken['spoken_drop_onset_seconds']:.0f}s "
            f"({spoken['spoken_sustained_drop_db']:.1f} dB lower than opening speech)"
        )
    if burst_after_gap:
        flags.append("non-silent burst after quiet gap")

    return {
        "qa_revision": "speech-level-v2",
        "duration": duration,
        "body_db": body_ref,
        "tail_db": tail_ref,
        "fade_db": fade_db,
        "drop_onset_seconds": volume_drop[0] if volume_drop else None,
        "sustained_drop_db": volume_drop[1] if volume_drop else None,
        **spoken,
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

#!/usr/bin/env python3
"""
course_delivery_summary.py - report final LMS metadata and module durations.

Usage:
    python course_delivery_summary.py course.json [--short-max 130]

Durations are calculated from the actual WAV files referenced by course.json.
"""

from __future__ import annotations

import argparse
import json
import wave
from pathlib import Path


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def clamp_words(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    words = text.split()
    out = ""
    for word in words:
        candidate = f"{out} {word}".strip()
        if len(candidate) > limit - 1:
            break
        out = candidate
    return out.rstrip(" .,;:") + "."


def module_audio_seconds(root: Path, module: dict) -> float:
    total = 0.0
    for slide in module.get("slides", []):
        wav = (slide.get("audio") or {}).get("wav_file")
        if wav and (root / wav).exists():
            total += wav_duration(root / wav)
    return total


def summary_sentence(module: dict) -> str:
    subtitle = module.get("subtitle") or ""
    if subtitle:
        return subtitle.rstrip(".") + "."
    titles = [
        slide.get("title")
        for slide in module.get("slides", [])
        if slide.get("type", "").startswith("content") and slide.get("title")
    ]
    if titles:
        return "Covers " + ", ".join(titles[:4]).rstrip(".") + "."
    return "Covers the module's core learning objectives."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_json", type=Path)
    parser.add_argument("--short-max", type=int, default=130)
    args = parser.parse_args()

    course_json = args.course_json.resolve()
    root = course_json.parent
    course = json.loads(course_json.read_text(encoding="utf-8"))

    title = course.get("course_title") or course.get("title") or course_json.stem
    subtitle = course.get("course_subtitle") or ""
    short = clamp_words(subtitle or f"Learn the essentials of {title}.", args.short_max)

    module_rows = []
    total_seconds = 0.0
    if str(course.get("style") or "Slides").strip().casefold() == "scrolling":
        print("TITLE")
        print(title)
        print()
        print(f"SHORT DESCRIPTION ({len(short)} chars)")
        print(short)
        print()
        print("LONG DESCRIPTION")
        print((subtitle or f"This OCP Academy course introduces {title}.").rstrip(".") + ".")
        print()
        print(f"Scrolling course: {len(course.get('lessons', []))} lessons; no narration by default.")
        for lesson in course.get("lessons", []):
            print(f"Lesson {lesson.get('id')}: {lesson.get('title')}")
        return 0
    for module in course.get("modules", []):
        seconds = module_audio_seconds(root, module)
        total_seconds += seconds
        module_rows.append((module, seconds))

    print("TITLE")
    print(title)
    print()
    print(f"SHORT DESCRIPTION ({len(short)} chars)")
    print(short)
    print()
    print("LONG DESCRIPTION")
    overview = subtitle or f"This OCP Academy course introduces {title}."
    print(overview.rstrip(".") + ".")
    print()
    print(
        f"Total narrated runtime: {total_seconds / 60:.1f} minutes. "
        "Allow additional time for knowledge checks, review, and learner interaction."
    )
    print()
    for module, seconds in module_rows:
        minutes = round(seconds / 60)
        print(f"Module {module.get('id')}: {module.get('title')} ({minutes} min narrated)")
        print(summary_sentence(module))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

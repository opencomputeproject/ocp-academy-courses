#!/usr/bin/env python3
"""Scaffold a lightweight locale source for an existing Scrolling course."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


LANGUAGE_NAMES = {
    "ar": "Arabic",
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "sv": "Swedish",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
    "zh": "Chinese",
    "zh-cn": "Simplified Chinese",
    "zh-hans": "Simplified Chinese",
    "zh-sg": "Simplified Chinese",
    "zh-hant": "Traditional Chinese",
    "zh-hk": "Traditional Chinese",
    "zh-tw": "Traditional Chinese",
}


def language_name(locale: str) -> str:
    return LANGUAGE_NAMES.get(locale.casefold(), LANGUAGE_NAMES.get(locale.split("-")[0].casefold(), locale))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("course_dir", type=Path, help="Canonical Scrolling course folder")
    parser.add_argument("locale", help="BCP 47 language tag, such as ko-KR")
    parser.add_argument("--force", action="store_true", help="Replace an existing locale course.json")
    args = parser.parse_args()

    source_path = args.course_dir.resolve() / "course.json"
    if not source_path.is_file():
        raise SystemExit(f"Canonical course.json not found: {source_path}")
    raw = source_path.read_bytes()
    course = json.loads(raw)
    if str(course.get("style") or "Slides").casefold() != "scrolling":
        raise SystemExit("scaffold_scrolling_translation.py requires a Scrolling course")

    locale_dir = source_path.parent / "locales" / args.locale
    target_path = locale_dir / "course.json"
    if target_path.exists() and not args.force:
        raise SystemExit(f"Locale already exists: {target_path} (pass --force to replace it)")

    locale_dir.mkdir(parents=True, exist_ok=True)
    for name in ("videos", "captions", "images", "documents"):
        (locale_dir / "resources" / name).mkdir(parents=True, exist_ok=True)

    source_language = str(course.get("language") or "en-US")
    course["language"] = args.locale
    course["metadata_language_name"] = language_name(args.locale)
    course["localization"] = {
        "source_course": "../../course.json",
        "source_language": source_language,
        "target_language": args.locale,
        "source_course_sha256": hashlib.sha256(raw).hexdigest(),
        "resource_mode": "canonical-base-with-locale-overlay",
    }
    target_path.write_text(json.dumps(course, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target_path)


if __name__ == "__main__":
    main()

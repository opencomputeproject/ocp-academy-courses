#!/usr/bin/env python3
"""Create a self-contained locale source branch for a Slides course.

Usage:
    python scaffold_slides_translation.py <source-course.json> <language-tag>
        [--language-name Korean] [--scorm-title "Exact LMS title"]
        [--output-dir /path/to/locales/ko-KR]

The source course is never modified. The new locale starts with the same slide
structure and copied visual assets, but narration folders are empty and every
audio block is reset to approved=false so translated scripts must be reviewed
and synthesized deliberately. Maintained locale narration defaults are written
to top-level course metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path


LANGUAGE_TAG_RE = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")

LOCALE_NARRATION_DEFAULTS = {
    "es-419": {
        "engine": "elevenlabs",
        "voice_id": "zl1Ut8dvwcVSuQSB9XkG",
        "voice_name": "Ninoska",
    },
    "ja": {
        "engine": "elevenlabs",
        "voice_id": "b34JylakFZPlGS0BnwyY",
    },
    "ko": {
        "engine": "elevenlabs",
        "voice_id": "PDoCXqBQFGsvfO0hNkEs",
        "voice_name": "Chris - Warm and clear",
    },
    "pt-BR": {
        "engine": "elevenlabs",
        "voice_id": "m151rjrbWXbBqyq56tly",
        "voice_name": "Carla",
    },
    "vi": {
        "engine": "elevenlabs",
        "voice_id": "A5w1fw5x0uXded1LDvZp",
        "voice_name": "Nhu",
        "model_id": "eleven_flash_v2_5",
    },
    "zh-CN": {
        "engine": "elevenlabs",
        "voice_id": "bZtjnyJAFD0Cp3lfNG5g",
        "voice_name": "Lan Chen",
    },
    "zh-TW": {
        "engine": "elevenlabs",
        "voice_id": "1AKkSX7KMPHIWuz76m0n",
        "voice_name": "Tiffy",
    },
}


def canonical_language_tag(value: str) -> str:
    value = value.strip().replace("_", "-")
    if not LANGUAGE_TAG_RE.fullmatch(value):
        raise ValueError(f"Invalid BCP 47 language tag: {value!r}")
    parts = value.split("-")
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif len(part) in (2, 3) and part.isalnum():
            normalized.append(part.upper())
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def is_slides(course: dict) -> bool:
    return str(course.get("style") or "Slides").strip().casefold() == "slides"


def locale_narration_default(language: str) -> dict | None:
    normalized_language = canonical_language_tag(language)
    primary_language = normalized_language.split("-", 1)[0]
    default = LOCALE_NARRATION_DEFAULTS.get(normalized_language)
    if default is None:
        default = LOCALE_NARRATION_DEFAULTS.get(primary_language)
    return dict(default) if default else None


def copy_tree_if_present(source_root: Path, target_root: Path, name: str) -> None:
    source = source_root / name
    if not source.is_dir():
        return
    shutil.copytree(source, target_root / name)
    print(f"copied {name}/")


def referenced_root_assets(course: dict) -> set[str]:
    assets: set[str] = set()
    brand = course.get("brand") or {}
    for key in ("course_logo", "academy_logo", "motion_intro_logo"):
        value = brand.get(key)
        if isinstance(value, str) and value:
            assets.add(value)

    motion = course.get("motion_intro") or {}
    if isinstance(motion, dict):
        for value in (motion.get("logo"), (motion.get("index") or {}).get("logo")):
            if isinstance(value, str) and value:
                assets.add(value)
        modules = motion.get("modules") or {}
        if isinstance(modules, dict) and isinstance(modules.get("logo"), str):
            assets.add(modules["logo"])

    for module in course.get("modules", []):
        intro = module.get("motion_intro") or {}
        if isinstance(intro, dict) and isinstance(intro.get("logo"), str):
            assets.add(intro["logo"])
    return assets


def copy_root_assets(course: dict, source_root: Path, target_root: Path) -> None:
    for value in sorted(referenced_root_assets(course)):
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            print(f"NOTE: skipped non-local asset path {value!r}")
            continue
        source = source_root / relative
        if not source.is_file():
            print(f"NOTE: referenced asset not found next to source course: {value}")
            continue
        target = target_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        print(f"copied {value}")


def reset_audio_approvals(course: dict, target_root: Path) -> int:
    count = 0
    for module in course.get("modules", []):
        module_id = module.get("id")
        (target_root / "audio" / f"module{module_id}").mkdir(parents=True, exist_ok=True)
        for slide in module.get("slides", []):
            audio = slide.get("audio")
            if not isinstance(audio, dict):
                continue
            audio["approved"] = False
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_course_json", type=Path)
    parser.add_argument("language_tag")
    parser.add_argument("--language-name", help="English LMS label, for example Korean")
    parser.add_argument("--scorm-title", help="Exact manifest-only title override")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    source_json = args.source_course_json.resolve()
    if not source_json.is_file():
        sys.exit(f"Source course.json not found: {source_json}")

    try:
        language = canonical_language_tag(args.language_tag)
    except ValueError as error:
        sys.exit(str(error))

    try:
        course = json.loads(source_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        sys.exit(f"Source course.json does not parse: {error}")
    if not is_slides(course):
        sys.exit("This scaffold supports style=Slides only.")

    source_root = source_json.parent
    target_root = (
        args.output_dir.resolve()
        if args.output_dir
        else source_root / "locales" / language
    )
    if target_root == source_root:
        sys.exit("Output directory must be a separate locale folder.")
    if target_root.exists() and any(target_root.iterdir()):
        sys.exit(f"Refusing to overwrite non-empty locale folder: {target_root}")
    target_root.mkdir(parents=True, exist_ok=True)

    source_language = canonical_language_tag(str(course.get("language") or "en-US"))
    course["style"] = "Slides"
    course["language"] = language
    course.pop("narration", None)
    narration_default = locale_narration_default(language)
    if narration_default:
        course["narration"] = narration_default
    course.pop("scorm_title", None)
    if args.scorm_title:
        course["scorm_title"] = args.scorm_title
    if args.language_name:
        course["metadata_language_name"] = args.language_name
    else:
        course.pop("metadata_language_name", None)

    source_slug = str(course.get("course_slug") or source_root.name)
    locale_slug = re.sub(r"[^a-z0-9]+", "_", language.lower()).strip("_")
    course["course_slug"] = f"{source_slug}_{locale_slug}"
    relative_source = os.path.relpath(source_json, target_root)
    course["localization"] = {
        "source_course": Path(relative_source).as_posix(),
        "source_language": source_language,
        "target_language": language,
        "source_course_sha256": hashlib.sha256(source_json.read_bytes()).hexdigest(),
    }
    course.setdefault("ui_labels", {})

    audio_count = reset_audio_approvals(course, target_root)
    copy_tree_if_present(source_root, target_root, "figures")
    copy_tree_if_present(source_root, target_root, "animations")
    copy_root_assets(course, source_root, target_root)

    target_json = target_root / "course.json"
    target_json.write_text(
        json.dumps(course, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {target_json}")
    print(f"reset {audio_count} narration approval(s)")
    if narration_default:
        voice_label = narration_default.get("voice_name") or f"{language} ElevenLabs voice"
        print(
            "set narration default: "
            f"{voice_label} ({narration_default['voice_id']})"
        )
    print("\nNext steps:")
    print("  1. Translate learner-facing course.json fields and ui_labels.")
    print("  2. Write locale narration scripts under audio/moduleN/.")
    print("  3. Replace or edit every text-bearing figure and animation.")
    print("  4. Review scripts, synthesize audio, render, validate, and zip independently.")


if __name__ == "__main__":
    main()

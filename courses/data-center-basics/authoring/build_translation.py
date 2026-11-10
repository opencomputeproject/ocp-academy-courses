#!/usr/bin/env python3
"""Rebuild a delivered DC Basics locale using its unchanged MP3 narration."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


COURSE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = COURSE_ROOT.parents[1]
LOCALES = ("es-419", "ja-JP", "ko-KR", "pt-BR", "vi-VN", "zh-CN", "zh-TW")


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        digest = hashlib.sha256()
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("locale", choices=LOCALES)
    parser.add_argument("--audio-dir", type=Path, required=True,
                        help="Extracted delivery audio containing module1/ through module4/")
    parser.add_argument("--output", type=Path, help="An empty directory outside course source")
    parser.add_argument("--zip", action="store_true", help="Also create the strict LMS ZIP")
    args = parser.parse_args()

    source = COURSE_ROOT / "locales" / args.locale
    course_path = source / "course.json"
    course = json.loads(course_path.read_text(encoding="utf-8"))
    audio_manifest = json.loads((source / "authoring/delivery-audio.json").read_text())
    if audio_manifest["course_sha256"] != sha256(course_path):
        parser.error("Course source changed since delivery; review media and audio before releasing it.")

    audio_root = args.audio_dir.resolve()
    expected = {
        slide["audio"]["delivery_file"]
        for module in course["modules"] for slide in module["slides"]
        if slide.get("audio")
    }
    clips = audio_manifest["clips"]
    if len(clips) != 68 or {clip["path"] for clip in clips} != expected:
        parser.error("Delivery audio inventory does not match the 68 narrated slides.")
    audio_files = []
    for clip in clips:
        relative = Path(clip["path"])
        if relative.is_absolute() or ".." in relative.parts or relative.parts[0] != "audio":
            parser.error(f"Invalid audio path: {relative}")
        audio_file = audio_root / Path(*relative.parts[1:])
        if not audio_file.is_file() or sha256(audio_file) != clip["sha256"]:
            parser.error(f"Missing or changed delivered MP3: {audio_file}")
        audio_files.append((audio_file, relative))

    output = (args.output or REPO_ROOT / "build/data-center-basics" / args.locale).resolve()
    if output == COURSE_ROOT or COURSE_ROOT in output.parents:
        parser.error("Build output must stay outside the editable course source.")
    if output.exists() and any(output.iterdir()):
        parser.error("Choose an empty output directory to avoid mixing release files.")

    tool = source / course["authoring_toolchain"] / "scripts"

    def run(script: str, *arguments: object) -> None:
        subprocess.run([sys.executable, str(tool / script), *map(str, arguments)], check=True)

    run("course_delivery_summary.py", course_path, "--check")
    run("slides_course_qa.py", course_path, "--repo-root", REPO_ROOT, "--fail-on-flags")
    run("check_svg_arrows.py", course_path, "--fail-on-flags")
    run("new_course.py", output, course_path)
    for folder in ("assets", "resources", "figures"):
        shutil.copytree(source / folder, output / folder, dirs_exist_ok=True)
    for schema in source.glob("*.xsd"):
        shutil.copy2(schema, output / schema.name)
    for audio_file, relative in audio_files:
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(audio_file, target)

    run("render_module.py", output / "course.json", "--all")
    run("render_index.py", output / "course.json")
    run("validate_package.py", output)
    if args.zip:
        run("zip_for_lms.py", output, "--course-json", course_path)

    print(f"Validated {args.locale}: {output}")
    print("Reused 68 verified MP3s; no TTS, audio encoding, or video encoding performed.")


if __name__ == "__main__":
    main()

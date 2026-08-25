#!/usr/bin/env python3
"""Report source-level quality gates for a newly authored Slides course.

Usage:
    python slides_course_qa.py course.json --fail-on-flags
    python slides_course_qa.py course.json --repo-root /path/to/repo --fail-on-flags
    python slides_course_qa.py course.json --allow-missing-module-video 3 --fail-on-flags

This complements, rather than replaces, rendered visual inspection. It verifies
per-module teaching-video coverage, local media/poster files, glossary-reference
integrity, and (when requested) the course README, 800x400 thumbnail, and both
root README catalog locations.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path


VIDEO_SUFFIXES = {".mp4", ".webm", ".mov", ".m4v"}


def is_video(figure: dict) -> bool:
    path = str(figure.get("path") or "")
    return str(figure.get("media_type") or "").casefold() == "video" or Path(path).suffix.casefold() in VIDEO_SUFFIXES


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("not a PNG with a readable IHDR header")
    return struct.unpack(">II", header[16:24])


def section(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    start = markdown.find(marker)
    if start < 0:
        return ""
    start += len(marker)
    end = markdown.find("\n## ", start)
    return markdown[start:] if end < 0 else markdown[start:end]


def check_course(
    course_json: Path,
    repo_root: Path | None,
    allowed_video_opt_outs: set[int],
) -> tuple[list[str], list[str]]:
    root = course_json.parent
    course = json.loads(course_json.read_text(encoding="utf-8"))
    errors: list[str] = []
    notes: list[str] = []

    if str(course.get("style") or "Slides").casefold() != "slides":
        return ["course style is not Slides"], notes

    glossary = course.get("term_glossary") or []
    glossary_ids = {item.get("id") for item in glossary if isinstance(item, dict) and item.get("id")}
    used_glossary: set[str] = set()

    modules = course.get("modules") or []
    if not modules:
        errors.append("course has no modules")

    for module in modules:
        module_id = module.get("id")
        videos: list[tuple[dict, dict]] = []
        refs_by_term: dict[str, list[object]] = defaultdict(list)
        for slide in module.get("slides") or []:
            figure = slide.get("figure") or {}
            if figure:
                media_path = str(figure.get("path") or "")
                if not media_path:
                    errors.append(f"M{module_id}S{slide.get('id')}: figure has no path")
                elif not (root / media_path).is_file():
                    errors.append(f"M{module_id}S{slide.get('id')}: missing media {media_path}")
                if is_video(figure):
                    videos.append((slide, figure))
                    poster = str(figure.get("poster") or "")
                    if not poster:
                        errors.append(f"M{module_id}S{slide.get('id')}: video has no poster")
                    elif not (root / poster).is_file():
                        errors.append(f"M{module_id}S{slide.get('id')}: missing poster {poster}")
                    for field in ("autoplay", "loop", "muted"):
                        if figure.get(field) is not True:
                            errors.append(f"M{module_id}S{slide.get('id')}: teaching video must set {field}=true")
                    if not str(figure.get("alt") or "").strip():
                        errors.append(f"M{module_id}S{slide.get('id')}: video has no alt text")
                    if not str(figure.get("caption") or "").strip():
                        errors.append(f"M{module_id}S{slide.get('id')}: video has no teaching caption")

            for term_id in slide.get("term_refs") or []:
                refs_by_term[str(term_id)].append(slide.get("id"))
                used_glossary.add(str(term_id))
                if term_id not in glossary_ids:
                    errors.append(f"M{module_id}S{slide.get('id')}: unknown glossary id {term_id!r}")

        if not videos and module_id in allowed_video_opt_outs:
            notes.append(f"M{module_id}: teaching-video requirement explicitly waived")
        elif not videos:
            errors.append(f"M{module_id}: no teaching video; obtain an explicit user opt-out before delivery")
        else:
            notes.append(f"M{module_id}: {len(videos)} teaching video(s)")

        for term_id, slide_ids in refs_by_term.items():
            if len(slide_ids) > 1:
                errors.append(f"M{module_id}: glossary term {term_id!r} is attached to multiple slides {slide_ids}")

    unused = sorted(str(term_id) for term_id in glossary_ids - used_glossary)
    if unused:
        errors.append("glossary entries never attached to a slide: " + ", ".join(unused))

    if repo_root is not None:
        repo_root = repo_root.resolve()
        courses_root = repo_root / "courses"
        try:
            folder = root.resolve().relative_to(courses_root).as_posix()
        except ValueError:
            errors.append(f"course folder is not beneath {courses_root}")
            folder = root.name

        local_readme = root / "README.md"
        if not local_readme.is_file():
            errors.append("course-local README.md is missing")
        elif str(course.get("course_title") or "") not in local_readme.read_text(encoding="utf-8"):
            errors.append("course-local README.md does not contain course_title")

        thumbnail = root / "thumbnail.png"
        if not thumbnail.is_file():
            errors.append("thumbnail.png is missing")
        else:
            try:
                dimensions = png_size(thumbnail)
                if dimensions != (800, 400):
                    errors.append(f"thumbnail.png is {dimensions[0]}x{dimensions[1]}, expected 800x400")
            except Exception as exc:
                errors.append(f"thumbnail.png: {exc}")

        root_readme = repo_root / "README.md"
        if not root_readme.is_file():
            errors.append("root README.md is missing")
        else:
            markdown = root_readme.read_text(encoding="utf-8")
            layout = section(markdown, "Repository layout")
            available = section(markdown, "Available Courses")
            if folder not in layout:
                errors.append(f"root README Repository layout is missing {folder}")
            if f"`{folder}`" not in available:
                errors.append(f"root README Available Courses table is missing {folder}")

    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_json", type=Path)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument(
        "--allow-missing-module-video",
        type=int,
        action="append",
        default=[],
        metavar="N",
        help="record an explicit user opt-out for module N; repeat for multiple modules",
    )
    parser.add_argument("--fail-on-flags", action="store_true")
    args = parser.parse_args()

    course_json = args.course_json.resolve()
    errors, notes = check_course(course_json, args.repo_root, set(args.allow_missing_module_video))
    for note in notes:
        print(f"OK: {note}")
    for error in errors:
        print(f"FLAG: {error}")
    print(f"\nchecked: {course_json}; flagged: {len(errors)}")
    return 1 if errors and args.fail_on_flags else 0


if __name__ == "__main__":
    sys.exit(main())

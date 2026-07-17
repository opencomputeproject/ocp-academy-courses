#!/usr/bin/env python3
"""
validate_package.py — sanity-check a finished SCORM folder before delivery.

Usage:
    python validate_package.py <folder>

Checks:
  - imsmanifest.xml exists and parses as XML
  - index.html exists
  - For each <resource>: every <file href="..."/> resolves to a real file
  - For each moduleN.html: every audioMap path resolves on disk
  - Each moduleN.html has slide IDs 1..N contiguously
  - No file in the folder is larger than 50 MB (likely a mistake)
  - Brand logos and scorm_api.js are present

Exits 0 on clean validation, 1 with a list of failures otherwise.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from render_scrolling import parse_webvtt


def _is_scrolling(course: dict) -> bool:
    return str(course.get("style") or "Slides").strip().casefold() == "scrolling"


def _resource_paths(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for item in value.values():
            found.update(_resource_paths(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_resource_paths(item))
    elif isinstance(value, str) and value.startswith("resources/"):
        found.add(value)
    return found


def _scrolling_block_types(course: dict) -> set[str]:
    return {
        str(block.get("type") or "").strip().casefold()
        for lesson in course.get("lessons", [])
        for block in lesson.get("blocks", [])
        if isinstance(block, dict)
    }


def _scrolling_has_quote_avatar(course: dict) -> bool:
    return any(
        block.get("type") == "quote" and bool(block.get("avatar"))
        for lesson in course.get("lessons", [])
        for block in lesson.get("blocks", [])
        if isinstance(block, dict)
    )


def _scrolling_caption_tracks(course: dict) -> list[dict]:
    tracks: list[dict] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            captions = value.get("captions")
            if isinstance(captions, list):
                tracks.extend(track for track in captions if isinstance(track, dict))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(course)
    return tracks


def _dark_hex_color(value: object) -> bool:
    text = str(value or "").lstrip("#")
    if len(text) == 3:
        text = "".join(char * 2 for char in text)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", text):
        return False
    red, green, blue = (int(text[index:index + 2], 16) for index in (0, 2, 4))
    return (0.299 * red + 0.587 * green + 0.114 * blue) / 255 <= 0.58


def main():
    p = argparse.ArgumentParser()
    p.add_argument("folder", type=Path)
    args = p.parse_args()
    root = args.folder.resolve()
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    errors: list[str] = []
    warnings: list[str] = []

    def err(m): errors.append(m)
    def warn(m): warnings.append(m)

    manifest = root / "imsmanifest.xml"
    index = root / "index.html"
    api = root / "scorm_api.js"
    course_json = root / "course.json"
    course = {}
    if course_json.exists():
        try:
            course = json.loads(course_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"course.json does not parse: {e}")

    if not manifest.exists():
        err("imsmanifest.xml is missing")
    if not index.exists():
        err("index.html is missing")
    if not api.exists():
        err("scorm_api.js is missing")

    if manifest.exists():
        try:
            tree = ET.parse(manifest)
            ns = {"ims": "http://www.imsproject.org/xsd/imscp_rootv1p1p2",
                  "adl": "http://www.adlnet.org/xsd/adlcp_rootv1p2"}
            for res in tree.getroot().iter("{http://www.imsproject.org/xsd/imscp_rootv1p1p2}resource"):
                for f in res.findall("{http://www.imsproject.org/xsd/imscp_rootv1p1p2}file"):
                    href = f.get("href")
                    if href and not (root / href).exists():
                        err(f"manifest references missing file: {href}")
        except ET.ParseError as e:
            err(f"imsmanifest.xml does not parse: {e}")

    for module_file in sorted(root.glob("module*.html")):
        html = module_file.read_text(errors="replace")
        slide_ids = [int(m.group(1)) for m in re.finditer(r'data-slide="(\d+)"', html)]
        if not slide_ids:
            err(f"{module_file.name}: no data-slide markers")
        else:
            expected = list(range(1, max(slide_ids) + 1))
            if sorted(slide_ids) != expected:
                err(f"{module_file.name}: slide IDs not contiguous 1..{max(slide_ids)} — got {sorted(slide_ids)}")
        # audioMap audit
        m = re.search(r"const audioMap\s*=\s*\{([^}]*)\}", html, re.S)
        if m:
            for entry in re.finditer(r'(\d+):\s*"([^"]+)"', m.group(1)):
                audio_rel = entry.group(2)
                if not (root / audio_rel).exists():
                    err(f"{module_file.name}: audioMap references missing audio: {audio_rel}")

    if course and _is_scrolling(course):
        index_html = index.read_text(errors="replace") if index.exists() else ""
        lesson_ids = [int(match.group(1)) for match in re.finditer(r'data-lesson-id="(\d+)"', index_html)]
        expected = list(range(1, len(course.get("lessons", [])) + 1))
        if lesson_ids != expected:
            err(f"index.html: Scrolling lesson IDs do not match course.json — expected {expected}, got {lesson_ids}")
        if list(root.glob("module*.html")):
            err("Scrolling packages must be a single SCO and must not contain moduleN.html files")
        for resource in sorted(_resource_paths(course)):
            if not (root / resource).exists():
                err(f"course.json references missing resource: {resource}")
        if re.search(r"\son[a-z]+\s*=", index_html, flags=re.I):
            err("index.html contains an inline JavaScript event handler")

        required_runtime = {
            "cover-first entry": 'class="course-cover"',
            "lesson table of contents": 'class="lesson-nav"',
            "previous-lesson strip": 'class="previous-lesson-nav"',
            "inline lesson progress": "lesson-read-progress--inline",
            "sticky lesson progress": 'id="lesson-read-progress-sticky"',
            "completed-lesson next bar": "data-next-lesson",
            "next-lesson upward transition": "lesson--enter-next",
            "previous-lesson downward transition": "lesson--enter-previous",
            "viewport entrance animation": "IntersectionObserver",
            "maintained inset TOC shadow": "box-shadow: inset -15px 0 25px -20px #00000050;",
        }
        scrolling = course.get("scrolling") or {}
        if scrolling.get("show_cover_lesson_list", True):
            required_runtime["cover lesson list"] = 'class="course-cover__lesson-list"'
        if scrolling.get("show_search", True):
            required_runtime["full-course search results"] = 'class="sidebar-search-results"'
        for label, marker in required_runtime.items():
            if marker not in index_html:
                err(f"index.html: Scrolling runtime is missing {label} ({marker})")

        block_types = _scrolling_block_types(course)
        interaction_requirements = {
            "video": (
                "data-video-player",
                "academy-video__big-play",
                "data-video-progress",
                'data-video-menu="rate"',
                'data-video-rate="0.5"',
                'data-video-rate="2"',
                'data-video-action="picture-in-picture"',
                "data-video-volume",
                "M1419 971H821V523H1419",
            ),
            "accordion": ("interactive-card__toggler", "interactive-card__plus", "interactive-card__minus"),
            "tabs": ("data-tab-panel", "tab-button"),
            "process": ("data-process-slide", "process-controls__previous", "process-controls__next"),
            "flashcards": ("flashcard__description-inner", "transform: scale(.9) translateZ(0);", "flashcard.is-flipped"),
            "knowledge_check": (
                "quiz-choice__indicator",
                "quiz-feedback__glyph",
                "quiz-retake__icon",
                '.quiz-question [style*="font-size"]',
                "border-top: 1px solid #8f8f8f;",
            ),
            "labeled_graphic": (
                "data-labeled-graphic",
                "data-labeled-marker",
                "data-labeled-callout",
                'data-labeled-action="previous"',
                "labeled-graphic__plus",
            ),
            "attachment": (
                "attachment-card",
                "attachment-card__file-icon",
                "attachment-card__size",
                "attachment-card__download-icon",
            ),
        }
        for block_type, markers in interaction_requirements.items():
            if block_type not in block_types:
                continue
            for marker in markers:
                if marker not in index_html:
                    err(f"index.html: {block_type} rendering is missing {marker}")
        caption_tracks = _scrolling_caption_tracks(course)
        if caption_tracks:
            for marker in (
                "academy-video__caption-display",
                "academy-video__caption-data",
                'data-video-menu="captions"',
                "Captions off",
                "M1419 1493H373",
            ):
                if marker not in index_html:
                    err(f"index.html: captioned video rendering is missing {marker}")
            rendered_caption_tracks: list[dict] = []
            for payload_text in re.findall(
                r'<script class="academy-video__caption-data" type="application/json">(.*?)</script>',
                index_html,
                flags=re.S,
            ):
                try:
                    payload = json.loads(payload_text)
                    rendered_caption_tracks.extend(
                        track for track in payload.get("tracks", []) if isinstance(track, dict)
                    )
                except json.JSONDecodeError as exc:
                    err(f"index.html: embedded caption data does not parse: {exc}")
            for track in caption_tracks:
                path = str(track.get("path") or "")
                label = str(track.get("label") or "")
                language = str(track.get("language") or "")
                if not path or not label or not language:
                    err(f"course.json: caption track requires path, label, and language: {track}")
                    continue
                source = root / path
                if source.exists():
                    try:
                        source_cues = parse_webvtt(source.read_text(encoding="utf-8-sig"))
                    except (OSError, UnicodeError):
                        source_cues = []
                    if not source_cues:
                        err(f"course.json: caption track is not valid cue-bearing WebVTT: {path}")
                rendered = next((item for item in rendered_caption_tracks if item.get("path") == path), None)
                if not rendered:
                    err(f"index.html: caption track is not embedded for local playback: {path}")
                elif not rendered.get("cues"):
                    err(f"index.html: caption track has no embedded local-playback cues: {path}")
        for lesson in course.get("lessons", []):
            for block in lesson.get("blocks", []):
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "process":
                    items = [item for item in block.get("items", []) if isinstance(item, dict) and not item.get("hidden")]
                    roles = [str(item.get("type") or "step").casefold() for item in items]
                    if "intro" in roles and roles[0] != "intro":
                        err("course.json: process intro must be first in learner-facing order")
                    if "summary" in roles and roles[-1] != "summary":
                        err("course.json: process summary must be last in learner-facing order")
                    if "intro" in roles and "process-step--intro" not in index_html:
                        err("index.html: process intro card/action is missing")
                    if "summary" in roles and "process-step--summary" not in index_html:
                        err("index.html: process summary card/action is missing")
                    style = block.get("style") if isinstance(block.get("style"), dict) else {}
                    if _dark_hex_color(style.get("background_color")) and "process-carousel--controls-light" not in index_html:
                        err("index.html: dark process block is missing light carousel controls")
                    corner_style = str((course.get("theme") or {}).get("corner_style") or "Rounded").casefold()
                    expected_radius = "10px" if "round" in corner_style else "0px"
                    if "border-radius: var(--process-step-badge-radius, 10px);" not in index_html:
                        err("index.html: process Step badge is missing the maintained theme-driven corner rule")
                    if f"--process-step-badge-radius:{expected_radius}" not in index_html:
                        err(f"index.html: process Step badge radius does not match theme.corner_style ({expected_radius})")
                if block.get("type") == "labeled_graphic":
                    style = block.get("style") if isinstance(block.get("style"), dict) else {}
                    width_variant = str(style.get("media_width_variant") or "").casefold()
                    if width_variant in {"medium", "full"} and f"labeled-graphic--{width_variant}" not in index_html:
                        err(f"index.html: labeled graphic is missing its {width_variant} width variant")
                style = block.get("style") if isinstance(block.get("style"), dict) else {}
                background_media = style.get("background_media") if isinstance(style.get("background_media"), dict) else {}
                if background_media.get("path") and style.get("background_overlay_opacity") is not None:
                    required = {
                        "background-image block class": "block--background-image",
                        "separate background overlay layer": "linear-gradient(",
                    }
                    for label, marker in required.items():
                        if marker not in index_html:
                            err(f"index.html: image-background rendering is missing {label} ({marker})")
                if block.get("type") == "buttons" and str(style.get("button_alignment") or "").casefold() == "left":
                    if "block--button-left" not in index_html:
                        err("index.html: left-aligned button block is missing its alignment class")
                    if 'resource-button-row--action-left"><div class="resource-button-action"' not in index_html:
                        err("index.html: left-aligned button action does not precede its description")
        if _scrolling_has_quote_avatar(course) and "quote-card__avatar" not in index_html:
            err("index.html: quote avatar is missing from the rendered quote")

    # Big-file warning
    for f in root.rglob("*"):
        if f.is_file() and f.stat().st_size > 50 * 1024 * 1024:
            warn(f"large file (>50MB): {f.relative_to(root)} ({f.stat().st_size // (1024*1024)} MB)")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    if not errors:
        print(f"\nOK — package at {root} validates.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

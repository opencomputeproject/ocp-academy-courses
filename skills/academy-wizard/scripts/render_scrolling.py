#!/usr/bin/env python3
"""Render an OCP Academy course using the Scrolling style from course.json."""

from __future__ import annotations

import html
import json
import copy
from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "templates"

# Canonical learner-facing control art for the maintained Scrolling style.
# Keep these vector paths verbatim; do not replace them with CSS-drawn approximations.
SCROLLING_FEEDBACK_CORRECT_PATH = (
    "M394 202 171 420Q167 424 164.5 429.5Q162 435 162 441Q162 447 164.5 452.5Q167 458 171 462"
    "L216 506Q221 510 226.5 512.5Q232 515 239 515Q246 515 251.5 512.5Q257 510 262 506L417 355"
    "L764 694Q768 698 773.5 700.5Q779 703 786 703Q792 703 798 700.5Q804 698 808 694L853 650"
    "Q857 646 859.5 640.5Q862 635 862 629Q862 623 859.5 617.5Q857 612 853 608L438 202"
    "Q434 198 428.5 195.5Q423 193 417 193Q410 193 404.5 195.5Q399 198 394 202Z"
)
SCROLLING_FEEDBACK_INCORRECT_PATH = (
    "M640 235 512 363 341 192 256 278 299 320 427 448 256 619 341 704 512 533 683 704 768 618 "
    "725 576 597 448 768 277 683 192Z"
)
SCROLLING_RETAKE_PATH = (
    "M40 224c-13.3 0-24-10.7-24-24L16 56c0-13.3 10.7-24 24-24s24 10.7 24 24l0 80.1 20-23.5"
    "C125 63.4 186.9 32 256 32c123.7 0 224 100.3 224 224s-100.3 224-224 224c-50.4 0-97-16.7-134.4-44.8"
    "c-10.6-8-12.7-23-4.8-33.6s23-12.7 33.6-4.8C179.8 418.9 216.3 432 256 432c97.2 0 176-78.8 176-176"
    "s-78.8-176-176-176c-54.3 0-102.9 24.6-135.2 63.4l-.1 .2s0 0 0 0L93.1 176l90.9 0c13.3 0 24 10.7 24 24"
    "s-10.7 24-24 24L40 224z"
)
SCROLLING_PROCESS_FORWARD_PATH = (
    "M305 239c9.4 9.4 9.4 24.6 0 33.9L113 465c-9.4 9.4-24.6 9.4-33.9 0"
    "s-9.4-24.6 0-33.9l175-175L79 81c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0L305 239z"
)
SCROLLING_MARKER_PLUS_PATH = (
    "M50 68.75Q52.637 68.75 54.443 66.943Q56.25 65.137 56.25 62.5L56.25 25"
    "Q56.25 22.363 54.443 20.557Q52.637 18.75 50 18.75Q47.363 18.75 45.557 20.557"
    "Q43.75 22.363 43.75 25L43.75 62.5Q43.75 65.137 45.557 66.943Q47.363 68.75 50 68.75Z"
    "M31.25 50L68.75 50Q71.387 50 73.193 48.193Q75 46.387 75 43.75Q75 41.113 73.193 39.307"
    "Q71.387 37.5 68.75 37.5L31.25 37.5Q28.613 37.5 26.807 39.307Q25 41.113 25 43.75"
    "Q25 46.387 26.807 48.193Q28.613 50 31.25 50Z"
)
SCROLLING_CALLOUT_PREVIOUS_PATH = (
    "M21.289 43.75L71.289 93.75L82.227 84.668L41.211 43.75L82.227 2.832L71.582-6.25L21.289 43.75Z"
)
SCROLLING_CALLOUT_NEXT_PATH = (
    "M78.711 43.75L28.711-6.25L17.773 2.832L58.789 43.75L17.773 84.668L28.418 93.75L78.711 43.75Z"
)
SCROLLING_CALLOUT_CLOSE_PATH = (
    "M9.78572 9.78572C9.5 10.0714 9.07143 10.0714 8.78571 9.78572L5 6.00001L1.21429 9.78572"
    "C0.928571 10.0714 0.500001 10.0714 0.214285 9.78572C-0.0714284 9.49999-0.0714284 9.07144 0.214285 8.78571"
    "L4 5 0.214285 1.21429C-0.0714284 0.928564-0.0714284 0.500007 0.214285 0.214279"
    "C0.357143 0.0714143 0.500001 0 0.714286 0 0.928571 0 1.07143 0.0714143 1.21429 0.214279"
    "L5 3.99999 8.78571 0.214279C8.92857 0.0714143 9.14286 0 9.28572 0 9.42857 0 9.64286 0.0714143 9.78572 0.214279"
    "C10.0714 0.500007 10.0714 0.928564 9.78572 1.21429L6 5 9.78572 8.78571"
    "C10.0714 9.07144 10.0714 9.49999 9.78572 9.78572Z"
)

# Canonical outlines for the maintained Video.js-compatible controls. Keeping
# the glyph geometry here avoids substitute artwork while leaving the renderer
# readable and dependency-free.
SCROLLING_VIDEO_ICONS = {
    "play": (1792, "M597 1419V373L1419 896Z"),
    "pause": (1792, "M448 373H747V1419H448ZM1045 1419V373H1344V1419Z"),
    "volume_muted": (
        1792,
        "M1232 896Q1232 993 1180 1075Q1130 1155 1045 1197V1032L1229 848Q1232 872 1232 896Z"
        "M1419 896Q1419 797 1378 699L1491 586Q1568 732 1568 896Q1568 1053 1499 1193Q1432 1328 1313 1422.5"
        "Q1194 1517 1045 1551V1397Q1153 1365 1238 1291.5Q1323 1218 1370 1117Q1419 1012 1419 896Z"
        "M319 1568 224 1473 577 1120H224V672H523L896 299V801L1214 483Q1134 422 1045 395V241Q1198 276 1320 376"
        "L1473 224L1568 319ZM896 1493 740 1337 896 1181Z",
    ),
    "volume_high": (
        1792,
        "M224 1120V672H523L896 299V1493L523 1120ZM1232 896Q1232 993 1180 1075Q1130 1155 1045 1197V595"
        "Q1130 637 1180 717Q1232 799 1232 896ZM1045 1551V1397Q1153 1365 1238 1291.5Q1323 1218 1370 1117"
        "Q1419 1012 1419 896Q1419 780 1370 675Q1323 574 1238 500.5Q1153 427 1045 395V241Q1194 275 1313 369.5"
        "Q1432 464 1499 599Q1568 739 1568 896Q1568 1053 1499 1193Q1432 1328 1313 1422.5Q1194 1517 1045 1551Z",
    ),
    "fullscreen_enter": (1792, "M523 747H373V373H747V523H523ZM373 1045H523V1269H747V1419H373ZM1269 523H1045V373H1419V747H1269ZM1045 1419V1269H1269V1045H1419V1419Z"),
    "fullscreen_exit": (1792, "M373 597H597V373H747V747H373ZM597 1195H373V1045H747V1419H597ZM1045 373H1195V597H1419V747H1045ZM1195 1195V1419H1045V1045H1419V1195Z"),
    "captions": (
        1792,
        "M1419 1493H373Q333 1493 298.5 1473Q264 1453 244 1419Q224 1385 224 1344V448Q224 407 244 373"
        "Q264 339 298.5 319Q333 299 373 299H1419Q1459 299 1493.5 319Q1528 339 1548 373Q1568 407 1568 448V1344"
        "Q1568 1385 1548 1419Q1528 1453 1493.5 1473Q1459 1493 1419 1493ZM821 971H709V1008H560V784H709V821H821V747"
        "Q821 716 799.5 694Q778 672 747 672H523Q492 672 470 694Q448 716 448 747V1045Q448 1076 470 1098Q492 1120 523 1120H747"
        "Q778 1120 799.5 1098Q821 1076 821 1045ZM1344 971H1232V1008H1083V784H1232V821H1344V747Q1344 716 1322 694"
        "Q1300 672 1269 672H1045Q1014 672 992.5 694Q971 716 971 747V1045Q971 1076 992.5 1098Q1014 1120 1045 1120H1269"
        "Q1300 1120 1322 1098Q1344 1076 1344 1045Z",
    ),
    "picture_in_picture_enter": (
        1792,
        "M1419 971H821V523H1419ZM1717 373V1420Q1717 1461 1697 1494.5Q1677 1528 1642.5 1548Q1608 1568 1568 1568H224"
        "Q184 1568 149.5 1548Q115 1528 95 1494.5Q75 1461 75 1420V373Q75 333 95 298.5Q115 264 149.5 244Q184 224 224 224H1568"
        "Q1608 224 1642.5 244Q1677 264 1697 298.5Q1717 333 1717 373ZM1568 372H224V1421H1568Z",
    ),
    "picture_in_picture_exit": (
        2190,
        "M1792 1394H398V398H1792ZM2190 199V1595Q2190 1649 2163.5 1694Q2137 1739 2091 1765.5Q2045 1792 1991 1792H199"
        "Q145 1792 99.5 1765.5Q54 1739 27 1694Q0 1649 0 1595V199Q0 145 27 99.5Q54 54 99.5 27Q145 0 199 0H1991"
        "Q2045 0 2090.5 27Q2136 54 2163 99.5Q2190 145 2190 199ZM1991 197H199V1596H1991Z",
    ),
}


def scrolling_video_icon(name: str, class_name: str = "") -> str:
    width, path = SCROLLING_VIDEO_ICONS[name]
    class_attr = f' class="{esc(class_name)}"' if class_name else ""
    return (
        f'<svg{class_attr} aria-hidden="true" viewBox="0 0 {width} 1792" focusable="false">'
        f'<g transform="translate(0 1792) scale(1 -1)"><path d="{path}" fill="currentColor"/></g></svg>'
    )


def _vtt_seconds(value: str) -> float | None:
    match = re.fullmatch(r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})", value.strip())
    if not match:
        return None
    hours = int(match.group(1) or 0)
    return hours * 3600 + int(match.group(2)) * 60 + int(match.group(3)) + int(match.group(4)) / 1000


def parse_webvtt(text: str) -> list[dict]:
    """Return readable cue data for the file://-safe caption renderer."""
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("WEBVTT"):
        return []
    cues: list[dict] = []
    for chunk in re.split(r"\n{2,}", normalized)[1:]:
        lines = [line for line in chunk.split("\n") if line.strip()]
        if not lines or lines[0].startswith(("NOTE", "STYLE", "REGION")):
            continue
        timing_index = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        start_text, end_text = (part.strip() for part in lines[timing_index].split("-->", 1))
        start = _vtt_seconds(start_text)
        end = _vtt_seconds(end_text.split()[0])
        if start is None or end is None or end <= start:
            continue
        cue_text = "\n".join(lines[timing_index + 1:]).strip()
        cue_text = re.sub(r"</?v(?:\s+[^>]*)?>", "", cue_text, flags=re.I)
        cue_text = re.sub(r"<[^>]+>", "", cue_text)
        cue_text = html.unescape(cue_text)
        if cue_text:
            cues.append({"start": start, "end": end, "text": cue_text})
    return cues


def hydrate_caption_cues(course: dict, resource_root: Path | None) -> dict:
    """Copy a course and embed VTT cue data without changing course.json."""
    hydrated = copy.deepcopy(course)
    if resource_root is None:
        return hydrated
    root = resource_root.resolve()

    def walk(value: object) -> None:
        if isinstance(value, dict):
            captions = value.get("captions")
            if isinstance(captions, list):
                for track in captions:
                    if not isinstance(track, dict) or not track.get("path"):
                        continue
                    candidate = (root / str(track["path"])).resolve()
                    try:
                        candidate.relative_to(root)
                    except ValueError:
                        track["_cues"] = []
                        continue
                    try:
                        track["_cues"] = parse_webvtt(candidate.read_text(encoding="utf-8-sig"))
                    except (OSError, UnicodeError):
                        track["_cues"] = []
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(hydrated)
    return hydrated


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def ui(labels: dict | None, key: str, default: str, **values: object) -> str:
    """Return a localized interface label while preserving English defaults."""
    template = str((labels or {}).get(key) or default)
    try:
        return template.format(**values)
    except (KeyError, ValueError):
        return default.format(**values)


def css_string(value: object) -> str:
    text = str(value or "Arial").replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def safe_color(value: object, fallback: str) -> str:
    text = str(value or "")
    return text if re.fullmatch(r"#[0-9a-fA-F]{3,8}", text) else fallback


def contrasting_text(color: str) -> str:
    value = color.lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if len(value) < 6:
        return "#000000"
    red, green, blue = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    luminance = (0.299 * red + 0.587 * green + 0.114 * blue) / 255
    return "#000000" if luminance > 0.58 else "#ffffff"


def rgba_color(color: str, opacity: float) -> str | None:
    value = color.lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if not re.fullmatch(r"[0-9a-fA-F]{6,8}", value):
        return None
    red, green, blue = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    return f"rgba({red},{green},{blue},{opacity:g})"


def format_file_size(value: object) -> str:
    try:
        size = max(0, int(value))
    except (TypeError, ValueError):
        return ""
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    if size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / (1024 * 1024 * 1024):.1f} GB"


def is_scrolling(course: dict) -> bool:
    return str(course.get("style") or "Slides").strip().casefold() == "scrolling"


def runtime_files(course: dict) -> list[str]:
    found: set[str] = {"index.html", "scorm_api.js"}

    def walk(value: object) -> None:
        if isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str) and value.startswith("resources/"):
            found.add(value)

    walk(course)
    for key in ("course_logo", "academy_logo"):
        path = (course.get("brand") or {}).get(key)
        if path:
            found.add(path)
    return sorted(found)


def font_face_css(theme: dict) -> str:
    rules = []
    for face in theme.get("font_faces", []) if isinstance(theme.get("font_faces"), list) else []:
        if not isinstance(face, dict) or not face.get("family") or not face.get("path"):
            continue
        path = str(face["path"]).replace('"', "%22")
        weight = int(face.get("weight") or 400)
        style = "italic" if str(face.get("style") or "normal").casefold() == "italic" else "normal"
        suffix = Path(path).suffix.lower().lstrip(".")
        format_name = {"woff": "woff", "woff2": "woff2", "ttf": "truetype", "otf": "opentype"}.get(suffix, suffix)
        rules.append(
            f'@font-face{{font-family:{css_string(face["family"])};src:url("{path}") format("{format_name}");'
            f'font-weight:{weight};font-style:{style};font-display:swap;}}'
        )
    return "\n".join(rules)


def media_figure(
    media: dict | None,
    caption_html: str = "",
    extra_class: str = "",
    zoomable: bool = False,
    cropped: bool = False,
    decorative: bool = False,
    ui_labels: dict | None = None,
) -> str:
    if not media or not media.get("path"):
        return ""
    path = esc(media["path"])
    alt = "" if decorative else esc(media.get("alt") or ui(ui_labels, "course_media", "Course media"))
    accessibility = ' aria-hidden="true"' if decorative else ""
    caption = f"<figcaption>{caption_html}</figcaption>" if caption_html else ""
    image = f'<img src="{path}" alt="{alt}" loading="lazy"{accessibility}>'
    if zoomable and not decorative:
        image = (
            f'<button class="media-zoom" type="button" data-zoom-src="{path}" data-zoom-alt="{alt}" '
            f'aria-label="{esc(ui(ui_labels, "zoom_image", "Zoom image"))}">{image}</button>'
        )
    crop_class = " media-card--crop" if cropped else ""
    crop_style = f' style="background-image:url(\'{path}\')"' if cropped else ""
    return f'<figure class="media-card {esc(extra_class)}{crop_class}"{crop_style}>{image}{caption}</figure>'


def video_figure(
    media: dict | None,
    caption_html: str = "",
    animate: bool = True,
    ui_labels: dict | None = None,
) -> str:
    if not media or not media.get("path"):
        return ""
    poster = f' poster="{esc(media.get("poster"))}"' if media.get("poster") else ""
    caption_tracks = [track for track in media.get("captions", []) if isinstance(track, dict) and track.get("path")]
    tracks = "".join(
        f'<track kind="captions" src="{esc(track["path"])}" srclang="{esc(track.get("language") or "en")}" '
        f'label="{esc(track.get("label") or track.get("language") or ui(ui_labels, "captions", "Captions"))}">'
        for track in caption_tracks
    )
    caption_payload = {
        "tracks": [
            {
                "path": str(track["path"]),
                "language": str(track.get("language") or "en"),
                "label": str(track.get("label") or track.get("language") or ui(ui_labels, "captions", "Captions")),
                "cues": track.get("_cues") or [],
            }
            for track in caption_tracks
        ]
    }
    caption_json = json.dumps(caption_payload, ensure_ascii=False, indent=2).replace("</", "<\\/")
    caption = f"<figcaption>{caption_html}</figcaption>" if caption_html else '<figcaption class="is-empty"></figcaption>'
    motion = " scroll-animate scroll-animate--fade" if animate else ""
    duration = media.get("duration_seconds")
    if isinstance(duration, (int, float)) and duration >= 0:
        initial_remaining = f'-{int(duration) // 60}:{int(duration) % 60:02d}'
    else:
        initial_remaining = "-0:00"
    speed_items = "".join(
        f'<button class="academy-video__menu-item{" is-selected" if rate == 1 else ""}" type="button" role="menuitemradio" '
        f'data-video-rate="{rate:g}" aria-checked="{"true" if rate == 1 else "false"}">{rate:g}x</button>'
        for rate in (2, 1.75, 1.5, 1.25, 1, 0.75, 0.5)
    )
    captions_control = ""
    caption_data = ""
    if caption_tracks:
        caption_items = (
            '<button class="academy-video__menu-item is-selected" type="button" role="menuitemradio" '
            f'data-video-caption-index="-1" aria-checked="true">{esc(ui(ui_labels, "captions_off", "Captions off"))}</button>'
            + "".join(
                f'<button class="academy-video__menu-item" type="button" role="menuitemradio" '
                f'data-video-caption-index="{index}" aria-checked="false">'
                f'{esc(track.get("label") or track.get("language") or ui(ui_labels, "captions", "Captions"))}</button>'
                for index, track in enumerate(caption_tracks)
            )
        )
        captions_label = esc(ui(ui_labels, "captions", "Captions"))
        captions_control = (
            '<div class="academy-video__menu-control academy-video__captions-control">'
            '<button class="academy-video__button academy-video__captions" type="button" data-video-menu-button="captions" '
            f'title="{captions_label}" aria-label="{captions_label}" aria-haspopup="true" aria-expanded="false">'
            f'{scrolling_video_icon("captions")}</button>'
            '<div class="academy-video__menu" data-video-menu="captions" hidden>'
            f'<div class="academy-video__menu-content" role="menu">{caption_items}</div></div></div>'
        )
        caption_data = (
            '<div class="academy-video__caption-display" data-video-caption-display aria-live="off" aria-atomic="true" hidden>'
            '<span data-video-caption-text></span></div>'
            f'<script class="academy-video__caption-data" type="application/json">{caption_json}</script>'
        )
    return (
        f'<figure class="media-card video-wrap{motion}">'
        '<div class="academy-video" data-video-player>'
        f'<video preload="auto" playsinline src="{esc(media["path"])}"{poster}><source src="{esc(media["path"])}">{tracks}</video>'
        f'{caption_data}'
        f'<button class="academy-video__big-play" type="button" data-video-action="toggle" aria-label="{esc(ui(ui_labels, "play_video", "Play video"))}">'
        f'{scrolling_video_icon("play")}'
        '</button>'
        '<div class="academy-video__controls">'
        f'<button class="academy-video__button academy-video__toggle" type="button" data-video-action="toggle" aria-label="{esc(ui(ui_labels, "play", "Play"))}">'
        f'{scrolling_video_icon("play", "academy-video__play-icon")}{scrolling_video_icon("pause", "academy-video__pause-icon")}'
        '</button>'
        '<div class="academy-video__progress-control">'
        '<div class="academy-video__progress-track"><span class="academy-video__progress-loaded" data-video-loaded></span>'
        '<span class="academy-video__progress-played" data-video-played><i aria-hidden="true"></i></span></div>'
        f'<input class="academy-video__progress" type="range" min="0" max="100" step="0.1" value="0" data-video-progress aria-label="{esc(ui(ui_labels, "seek", "Seek"))}">'
        '</div>'
        f'<span class="academy-video__remaining" data-video-remaining>{initial_remaining}</span>'
        '<div class="academy-video__menu-control academy-video__rate-control">'
        '<span class="academy-video__rate-value" data-video-rate-value aria-hidden="true">1x</span>'
        f'<button class="academy-video__button academy-video__rate" type="button" data-video-menu-button="rate" '
        f'title="{esc(ui(ui_labels, "playback_rate", "Playback Rate"))}" aria-label="{esc(ui(ui_labels, "playback_rate", "Playback Rate"))}" aria-haspopup="true" aria-expanded="false"></button>'
        f'<div class="academy-video__menu" data-video-menu="rate" hidden><div class="academy-video__menu-content" role="menu">{speed_items}</div></div></div>'
        f'{captions_control}'
        f'<button class="academy-video__button academy-video__picture-in-picture" type="button" data-video-action="picture-in-picture" title="{esc(ui(ui_labels, "picture_in_picture", "Picture-in-picture"))}" aria-label="{esc(ui(ui_labels, "picture_in_picture", "Picture-in-picture"))}">'
        f'{scrolling_video_icon("picture_in_picture_enter", "academy-video__pip-enter")}{scrolling_video_icon("picture_in_picture_exit", "academy-video__pip-exit")}</button>'
        f'<button class="academy-video__button academy-video__fullscreen" type="button" data-video-action="fullscreen" aria-label="{esc(ui(ui_labels, "fullscreen", "Fullscreen"))}">'
        f'{scrolling_video_icon("fullscreen_enter", "academy-video__fullscreen-enter")}{scrolling_video_icon("fullscreen_exit", "academy-video__fullscreen-exit")}'
        '</button>'
        '<div class="academy-video__volume-panel">'
        f'<button class="academy-video__button academy-video__mute" type="button" data-video-action="mute" aria-label="{esc(ui(ui_labels, "mute", "Mute"))}">'
        f'{scrolling_video_icon("volume_high", "academy-video__volume-high")}{scrolling_video_icon("volume_muted", "academy-video__volume-muted")}</button>'
        f'<div class="academy-video__volume-control"><input class="academy-video__volume" type="range" min="0" max="1" step="0.05" value="1" data-video-volume aria-label="{esc(ui(ui_labels, "volume", "Volume"))}"></div>'
        '</div>'
        '</div></div>'
        f'{caption}</figure>'
    )


def interactive_content(item: dict, ui_labels: dict | None = None) -> str:
    description = item.get("description_html") or item.get("body_html") or ""
    media = media_figure(item.get("media"), item.get("caption_html") or "", ui_labels=ui_labels)
    return f'{description}{media}'


def flashcard_content(item: dict, ui_labels: dict | None = None) -> str:
    """Description cards may carry a placeholder image that is not displayed."""
    description = item.get("description_html") or item.get("body_html") or ""
    if str(item.get("type") or "").casefold() == "description":
        return description
    return interactive_content(item, ui_labels)


def render_interactive(block: dict, lesson_id: int, ui_labels: dict | None = None) -> str:
    block_type = block.get("type") or "interactive"
    visible_items = [item for item in block.get("items", []) if not item.get("hidden")]
    if block_type == "tabs":
        tab_id = f'tabs-{lesson_id}-{block.get("id")}'
        buttons = []
        panels = []
        for index, item in enumerate(visible_items, start=1):
            active = " is-active" if index == 1 else ""
            selected = "true" if index == 1 else "false"
            panel_id = f'{tab_id}-panel-{index}'
            buttons.append(
                f'<button class="tab-button{active}" type="button" role="tab" aria-selected="{selected}" '
                f'data-tab-panel="{panel_id}">{esc(item.get("title") or item.get("label") or f"Tab {index}")}</button>'
            )
            panels.append(
                f'<section class="tab-panel{active}" id="{panel_id}" role="tabpanel">{interactive_content(item, ui_labels)}</section>'
            )
        return f'<div class="tab-set"><div class="tab-list" role="tablist">{"".join(buttons)}</div>{"".join(panels)}</div>'
    if block_type == "process":
        role_order = {"intro": 0, "step": 1, "summary": 3}
        visible_items = [
            item for _, item in sorted(
                enumerate(visible_items),
                key=lambda pair: (role_order.get(str(pair[1].get("type") or "step").casefold(), 2), pair[0]),
            )
        ]
        process_id = f'process-{lesson_id}-{block.get("id")}'
        steps = []
        controls = []
        zoomable = bool((block.get("style") or {}).get("zoom_on_click", False))
        process_style = block.get("style") if isinstance(block.get("style"), dict) else {}
        control_tone = str(process_style.get("control_tone") or "").casefold()
        if control_tone not in {"light", "dark"}:
            background_color = str(process_style.get("background_color") or "")
            control_tone = "light" if background_color and contrasting_text(background_color) == "#ffffff" else "dark"
        step_number = 0
        for index, item in enumerate(visible_items, start=1):
            item_type = str(item.get("type") or "step").casefold()
            if item_type == "step":
                step_number += 1
            selected = "true" if index == 1 else "false"
            hidden = "" if index == 1 else " hidden"
            media = media_figure(
                item.get("media"), item.get("caption_html") or "", zoomable=zoomable, ui_labels=ui_labels
            )
            number = (
                f'<span class="process-step__number">{esc(ui(ui_labels, "step", "Step {number}", number=step_number))}</span>'
                if item_type == "step" else ""
            )
            action = ""
            if item_type == "intro":
                action = (
                    '<button class="process-step__start" type="button" data-process-action="next">'
                    f'<span>{esc(ui(ui_labels, "start", "START"))}</span><svg aria-hidden="true" viewBox="0 0 320 512" focusable="false">'
                    f'<path fill="currentColor" d="{SCROLLING_PROCESS_FORWARD_PATH}"/></svg></button>'
                )
                control_content = (
                    '<svg aria-hidden="true" viewBox="0 0 320 512" focusable="false">'
                    f'<path fill="currentColor" d="{SCROLLING_PROCESS_FORWARD_PATH}"/></svg>'
                )
                control_label = item.get("title") or ui(ui_labels, "introduction", "Introduction")
            elif item_type == "summary":
                action = (
                    '<button class="process-step__restart" type="button" data-process-target="0">'
                    f'<span>{esc(ui(ui_labels, "start_again", "START AGAIN"))}</span><svg aria-hidden="true" viewBox="0 0 512 512" focusable="false">'
                    f'<path fill="currentColor" d="{SCROLLING_RETAKE_PATH}"/></svg></button>'
                )
                control_content = (
                    '<svg aria-hidden="true" viewBox="0 0 512 512" focusable="false">'
                    f'<path fill="currentColor" d="{SCROLLING_RETAKE_PATH}"/></svg>'
                )
                control_label = item.get("title") or ui(ui_labels, "conclusion", "Conclusion")
            else:
                control_content = str(step_number)
                control_label = ui(ui_labels, "step", "Step {number}", number=step_number)
            steps.append(
                f'<article class="process-slide process-slide--{esc(item_type)}" data-process-slide="{index - 1}"{hidden} role="group" '
                f'aria-label="{esc(ui(ui_labels, "slide_position", "{current} of {total}", current=index, total=len(visible_items)))}">'
                f'<div class="process-step process-step--{esc(item_type)}">'
                f'{number}'
                f'<div class="process-step__title"><h2>{esc(item.get("title") or item.get("label") or "")}</h2></div>'
                f'<div class="process-step__media">{media}</div>'
                f'<div class="process-step__description">{item.get("description_html") or item.get("body_html") or ""}</div>'
                f'{action}</div></article>'
            )
            controls.append(
                f'<li><button type="button" data-process-target="{index - 1}" '
                f'aria-label="{esc(ui(ui_labels, "go_to_slide", "Go to slide {title}", title=control_label))}" '
                f'aria-current="{selected}">{control_content}</button></li>'
            )
        return (
            f'<div class="process-shell"><div class="process-carousel process-carousel--controls-{control_tone}" '
            f'id="{esc(process_id)}" data-process-index="0" role="region" aria-label="{esc(ui(ui_labels, "carousel", "Carousel"))}">'
            '<div class="process-controls">'
            f'<button class="process-controls__previous" type="button" data-process-action="previous" aria-label="{esc(ui(ui_labels, "previous_slide", "Go to previous slide"))}">'
            '<span aria-hidden="true"><svg viewBox="0 0 320 512" focusable="false"><path fill="currentColor" d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l192 192c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L77.3 256 246.6 86.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-192 192z"/></svg></span></button>'
            f'<ol class="process-controls__items">{"".join(controls)}</ol>'
            f'<span class="visually-hidden" data-process-count>{esc(ui(ui_labels, "slide_position", "{current} of {total}", current=1, total=len(visible_items)))}</span>'
            f'<button class="process-controls__next" type="button" data-process-action="next" aria-label="{esc(ui(ui_labels, "next_slide", "Go to next slide"))}">'
            '<span aria-hidden="true"><svg viewBox="0 0 320 512" focusable="false"><path fill="currentColor" d="M310.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-192 192c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L242.7 256 73.4 86.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l192 192z"/></svg></span></button>'
            f'</div><div class="process-slides" aria-live="polite">{"".join(steps)}</div>'
            '</div></div>'
        )
    items = []
    for item in visible_items:
        items.append(
            '<details class="interactive-card">'
            '<summary><span class="interactive-card__title">'
            f'{esc(item.get("title") or item.get("label") or ui(ui_labels, "explore", "Explore"))}'
            '</span><span class="interactive-card__toggler" aria-hidden="true">'
            '<svg class="interactive-card__plus" viewBox="0 0 512 512" focusable="false"><path fill="currentColor" d="M488 232c13.3 0 24 10.7 24 24s-10.7 24-24 24H280v208c0 13.3-10.7 24-24 24s-24-10.7-24-24V280H24c-13.3 0-24-10.7-24-24s10.7-24 24-24h208V24c0-13.3 10.7-24 24-24s24 10.7 24 24v208h208z"/></svg>'
            '<svg class="interactive-card__minus" viewBox="0 0 448 512" focusable="false"><path fill="currentColor" d="M432 232c13.3 0 24 10.7 24 24s-10.7 24-24 24H40c-13.3 0-24-10.7-24-24s10.7-24 24-24h392z"/></svg>'
            '</span></summary>'
            f'<div class="interactive-card__content">{interactive_content(item, ui_labels)}</div></details>'
        )
    return "".join(items)


def render_block(block: dict, lesson_id: int, ui_labels: dict | None = None) -> str:
    block_type = block.get("type") or "unknown"
    variant = block.get("variant") or ""
    style = block.get("style") if isinstance(block.get("style"), dict) else {}
    if block_type == "text":
        heading_html = str(block.get("heading_html") or "")
        if heading_html:
            heading_tag = "h3" if "subheading" in str(variant).casefold() else "h2"
            if not re.search(r"<h[1-6](?:\s|>)", heading_html, flags=re.I):
                heading_html = re.sub(
                    r"<p(?:\s[^>]*)?>(.*?)</p>",
                    rf"<{heading_tag}>\1</{heading_tag}>",
                    heading_html,
                    flags=re.I | re.S,
                )
        return f'<div class="block-content">{heading_html}{block.get("body_html", "")}</div>'
    if block_type == "list":
        tag = "ol" if block.get("list_style") == "numbered" else "ul"
        numbered = tag == "ol"
        animate = style.get("entrance_animation", True)
        rendered_items = []
        for index, item in enumerate(block.get("items_html", [])):
            animation_class = ' class="scroll-animate scroll-animate--slide-right"' if animate else ""
            animation_style = f' style="--animation-delay:{0.12 + index * 0.25:.2f}s"' if animate else ""
            if numbered:
                content = (
                    f'<span class="numbered-list__number" aria-hidden="true">{index + 1}</span>'
                    f'<div class="numbered-list__content">{item}</div>'
                )
            else:
                content = item
            rendered_items.append(f'<li{animation_class}{animation_style}>{content}</li>')
        items = "".join(rendered_items)
        return f'<{tag}>{items}</{tag}>'
    if block_type == "image":
        media = block.get("media") if isinstance(block.get("media"), dict) else {}
        dimensions = media.get("dimensions") if isinstance(media.get("dimensions"), dict) else {}
        cropped = variant == "full"
        image_role = str(block.get("image_role") or "content").strip().casefold()
        decorative = image_role in {"decorative", "design"}
        position = str(style.get("image_position") or "left").strip().casefold()
        if position not in {"left", "right"}:
            position = "left"
        motion = "scroll-animate--slide-left" if position == "left" else "scroll-animate--slide-right"
        if variant != "text_aside":
            motion = "scroll-animate--fade"
        animate = style.get("entrance_animation", True)
        figure = media_figure(
            media,
            block.get("caption_html") or "",
            extra_class=f"scroll-animate {motion}" if animate else "",
            zoomable=not decorative and bool(style.get("zoom_on_click", False)),
            cropped=cropped,
            decorative=decorative,
            ui_labels=ui_labels,
        )
        body = block.get("body_html") or ""
        if variant == "text_aside" and body:
            return f'<div class="media-aside"><div class="media-aside__text">{body}</div>{figure}</div>'
        return f'{body}{figure}'
    if block_type == "video":
        return video_figure(
            block.get("media"),
            block.get("caption_html") or "",
            animate=style.get("entrance_animation") is True,
            ui_labels=ui_labels,
        )
    if block_type == "attachment":
        media = block.get("media") or {}
        if not media.get("path"):
            return ""
        label = str(block.get("label") or media.get("alt") or ui(ui_labels, "open_attachment", "Open attachment"))
        size = format_file_size(media.get("bytes"))
        size_markup = f'<span class="attachment-card__size">{esc(size)}</span>' if size else ""
        pdf_icon = (
            f'<svg class="attachment-card__file-icon" aria-label="{esc(ui(ui_labels, "pdf_file", "PDF file"))}" fill="none" focusable="false" '
            'height="50" role="img" viewBox="0 0 40 50" width="40" xmlns="http://www.w3.org/2000/svg">'
            '<path clip-rule="evenodd" d="M2 0C.895 0 0 .895 0 2v46c0 1.105.895 2 2 2h36c1.105 0 2-.895 2-2V14L26 0H2Z" fill="#F5D0CE" fill-rule="evenodd"/>'
            '<path clip-rule="evenodd" d="M26 0v14h14" fill="#EDADA9" fill-rule="evenodd"/>'
            '<path d="M10.8678 28.3213V30.9998H9.00879V22.9863H11.8358C12.4005 22.9863 12.8845 23.0542 13.2878 23.1898C13.6948 23.3218 14.0285 23.5052 14.2888 23.7398C14.5528 23.9745 14.7471 24.2513 14.8718 24.5703C14.9965 24.8893 15.0588 25.234 15.0588 25.6043C15.0588 26.004 14.9946 26.3707 14.8663 26.7043C14.738 27.038 14.5418 27.324 14.2778 27.5623C14.0138 27.8007 13.6783 27.9877 13.2713 28.1233C12.868 28.2553 12.3895 28.3213 11.8358 28.3213H10.8678ZM10.8678 26.9188H11.8358C12.3198 26.9188 12.6681 26.8033 12.8808 26.5723C13.0935 26.3413 13.1998 26.0187 13.1998 25.6043C13.1998 25.421 13.1723 25.2542 13.1173 25.1038C13.0623 24.9535 12.978 24.8252 12.8643 24.7188C12.7543 24.6088 12.6131 24.5245 12.4408 24.4658C12.2721 24.4072 12.0705 24.3778 11.8358 24.3778H10.8678V26.9188Z" fill="#771D18"/>'
            '<path d="M24.2944 26.9903C24.2944 27.5697 24.1936 28.105 23.9919 28.5963C23.7939 29.084 23.5134 29.5075 23.1504 29.8668C22.7874 30.2225 22.3493 30.5012 21.8359 30.7028C21.3263 30.9008 20.7598 30.9998 20.1364 30.9998H17.0234V22.9863H20.1364C20.7598 22.9863 21.3263 23.0872 21.8359 23.2888C22.3493 23.4905 22.7874 23.7692 23.1504 24.1248C23.5134 24.4805 23.7939 24.904 23.9919 25.3953C24.1936 25.883 24.2944 26.4147 24.2944 26.9903ZM22.3914 26.9903C22.3914 26.5943 22.3401 26.2368 22.2374 25.9178C22.1348 25.5988 21.9863 25.3293 21.7919 25.1093C21.6013 24.8857 21.3666 24.7152 21.0879 24.5978C20.8093 24.4768 20.4921 24.4163 20.1364 24.4163H18.8934V29.5698H20.1364C20.4921 29.5698 20.8093 29.5112 21.0879 29.3938C21.3666 29.2728 21.6013 29.1023 21.7919 28.8823C21.9863 28.6587 22.1348 28.3873 22.2374 28.0683C22.3401 27.7493 22.3914 27.39 22.3914 26.9903Z" fill="#771D18"/>'
            '<path d="M31.3465 22.9863V24.4163H28.0575V26.4458H30.7965V27.8813H28.0575V30.9998H26.1875V22.9863H31.3465Z" fill="#771D18"/>'
            '</svg>'
        )
        download_icon = (
            '<svg class="attachment-card__download-icon" focusable="false" height="19" viewBox="0 0 16 19" width="16">'
            f'<title>{esc(ui(ui_labels, "download", "Download"))}</title><desc>{esc(ui(ui_labels, "download", "Download"))}</desc>'
            '<rect height="2" rx="1" width="16" y="17"/>'
            '<path d="M4.464 8.293A1 1 0 1 0 3.05 9.707l4.24 4.24c.4.4 1.028.392 1.42 0l4.24-4.24a1 1 0 1 0-1.414-1.414L8 4.757 4.464 8.293zm0 0L8 4.757l3.536 3.536L8 11.828 4.464 8.293z"/>'
            '<path d="M7 0h2v12H7z"/></svg>'
        )
        return (
            f'<a class="attachment-card" href="{esc(media["path"])}" download="{esc(label)}" '
            f'target="_blank" rel="noopener noreferrer nofollow" aria-label="{esc(ui(ui_labels, "download", "Download"))} {esc(label)}">'
            f'<span class="attachment-card__main"><span class="attachment-card__icon">{pdf_icon}</span>'
            f'<span class="attachment-card__info"><span class="attachment-card__title">{esc(label)}</span>{size_markup}</span></span>'
            f'<span class="attachment-card__rest">{download_icon}</span></a>'
        )
    if block_type == "impact":
        return f'<div class="impact-statement">{block.get("body_html") or ""}</div>'
    if block_type == "divider":
        if variant == "numbered_divider":
            number = esc(block.get("number") or block.get("id") or "")
            return (
                '<div class="numbered-divider">'
                f'<span class="numbered-divider__number"><span class="visually-hidden">Numbered divider</span>{number}</span>'
                '</div>'
            )
        return "<hr>"
    if block_type == "continue":
        label = esc(block.get("label") or ui(ui_labels, "continue", "CONTINUE"))
        motion = " scroll-animate scroll-animate--fade" if style.get("entrance_animation", True) else ""
        return (
            f'<div class="continue-band{motion}">'
            f'<button class="continue-button" type="button" data-label="{label}">{label}</button>'
            f'<p class="continue-hint">{esc(block.get("complete_hint") or ui(ui_labels, "complete_hint", "Complete the content above before moving on."))}</p>'
            '</div>'
        )
    if block_type == "quote":
        variant = re.sub(r"[^a-z0-9_-]+", "-", str(block.get("variant") or "").casefold()).strip("-").replace("_", "-")
        avatar = block.get("avatar") if isinstance(block.get("avatar"), dict) else {}
        avatar_html = ""
        if avatar.get("path"):
            avatar_html = f'<img class="quote-card__avatar" src="{esc(avatar["path"])}" alt="{esc(avatar.get("alt") or "")}">'
        classes = f'quote-card quote-card--{variant}' if variant else 'quote-card'
        if avatar_html:
            classes += ' quote-card--with-avatar'
        return (
            f'<figure class="{classes}">{avatar_html}<div class="quote-card__body">'
            f'<blockquote><div class="quote-card__text">{block.get("quote_html", "")}</div></blockquote>'
            f'<footer>{block.get("attribution_html", "")}</footer></div></figure>'
        )
    if block_type == "buttons":
        rows = []
        action_left = str(style.get("button_alignment") or "right").casefold() == "left"
        configured_button_width = style.get("button_width_px")
        if isinstance(configured_button_width, (int, float)):
            button_width = max(170, min(int(configured_button_width), 600))
        else:
            longest_label = max((len(str(item.get("label") or "")) for item in block.get("buttons", [])), default=0)
            button_width = max(170, min(360, 80 + longest_label * 7))
        for item in block.get("buttons", []):
            label = esc(item.get("label") or ui(ui_labels, "open_resource", "Open resource"))
            is_exit = str(item.get("type") or "").casefold() == "exit-course"
            if is_exit:
                control = f'<button class="course-button" type="button" data-exit-course>{label}</button>'
            else:
                control = (
                    f'<a class="course-button" href="{esc(item.get("url") or "#")}" '
                    f'target="_blank" rel="noopener">{label}</a>'
                )
            description = f'<div class="resource-button-description">{item.get("description_html") or ""}</div>'
            action = f'<div class="resource-button-action">{control}</div>'
            row_classes = ["resource-button-row"]
            if action_left:
                row_classes.append("resource-button-row--action-left")
            if is_exit:
                row_classes.append("resource-button-row--exit")
            row_content = action + description if action_left else description + action
            rows.append(f'<div class="{" ".join(row_classes)}">{row_content}</div>')
        return f'<div class="resource-button-list" style="--resource-button-width:{button_width}px">{"".join(rows)}</div>'
    if block_type == "flashcards":
        cards = []
        flashcard_size = str(style.get("flashcard_size") or "small").strip().casefold()
        large_cards = flashcard_size == "large"
        card_class = "flashcard flashcard--large" if large_cards else "flashcard"
        flip_icon = (
            '<span class="flashcard__flip" aria-hidden="true">'
            '<svg viewBox="0 0 23 17" focusable="false"><path fill="currentColor" fill-rule="nonzero" '
            'd="M19.347 8.275l1.88 1.714a.727.727 0 0 0 .98-1.074l-3.225-2.941a.727.727 0 0 0-1.027.047l-2.94 3.224a.727.727 0 0 0 1.075.98l1.802-1.976a6.545 6.545 0 0 1-11.56 4.288.727.727 0 1 0-1.114.935 8 8 0 0 0 14.129-5.197zm-16.039.162l-1.79-1.633a.727.727 0 1 0-.98 1.074l3.223 2.94c.297.272.757.25 1.028-.046l2.94-3.224a.727.727 0 0 0-1.075-.98L4.768 8.636a6.545 6.545 0 0 1 11.555-4.482.727.727 0 1 0 1.114-.936A8 8 0 0 0 3.308 8.437z"/>'
            '</svg></span>'
        )
        for index, card in enumerate(block.get("cards", []), start=1):
            front = flashcard_content(card.get("front") or {}, ui_labels)
            back = flashcard_content(card.get("back") or {}, ui_labels)
            cards.append(
                f'<div class="{card_class}" role="button" tabindex="0" aria-pressed="false" '
                f'aria-label="{esc(ui(ui_labels, "flip_card", "Flip card {number}", number=index))}">'
                f'<div class="flashcard__front"><div class="flashcard__description"><div class="flashcard__description-inner">'
                f'{front}</div></div>{flip_icon}</div>'
                f'<div class="flashcard__back"><div class="flashcard__description"><div class="flashcard__description-inner">'
                f'{back}</div></div>{flip_icon}</div></div>'
            )
        count_class = f' flashcard-grid--{len(cards)}' if cards else ""
        size_class = " flashcard-grid--large" if large_cards else ""
        return f'<div class="flashcard-grid{count_class}{size_class}">{"".join(cards)}</div>'
    if block_type in {"accordion", "tabs", "process", "interactive"}:
        return render_interactive(block, lesson_id, ui_labels)
    if block_type == "labeled_graphic":
        media = block.get("media") or {}
        if not media.get("path"):
            return ""
        labeled_style = block.get("style") if isinstance(block.get("style"), dict) else {}
        media_width = str(labeled_style.get("media_width") or "").strip()
        width_variant = str(labeled_style.get("media_width_variant") or "").casefold()
        if width_variant not in {"medium", "full"}:
            width_variant = {"1": "medium", "2": "full"}.get(media_width, "medium")
        graphic_id = f'labeled-graphic-{lesson_id}-{block.get("id")}'
        dimensions = media.get("dimensions") if isinstance(media.get("dimensions"), dict) else {}
        width = dimensions.get("originalWidth") or dimensions.get("width")
        height = dimensions.get("originalHeight") or dimensions.get("height")
        size_attrs = f' width="{esc(width)}" height="{esc(height)}"' if width and height else ""
        items = []
        visible_items = [item for item in block.get("items", []) if not item.get("hidden")]
        for index, item in enumerate(visible_items, start=1):
            marker_id = f'{graphic_id}-marker-{index}'
            callout_id = f'{graphic_id}-callout-{index}'
            title = str(item.get("title") or ui(ui_labels, "marker", "Marker {number}", number=index))
            try:
                x = max(0.0, min(100.0, float(item.get("x") or 50)))
            except (TypeError, ValueError):
                x = 50.0
            try:
                y = max(0.0, min(100.0, float(item.get("y") or 50)))
            except (TypeError, ValueError):
                y = 50.0
            horizontal = "left" if x >= 50 else "right"
            vertical = "top" if y < 66 else "bottom"
            marker_style = f'--marker-x:{x:g}%;--marker-y:{y:g}%;--marker-delay:{(index - 1) * 0.2:g}s'
            plus_icon = (
                '<svg class="labeled-graphic__plus" viewBox="25 18.75 50 50" focusable="false" aria-hidden="true">'
                f'<path fill="currentColor" d="{SCROLLING_MARKER_PLUS_PATH}"/></svg>'
            )
            previous_icon = (
                '<svg viewBox="0 -6.25 100 100" focusable="false" aria-hidden="true">'
                f'<path fill="currentColor" d="{SCROLLING_CALLOUT_PREVIOUS_PATH}"/></svg>'
            )
            next_icon = (
                '<svg viewBox="0 -6.25 100 100" focusable="false" aria-hidden="true">'
                f'<path fill="currentColor" d="{SCROLLING_CALLOUT_NEXT_PATH}"/></svg>'
            )
            close_icon = (
                '<svg aria-hidden="true" class="labeled-graphic__close-icon" fill="currentColor" focusable="false" '
                'viewBox="0 0 10 10"><path '
                f'd="{SCROLLING_CALLOUT_CLOSE_PATH}"/></svg>'
            )
            items.append(
                '<li class="labeled-graphic__item">'
                f'<button class="labeled-graphic__marker" id="{marker_id}" type="button" style="{marker_style}" '
                f'data-labeled-marker="{index - 1}" data-marker-index="{index - 1}" data-marker-title="{esc(title)}" '
                f'aria-controls="{callout_id}" aria-expanded="false" '
                f'aria-label="{esc(ui(ui_labels, "marker_status", "Marker, {title}, Plus, Not viewed", title=title))}">'
                f'<span class="labeled-graphic__pin">{plus_icon}</span></button>'
                f'<div class="labeled-graphic__bubble labeled-graphic__bubble--{horizontal} labeled-graphic__bubble--{vertical}" '
                f'id="{callout_id}" data-labeled-callout="{index - 1}" data-marker-index="{index - 1}" style="{marker_style}" hidden>'
                '<div class="labeled-graphic__callout" role="dialog" aria-modal="false" '
                f'aria-labelledby="{callout_id}-title">'
                f'<h2 class="labeled-graphic__title" id="{callout_id}-title" tabindex="-1">{esc(title)}</h2>'
                f'<button class="labeled-graphic__close" type="button" data-labeled-action="close" aria-label="{esc(ui(ui_labels, "close_modal", "Close modal"))}">{close_icon}</button>'
                f'<div class="labeled-graphic__content"><div class="labeled-graphic__description">{item.get("description_html") or ""}</div></div>'
                '<div class="labeled-graphic__controls">'
                f'<button class="labeled-graphic__previous" type="button" data-labeled-action="previous" aria-label="{esc(ui(ui_labels, "previous", "Previous"))}">{previous_icon}</button>'
                f'<button class="labeled-graphic__next" type="button" data-labeled-action="next" aria-label="{esc(ui(ui_labels, "next", "Next"))}">{next_icon}</button>'
                '</div></div></div></li>'
            )
        return (
            f'<div class="labeled-graphic labeled-graphic--{width_variant}" id="{graphic_id}" '
            f'data-labeled-graphic data-media-width="{esc(media_width)}" data-marker-index="-1">'
            '<figure class="labeled-graphic__figure">'
            f'<img class="labeled-graphic__image" src="{esc(media["path"])}" alt="{esc(media.get("alt") or ui(ui_labels, "labeled_graphic", "Labeled graphic"))}"{size_attrs} loading="lazy">'
            f'<ol class="labeled-graphic__items">{"".join(items)}</ol></figure></div>'
        )
    if block_type == "knowledge_check":
        qid = f'q-{lesson_id}-{block.get("id")}'
        question_type = re.sub(
            r"[^a-z0-9]+", "_", str(block.get("question_type") or "multiple_choice").casefold()
        ).strip("_")
        question_id = f'{qid}-question'
        if question_type in {"multiple_choice", "multiple_response"}:
            input_type = "checkbox" if question_type == "multiple_response" else "radio"
            role = "group" if input_type == "checkbox" else "radiogroup"
            choices = "".join(
                f'<label class="quiz-choice"><input type="{input_type}" name="{qid}" value="{index}" data-correct="{str(bool(choice.get("correct"))).lower()}">'
                '<span class="quiz-choice__indicator" aria-hidden="true">'
                '<svg class="quiz-choice__dot" viewBox="0 0 10 10" focusable="false"><circle cx="5" cy="5" r="5"/></svg>'
                '<svg class="quiz-choice__check" viewBox="0 0 11 8" focusable="false"><path d="M9.6 0 11 1.3 3.9 8 0 4.3 1.4 3l2.6 2.4L9.6 0Z"/></svg>'
                '<svg class="quiz-choice__x" viewBox="0 0 10 10" focusable="false"><path d="M5 4.17 9.17 0 10 .83 5.83 5 10 9.17 9.17 10 5 5.83.83 10 0 9.17 4.17 5 0 .83.83 0Z"/></svg>'
                '</span>'
                f'<span class="quiz-choice__text">{choice.get("text_html") or ""}</span>'
                '<span class="visually-hidden" data-quiz-choice-result></span></label>'
                for index, choice in enumerate(block.get("choices", []), start=1)
            )
            answer_controls = (
                f'<div class="quiz-choices" role="{role}" aria-labelledby="{question_id}">{choices}</div>'
            )
        elif question_type == "fill_in_the_blank":
            accepted_answers = [str(value) for value in block.get("accepted_answers", [])]
            accepted = esc(json.dumps(accepted_answers, ensure_ascii=False))
            accepted_id = f'{qid}-accepted'
            accepted_label = esc(ui(ui_labels, "acceptable_responses", "Acceptable responses"))
            accepted_text = ", ".join(esc(value) for value in accepted_answers)
            answer_controls = (
                '<div class="quiz-fillin">'
                f'<input type="text" data-quiz-fillin data-accepted-answers="{accepted}" '
                f'aria-labelledby="{question_id}" aria-describedby="{accepted_id}" '
                f'placeholder="{esc(ui(ui_labels, "type_answer", "Type your answer here"))}">'
                f'<div class="quiz-fillin__accepted" id="{accepted_id}" data-quiz-accepted hidden>'
                f'{accepted_label}: {accepted_text}</div>'
                '</div>'
            )
        elif question_type == "matching":
            pairs = list(block.get("pairs", []))
            left_items = []
            right_items = []
            result_items = []
            indexed_pairs = list(enumerate(pairs, start=1))
            # Rise deliberately shuffles the draggable source pieces while keeping
            # the target column in authored order. A deterministic rotation keeps
            # the interaction reproducible without presenting an already-solved row.
            shuffled_pairs = indexed_pairs[-1:] + indexed_pairs[:-1]
            grip_path = (
                "M64 128a32 32 0 1 0 0-64 32 32 0 1 0 0 64zm0 160a32 32 0 1 0 0-64 "
                "32 32 0 1 0 0 64zM96 416a32 32 0 1 0-64 0 32 32 0 1 0 64 0zm96-288a32 "
                "32 0 1 0 0-64 32 32 0 1 0 0 64zm32 128a32 32 0 1 0-64 0 32 32 0 1 0 64 "
                "0zM192 448a32 32 0 1 0 0-64 32 32 0 1 0 0 64z"
            )
            for display_order, (index, pair) in enumerate(shuffled_pairs, start=1):
                left_items.append(
                    '<li class="quiz-matching__item quiz-matching__item--source" role="listitem" data-match-drag-source>'
                    f'<button class="quiz-match-piece quiz-match-piece--source" type="button" '
                    f'data-match-side="left" data-match-key="{index}" data-match-order="{display_order}" aria-pressed="false">'
                    '<span class="quiz-match-piece__decoration quiz-match-piece__decoration--grip" aria-hidden="true">'
                    f'<svg viewBox="0 0 256 512" focusable="false"><path fill="currentColor" d="{grip_path}"/></svg></span>'
                    f'<span class="quiz-match-piece__content">{pair.get("prompt_html") or ""}</span>'
                    '<span class="visually-hidden" data-match-announcement></span>'
                    '<span class="visually-hidden"> Selectable item</span></button></li>'
                )
            for index, pair in indexed_pairs:
                right_items.append(
                    '<li class="quiz-matching__item quiz-matching__item--target" role="listitem" data-match-drop-zone>'
                    f'<button class="quiz-match-piece quiz-match-piece--target" type="button" '
                    f'data-match-side="right" data-match-key="{index}" aria-pressed="false">'
                    '<span class="quiz-match-piece__jigsaw" aria-hidden="true"></span>'
                    f'<span class="quiz-match-piece__content">{pair.get("match_html") or ""}</span>'
                    '<span class="quiz-match-piece__decoration quiz-match-piece__decoration--target" aria-hidden="true"></span>'
                    '<span class="visually-hidden" data-match-announcement></span>'
                    '<span class="visually-hidden"> Selectable item</span></button></li>'
                )
                result_items.append(
                    f'<li class="quiz-matching-result" data-match-result-key="{index}">'
                    '<div class="quiz-matching-result__pieces">'
                    '<div class="quiz-matching-result__piece quiz-matching-result__piece--source">'
                    '<span class="quiz-matching-result__content" data-match-result-left></span>'
                    '<span class="quiz-matching-result__socket" aria-hidden="true"></span></div>'
                    '<div class="quiz-matching-result__piece quiz-matching-result__piece--target">'
                    '<span class="quiz-matching-result__tab" aria-hidden="true"></span>'
                    f'<span class="quiz-matching-result__content">{pair.get("match_html") or ""}</span></div></div>'
                    '<div class="quiz-matching-result__feedback quiz-matching-result__feedback--correct">'
                    '<span class="quiz-matching-result__icon" aria-hidden="true">'
                    '<svg viewBox="0 0 11 8" focusable="false"><path fill="currentColor" d="M9.6 0 11 1.3 3.9 8 0 4.3 1.4 3l2.6 2.4L9.6 0Z"/></svg></span>'
                    f'<span>{esc(ui(ui_labels, "correct", "Correct"))}.</span></div>'
                    '<div class="quiz-matching-result__feedback quiz-matching-result__feedback--incorrect">'
                    '<span class="quiz-matching-result__icon" aria-hidden="true">'
                    '<svg viewBox="0 0 10 10" focusable="false"><path fill="currentColor" d="M5 4.17 9.17 0 10 .83 5.83 5 10 9.17 9.17 10 5 5.83.83 10 0 9.17 4.17 5 0 .83.83 0Z"/></svg></span>'
                    f'<span><span>{esc(ui(ui_labels, "incorrect", "Incorrect"))}.</span> '
                    f'<span class="quiz-matching-result__correction">Correct: <span>{pair.get("prompt_html") or ""}</span></span></span>'
                    '</div></li>'
                )
            answer_controls = (
                '<div class="quiz-matching" aria-labelledby="' + question_id + '">'
                '<ul class="quiz-matching__column quiz-matching__column--source" role="list" aria-label="Matching column 1">'
                + "".join(left_items) + '</ul>'
                '<ul class="quiz-matching__column quiz-matching__column--target" role="list" aria-label="Matching column 2">'
                + "".join(right_items) + '</ul></div>'
                '<ul class="quiz-matching-results" aria-label="Matching results" hidden>'
                + "".join(result_items) + '</ul>'
            )
        else:
            answer_controls = ""
        return (
            f'<div class="quiz-card" data-question-id="{qid}" data-question-type="{question_type}">'
            f'<div class="quiz-question" id="{question_id}">{block.get("question_html") or ""}</div>'
            f'{answer_controls}<div class="quiz-actions">'
            f'<button class="quiz-submit" type="button">{esc(ui(ui_labels, "submit", "SUBMIT"))}</button></div>'
            '<div class="quiz-feedback quiz-feedback--correct"><span class="quiz-feedback__icon" aria-hidden="true">'
            f'<svg class="quiz-feedback__glyph" viewBox="0 0 1024 1024" focusable="false"><g transform="translate(0 1024) scale(1 -1)"><path fill="currentColor" d="{SCROLLING_FEEDBACK_CORRECT_PATH}"/></g></svg></span>'
            f'<strong class="quiz-feedback__label">{esc(ui(ui_labels, "correct", "Correct"))}</strong><div class="quiz-feedback__text">{block.get("feedback_correct_html") or ui(ui_labels, "correct", "Correct") + "."}</div></div>'
            '<div class="quiz-feedback quiz-feedback--incorrect"><span class="quiz-feedback__icon" aria-hidden="true">'
            f'<svg class="quiz-feedback__glyph" viewBox="0 0 1024 1024" focusable="false"><g transform="translate(0 1024) scale(1 -1)"><path fill="currentColor" d="{SCROLLING_FEEDBACK_INCORRECT_PATH}"/></g></svg></span>'
            f'<strong class="quiz-feedback__label">{esc(ui(ui_labels, "incorrect", "Incorrect"))}</strong><div class="quiz-feedback__text">{block.get("feedback_incorrect_html") or "Review the lesson and try again."}</div></div>'
            '<div class="quiz-retake-wrap" hidden><button class="quiz-retake" type="button"><span class="quiz-retake__content">'
            f'<span class="quiz-retake__icon" aria-hidden="true"><svg viewBox="0 0 512 512" focusable="false"><path fill="currentColor" d="{SCROLLING_RETAKE_PATH}"/></svg></span>'
            f'{esc(ui(ui_labels, "take_again", "TAKE AGAIN"))}</span></button></div></div>'
        )
    content = block.get("content")
    return f'<pre>{esc(json.dumps(content, indent=2, ensure_ascii=False))}</pre>' if content else ""


def padding_pixels(style: dict, key: str, custom_key: str) -> float | None:
    custom = style.get(custom_key)
    if isinstance(custom, (int, float)):
        return max(0, min(float(custom), 240))
    value = style.get(key)
    if isinstance(value, (int, float)):
        return max(0, min(float(value) * 10, 240))
    return None


def block_style_attr(block: dict) -> str:
    style = block.get("style") if isinstance(block.get("style"), dict) else {}
    rules = []
    color = str(style.get("background_color") or "")
    if color and re.fullmatch(r"#[0-9a-fA-F]{3,8}", color):
        rules.extend([f"background-color:{color}", f"color:{contrasting_text(color)}"])
    background_media = style.get("background_media") if isinstance(style.get("background_media"), dict) else {}
    if background_media.get("path"):
        path = str(background_media["path"]).replace('"', "%22")
        opacity = style.get("background_overlay_opacity")
        overlay = None
        if isinstance(opacity, (int, float)):
            overlay = rgba_color(str(style.get("background_overlay_color") or "#000000"), max(0, min(float(opacity), 1)))
        image_layers = f'linear-gradient(0deg,{overlay},{overlay}),url("{path}")' if overlay else f'url("{path}")'
        position = str(style.get("background_position") or "center").casefold()
        size = str(style.get("background_size") or "cover").casefold()
        if position not in {"center", "top", "bottom", "left", "right"}:
            position = "center"
        if size not in {"cover", "contain", "auto"}:
            size = "cover"
        rules.extend([f"background-image:{image_layers}", f"background-position:{position}", f"background-size:{size}"])
    foreground = str(style.get("foreground_color") or "")
    if foreground and re.fullmatch(r"#[0-9a-fA-F]{3,8}", foreground):
        rules.append(f"color:{foreground}")
    button_color = str(style.get("button_color") or "")
    if button_color and re.fullmatch(r"#[0-9a-fA-F]{3,8}", button_color):
        rules.extend([
            f"--block-button-color:{button_color}",
            f"--block-button-text-color:{contrasting_text(button_color)}",
        ])
    top = padding_pixels(style, "padding_top", "custom_padding_top")
    bottom = padding_pixels(style, "padding_bottom", "custom_padding_bottom")
    if top is not None:
        rules.append(f"padding-top:{top:g}px")
    if bottom is not None:
        rules.append(f"padding-bottom:{bottom:g}px")
    return f' style="{esc(";".join(rules))}"' if rules else ""


def block_classes(block: dict) -> str:
    block_type = str(block.get("type") or "unknown")
    variant = re.sub(r"[^a-z0-9_-]+", "-", str(block.get("variant") or "").casefold()).strip("-").replace("_", "-")
    style = block.get("style") if isinstance(block.get("style"), dict) else {}
    classes = ["block", f"block--{block_type}"]
    if variant:
        classes.append(f"block--variant-{variant}")
    position = re.sub(r"[^a-z]+", "", str(style.get("image_position") or "").casefold())
    if block_type == "image" and variant == "text-aside" and position not in {"left", "right"}:
        position = "left"
    size = re.sub(r"[^a-z]+", "", str(style.get("image_size") or "").casefold())
    if position:
        classes.append(f"block--image-{position}")
    if size:
        classes.append(f"block--image-size-{size}")
    if style.get("attached_to_next"):
        classes.append("block--attached-next")
    background_media = style.get("background_media") if isinstance(style.get("background_media"), dict) else {}
    if background_media.get("path"):
        classes.append("block--background-image")
    if block_type == "buttons":
        alignment = re.sub(r"[^a-z]+", "", str(style.get("button_alignment") or "right").casefold())
        classes.append(f"block--button-{alignment if alignment in {'left', 'right'} else 'right'}")
    background_color = str(style.get("background_color") or "")
    if block_type == "accordion":
        classes.append(
            "block--surface-dark"
            if background_color and contrasting_text(background_color) == "#ffffff"
            else "block--surface-light"
        )
    if block_type == "list" and style.get("entrance_animation", True):
        classes.append("scroll-animation-group")
    return " ".join(classes)


def render_lesson(
    lesson: dict,
    index: int,
    total: int,
    next_title: str = "",
    previous_title: str = "",
    ui_labels: dict | None = None,
) -> str:
    gate_count = sum(1 for block in lesson.get("blocks", []) if (block.get("type") or "unknown") == "continue")
    has_exit = any(
        str(item.get("type") or "").casefold() == "exit-course"
        for block in lesson.get("blocks", []) if block.get("type") == "buttons"
        for item in block.get("buttons", [])
    )
    gate_level = 0
    blocks = []
    lesson_blocks = lesson.get("blocks", [])
    for block_index, block in enumerate(lesson_blocks, start=1):
        block_type = block.get("type") or "unknown"
        gate_attr = f' data-gate-level="{gate_level}"'
        gate_index = f' data-gate-index="{gate_level}"' if block_type == "continue" else ""
        final_gate = ' data-final-gate="true"' if block_type == "continue" and gate_level == gate_count - 1 else ""
        progress_attr = f' data-progress-index="{block_index}" data-progress-mode="{"action" if block_type == "continue" else "view"}"'
        content = render_block(block, lesson.get("id") or index, ui_labels)
        blocks.append(
            f'<section class="{esc(block_classes(block))}"{gate_attr}{gate_index}{final_gate}{progress_attr}{block_style_attr(block)}>'
            f'<div class="block__container"><div class="block__content">{content}</div></div></section>'
        )
        if block_type == "continue":
            gate_level += 1
    if index < total:
        completed_navigation = (
            '<div class="completed-lesson-nav" hidden>'
            f'<button class="completed-lesson-nav__link" type="button" data-next-lesson="{index + 1}">'
            f'<span>{esc(ui(ui_labels, "lesson_next", "Lesson {number} - {title}", number=index + 1, title=next_title or ui(ui_labels, "lesson", "Lesson {number}", number=index + 1)))}</span>'
            '<svg aria-hidden="true" viewBox="0 0 15 16" focusable="false"><path d="M2 8L7.65685 13.6569L13.3137 8" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>'
            '</button></div>'
        )
    else:
        completed_navigation = ''
    previous_label = (
        ui(ui_labels, "home", "Home")
        if index == 1
        else ui(
            ui_labels,
            "lesson_previous",
            "Lesson {number} - {title}",
            number=index - 1,
            title=previous_title or ui(ui_labels, "lesson", "Lesson {number}", number=index - 1),
        )
    )
    previous_navigation = (
        '<div class="previous-lesson-nav">'
        f'<button class="previous-lesson-nav__link" type="button" data-lesson-target="{index - 1}">'
        '<svg aria-hidden="true" viewBox="0 0 15 16" focusable="false"><path d="M2 8L7.65685 2.34315L13.3137 8" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>'
        f'<span>{esc(previous_label)}</span>'
        '</button></div>'
    )
    return f'''
<article class="lesson" id="lesson-{index}" data-lesson-id="{index}" data-lesson-slug="{esc(lesson.get("slug") or f"lesson-{index}")}" data-gate-count="{gate_level}" data-progress-total="{len(lesson_blocks)}" data-has-exit="{str(has_exit).lower()}">
  {previous_navigation}
  <header class="lesson__hero"><div class="lesson__hero-inner">
    <p class="lesson__number">{esc(ui(ui_labels, "lesson_of", "Lesson {current} of {total}", current=index, total=total))}</p>
    <h2>{esc(lesson.get("title") or ui(ui_labels, "lesson", "Lesson {number}", number=index))}</h2>
    <span class="lesson__rule" aria-hidden="true"></span>
    <div class="lesson__description">{lesson.get("description_html") or ""}</div>
  </div></header>
  <div class="lesson-read-progress lesson-read-progress--inline" aria-hidden="true"><div class="lesson-read-progress__progress"><div class="lesson-read-progress__track"><div class="lesson-read-progress__indicator"></div></div></div></div>
  <div class="lesson__body">{"".join(blocks)}</div>
  {completed_navigation}
</article>'''


def searchable_lesson_text(lesson: dict) -> str:
    parts: list[str] = []
    visible_text_keys = {
        "title", "label", "tagline", "heading_html", "body_html", "description_html",
        "caption_html", "quote_html", "attribution_html", "question_html", "text_html",
        "feedback_correct_html", "feedback_incorrect_html", "complete_hint", "items_html",
    }

    def walk(value: object, key: str = "") -> None:
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(child, str(child_key))
        elif isinstance(value, list):
            for child in value:
                walk(child, key)
        elif isinstance(value, str) and key in visible_text_keys:
            text = html.unescape(re.sub(r"<[^>]+>", " ", value))
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                parts.append(text)

    walk(lesson)
    return " ".join(parts).casefold()


def render_scrolling_course(course: dict, resource_root: Path | None = None) -> str:
    course = hydrate_caption_cues(course, resource_root)
    css = (TEMPLATE_DIR / "scrolling_styles.css").read_text(encoding="utf-8")
    brand = course.get("brand") or {}
    theme = course.get("theme") or {}
    scrolling = course.get("scrolling") or {}
    ui_labels = course.get("ui_labels") if isinstance(course.get("ui_labels"), dict) else {}
    accent = safe_color(brand.get("primary_color") or theme.get("accent_color"), "#8cc53f")
    accent_dark = safe_color(brand.get("primary_color_dark"), "#6fa030")
    header_style = str(theme.get("lesson_header_style") or "ACCENT").upper()
    if header_style == "CUSTOM":
        header_background = safe_color(theme.get("lesson_header_color"), accent)
    elif header_style == "DARK":
        header_background = "#1c1c1c"
    elif header_style == "LIGHT":
        header_background = "#ffffff"
    else:
        header_background = accent
    header_text = contrasting_text(header_background)
    families = theme.get("font_families") if isinstance(theme.get("font_families"), dict) else {}
    corner_style = str(theme.get("corner_style") or "Rounded").strip().casefold()
    process_step_badge_radius = "10px" if "round" in corner_style else "0px"
    heading_family = families.get("heading") or "Arial"
    body_family = families.get("body") or heading_family
    ui_family = families.get("ui") or body_family
    cover = theme.get("cover_image") or ""
    dimensions = theme.get("cover_image_dimensions") if isinstance(theme.get("cover_image_dimensions"), dict) else {}
    cover_width = dimensions.get("originalWidth") or dimensions.get("width") or 1680
    cover_height = dimensions.get("originalHeight") or dimensions.get("height") or 737
    try:
        cover_width = max(1, float(cover_width))
        cover_height = max(1, float(cover_height))
    except (TypeError, ValueError):
        cover_width, cover_height = 1680, 737
    overlay = theme.get("cover_overlay_opacity", 0)
    try:
        overlay = float(overlay)
    except (TypeError, ValueError):
        overlay = 0
    if overlay > 1:
        overlay /= 100
    overlay = min(max(overlay, 0), 1)
    cover_style = (
        f' style="--cover-image:url(\'{esc(cover)}\');--cover-overlay:rgba(0,0,0,{overlay:g})"'
        if cover else ""
    )
    lessons = course.get("lessons") or []
    search_enabled = bool(scrolling.get("show_search", True))
    show_lesson_count = bool(scrolling.get("show_lesson_count", True))
    show_cover_lesson_list = bool(scrolling.get("show_cover_lesson_list", True))
    directional_transitions = str(scrolling.get("lesson_transition") or "directional_vertical").casefold() != "none"
    navigation_restricted = bool(theme.get("navigation_restricted", False))
    lesson_icon = (
        '<svg class="lesson-nav__handle" aria-hidden="true" viewBox="0 0 18 12" focusable="false">'
        '<path d="M.667 1A.833.833 0 0 1 1.5.167H14a.833.833 0 1 1 0 1.666H1.5A.833.833 0 0 1 .667 1Zm0 5A.833.833 0 0 1 1.5 5.167h15a.833.833 0 1 1 0 1.666h-15A.833.833 0 0 1 .667 6Zm0 5a.833.833 0 0 1 .833-.833h9.167a.833.833 0 1 1 0 1.666H1.5A.833.833 0 0 1 .667 11Z" fill="currentColor"/>'
        '</svg>'
    )
    lesson_status_icon = (
        '<svg class="lesson-nav__status-icon" aria-hidden="true" viewBox="0 0 16 16" focusable="false">'
        '<circle class="lesson-nav__status-track" cx="8" cy="8" r="7" fill="transparent" stroke-width="2" transform="rotate(-89.9 8 8)"/>'
        '<circle class="lesson-nav__status-runner" cx="8" cy="8" r="7" fill="transparent" stroke-width="2" transform="rotate(-89.9 8 8)"/>'
        '<path class="lesson-nav__status-pass" d="M11.3227 6.65905C11.6133 6.37599 11.6347 5.89413 11.3705 5.58277C11.1063 5.27141 10.6566 5.24847 10.366 5.53152L6.93323 8.87512L5.6338 7.60944C5.3432 7.32639 4.89345 7.34933 4.62927 7.66069C4.36509 7.97205 4.38651 8.45391 4.67711 8.73697L6.45488 10.4686C6.72611 10.7328 7.14034 10.7328 7.41157 10.4686L11.3227 6.65905Z"/>'
        '</svg>'
    )
    search_icon = (
        '<svg aria-hidden="true" viewBox="0 0 12 12" focusable="false">'
        '<path fill="currentColor" fill-rule="evenodd" d="M5.325 9.018C3.225 9.018 1.5 7.379 1.5 5.292S3.225 1.49 5.325 1.49 9.15 3.205 9.15 5.292 7.425 9.018 5.325 9.018Zm4.2-.596a5.25 5.25 0 1 0-1.05 1.118l2.25 2.236a.743.743 0 0 0 1.05 0 .735.735 0 0 0 0-1.043l-2.25-2.31Z"/>'
        '</svg>'
    )
    close_icon = (
        '<svg aria-hidden="true" viewBox="0 0 10 10" focusable="false">'
        '<path fill="currentColor" d="M9.786 9.786a.707.707 0 0 1-1 0L5 6 1.214 9.786a.707.707 0 0 1-1-1L4 5 .214 1.214a.707.707 0 0 1 1-1L5 4 8.786.214a.707.707 0 0 1 1 1L6 5l3.786 3.786a.707.707 0 0 1 0 1Z"/>'
        '</svg>'
    )
    def initial_lock_attributes(index: int) -> str:
        return ' disabled aria-disabled="true"' if navigation_restricted and index > 1 else ""

    nav = "".join(
        f'<button class="lesson-nav__item" type="button" data-lesson-target="{index}" data-search-text="{esc(searchable_lesson_text(lesson))}"'
        f'{initial_lock_attributes(index)}>'
        f'{lesson_icon}'
        f'<span class="lesson-nav__title">{esc(lesson.get("title") or ui(ui_labels, "lesson", "Lesson {number}", number=index))}</span>'
        f'<span class="lesson-nav__status" aria-label="{esc(ui(ui_labels, "unstarted", "Unstarted"))}">{lesson_status_icon}</span></button>'
        for index, lesson in enumerate(lessons, start=1)
    )
    search_results = "".join(
        f'<button class="sidebar-search-result" type="button" data-lesson-target="{index}" data-search-text="{esc(searchable_lesson_text(lesson))}" hidden'
        f'{initial_lock_attributes(index)}>'
        f'{lesson_icon}<span class="sidebar-search-result__title">{esc(lesson.get("title") or ui(ui_labels, "lesson", "Lesson {number}", number=index))}</span>'
        '<span class="sidebar-search-result__count"></span></button>'
        for index, lesson in enumerate(lessons, start=1)
    )
    cover_nav = "".join(
        f'<button class="course-cover__lesson-item" type="button" data-lesson-target="{index}"'
        f'{initial_lock_attributes(index)}>'
        '<span class="course-cover__lesson-handle" aria-hidden="true"><i></i><i></i><i></i></span>'
        f'<span class="course-cover__lesson-title">{esc(lesson.get("title") or ui(ui_labels, "lesson", "Lesson {number}", number=index))}</span>'
        f'<span class="course-cover__lesson-status" aria-label="{esc(ui(ui_labels, "unstarted", "Unstarted"))}"></span></button>'
        for index, lesson in enumerate(lessons, start=1)
    )
    lesson_html = "".join(
        render_lesson(
            lesson,
            index,
            len(lessons),
            (lessons[index].get("title") or ui(ui_labels, "lesson", "Lesson {number}", number=index + 1)) if index < len(lessons) else "",
            (lessons[index - 2].get("title") or ui(ui_labels, "lesson", "Lesson {number}", number=index - 1)) if index > 1 else "",
            ui_labels,
        )
        for index, lesson in enumerate(lessons, start=1)
    )
    course_title_json = json.dumps(course.get("course_title") or "OCP Academy Course")
    ui_labels_json = json.dumps(ui_labels, ensure_ascii=False).replace("</", "<\\/")
    initial_nav_class = "" if bool(scrolling.get("toc_initially_open", True)) else " nav-closed"
    theme_classes = ["is-cover"]
    if theme.get("hide_lesson_headers"):
        theme_classes.append("hide-lesson-headers")
    if not theme.get("animate_block_entrance", True):
        theme_classes.append("reduce-block-motion")
    if initial_nav_class:
        theme_classes.append("nav-closed")
    script = r'''
(function() {
  'use strict';
  var lessonCount = __LESSON_COUNT__;
  var directionalTransitions = __DIRECTIONAL_TRANSITIONS__;
  var navigationRestricted = __NAVIGATION_RESTRICTED__;
  var uiLabels = __UI_LABELS__;
  var activeLesson = 0;
  function uiText(key, fallback, values) {
    var text = String(uiLabels[key] || fallback);
    Object.keys(values || {}).forEach(function(name) {
      text = text.split('{' + name + '}').join(String(values[name]));
    });
    return text;
  }
  var state = {
    currentLesson: 0,
    gates: {},
    completedLessons: [],
    quizzes: {},
    viewedBlocks: {},
    videoPreferences: { playbackRate: 1, captionLanguage: "off" }
  };

  SCORM.init();
  var existingStatus = SCORM.getStatus();
  if (existingStatus !== 'completed' && existingStatus !== 'passed') SCORM.setIncomplete();
  try {
    var saved = JSON.parse(SCORM.getSuspendData() || '{}');
    if (saved && saved.scrolling) state = Object.assign(state, saved.scrolling);
  } catch (e) {}
  if (!state.viewedBlocks || typeof state.viewedBlocks !== 'object') state.viewedBlocks = {};
  if (!state.videoPreferences || typeof state.videoPreferences !== 'object') {
    state.videoPreferences = { playbackRate: 1, captionLanguage: "off" };
  }

  function saveState() {
    SCORM.setSuspendData(JSON.stringify({ scrolling: state }));
    SCORM.setLocation(activeLesson ? 'lesson-' + activeLesson : 'cover');
  }
  function completed(id) { return state.completedLessons.indexOf(id) !== -1; }
  function lessonUnlocked(id) {
    id = Number(id || 0);
    return !navigationRestricted || id <= 1 || completed(id - 1);
  }
  function markComplete(id) {
    if (!completed(id)) state.completedLessons.push(id);
    var lesson = document.getElementById('lesson-' + id);
    if (lesson) state.viewedBlocks[id] = Number(lesson.dataset.progressTotal || 0);
    if (id === activeLesson) syncLessonReadProgress();
    if (state.completedLessons.length >= lessonCount) SCORM.setCompleted();
  }
  function clearMatchingPiece(piece) {
    if (!piece) return;
    piece.classList.remove('is-pending', 'is-paired', 'is-drop-target');
    piece.setAttribute('aria-pressed', 'false');
    var item = piece.closest('.quiz-matching__item');
    if (item) {
      item.classList.remove('is-dragging', 'is-drop-target');
      item.style.removeProperty('transform');
    }
    var announcement = piece.querySelector('[data-match-announcement]');
    if (announcement) announcement.textContent = '';
    delete piece.dataset.pairedWith;
  }
  function syncMatchingSourceRows(quiz) {
    if (!quiz) return;
    var sourceColumn = quiz.querySelector('.quiz-matching__column--source');
    if (!sourceColumn) return;
    var sourceItems = Array.from(sourceColumn.querySelectorAll('.quiz-matching__item--source'));
    var targets = Array.from(quiz.querySelectorAll('[data-match-side="right"]'));
    var placed = new Set();
    var rows = targets.map(function(target) {
      if (!target.dataset.pairedWith) return null;
      var source = quiz.querySelector('[data-match-side="left"][data-match-key="' + target.dataset.pairedWith + '"]');
      var sourceItem = source ? source.closest('.quiz-matching__item--source') : null;
      if (sourceItem) placed.add(sourceItem);
      return sourceItem;
    });
    var remaining = sourceItems.filter(function(sourceItem) { return !placed.has(sourceItem); });
    var remainingIndex = 0;
    rows.forEach(function(source, index) {
      if (!source) rows[index] = remaining[remainingIndex++];
    });
    rows.forEach(function(source) { if (source) sourceColumn.appendChild(source); });
  }
  function restoreMatchingSourceRows(quiz) {
    if (!quiz) return;
    var sourceColumn = quiz.querySelector('.quiz-matching__column--source');
    if (!sourceColumn) return;
    Array.from(sourceColumn.querySelectorAll('.quiz-matching__item--source'))
      .sort(function(a, b) {
        var aPiece = a.querySelector('[data-match-side="left"]');
        var bPiece = b.querySelector('[data-match-side="left"]');
        return Number((aPiece && aPiece.dataset.matchOrder) || 0) - Number((bPiece && bPiece.dataset.matchOrder) || 0);
      })
      .forEach(function(sourceItem) { sourceColumn.appendChild(sourceItem); });
  }
  function syncMatchingPieceHeights(quiz) {
    if (!quiz) return;
    var matching = quiz.querySelector('.quiz-matching');
    if (!matching || matching.hidden || !matching.getClientRects().length) return;
    var pieces = Array.from(matching.querySelectorAll('.quiz-match-piece'));
    if (!pieces.length) return;
    pieces.forEach(function(piece) { piece.style.removeProperty('height'); });
    var resolvedHeight = 0;
    pieces.forEach(function(piece) {
      var content = piece.querySelector('.quiz-match-piece__content');
      var style = window.getComputedStyle(piece);
      var verticalChrome = parseFloat(style.paddingTop || 0) + parseFloat(style.paddingBottom || 0)
        + parseFloat(style.borderTopWidth || 0) + parseFloat(style.borderBottomWidth || 0);
      var contentHeight = content ? content.scrollHeight : piece.scrollHeight - verticalChrome;
      resolvedHeight = Math.max(resolvedHeight, parseFloat(style.minHeight || 0), contentHeight + verticalChrome);
    });
    var height = Math.ceil(resolvedHeight) + 'px';
    pieces.forEach(function(piece) { piece.style.height = height; });
  }
  function pairMatchingPieces(quiz, leftKey, rightKey) {
    if (!quiz || quiz.classList.contains('is-submitted')) return;
    leftKey = String(leftKey || '');
    rightKey = String(rightKey || '');
    var left = quiz.querySelector('[data-match-side="left"][data-match-key="' + leftKey + '"]');
    var right = quiz.querySelector('[data-match-side="right"][data-match-key="' + rightKey + '"]');
    if (!left || !right) return;
    var oldRight = left.dataset.pairedWith
      ? quiz.querySelector('[data-match-side="right"][data-match-key="' + left.dataset.pairedWith + '"]')
      : null;
    var oldLeft = right.dataset.pairedWith
      ? quiz.querySelector('[data-match-side="left"][data-match-key="' + right.dataset.pairedWith + '"]')
      : null;
    [left, right, oldLeft, oldRight].forEach(clearMatchingPiece);
    left.dataset.pairedWith = rightKey;
    right.dataset.pairedWith = leftKey;
    left.classList.add('is-paired');
    right.classList.add('is-paired');
    left.setAttribute('aria-pressed', 'true');
    right.setAttribute('aria-pressed', 'true');
    var leftText = (left.querySelector('.quiz-match-piece__content') || left).textContent.trim();
    var rightText = (right.querySelector('.quiz-match-piece__content') || right).textContent.trim();
    var leftAnnouncement = left.querySelector('[data-match-announcement]');
    var rightAnnouncement = right.querySelector('[data-match-announcement]');
    if (leftAnnouncement) leftAnnouncement.textContent = ' Matched with ' + rightText + '.';
    if (rightAnnouncement) rightAnnouncement.textContent = ' Matched with ' + leftText + '.';
    syncMatchingSourceRows(quiz);
    delete quiz.dataset.matchPendingLeft;
    delete quiz.dataset.matchPendingRight;
  }
  function showQuizResult(quiz, result) {
    if (!quiz || !result) return;
    var questionType = String(quiz.dataset.questionType || 'multiple_choice');
    quiz.classList.add('is-submitted');
    if (questionType === 'multiple_choice' || questionType === 'multiple_response') {
      var selectedValues = Array.isArray(result.selected)
        ? result.selected.map(String)
        : [String(result.selected || '')];
      quiz.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(function(input) {
        input.checked = selectedValues.indexOf(input.value) !== -1;
        input.disabled = true;
        var choice = input.closest('.quiz-choice');
        if (choice) {
          choice.classList.toggle('is-selected', input.checked);
          choice.classList.toggle('is-correct', input.dataset.correct === 'true');
          choice.classList.toggle('is-incorrect', input.dataset.correct !== 'true');
          var choiceResult = choice.querySelector('[data-quiz-choice-result]');
          if (choiceResult) {
            choiceResult.textContent = input.dataset.correct === 'true'
              ? (input.checked ? ' Correctly selected.' : ' Correctly unselected.')
              : (input.checked ? ' Incorrectly selected.' : ' Incorrectly unselected.');
          }
        }
      });
    } else if (questionType === 'fill_in_the_blank') {
      var fillin = quiz.querySelector('[data-quiz-fillin]');
      if (fillin) {
        fillin.value = String(result.answer || '');
        fillin.disabled = true;
        fillin.classList.toggle('is-correct', !!result.correct);
        fillin.classList.toggle('is-incorrect', !result.correct);
      }
      var acceptedAnswers = quiz.querySelector('[data-quiz-accepted]');
      if (acceptedAnswers) acceptedAnswers.hidden = false;
    } else if (questionType === 'matching') {
      var pairs = result.pairs && typeof result.pairs === 'object' ? result.pairs : {};
      quiz.querySelectorAll('.quiz-match-piece').forEach(function(choice) {
        choice.disabled = true;
        choice.classList.remove('is-pending', 'is-dragging', 'is-drop-target');
      });
      quiz.querySelectorAll('.quiz-matching__item').forEach(function(item) {
        item.classList.remove('is-dragging', 'is-drop-target');
        item.style.removeProperty('transform');
      });
      var matching = quiz.querySelector('.quiz-matching');
      var results = quiz.querySelector('.quiz-matching-results');
      if (matching) matching.hidden = true;
      if (results) results.hidden = false;
      quiz.querySelectorAll('.quiz-matching-result').forEach(function(row) {
        var rightKey = String(row.dataset.matchResultKey || '');
        var leftKey = Object.keys(pairs).find(function(key) { return String(pairs[key]) === rightKey; }) || '';
        var source = quiz.querySelector('[data-match-side="left"][data-match-key="' + leftKey + '"]');
        var sourceContent = source ? source.querySelector('.quiz-match-piece__content') : null;
        var resultContent = row.querySelector('[data-match-result-left]');
        if (resultContent) resultContent.innerHTML = sourceContent ? sourceContent.innerHTML : '';
        var pairCorrect = leftKey === rightKey;
        row.classList.toggle('is-correct', pairCorrect);
        row.classList.toggle('is-incorrect', !pairCorrect);
      });
    }
    var actions = quiz.querySelector('.quiz-actions');
    if (actions) {
      actions.classList.add('is-proceed');
      var submit = actions.querySelector('.quiz-submit');
      if (submit) submit.hidden = true;
    }
    quiz.querySelectorAll('.quiz-feedback').forEach(function(item) {
      item.classList.remove('is-visible', 'is-correct', 'is-incorrect');
    });
    var feedback = quiz.querySelector(result.correct ? '.quiz-feedback--correct' : '.quiz-feedback--incorrect');
    if (feedback) feedback.classList.add('is-visible', result.correct ? 'is-correct' : 'is-incorrect');
    var retake = quiz.querySelector('.quiz-retake-wrap');
    if (retake) {
      retake.hidden = false;
      var retakeButton = retake.querySelector('.quiz-retake');
      if (retakeButton) retakeButton.hidden = !!result.correct;
    }
  }
  function resetQuiz(quiz) {
    if (!quiz) return;
    quiz.classList.remove('is-submitted');
    quiz.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(function(input) {
      input.checked = false;
      input.disabled = false;
      var choice = input.closest('.quiz-choice');
      if (choice) {
        choice.classList.remove('is-selected', 'is-correct', 'is-incorrect');
        var choiceResult = choice.querySelector('[data-quiz-choice-result]');
        if (choiceResult) choiceResult.textContent = '';
      }
    });
    var fillin = quiz.querySelector('[data-quiz-fillin]');
    if (fillin) {
      fillin.value = '';
      fillin.disabled = false;
      fillin.classList.remove('is-correct', 'is-incorrect');
    }
    var acceptedAnswers = quiz.querySelector('[data-quiz-accepted]');
    if (acceptedAnswers) acceptedAnswers.hidden = true;
    quiz.querySelectorAll('.quiz-match-piece').forEach(function(choice) {
      choice.disabled = false;
      choice.classList.remove('is-pending', 'is-paired', 'is-dragging', 'is-drop-target');
      choice.setAttribute('aria-pressed', 'false');
      var announcement = choice.querySelector('[data-match-announcement]');
      if (announcement) announcement.textContent = '';
      delete choice.dataset.pairedWith;
    });
    quiz.querySelectorAll('.quiz-matching__item').forEach(function(item) {
      item.classList.remove('is-dragging', 'is-drop-target');
      item.style.removeProperty('transform');
    });
    restoreMatchingSourceRows(quiz);
    var matching = quiz.querySelector('.quiz-matching');
    var results = quiz.querySelector('.quiz-matching-results');
    if (matching) matching.hidden = false;
    if (results) results.hidden = true;
    quiz.querySelectorAll('.quiz-matching-result').forEach(function(row) {
      row.classList.remove('is-correct', 'is-incorrect');
      var content = row.querySelector('[data-match-result-left]');
      if (content) content.innerHTML = '';
    });
    delete quiz.dataset.matchPendingLeft;
    delete quiz.dataset.matchPendingRight;
    var actions = quiz.querySelector('.quiz-actions');
    if (actions) {
      actions.hidden = false;
      actions.classList.remove('is-proceed');
      var submit = actions.querySelector('.quiz-submit');
      if (submit) submit.hidden = false;
    }
    quiz.querySelectorAll('.quiz-feedback').forEach(function(item) {
      item.classList.remove('is-visible', 'is-correct', 'is-incorrect');
    });
    var retake = quiz.querySelector('.quiz-retake-wrap');
    if (retake) retake.hidden = true;
  }
  function updateProgress() {
    document.querySelectorAll('.lesson-nav__item').forEach(function(item) {
      var id = Number(item.dataset.lessonTarget);
      var isLocked = !lessonUnlocked(id);
      item.disabled = isLocked;
      item.setAttribute('aria-disabled', isLocked ? 'true' : 'false');
      item.classList.toggle('is-active', id === activeLesson);
      var isComplete = completed(id);
      item.classList.toggle('is-complete', isComplete);
      var status = item.querySelector('.lesson-nav__status');
      if (status) status.setAttribute('aria-label', isComplete ? uiText('completed', 'Completed') : uiText('unstarted', 'Unstarted'));
    });
    document.querySelectorAll('.course-cover__lesson-item').forEach(function(item) {
      var id = Number(item.dataset.lessonTarget);
      var isLocked = !lessonUnlocked(id);
      item.disabled = isLocked;
      item.setAttribute('aria-disabled', isLocked ? 'true' : 'false');
      var isComplete = completed(id);
      item.classList.toggle('is-complete', isComplete);
      var status = item.querySelector('.course-cover__lesson-status');
      if (status) status.setAttribute('aria-label', isComplete ? uiText('completed', 'Completed') : uiText('unstarted', 'Unstarted'));
    });
    document.querySelectorAll('.sidebar-search-result').forEach(function(item) {
      var isLocked = !lessonUnlocked(Number(item.dataset.lessonTarget));
      item.disabled = isLocked;
      item.setAttribute('aria-disabled', isLocked ? 'true' : 'false');
    });
    var percent = lessonCount ? Math.round(state.completedLessons.length / lessonCount * 100) : 0;
    document.getElementById('progress-fill').style.width = percent + '%';
    document.getElementById('progress-value').textContent = uiText('complete_progress', '{percent}% COMPLETE', { percent: percent });
  }
  function lessonReadPercent(lesson) {
    if (!lesson) return 0;
    var id = Number(lesson.dataset.lessonId || 0);
    var total = Number(lesson.dataset.progressTotal || 0);
    if (!total) return 0;
    var viewed = completed(id) ? total : Math.min(total, Number(state.viewedBlocks[id] || 0));
    return Math.round(viewed / total * 100);
  }
  function syncLessonReadProgress() {
    var sticky = document.getElementById('lesson-read-progress-sticky');
    var lesson = document.querySelector('.lesson.is-active');
    var courseMain = document.querySelector('.course-main');
    if (!sticky || !lesson || !courseMain || activeLesson === 0) {
      if (sticky) sticky.classList.remove('is-visible');
      document.documentElement.style.setProperty('--lesson-read-progress', '0%');
      return;
    }
    document.documentElement.style.setProperty('--lesson-read-progress', lessonReadPercent(lesson) + '%');
    var inlineProgress = lesson.querySelector('.lesson-read-progress--inline');
    if (!inlineProgress) {
      sticky.classList.remove('is-visible');
      return;
    }
    var progressTop = inlineProgress.getBoundingClientRect().top + courseMain.scrollTop;
    sticky.classList.toggle('is-visible', courseMain.scrollTop > progressTop && courseMain.scrollTop > 0);
  }
  function recordVisibleLessonBlocks(lesson) {
    var courseMain = document.querySelector('.course-main');
    if (!lesson || !courseMain || !lesson.classList.contains('is-active')) return;
    var id = Number(lesson.dataset.lessonId || 0);
    var viewed = Number(state.viewedBlocks[id] || 0);
    var highest = viewed;
    var total = Number(lesson.dataset.progressTotal || 0);
    var gateCount = Number(lesson.dataset.gateCount || 0);
    var viewport = courseMain.getBoundingClientRect();
    lesson.querySelectorAll('[data-progress-mode="view"]:not(.is-locked)').forEach(function(block) {
      if (block.hidden) return;
      var rect = block.getBoundingClientRect();
      if (!rect.height) return;
      var visibleHeight = Math.max(0, Math.min(rect.bottom, viewport.bottom) - Math.max(rect.top, viewport.top));
      if (visibleHeight / rect.height >= 0.08) highest = Math.max(highest, Number(block.dataset.progressIndex || 0));
    });
    var changed = highest > viewed;
    if (changed) {
      state.viewedBlocks[id] = highest;
    }
    if (gateCount === 0 && total > 0 && highest >= total && !completed(id)) {
      markComplete(id);
      updateProgress();
      changed = true;
    }
    if (changed) {
      syncLessonReadProgress();
      saveState();
    }
  }
  function recordActionBlock(block) {
    if (!block) return;
    var lesson = block.closest('.lesson');
    if (!lesson) return;
    var id = Number(lesson.dataset.lessonId || 0);
    state.viewedBlocks[id] = Math.max(Number(state.viewedBlocks[id] || 0), Number(block.dataset.progressIndex || 0));
    syncLessonReadProgress();
  }
  function applyGates(lesson) {
    if (!lesson) return;
    var id = Number(lesson.dataset.lessonId);
    var unlocked = Number(state.gates[id] || 0);
    var gateCount = Number(lesson.dataset.gateCount || 0);
    var isComplete = completed(id);
    if (isComplete) unlocked = gateCount;
    lesson.querySelectorAll('[data-gate-level]').forEach(function(block) {
      block.classList.toggle('is-locked', Number(block.dataset.gateLevel) > unlocked);
    });
    lesson.querySelectorAll('[data-gate-index]').forEach(function(block) {
      var index = Number(block.dataset.gateIndex);
      var button = block.querySelector('.continue-button');
      if (!button) return;
      var done = index < unlocked;
      button.classList.toggle('is-complete', done);
      button.textContent = button.dataset.label || 'CONTINUE';
      button.disabled = false;
      button.title = '';
      block.hidden = done || isComplete;
    });
    lesson.querySelectorAll('.quiz-card').forEach(function(quiz) {
      var result = state.quizzes[quiz.dataset.questionId];
      if (result) showQuizResult(quiz, result);
    });
    lesson.querySelectorAll('.quiz-card[data-question-type="matching"]').forEach(syncMatchingPieceHeights);
    if (gateCount > 0 && unlocked >= gateCount) markComplete(id);
    isComplete = completed(id);
    if (isComplete) lesson.querySelectorAll('[data-gate-index]').forEach(function(block) { block.hidden = true; });
    var completedNavigation = lesson.querySelector('.completed-lesson-nav');
    if (completedNavigation) completedNavigation.hidden = !isComplete;
  }
  function openLesson(id, focus) {
    var previousLesson = activeLesson;
    var targetLesson = Number(id || 0);
    if (targetLesson > 0 && !lessonUnlocked(targetLesson)) return;
    var direction = directionalTransitions && previousLesson > 0 && targetLesson > 0 && targetLesson !== previousLesson
      ? (targetLesson > previousLesson ? 'next' : 'previous')
      : '';
    activeLesson = targetLesson;
    state.currentLesson = activeLesson;
    document.body.classList.toggle('is-cover', activeLesson === 0);
    document.getElementById('course-cover').hidden = activeLesson !== 0;
    document.querySelectorAll('.lesson').forEach(function(lesson) {
      var isActive = Number(lesson.dataset.lessonId) === activeLesson;
      lesson.classList.remove('lesson--enter-next', 'lesson--enter-previous');
      lesson.classList.toggle('is-active', isActive);
      if (isActive) {
        applyGates(lesson);
        lesson.querySelectorAll('.scroll-animate').forEach(function(item) { item.classList.remove('is-in'); });
        lesson.querySelectorAll('.scroll-animation-group').forEach(function(item) { item.classList.remove('is-in'); });
        window.requestAnimationFrame(function() { observeLessonAnimations(lesson); });
        if (direction) {
          void lesson.offsetWidth;
          lesson.classList.add(direction === 'next' ? 'lesson--enter-next' : 'lesson--enter-previous');
          window.setTimeout(function() {
            lesson.classList.remove('lesson--enter-next', 'lesson--enter-previous');
          }, 800);
        }
      }
    });
    updateProgress();
    saveState();
    closeSearch();
    document.getElementById('sidebar').classList.remove('is-open');
    if (focus) {
      if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
      var courseMain = document.querySelector('.course-main');
      var lessonEntryOffset = activeLesson > 0 ? 62 : 0;
      courseMain.style.scrollBehavior = 'auto';
      courseMain.scrollTop = lessonEntryOffset;
      window.scrollTo(0, 0);
      window.requestAnimationFrame(function() {
        courseMain.scrollTop = lessonEntryOffset;
        courseMain.style.removeProperty('scroll-behavior');
      });
    }
    window.requestAnimationFrame(function() {
      var currentLesson = document.querySelector('.lesson.is-active');
      recordVisibleLessonBlocks(currentLesson);
      syncLessonReadProgress();
    });
  }

  function showProcessStep(carousel, requestedIndex) {
    if (!carousel) return;
    var slides = Array.from(carousel.querySelectorAll('[data-process-slide]'));
    if (!slides.length) return;
    var index = Math.max(0, Math.min(Number(requestedIndex) || 0, slides.length - 1));
    var previousIndex = Math.max(0, Math.min(Number(carousel.dataset.processIndex) || 0, slides.length - 1));
    var shouldAnimate = carousel.dataset.processReady === 'true' && index !== previousIndex &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (carousel._processTransitionTimer) window.clearTimeout(carousel._processTransitionTimer);
    slides.forEach(function(slide) {
      slide.classList.remove(
        'process-slide--enter-next', 'process-slide--enter-previous', 'process-slide--enter-active',
        'process-slide--leave', 'process-slide--leave-next', 'process-slide--leave-previous', 'process-slide--leave-active'
      );
    });
    if (shouldAnimate) {
      var outgoing = slides[previousIndex];
      var incoming = slides[index];
      var direction = index > previousIndex ? 'next' : 'previous';
      outgoing.classList.add('process-slide--leave', 'process-slide--leave-' + direction);
      incoming.hidden = false;
      incoming.classList.add('process-slide--enter-' + direction);
      void incoming.offsetWidth;
      window.requestAnimationFrame(function() {
        incoming.classList.add('process-slide--enter-active');
        outgoing.classList.add('process-slide--leave-active');
      });
      carousel._processTransitionTimer = window.setTimeout(function() {
        outgoing.hidden = true;
        outgoing.classList.remove('process-slide--leave', 'process-slide--leave-' + direction, 'process-slide--leave-active');
        incoming.classList.remove('process-slide--enter-' + direction, 'process-slide--enter-active');
      }, 520);
    } else {
      slides.forEach(function(slide, slideIndex) { slide.hidden = slideIndex !== index; });
    }
    carousel.dataset.processIndex = index;
    carousel.dataset.processReady = 'true';
    carousel.querySelectorAll('[data-process-target]').forEach(function(button) {
      var current = Number(button.dataset.processTarget) === index;
      button.setAttribute('aria-current', current ? 'true' : 'false');
      button.tabIndex = current ? 0 : -1;
    });
    var count = carousel.querySelector('[data-process-count]');
    if (count) count.textContent = uiText('slide_position', '{current} of {total}', { current: index + 1, total: slides.length });
    var previous = carousel.querySelector('[data-process-action="previous"]');
    var next = carousel.querySelector('[data-process-action="next"]');
    if (previous) {
      previous.setAttribute('aria-disabled', index === 0 ? 'true' : 'false');
    }
    if (next) {
      next.setAttribute('aria-disabled', index === slides.length - 1 ? 'true' : 'false');
    }
  }

  function showLabeledGraphicItem(graphic, requestedIndex, focusTitle) {
    if (!graphic) return;
    var markers = Array.from(graphic.querySelectorAll('[data-labeled-marker]'));
    if (!markers.length) return;
    var index = ((Number(requestedIndex) || 0) % markers.length + markers.length) % markers.length;
    markers.forEach(function(marker, markerIndex) {
      var current = markerIndex === index;
      marker.classList.toggle('is-active', current);
      if (current) marker.classList.add('is-viewed');
      marker.setAttribute('aria-expanded', current ? 'true' : 'false');
      var title = marker.dataset.markerTitle || 'Marker';
      marker.setAttribute('aria-label', title + (marker.classList.contains('is-viewed')
        ? ', ' + uiText('viewed', 'viewed')
        : ', ' + uiText('not_viewed', 'not viewed')));
    });
    graphic.querySelectorAll('[data-labeled-callout]').forEach(function(callout) {
      callout.hidden = Number(callout.dataset.labeledCallout) !== index;
    });
    graphic.dataset.markerIndex = String(index);
    if (focusTitle) {
      var titleTarget = graphic.querySelector('[data-labeled-callout="' + index + '"] .labeled-graphic__title');
      if (titleTarget) titleTarget.focus({ preventScroll: true });
    }
  }

  function closeLabeledGraphic(graphic) {
    if (!graphic) return;
    graphic.querySelectorAll('[data-labeled-marker]').forEach(function(marker) {
      marker.classList.remove('is-active');
      marker.setAttribute('aria-expanded', 'false');
    });
    graphic.querySelectorAll('[data-labeled-callout]').forEach(function(callout) { callout.hidden = true; });
    graphic.dataset.markerIndex = '-1';
  }

  function revealAnimated(item) {
    if (item.classList.contains('scroll-animation-group')) {
      item.classList.add('is-in');
      item.querySelectorAll('.scroll-animate').forEach(function(child) { child.classList.add('is-in'); });
    } else {
      item.classList.add('is-in');
    }
  }

  var entranceObserver = 'IntersectionObserver' in window ? new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (!entry.isIntersecting) return;
      revealAnimated(entry.target);
      entranceObserver.unobserve(entry.target);
    });
  }, { threshold: 0.08 }) : null;

  function observeLessonAnimations(lesson) {
    if (!lesson) return;
    var groupedChildren = new Set();
    lesson.querySelectorAll('.scroll-animation-group .scroll-animate').forEach(function(item) { groupedChildren.add(item); });
    lesson.querySelectorAll('.scroll-animation-group, .scroll-animate').forEach(function(item) {
      if (groupedChildren.has(item)) return;
      if (entranceObserver) entranceObserver.observe(item); else revealAnimated(item);
    });
  }

  function formatVideoTime(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0) seconds = 0;
    var minutes = Math.floor(seconds / 60);
    var remainder = Math.floor(seconds % 60);
    return minutes + ':' + String(remainder).padStart(2, '0');
  }

  function initVideoPlayer(player) {
    var video = player.querySelector('video');
    var progress = player.querySelector('[data-video-progress]');
    var progressLoaded = player.querySelector('[data-video-loaded]');
    var progressPlayed = player.querySelector('[data-video-played]');
    var remaining = player.querySelector('[data-video-remaining]');
    var rateValue = player.querySelector('[data-video-rate-value]');
    var volume = player.querySelector('[data-video-volume]');
    var mute = player.querySelector('[data-video-action="mute"]');
    var fullscreen = player.querySelector('[data-video-action="fullscreen"]');
    var pictureInPicture = player.querySelector('[data-video-action="picture-in-picture"]');
    var captionDisplay = player.querySelector('[data-video-caption-display]');
    var captionText = player.querySelector('[data-video-caption-text]');
    var captionDataNode = player.querySelector('.academy-video__caption-data');
    var captionTracks = [];
    var activeCaptionIndex = -1;
    var inactivityTimer = 0;
    if (!video) return;
    if (captionDataNode) {
      try { captionTracks = (JSON.parse(captionDataNode.textContent || '{}').tracks || []); }
      catch (e) { captionTracks = []; }
    }

    function closeMenus(except) {
      player.querySelectorAll('[data-video-menu]').forEach(function(menu) {
        if (menu === except) return;
        menu.hidden = true;
        var control = menu.closest('.academy-video__menu-control');
        if (control) control.classList.remove('is-open');
        var button = control && control.querySelector('[data-video-menu-button]');
        if (button) button.setAttribute('aria-expanded', 'false');
      });
    }

    function toggleMenu(name) {
      var menu = player.querySelector('[data-video-menu="' + name + '"]');
      var button = player.querySelector('[data-video-menu-button="' + name + '"]');
      if (!menu || !button) return;
      var open = menu.hidden;
      closeMenus(open ? menu : null);
      menu.hidden = !open;
      var control = menu.closest('.academy-video__menu-control');
      if (control) control.classList.toggle('is-open', open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        var selected = menu.querySelector('[aria-checked="true"]');
        if (selected) selected.focus();
      }
    }

    function showControls() {
      player.classList.remove('is-user-inactive');
      window.clearTimeout(inactivityTimer);
      if (!video.paused) {
        inactivityTimer = window.setTimeout(function() {
          if (!player.matches(':focus-within') && !player.querySelector('.academy-video__menu-control.is-open')) {
            player.classList.add('is-user-inactive');
          }
        }, 2000);
      }
    }

    function disableNativeCaptions() {
      Array.from(video.textTracks || []).forEach(function(track) { track.mode = 'disabled'; });
    }

    function updateCaption() {
      if (!captionDisplay || !captionText || activeCaptionIndex < 0 || !captionTracks[activeCaptionIndex]) {
        if (captionDisplay) captionDisplay.hidden = true;
        if (captionText) captionText.textContent = '';
        return;
      }
      var track = captionTracks[activeCaptionIndex];
      var current = Number.isFinite(video.currentTime) ? video.currentTime : 0;
      var cue = (track.cues || []).find(function(item) { return current >= Number(item.start) && current < Number(item.end); });
      if (!cue && video.textTracks && video.textTracks[activeCaptionIndex]) {
        var activeCues = Array.from(video.textTracks[activeCaptionIndex].activeCues || []);
        if (activeCues.length) cue = { text: activeCues.map(function(item) { return item.text; }).join('\n') };
      }
      captionText.textContent = cue ? String(cue.text || '') : '';
      captionDisplay.hidden = !cue || !captionText.textContent;
    }

    function selectCaption(index, persist) {
      activeCaptionIndex = index >= 0 && index < captionTracks.length ? index : -1;
      player.querySelectorAll('[data-video-caption-index]').forEach(function(item) {
        var selected = Number(item.dataset.videoCaptionIndex) === activeCaptionIndex;
        item.classList.toggle('is-selected', selected);
        item.setAttribute('aria-checked', selected ? 'true' : 'false');
      });
      disableNativeCaptions();
      updateCaption();
      if (persist) {
        state.videoPreferences.captionLanguage = activeCaptionIndex >= 0 ? String(captionTracks[activeCaptionIndex].language || '') : 'off';
        saveState();
      }
    }

    function setPlaybackRate(value, persist) {
      var allowed = [2, 1.75, 1.5, 1.25, 1, 0.75, 0.5];
      var rate = Number(value);
      if (allowed.indexOf(rate) === -1) rate = 1;
      video.playbackRate = rate;
      if (rateValue) rateValue.textContent = rate + 'x';
      player.querySelectorAll('[data-video-rate]').forEach(function(item) {
        var selected = Number(item.dataset.videoRate) === rate;
        item.classList.toggle('is-selected', selected);
        item.setAttribute('aria-checked', selected ? 'true' : 'false');
      });
      if (persist) {
        state.videoPreferences.playbackRate = rate;
        saveState();
      }
    }

    function syncState() {
      var duration = Number.isFinite(video.duration) ? video.duration : 0;
      var current = Number.isFinite(video.currentTime) ? video.currentTime : 0;
      player.classList.toggle('is-playing', !video.paused);
      if (current > 0) player.classList.add('is-started');
      player.querySelectorAll('[data-video-action="toggle"]').forEach(function(button) {
        button.setAttribute('aria-label', video.paused ? uiText('play_video', 'Play video') : uiText('pause_video', 'Pause video'));
      });
      if (progress) progress.value = duration ? String(current / duration * 100) : '0';
      if (progressPlayed) progressPlayed.style.width = (duration ? current / duration * 100 : 0) + '%';
      if (progressLoaded) {
        var buffered = video.buffered && video.buffered.length ? video.buffered.end(video.buffered.length - 1) : 0;
        progressLoaded.style.width = (duration ? Math.min(100, buffered / duration * 100) : 0) + '%';
      }
      if (remaining) remaining.textContent = '-' + formatVideoTime(Math.max(0, duration - current));
      if (mute) mute.classList.toggle('is-muted', video.muted || video.volume === 0);
      if (volume && document.activeElement !== volume) volume.value = video.muted ? '0' : String(video.volume);
      updateCaption();
    }

    function togglePlayback() {
      player.classList.add('is-started');
      if (video.paused) {
        var promise = video.play();
        if (promise && promise.catch) promise.catch(function() {});
      } else {
        video.pause();
      }
    }

    player.querySelectorAll('[data-video-action="toggle"]').forEach(function(button) {
      button.addEventListener('click', togglePlayback);
    });
    video.addEventListener('click', togglePlayback);
    video.addEventListener('loadedmetadata', function() { disableNativeCaptions(); syncState(); });
    video.addEventListener('durationchange', syncState);
    video.addEventListener('timeupdate', syncState);
    video.addEventListener('progress', syncState);
    video.addEventListener('play', function() { syncState(); showControls(); });
    video.addEventListener('pause', function() { player.classList.remove('is-user-inactive'); syncState(); });
    video.addEventListener('ended', syncState);
    if (progress) progress.addEventListener('input', function() {
      if (Number.isFinite(video.duration)) video.currentTime = Number(progress.value) / 100 * video.duration;
      syncState();
    });
    player.querySelectorAll('[data-video-menu-button]').forEach(function(button) {
      button.addEventListener('click', function(event) {
        event.stopPropagation();
        toggleMenu(button.dataset.videoMenuButton);
        showControls();
      });
    });
    player.querySelectorAll('[data-video-rate]').forEach(function(item) {
      item.addEventListener('click', function(event) {
        event.stopPropagation();
        setPlaybackRate(item.dataset.videoRate, true);
        closeMenus();
        showControls();
      });
    });
    player.querySelectorAll('[data-video-caption-index]').forEach(function(item) {
      item.addEventListener('click', function(event) {
        event.stopPropagation();
        selectCaption(Number(item.dataset.videoCaptionIndex), true);
        closeMenus();
        showControls();
      });
    });
    if (mute) mute.addEventListener('click', function() {
      video.muted = !video.muted;
      mute.setAttribute('aria-label', video.muted ? uiText('unmute', 'Unmute') : uiText('mute', 'Mute'));
      syncState();
      showControls();
    });
    if (volume) volume.addEventListener('input', function() {
      video.volume = Number(volume.value);
      video.muted = video.volume === 0;
      syncState();
      showControls();
    });
    if (fullscreen) fullscreen.addEventListener('click', function() {
      if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen();
      else if (player.requestFullscreen) player.requestFullscreen();
    });
    document.addEventListener('fullscreenchange', function() {
      var active = document.fullscreenElement === player;
      player.classList.toggle('is-fullscreen', active);
      if (fullscreen) fullscreen.setAttribute('aria-label', active ? uiText('exit_fullscreen', 'Exit fullscreen') : uiText('fullscreen', 'Fullscreen'));
    });
    if (pictureInPicture) pictureInPicture.addEventListener('click', function() {
      if (document.pictureInPictureElement && document.exitPictureInPicture) {
        document.exitPictureInPicture().catch(function() {});
      } else if (video.requestPictureInPicture) {
        video.requestPictureInPicture().catch(function() {});
      }
    });
    video.addEventListener('enterpictureinpicture', function() { player.classList.add('is-picture-in-picture'); });
    video.addEventListener('leavepictureinpicture', function() { player.classList.remove('is-picture-in-picture'); });
    player.addEventListener('mousemove', showControls);
    player.addEventListener('touchstart', showControls, { passive: true });
    player.addEventListener('keydown', function(event) {
      showControls();
      if (event.key === 'Escape') closeMenus();
    });
    document.addEventListener('click', function(event) {
      if (!player.contains(event.target)) closeMenus();
    });
    var savedRate = Number(state.videoPreferences.playbackRate || 1);
    setPlaybackRate(savedRate, false);
    var savedLanguage = String(state.videoPreferences.captionLanguage || 'off');
    var savedCaptionIndex = captionTracks.findIndex(function(track) { return String(track.language || '') === savedLanguage; });
    selectCaption(savedLanguage === 'off' ? -1 : savedCaptionIndex, false);
    disableNativeCaptions();
    syncState();
  }

  function toggleFlashcard(card) {
    if (!card) return;
    var flipped = card.classList.toggle('is-flipped');
    card.setAttribute('aria-pressed', flipped ? 'true' : 'false');
  }

  var matchingPointerDrag = null;
  var matchingClickSuppressUntil = 0;
  var matchingDropOverlap = .015;
  var matchingPointerMoveTolerance = 8;
  function matchingOverlapRatio(sourceRect, targetRect) {
    var overlapWidth = Math.max(0, Math.min(sourceRect.right, targetRect.right) - Math.max(sourceRect.left, targetRect.left));
    var overlapHeight = Math.max(0, Math.min(sourceRect.bottom, targetRect.bottom) - Math.max(sourceRect.top, targetRect.top));
    var sourceArea = Math.max(1, sourceRect.width * sourceRect.height);
    return (overlapWidth * overlapHeight) / sourceArea;
  }
  function matchingDropTargetFor(drag) {
    if (!drag || !drag.item || !drag.quiz) return null;
    var sourceRect = drag.item.getBoundingClientRect();
    var bestTarget = null;
    var bestOverlap = matchingDropOverlap;
    drag.quiz.querySelectorAll('.quiz-match-piece--target').forEach(function(target) {
      if (target.disabled) return;
      var targetItem = target.closest('.quiz-matching__item--target');
      if (!targetItem) return;
      var overlap = matchingOverlapRatio(sourceRect, targetItem.getBoundingClientRect());
      if (overlap >= bestOverlap) {
        bestOverlap = overlap;
        bestTarget = target;
      }
    });
    return bestTarget;
  }
  function setMatchingDropTarget(drag, target) {
    if (!drag || drag.target === target) return;
    if (drag.target) {
      var oldItem = drag.target.closest('.quiz-matching__item--target');
      if (oldItem) oldItem.classList.remove('is-drop-target');
    }
    drag.target = target;
    if (target) {
      var targetItem = target.closest('.quiz-matching__item--target');
      if (targetItem) targetItem.classList.add('is-drop-target');
    }
  }
  function beginMatchingPointerDrag(source, event) {
    if (!source || source.disabled || source.closest('.quiz-card').classList.contains('is-submitted')) return;
    var item = source.closest('.quiz-matching__item--source');
    if (!item) return;
    matchingPointerDrag = {
      source: source,
      item: item,
      quiz: source.closest('.quiz-card'),
      pointerId: event.pointerId,
      startX: Number(event.clientX || 0),
      startY: Number(event.clientY || 0),
      active: false,
      target: null
    };
    try { source.setPointerCapture(event.pointerId); } catch (e) {}
  }
  function updateMatchingPointerDrag(event) {
    if (!matchingPointerDrag || event.pointerId !== matchingPointerDrag.pointerId) return;
    var deltaX = Number(event.clientX || 0) - matchingPointerDrag.startX;
    var deltaY = Number(event.clientY || 0) - matchingPointerDrag.startY;
    if (!matchingPointerDrag.active && Math.hypot(deltaX, deltaY) < matchingPointerMoveTolerance) return;
    matchingPointerDrag.active = true;
    if (event.cancelable) event.preventDefault();
    matchingPointerDrag.item.classList.add('is-dragging');
    matchingPointerDrag.item.style.transform = 'translate3d(' + deltaX + 'px, ' + deltaY + 'px, 0)';
    setMatchingDropTarget(matchingPointerDrag, matchingDropTargetFor(matchingPointerDrag));
  }
  function finishMatchingPointerDrag(event) {
    if (!matchingPointerDrag || event.pointerId !== matchingPointerDrag.pointerId) return;
    var drag = matchingPointerDrag;
    if (drag.active && event.type !== 'pointercancel') updateMatchingPointerDrag(event);
    matchingPointerDrag = null;
    try { drag.source.releasePointerCapture(drag.pointerId); } catch (e) {}
    drag.item.classList.remove('is-dragging');
    drag.item.style.removeProperty('transform');
    if (drag.target) {
      var targetItem = drag.target.closest('.quiz-matching__item--target');
      if (targetItem) targetItem.classList.remove('is-drop-target');
    }
    if (!drag.active) return;
    if (event && event.cancelable) event.preventDefault();
    matchingClickSuppressUntil = Date.now() + 350;
    if (drag.target && event.type !== 'pointercancel') {
      pairMatchingPieces(drag.quiz, drag.source.dataset.matchKey, drag.target.dataset.matchKey);
    }
  }

  document.addEventListener('pointerdown', function(event) {
    var source = event.target.closest('.quiz-match-piece--source');
    if (!source || source.disabled || event.button !== 0 || event.isPrimary === false) return;
    try { source.focus({ preventScroll: true }); } catch (e) { source.focus(); }
    beginMatchingPointerDrag(source, event);
  });
  document.addEventListener('pointermove', updateMatchingPointerDrag, { passive: false });
  document.addEventListener('pointerup', finishMatchingPointerDrag, { passive: false });
  document.addEventListener('pointercancel', finishMatchingPointerDrag, { passive: false });

  document.addEventListener('click', function(event) {
    var nav = event.target.closest('[data-lesson-target]');
    if (nav) { openLesson(nav.dataset.lessonTarget, true); return; }
    var start = event.target.closest('[data-start-course]');
    if (start) { openLesson(state.currentLesson || 1, true); return; }
    var exitCourse = event.target.closest('[data-exit-course]');
    if (exitCourse) {
      var exitLesson = exitCourse.closest('.lesson');
      if (exitLesson) {
        markComplete(Number(exitLesson.dataset.lessonId));
        applyGates(exitLesson);
        updateProgress();
        saveState();
        var completion = exitLesson.querySelector('.course-complete');
        if (completion) completion.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      SCORM.finish();
      window.setTimeout(function() { try { window.close(); } catch (e) {} }, 150);
      return;
    }
    var gate = event.target.closest('.continue-button');
    if (gate) {
      var block = gate.closest('[data-gate-index]');
      var lesson = gate.closest('.lesson');
      recordActionBlock(block);
      var id = Number(lesson.dataset.lessonId);
      var index = Number(block.dataset.gateIndex);
      var gateCount = Number(lesson.dataset.gateCount || 0);
      var unlocked = Number(state.gates[id] || 0);
      if (index === unlocked) state.gates[id] = unlocked + 1;
      if (index === gateCount - 1) {
        state.gates[id] = gateCount;
        markComplete(id);
        updateProgress();
        saveState();
        if (id < lessonCount) openLesson(id + 1, true); else applyGates(lesson);
        return;
      }
      applyGates(lesson); updateProgress(); saveState();
      observeLessonAnimations(lesson);
      var next = lesson.querySelector('[data-gate-level="' + (index + 1) + '"]:not(.is-locked)');
      if (next) next.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    var nextLesson = event.target.closest('[data-next-lesson]');
    if (nextLesson) { markComplete(activeLesson); openLesson(nextLesson.dataset.nextLesson, true); return; }
    var card = event.target.closest('.flashcard');
    if (card && !event.target.closest('a')) { toggleFlashcard(card); return; }
    var tab = event.target.closest('[data-tab-panel]');
    if (tab) {
      var tabSet = tab.closest('.tab-set');
      tabSet.querySelectorAll('.tab-button').forEach(function(item) { item.classList.remove('is-active'); item.setAttribute('aria-selected', 'false'); });
      tabSet.querySelectorAll('.tab-panel').forEach(function(item) { item.classList.remove('is-active'); });
      tab.classList.add('is-active'); tab.setAttribute('aria-selected', 'true');
      var tabPanel = document.getElementById(tab.dataset.tabPanel);
      if (tabPanel) tabPanel.classList.add('is-active');
      return;
    }
    var processTarget = event.target.closest('[data-process-target]');
    if (processTarget) {
      showProcessStep(processTarget.closest('.process-carousel'), processTarget.dataset.processTarget);
      return;
    }
    var processAction = event.target.closest('[data-process-action]');
    if (processAction) {
      if (processAction.getAttribute('aria-disabled') === 'true') return;
      var carousel = processAction.closest('.process-carousel');
      var current = Number(carousel.dataset.processIndex || 0);
      showProcessStep(carousel, current + (processAction.dataset.processAction === 'next' ? 1 : -1));
      return;
    }
    var labeledAction = event.target.closest('[data-labeled-action]');
    if (labeledAction) {
      var labeledGraphic = labeledAction.closest('[data-labeled-graphic]');
      if (labeledAction.dataset.labeledAction === 'close') {
        closeLabeledGraphic(labeledGraphic);
      } else {
        var labeledIndex = Number(labeledGraphic.dataset.markerIndex || 0);
        showLabeledGraphicItem(labeledGraphic, labeledIndex + (labeledAction.dataset.labeledAction === 'next' ? 1 : -1), true);
      }
      return;
    }
    var marker = event.target.closest('[data-labeled-marker]');
    if (marker) {
      showLabeledGraphicItem(marker.closest('[data-labeled-graphic]'), marker.dataset.labeledMarker, true);
      return;
    }
    var zoom = event.target.closest('[data-zoom-src]');
    if (zoom) {
      var zoomDialog = document.getElementById('image-zoom-dialog');
      zoomDialog.querySelector('img').src = zoom.dataset.zoomSrc;
      zoomDialog.querySelector('img').alt = zoom.dataset.zoomAlt || 'Course image';
      if (zoomDialog.showModal) zoomDialog.showModal(); else zoomDialog.setAttribute('open', '');
      return;
    }
    if (event.target.closest('[data-close-zoom]')) {
      var openDialog = document.getElementById('image-zoom-dialog');
      if (openDialog.close) openDialog.close(); else openDialog.removeAttribute('open');
      return;
    }
    var matchChoice = event.target.closest('.quiz-match-piece');
    if (matchChoice && !matchChoice.disabled) {
      if (Date.now() < matchingClickSuppressUntil) return;
      var matchQuiz = matchChoice.closest('.quiz-card');
      var matchSide = matchChoice.dataset.matchSide;
      var pendingName = matchSide === 'left' ? 'matchPendingLeft' : 'matchPendingRight';
      matchQuiz.querySelectorAll('[data-match-side="' + matchSide + '"]').forEach(function(choice) {
        choice.classList.remove('is-pending');
      });
      matchChoice.classList.add('is-pending');
      matchQuiz.dataset[pendingName] = matchChoice.dataset.matchKey;
      var leftKey = matchQuiz.dataset.matchPendingLeft;
      var rightKey = matchQuiz.dataset.matchPendingRight;
      if (leftKey && rightKey) {
        pairMatchingPieces(matchQuiz, leftKey, rightKey);
      }
      return;
    }
    var submit = event.target.closest('.quiz-submit');
    if (submit) {
      var quiz = submit.closest('.quiz-card');
      var questionType = String(quiz.dataset.questionType || 'multiple_choice');
      var result;
      if (questionType === 'multiple_response') {
        var selectedInputs = Array.from(quiz.querySelectorAll('input[type="checkbox"]:checked'));
        if (!selectedInputs.length) return;
        var allInputs = Array.from(quiz.querySelectorAll('input[type="checkbox"]'));
        var correct = allInputs.every(function(input) {
          return input.checked === (input.dataset.correct === 'true');
        });
        result = { selected: selectedInputs.map(function(input) { return input.value; }), correct: correct };
      } else if (questionType === 'fill_in_the_blank') {
        var fillin = quiz.querySelector('[data-quiz-fillin]');
        var answer = String(fillin ? fillin.value : '').trim();
        if (!answer) return;
        var accepted = [];
        try { accepted = JSON.parse(fillin.dataset.acceptedAnswers || '[]'); } catch (e) {}
        var normalized = answer.toLocaleLowerCase().replace(/\s+/g, ' ').trim();
        var fillCorrect = accepted.some(function(value) {
          return String(value).toLocaleLowerCase().replace(/\s+/g, ' ').trim() === normalized;
        });
        result = { answer: answer, correct: fillCorrect };
      } else if (questionType === 'matching') {
        var leftChoices = Array.from(quiz.querySelectorAll('[data-match-side="left"]'));
        if (!leftChoices.length || leftChoices.some(function(choice) { return !choice.dataset.pairedWith; })) return;
        var pairs = {};
        leftChoices.forEach(function(choice) { pairs[choice.dataset.matchKey] = choice.dataset.pairedWith; });
        var matchCorrect = leftChoices.every(function(choice) {
          return choice.dataset.matchKey === choice.dataset.pairedWith;
        });
        result = { pairs: pairs, correct: matchCorrect };
      } else {
        var selected = quiz.querySelector('input[type="radio"]:checked');
        if (!selected) return;
        result = { selected: selected.value, correct: selected.dataset.correct === 'true' };
      }
      state.quizzes[quiz.dataset.questionId] = result;
      showQuizResult(quiz, result);
      applyGates(quiz.closest('.lesson'));
      saveState();
      return;
    }
    var retake = event.target.closest('.quiz-retake');
    if (retake) {
      var retakeQuiz = retake.closest('.quiz-card');
      delete state.quizzes[retakeQuiz.dataset.questionId];
      resetQuiz(retakeQuiz);
      saveState();
      return;
    }
  });

  document.addEventListener('keydown', function(event) {
    var matchChoice = event.target.closest('.quiz-match-piece');
    if (matchChoice && !matchChoice.disabled && (event.key === 'Enter' || event.key === ' ')) {
      event.preventDefault();
      matchChoice.click();
      return;
    }
    var card = event.target.closest('.flashcard');
    if (!card || event.target.closest('a') || (event.key !== 'Enter' && event.key !== ' ')) return;
    event.preventDefault();
    toggleFlashcard(card);
  });

  document.getElementById('toc-toggle').addEventListener('click', function() {
    if (window.matchMedia('(max-width: 900px)').matches) document.getElementById('sidebar').classList.toggle('is-open');
    else document.body.classList.toggle('nav-closed');
  });
  var lessonScrollMain = document.querySelector('.course-main');
  if (lessonScrollMain) lessonScrollMain.addEventListener('scroll', function() {
    var lesson = document.querySelector('.lesson.is-active');
    recordVisibleLessonBlocks(lesson);
    syncLessonReadProgress();
  }, { passive: true });
  window.addEventListener('resize', function() {
    var lesson = document.querySelector('.lesson.is-active');
    if (lesson) lesson.querySelectorAll('.quiz-card[data-question-type="matching"]').forEach(syncMatchingPieceHeights);
    recordVisibleLessonBlocks(lesson);
    syncLessonReadProgress();
  });
  var searchToggle = document.getElementById('search-toggle');
  var searchArea = document.getElementById('sidebar-search-area');
  var searchForm = document.getElementById('sidebar-search-form');
  var search = document.getElementById('lesson-search');
  var searchClose = document.getElementById('search-close');
  var lessonNav = document.getElementById('lesson-nav');
  var searchResults = document.getElementById('sidebar-search-results');
  var searchMessage = document.getElementById('sidebar-search-message');
  function openSearch() {
    if (!searchArea || !search || !lessonNav || !searchResults) return;
    document.getElementById('sidebar').classList.add('is-searching');
    searchArea.hidden = false;
    lessonNav.hidden = true;
    searchResults.hidden = false;
    search.focus();
  }
  function closeSearch() {
    var sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.remove('is-searching');
    if (searchArea) searchArea.hidden = true;
    if (lessonNav) lessonNav.hidden = false;
    if (searchResults) searchResults.hidden = true;
    if (search) search.value = '';
    if (searchMessage) searchMessage.textContent = '';
    document.querySelectorAll('.sidebar-search-result').forEach(function(item) { item.hidden = true; });
  }
  function occurrenceCount(text, query) {
    var count = 0;
    var position = 0;
    while (query && (position = text.indexOf(query, position)) !== -1) {
      count += 1;
      position += query.length;
    }
    return count;
  }
  function runSearch() {
    var query = search.value.trim().toLowerCase();
    var visible = 0;
    document.querySelectorAll('.sidebar-search-result').forEach(function(item) {
      var count = occurrenceCount(item.dataset.searchText || '', query);
      item.hidden = !query || count === 0;
      if (count) {
        visible += 1;
        var label = item.querySelector('.sidebar-search-result__count');
        if (label) label.textContent = uiText('result', count === 1 ? '{count} result' : '{count} results', { count: count });
      }
    });
    if (searchMessage) searchMessage.textContent = query && !visible
      ? uiText('no_results', 'No results for “{query}”', { query: search.value.trim() })
      : '';
  }
  if (searchToggle) searchToggle.addEventListener('click', openSearch);
  if (searchClose) searchClose.addEventListener('click', function(event) { event.preventDefault(); closeSearch(); });
  if (search) search.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') { event.preventDefault(); closeSearch(); }
    if (event.key === 'Enter') { event.preventDefault(); runSearch(); }
  });
  if (searchForm) searchForm.addEventListener('submit', function(event) {
    event.preventDefault();
    runSearch();
  });
  window.addEventListener('beforeunload', function() { saveState(); SCORM.finish(); });

  document.querySelectorAll('.process-carousel').forEach(function(carousel) { showProcessStep(carousel, 0); });
  document.querySelectorAll('[data-labeled-graphic]').forEach(closeLabeledGraphic);
  document.querySelectorAll('[data-video-player]').forEach(initVideoPlayer);

  var location = SCORM.getLocation();
  var match = /^lesson-(\d+)$/.exec(location || '');
  openLesson(match ? Number(match[1]) : 0, false);
  document.title = __COURSE_TITLE__;
})();
'''.replace("__LESSON_COUNT__", str(len(lessons))).replace(
        "__DIRECTIONAL_TRANSITIONS__", "true" if directional_transitions else "false"
    ).replace(
        "__NAVIGATION_RESTRICTED__", "true" if navigation_restricted else "false"
    ).replace("__COURSE_TITLE__", course_title_json).replace("__UI_LABELS__", ui_labels_json)
    root_css = (
        f':root{{--accent:{accent};--accent-dark:{accent_dark};--accent-text:{contrasting_text(accent)};'
        f'--lesson-header-bg:{header_background};--lesson-header-text:{header_text};'
        f'--process-step-badge-radius:{process_step_badge_radius};'
        f'--heading:{css_string(heading_family)},"Noto Sans Myanmar",sans-serif;'
        f'--body:{css_string(body_family)},"Noto Sans Myanmar",sans-serif;'
        f'--ui:{css_string(ui_family)},"Noto Sans Myanmar",sans-serif;}}'
    )
    return f'''<!doctype html>
<html lang="{esc(course.get("language") or "en")}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(course.get("course_title") or "OCP Academy Course")}</title>
  <script src="scorm_api.js"></script>
  <style>{font_face_css(theme)}\n{css}\n{root_css}</style>
</head>
<body class="{esc(' '.join(theme_classes))}">
  <button class="toc-toggle" id="toc-toggle" type="button" aria-label="{esc(ui(ui_labels, "toggle_toc", "Toggle lesson table of contents"))}"><span></span><span></span><span></span></button>
  <aside class="sidebar" id="sidebar">
    <header class="sidebar__header">
      <div class="sidebar__header-content">
        {f'<button class="sidebar__search-toggle" id="search-toggle" type="button" aria-label="{esc(ui(ui_labels, "open_search", "Open search menu"))}">{search_icon}</button>' if search_enabled else ''}
        <h1><button class="sidebar__course-title" type="button" data-lesson-target="0">{esc(course.get("course_title") or "OCP Academy Course")}</button></h1>
        <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
        <p class="progress-value" id="progress-value">{esc(ui(ui_labels, "complete_progress", "{percent}% COMPLETE", percent=0))}</p>
      </div>
      {f'<div class="sidebar__search-area" id="sidebar-search-area" hidden><form class="sidebar__search" id="sidebar-search-form" autocomplete="off">{search_icon}<input id="lesson-search" name="search" type="search" placeholder="{esc(ui(ui_labels, "search", "search"))}" aria-label="{esc(ui(ui_labels, "search", "Search"))}"><button id="search-close" type="reset" aria-label="{esc(ui(ui_labels, "close_search", "Close search menu"))}">{close_icon}</button></form></div>' if search_enabled else ''}
    </header>
    <div class="sidebar__body">
      <nav class="lesson-nav" id="lesson-nav" aria-label="{esc(ui(ui_labels, "lessons", "Lessons"))}">{nav}</nav>
      {f'<div class="sidebar-search-results" id="sidebar-search-results" hidden><p class="sidebar-search-results__message" id="sidebar-search-message"></p>{search_results}</div>' if search_enabled else ''}
    </div>
  </aside>
  <main class="course-main">
    <section class="course-cover" id="course-cover">
      <header class="course-cover__hero"{cover_style}><div class="course-cover__hero-content">
        <div class="course-cover__title-frame"><h2>{esc(course.get("course_title") or "OCP Academy Course")}</h2></div>
        <button class="start-button" type="button" data-start-course>{esc(ui(ui_labels, "start_course", "START COURSE"))}</button>
      </div></header>
      <div class="course-cover__details"><div class="course-cover__description">{course.get("course_description_html") or esc(course.get("course_subtitle") or "")}</div>
      {f'<p class="course-cover__lesson-count">{esc(ui(ui_labels, "lessons_count", "{count} lessons", count=len(lessons)))}</p>' if show_lesson_count else ''}
      {f'<nav class="course-cover__lesson-list" aria-label="{esc(ui(ui_labels, "course_lessons", "Course lessons"))}">{cover_nav}</nav>' if show_cover_lesson_list else ''}</div>
    </section>
    {lesson_html}
  </main>
  <div class="lesson-read-progress-sticky" id="lesson-read-progress-sticky" aria-hidden="true"><div class="lesson-read-progress"><div class="lesson-read-progress__progress"><div class="lesson-read-progress__track"><div class="lesson-read-progress__indicator"></div></div></div></div></div>
  <dialog class="image-zoom-dialog" id="image-zoom-dialog"><button type="button" data-close-zoom aria-label="{esc(ui(ui_labels, "close_image", "Close image"))}">×</button><img alt=""></dialog>
  <script>{script}</script>
</body>
</html>'''

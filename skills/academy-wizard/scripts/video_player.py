"""Shared Chiplet-style video markup for Slides and Scrolling."""
from __future__ import annotations
import json
from html import escape
def esc(value): return escape(str(value or ''), quote=True)
def ui(labels, key, default): return str((labels or {}).get(key, default))
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


def academy_video_html(
    media: dict | None,
    caption_html: str = "",
    animate: bool = True,
    video_class: str = "",
    video_attributes: str = "",
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
        '<div class="academy-video" data-video-player>'
        f'<div class="academy-video__surface"><video class="{esc(video_class)}" {video_attributes} preload="metadata" playsinline src="{esc(media["path"])}"{poster}><source src="{esc(media["path"])}">{tracks}</video>'
        f'{caption_data}'
        f'<button class="academy-video__big-play" type="button" data-video-action="toggle" aria-label="{esc(ui(ui_labels, "play_video", "Play video"))}">'
        f'{scrolling_video_icon("play")}'
        '</button>'
        '</div><div class="academy-video__controls" role="group" aria-label="Video controls">'
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
    )

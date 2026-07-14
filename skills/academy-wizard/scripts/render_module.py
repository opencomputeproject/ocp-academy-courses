#!/usr/bin/env python3
"""
render_module.py — render a moduleN.html from course.json + a module index.

Usage:
    python render_module.py <course.json> --module N [--out moduleN.html]
    python render_module.py <course.json> --all          # render every module

The module HTML is fully self-contained: CSS inlined from templates/module_styles.css,
SCORM wiring inlined, audio map built from each slide's audio.wav_file. The output
goes next to course.json by default unless --out specifies otherwise.

Slide types supported: title, course_overview, objectives, content_bullets,
content_two_column, content_grid, content_table, content_diagram, takeaways,
up_next, course_complete.
"""

from __future__ import annotations
import argparse
import hashlib
import html
import itertools
import json
import os
import sys
from pathlib import Path
from motion_intro import (
    load_motion_intro_css,
    motion_intro_body_class,
    motion_intro_noscript_style,
    motion_intro_script,
    render_motion_intro,
)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "templates"
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".m4v"}


def _is_video_figure(fig: dict | None) -> bool:
    if not fig:
        return False
    media_type = (fig.get("media_type") or fig.get("type") or "").lower()
    return media_type == "video" or Path(fig.get("path", "")).suffix.lower() in VIDEO_EXTENSIONS


def esc(s: str | None) -> str:
    """HTML-escape a value, treating None as ''."""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def _norm_text(value: str | None) -> str:
    return " ".join(str(value or "").split()).casefold()


def _title_for_slide(slide: dict, label: str | None, default: str, module: dict) -> str:
    """Return a visible title that never duplicates the section label."""
    title = slide.get("title") or default
    if label and _norm_text(title) == _norm_text(label):
        descriptive = slide.get("descriptive_title")
        if descriptive and _norm_text(descriptive) != _norm_text(label):
            return str(descriptive)
        slide_type = slide.get("type", "")
        norm_label = _norm_text(label)
        norm_default = _norm_text(default)
        if slide_type == "course_overview" or norm_label == "course overview" or norm_default == "course overview":
            return "Course Roadmap"
        if slide_type == "objectives" or norm_label == "learning objectives" or norm_default == "learning objectives":
            return "What You Will Learn"
        if slide_type == "takeaways" or norm_label == "key takeaways" or norm_default == "key takeaways":
            module_id = module.get("id")
            return f"Module {module_id} Summary" if module_id else "Module Summary"
        return f"{label} In Practice"
    return str(title)


def _badge_text_html(course: dict) -> str:
    brand = course.get("brand", {})
    text = brand.get("badge_text")
    if not text or not str(text).strip():
        return ""
    return f'<span>{esc(text)}</span>'


def load_styles() -> str:
    css = (TEMPLATE_DIR / "module_styles.css").read_text()
    css += "\n\n" + load_motion_intro_css(TEMPLATE_DIR)
    return css


# ----- Slide renderers ------------------------------------------------------

def render_title(slide: dict, course: dict, module: dict) -> str:
    title = slide.get("title") or module.get("title", "")
    subtitle = slide.get("subtitle") or course.get("course_subtitle", "")
    version_chip = slide.get("version_chip") or course.get("spec_version_chip", "")
    tagline = slide.get("tagline") or course.get("tagline", "")
    course_logo = course.get("brand", {}).get("course_logo", "")
    return f'''
  <div class="slide slide-hero active" data-slide="{slide["id"]}">
    <div class="hero-content">
      {f'<img src="{esc(course_logo)}" alt="{esc(course.get("course_title",""))}" class="hero-logo animate-in">' if course_logo else ""}
      <h1 class="hero-title animate-in">{esc(title)}</h1>
      <p class="hero-subtitle animate-in">{esc(subtitle)}</p>
      {f'<span class="hero-version animate-in">{esc(version_chip)}</span>' if version_chip else ""}
      <div class="hero-start-hint animate-in">
        Press <span class="inline-play-icon" aria-hidden="true">&#9654;</span><span>then advance with</span> <strong style="margin: 0 4px;">&#8594;</strong> or <strong style="margin: 0 4px;">Space</strong>
      </div>
      {f'<p class="hero-tagline animate-in">{esc(tagline)}</p>' if tagline else ""}
    </div>
  </div>
'''


def render_course_overview(slide: dict, course: dict, module: dict) -> str:
    label = "Course Overview"
    items = []
    for i, mt in enumerate(slide.get("modules_listed", []), start=1):
        current = ' current' if i == module["id"] else ""
        items.append(f'''
        <li class="module-item{current}">
          <div class="module-number">{i}</div>
          <div class="module-name">{esc(mt)}</div>
        </li>''')
    chips_html = ""
    for chip in slide.get("chips", []):
        # Optional url makes a chip clickable.
        url = chip.get("url")
        icon = str(chip.get("icon", "")).strip()
        inner = f'''
          {f'<div class="meta-chip-icon">{esc(icon)}</div>' if icon else ""}
          <span>{esc(chip.get("text",""))}</span>'''
        if url:
            chips_html += f'''
        <a class="meta-chip" href="{esc(url)}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit;">{inner}
        </a>'''
        else:
            chips_html += f'''
        <div class="meta-chip">{inner}
        </div>'''
    media_embed = slide.get("media_embed")
    if media_embed:
        # Accept either a raw HTML string OR a dict with {type:'youtube', id:'XXX', title:'...'}
        if isinstance(media_embed, dict):
            if media_embed.get("type") == "youtube":
                yt_id = media_embed.get("id","")
                title = esc(media_embed.get("title","Video"))
                label = esc(media_embed.get("label","Watch"))
                media_embed_html = f'<div class="animate-in" style="margin: 24px auto 0; max-width: 720px; text-align: center;"><div style="font-family: var(--font-heading); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ocp-green); margin-bottom: 10px;">{label}</div><div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);"><iframe src="https://www.youtube.com/embed/{yt_id}?rel=0&modestbranding=1" title="{title}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"></iframe></div><p style="margin-top: 10px; font-size: 0.85rem; color: var(--text-muted);">If the embed is blocked by your LMS, the video link is also in the chips above.</p></div>'
            else:
                media_embed_html = ""
        else:
            media_embed_html = str(media_embed)
    else:
        media_embed_html = ""
    return f'''
  <div class="slide" data-slide="{slide["id"]}">
    <div class="slide-content">
      <span class="section-label animate-in">{label}</span>
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "Course Roadmap", module))}</h2>
      {f'<p class="slide-subtitle animate-in">{esc(slide.get("subtitle"))}</p>' if slide.get("subtitle") else ""}
      <ol class="module-list animate-in">{"".join(items)}
      </ol>
      <div class="course-meta animate-in">{chips_html}
      </div>
      {media_embed_html}
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def render_objectives(slide: dict, course: dict, module: dict) -> str:
    label = "Learning Objectives"
    items = "".join(
        f'''
        <li class="takeaway-item animate-in">
          <span class="check-icon">&#10003;</span>
          <p>{esc(obj)}</p>
        </li>''' for obj in slide.get("objectives", [])
    )
    return f'''
  <div class="slide" data-slide="{slide["id"]}">
    <div class="slide-content">
      <span class="section-label animate-in">{label}</span>
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "What You Will Learn", module))}</h2>
      {f'<p class="slide-subtitle animate-in">{esc(slide.get("subtitle"))}</p>' if slide.get("subtitle") else ""}
      <ul class="takeaway-list">{items}
      </ul>
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def _bullets_html(bullets: list[dict]) -> str:
    parts = []
    for b in bullets:
        bold_lead = b.get("bold_lead", "")
        text = b.get("text", "")
        if bold_lead:
            inner = f'<strong>{esc(bold_lead)}</strong> {esc(text)}'
        else:
            inner = esc(text)
        parts.append(f'''
            <li>
              <span class="bullet-icon">&#10003;</span>
              <span>{inner}</span>
            </li>''')
    return "".join(parts)


def _learner_aids_html(slide: dict, course: dict) -> str:
    # Render optional learner aids in the slide content flow. The returned
    # block is appended inside `.slide-content`, after the slide's primary
    # text/table/image content. It is never fixed or floating.
    glossary = {
        item.get("id"): item
        for item in course.get("term_glossary", [])
        if isinstance(item, dict) and item.get("id")
    }
    glossary_chips = []
    for term_id in slide.get("term_refs", []):
        item = glossary.get(term_id)
        if not item:
            continue
        term = esc(item.get("term"))
        tip = esc(item.get("tooltip"))
        label = item.get("reference_label")
        tooltip = tip + (f" Reference: {esc(label)}." if label else "")
        url = item.get("url")
        if url:
            glossary_chips.append(
                f'<a class="glossary-chip" href="{esc(url)}" target="_blank" rel="noopener" '
                f'data-tooltip="{tooltip}" title="{tip}">{term}</a>'
            )
        else:
            glossary_chips.append(
                f'<span class="glossary-chip" data-tooltip="{tooltip}" title="{tip}">{term}</span>'
            )

    ref_links = []
    for link in slide.get("reference_links", []):
        url = link.get("url")
        if not url:
            continue
        ref_links.append(
            f'<a class="reference-pill" href="{esc(url)}" target="_blank" rel="noopener">{esc(link.get("label") or "Learn more")}</a>'
        )

    callout_html = ""
    callout = slide.get("resource_callout")
    if isinstance(callout, dict) and callout.get("url"):
        callout_html = f'''
        <div class="resource-callout animate-in">
          <div>
            <span class="resource-label">Learner Resource</span>
            <strong>{esc(callout.get("title"))}</strong>
            <p>{esc(callout.get("text"))}</p>
          </div>
          <a class="resource-button" href="{esc(callout.get("url"))}" target="_blank" rel="noopener">{esc(callout.get("button_text") or "Open")}</a>
        </div>'''

    if not glossary_chips and not ref_links and not callout_html:
        return ""

    glossary_html = ""
    if glossary_chips:
        glossary_html = '<div class="glossary-strip animate-in">' + "".join(glossary_chips) + '</div>'
    refs_html = ""
    if ref_links:
        refs_html = '<div class="reference-strip animate-in">' + "".join(ref_links) + '</div>'
    return f'''
      <div class="learner-aids">{glossary_html}{refs_html}{callout_html}
      </div>'''


def _summary_items_html(slide: dict) -> str:
    items = [str(item).strip() for item in slide.get("summary_items", []) if str(item).strip()]
    if not items:
        return ""
    return '''
      <ul class="summary-list animate-in">''' + "".join(
        f'''
        <li>{esc(item)}</li>''' for item in items
    ) + '''
      </ul>'''


def render_content_bullets(slide: dict, course: dict, module: dict) -> str:
    label = slide.get("section_label")
    slide_class = "slide slide--mobile-scroll" if slide.get("mobile_scroll") else "slide"
    return f'''
  <div class="{slide_class}" data-slide="{slide["id"]}">
    <div class="slide-content">
      {f'<span class="section-label animate-in">{esc(label)}</span>' if label else ""}
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "", module))}</h2>
      {f'<p class="slide-subtitle animate-in">{esc(slide.get("subtitle"))}</p>' if slide.get("subtitle") else ""}
      <ul class="bullet-list animate-in">{_bullets_html(slide.get("bullets", []))}
      </ul>
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def _figure_html(fig: dict | None) -> str:
    """Wrap image, inline-SVG, or video media in a white panel so dark lines
    and text stay legible in dark mode. Video figures get hover controls for
    play/pause and zoom; image figures keep the click-to-enlarge behavior."""
    if not fig:
        return ""
    path = fig.get("path", "")
    alt = fig.get("alt", "")
    caption = fig.get("caption", "")
    media_type = "video" if _is_video_figure(fig) else (fig.get("media_type") or fig.get("type") or "").lower()
    # Prefer inline SVG markup when explicitly provided (svg_inline + svg key);
    # otherwise reference the file at `path` via <img>. Browsers render .svg
    # files via <img> cleanly, so figures with source: "svg_inline" + a .svg
    # file path also work.
    inline_svg = fig.get("svg") if fig.get("source") == "svg_inline" else None
    if media_type == "video":
        poster = fig.get("poster", "")
        preload = fig.get("preload", "metadata")
        attr_bits = [
            f'class="figure-video"',
            f'src="{esc(path)}"',
            f'aria-label="{esc(alt)}"',
            f'preload="{esc(preload)}"',
            "playsinline",
            "muted" if fig.get("muted", True) else "",
            "loop" if fig.get("loop", True) else "",
            "autoplay" if fig.get("autoplay", True) else "",
            f'poster="{esc(poster)}"' if poster else "",
        ]
        attrs = " ".join(bit for bit in attr_bits if bit)
        body = f'''
          <video {attrs}></video>
          <div class="figure-video-controls" aria-label="Video controls">
            <button type="button" class="figure-video-control" data-video-toggle aria-label="Pause video" title="Pause video">
              <span class="video-icon video-icon-pause" aria-hidden="true"></span>
            </button>
            <button type="button" class="figure-video-control" data-video-zoom aria-label="Zoom video" title="Zoom video">
              <span aria-hidden="true">&#8981;</span>
            </button>
          </div>'''
    elif inline_svg:
        body = inline_svg
    else:
        body = f'<img src="{esc(path)}" alt="{esc(alt)}" style="max-width:100%;height:auto;display:block;margin:0 auto;cursor:zoom-in;">'
    panel_class = "figure-panel figure-panel--video" if media_type == "video" else "figure-panel"
    video_attr = ' data-video-figure="true"' if media_type == "video" else ""
    role = "group" if media_type == "video" else "button"
    aria_label = "Video figure" if media_type == "video" else "Zoom figure"
    panel_style = (
        "background:#ffffff;"
        "border-radius:12px;"
        "padding:14px;"
        "box-shadow:var(--card-shadow);"
        "display:flex;"
        "align-items:center;"
        "justify-content:center;"
    )
    return f'''
      <div class="figure-wrap animate-in" style="margin-top:8px;">
        <div class="{panel_class}" data-zoomable-figure="true"{video_attr} tabindex="0" role="{role}" aria-label="{aria_label}: {esc(alt)}" style="{panel_style}">
          {body}
        </div>
        {f'<p style="font-size:0.8rem;color:var(--text-muted);margin-top:8px;line-height:1.45;">{esc(caption)}</p>' if caption else ""}
      </div>'''


def _compact_table_html(table: dict | None) -> str:
    if not table:
        return ""
    columns = table.get("columns", [])
    rows = table.get("rows", [])
    if not columns or not rows:
        return ""
    header = "".join(f'<th scope="col">{esc(column)}</th>' for column in columns)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(value)}</td>" for value in row) + "</tr>"
        for row in rows
    )
    title = table.get("title")
    return f'''
          <div class="compact-data-table animate-in">
            {f'<h3>{esc(title)}</h3>' if title else ""}
            <div class="compact-data-table__scroll">
              <table>
                <thead><tr>{header}</tr></thead>
                <tbody>{body}</tbody>
              </table>
            </div>
          </div>'''


def render_content_two_column(slide: dict, course: dict, module: dict) -> str:
    label = slide.get("section_label")
    compact_table = slide.get("compact_table")
    slide_class = "slide slide--mobile-scroll" if compact_table or slide.get("mobile_scroll") else "slide"
    column_class = "two-column two-column--with-table" if compact_table else "two-column"
    video_attr = ' data-video-slide="true"' if _is_video_figure(slide.get("figure")) else ""
    return f'''
  <div class="{slide_class}" data-slide="{slide["id"]}"{video_attr}>
    <div class="slide-content">
      {f'<span class="section-label animate-in">{esc(label)}</span>' if label else ""}
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "", module))}</h2>
      {f'<p class="slide-subtitle animate-in">{esc(slide.get("subtitle"))}</p>' if slide.get("subtitle") else ""}
      <div class="{column_class}">
        <div>
          <ul class="bullet-list animate-in">{_bullets_html(slide.get("bullets", []))}
          </ul>
          {_compact_table_html(compact_table)}
        </div>
        <div>{_figure_html(slide.get("figure"))}
        </div>
      </div>
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def render_content_grid(slide: dict, course: dict, module: dict) -> str:
    label = slide.get("section_label")
    cards = []
    for c in slide.get("cards", []):
        tone = str(c.get("tone", "")).strip().lower()
        tone = "".join(ch for ch in tone if ch.isalnum() or ch in ("-", "_"))
        card_class = "tenet-card animate-in" + (f" tenet-card--{tone}" if tone else "")
        # Optional url + link_text make a card clickable, with a visible
        # URL line under the body.
        url = c.get("url")
        link_text = c.get("link_text")
        link_html = ""
        if url and link_text:
            link_html = (
                f'<p style="margin-top:8px;font-size:0.78rem;'
                f'color:var(--ocp-green-dark,#6FA030);word-break:break-all;">'
                f'<span style="text-decoration:underline;">{esc(link_text)}</span></p>'
            )
        elif url:
            link_html = (
                f'<p style="margin-top:8px;font-size:0.78rem;'
                f'color:var(--ocp-green-dark,#6FA030);word-break:break-all;">'
                f'<span style="text-decoration:underline;">{esc(url)}</span></p>'
            )
        inner = f'''
          {f'<div class="tenet-icon">{esc(c.get("icon",""))}</div>' if c.get("icon") else ""}
          <h3>{esc(c.get("title",""))}</h3>
          <p>{esc(c.get("body",""))}</p>
          {link_html}'''
        if url:
            cards.append(f'''
        <a class="{card_class}" href="{esc(url)}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit;display:block;">{inner}
        </a>''')
        else:
            cards.append(f'''
        <div class="{card_class}">{inner}
        </div>''')
    # Allow a slide to pin its column count explicitly (e.g., 6 cards as 3x2
    # instead of the default 5+1).
    explicit = slide.get("grid_cols")
    if isinstance(explicit, int) and explicit >= 2:
        grid_cols = explicit
    else:
        grid_cols = max(2, min(5, len(slide.get("cards", [])) or 3))
    slide_class = "slide slide--mobile-scroll" if slide.get("mobile_scroll") else "slide"
    return f'''
  <div class="{slide_class}" data-slide="{slide["id"]}">
    <div class="slide-content">
      {f'<span class="section-label animate-in">{esc(label)}</span>' if label else ""}
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "", module))}</h2>
      {f'<p class="slide-subtitle animate-in">{esc(slide.get("subtitle"))}</p>' if slide.get("subtitle") else ""}
      <div class="tenets-grid" style="grid-template-columns: repeat({grid_cols}, 1fr);">{"".join(cards)}
      </div>
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def render_content_table(slide: dict, course: dict, module: dict) -> str:
    label = slide.get("section_label")
    cols = slide.get("columns", [])
    rows = slide.get("rows", [])
    header = "".join(f'<th style="text-align:left;padding:10px 14px;border-bottom:2px solid var(--ocp-green);font-size:0.85rem;color:var(--text-primary);">{esc(c)}</th>' for c in cols)
    body = ""
    for row in rows:
        cells = "".join(f'<td style="padding:10px 14px;border-bottom:1px solid var(--border-color);font-size:0.85rem;color:var(--text-secondary);">{esc(v)}</td>' for v in row)
        body += f"<tr>{cells}</tr>"
    return f'''
  <div class="slide" data-slide="{slide["id"]}">
    <div class="slide-content">
      {f'<span class="section-label animate-in">{esc(label)}</span>' if label else ""}
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "", module))}</h2>
      {f'<p class="slide-subtitle animate-in">{esc(slide.get("subtitle"))}</p>' if slide.get("subtitle") else ""}
      <div class="animate-in" style="margin-top:24px;background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:8px 4px;box-shadow:var(--card-shadow);overflow:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead><tr>{header}</tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def render_content_diagram(slide: dict, course: dict, module: dict) -> str:
    label = slide.get("section_label")
    video_attr = ' data-video-slide="true"' if _is_video_figure(slide.get("figure")) else ""
    return f'''
  <div class="slide" data-slide="{slide["id"]}"{video_attr}>
    <div class="slide-content">
      {f'<span class="section-label animate-in">{esc(label)}</span>' if label else ""}
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "", module))}</h2>
      {_figure_html(slide.get("figure"))}
      {f'<p class="slide-main-text animate-in">{esc(slide.get("caption"))}</p>' if slide.get("caption") else ""}
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def render_full_slide_image(slide: dict, course: dict, module: dict) -> str:
    fig = slide.get("figure") or {}
    path = fig.get("path", "")
    alt = fig.get("alt", "")
    return f'''
  <div class="slide slide-full-image" data-slide="{slide["id"]}">
    <div class="full-slide-figure animate-in" data-zoomable-figure="true" tabindex="0" role="button" aria-label="Zoom figure: {esc(alt)}">
      <img src="{esc(path)}" alt="{esc(alt)}">
    </div>
  </div>
'''


def render_takeaways(slide: dict, course: dict, module: dict) -> str:
    label = "Key Takeaways"
    items = "".join(
        f'''
        <li class="takeaway-item animate-in">
          <span class="check-icon">&#10003;</span>
          <p>{esc(item)}</p>
        </li>''' for item in slide.get("items", [])
    )
    return f'''
  <div class="slide" data-slide="{slide["id"]}">
    <div class="slide-content">
      <span class="section-label animate-in">{label}</span>
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "Module Summary", module))}</h2>
      <ul class="takeaway-list">{items}
      </ul>
    </div>
  </div>
'''


def _stable_int(value: str) -> int:
    return int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)


def _correct_slots(seed: str, n: int, k: int, multiple: bool) -> set[int]:
    combos = list(itertools.combinations(range(n), k))
    if multiple and 1 < k < n:
        non_edge_blocks = [
            c for c in combos
            if c != tuple(range(k)) and c != tuple(range(n - k, n))
        ]
        if non_edge_blocks:
            combos = non_edge_blocks
        non_contiguous = [
            c for c in combos
            if not all(c[i] + 1 == c[i + 1] for i in range(len(c) - 1))
        ]
        if non_contiguous:
            combos = non_contiguous
    return set(combos[_stable_int(seed + "|correct-slots") % len(combos)])


def _shuffled_choices(q: dict, module: dict, slide: dict, qid: str) -> list[dict]:
    """Return a stable per-question shuffle unless explicitly disabled."""
    choices = list(q.get("choices", []))
    if q.get("shuffle_choices") is False or len(choices) < 2:
        return choices
    seed = "|".join(
        str(part or "")
        for part in (
            course_key_for_shuffle(module),
            slide.get("id"),
            qid,
            q.get("prompt"),
        )
    )
    shuffled = [
        choice for _, choice in sorted(
            enumerate(choices),
            key=lambda item: (
                _stable_int(f"{seed}|{item[1].get('id','')}|{item[1].get('text','')}"),
                item[0],
            ),
        )
    ]
    correct = [choice for choice in shuffled if choice.get("correct")]
    incorrect = [choice for choice in shuffled if not choice.get("correct")]
    if not correct or not incorrect:
        return shuffled
    slots = _correct_slots(seed, len(shuffled), len(correct), bool(q.get("multiple")))
    correct_iter = iter(correct)
    incorrect_iter = iter(incorrect)
    return [
        next(correct_iter) if idx in slots else next(incorrect_iter)
        for idx in range(len(shuffled))
    ]


def course_key_for_shuffle(module: dict) -> str:
    return f"module{module.get('id', '')}:{module.get('title', '')}"


def render_knowledge_check(slide: dict, course: dict, module: dict) -> str:
    label = "Knowledge Check"
    questions_html = []
    for qi, q in enumerate(slide.get("questions", []), start=1):
        qid = q.get("id") or f"m{module.get('id')}_s{slide.get('id')}_q{qi}"
        multi = bool(q.get("multiple"))
        input_type = "checkbox" if multi else "radio"
        choices_html = []
        for choice in _shuffled_choices(q, module, slide, qid):
            cid = choice.get("id", "")
            input_id = f"{qid}_{cid}"
            choice_feedback = choice.get("feedback_incorrect") or choice.get("feedback") or ""
            choices_html.append(f'''
            <label class="quiz-choice" for="{esc(input_id)}">
              <input id="{esc(input_id)}" type="{input_type}" name="{esc(qid)}" value="{esc(cid)}" data-correct="{'true' if choice.get('correct') else 'false'}" data-feedback="{esc(choice_feedback)}">
              <span>{esc(choice.get("text"))}</span>
            </label>''')
        questions_html.append(f'''
        <div class="quiz-card animate-in" data-question-id="{esc(qid)}" data-multiple="{'true' if multi else 'false'}"
             data-correct-feedback="{esc(q.get("feedback_correct") or q.get("feedback") or "Correct.")}"
             data-incorrect-feedback="{esc(q.get("feedback_incorrect") or q.get("feedback") or "Review the feedback and try again.")}">
          <p class="quiz-question">{esc(q.get("prompt"))}</p>
          <div class="quiz-choices">{"".join(choices_html)}
          </div>
          <div class="quiz-actions">
            <button class="quiz-submit" type="button">Submit</button>
            <button class="quiz-retry" type="button">Retry</button>
          </div>
          <div class="quiz-feedback" aria-live="polite"></div>
        </div>''')
    return f'''
  <div class="slide" data-slide="{slide["id"]}" data-quiz-slide="true">
    <div class="slide-content">
      <span class="section-label animate-in">{label}</span>
      <h2 class="slide-title animate-in">{esc(_title_for_slide(slide, label, "Check Your Understanding", module))}</h2>
      {f'<p class="slide-subtitle animate-in">{esc(slide.get("subtitle"))}</p>' if slide.get("subtitle") else ""}
      <div class="knowledge-check-wrap">{"".join(questions_html)}
      </div>
      <p class="quiz-gate-note animate-in">Submit each question once to continue. Correct answers are not required, and retries are available.</p>
      <div class="quiz-gate-warning" role="status">Submit each question once before advancing.</div>
      {_learner_aids_html(slide, course)}
    </div>
  </div>
'''


def render_up_next(slide: dict, course: dict, module: dict) -> str:
    """End-of-module slide. Thanks the learner for completing this module and
    introduces the next one. Used on every module *except* the final one
    (which uses course_complete instead)."""
    nm = slide.get("next_module_number", module["id"] + 1)
    nt = slide.get("next_module_title", "")
    this_title = module.get("title", "")
    # The thank-you line is customizable; provide a sensible default that names this module.
    thanks = slide.get("thank_you_message") or (
        f"Thank you for completing Module {module['id']}"
        + (f": {this_title}." if this_title else ".")
    )
    # Use the standard .slide/.slide-content shell so colors follow the
    # theme (black on light, white on dark). The .slide-next class was
    # found to render blank in some browsers; avoid it. Use a vertical
    # flexbox so block children with their own max-width sit on the
    # vertical center line instead of flushing left.
    return f'''
  <div class="slide" data-slide="{slide["id"]}">
    <div class="slide-content" style="text-align:center; display:flex; flex-direction:column; align-items:center;">
      <div class="module-complete-badge animate-in" style="margin: 0 0 28px 0;">
        &#10003;&ensp;Module {module["id"]} Complete
      </div>
      <span class="section-label animate-in">Up Next</span>
      <div class="next-module-heading animate-in">
        <h2 class="slide-title">Module {nm}</h2>
        <a class="next-module-link" href="module{nm}.html" aria-label="Go to Module {nm}" title="Go to Module {nm}">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M6 5l7 7-7 7"></path>
            <path d="M12 5l7 7-7 7"></path>
          </svg>
        </a>
      </div>
      <p class="slide-subtitle animate-in" style="margin: 0 auto 32px; text-align:center;">{esc(nt)}</p>
      <p class="animate-in" style="margin: 0 auto; max-width: 680px; font-size: 1.05rem; line-height: 1.6; padding: 18px 28px; background: var(--ocp-green-subtle); border: 1px solid rgba(141,198,63,0.35); border-radius: 8px; text-align: center;">{esc(thanks)}</p>
      {_summary_items_html(slide)}
    </div>
  </div>
'''


def render_course_complete(slide: dict, course: dict, module: dict) -> str:
    """End-of-final-module slide. Thanks the learner and wraps up the course."""
    this_title = module.get("title", "")
    course_title = slide.get("course_title", course.get("course_title", ""))
    # Two messages: a per-module thanks and a course-level wrap-up.
    module_thanks = slide.get("thank_you_message") or (
        f"Thank you for completing Module {module['id']}"
        + (f": {this_title}." if this_title else ".")
    )
    wrap_up = slide.get("cert_message") or (
        f"You've completed every module of {course_title}. "
        "We hope this course leaves you ready to put what you've learned into practice."
    )
    # Survey CTA — invariant URL and body baked into the skill so every
    # OCP Academy course gets the same feedback ask. These constants must
    # not be changed by per-course course.json overrides. button_text
    # alone remains customizable via slide.survey.button_text (defaults
    # to "Share Feedback").
    SURVEY_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf-IDIuFSXbRk-nks90x7J_4-iiZ6vEvmmNQoVps3ySP6UFmg/viewform?usp=header"
    SURVEY_BODY = (
        "Got a couple minutes to help us improve? Help us shape "
        "improvements and our future courses by sharing your feedback "
        "with our development team. We periodically select submitters "
        "at random for great giveaways!"
    )
    survey = slide.get("survey") or {}
    survey_button = survey.get("button_text", "Share Feedback")
    survey_html = f'''
      <div class="survey-cta animate-in" style="max-width: 680px; margin: 18px auto 0; padding: 18px 24px; background: var(--bg-card); border: 1px solid var(--ocp-green); border-radius: 12px; box-shadow: var(--card-shadow); text-align: center;">
        <p style="font-size: 1.0rem; line-height: 1.45; margin: 0 0 12px 0; color: var(--text-primary);">{esc(SURVEY_BODY)}</p>
        <a class="survey-btn" href="{esc(SURVEY_URL)}" target="_blank" rel="noopener" style="display: inline-block; padding: 10px 24px; background: var(--ocp-green); color: #ffffff; text-decoration: none; font-weight: 700; font-size: 0.95rem; letter-spacing: 0.05em; border-radius: 8px; transition: background 0.15s ease;">{esc(survey_button)} &#8594;</a>
      </div>'''
    # Same centering treatment as render_up_next.
    return f'''
  <div class="slide" data-slide="{slide["id"]}">
    <div class="slide-content" style="text-align:center; display:flex; flex-direction:column; align-items:center;">
      <div class="module-complete-badge animate-in" style="margin: 0 0 18px 0;">
        &#10003;&ensp;Module {module["id"]} Complete
      </div>
      <p class="animate-in" style="margin: 0 auto 20px; max-width: 680px; font-size: 1.05rem; line-height: 1.5; padding: 14px 24px; background: var(--ocp-green-subtle); border: 1px solid rgba(141,198,63,0.35); border-radius: 8px; text-align: center;">{esc(module_thanks)}</p>
      <span class="section-label animate-in">Course Complete</span>
      <h2 class="slide-title animate-in" style="margin: 0 0 6px 0; text-align:center;">{esc(course_title)}</h2>
      <p class="slide-subtitle animate-in" style="margin: 0 auto 18px; text-align:center;">{esc(wrap_up)}</p>
      <div class="module-complete-badge animate-in" style="margin: 0;">
        &#10003;&ensp;All Modules Complete
      </div>
      {_summary_items_html(slide)}{survey_html}
    </div>
  </div>
'''


RENDERERS = {
    "title": render_title,
    "course_overview": render_course_overview,
    "objectives": render_objectives,
    "content_bullets": render_content_bullets,
    "content_two_column": render_content_two_column,
    "content_grid": render_content_grid,
    "content_table": render_content_table,
    "content_diagram": render_content_diagram,
    "full_slide_image": render_full_slide_image,
    "takeaways": render_takeaways,
    "knowledge_check": render_knowledge_check,
    "up_next": render_up_next,
    "course_complete": render_course_complete,
}


def validate_knowledge_check_audio(module: dict) -> None:
    missing = []
    for slide in module.get("slides", []):
        if slide.get("type") != "knowledge_check":
            continue
        audio = slide.get("audio") or {}
        if not audio.get("script_file") or not audio.get("wav_file"):
            missing.append(
                f"M{module.get('id')}S{slide.get('id')} "
                f"({slide.get('slug', 'knowledge_check')})"
            )
    if missing:
        joined = "\n  - ".join(missing)
        raise ValueError(
            "Knowledge-check slides must include narration metadata before rendering.\n"
            "Add audio.script_file and audio.wav_file, generate the matching WAV, "
            f"then render again:\n  - {joined}"
        )


def render_module(course: dict, module_index: int) -> str:
    """Return full HTML string for moduleN.html."""
    module = course["modules"][module_index]
    validate_knowledge_check_audio(module)
    module_num = module["id"]
    slides_html = []
    audio_map_entries = []
    for slide in module["slides"]:
        renderer = RENDERERS.get(slide["type"])
        if renderer is None:
            raise ValueError(f"Unknown slide type: {slide['type']}")
        slides_html.append(renderer(slide, course, module))
        audio = slide.get("audio") or {}
        wav = audio.get("wav_file")
        if wav:
            audio_map_entries.append(f'    {slide["id"]}: {json.dumps(wav)},')

    audio_map = "\n".join(audio_map_entries).rstrip(",")
    css = load_styles()
    course_title = course.get("course_title", "Course")
    module_title = module.get("title", "")
    badge_logo = course.get("brand", {}).get("course_logo", "")

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script src="scorm_api.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(course_title)} - Module {module_num}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body{motion_intro_body_class(course, "modules")}>
{render_motion_intro(course, "modules", module)}
{motion_intro_noscript_style()}
<div class="module-badge">
  <div class="module-badge-logo">
    {f'<img src="{esc(badge_logo)}" alt="course logo">' if badge_logo else ""}
    {_badge_text_html(course)}
  </div>
  <div class="module-badge-text">Module {module_num}</div>
</div>

<div class="deck" id="deck">
{"".join(slides_html)}
</div>

<!-- ===== CONTROLS BAR ===== -->
<div class="progress-bar" id="progressBar"></div>
<div class="controls">
  <div class="controls-left">
    <span class="theme-label">Theme</span>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"></button>
    <span class="key-hint">D</span>
  </div>
  <div class="controls-center">
    <button class="btn btn-nav" id="prevBtn" aria-label="Previous slide" disabled>&#8592;</button>
    <span class="slide-counter" id="slideCounter">1 / {len(module["slides"])}</span>
    <button class="btn btn-nav" id="nextBtn" aria-label="Next slide">&#8594;</button>
  </div>
  <div class="controls-right">
    <div class="audio-controls">
      <button class="btn-audio" id="audioPlayBtn" aria-label="Play/Pause narration" title="Play/Pause (P)">&#9654;</button>
      <div class="audio-progress-wrap" id="audioProgressWrap">
        <div class="audio-progress-fill" id="audioProgressFill"></div>
      </div>
      <span class="audio-time" id="audioTime">0:00</span>
      <div class="audio-speed-wrap" id="audioSpeedWrap">
        <button class="btn-audio-speed" id="audioSpeedBtn" aria-label="Playback speed" title="Playback speed" aria-haspopup="true" aria-expanded="false">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 16a8 8 0 1 1 16 0"/><line x1="12" y1="16" x2="16" y2="11"/><circle cx="12" cy="16" r="1.2" fill="currentColor"/></svg>
        </button>
        <div class="audio-speed-popup" id="audioSpeedPopup" role="dialog" aria-label="Playback speed">
          <div class="audio-speed-popup-label">Speed <span class="audio-speed-popup-value" id="audioSpeedValue">1.0&times;</span></div>
          <input type="range" id="audioSpeedSlider" min="0.8" max="1.6" step="0.1" value="1.0" aria-label="Playback speed slider">
          <div class="audio-speed-popup-scale"><span>0.8&times;</span><span>1.2&times;</span><span>1.6&times;</span></div>
        </div>
      </div>
    </div>
    <button class="btn" id="fullscreenBtn" aria-label="Toggle fullscreen" title="Fullscreen (F)">
      <svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
    </button>
    <span class="key-hint">F</span>
  </div>
</div>

{motion_intro_script()}
<script>
(function() {{
  'use strict';
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentSlide = 1;
  const counter = document.getElementById('slideCounter');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const progressBar = document.getElementById('progressBar');
  const themeToggle = document.getElementById('themeToggle');
  const fullscreenBtn = document.getElementById('fullscreenBtn');

  function syncSlideVideos(activeSlideNumber, restartActive) {{
    slides.forEach(function(slide) {{
      const video = slide.querySelector('video.figure-video');
      if (!video) return;
      const isActive = slide.dataset.slide === String(activeSlideNumber);
      if (!isActive) {{
        video.pause();
        video.currentTime = 0;
        return;
      }}
      if (restartActive) video.currentTime = 0;
      if (video.hasAttribute('autoplay')) video.play().catch(function() {{}});
    }});
  }}

  function goToSlide(n, direction) {{
    if (n < 1 || n > totalSlides || n === currentSlide) return;
    const oldSlide = document.querySelector('.slide.active');
    const newSlide = document.querySelector(`.slide[data-slide="${{n}}"]`);
    if (oldSlide) {{
      oldSlide.classList.remove('active');
      if (direction === 'forward') oldSlide.classList.add('exit-left');
      setTimeout(() => oldSlide.classList.remove('exit-left'), 600);
    }}
    requestAnimationFrame(() => newSlide.classList.add('active'));
    currentSlide = n;
    syncSlideVideos(currentSlide, true);
    updateControls();
    if (typeof loadSlideAudio === 'function') loadSlideAudio(n);
    if (typeof checkCompletion === 'function') checkCompletion();
  }}

  function updateFirstSlideAudioCue() {{
    document.body.classList.toggle('first-slide-audio-cue', currentSlide === 1);
  }}

  function updateControls() {{
    counter.textContent = `${{currentSlide}} / ${{totalSlides}}`;
    prevBtn.disabled = currentSlide === 1;
    nextBtn.disabled = currentSlide === totalSlides;
    progressBar.style.width = `${{(currentSlide / totalSlides) * 100}}%`;
    updateFirstSlideAudioCue();
  }}

  function currentQuizAttempted() {{
    const slide = document.querySelector(`.slide[data-slide="${{currentSlide}}"]`);
    if (!slide || slide.dataset.quizSlide !== 'true') return true;
    const cards = Array.from(slide.querySelectorAll('.quiz-card'));
    const attempted = cards.length > 0 && cards.every(card => card.dataset.attempted === 'true');
    slide.classList.toggle('quiz-needs-attempt', !attempted);
    return attempted;
  }}

  function nextSlide() {{
    if (!currentQuizAttempted()) return;
    goToSlide(currentSlide + 1, 'forward');
  }}
  function prevSlide() {{ goToSlide(currentSlide - 1, 'backward'); }}

  function toggleTheme() {{
    const htmlEl = document.documentElement;
    const isDark = htmlEl.getAttribute('data-theme') === 'dark';
    htmlEl.setAttribute('data-theme', isDark ? 'light' : 'dark');
    localStorage.setItem('ocp-deck-theme', isDark ? 'light' : 'dark');
  }}

  function toggleFullscreen() {{
    if (!document.fullscreenElement) {{
      document.documentElement.requestFullscreen().catch(() => {{}});
    }} else {{
      document.exitFullscreen();
    }}
  }}

  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    switch(e.key) {{
      case 'ArrowRight': case ' ': e.preventDefault(); nextSlide(); break;
      case 'ArrowLeft': e.preventDefault(); prevSlide(); break;
      case 'f': case 'F': e.preventDefault(); toggleFullscreen(); break;
      case 'd': case 'D': e.preventDefault(); toggleTheme(); break;
      case 'Home': e.preventDefault(); goToSlide(1, 'backward'); break;
      case 'End': e.preventDefault(); goToSlide(totalSlides, 'forward'); break;
    }}
  }});

  nextBtn.addEventListener('click', nextSlide);
  prevBtn.addEventListener('click', prevSlide);
  themeToggle.addEventListener('click', toggleTheme);
  fullscreenBtn.addEventListener('click', toggleFullscreen);

  let touchStartX = 0, touchEndX = 0;
  document.addEventListener('touchstart', (e) => {{ touchStartX = e.changedTouches[0].screenX; }}, {{ passive: true }});
  document.addEventListener('touchend', (e) => {{
    touchEndX = e.changedTouches[0].screenX;
    const diff = touchStartX - touchEndX;
    if (Math.abs(diff) > 60) {{ if (diff > 0) nextSlide(); else prevSlide(); }}
  }}, {{ passive: true }});

  const savedTheme = localStorage.getItem('ocp-deck-theme');
  if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);
  else if (window.matchMedia('(prefers-color-scheme: dark)').matches) document.documentElement.setAttribute('data-theme', 'dark');

  // ===== AUDIO NARRATION =====
  const audioMap = {{
{audio_map}
  }};

  let audioPlayer = new Audio();
  let audioPlaying = false;
  let autoPlayAudio = true;
  const audioPlayBtn = document.getElementById('audioPlayBtn');
  const audioProgressFill = document.getElementById('audioProgressFill');
  const audioProgressWrap = document.getElementById('audioProgressWrap');
  const audioTime = document.getElementById('audioTime');

  function formatTime(sec) {{
    if (!sec || isNaN(sec)) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }}

  function loadSlideAudio(slideNum) {{
    audioPlayer.pause();
    audioPlaying = false;
    audioPlayBtn.innerHTML = '&#9654;';
    audioProgressFill.style.width = '0%';
    audioTime.textContent = '0:00';
    const src = audioMap[slideNum];
    if (src) {{
      audioPlayer.src = src;
      audioPlayer.load();
      // Re-apply the saved playback rate to the new source. playbackRate
      // generally persists on HTMLMediaElement across src changes, but this
      // is a belt-and-braces guarantee that the user's slider value sticks.
      audioPlayer.playbackRate = getSavedSpeed();
      if (autoPlayAudio) {{
        audioPlayer.play().then(() => {{
          audioPlaying = true;
          audioPlayBtn.innerHTML = '&#9646;&#9646;';
        }}).catch(() => {{}});
      }}
    }}
  }}

  function toggleAudio() {{
    if (!audioPlayer.src) return;
    if (audioPlaying) {{
      audioPlayer.pause();
      audioPlaying = false;
      audioPlayBtn.innerHTML = '&#9654;';
    }} else {{
      audioPlayer.play().then(() => {{
        audioPlaying = true;
        audioPlayBtn.innerHTML = '&#9646;&#9646;';
      }}).catch(() => {{}});
    }}
  }}

  audioPlayer.addEventListener('timeupdate', () => {{
    if (audioPlayer.duration) {{
      const pct = (audioPlayer.currentTime / audioPlayer.duration) * 100;
      audioProgressFill.style.width = pct + '%';
      audioTime.textContent = formatTime(audioPlayer.currentTime);
    }}
  }});

  audioPlayer.addEventListener('ended', () => {{
    audioPlaying = false;
    audioPlayBtn.innerHTML = '&#9654;';
    audioProgressFill.style.width = '100%';
  }});

  audioProgressWrap.addEventListener('click', (e) => {{
    if (!audioPlayer.duration) return;
    const rect = audioProgressWrap.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    audioPlayer.currentTime = pct * audioPlayer.duration;
  }});

  audioPlayBtn.addEventListener('click', toggleAudio);
  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'p' || e.key === 'P') {{ e.preventDefault(); toggleAudio(); }}
  }});

  // ===== PLAYBACK SPEED =====
  // Slider 0.8-1.6 in 0.1 increments. Persisted to localStorage so the
  // setting carries across slides within the module — and across reloads.
  const SPEED_KEY = 'ocp-deck-audio-speed';
  const audioSpeedSlider = document.getElementById('audioSpeedSlider');
  const audioSpeedValue = document.getElementById('audioSpeedValue');
  const audioSpeedBtn = document.getElementById('audioSpeedBtn');

  function getSavedSpeed() {{
    const v = parseFloat(localStorage.getItem(SPEED_KEY));
    if (isNaN(v) || v < 0.8 || v > 1.6) return 1.0;
    return Math.round(v * 10) / 10;
  }}

  function applySpeed(rate) {{
    audioPlayer.playbackRate = rate;
    if (audioSpeedSlider) audioSpeedSlider.value = String(rate);
    if (audioSpeedValue) audioSpeedValue.textContent = rate.toFixed(rate === Math.floor(rate) ? 1 : 2) + '×';
    // Highlight the button when off-default so the user knows speed is engaged.
    if (audioSpeedBtn) audioSpeedBtn.classList.toggle('active', Math.abs(rate - 1.0) > 1e-6);
  }}

  applySpeed(getSavedSpeed());

  if (audioSpeedSlider) {{
    audioSpeedSlider.addEventListener('input', (e) => {{
      const rate = Math.round(parseFloat(e.target.value) * 10) / 10;
      applySpeed(rate);
      try {{ localStorage.setItem(SPEED_KEY, String(rate)); }} catch (_) {{}}
    }});
  }}

  // ===== KNOWLEDGE CHECKS =====
  let quizInteractionIndex = 0;

  function getSuspendObject() {{
    var data = SCORM.getSuspendData();
    var obj = {{ modules: [] }};
    try {{ if (data) obj = JSON.parse(data); }} catch(e) {{}}
    if (!obj || typeof obj !== 'object') obj = {{ modules: [] }};
    if (!obj.modules) obj.modules = [];
    if (!obj.quizzes) obj.quizzes = {{}};
    return obj;
  }}

  function writeSuspendObject(obj) {{
    SCORM.setSuspendData(JSON.stringify(obj));
  }}

  function selectedInputs(card) {{
    return Array.from(card.querySelectorAll('input:checked'));
  }}

  function selectedChoiceIds(card) {{
    return selectedInputs(card).map(input => input.value).sort();
  }}

  function correctChoiceIds(card) {{
    return Array.from(card.querySelectorAll('input[data-correct="true"]')).map(input => input.value).sort();
  }}

  function sameArray(a, b) {{
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
    return true;
  }}

  function selectedChoiceFeedback(card) {{
    if (card.dataset.multiple === 'true') return '';
    const input = selectedInputs(card)[0];
    return input && input.dataset.feedback ? input.dataset.feedback : '';
  }}

  function saveQuizState(questionId, selected, isCorrect) {{
    var obj = getSuspendObject();
    if (!obj.quizzes) obj.quizzes = {{}};
    obj.quizzes[questionId] = {{
      module: {module_num},
      selected: selected,
      correct: !!isCorrect,
      attempted: true
    }};
    writeSuspendObject(obj);
  }}

  function recordQuizInteraction(questionId, selected, correctIds, isCorrect) {{
    if (!SCORM.setValue) return;
    var count = parseInt(SCORM.getValue ? SCORM.getValue('cmi.interactions._count') : '', 10);
    if (isNaN(count)) count = quizInteractionIndex;
    var idx = Math.max(count, quizInteractionIndex);
    quizInteractionIndex = idx + 1;
    var studentResponse = selected.join(',');
    var correctPattern = correctIds.join(',');
    SCORM.setValue('cmi.interactions.' + idx + '.id', questionId);
    SCORM.setValue('cmi.interactions.' + idx + '.type', 'choice');
    SCORM.setValue('cmi.interactions.' + idx + '.student_response', studentResponse);
    SCORM.setValue('cmi.interactions.' + idx + '.correct_responses.0.pattern', correctPattern);
    SCORM.setValue('cmi.interactions.' + idx + '.result', isCorrect ? 'correct' : 'wrong');
    SCORM.setValue('cmi.interactions.' + idx + '.latency', '00:00:00');
  }}

  function applyQuizFeedback(card, isCorrect) {{
    const box = card.querySelector('.quiz-feedback');
    if (!box) return;
    box.classList.remove('correct', 'incorrect');
    box.classList.add(isCorrect ? 'correct' : 'incorrect');
    box.textContent = isCorrect
      ? card.dataset.correctFeedback
      : (selectedChoiceFeedback(card) || card.dataset.incorrectFeedback);
  }}

  function restoreQuizState() {{
    var obj = getSuspendObject();
    var quizzes = obj.quizzes || {{}};
    document.querySelectorAll('.quiz-card').forEach(card => {{
      const qid = card.dataset.questionId;
      const state = quizzes[qid];
      if (!state || !state.attempted) return;
      card.dataset.attempted = 'true';
      (state.selected || []).forEach(value => {{
        const input = card.querySelector('input[value="' + CSS.escape(value) + '"]');
        if (input) input.checked = true;
      }});
      applyQuizFeedback(card, !!state.correct);
    }});
  }}

  function setupKnowledgeChecks() {{
    document.querySelectorAll('.quiz-card').forEach(card => {{
      const submit = card.querySelector('.quiz-submit');
      const retry = card.querySelector('.quiz-retry');
      if (submit) submit.addEventListener('click', () => {{
        const selected = selectedChoiceIds(card);
        const correct = correctChoiceIds(card);
        if (selected.length === 0) {{
          applyQuizFeedback(card, false);
          const box = card.querySelector('.quiz-feedback');
          if (box) box.textContent = 'Select at least one answer, then submit.';
          return;
        }}
        const isCorrect = sameArray(selected, correct);
        card.dataset.attempted = 'true';
        const slide = card.closest('.slide');
        if (slide) slide.classList.remove('quiz-needs-attempt');
        applyQuizFeedback(card, isCorrect);
        saveQuizState(card.dataset.questionId, selected, isCorrect);
        recordQuizInteraction(card.dataset.questionId, selected, correct, isCorrect);
      }});
      if (retry) retry.addEventListener('click', () => {{
        card.querySelectorAll('input').forEach(input => {{ input.checked = false; }});
        delete card.dataset.attempted;
        const box = card.querySelector('.quiz-feedback');
        if (box) {{
          box.textContent = '';
          box.classList.remove('correct', 'incorrect');
        }}
      }});
    }});
  }}

  // SCORM integration
  SCORM.init();
  var existingStatus = SCORM.getStatus();
  if (existingStatus !== 'completed' && existingStatus !== 'passed') {{
    SCORM.setIncomplete();
  }}
  SCORM.setLocation('module{module_num}');
  restoreQuizState();
  setupKnowledgeChecks();

  function checkCompletion() {{
    if (currentSlide === totalSlides) {{
      var completed = getSuspendObject();
      if (!completed.modules) completed.modules = [];
      if (completed.modules.indexOf({module_num}) === -1) {{
        completed.modules.push({module_num});
      }}
      writeSuspendObject(completed);
      SCORM.setCompleted();
    }}
  }}

  window.addEventListener('beforeunload', function() {{ SCORM.finish(); }});

  syncSlideVideos(currentSlide, true);
  updateControls();
  document.addEventListener('click', function initAudio() {{
    loadSlideAudio(currentSlide);
    document.removeEventListener('click', initAudio);
  }}, {{ once: true }});
}})();
</script>
<!-- Click-to-enlarge lightbox for figures -->
<script>
(function() {{
  function syncVideoToggle(panel) {{
    if (!panel) return;
    var video = panel.querySelector('video.figure-video');
    var button = panel.querySelector('[data-video-toggle]');
    if (!video || !button) return;
    var paused = video.paused;
    button.innerHTML = paused ? '<span class="video-icon video-icon-play" aria-hidden="true"></span>' : '<span class="video-icon video-icon-pause" aria-hidden="true"></span>';
    button.setAttribute('aria-label', paused ? 'Play video' : 'Pause video');
    button.setAttribute('title', paused ? 'Play video' : 'Pause video');
  }}
  function openLightbox(panel) {{
    var overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-label', 'Enlarged figure');
    var frame = document.createElement('div');
    frame.className = 'lightbox-figure';
    frame.innerHTML = panel.innerHTML;
    if (panel.hasAttribute('data-video-figure')) {{
      frame.classList.add('figure-panel', 'figure-panel--video');
      frame.setAttribute('data-zoomable-figure', 'true');
      frame.setAttribute('data-video-figure', 'true');
    }}
    overlay.appendChild(frame);
    var hint = document.createElement('div');
    hint.className = 'lightbox-hint';
    hint.textContent = 'Click outside or press Esc to close';
    overlay.appendChild(hint);
    overlay.addEventListener('click', function(e) {{
      if (!e.target.closest('.lightbox-figure')) closeLightbox();
    }});
    document.body.appendChild(overlay);
    var sourceVideo = panel.querySelector('video.figure-video');
    var lightboxPanel = frame;
    var lightboxVideo = frame.querySelector('video.figure-video');
    if (sourceVideo && lightboxVideo) {{
      lightboxVideo.currentTime = sourceVideo.currentTime || 0;
      if (sourceVideo.paused) {{
        lightboxVideo.pause();
      }} else {{
        lightboxVideo.play().catch(function() {{}});
      }}
      syncVideoToggle(lightboxPanel);
    }}
    document.addEventListener('keydown', escClose);
  }}
  function closeLightbox() {{
    var o = document.querySelector('.lightbox-overlay');
    if (o) o.remove();
    document.removeEventListener('keydown', escClose);
  }}
  function escClose(e) {{ if (e.key === 'Escape') closeLightbox(); }}
  function figurePanelFromEventTarget(target) {{
    if (!target || !target.closest) return null;
    return target.closest('.figure-panel[data-zoomable-figure="true"]');
  }}
  document.addEventListener('click', function(e) {{
    var toggle = e.target.closest && e.target.closest('[data-video-toggle]');
    if (toggle) {{
      e.preventDefault();
      e.stopPropagation();
      var togglePanel = figurePanelFromEventTarget(toggle);
      var video = togglePanel && togglePanel.querySelector('video.figure-video');
      if (video) {{
        if (video.paused) {{
          video.play().catch(function() {{}});
        }} else {{
          video.pause();
        }}
        syncVideoToggle(togglePanel);
      }}
      return;
    }}
    var zoomButton = e.target.closest && e.target.closest('[data-video-zoom]');
    if (zoomButton) {{
      e.preventDefault();
      e.stopPropagation();
      if (zoomButton.closest('.lightbox-overlay')) return;
      var zoomPanel = figurePanelFromEventTarget(zoomButton);
      if (zoomPanel) openLightbox(zoomPanel);
      return;
    }}
    if (e.target.closest && e.target.closest('.lightbox-overlay')) return;
    var panel = figurePanelFromEventTarget(e.target);
    if (panel) {{
      e.stopPropagation();
      openLightbox(panel);
    }}
  }});
  document.addEventListener('keydown', function(e) {{
    if (e.key !== 'Enter' && e.key !== ' ') return;
    if (e.target.closest && e.target.closest('.figure-video-control')) return;
    if (e.target.closest && e.target.closest('.lightbox-overlay')) return;
    var panel = figurePanelFromEventTarget(e.target);
    if (panel) {{
      e.preventDefault();
      openLightbox(panel);
    }}
  }});
  document.addEventListener('play', function(e) {{
    if (e.target && e.target.matches && e.target.matches('video.figure-video')) {{
      syncVideoToggle(figurePanelFromEventTarget(e.target));
    }}
  }}, true);
  document.addEventListener('pause', function(e) {{
    if (e.target && e.target.matches && e.target.matches('video.figure-video')) {{
      syncVideoToggle(figurePanelFromEventTarget(e.target));
    }}
  }}, true);
  document.querySelectorAll('.figure-panel[data-video-figure="true"]').forEach(syncVideoToggle);
}})();
</script>
</body>
</html>
'''


def main():
    p = argparse.ArgumentParser()
    p.add_argument("course_json", type=Path)
    p.add_argument("--module", type=int, help="1-based module number")
    p.add_argument("--all", action="store_true")
    p.add_argument("--out", type=Path)
    args = p.parse_args()

    course = json.loads(args.course_json.read_text())
    out_dir = args.course_json.resolve().parent

    if args.all:
        for i, mod in enumerate(course["modules"]):
            html_s = render_module(course, i)
            (out_dir / f'module{mod["id"]}.html').write_text(html_s)
            print(f'wrote module{mod["id"]}.html')
    else:
        if args.module is None:
            sys.exit("Specify --module N or --all")
        idx = args.module - 1
        if idx < 0 or idx >= len(course["modules"]):
            sys.exit(f"Module {args.module} out of range (1..{len(course['modules'])})")
        html_s = render_module(course, idx)
        out_path = args.out or (out_dir / f'module{course["modules"][idx]["id"]}.html')
        out_path.write_text(html_s)
        print(f'wrote {out_path}')


if __name__ == "__main__":
    main()

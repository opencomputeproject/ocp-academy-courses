#!/usr/bin/env python3
"""
render_index.py — render the course home (index.html) and the SCORM manifest
(imsmanifest.xml) from course.json. Run after render_module.py.

Usage:
    python render_index.py <course.json>

Writes index.html and imsmanifest.xml next to course.json.

The manifest now derives audio file listings from course.json
(slides[*].audio.wav_file) rather than walking the filesystem, so the manifest
is correct even if render_index.py is run before gen_audio.py. (Strict LMSes
reject zips containing files not listed in the manifest — and audio files
referenced by audioMap MUST be in the manifest's per-module resource block.)
"""

from __future__ import annotations
import argparse
import html
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
from motion_intro import (
    load_motion_intro_css,
    motion_intro_body_class,
    motion_intro_enabled,
    motion_intro_logo,
    motion_intro_noscript_style,
    motion_intro_script,
    render_motion_intro,
)
from render_scrolling import is_scrolling, render_scrolling_course, runtime_files

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "templates"


def esc(s):
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def ui(course: dict, key: str, default: str) -> str:
    """Return an optional course-localized interface label."""
    return str((course.get("ui_labels") or {}).get(key, default))


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
    "zh-cn": "Chinese (Simplified)",
    "zh-sg": "Chinese (Simplified)",
    "zh-hans": "Chinese (Simplified)",
    "zh-hk": "Chinese (Traditional)",
    "zh-tw": "Chinese (Traditional)",
    "zh-hant": "Chinese (Traditional)",
}


def scorm_metadata_title(course: dict) -> str:
    """Return the LMS-facing title without changing learner-facing HTML."""
    course_title = str(course.get("course_title") or "OCP Academy Course")
    explicit = str(course.get("scorm_title") or "").strip()
    if explicit:
        return explicit

    language = str(course.get("language") or "en").strip().lower().replace("_", "-")
    parts = language.split("-")
    primary = parts[0]
    script_tag = "-".join(parts[:2]) if len(parts) > 1 and len(parts[1]) == 4 else ""
    if primary in ("", "en"):
        return course_title

    language_name = str(course.get("metadata_language_name") or "").strip()
    if not language_name:
        language_name = (
            LANGUAGE_NAMES.get(language)
            or (LANGUAGE_NAMES.get(script_tag) if script_tag else None)
            or LANGUAGE_NAMES.get(primary)
            or language
        )
    suffix = f"({language_name})"
    return course_title if course_title.endswith(suffix) else f"{course_title} {suffix}"


def render_index_html(course: dict, resource_root: Path | None = None) -> str:
    if is_scrolling(course):
        return render_scrolling_course(course, resource_root)
    css = (TEMPLATE_DIR / "index_styles.css").read_text()
    css += "\n\n" + load_motion_intro_css(TEMPLATE_DIR)
    course_title = course.get("course_title", "OCP Academy Course")
    course_subtitle = course.get("course_subtitle", "")
    # Brand tenet: the index tagline is fixed. CSS renders all caps;
    # store the phrase in mixed case.
    tagline = course.get("tagline") or "Community-driven Hyperscale Innovation for All"
    version_chip = course.get("spec_version_chip", "")
    footer_line = course.get("index_footer_line") or (
        course_title + (f" · {version_chip}" if version_chip else "")
    )
    brand = course.get("brand", {})
    academy_logo = brand.get("academy_logo", "")
    course_logo = brand.get("course_logo", "")
    language = course.get("language") or "en"
    not_started = ui(course, "not_started", "Not Started")
    completed = ui(course, "completed", "Completed")

    cards = []
    for i, mod in enumerate(course["modules"], start=1):
        cards.append(f'''
  <a class="module-card" href="module{mod["id"]}.html" data-module="{mod["id"]}">
    <div class="module-num">{mod["id"]}</div>
    <div class="module-info">
      <h3>{esc(mod.get("title",""))}</h3>
      <p>{esc(mod.get("subtitle",""))}</p>
      <div class="status status-incomplete" id="status-{mod["id"]}">{esc(not_started)}</div>
    </div>
  </a>''')

    # Split course_title at last space to allow a colored "span" piece, matching the reference.
    parts = course_title.rsplit(" ", 1)
    if len(parts) == 2 and any(c.isdigit() or c == "." for c in parts[1]):
        title_html = f'{esc(parts[0])} <span>{esc(parts[1])}</span>'
    else:
        title_html = esc(course_title)

    return f'''<!DOCTYPE html>
<html lang="{esc(language)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(course_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="scorm_api.js"></script>
<style>
{css}
</style>
</head>
<body{motion_intro_body_class(course, "index")}>
{render_motion_intro(course, "index")}
{motion_intro_noscript_style()}

<div class="index-shell">
<div class="header">
  <div class="header-logos">
    {f'<img src="{esc(academy_logo)}" alt="OCP Academy" class="academy-logo">' if academy_logo else ""}
    {'<div class="logo-divider"></div>' if academy_logo and course_logo else ""}
    {f'<img src="{esc(course_logo)}" alt="{esc(course_title)}" class="nic-logo">' if course_logo else ""}
  </div>
  <h1>{title_html}</h1>
  {f'<p>{esc(course_subtitle)}</p>' if course_subtitle else ""}
  {f'<!-- tagline moved to footer pill -->' if tagline else ""}
</div>

<div class="modules" id="modules">
{"".join(cards)}
</div>

<div class="footer">
  {esc(footer_line)}
  {f'<br><span class="version">{esc(tagline)}</span>' if tagline else ""}
</div>
</div>

{motion_intro_script()}
<script>
(function() {{
  'use strict';
  SCORM.init();
  SCORM.setCompleted();
  var data = SCORM.getSuspendData();
  if (data) {{
    try {{
      var completed = JSON.parse(data);
      if (completed && completed.modules) {{
        completed.modules.forEach(function(m) {{
          var card = document.querySelector('[data-module="' + m + '"]');
          var status = document.getElementById('status-' + m);
          if (card) card.classList.add('completed');
          if (status) {{
            status.textContent = {json.dumps(completed, ensure_ascii=False)};
            status.className = 'status status-completed';
          }}
        }});
      }}
    }} catch(e) {{}}
  }}

  document.querySelectorAll('.module-card').forEach(function(card) {{
    card.addEventListener('click', function(e) {{
      var mod = this.getAttribute('data-module');
      SCORM.setLocation('module' + mod);
    }});
  }});

  window.addEventListener('beforeunload', function() {{ SCORM.finish(); }});
}})();
</script>
</body>
</html>
'''


def render_manifest(course: dict, out_dir: Path) -> str:
    """Build imsmanifest.xml. Audio file entries come from course.json's
    slides[*].audio.wav_file (canonical source of truth) so the manifest is
    truthful even if rendered before audio has been generated. Figures come
    from slides[*].figure.path. The manifest must list every file referenced
    by HTML pages — strict LMSes reject zips with unlisted files."""
    if is_scrolling(course):
        course_slug = course.get("course_slug", "ocp_academy_scrolling_course")
        course_title = scorm_metadata_title(course)
        files_xml = "\n      ".join(
            f'<file href="{xml_escape(path)}"/>' for path in runtime_files(course)
        )
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{xml_escape(course_slug.upper())}_MANIFEST" version="1.0"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                       http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd
                       http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="COURSE_ORG">
    <organization identifier="COURSE_ORG">
      <title>{xml_escape(course_title)}</title>
      <item identifier="ITEM_COURSE" identifierref="RES_COURSE">
        <title>{xml_escape(course_title)}</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_COURSE" type="webcontent" adlcp:scormtype="sco" href="index.html">
      {files_xml}
    </resource>
  </resources>
</manifest>
'''

    brand = course.get("brand", {})
    course_logo = brand.get("course_logo", "")
    academy_logo = brand.get("academy_logo", "")
    course_slug = course.get("course_slug", "ocp_academy_course")
    course_title = scorm_metadata_title(course)

    org_items = []
    resources = []

    # Launcher resource
    def add_file(files: list[str], value: str | None):
        if value and value not in files:
            files.append(value)

    launcher_files = ["index.html", "scorm_api.js"]
    add_file(launcher_files, course_logo)
    add_file(launcher_files, academy_logo)
    if motion_intro_enabled(course, "index"):
        add_file(launcher_files, motion_intro_logo(course, "index"))
    launcher_files_xml = "\n      ".join(f'<file href="{xml_escape(f)}"/>' for f in launcher_files)
    resources.append(f'''
    <resource identifier="RES_LAUNCHER" type="webcontent" adlcp:scormtype="sco" href="index.html">
      {launcher_files_xml}
    </resource>''')

    org_items.append('      <item identifier="ITEM_LAUNCHER" identifierref="RES_LAUNCHER">\n        <title>Course Home</title>\n      </item>')

    for mod in course["modules"]:
        mid = mod["id"]
        files = [f"module{mid}.html", "scorm_api.js"]
        add_file(files, course_logo)
        add_file(files, academy_logo)
        if motion_intro_enabled(course, "modules"):
            add_file(files, motion_intro_logo(course, "modules"))
            mod_intro = mod.get("motion_intro", {})
            if isinstance(mod_intro, dict):
                add_file(files, mod_intro.get("logo"))
        # Figures/media referenced by this module's slides — but only those that
        # actually live on disk. Inline SVGs (source == "svg_inline") carry
        # a `path` for figure-plan bookkeeping but never exist as standalone
        # files, so registering them would break the manifest. Video figures
        # may also declare a poster frame; include both runtime files.
        for slide in mod.get("slides", []):
            fig = slide.get("figure")
            if not fig or not fig.get("path"):
                continue
            if fig.get("source") == "svg_inline" and fig.get("svg"):
                # Truly inline (raw SVG markup in `svg` field) — no external file
                continue
            p = fig["path"]
            if p not in files:
                files.append(p)
            poster = fig.get("poster")
            if poster and poster not in files:
                files.append(poster)
        # Audio files declared in course.json (canonical) — derive even if
        # .wav doesn't exist yet, so the manifest stays correct across renders.
        for slide in mod.get("slides", []):
            audio = slide.get("audio") or {}
            wav = audio.get("wav_file")
            if wav and wav not in files:
                files.append(wav)
        files_xml = "\n      ".join(f'<file href="{xml_escape(f)}"/>' for f in files)
        resources.append(f'''
    <resource identifier="RES_MODULE{mid}" type="webcontent" adlcp:scormtype="sco" href="module{mid}.html">
      {files_xml}
    </resource>''')
        org_items.append(f'      <item identifier="ITEM_MODULE{mid}" identifierref="RES_MODULE{mid}">\n        <title>Module {mid}: {xml_escape(mod.get("title",""))}</title>\n      </item>')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{xml_escape(course_slug.upper())}_MANIFEST" version="1.0"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                       http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd
                       http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">

  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>

  <organizations default="COURSE_ORG">
    <organization identifier="COURSE_ORG">
      <title>{xml_escape(course_title)}</title>

{chr(10).join(org_items)}

    </organization>
  </organizations>

  <resources>{"".join(resources)}
  </resources>

</manifest>
'''


def main():
    p = argparse.ArgumentParser()
    p.add_argument("course_json", type=Path)
    args = p.parse_args()
    course = json.loads(args.course_json.read_text())
    out_dir = args.course_json.resolve().parent

    (out_dir / "index.html").write_text(render_index_html(course, out_dir))
    print(f"wrote {out_dir / 'index.html'}")
    (out_dir / "imsmanifest.xml").write_text(render_manifest(course, out_dir))
    print(f"wrote {out_dir / 'imsmanifest.xml'}")


if __name__ == "__main__":
    main()

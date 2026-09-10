"""Opt-in SCORM 1.2 Slides shell; existing multi-SCO builds remain unchanged."""
import html
import json
from pathlib import Path
from xml.etree import ElementTree as ET

IMS = "http://www.imsproject.org/xsd/imscp_rootv1p1p2"
ADL = "http://www.adlnet.org/xsd/adlcp_rootv1p2"
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def enabled(course):
    config = course.get("scorm") or {}
    version = config.get("version", "1.2")
    mode = config.get("organization", "multi-sco")
    if version != "1.2":
        raise ValueError("Only SCORM 1.2 is implemented; do not relabel a 1.2 runtime as 2004")
    if mode not in ("multi-sco", "single-sco"):
        raise ValueError("scorm.organization must be multi-sco or single-sco")
    active = mode == "single-sco"
    if active and str(course.get("style", "Slides")).lower() != "slides":
        raise ValueError("The Slides single-SCO shell is not the Scrolling renderer")
    return active


def configuration(course):
    modules = []
    worst_state = {"academySingleSCO": 1, "modules": [], "quizzes": {}, "bookmarks": {}, "page": "index.html"}
    for module in course["modules"]:
        mid = int(module["id"])
        modules.append({"id": mid, "file": f"module{mid}.html", "quizzes": [
            str(q["id"]) for slide in module["slides"]
            for q in slide.get("questions", []) if slide.get("type") == "knowledge_check"
        ]})
        worst_state["modules"].append(mid)
        worst_state["bookmarks"][str(mid)] = f'module{mid}:slide{len(module["slides"])}'
        worst_state["page"] = f'module{mid}.html'
        for slide in module["slides"]:
            if slide.get("type") != "knowledge_check":
                continue
            for question in slide.get("questions", []):
                worst_state["quizzes"][str(question["id"])] = {
                    "module": mid, "selected": [str(c["id"]) for c in question.get("choices", [])],
                    "correct": False, "attempted": True,
                }
    if not modules or len({m["id"] for m in modules}) != len(modules):
        raise ValueError("A single-SCO course needs uniquely numbered modules")
    question_ids = [qid for module in modules for qid in module["quizzes"]]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("Single-SCO quiz question IDs must be unique across all modules")
    if len(json.dumps(worst_state, separators=(",", ":"))) > 4096:
        raise ValueError("Single-SCO progress could exceed SCORM 1.2's 4096-character limit; compact the state design before building")
    return {"slug": course["course_slug"], "modules": modules}


def render_launch(course):
    config = json.dumps(configuration(course), ensure_ascii=True).replace("<", "\\u003c")
    title = html.escape(course["course_title"], quote=True)
    language = html.escape(course.get("language", "en"), quote=True)
    return f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#fff}}
body{{display:flex;flex-direction:column}}
#courseFrame{{width:100%;flex:1;min-height:0;border:0;display:block}}
#saveWarning{{flex:0 0 auto;padding:14px;
background:#fff;color:#333;border-bottom:3px solid #8DC63F;font:16px/1.4 sans-serif}}
</style>
<script src="scorm_api.js"></script></head><body>
<div id="saveWarning" role="alert" hidden></div>
<iframe id="courseFrame" title="{title}" allow="autoplay; fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>
<noscript>This course requires JavaScript for navigation and progress tracking.</noscript>
<script id="singleSCOConfig" type="application/json">{config}</script>
<script src="single_sco_runtime.js"></script>
</body></html>
'''


def render_manifest(course, multi_manifest, title):
    """Retain the exact union of runtime assets, but expose only one launch SCO."""
    original = ET.fromstring(multi_manifest)
    files = {f.attrib["href"] for f in original.iter(f"{{{IMS}}}file")}
    files.update(("launch.html", "single_sco_runtime.js"))
    esc = lambda value: html.escape(str(value), quote=True)
    file_xml = "\n".join(f'      <file href="{esc(name)}"/>' for name in sorted(files))
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{esc(course['course_slug'].upper())}_SINGLE_SCO_MANIFEST" version="1.0"
 xmlns="{IMS}" xmlns:adlcp="{ADL}"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="{IMS} imscp_rootv1p1p2.xsd {ADL} adlcp_rootv1p2.xsd">
  <metadata><schema>ADL SCORM</schema><schemaversion>1.2</schemaversion></metadata>
  <organizations default="COURSE_ORG">
    <organization identifier="COURSE_ORG">
      <title>{esc(title)}</title>
      <item identifier="ITEM_COURSE" identifierref="RES_COURSE"><title>{esc(title)}</title></item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_COURSE" type="webcontent" adlcp:scormtype="sco" href="launch.html">
{file_xml}
    </resource>
  </resources>
</manifest>
'''


def write_runtime(course, output):
    (output / "launch.html").write_text(render_launch(course), encoding="utf-8")
    for name in ("single_sco_runtime.js", "scorm_api.js"):
        (output / name).write_bytes((ASSETS / name).read_bytes())


def validate(course, manifest, output):
    """Verify opt-in organization and session artifacts, not just XML parsing."""
    if not enabled(course):
        return []
    errors = []
    root = manifest.getroot()
    items = list(root.iter(f"{{{IMS}}}item"))
    resources = list(root.iter(f"{{{IMS}}}resource"))
    if len(items) != 1 or len(resources) != 1:
        errors.append("single-SCO Slides must expose exactly one item/resource")
    elif (resources[0].get("href") != "launch.html" or
          resources[0].get(f"{{{ADL}}}scormtype") != "sco" or
          items[0].get("identifierref") != resources[0].get("identifier")):
        errors.append("single-SCO Slides must launch the persistent launch.html session")
    if root.findtext(f"{{{IMS}}}metadata/{{{IMS}}}schemaversion") != "1.2":
        errors.append("single-SCO Slides runtime requires SCORM 1.2")
    required = {"launch.html", "single_sco_runtime.js", "scorm_api.js", "index.html"}
    required.update(m["file"] for m in configuration(course)["modules"])
    declared = {node.get("href") for node in root.iter(f"{{{IMS}}}file")}
    for name in sorted(required):
        if name not in declared or not (output / name).is_file():
            errors.append(f"single-SCO runtime missing or undeclared: {name}")
    if (output / "scorm_api.js").exists() and "AcademySingleSCO" not in (output / "scorm_api.js").read_text():
        errors.append("single-SCO runtime has a stale API adapter without session delegation")
    return errors

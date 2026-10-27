"""SCORM 2004 3rd Edition manifest and validation for standalone Scrolling."""
from html import escape

IMS = "http://www.imsglobal.org/xsd/imscp_v1p1"
ADL = "http://www.adlnet.org/xsd/adlcp_v1p3"


def enabled(course):
    config = course.get("scorm") or {}
    active = config.get("version") == "2004 3rd Edition"
    if active and str(course.get("style", "Slides")).lower() != "scrolling" and config.get('organization') != 'multi-sco':
        raise ValueError("SCORM 2004 Slides requires multi-sco organization")
    return active


def render_manifest(course, files, title):
    esc = lambda value: escape(str(value), quote=True)
    file_xml = "\n".join(f'      <file href="{esc(path)}"/>' for path in sorted(files))
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{esc(course['course_slug'].upper())}_MANIFEST" version="1.0"
 xmlns="{IMS}" xmlns:adlcp="{ADL}"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <metadata><schema>ADL SCORM</schema><schemaversion>2004 3rd Edition</schemaversion></metadata>
  <organizations default="COURSE_ORG">
    <organization identifier="COURSE_ORG">
      <title>{esc(title)}</title>
      <item identifier="ITEM_COURSE" identifierref="RES_COURSE"><title>{esc(title)}</title></item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_COURSE" type="webcontent" adlcp:scormType="sco" href="index.html">
{file_xml}
    </resource>
  </resources>
</manifest>
'''


def validate(course, tree, output):
    if not enabled(course):
        return []
    issues = []
    root = tree.getroot()
    if root.tag != f"{{{IMS}}}manifest":
        issues.append("SCORM 2004 manifest uses the wrong IMS namespace")
    if root.findtext(f"{{{IMS}}}metadata/{{{IMS}}}schemaversion") != "2004 3rd Edition":
        issues.append("SCORM 2004 manifest edition does not match course.json")
    resources = list(root.iter(f"{{{IMS}}}resource"))
    if str(course.get('style','Slides')).lower()=='slides':
        import slides_2004
        issues.extend(slides_2004.validate(course,tree))
    elif len(resources) != 1 or resources[0].get(f"{{{ADL}}}scormType") != "sco" or resources[0].get("href") != "index.html":
        issues.append("SCORM 2004 Scrolling requires exactly one index.html SCO")
    api_path = output / "scorm_api.js"
    api = api_path.read_text() if api_path.exists() else ""
    if "API_1484_11" not in api or "LMSInitialize" in api or "cmi.core." in api:
        issues.append("SCORM 2004 package must use its 2004 runtime adapter")
    return issues

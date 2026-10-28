"""Place the supplied trademark SVG above the publication teaching diagram on M2S7."""
import base64
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT
logo = ROOT / 'authoring/ocp_safe_official_tm.svg'
diagram = (ROOT / 'authoring/publication_path.svg').read_text()
diagram = re.sub(r'<svg\b[^>]*>',
                 '<svg x="0" y="150" width="790" height="240" viewBox="0 50 790 240">',
                 diagram, count=1)
encoded = base64.b64encode(logo.read_bytes()).decode()
art = ('<svg xmlns="http://www.w3.org/2000/svg" width="790" height="410" '
       'viewBox="0 0 790 410" role="img" aria-label="S.A.F.E. logo and publication process">'
       '<rect width="790" height="410" fill="white"/>'
       f'<image x="245" y="0" width="300" height="150" '
       f'href="data:image/svg+xml;base64,{encoded}"/>{diagram}</svg>')
target = COURSE / 'figures/publication_marketplace.svg'
target.write_text(art)
if '--reviewed' not in sys.argv:
    print('Figure generated. Review it, then pass --reviewed to bind its text inventory.')
    raise SystemExit(0)
# All diagram labels are unchanged. The only additional visible words belong
# to the supplied trademark SVG; preserve that original asset and its hash as provenance.
entries = [{'text': 'OCP S.A.F.E.™'}]
entries += [{'text': ' '.join(''.join(node.itertext()).split())}
            for node in ET.fromstring(art).iter()
            if node.tag.rsplit('}', 1)[-1] == 'text']
p = COURSE / 'course.json'
course = json.loads(p.read_text())
slide = next(s for m in course['modules'] if m['id'] == 2
             for s in m['slides'] if s['id'] == 7)
slide['figure']['text_inventory'] = {
    'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    'entries': entries,
    'review_record': 'User-supplied trademark SVG embedded unchanged above the reviewed publication diagram; final composite render checked on M2S7.'
}
p.write_text(json.dumps(course, indent=2, ensure_ascii=False) + '\n')
print('Built M2S7 figure with the supplied trademark SVG; course branding is unchanged.')

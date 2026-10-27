"""Use the shared Slides renderer with reviewed enlarged-video control styling."""
from pathlib import Path
import json
import os
import sys

source = Path(sys.argv[1]).resolve()
skill = os.environ.get('ACADEMY_WIZARD_SKILL_DIR')
if not skill:
    skill = next(parent / 'skills/academy-wizard' for parent in source.parents
                 if (parent / 'skills/academy-wizard').is_dir())
sys.path.insert(0, str(Path(skill) / 'scripts'))
import render_module

course = json.loads(source.read_text())
assert course['scorm']['include_home_sco'] is True
assert [module['id'] for module in course['modules']] == [1, 2, 3, 4]
base_styles = render_module.load_styles
def course_styles():
    styles = base_styles().replace('.slide .figure-video-control',
                                  ':is(.slide,.lightbox-figure) .figure-video-control')
    return styles + '\n.lightbox-figure.figure-panel--video{position:relative;display:block}.lightbox-figure [data-video-zoom]{display:none}\n'
render_module.load_styles = course_styles
for index, module in enumerate(course['modules']):
    (source.parent / f'module{module["id"]}.html').write_text(render_module.render_module(course, index))

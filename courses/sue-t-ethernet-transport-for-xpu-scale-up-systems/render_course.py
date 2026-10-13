"""Render this course with its authored figure sizes and caption layout.

Usage: python render_course.py course.json --module 2
The maintained AcademyWizard renderer supplies every other layout and control.
"""
from pathlib import Path
import argparse
import json
import os
import re
import sys

skill_override = os.environ.get('ACADEMY_WIZARD_SKILL_DIR')
if skill_override:
    skill_scripts = Path(skill_override).expanduser().resolve() / 'scripts'
else:
    skill_scripts = next(
        (parent / 'skills/academy-wizard/scripts' for parent in Path(__file__).resolve().parents
         if (parent / 'skills/academy-wizard/scripts/render_module.py').is_file()),
        Path.home() / '.codex/skills/academy-wizard/scripts',
    )
if not (skill_scripts / 'render_module.py').is_file():
    raise SystemExit('AcademyWizard renderer not found; set ACADEMY_WIZARD_SKILL_DIR')
sys.path.insert(0, str(skill_scripts))
import render_module as academy

original_figure = academy._figure_html


def figure_html(figure, course=None):
    result = original_figure(figure, course)
    if not figure:
        return result
    if figure.get('caption'):
        result = result.replace('figure-wrap animate-in', 'figure-wrap figure-wrap--captioned animate-in', 1)
        result, count = re.subn(
            r'<p style="font-size:0\.8rem;color:var\(--text-muted\);margin-top:8px;line-height:1\.45;">',
            '<p class="figure-caption">', result, count=1,
        )
        if count != 1:
            raise ValueError('The maintained figure caption markup changed; review its layout before rendering')
    if 'display_scale' not in figure:
        return result
    scale = float(figure['display_scale'])
    if not 0 < scale <= 1:
        raise ValueError('figure.display_scale must be between 0 and 1')
    if academy._is_video_figure(figure):
        raise ValueError('display_scale currently applies to static figures')
    # Halve available image width and its height cap together. Keep the 18px
    # media-frame inset and caption type at their maintained sizes.
    cap = f'calc({100 * scale:g}% + {36 * (1 - scale):g}px)'
    result = result.replace('width:fit-content;max-width:100%;', f'width:fit-content;max-width:{cap};', 1)
    if figure.get('path', '').lower().endswith('.svg'):
        result = result.replace('width:1200px;', f'width:{1200 * scale:g}px;', 1)
    else:
        result = re.sub(r'(<img\b[^>]*\bstyle=")', rf'\1max-height:{56 * scale:g}vh;', result, count=1)
    return result


academy._figure_html = figure_html

CAPTION_SCRIPT = '''
<script>
// Match the caption to the visible figure frame, including its white edge.
// Measuring the frame keeps the media and its authored scale unchanged.
// ResizeObserver also runs when a hidden slide is shown or the viewport changes.
(() => {
  const updates = [];
  document.querySelectorAll('.figure-wrap--captioned').forEach(wrap => {
    const panel = wrap.querySelector('.figure-panel');
    const media = wrap.querySelector('.figure-panel img, .figure-panel video, .figure-panel svg');
    if (!panel || !media) return;
    const update = () => {
      const width = panel.getBoundingClientRect().width;
      if (width > 0) wrap.style.setProperty('--figure-caption-width', `${width}px`);
    };
    updates.push(update);
    if (typeof ResizeObserver === 'function') {
      const observer = new ResizeObserver(update);
      observer.observe(panel);
    }
    media.addEventListener('load', update);
    media.addEventListener('loadedmetadata', update);
    update();
  });
  window.addEventListener('resize', () => updates.forEach(update => update()));
  document.addEventListener('click', () => requestAnimationFrame(() => updates.forEach(update => update())));
})();
</script>
'''


def render_module(course, index):
    result = academy.render_module(course, index)
    layout = course['figure_caption_layout']
    alignment = layout['alignment']
    if alignment not in {'left', 'center', 'right'}:
        raise ValueError('figure_caption_layout.alignment must be left, center, or right')
    css = f'''
/* Course review: captions match the figure frame; pills have a separate clear gap. */
.slide .figure-caption {{
  width:var(--figure-caption-width, 100%);
  max-width:100%;
  margin:{int(layout['media_gap_px'])}px auto 0;
  font-size:0.8rem;
  color:var(--text-muted);
  line-height:1.45;
  text-align:{alignment};
}}
.slide[data-captioned-figure="true"] .learner-aids {{
  margin-top:{int(layout['resource_gap_px'])}px;
}}
.slide[data-captioned-figure="true"] .learner-aids > :first-child {{
  margin-top:0;
}}
'''
    result = result.replace('</style>', css + '\n</style>', 1)
    for slide in course['modules'][index]['slides']:
        if (slide.get('figure') or {}).get('caption'):
            result = re.sub(
                rf'(<div class="slide[^\"]*" data-slide="{slide["id"]}")',
                r'\1 data-captioned-figure="true"', result, count=1,
            )
    return result.replace('</body>', CAPTION_SCRIPT + '\n</body>', 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('course_json', type=Path)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument('--module', type=int)
    selection.add_argument('--all', action='store_true')
    args = parser.parse_args()
    course = json.loads(args.course_json.read_text())
    indices = range(len(course['modules'])) if args.all else [args.module - 1]
    for index in indices:
        module = course['modules'][index]
        out = args.course_json.parent / f'module{module["id"]}.html'
        out.write_text(render_module(course, index))
        print('wrote', out.name)

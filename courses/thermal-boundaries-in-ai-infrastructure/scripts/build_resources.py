#!/usr/bin/env python3
"""Generate the attribution page and stage the catalog poster in the build.

Called by scripts/build-course.sh with the staged course.json path.
This hook writes only to the build directory, never the source checkout.
"""
from pathlib import Path
import shutil
import sys

SOURCE = Path(__file__).resolve().parents[1]
ATTRIBUTION_HTML = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thermal Boundaries — source attribution</title><style>body{max-width:760px;margin:60px auto;padding:0 24px;font:18px/1.65 Arial,sans-serif;color:#26334d}h1{color:#343895;font-size:32px}a{color:#343895}li{margin:8px 0}</style></head><body><h1>Source attribution</h1><p>This OCP Academy course adapts <a href="https://www.opencompute.org/wp-content/uploads/2026/10/Thermal-Boundaries-in-AI-Infrastructure.pdf" target="_blank" rel="noopener">Thermal Boundaries in AI Infrastructure</a>, published version 1.00, October 12, 2026.</p><p>Original authors: Rolf Brink (Promersion), Mohan J. Kumar (Oracle), Steve Mills (Meta), and Kelley Mullick (Avayla).</p><p>The original work is licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">Creative Commons Attribution-ShareAlike 4.0 International</a>. The adapted teaching text, narration scripts, and course-owned instructional diagrams are provided under the same license.</p><p>Changes include an instructional outline, condensed and reordered explanations, fictional review cases, knowledge checks, glossary definitions, cross references, original diagrams, and teaching animations. Source Figures 5 and 19 are cropped from rendered PDF pages, preserving their axes, labels, and plotted evidence. Source page references accompany the teaching content. The authors have not been represented as endorsing this course.</p><p>The OCP Academy logo and associated marks remain the property of their respective owners. Their inclusion does not alter applicable trademark rights.</p><p><a href="index.html">Return to the course home</a></p></body></html>\n'


def main():
    destination = Path(sys.argv[1]).resolve().parent
    if destination == SOURCE:
        raise SystemExit("Build into a separate directory; do not overwrite source files.")
    (destination / 'attribution.html').write_text(ATTRIBUTION_HTML, encoding='utf-8')
    shutil.copy2(SOURCE / 'thumbnail.png', destination / 'thumbnail.png')
    print('Generated source attribution and staged the catalog poster.')


if __name__ == '__main__':
    main()

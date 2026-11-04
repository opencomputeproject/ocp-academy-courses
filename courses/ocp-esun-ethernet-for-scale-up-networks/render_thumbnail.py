#!/usr/bin/env python3
"""Compatibility entrypoint: use the shared Academy poster standard."""
from pathlib import Path
import subprocess
import sys
here = Path(__file__).resolve().parent
course = next(p for p in (here, *here.parents) if (p / 'poster.json').is_file())
repo = next(p for p in course.parents if (p / 'skills/academy-wizard/scripts/render_lms_posters.mjs').is_file())
subprocess.run(['node', str(repo / 'skills/academy-wizard/scripts/render_lms_posters.mjs'),
                '--repo-root', str(repo), '--course', str(course), *sys.argv[1:]], check=True)

"""Stage course-owned fonts and poster through the shared build hook."""
from pathlib import Path
import shutil
import sys

source = Path(__file__).resolve().parents[1]
target = Path(sys.argv[1]).resolve().parent
shutil.copytree(source / 'assets', target / 'assets', dirs_exist_ok=True)
shutil.copy2(source / 'thumbnail.png', target / 'thumbnail.png')
print('Staged MGX local fonts and LMS poster.')

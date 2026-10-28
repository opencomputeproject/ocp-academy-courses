"""Stage course-owned offline fonts and the separate LMS poster."""
from pathlib import Path
import shutil
import sys
source = Path(__file__).resolve().parents[1]
output = Path(sys.argv[1]).resolve().parent
shutil.copytree(source / 'assets', output / 'assets', dirs_exist_ok=True)
shutil.copy2(source / 'thumbnail.png', output / 'thumbnail.png')

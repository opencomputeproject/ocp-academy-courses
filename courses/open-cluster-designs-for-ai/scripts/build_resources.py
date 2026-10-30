"""Stage course-owned fonts and branding without touching source or narration."""
from pathlib import Path
import shutil,sys
source=Path(__file__).resolve().parents[1]
target=Path(sys.argv[1]).resolve().parent
if source==target:raise SystemExit('Build into a separate folder.')
shutil.copytree(source/'assets',target/'assets',dirs_exist_ok=True)
for name in ['open_cluster_mark.svg','thumbnail.png']:shutil.copy2(source/name,target/name)

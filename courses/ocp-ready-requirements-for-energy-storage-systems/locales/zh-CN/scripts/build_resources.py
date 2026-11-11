"""Use the canonical course's reviewed-media preflight."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parents[3] / 'scripts/build_resources.py'), run_name='__main__')

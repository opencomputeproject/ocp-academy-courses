"""Record reviewed finite sources with the shared lossless recorder."""
from pathlib import Path
import argparse,json,os,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--modules',nargs='+',type=int,default=[1,2,3,4,5])
args=parser.parse_args()
skill=Path(os.environ.get('ACADEMY_WIZARD_SKILL_DIR',ROOT.parents[1]/'skills/academy-wizard'))
for n in args.modules:
    timing=json.loads((ROOT/f'animations/m{n}_timing.json').read_text())
    if not timing['measured_audio']:raise SystemExit(f'Module {n} lacks final measured audio')
    subprocess.run(['node',str(skill/'scripts/record_css_animation.mjs'),str(ROOT/f'animations/m{n}_teaching_animation.html'),str(ROOT/f'figures/m{n}_teaching_animation.mp4'),str(ROOT/f'figures/m{n}_teaching_animation_poster.png'),str(timing['durationMs']),str(timing['posterMs']),'30'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/correct_color_metadata.py'),'--modules',*[str(n) for n in args.modules]],check=True)

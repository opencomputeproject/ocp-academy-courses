"""Decode the reviewed course excerpts needed by build_promo.py."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'animations'))
from build_media import find_ffmpeg

RECIPES = [
    ('cad', 'hpm_exploded', 42.5, 8, 7, (940, 140, 730, 610)),
    ('float', 'blind_mate_float', 16, 25.5, 4, (730, 160, 1100, 713)),
    ('busbar', 'busbar_layers', 4, 10, 4, (715, 240, 1125, 415)),
    ('force', 'force_budget', 20, 36, 2.5, None),
]

for name, video, start, source_duration, target_duration, crop in RECIPES:
    output = ROOT / '_analysis/promo_frames' / name
    output.mkdir(parents=True, exist_ok=True)
    # Remove stale decoded frames if a previous recipe had a different length.
    for old in output.glob('*.png'):
        old.unlink()
    filters = [f'setpts=(PTS-STARTPTS)/({source_duration}/{target_duration})', 'fps=30']
    if crop:
        x, y, width, height = crop
        filters.append(f'crop={width}:{height}:{x}:{y}')
    subprocess.run([find_ffmpeg(), '-y', '-loglevel', 'error',
        '-ss', str(start), '-t', str(source_duration),
        '-i', str(ROOT / 'figures' / (video + '.mp4')),
        '-vf', ','.join(filters), '-frames:v', str(round(target_duration * 30)),
        str(output / '%04d.png')], check=True)
    assert len(list(output.glob('*.png'))) == round(target_duration * 30), name
    print('Prepared', name, flush=True)

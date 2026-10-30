"""Reproduce the two source-figure crops from the published January XOC-N PDF.
Usage: python3 scripts/extract_xoc_source_figures.py /path/to/xoc-n.pdf
Requires pdftoppm and Pillow. The original research PDF remains outside Git.
"""
from pathlib import Path
from PIL import Image
import argparse,hashlib,subprocess,tempfile
p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);a=p.parse_args();root=Path(__file__).resolve().parents[1]
assert hashlib.sha256(a.pdf.read_bytes()).hexdigest()=='c574d3baa9526fe690496303efc54b960bb678ad99aea7877971b5593b72bffc','Source PDF revision differs; review it before extracting.'
with tempfile.TemporaryDirectory(prefix='xoc-source-figure-') as tmp:
 for page,number,kind,box in [(24,6,'clos',(65,128,550,450)),(33,7,'rail',(65,237,550,569))]:
  prefix=Path(tmp)/f'page{page}';subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r','400','-png','-singlefile',str(a.pdf.resolve()),str(prefix)],check=True)
  image=Image.open(prefix.with_suffix('.png'));image.crop(tuple(round(v*400/72) for v in box)).save(root/f'figures/xoc-n-figure-{number:02d}-{kind}.png')
  print(f'Figure {number}: reproduced original artwork from PDF viewer page {page}.')

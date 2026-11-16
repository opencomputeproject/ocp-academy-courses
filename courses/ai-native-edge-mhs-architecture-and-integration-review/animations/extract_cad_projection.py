"""Read official STEP geometry; project actual model edges onto local X/Z.
No meshing repair, dimensional edits, component invention, or compliance test.
"""
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE,TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Line
from pathlib import Path
import json,argparse
out=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cad-dir', type=Path, required=True, help='Directory containing the official extracted STEP files')
parser.add_argument('--class', dest='board_class', choices=['n','l','all'], default='l')
args=parser.parse_args()
for kind,name in [('n','edge_mhs_classn_hpm_asm.stp'),('l','edge_mhs_class_l_hpm_asm.stp')]:
 if args.board_class not in (kind,'all'):continue
 source=args.cad_dir/name
 if not source.is_file():raise FileNotFoundError(source)
 r=STEPControl_Reader();r.ReadFile(str(source));r.TransferRoots();ex=TopExp_Explorer(r.OneShape(),TopAbs_SOLID);solids=[]
 while ex.More():
  ee=TopExp_Explorer(ex.Current(),TopAbs_EDGE);paths=set()
  while ee.More():
   c=BRepAdaptor_Curve(TopoDS.Edge_s(ee.Current()));a,b=c.FirstParameter(),c.LastParameter();count=2 if c.GetType()==GeomAbs_Line else 17;pts=[]
   for i in range(count):
    p=c.Value(a+(b-a)*i/(count-1));pts.append((round(p.X(),2),round(365+p.Z(),2)))
   if len(set(pts))>1:
    pts=min(tuple(pts),tuple(reversed(pts)));paths.add('M'+' L'.join(f'{x},{y}' for x,y in pts))
   ee.Next()
  solids.append(sorted(paths));ex.Next()
 width=168 if kind=='n' else 295
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width*4}" height="1460" viewBox="0 0 {width} 365"><rect width="{width}" height="365" fill="#f5f7f8"/>'
 for j,paths in enumerate(solids):
  svg+=f'<g fill="none" stroke="{"#67737b" if j==0 else "#343895"}" stroke-width="{0.32 if j==0 else 0.12}">'+''.join(f'<path d="{p}"/>' for p in paths)+'</g>'
 svg+='</svg>'; (out/f'cad_class_{kind}_top.svg').write_text(svg)
 print(kind,len(svg),'bytes')

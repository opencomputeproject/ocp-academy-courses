from pathlib import Path
import json, base64
R=Path(__file__).resolve().parents[2]; F=R/'figures'
C={'ink':'#253047','indigo':'#4F46A5','green':'#8DC63F','muted':'#657083','line':'#CFD5DE'}
def text(x,y,s,size=26,weight=400,fill='#253047',anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'
def box(x,y,w,h,fill='#F5F7FA',stroke='#CFD5DE',r=16):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def arrow(x1,y1,x2,y2,color='#4F46A5'):
 import math
 a=math.atan2(y2-y1,x2-x1); bx=x2-12*math.cos(a);by=y2-12*math.sin(a);px=5*math.sin(a);py=-5*math.cos(a)
 return f'<path d="M{x1},{y1} L{bx},{by}" stroke="{color}" stroke-width="3" fill="none"/><polygon points="{x2},{y2} {bx+px},{by+py} {bx-px},{by-py}" fill="{color}"/>'
fonts=''.join('@font-face{font-family:Open Sans;font-weight:'+str(v)+';src:url(data:font/ttf;base64,'+base64.b64encode((R/'animations/module2'/f'open-sans-{v}.ttf').read_bytes()).decode()+')}' for v in [400,700])
def svg(body,w,h):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><style>{fonts}text{{font-family:Open Sans,Arial,sans-serif}}</style><rect width="100%" height="100%" fill="white"/>{body}</svg>'
b=''
for x,y,w,h,t,sub in [(55,45,1330,116,'Application','Express the workload'),(55,197,1330,116,'Framework','Select and dispatch operations'),(55,350,630,116,'Library path','Call an implemented operation'),(755,350,630,116,'Compiler path','Lower an operation to target code'),(55,503,1330,116,'Runtime / adapter','Prepare memory and schedule execution'),(55,656,630,116,'Driver','Reach the device interface'),(755,656,630,116,'Device','Execute supported operations')]:
 b+=box(x,y,w,h,'#F2F5EE' if t=='Device' else '#F5F7FA')+text(x+28,y+49,t,26,700)+text(x+28,y+84,sub,21)
b+=arrow(720,161,720,197)+arrow(370,313,370,350)+arrow(1070,313,1070,350)+arrow(370,466,370,503)+arrow(1070,466,1070,503)+arrow(370,619,370,656)+arrow(685,714,755,714)
b+=text(720,826,'Conceptual paths can combine. New devices still need backends, kernels and runtime support.',24,400,anchor='middle')
(F/'module2_software_stack.svg').write_text(svg(b,1440,860))
b=text(55,50,'DATA DESCRIPTION',25,700,'#4F46A5')+text(755,50,'EXECUTION CONTRACT',25,700,'#4F46A5')
for x,y,w,h,t,sub in [(55,80,630,110,'Type','How each value is interpreted'),(55,206,630,110,'Shape','Dimensions and element counts'),(55,332,630,110,'Layout / strides','Where elements are stored'),(55,458,630,110,'Alignment','Required address boundaries'),(755,80,630,152,'Operation semantics','What function means and returns'),(755,250,630,152,'Ownership / lifetime','Who may access data, and for how long'),(755,420,630,152,'Completion / visibility','When the result is safe to consume')]:
 b+=box(x,y,w,h)+text(x+28,y+50,t,27,700)+text(x+28,y+84,sub,22)
b+=box(55,600,1330,110,'#F2F7EB','#8DC63F')+text(720,650,'Both are needed to interpret an offloaded request.',27,700,anchor='middle')+text(720,684,'Illustrative review checklist — not a defined NDC descriptor or adopted specification.',22,anchor='middle')
(F/'module2_data_contract.svg').write_text(svg(b,1440,742))

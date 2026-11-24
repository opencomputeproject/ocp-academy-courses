from pathlib import Path
import json,base64
root=Path(__file__).resolve().parents[2]
assets=Path(__file__).parent
fontroot=assets/'fonts'
font=''.join('@font-face{font-family:Open Sans; font-weight:'+w+';src:url(data:font/ttf;base64,'+base64.b64encode((fontroot/f'open-sans-{w}.ttf').read_bytes()).decode()+')}\n' for w in ['400','600','700'])
style=font+'text{font-family:"Open Sans",sans-serif;fill:#303942} .h{font-size:48px;font-weight:700}.s{font-size:32px}.m{font-size:38px;font-weight:600}.tiny{font-size:28px}.muted{fill:#65717a}.green{fill:#517e24}.indigo{fill:#525989}.bold{font-weight:700}'
def text(x,y,t,cl='s',anchor='start'): return f'<text x="{x}" y="{y}" class="{cl}" text-anchor="{anchor}">{t}</text>'
def box(x,y,w,h,fill='#fff',stroke='#d5dce0',r=20): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
def arrow(x1,y1,x2,y2,color='#679b32'):
    # explicit rear-flat-center shaft attachment; tip ends at target boundary
    import math
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); ux,uy=dx/n,dy/n; bx,by=x2-18*ux,y2-18*uy
    return f'<path d="M{x1} {y1} L{bx} {by}" fill="none" stroke="{color}" stroke-width="5"/><polygon points="{x2},{y2} {bx-9*uy},{by+9*ux} {bx+9*uy},{by-9*ux}" fill="{color}"/>'
def group(id,body): return f'<g id="{id}">{body}</g>'
def matrix(x,y,rows=5,cols=5,cell=30):
    return ''.join(f'<rect x="{x+c*cell}" y="{y+r*cell}" width="{cell-5}" height="{cell-5}" rx="3" fill="#8dc63f" opacity="{0.4+(r+c)%3*.23}"/>' for r in range(rows) for c in range(cols))
def tag(x,y,w,t):return box(x,y,w,84,'#eff5e8','#eff5e8',12)+text(x+26,y+54,t,'tiny green bold')
svg=''
svg+=group('intro',text(100,150,'Two integrations. One data-placement idea.','h')+text(100,220,'Proof of concept • selected work executes near resident data','s muted')+box(100,310,800,520,'#f7f9f5')+box(1020,310,800,520,'#f5f6fa')+text(160,390,'Inference','m')+text(1080,390,'Retrieval','m')+matrix(180,440,5,7,42)+text(580,500,'Resident','s')+text(580,550,'matrix','m')+matrix(1100,450,4,7,42)+text(1500,500,'Resident','s')+text(1500,550,'index','m')+text(160,745,'LLaMA 3.2-1B / ExecuTorch','s')+text(1080,745,'Faiss IVFFlat / RAG','s')+tag(100,910,1060,'Integration evidence • not a new industry standard'))
# detailed reusable structure
for kind in ['gemv','search']:
    isg=kind=='gemv'
    b=text(100,125,'GEMV: keep the matrix resident' if isg else 'Vector search: keep the index resident','h')
    b+=text(100,185,'Inference • LLaMA 3.2-1B / ExecuTorch' if isg else 'Retrieval for RAG • Faiss IVFFlat','s muted')
    b+=box(100,250,540,580,'#f8f9fa')+text(140,315,'HOST','tiny muted bold')
    b+=text(140,390,'ExecuTorch' if isg else 'Faiss IVFFlat','m')
    b+=group(kind+'-stack',box(140,440,460,100,'#fff')+text(170,499,'CPU-side GEMV path' if isg else 'Search request','s')+box(140,570,460,100,'#f1f2f8','#d8daea')+text(170,629,'NDC API + driver' if isg else 'NDC API','s indigo')+text(140,768,'Subsequent inference' if isg else 'Search results for RAG','tiny muted'))
    b+=box(1060,250,760,580,'#f7faf3','#b9d78f')+text(1100,315,'PNM DEVICE' if isg else 'CMM-DC MEMORY + PNM','tiny green bold')
    b+=group(kind+'-resident',box(1100,365,330,300,'#fff','#b8ce9c')+text(1130,420,'Resident matrix' if isg else 'Resident index','tiny bold')+matrix(1140,455,5,7,34))
    b+=box(1510,455,270,210,'#eaf3dd','#8dc63f')+text(1645,526,'PNM','m','middle')+text(1645,574,'engine','m','middle')
    b+=group(kind+'-compute',arrow(1430,560,1510,560)+text(1645,624,'GEMV' if isg else 'Search','tiny green bold','middle')+text(1100,770,'Compute with device-local data','tiny green'))
    b+=group(kind+'-input',text(850,420,'Input vector' if isg else 'Search request','s indigo','middle')+arrow(640,470,1060,470,'#626c9e')+group(kind+'-packet',box(680,450,40,40,'#626c9e','#626c9e',5)))
    b+=group(kind+'-output',arrow(1060,720,640,720)+group(kind+'-result-packet',box(1000,700,40,40,'#679b32','#679b32',5))+text(850,790,'Output vector' if isg else 'Smaller results','s green','middle'))
    b+=text(850,620,'Host–device','tiny muted','middle')+text(850,658,'connection','tiny muted','middle')
    if isg:
        b+=group('gemv-conclusion',tag(100,900,1420,'Reuse the matrix • exchange vectors • schematic sizes, not byte counts'))
    else:
        b+=group('search-setup',box(100,870,540,134,'#f5f6fa','#d7daea')+text(140,930,'SSD: generated index','s indigo')+text(140,972,'From vector dataset','tiny muted')+f'<path d="M640 925 L1240 925 L1240 848" fill="none" stroke="#8b93aa" stroke-width="5"/><polygon points="1240,830 1231,848 1249,848" fill="#8b93aa"/>'+text(860,888,'Load before search','tiny muted','middle')+text(1370,940,'Setup has a cost','tiny muted'))
    svg+=group(kind,b)
# final summary
b=text(100,130,'Resident data. Selected work. Smaller results.','h')+text(100,200,'Two proof-of-concept paths using NDC API','s muted')
for x,title,operand,operation in [(100,'Inference','Matrix','GEMV'),(1020,'Retrieval','Index','Search')]:
    b+=box(x,290,800,430,'#f8faf5','#cdddb8')+text(x+40,360,title,'m')+box(x+40,405,320,230,'#fff','#cdddb8')+text(x+200,475,operand,'m','middle')+matrix(x+100,495,3,5,30)+box(x+470,405,290,230,'#edf4e4','#abc982')+text(x+615,490,operation,'m','middle')+text(x+615,540,'near data','s','middle')+arrow(x+360,520,x+470,520)+text(x+40,680,'Resident data stays • results return','s green')
b+=group('evidence',box(100,790,1720,210,'#f5f6fa','#d8dbe9')+text(140,860,'Less traffic is not an end-to-end speedup result.','m indigo')+text(140,915,'Measure setup, latency, throughput, energy and correctness.','s')+text(140,965,'Compare against a suitable baseline.','tiny muted'))
svg+=group('summary',b)
import xml.etree.ElementTree as ET
svg_scenes=''
for scene in ET.fromstring('<root>'+svg+'</root>'):
    sid=scene.attrib.pop('id')
    svg_scenes+=f'<svg xmlns="http://www.w3.org/2000/svg" id="{sid}" viewBox="0 0 1920 1080" role="img" style="position:absolute;inset:0"><rect width="1920" height="1080" fill="white"/>'+ET.tostring(scene,encoding='unicode')+'</svg>'
html='<!DOCTYPE html><html><head><meta charset="utf-8"><title>Two NDC proof-of-concept dataflows</title><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:white}svg{display:block;width:100%;height:100%}'+style+'</style></head><body data-duration-ms="130000" data-poster-ms="126000">'+svg_scenes+'<script src="timing.js"></script><script>\n'+'''
const D=window.TIMING;
document.body.dataset.durationMs=D.duration_ms;document.body.dataset.posterMs=D.duration_ms-1000;
function clamp(x){return Math.max(0,Math.min(1,x))}
function opacity(id,a){document.getElementById(id).setAttribute('opacity',a)}
function reveal(id,t,at){opacity(id,clamp((t-at)/650))}
window.setTeachingTime=function(ms){let t=Math.max(0,Math.min(ms,D.duration_ms));
let scene=t<D.gemv?'intro':t<D.search?'gemv':t<D.summary?'search':'summary';
for(let id of ['intro','gemv','search','summary'])opacity(id,id===scene?1:0);
for(let k of ['gemv','search']){
let q=D[k+'_cues'];reveal(k+'-stack',t,q.stack);reveal(k+'-resident',t,q.resident);reveal(k+'-input',t,q.input);reveal(k+'-compute',t,q.compute);reveal(k+'-output',t,q.output);
let p=clamp((t-q.input-650)/1200);let packet=document.getElementById(k+'-packet');packet.setAttribute('transform','translate('+(p*340)+' 0)');packet.setAttribute('opacity',p===1?0:1);let rp=clamp((t-q.output-650)/2000);let result=document.getElementById(k+'-result-packet');result.setAttribute('transform','translate('+(-rp*360)+' 0)');result.setAttribute('opacity',rp===1?0:1);
}
reveal('gemv-conclusion',t,D.gemv_cues.conclusion);reveal('search-setup',t,D.search_cues.setup);reveal('evidence',t,D.evidence);
};window.setTeachingTime(0);
// Deterministic, finite, seekable authoring preview. Recorder drives the same clock.
window.playTeachingPass=()=>{const begin=performance.now();function tick(now){const t=Math.min(D.duration_ms,now-begin);window.setTeachingTime(t);if(t<D.duration_ms)requestAnimationFrame(tick)}requestAnimationFrame(tick)};
</script></body></html>'''
(assets/'workloads.html').write_text(html)
if not (assets/'timing.js').exists():(assets/'timing.js').write_text('window.TIMING='+json.dumps({'duration_ms':130000,'gemv':18000,'search':65000,'summary':109000,'evidence':116000,'gemv_cues':{'stack':26000,'resident':34000,'input':39000,'compute':42000,'output':47000,'conclusion':52000},'search_cues':{'stack':65000,'setup':75000,'resident':79000,'input':87000,'compute':93000,'output':98000}})+';')
# Compact static diagram: comparison table
s=text(35,55,'Test the proposed mapping across device classes','m')+text(35,101,'Illustrative review questions • not adopted cross-device requirements','tiny muted')
cols=[35,295,700,1110]
for x,t in zip(cols,['Device class','Where the data lives','Source / sink','Adaptation or gap to test']):s+=text(x,165,t,'tiny bold')
rows=[('Storage',['Storage media;', 'device memory'],['Storage extent ↔ host buffer'],['Map existing storage path']),('PIM',['Memory banks'],['Host / mapped memory'],['Whole operator →', 'bank execution']),('PNM',['Device-attached memory'],['Host ↔ device memory'],['Addressing, visibility,', 'completion']),('DPU',['Network flow;', 'host memory'],['Stream ↔ buffer / stream'],['Name streams;', 'bound lifetime'])]
for i,(a,b,c,d) in enumerate(rows):
    y=200+i*124;s+=box(25,y,1570,112,'#f7f9f5' if i%2==0 else '#f7f8fb','#eef0ee',10)
    s+=text(50,y+66,a,'tiny bold')
    for x,lines in [(295,b),(700,c),(1110,d)]:
        for j,line in enumerate(lines):s+=text(x,y+(46+j*36 if len(lines)>1 else 66),line,'tiny')
s+=text(35,750,'Common descriptors are a proposal; each device still needs a valid execution and data-access contract.','tiny muted')
(root/'figures/module3_device_matrix.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1620 785" role="img"><title>Proposed device mappings and unresolved contracts</title><style>'+style+'.tiny{font-size:26px}</style><rect width="1620" height="785" fill="white"/>'+s+'</svg>')
# evidence plan two comparison arms and common measurements, compact
s=text(40,60,'Compare the complete workload, including preparation','m')+text(40,110,'Illustrative measurement protocol • no synthetic performance numbers','tiny muted')
for x,title,l1,l2 in [(40,'BASELINE','Host executes the operation','Record transfers and setup'),(850,'OFFLOAD','Device executes selected work','Record setup, transfers and fallback')]:
    s+=box(x,160,730,190,'#f7faf3','#cdddb8')+text(x+35,210,title,'tiny green bold')+text(x+35,270,l1,'s')+text(x+35,317,l2,'tiny muted')
s+=text(810,268,'vs.','tiny muted','middle')
s+=box(40,390,1540,220,'#f5f6fa','#d8dbe9')+text(75,443,'Hold the comparison conditions fixed','s indigo bold')+text(75,496,'Hardware / software • dataset / model / index • quality target • warm-up • concurrency','tiny')+text(75,558,'Measure end-to-end latency • throughput • transferred bytes • energy • correctness','tiny bold')
s+=text(40,672,'Report setup separately and in amortized totals; test an unsupported operation or device failure.','tiny muted')
(root/'figures/module3_evidence_plan.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1620 710" role="img"><title>Baseline and offload evidence plan</title><style>'+style+'.tiny{font-size:26px}</style><rect width="1620" height="710" fill="white"/>'+s+'</svg>')
print('Created deterministic video source and two static SVGs.')

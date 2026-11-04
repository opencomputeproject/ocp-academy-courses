from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'figures'; OUT.mkdir(exist_ok=True)
G='#8DC63F'; I='#343895'; D='#27313B'; M='#5F6062'; L='#DCE2E6'; PALE='#F6F8FA'; GP='#F1F8E8'; IP='#F0F0FA'; A='#9A621D'
manifest=[]
def text(x,y,s,size=25,color=D,weight=400,anchor='start'):
 lines=s.split('|'); return '<text x="%s" y="%s" font-size="%s" fill="%s" font-weight="%s" text-anchor="%s">'%(x,y,size,color,weight,anchor)+''.join('<tspan x="%s" dy="%s">%s</tspan>'%(x,0 if i==0 else size*1.35,escape(t)) for i,t in enumerate(lines))+'</text>'
def rect(x,y,w,h,fill=PALE,stroke=L,r=18): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def line(x1,y1,x2,y2,color=M,width=3,dash=''): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def arrow(x1,y1,x2,y2,color=I,width=4):
 import math
 a=math.atan2(y2-y1,x2-x1); bx=x2-13*math.cos(a); by=y2-13*math.sin(a); nx=6*math.sin(a); ny=-6*math.cos(a)
 return line(x1,y1,bx,by,color,width)+f'<polygon points="{x2},{y2} {bx+nx},{by+ny} {bx-nx},{by-ny}" fill="{color}"/>'
def node(x,y,w,h,label,sub='',fill=PALE,stroke=L):
 yy=y+h/2-8 if sub else y+h/2+9
 return rect(x,y,w,h,fill,stroke)+text(x+w/2,yy,label,24 if label=='Electrical endpoint' else 26 if label=='Packet switch' else 27,D,600,'middle')+(text(x+w/2,yy+37,sub,21,M,400,'middle') if sub else '')
def badge(x,y,label,color=I,w=180): return rect(x,y,w,46,IP if color==I else GP,'none',23)+text(x+w/2,y+30,label,20,color,600,'middle')
def save(name,w,h,body,caption,alt,source):
 p=OUT/(name+'.svg'); p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(alt,quote=True)}"><rect width="100%" height="100%" fill="white"/><g font-family="Arial, Helvetica, sans-serif">{body}</g></svg>\n')
 manifest.append(dict(path='figures/'+p.name,width=w,height=h,caption=caption,alt=alt,source_scope=source,kind='new editable technical SVG',built=True))
# Module 1
b=node(30,145,245,120,'Electrical endpoint','packet functions',IP)+node(445,145,310,120,'Optical circuit','selected light path',GP,G)+node(925,145,245,120,'Electrical endpoint','packet functions',IP)
b+=arrow(275,205,445,205,G,7)+arrow(755,205,925,205,G,7)
b+=text(600,60,'One established connection',27,D,600,'middle')+text(600,100,'Light stays optical through the switching stage',24,M,400,'middle')
b+=line(405,125,405,295,L,2,'7 7')+line(795,125,795,295,L,2,'7 7')
b+=rect(80,335,1040,120,PALE,'none')+text(110,377,'Inside the OCS',24,I,600)+text(110,417,'Port-to-port connectivity',24)+text(600,377,'Elsewhere in the system',24,I,600)+text(600,417,'Buffering · packet inspection · scheduling',24)
save('m1_optical_boundary',1200,480,b,'The optical switch provides selected connectivity. Packet services and workload scheduling remain functions of the surrounding system.','Electrical endpoints flank a transparent optical circuit, with the service boundary explicitly marked.','M1 / How OCS Works; Packet Handling marker')
rows=[('Signal path','No OEO inside the OCS','Electronic packet processing'),('Timing','No packet queue in the OCS','Queueing depends on traffic'),('Packet services','No per-packet inspection','Forwarding and QoS functions'),('Speed upgrades','Rate-transparent optical path','Electronic port-rate limits'),('Optical budget','Insertion loss must be budgeted','OEO can regenerate signals')]
b=rect(30,20,1140,66,I,'none',14)+text(60,63,'Dimension',24,'white',600)+text(360,63,'OCS',24,'white',600)+text(810,63,'EPS',24,'white',600)
for j,(a,c,d) in enumerate(rows):
 y=100+j*81;b+=rect(30,y,1140,70,GP if j%2==0 else PALE,'none',8)+text(60,y+44,a,23,D,600)+text(360,y+44,c,23)+text(810,y+44,d,22)
save('m1_five_tradeoffs',1200,515,b,'Compare the switching stage across five dimensions; whole-network performance still depends on the complete design.','A five-row OCS versus electrical packet switching comparison.','M1 / How OCS Works / five labeled markers')
b=node(30,150,210,100,'Transmitter','launch power',IP)+node(360,150,190,100,'OCS path','insertion loss',GP,G)+node(670,150,190,100,'Connectors','additional loss')+node(980,150,190,100,'Receiver','required power',IP)
for a,c in [(240,360),(550,670),(860,980)]:b+=arrow(a,200,c,200,G,6)
b+=text(600,35,'Illustrative relative power — no numeric loss scale',23,M,400,'middle')
for x,h in [(110,65),(455,49),(765,33),(1075,23)]: b+=rect(x-22,125-h,44,h,G,'none',4)
b+=rect(90,310,1020,90,PALE,'none')+text(600,348,'Every passive element contributes to the link budget.',26,D,600,'middle')+text(600,382,'Allowed hop count depends on the complete optical design.',24,M,400,'middle')
save('m1_optical_loss',1200,430,b,'Insertion loss accumulates along the optical path. Verify the complete link budget instead of assuming one universal hop limit.','Four progressively smaller qualitative power bars accompany a transmitter, optical switch, connectors and receiver.','M1 / Insertion Loss; Benefits and Limitations')
# Module 2
families=[('Robotic','Move and connect fibers','Long-lived physical patching'),('MEMS','Tilt microscopic mirrors','Free-space beam steering'),('Liquid crystal','Control polarization','Solid-state path selection'),('Piezoelectric','Deform a material','Precision optical alignment'),('Silicon photonics','Control on-chip waveguides','Thermo- or electro-optic'),('Metasurface','Control optical phase','Tunable sub-wavelength pixels')]
b=''
for j,(a,c,d) in enumerate(families):
 x=30+(j%3)*390;y=25+(j//3)*210
 b+=rect(x,y,360,185,PALE,L)+badge(x+20,y+18,f'{j+1:02}',I,55)+text(x+95,y+47,a,27,D,600)+text(x+22,y+100,c,24)+text(x+22,y+145,d,22,M)
b+=text(600,482,'Hybrid systems combine mechanisms; they are not a seventh physical principle.',23,I,400,'middle')
save('m2_mechanism_atlas',1200,510,b,'Six primary mechanisms route light in different ways. Hybrid designs combine mechanisms to balance their tradeoffs.','Six cards describe robotic, MEMS, liquid crystal, piezoelectric, silicon-photonic and metasurface switching.','M2 / OCS Technology Families')
b=node(435,200,330,120,'Workload requirement','communication pattern',GP,G)
for x,y,l,s in [(35,30,'Switching time','available setup interval'),(805,30,'Radix','required port count'),(35,370,'Optical loss','complete link budget'),(805,370,'Power profile','change and hold state')]:b+=node(x,y,360,110,l,s,IP)
b+=arrow(395,110,435,220,I)+arrow(805,110,765,220,I)+arrow(395,410,435,300,I)+arrow(805,410,765,300,I)
b+=''
save('m2_selection_constraints',1200,510,b,'Match the device to the workload using switching time, radix, optical loss and power together. No single metric determines the best fit.','Four engineering constraints feed a central workload requirement.','M2 / Technology Deep Dives and Comparison Matrix')
b=rect(30,25,555,360,PALE,L)+rect(615,25,555,360,PALE,L)
b+=text(65,75,'Thermo-optic actuation',29,D,600)+text(650,75,'Electro-optic actuation',29,D,600)
b+=node(65,115,485,78,'Temperature change',fill=IP)+arrow(307,193,307,230,I)+node(65,230,485,80,'Refractive-index change',fill=GP,stroke=G)
b+=node(650,115,485,78,'Electrical field / carrier effect',fill=IP)+arrow(892,193,892,230,I)+node(650,230,485,80,'Refractive-index change',fill=GP,stroke=G)
b+=text(307,350,'Often microsecond-scale',24,M,400,'middle')+text(892,350,'Can reach nanosecond-scale',24,M,400,'middle')
b+=rect(170,420,860,70,IP,'none')+text(600,464,'Phase control changes interference and the output path.',25,I,600,'middle')
save('m2_photonic_actuation',1200,520,b,'Silicon photonics describes an integration platform, not one universal switching speed. Actuation and device design determine behavior.','Thermo-optic and electro-optic actuation both lead to refractive-index and phase changes through different physical controls.','M2 / MEMS vs. Silicon Photonics original video')
# Module 3
b=text(300,55,'Electrical interconnect stage',27,D,600,'middle')+text(900,55,'Configurable optical stage',27,D,600,'middle')
for shift,typ in [(0,'Electrical'),(600,'Optical')]:
 for xx in [65,335]:b+=node(xx+shift,330,200,80,'Packet switch',fill=IP)
 b+=node(135+shift,125,330,100,typ+' fabric','schematic layer',GP if shift else PALE,G if shift else L)
 b+=arrow(165+shift,330,215+shift,225,G if shift else I,5)+arrow(435+shift,330,385+shift,225,G if shift else I,5)
 b+=text(300+shift,465,'Electrical packet functions remain',23,M,400,'middle')
b+=line(600,95,600,450,L,2,'8 8')
save('m3_architecture_layers',1200,500,b,'The selected interconnect layer changes, while electrical packet-switching functions remain at the edges. This is a conceptual comparison, not a production wiring diagram.','Side-by-side fabrics show electrical packet switches below an electrical or optical interconnect stage.','M3 / EPS Spine Replacement')
b=rect(30,25,335,310,PALE,L)+text(197,75,'1 Cube',30,D,600,'middle')+text(197,122,'64 TPUs',35,I,600,'middle')+text(197,169,'4 × 4 × 4',29,D,600,'middle')+text(197,210,'electrical mesh',25,M,400,'middle')
for row in range(3):
 for col in range(6):b+=rect(65+col*45,245+row*20,28,12,G,'none',2)
b+=arrow(365,180,445,180,I)
b+=rect(445,25,335,310,GP,G)+text(612,75,'64 Cubes',30,D,600,'middle')+text(612,130,'4,096 TPUs',35,I,600,'middle')+text(612,180,'one full Superpod',25,M,400,'middle')+text(612,260,'Inter-Cube optical links',24,D,600,'middle')
b+=arrow(780,180,860,180,I)+rect(860,25,310,310,PALE,L)+text(1015,75,'48 OCS devices',29,D,600,'middle')+text(1015,130,'128 ports each',27,I,600,'middle')+text(1015,197,'X · Y · Z',35,D,600,'middle')+text(1015,247,'switch groups',25,M,400,'middle')
b+=rect(100,375,1000,70,IP,'none')+text(600,420,'Electrical within a Cube; optical switching between Cubes.',25,I,600,'middle')
save('m3_tpu_hierarchy',1200,475,b,'The TPUv4 hierarchy separates electrical connectivity within each Cube from optical switching between Cubes. Counts describe the full source Superpod configuration.','Three connected panels show 64 TPUs per Cube, 64 Cubes per 4096-TPU Superpod, and 48 128-port OCS devices grouped by dimension.','M3 / Static-to-Dynamic AI Cluster Reconfiguration')
b=''
steps=[('Detect','Identify the failed link|or component'),('Plan','Find supported spare|connectivity'),('Reconfigure','Establish the revised|physical path'),('Validate','Check topology and|service capacity')]
for j,(a,c) in enumerate(steps):
 x=30+j*295;b+=rect(x,75,255,200,GP if j==2 else PALE,G if j==2 else L)+badge(x+20,94,f'{j+1:02}',I,50)+text(x+25,177,a,29,D,600)+text(x+25,220,c,22,M)
 if j<3:b+=arrow(x+255,175,x+295,175,I)
b+=rect(75,330,1050,110,IP,'none')+text(600,373,'Recovery depends on available spares and application behavior.',25,I,600,'middle')+text(600,412,'Restored connectivity does not replace lost compute state.',24,M,400,'middle')
save('m3_recovery_dependencies',1200,470,b,'Physical reconfiguration can restore supported connectivity, but the outcome depends on spare resources, control actions and application recovery.','A four-step detect, plan, reconfigure and validate sequence includes a distinction between restored connectivity and lost compute state.','M3 / Hardware Failure Resiliency; M5 recovery scenario clarification')
# Module 4
b=''
items=[('Local scale-up','Within a server / high-bandwidth domain','Electrical fabric; e.g. NVSwitch',I,IP),('Global scale-out','Across the cluster','EPS; e.g. Ethernet or InfiniBand',M,PALE),('Regional OCS','Expert-parallel communication groups','Optical circuits; workload-aware allocation',G,GP)]
for j,(a,c,d,col,bg) in enumerate(items):
 y=25+j*145;b+=rect(30,y,1140,120,bg,L)+rect(30,y,13,120,col,'none',3)+text(65,y+48,a,28,D,600)+text(420,y+45,c,25,D,600)+text(420,y+88,d,24,M)
b+=badge(30,480,'Research architecture',I,240)+text(310,508,'MixNet combines fabrics for different communication roles.',24,M)
save('m4_mixnet_fabrics',1200,540,b,'MixNet is a research architecture that assigns different communication roles to three fabrics. Regional OCS serves expert parallelism rather than replacing every interconnect.','Three horizontal bands distinguish local electrical scale-up, cluster-wide electrical scale-out and regional optical expert-parallel traffic.','M4 / MixNet, Quantum and Disaggregation')
b=node(30,145,305,120,'Traffic demand','who needs to communicate?',IP)+node(447,145,305,120,'Control decision','supported allocation',GP,G)+node(865,145,305,120,'Optical resources','available paths',IP)
b+=arrow(335,205,447,205,I)+arrow(752,205,865,205,I)
b+=rect(120,330,960,100,PALE,'none')+text(600,372,'Wavelength assignment operates within the physical topology.',25,D,600,'middle')+text(600,409,'It does not create arbitrary new fiber connections.',24,M,400,'middle')+badge(30,35,'Conceptual research model',I,300)
save('m4_demand_control_paths',1200,460,b,'Separate changing demand from the control decision and the physical resources available to it. The conceptual model explains the source’s traffic-aware allocation.','Traffic demand flows through a control decision to supported optical resources, with a physical-topology constraint.','M4 / ACTINA, OCS-BCube and Topology Explorer')
b=rect(30,25,555,355,PALE,L)+rect(615,25,555,355,PALE,L)+text(65,75,'Quantum transport',30,D,600)+text(650,75,'Classical resource pooling',30,D,600)
b+=node(65,120,160,85,'Photons',fill=IP)+arrow(225,162,310,162,G,6)+node(310,120,240,85,'Optical path',fill=GP,stroke=G)
b+=text(65,260,'Avoid measurement-based routing',24,D,600)+text(65,305,'Loss, noise and state fidelity|still require verification.',24,M)
b+=node(650,120,175,85,'Compute',fill=IP)+arrow(825,162,910,162,G,6)+node(910,120,225,85,'Resources',fill=GP,stroke=G)
b+=text(650,260,'Connect supported pooled resources',24,D,600)+text(650,305,'Protocol, distance and latency|budgets still apply.',24,M)
b+=badge(30,420,'Emerging applications',I,265)+text(325,448,'Optical transparency is a property, not an end-to-end guarantee.',24,M)
save('m4_quantum_disaggregation',1200,480,b,'Optical transparency can support quantum transport and classical resource pooling. Each still needs its own system-level compatibility and performance checks.','Two panels distinguish quantum state transport constraints from classical compute-to-resource connections.','M4 / OCS in Quantum and Disaggregation; approved technical clarifications')
# Module 5
b=''
roles=[('Technology suppliers','Components and|device capabilities'),('Systems integrators','Hardware and|orchestration'),('Operators','Deployment requirements|and operating evidence'),('Standards community','Open specifications|and shared models')]
for j,(a,c) in enumerate(roles):
 x=30+(j%2)*600;y=25+(j//2)*235;b+=rect(x,y,540,205,GP if j==3 else PALE,G if j==3 else L)+badge(x+25,y+20,f'{j+1:02}',I,55)+text(x+105,y+53,a,29,D,600)+text(x+30,y+117,c,26,M)
save('m5_ecosystem_roles',1200,485,b,'Interoperability requires contributions from component suppliers, systems integrators, operators and the standards community.','Four equally sized panels describe the responsibilities of the source ecosystem roles.','M5 / The OCS Ecosystem Layers')
b=node(30,150,295,120,'Device','supported capabilities',IP)+node(452,150,295,120,'Control model','shared meaning',GP,G)+node(874,150,295,120,'Operations','requested service',IP)
b+=arrow(325,188,452,188,I)+arrow(874,188,747,188,I)+arrow(452,235,325,235,G)+arrow(747,235,874,235,G)
b+=text(388,140,'capability',21,M,400,'middle')+text(810,140,'request',21,M,400,'middle')+text(388,310,'command',21,M,400,'middle')+text(810,310,'state / evidence',21,M,400,'middle')
b+=rect(100,365,1000,80,PALE,'none')+text(600,412,'Illustrative contract — not a published API or certification scheme',24,M,400,'middle')
save('m5_interoperability_contract',1200,475,b,'A common control model gives capability, command and state information a shared meaning. This is a conceptual contract, not a specific OCP API.','Device and operator exchange capability, command, request and state information through a shared control model.','M5 / Building the OCS Ecosystem original video / standardized data models')
b=''
vals=[('Bring a requirement','Define the problem|and constraints'),('Contribute evidence','Share a reproducible|design or finding'),('Review together','Compare assumptions|and interface needs'),('Improve the work','Refine specifications|and reference designs')]
for j,(a,c) in enumerate(vals):
 x=30+j*295;b+=rect(x,60,255,230,GP if j==3 else PALE,G if j==3 else L)+badge(x+20,80,f'{j+1:02}',I,50)+text(x+22,160,a,22,D,600)+text(x+22,215,c,21,M)
 if j<3:b+=arrow(x+255,175,x+295,175,I)
b+=text(600,365,'Choose the handoff your team knows; contribute clear requirements and evidence.',25,I,600,'middle')
save('m5_contribution_path',1200,405,b,'Useful community contributions connect a clear requirement to evidence and collaborative review. Consult the linked OCP resources for current participation routes.','Four steps show requirements, evidence, review and improvements to shared specifications and reference designs.','M5 / Building the OCS Ecosystem; participation objective')
(ROOT/'authoring/astra-media/static-figure-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Built',len(manifest),'SVG figures')

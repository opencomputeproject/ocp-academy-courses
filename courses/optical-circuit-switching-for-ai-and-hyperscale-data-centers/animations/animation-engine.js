/* Editable deterministic instructional scenes. One finite master clock; no loops.
 * setTeachingTime(milliseconds) is the AcademyWizard lossless recorder contract.
 * Every path is conceptual. No measured performance is encoded by geometry. */
(()=>{
const C=window.MEDIA_CONFIG,G='#8DC63F',I='#343895',D='#27313B',M='#5F6062',L='#DCE2E6',P='#F6F8FA',GP='#F1F8E8',IP='#F0F0FA',AM='#9A621D';
const clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>{x=clamp(x);return x*x*(3-2*x)},esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const txt=(x,y,s,size=36,color=D,weight=400,anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" font-weight="${weight}" text-anchor="${anchor}">${s.split('|').map((a,j)=>`<tspan x="${x}" dy="${j?size*1.35:0}">${esc(a)}</tspan>`).join('')}</text>`;
const box=(x,y,w,h,fill=P,stroke=L,r=24)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="3"/>`;
const line=(x1,y1,x2,y2,color=M,w=5,dash='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${w}" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
const path=(d,color=G,w=7,dash='')=>`<path d="${d}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
const arrow=(x1,y1,x2,y2,color=I,w=5)=>{const a=Math.atan2(y2-y1,x2-x1),bx=x2-20*Math.cos(a),by=y2-20*Math.sin(a),nx=9*Math.sin(a),ny=-9*Math.cos(a);return line(x1,y1,bx,by,color,w)+`<polygon points="${x2},${y2} ${bx+nx},${by+ny} ${bx-nx},${by-ny}" fill="${color}"/>`};
const circle=(x,y,r,fill=G,stroke='none')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="3"/>`;
const group=(opacity,body)=>`<g opacity="${clamp(opacity)}">${body}</g>`;
const node=(x,y,w,h,label,sub='',fill=P,stroke=L)=>box(x,y,w,h,fill,stroke)+txt(x+w/2,y+h/2+(sub?-8:13),label,38,D,600,'middle')+(sub?txt(x+w/2,y+h/2+43,sub,29,M,400,'middle'):'');
const pill=(x,y,w,label,fill=IP,color=I)=>box(x,y,w,58,fill,'none',29)+txt(x+w/2,y+39,label,28,color,600,'middle');
const note=(y,s,sub='')=>box(160,y,1600,sub?126:90,P,'none')+txt(960,y+(sub?48:57),s,34,D,600,'middle')+(sub?txt(960,y+94,sub,30,M,400,'middle'):'');
function state(t){let n=0;for(let j=1;j<4;j++)if(t>=C.scene_starts_ms[j])n=j;let start=C.scene_starts_ms[n],end=C.scene_starts_ms[n+1]||C.duration_ms;return {n,u:clamp((t-start)/(end-start)),t};}
function m1({n,u}){
 let s=box(700,185,520,630,GP,G)+txt(960,245,'Optical circuit switch',39,D,600,'middle')+txt(960,292,'selected port-to-port path',29,M,400,'middle');
 s+=node(80,310,350,145,'Endpoint A','electrical system',IP)+node(1490,310,350,145,'Endpoint B','electrical system',IP)+node(80,620,350,145,'Endpoint C','electrical system',IP)+node(1490,620,350,145,'Endpoint D','electrical system',IP);
 for(const y of [382,692]){s+=line(430,y,760,y,L,8)+line(1160,y,1490,y,L,8)+circle(760,y,12,'white',M)+circle(1160,y,12,'white',M);}
 const f=n>0?1:ease(u*2);s+=group(f,line(430,382,1490,382,G,10)+circle(760,382,13,G)+circle(1160,382,13,G));
 if(n===0&&u>.15&&u<.8){const q=clamp((u-.15)/.65);s+=circle(430+1060*q,382,17,I);}
 s+=txt(960,450,'Established: A ↔ B',31,I,600,'middle');
 s+=group(n>=1?1:0,pill(80,490,350,'Packet services',IP)+pill(1490,490,350,'Packet services',IP)+txt(960,530,'No packet inspection',31,M,400,'middle')+txt(960,574,'inside this path',31,M,400,'middle'));
 if(n>=2){let q=n>2?1:ease(u*2);s+=group(q,line(430,692,760,692,AM,8,'16 10')+circle(760,692,16,'#FFF4E4',AM)+txt(960,696,'C → B requested',33,AM,600,'middle')+txt(960,743,'Allocation decision needed',29,M,400,'middle'));}
 if(n<3)s+=note(880,n===0?'The circuit redirects light; it does not read packets.':n===1?'Packet services remain in the surrounding electrical systems.':'A second demand needs a supported allocation.');
 else{s+=box(260,880,630,100,IP,'none')+txt(575,942,'1  Select a circuit',34,I,600,'middle')+arrow(905,930,1015,930,I)+box(1030,880,630,100,GP,'none')+txt(1345,942,'2  Transfer data',34,D,600,'middle');}
 return s;
}
function m2({n,u}){
 let s=pill(90,70,400,'Schematic time windows',IP)+txt(1780,112,'No measured time scale',29,M,400,'end');
 s+=txt(90,210,'Long stable communication phase',40,D,600)+line(360,300,1780,300,L,4);
 s+=box(360,255,240,100,IP,'none',12)+txt(480,318,'Setup',34,I,600,'middle');
 let width=1180*(n>0?1:ease(u*1.5));s+=box(600,255,width,100,GP,'none',12)+group(ease((width-600)/300),txt(1190,318,'Useful transfer',34,D,600,'middle'));
 s+=txt(360,405,'The connection remains useful after setup.',31,M);
 if(n>=1){let q=n>1?1:ease(u*1.8);s+=group(q,txt(90,515,'Frequent changes',40,D,600)+line(360,605,1780,605,L,4));for(let j=0;j<3;j++){const x=360+j*480;s+=group(q,box(x,560,240,100,IP,'none',12)+box(x+240,560,200,100,GP,'none',12)+txt(x+120,624,'Setup',32,I,600,'middle')+txt(x+340,624,'Transfer',30,D,600,'middle'));}s+=group(q,txt(360,710,'The same setup occupies more of each short interval.',31,M));}
 if(n>=2){s+=group(n>2?1:ease(u*2),pill(90,795,260,'Robotic',P,M)+pill(380,795,260,'MEMS',P,M)+pill(670,795,260,'Liquid crystal',P,M)+pill(960,795,260,'Piezoelectric',P,M)+pill(1250,795,270,'Photonics',P,M)+pill(1550,795,280,'Metasurface',P,M));}
 if(n>=3){let q=ease(u*2);s+=group(q,txt(960,930,'Timing + radix + optical loss + power + maturity',37,I,600,'middle')+txt(960,989,'Choose an implementation that fits the workload.',32,M,400,'middle'));}
 return s;
}
function m3({n,u}){
 const change=n>=1?ease(n>1?1:u*2):0, oldAlpha=1-ease(change*2), newAlpha=ease((change-.5)*2);
 let s=pill(90,65,390,'Conceptual architecture',IP)+txt(1780,106,'Selected interconnect stage',30,M,400,'end');
 for(let j=0;j<4;j++){let x=120+j*450;s+=node(x,675,330,145,'Packet switch',n>=3?'upgraded interface':'electrical functions',IP);s+=line(x+165,675,x+165,550,L,8);}
 s+=box(120,245,1680,305,change>0?GP:P,change>0?G:L)+group(oldAlpha,txt(960,310,'Electrical interconnect',44,D,600,'middle'))+group(newAlpha,txt(960,310,'Configurable optical interconnect',44,D,600,'middle'));
 s+=group(oldAlpha,node(280,370,360,115,'O → E','conversion',IP)+node(780,370,360,115,'Packet processing','electronic stage',IP)+node(1280,370,360,115,'E → O','conversion',IP)+arrow(640,427,780,427,I)+arrow(1140,427,1280,427,I));
 s+=group(newAlpha,path('M 285 550 L 285 430 Q 285 395 325 395 L 695 395 Q 735 395 735 430 L 735 550',G,10)+path('M 1185 550 L 1185 430 Q 1185 395 1225 395 L 1595 395 Q 1635 395 1635 430 L 1635 550',G,10)+txt(510,465,'Selected circuit',30,I,600,'middle')+txt(1410,465,'Selected circuit',30,I,600,'middle'));
 if(n===0&&u>.15&&u<.85)s+=circle(285+1350*clamp((u-.15)/.7),427,15,G);
 if(n>=2)s+=note(875,n===2?'Packet functions remain at the electrical edges.':'Rate transparency does not remove the optical link budget.',n===2?'Connectivity can change without per-packet inspection inside the OCS.':'Check transceivers, optical bandwidth, insertion loss and compatibility.');
 else s+=note(875,n===0?'Trace the functions performed at the interconnect stage.':'The optical fabric changes one architectural layer.');
 return s;
}
function m4({n,u}){
 let s=pill(70,50,510,'Research concept · schematic paths',IP)+txt(1820,92,'No performance values implied',28,M,400,'end');
 s+=box(70,145,500,690,P,L)+txt(320,208,'Workload demand',39,D,600,'middle')+txt(320,256,n<2?'Iteration A':'Iteration B',32,I,600,'middle');
 const swap=n>=2?ease(n>2?1:u*1.7):0;
 for(let j=0;j<3;j++){let y=335+j*140;let valsA=[.9,.4,.2],valsB=[.25,.8,.6],w=330*(valsA[j]*(1-swap)+valsB[j]*swap);s+=txt(108,y-25,['Group 1','Group 2','Group 3'][j],30,M)+box(108,y,390,48,'#E8EDEF','none',8)+box(108,y,w,48,j===0?I:G,'none',8);}
 s+=txt(320,790,'Qualitative demand only',26,M,400,'middle');
 s+=box(665,335,390,270,GP,G)+txt(860,397,'Controller',40,D,600,'middle')+txt(860,456,'Select supported',31,M,400,'middle')+txt(860,500,'wavelength / path',31,M,400,'middle')+txt(860,544,'allocation',31,M,400,'middle');
 s+=arrow(570,470,665,470,I)+arrow(1055,470,1150,470,I);
 s+=box(1150,145,700,690,P,L)+txt(1500,208,'Available optical resources',37,D,600,'middle')+txt(1500,257,'Physical paths remain constrained',28,M,400,'middle');
 const ys=[350,500,650];for(let j=0;j<3;j++){s+=node(1190,ys[j]-44,150,90,['A','B','C'][j], '',IP)+node(1660,ys[j]-44,150,90,['D','E','F'][j],'',IP);s+=line(1340,ys[j],1660,ys[j],L,6);}
 s+=path('M 1340 350 C 1460 350 1540 650 1660 650',L,6)+path('M 1340 650 C 1460 650 1540 350 1660 350',L,6);
 let active=n===0?ease(u*2):1;
 s+=group(active*(1-ease(swap*2)),line(1340,350,1660,350,I,10)+line(1340,500,1660,500,G,10)+pill(1400,292,190,'λ set A',IP));
 s+=group(active*ease((swap-.5)*2),path('M 1340 350 C 1460 350 1540 650 1660 650',I,10)+path('M 1340 650 C 1460 650 1540 350 1660 350',G,10)+pill(1400,710,190,'λ set B',GP,D));
 s+=note(890,n<2?'Demand informs allocation within the available topology.':n===2?'Explicit iteration boundary: revise the supported allocation.':'Demand, control and physical connectivity remain distinct.',n>=3?'Evaluate overhead and workload conditions before generalizing research results.':'Wavelength selection does not create arbitrary new fiber connections.');
 return s;
}
function m5({n,u}){
 let s=pill(80,60,470,'Illustrative interoperability flow',IP);
 const xs=[100,740,1380],labels=['Supplier','Integrator','Operator'],subs=['device capabilities','orchestration + model','service requirements'];
 for(let j=0;j<3;j++)s+=node(xs[j],260,440,180,labels[j],subs[j],j===1?GP:IP,j===1?G:L);
 s+=line(540,350,740,350,L,6)+line(1180,350,1380,350,L,6);
 s+=group(n>=1?1:ease(u*2),pill(130,520,380,'Ports · optical limits',P,M)+arrow(540,350,740,350,I,7));
 if(n>=1){s+=group(n>1?1:ease(u*2),pill(770,520,380,'Shared meaning',GP,D)+txt(960,630,'Request',34,I,600,'middle')+txt(960,680,'Reported state',34,I,600,'middle'));}
 if(n>=2){s+=group(n>2?1:ease(u*2),arrow(1380,325,1180,325,I,7)+arrow(1180,380,1380,380,G,7)+pill(1410,520,380,'Verify intended state',P,M));}
 if(n>=3){let q=ease(u*2);s+=group(q,box(230,790,1460,170,GP,G)+txt(960,850,'Open specifications · reference designs · validation',36,D,600,'middle')+txt(960,911,'Requirements and evidence improve the next shared revision.',31,M,400,'middle'));}
 else s+=note(850,n===0?'A component needs a clear description of its capabilities.':n===1?'Hardware and software must attach the same meaning to a connection.':'The reported state must match the service the operator requested.');
 return s;
}
const renders=[null,m1,m2,m3,m4,m5];
window.setTeachingTime=ms=>{const t=Math.max(0,Math.min(C.duration_ms,Number(ms)||0));window.currentTeachingTime=t;document.getElementById('canvas').innerHTML='<rect width="1920" height="1080" fill="#fff"/>'+renders[C.module](state(t));};
window.setTeachingTime(0);
// Manual preview can call playTeachingPreview(); it stops and holds at the master end.
window.playTeachingPreview=()=>{const t0=performance.now();const frame=now=>{const t=Math.min(C.duration_ms,now-t0);window.setTeachingTime(t);if(t<C.duration_ms)requestAnimationFrame(frame)};requestAnimationFrame(frame)};
})();

/* Deterministic finite teaching sequences. Narration chapter boundaries are the master timeline. */
const C={g:'#8DC63F',b:'#343895',d:'#242947',gray:'#657080',p:'#F1F4F8',amber:'#B57926'};
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;');
function tx(x,y,v,size=23,color=C.d,anchor='middle',bold=false){return `<text x="${x}" y="${y}" font-family="Arial,sans-serif" font-size="${size}" fill="${color}" text-anchor="${anchor}" font-weight="${bold?700:400}">${String(v).split('|').map((s,i)=>`<tspan x="${x}" dy="${i?size*1.4:0}">${esc(s)}</tspan>`).join('')}</text>`}
function rect(x,y,w,h,fill=C.p,stroke='#D8DEE8',r=14){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`}
function box(x,y,w,h,label,fill=C.p,size=22){const count=String(label).split('|').length;return rect(x,y,w,h,fill)+tx(x+w/2,y+h/2-(count-1)*size*.7+size*.3,label,size)}
function ln(x,y,a,b,color=C.b,width=5,dash=''){return `<path d="M${x} ${y}L${a} ${b}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" ${dash?`stroke-dasharray="${dash}"`:''}/>`}
function dot(x,y,color=C.g,r=9){return `<circle cx="${x}" cy="${y}" r="${r}" fill="${color}"/>`}
function tag(t){return tx(55,48,t,22,C.b,'start',true)}
function communication(k,p){
 let body=tag(['Define the preparation window','Case A · sporadic transfer','Case B · repeating phases','Case C · irregular bursts','Compare the workload windows'][k]);
 const patterns=[[[710,200]],[[370,140],[650,140],[930,140]],[[320,80],[460,65],[625,110],[900,90]]];
 const labels=['Sporadic','Periodic','Irregular'];
 for(let r=0;r<3;r++){
  const y=130+r*135,active=k===0||k===4||r===k-1;
  body+=tx(180,y+36,labels[r],23,active?C.d:'#A3ADB8','end');body+=ln(235,y+68,1130,y+68,'#B6BFCA',2);
  for(const [x,w] of patterns[r])body+=rect(x,y+10,w,58,active?C.g:'#E6EBDf','none',5);
  const end=patterns[r][0][0],start=245;
  if(active){body+=ln(start,y-6,end-10,y-6,C.b,4);body+=ln(start,y-15,start,y+3,C.b,2)+ln(end-10,y-15,end-10,y+3,C.b,2);
   body+=tx((start+end-10)/2,y-20,k===0?'Setup window':'Prepare',17,C.b);
   if(k!==4)body+=dot(start+(end-start-12)*p,y-6,C.b,6);
  }
 }
 return body+tx(600,548,'Illustrative event spacing · compare complete readiness with the workload deadline',20,C.gray);
}
function reconfigure(k,p){
 let body=tag(['Declare the measurement boundary','Case A · fully serial work','Case B · faster switch only','Case C · prepared and coordinated work','The critical path determines readiness'][k]);
 const names=['Scheduler','Control','Switch','Receiver','Host'],cols=[C.b,'#798AAD',C.g,'#D49A32','#667686'];
 if(k===0){body+=box(75,170,280,125,'Request to change|connectivity')+ln(355,232,845,232,C.b,5)+dot(365+470*p,232,C.g,11)+box(845,170,280,125,'Endpoints can use|the new path','#EBF4DD');body+=tx(600,395,'Before topology selection → usable traffic',27)}
 else {
  const rows=k===3||k===4?[['Prepared beforehand',[40,20,0,0,0],120],['Remaining critical path',[0,0,10,80,10],310]]:k===1?[['Baseline',[40,20,10,80,10],220]]:[['Baseline',[40,20,10,80,10],140],['Faster optical element',[40,20,1,80,10],320]];
  for(const [label,vals,y] of rows){body+=tx(60,y-35,label,23,C.d,'start',true);let x=70;
   for(let i=0;i<5;i++){const w=vals[i]*5.6;if(!w)continue;body+=rect(x,y,w,68,cols[i],'none',3);if(w>90)body+=tx(x+w/2,y+40,names[i],20,'white');x+=w}
   body+=tx(x+20,y+42,vals.reduce((a,b)=>a+b,0)+' µs',24,C.d,'start',true);
   if(k<4)body+=dot(70+(x-70)*p,y+90,C.b,7);
  }
  for(let i=0;i<5;i++){body+=rect(115+i*210,422,18,18,cols[i],'none',3)+tx(144+i*210,438,names[i],18,C.d,'start');}
  if(k===1)body+=tx(600,488,'All five serial contributors must finish.',26);
  if(k===2)body+=tx(600,488,'A faster switch leaves the other dependencies in place.',25);
  if(k>=3)body+=tx(600,488,'Preparation must be valid; readiness still includes recovery and endpoints.',23);
 }
 return body+tx(600,548,'Illustrative timings and separate comparison cases · not a measured product',20,C.gray);
}
function optical(k,p){
 let body=tag(['Declare the optical routing task','Electro-optic control · state A','Electro-optic control · state B','Separate mechanism · SOA gain gating','Different mechanisms, the same readiness question'][k]);
 if(k<3){const target=k===2?365:190;body+=box(55,240,195,100,'Optical input')+ln(250,290,450,290,C.g,8)+box(450,185,300,205,'Controlled optical|structure');body+=ln(750,250,960,190,k===2?'#D4DBE5':C.g,7)+ln(750,330,960,365,k===2?C.g:'#D4DBE5',7)+box(960,145,190,90,'Output A',k===2?C.p:'#EBF4DD')+box(960,320,190,90,'Output B',k===2?'#EBF4DD':C.p);
  body+=box(455,70,290,70,k===2?'Electrical state B':'Electrical state A',C.p,20)+ln(600,140,600,185,C.b,3);
  if(k>0)body+=dot(250+200*p,290,C.b,9);
  body+=tx(600,485,k===0?'Select the intended optical route.':'Electrical control changes index or absorption.',25);
 }else if(k===3){body+=box(65,235,210,100,'Optical input')+ln(275,285,430,170,C.b,6)+ln(275,285,430,390,'#D4DBE5',6);body+=box(430,125,310,90,'SOA · gain enabled','#EBF4DD')+box(430,345,310,90,'SOA · suppressed');body+=ln(740,170,960,170,C.g,8)+ln(740,390,960,390,'#D4DBE5',6)+box(960,125,180,90,'Pass','#EBF4DD')+box(960,345,180,90,'Suppress');body+=dot(750+195*p,170,C.b,9)+tx(600,492,'Current controls optical gain; signal quality still matters.',24);
 }else{body+=box(70,150,500,150,'Electro-optic routing|Index / absorption control','#EBF4DD')+box(630,150,500,150,'SOA switching|Gain control');body+=tx(600,405,'Device transition ≠ end-to-end usable link',30,C.b,'middle',true)+tx(600,470,'Drive · stabilization · receiver · endpoint readiness',23)}
 return body+tx(600,548,'Conceptual operation · animation is not a device response-time measurement',20,C.gray);
}
function network(cx,cy,pairs,active,p){let out='';const pts=[[-165,-95],[165,-95],[-165,95],[165,95]].map(([a,b])=>[a+cx,b+cy]);
 for(const [a,b] of pairs){let [x,y]=pts[a],[xx,yy]=pts[b];out+=ln(x,y,xx,yy,active?C.g:'#CAD3DF',7);if(active)out+=dot(x+(xx-x)*p,y+(yy-y)*p,C.b,8)}
 pts.forEach(([x,y],i)=>{out+=`<circle cx="${x}" cy="${y}" r="44" fill="white" stroke="${C.b}" stroke-width="3"/>`+tx(x,y+8,String(i+1),26)});return out;
}
function workload(k,p){let body=tag(['Declare the communication phase','Collective example · phase A','Collective example · phase B','Separate MoE example · expert traffic','Evaluate the workload benefit'][k]);
 if(k<3){body+=network(600,290,k===2?[[0,2],[1,3]]:[[0,1],[2,3]],k>0,p)+tx(600,105,k===2?'Different pairs become active':'Selected endpoint pairs exchange data',25)+tx(600,490,k===0?'Connectivity is useful when it matches the required exchange.':k===1?'Prepare the paths before this phase needs them.':'Coordinate the change with the next communication phase.',23)}
 else if(k===3){body+=box(60,230,270,105,'Token group');for(let i=0;i<3;i++){const y=110+i*130;body+=ln(330,282,800,y+42,i===1?C.g:C.b,i===1?10:4)+box(800,y,325,85,'Expert group '+(i+1),i===1?'#EBF4DD':C.p);body+=dot(350+430*p,282+(y+42-282)*p,C.b,7)}body+=tx(600,524,'Uneven expert traffic · illustrative distribution, not a measured trace',20,C.gray)}
 else{body+=box(60,135,330,140,'Correct connectivity')+box(435,135,330,140,'Ready at the|required time','#EBF4DD')+box(810,135,330,140,'Measured workload|improvement');body+=tx(600,367,'MixNet can hide millisecond switching during computation.',24)+tx(600,443,'Faster actuation is useful only when it removes a workload constraint.',23,C.b)}
 return body;
}
window.OCSVideo={render(d,seconds){let k=d.chapters.findIndex(c=>seconds<c.end);if(k<0)k=d.chapters.length-1;const c=d.chapters[k];const p=Math.min(1,Math.max(0,(seconds-c.start)/Math.min(8,(c.end-c.start)*.55)));let body=({communication_windows:communication,reconfiguration_path:reconfigure,optical_routing:optical,workload_connectivity:workload})[d.asset](k,p);return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="562" viewBox="0 0 1200 562"><rect width="1200" height="562" fill="white"/>${body}</svg>`;}};

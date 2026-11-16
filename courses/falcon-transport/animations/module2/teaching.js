const G='#8DC63F',D='#26332d',M='#5F6062',L='#e8ebE7',P='#f2f7ec';
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const txt=(x,y,s,size=32,fill=D,anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor}">${esc(s)}</text>`;
const line=(x,y,x2,y2,color=M,width=3)=>`<line x1="${x}" y1="${y}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}"/>`;
const arrow=(x,y,x2,color=G)=>{let dir=Math.sign(x2-x),b=x2-16*dir;return line(x,y,b,y,color,5)+`<polygon class="arrowhead" points="${b},${y-9} ${x2},${y} ${b},${y+9}" fill="${color}"/>`};
const box=(x,y,w,h,lines,{fill='white',stroke=L,size=32,head='',accent=false}={})=>`<g data-containment="true"><rect class="container" x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="${fill}" stroke="${accent?G:stroke}" stroke-width="${accent?4:2}"/>${head?txt(x+32,y+53,head,26,M):''}${lines.map((s,i)=>txt(x+32,y+(head?108:lines.length===1?h/2+size*.35:55)+i*(size+16),s,size)).join('')}</g>`;
const badge=(text)=>box(64,48,1792,108,[text],{size:36,fill:P,stroke:P});
const footer=(a,b)=>txt(64,976,a,30,D)+txt(64,1022,b,25,M);
const bits=(y,label,v,green)=>txt(84,y+55,label,30,M)+[3,2,1,0].map((n,i)=>box(500+i*155,y,125,110,[String(v[n])],{fill:v[n]?P:'white',accent:!!v[n],size:38})).join('')+txt(1165,y+57,green,32);
const stepAt=(p,cues)=>{let n=0;cues.forEach((c,i)=>{if(p>=c)n=i});return n};
const film=document.body.dataset.film;
const cueSets={"a4": [0.0, 0.09297187776509663, 0.1848127107885254, 0.3859124658570677, 0.44947718033880046, 0.6148359215706389, 0.6770433823623703, 0.758931021659122], "a5a": [0.0, 0.21015415033801782, 0.3069642920568769, 0.5031951860578004, 0.5560600499627055, 0.6685338550607959, 0.7461995193161501, 0.8556276120905011], "a5b": [0.0, 0.1839553233263974, 0.25555340931041143, 0.3976712968509694, 0.43368599672847036, 0.4932072971248194, 0.6210918302227721, 0.8179865666788106]};
const eventNames={a4:['Four packets · one path · base 300','PSN 300 is lost; later packets arrive','Read received state separately from ACK state','EACK exposes a hole at bit 0','Distance and recency checks both pass','Retransmit only PSN 300','Deliver RSNs 1–4; await ULP acknowledgement','ULP ACK permits data base 304'],a5a:['A separate case · time-based inference','Original transmissions: t=0, 1, 2 µs','At t=7, EACK reports 301 and 302 received','RACK timeout = measured RTT + reordering cushion','PSN 300 passes time and recency conditions','Excluded: packets already reported received','Excluded: unknown horizon or newer transmission','Only eligible missing packets enter repair'],a5b:['New quiet-tail case · reset to PSNs 400–401','400 acknowledged; 401 unacknowledged','Last activity t=4; probe timeout = 8 µs','At t=12.1, inactivity exceeds the timeout','Probe lowest unacknowledged PSN: 401','AR=1 and ER=1 request useful feedback','Older peer: ER ignored; AR-triggered ACK fallback','Feedback may enable RACK; backup RTO remains']};
function a4(s,p){
 let count=s>=2?3:s===1?Math.min(3,1+Math.floor((p-cueSets.a4[1])/(cueSets.a4[2]-cueSets.a4[1])*3)):0; let received=count>0,filled=s>=6,done=s>=7;let rx=filled?[1,1,1,1]:[0,...[1,2,3].map(n=>n<=count?1:0)];
 let a=badge(eventNames.a4[s]);
 a+=txt(84,214,'Sender packet identities',27,M)+txt(1160,214,'Receiver · ordered connection',27,M);
 for(let i=0;i<4;i++){
  let x=84+i*253,ok=(i>0&&i<=count)||(i===0&&filled);a+=box(x,250,219,155,[`PSN ${300+i}`,`RSN ${1+i}`],{fill:ok?P:'white',accent:ok,size:30});
 }
 a+=box(1160,250,674,155,[done?'All four acknowledged':filled?'All four received':received?`Later packets retained: ${count}`:'Waiting for arrival',done?'Data base → 304':filled?'ULP ACK still required':'300 is the sequence hole'],{size:31,fill:P});
 a+=txt(84,465,done?'Final snapshot at base 300':'Displayed bit order: 3   2   1   0',27,M)+txt(1160,465,'Bit 0 (rightmost) = PSN 300',27,M);
 a+=bits(500,'Data-Rx',rx,[...rx].reverse().join('')+'b');
 a+=bits(618,'Data-ACK',done?[1,1,1,1]:[0,0,0,0],done?'1111b → base 304':'0000b');
 let msg=s<3?'Receiver retains out-of-order packets.':s<5?'300 < 303 − 2    AND    last_tx + RTT < now':s===5?'PSN 300 crosses the network again.':s===6?'RSNs 1 → 2 → 3 → 4 delivered in order.':'301–303 were preserved throughout recovery.';
 a+=box(84,774,1750,132,[msg],{fill:P,size:34});

 a+=footer('Distance is assessed within the recorded path; recency protects against repeated repair.','Threshold 2 and elapsed timing are illustrative. All four packets use one path.');return a;
}
function a5a(s,p){
 let a=badge(eventNames.a5a[s]);
 a+=txt(84,215,'Packet Sequence Numbers on the send-time axis · illustrative microseconds',28,M);
 let x=t=>130+t*160; a+=line(x(0),465,x(10),465,M,3);
 for(let t=0;t<=10;t++){a+=line(x(t),454,x(t),476,M,2)+txt(x(t),518,String(t),27,M,'middle');}
 [[0,300],[1,301],[2,302]].forEach(([t,n],i)=>{a+=box(x(t)-42,300,142,93,[`${n}`],{size:30,fill:n===300?'white':s>=2?P:'white',accent:n!==300&&s>=2});a+=line(x(t),393,x(t),451,n===300?M:G,3)});
 if(s>=2){a+=box(x(7)-70,268,410,145,['EACK at t=7','301 and 302 received'],{size:29,fill:P});a+=line(x(7),413,x(7),451,G,4);}
 a+=txt(84,570,s>=2?'Reported horizon includes 300; the received bits for 301 and 302 are set.':'The sender waits for feedback about received packets.',28,M);
 let cards=[['Known feedback',s>=2?'300 is inside the horizon':'Await a received-state bitmap.',s>=2?'and is not received.':'Receipt must be known.'],['Recency',s>=4?'tx_time 0 ≤ RACK.xmit_ts 2':'Compare transmission times.','Newer sends are excluded.'],['Elapsed time',s>=4?'7 µs ≥ timeout 5 µs':'Allow a reordering cushion.',s>=4?'Eligible for loss decision.':'Then evaluate loss.']];
 cards.forEach((v,i)=>a+=box(84+i*590,622,554,234,v.slice(1),{head:v[0],size:29,fill:s>=(i===0?2:4)?P:'white',accent:s>=(i===0?2:4)}));
 if(s>=3)a+=txt(84,926,'RACK_RTO = 4 + (4 × 0.25) = 5 µs',35);
 a+=txt(84,992,s>=6?'Exclude received packets, packets beyond the horizon, and sends after t=2.':'One early-retransmission method is selected at system initialization.',28,M);
 return a;
}
function a5b(s,p){
 let a=badge(eventNames.a5b[s]);
 a+=box(84,222,430,150,['PSN 400','Acknowledged'],{size:31,fill:P,accent:true});
 a+=box(558,222,530,150,['PSN 401','Lowest unacknowledged'],{size:31,fill:s>=4?P:'white',accent:s>=4});
 a+=box(1132,222,702,150,['tlp_pto = max(4 × 2, 6)','= 8 µs'],{size:31,fill:P});
 a+=txt(84,435,'No transmit or receive activity during this interval',29,M);
 let x=t=>100+(t-4)*195;
 a+=line(x(4),535,x(12.1),535,M,4);
 for(let t=4;t<=12;t+=2)a+=line(x(t),522,x(t),548,M,2)+txt(x(t),591,`${t} µs`,29,M,'middle');
 a+=box(84,650,500,175,[s>=4?'Probe PSN 401':'Await feedback',s>=5?'AR=1  ·  ER=1':'Outstanding data window'],{size:31,fill:P,accent:s>=4});
 a+=box(1320,650,514,175,[s>=6?'v1.0 / v1.1 peer':'v1.2 receiver',s>=6?'Ignores ER':'EACK requested'],{size:31,fill:s>=4?P:'white'});
 if(s>=4){a+=arrow(584,696,1320,G)+txt(952,665,'probe',28,M,'middle');}
 if(s>=5){a+=arrow(1320,784,584,M)+txt(952,752,s>=6?'AR-triggered ACK':'feedback',28,M,'middle');}
 a+=txt(84,912,s>=3?'At t=12.1: 8.1 µs of inactivity > 8 µs timeout':'Illustrative times; this is a new case, separate from the RACK timeline.',32);
 a+=txt(84,978,s>=7?'v1.1 receive capacity: cap Tx window at 256 for performance.':s>=6?'AR respects acknowledgement semantics; immediate EACK is not guaranteed.':'Probe each window with outstanding packets; a probe does not prove loss.',28,M);
 a+=txt(84,1025,'The backup retransmission timeout remains available.',27,M);
 return a;
}
const renderers={a4,a5a,a5b};
window.teachingCues=cueSets[film];
window.setTeachingTime=(ms)=>{const dur=Number(document.body.dataset.durationMs);const p=Math.max(0,Math.min(.999999,ms/dur));const s=stepAt(p,cueSets[film]);document.getElementById('stage').innerHTML=renderers[film](s,p);document.body.dataset.step=s;};
window.setTeachingTime(0);

import {createRequire} from 'node:module';
const require = createRequire(import.meta.url);
const {createCanvas} = require('@napi-rs/canvas');
const measure = createCanvas(1,1).getContext('2d');

export const C = {
  ink:'#3f4145', muted:'#666b72', green:'#6fa030', lime:'#8dc63f', greenTint:'#f0f8e7',
  blue:'#343895', blueTint:'#f1f2fb', line:'#cbd1d7', faint:'#f5f7f8',
  amber:'#a66b08', amberTint:'#fff7e5', hot:'#c74433', cold:'#2475b9', white:'#ffffff',
};
const esc = value => String(value).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const clamp = value => Math.max(0,Math.min(1,value));
const ease = value => {const x=clamp(value);return x*x*(3-2*x);};

export class Drawing {
  constructor() {this.parts=[];this.texts=[];this.bounds=[];}
  raw(value) {this.parts.push(value);}
  rect(x,y,w,h,{fill=C.white,stroke=C.line,r=12,sw=3}={}) {
    this.raw(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`);
  }
  line(x1,y1,x2,y2,color=C.line,sw=5,dash='') {
    this.raw(`<path d="M${x1},${y1} L${x2},${y2}" fill="none" stroke="${color}" stroke-width="${sw}"${dash?` stroke-dasharray="${dash}"`:''}/>`);
  }
  path(d,color=C.line,sw=5,dash='') {
    this.raw(`<path d="${d}" fill="none" stroke="${color}" stroke-width="${sw}"${dash?` stroke-dasharray="${dash}"`:''}/>`);
  }
  dot(x,y,r=13,color=C.lime) {
    this.raw(`<circle cx="${x}" cy="${y}" r="${r}" fill="${color}"/>`);
  }
  width(text,size=36,weight=400) {
    measure.font=`${weight} ${size}px Arial`;
    return measure.measureText(text).width;
  }
  text(x,y,value,{size=36,color=C.ink,weight=400,anchor='start'}={}) {
    const width=this.width(value,size,weight);
    const left=x-(anchor==='middle'?width/2:anchor==='end'?width:0);
    if(left<0||left+width>1920||y<0||y+size*1.3>1080)
      throw new Error(`Text outside frame: ${value}`);
    this.raw(`<text x="${x}" y="${y+size}" font-family="Arial, Helvetica, sans-serif" font-size="${size}" font-weight="${weight}" fill="${color}" text-anchor="${anchor}">${esc(value)}</text>`);
    this.texts.push(value);
    return {x:left,y,width,height:size*1.3};
  }
  wrap(value,width,size=36,weight=400) {
    const lines=[];
    for(const paragraph of String(value).split('\n')) {
      let line='';
      for(const word of paragraph.split(/\s+/).filter(Boolean)) {
        if(this.width(word,size,weight)>width) throw new Error(`Word needs a wider container: ${word}`);
        const next=line?`${line} ${word}`:word;
        if(this.width(next,size,weight)>width) {lines.push(line);line=word;}
        else line=next;
      }
      if(line) lines.push(line);
    }
    return lines;
  }
  paragraph(x,y,width,height,value,{size=36,color=C.ink,weight=400,center=false}={}) {
    const lines=this.wrap(value,width,size,weight);
    const lineHeight=size*1.3;
    if(lines.length*lineHeight>height+.01) throw new Error(`Text needs a taller container: ${value}`);
    for(const [i,line] of lines.entries()) this.text(center?x+width/2:x,y+i*lineHeight,line,{size,color,weight,anchor:center?'middle':'start'});
    return lines.length*lineHeight;
  }
  box(x,y,w,h,title,detail='',{color=C.blue,fill=C.white,size=34,detailSize=30,active=false}={}) {
    const pad=Math.max(28,size*.85);
    this.rect(x,y,w,h,{fill,stroke:active?color:C.line,sw:active?5:3});
    let used=this.paragraph(x+pad,y+pad,w-2*pad,h-2*pad,title,{size,color,weight:700});
    if(detail) {
      used+=10;
      used+=this.paragraph(x+pad,y+pad+used,w-2*pad,h-2*pad-used,detail,{size:detailSize,color:C.muted});
    }
    const clearance=h-pad-used;
    if(clearance<.75*Math.max(size,detail?detailSize:0)-.01) throw new Error(`Insufficient text clearance: ${title}`);
    this.bounds.push({title,x,y,w,h,padding:pad,bottom_clearance:clearance,font_size:size});
  }
  arrow(x1,y1,x2,y2,{color=C.blue,p=1,sw=6,head=24,dash=''}={}) {
    p=ease(p);
    if(p<=.001) return;
    const dx=x2-x1,dy=y2-y1,length=Math.hypot(dx,dy);
    const ux=dx/length,uy=dy/length;
    const tipX=x1+dx*p,tipY=y1+dy*p;
    const h=Math.min(head,length*p*.6),half=h*.55;
    const backX=tipX-ux*h,backY=tipY-uy*h;
    this.line(x1,y1,backX,backY,color,sw,dash);
    this.raw(`<polygon class="arrowhead" points="${backX-uy*half},${backY+ux*half} ${tipX},${tipY} ${backX+uy*half},${backY-ux*half}" fill="${color}"/>`);
  }
  curve(start,c1,c2,tip,{color=C.blue,head=24,dash='',sw=6}={}) {
    const length=Math.hypot(tip[0]-c2[0],tip[1]-c2[1]);
    const ux=(tip[0]-c2[0])/length,uy=(tip[1]-c2[1])/length;
    const bx=tip[0]-ux*head,by=tip[1]-uy*head,half=head*.55;
    this.path(`M${start} C${c1} ${c2} ${bx},${by}`,color,sw,dash);
    this.raw(`<polygon class="arrowhead" points="${bx-uy*half},${by+ux*half} ${tip} ${bx+uy*half},${by-ux*half}" fill="${color}"/>`);
  }
  orientation(title,sub='') {
    this.text(80,32,title,{size:40,weight:700});
    if(sub) this.text(80,93,sub,{size:27,color:C.muted});
  }
  note(value) {
    this.paragraph(80,982,1760,70,value,{size:27,color:C.muted});
  }
  svg() {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="1080" fill="#ffffff"/>${this.parts.join('')}</svg>`;
  }
}

function hostCase(d,kind,p=1) {
  const title={single:'Single-host example: 1 x16',dual:'Single-host example: 2 x8',quad:'Multi-host example: 4 x4'}[kind];
  d.orientation(title,'Separate supported configurations; not live reconfiguration. Conceptual lane connections.');
  if(kind==='single'||kind==='dual') {
    d.rect(100,210,480,580,{fill:C.faint});
    d.text(140,240,'One host',{size:38,weight:700});
    d.rect(1170,210,650,580,{fill:C.greenTint,stroke:C.lime});
    d.text(1210,240,'OCP NIC card',{size:38,weight:700});
    const n=kind==='single'?1:2;
    for(let i=0;i<n;i++) {
      const y=n===1?435:345+i*230;
      d.box(145,y,365,150,`Root port ${i}`,n===1?'x16':'x8',{size:32,detailSize:30});
      d.box(1240,y,510,150,`Endpoint ${i}`,n===1?'x16':'x8',{size:32,detailSize:30,fill:C.white});
      const cy=y+75;
      const color=i===0?C.green:C.blue;
      const count=n===1?16:8;
      for(let lane=0;lane<count;lane++) {
        const yy=cy-(count-1)*5+lane*10;
        d.line(510,yy,1240,yy,C.line,3);
        d.line(510,yy,510+730*ease(p),yy,color,4);
      }
      d.text(875,y-55,n===1?'16 PCIe lanes':'8 PCIe lanes',{size:34,weight:700,color,anchor:'middle'});
    }
  } else {
    d.rect(1170,210,650,580,{fill:C.greenTint,stroke:C.lime});
    d.text(1210,235,'OCP NIC card',{size:38,weight:700});
    for(let i=0;i<4;i++) {
      const y=320+i*115,color=[C.green,C.blue,C.cold,C.amber][i];
      d.box(100,y,440,96,`Host ${i+1} root port`, '', {size:30,color});
      d.box(1240,y,510,96,`Endpoint ${i}: x4`, '', {size:30,color});
      for(let lane=0;lane<4;lane++) {
        const yy=y+31+lane*10;
        d.line(540,yy,1240,yy,C.line,3);
        d.line(540,yy,540+700*ease(clamp(p*4-i)),yy,color,4);
      }
      d.text(875,y-35,'4 PCIe lanes',{size:30,color,weight:700,anchor:'middle'});
    }
  }
  d.note('Compatibility: root ports, card endpoints, lane grouping, reset and clock arrangements.');
}

function smallCase(d,x,kind) {
  const title={single:'1 host / 1 x16',dual:'1 host / 2 x8',quad:'4 hosts / 4 x4'}[kind];
  const n={single:1,dual:2,quad:4}[kind];
  d.text(x+260,205,title,{size:34,weight:700,anchor:'middle'});
  d.rect(x+310,292,230,410,{fill:C.greenTint,stroke:C.lime});
  d.text(x+425,311,'NIC',{size:30,weight:700,anchor:'middle'});
  if(kind!=='quad') {
    d.rect(x,292,180,410,{fill:C.faint});
    d.text(x+90,311,'One host',{size:28,weight:700,anchor:'middle'});
  }
  for(let i=0;i<n;i++) {
    const cy=380+i*(n===4?80:130);
    const color=[C.green,C.blue,C.cold,C.amber][i];
    d.text(x+(kind==='quad'?0:28),cy-15,kind==='quad'?`Host ${i+1}`:`Port ${i}`,{size:28,color,weight:700});
    d.line(x+(kind==='quad'?140:180),cy+6,x+360,cy+6,color,7);
    d.rect(x+360,cy-20,50,50,{fill:color,stroke:color,r:4});
    d.text(x+435,cy-14,`x${16/n}`,{size:28,color,weight:700});
  }
}

function m1(d,s) {
  if(['single','dual','quad'].includes(s.scene)) {hostCase(d,s.scene,clamp(s.elapsed/2));return;}
  d.orientation('Compare supported configurations','Not every card or baseboard implements every configuration.');
  for(const [i,kind] of ['single','dual','quad'].entries()) smallCase(d,80+i*610,kind);
  if(s.scene==='comparison') {
    d.paragraph(80,780,1760,135,'Compatibility depends on both ends: the root ports, card endpoints, supported subdivisions, reset and clock arrangements.',{size:38});
  } else {
    const facts=[
      ['Interface scope','Up to 32 lanes on DSFF; Gen 6 signal-integrity guidance.'],
      ['Programmable functions','Board area can support DRAM, SmartNIC and DPU designs.'],
      ['Management and identity','NC-SI sideband and FRU EEPROM support.'],
      ['Serviceability','Field replacement; platform-dependent live hot swap.'],
      ['Thermal validation','Standard fixtures support consistent comparisons.'],
    ];
    facts.forEach(([head,body],i)=>{
      const col=i%3,row=Math.floor(i/3),x=80+col*610,y=737+row*109;
      d.text(x,y,head,{size:29,weight:700,color:C.blue});
      d.paragraph(x,y+39,550,72,body,{size:25,color:C.muted});
    });
  }
  d.note('Card and baseboard support must match.');
}

function m2(d,s) {
  const phase=['slots','rail','alignment','pitch','capacity','tall','insulator'].indexOf(s.scene);
  const seated=phase>=3?1:phase===2?ease(s.elapsed/2.5):0;
  d.orientation('Middle-rail removal and connector alignment','Convertible bay only. Mechanical comparison; not a powered-service procedure. Not to scale.');
  d.rect(360,220,1200,535,{fill:C.faint,stroke:C.muted,r:8});
  d.text(590,240,'SFF position 0',{size:32,weight:700,anchor:'middle'});
  d.text(1330,240,'SFF position 1',{size:32,weight:700,anchor:'middle'});
  d.rect(460,330,360,75,{fill:C.blueTint,stroke:C.blue,r:4});
  d.rect(1100,330,360,75,{fill:C.blueTint,stroke:C.blue,r:4});
  d.text(640,342,'Primary 4C+',{size:30,weight:700,anchor:'middle',color:C.blue});
  d.text(1280,342,'Secondary 4C+',{size:30,weight:700,anchor:'middle',color:C.blue});
  if(phase<=1) {
    const progress=phase===1?ease(s.elapsed/2.5):0;
    const railY=415-progress*740;
    const railX=945;
    const visibleY=Math.max(155,railY),visibleBottom=Math.min(755,railY+300);
    if(visibleBottom>visibleY) d.rect(railX,visibleY,30,visibleBottom-visibleY,{fill:C.amberTint,stroke:C.amber,r:0});
    d.paragraph(80,385,230,160,phase===0?'Removable middle guide rail':'Middle rail removed',{size:32,color:C.amber,weight:700});
    if(phase===0) d.arrow(340,465,945,465,{color:C.amber,dash:'10 8'});
  }
  if(phase>=2) {
    const cardY=590-175*seated;
    d.rect(420,cardY,1080,285,{fill:C.greenTint,stroke:C.lime,r:8});
    d.rect(500,cardY-24,280,24,{fill:'#d8b652',stroke:C.amber,r:0});
    d.rect(1140,cardY-24,280,24,{fill:'#d8b652',stroke:C.amber,r:0});
    d.text(960,cardY+60,'One DSFF card',{size:43,weight:700,color:C.green,anchor:'middle'});
    d.text(960,cardY+135,'Two corresponding gold-finger edges',{size:32,color:C.muted,anchor:'middle'});
    if(phase>=3) {
      d.line(640,300,1280,300,C.blue,4);
      d.line(640,282,640,315,C.blue,4);
      d.line(1280,282,1280,315,C.blue,4);
      d.text(960,165,'81.55 mm connector pitch',{size:34,weight:700,color:C.blue,anchor:'middle'});
    }
  }
  if(phase>=4) {
    d.text(80,792,'Up to 32 PCIe lanes',{size:35,weight:700,color:C.green});
    d.text(80,844,'Up to 160 W at the card edge',{size:35,weight:700,color:C.green});
    d.text(80,896,'Cooling capacity still depends on conditions.',{size:28,color:C.muted});
  }
  if(phase>=5) {
    d.text(1190,770,'Tall variant: same outline and electrical model',{size:28,weight:700,color:C.blue});
    d.rect(1190,885,610,12,{fill:C.muted,stroke:C.muted,r:0});
    d.rect(1310,815,360,70,{fill:C.faint,stroke:C.blue,r:0});
    d.text(1370,824,'Taller Z-height',{size:28,color:C.blue});
  }
  if(phase>=6) {
    d.rect(1190,897,610,8,{fill:C.amber,stroke:C.amber,r:0});
    d.text(1190,916,'Insulator / backing plate is part of the card.',{size:26,color:C.amber});
  }
  const note=phase<3?'Designed for 2xSFF / 1xDSFF conversion; not an arbitrary pair of adjacent slots.':phase<4?'2xSFF conversion: thumb-screw faceplates not supported.':'TDSFF: additional Z-height. Bottom-side insulation: card construction, not a loose spacer.';
  d.note(note);
}

function signalStrip(d,phase) {
  const rows={
    overview:['Off','Off','--','--','0','0 asserted'],
    off:['Off','Off','--','--','0','0 asserted'],
    id:['On','Optional','0','0','0','0 asserted'],
    aux:['On','On','1','0','1 when ready','0 asserted'],
    main_ramp:['On','On','1','1','Wait for rails','0 asserted'],
    main_ready:['On','On','1','1','1 / rails valid','1 released'],
    programming:['On','Optional','0','1','0','0 asserted'],
    programming_signals:['On','Optional','0','1','0','0 asserted'],
    return_id:['On','Optional','0','0','0','0 asserted'],
  };
  const names=['+3.3V_EDGE','+12V_EDGE','AUX_PWR_EN','MAIN_PWR_EN','NIC_PWR_GOOD','PERST#'];
  for(let i=0;i<6;i++) {
    const x=80+i*292;
    d.box(x,380,280,190,names[i],rows[phase][i],{size:25,detailSize:30,color:i===4?C.green:C.blue,fill:i===4?C.greenTint:C.faint});
  }
}

function m3(d,s) {
  const phase=['overview','off','id','aux','main_ramp','main_ready','programming','programming_signals','return_id'].indexOf(s.scene);
  const active=phase<=1?0:phase===2?1:phase===3?2:phase<=5?3:-1;
  d.orientation('Normal power-up: four mandatory states','Conceptual sequence; expanded event spacing, not a timing waveform.');
  const titles=['NIC Power Off','ID Mode','Aux Power','Main Power'];
  for(let i=0;i<4;i++) {
    const x=80+i*460;
    const detail=i===3&&s.scene==='main_ramp'?'Await main rails':['Rails off','Read identity','AUX domain ready','Full operation'][i];
    d.box(x,170,380,155,titles[i],detail,{size:33,detailSize:29,color:C.green,fill:active===i?C.greenTint:C.white,active:active===i});
    if(i<3) d.arrow(x+380,247,x+460,247,{color:i<active?C.green:C.line});
  }
  signalStrip(d,s.scene);
  let note='Separate the edge rails, enables, and the card readiness indication.';
  if(s.scene==='id') note='ID Mode must not rely on +12V_EDGE, even when that rail is present.';
  if(s.scene==='aux') note='AUX rails within tolerance + NIC_PWR_GOOD; PERST# remains asserted.';
  if(s.scene==='main_ramp') note='Wait for main-rail readiness and the specified reset-release conditions.';
  if(s.scene==='main_ready') note='PCIe operates only after rail readiness and specified reset timing are satisfied.';
  if(phase>=6) note='Optional branch: MAIN_PWR_EN = 1, but AUX/Main regulators stay disabled.';
  if(s.scene==='return_id') note='Back in ID Mode: AUX_PWR_EN = 0 and MAIN_PWR_EN = 0; AUX/Main regulators stay disabled.';
  d.paragraph(80,590,1760,80,note,{size:34,color:phase>=6?C.blue:C.ink,weight:700});
  d.text(80,698,'Separate optional branch',{size:31,weight:700,color:C.blue});
  const branchActive=phase>=6;
  d.box(520,700,340,170,'ID Mode','', {size:34,color:C.blue,fill:branchActive?C.blueTint:C.faint,active:s.scene==='return_id'});
  d.box(1060,700,590,170,'Programming Mode','Supported cards only',{size:34,detailSize:28,color:C.blue,fill:branchActive?C.blueTint:C.faint,active:branchActive&&s.scene!=='return_id'});
  d.arrow(860,785,1060,785,{color:branchActive?C.blue:C.line,dash:'10 8'});
  d.curve([1355,870],[1355,944],[690,944],[690,870],{color:s.scene==='return_id'?C.blue:C.line,dash:'10 8'});
  d.text(940,877,'Return to ID Mode',{size:28,color:C.blue,anchor:'middle'});
  d.note('Programming: optional ID branch; FRU EEPROM update with AUX/Main regulators off.');
}

function trafficDiagram(d,pass,p) {
  d.orientation(pass?'NC-SI pass-through traffic':'NC-SI control traffic','NC-SI over RBT example; independent of host CPU execution.');
  d.box(80,220,350,310,'BMC','Management controller',{size:40,detailSize:32,color:C.blue,fill:C.blueTint});
  d.box(740,220,490,310,'NIC network controller',pass?'Carries BMC network packets':'Configures channels; queries state',{size:40,detailSize:32,color:C.green,fill:C.greenTint});
  d.box(1530,220,310,310,'Network','Ethernet port',{size:40,detailSize:32,color:C.blue});
  d.arrow(430,375,740,375,{color:pass?C.green:C.blue,p});
  d.text(585,307,pass?'Pass-through':'Control',{size:29,weight:700,color:pass?C.green:C.blue,anchor:'middle'});
  if(pass) d.arrow(1230,375,1530,375,{color:C.green,p:clamp(p*2-1)});
  d.box(740,695,490,165,'Host CPU','Separate PCIe path',{size:35,detailSize:29,color:C.muted,fill:C.faint});
  d.line(985,695,985,530,C.line,6,'10 8');
  d.text(1035,590,'Not needed for BMC sideband traffic',{size:30,color:C.muted});
  d.note(pass?'Pass-through: BMC network packets through the NIC Ethernet port.':'Control: configuration and queries; can operate without pass-through.');
}

function sharedBus(d,s) {
  const inactive=['bypass','isolation','summary'].includes(s.scene);
  d.orientation(inactive?'Inactive-slot example: two separate protections':'Shared RBT interface: one active transmitter','Illustrative token pass; not a bus-rate or timing simulation.');
  d.box(80,265,330,200,'BMC','Shared RBT interface',{size:34,detailSize:29,color:C.blue,fill:C.blueTint});
  d.line(410,350,1690,350,C.blue,7);
  d.text(970,263,'Shared RBT data path',{size:32,weight:700,color:C.blue,anchor:'middle'});
  const t=clamp(s.elapsed/Math.min(5,s.sceneDuration*.8));
  const activeB=s.scene==='token'&&t>=.55&&t<1;
  d.box(500,590,380,160,'Slot A',activeB?'Waiting':'Active transmitter',{size:34,detailSize:29,color:C.green,fill:C.greenTint,active:!activeB});
  d.box(1300,590,380,160,'Slot B',inactive?'Off / empty / ID Mode':activeB?'Active transmitter':'Waiting',{size:34,detailSize:29,color:inactive?C.muted:C.blue,fill:inactive?C.faint:C.blueTint,active:activeB});
  d.line(690,350,690,590,C.green,6);
  if(inactive) {
    d.line(1490,350,1490,435,C.line,5);
    d.line(1490,485,1490,590,C.line,5);
    d.line(1467,476,1513,438,C.muted,5);
    d.paragraph(1550,432,280,100,'Data path isolated',{size:29,color:C.muted,weight:700});
  } else d.line(1490,350,1490,590,C.blue,6);
  if(inactive) {
    d.path('M880,670 L1020,670 L1020,865 L690,865',C.blue,6);
    d.arrow(690,865,690,750,{color:C.blue});
    d.text(1050,778,'Bypass inactive slot',{size:31,weight:700,color:C.blue});
    d.dot(960,670,16,C.lime);
  } else {
    d.arrow(880,670,1300,670,{color:C.blue});
    d.curve([1490,750],[1490,886],[690,886],[690,750],{color:C.blue});
    d.text(1090,908,'Closed arbitration ring',{size:31,weight:700,color:C.blue,anchor:'middle'});
    const moving=s.scene==='token'?t:0;
    if(moving<.55) d.dot(904+372*(moving/.55),670,16,C.lime);
    else {
      const q=(moving-.55)/.45;
      const start=[1490,750],c1=[1490,886],c2=[690,886],end=[690,774];
      const b=(a,c,e,f)=>Math.pow(1-q,3)*a+3*Math.pow(1-q,2)*q*c+3*(1-q)*q*q*e+q*q*q*f;
      d.dot(b(start[0],c1[0],c2[0],end[0]),b(start[1],c1[1],c2[1],end[1]),16,C.lime);
    }
  }
  d.note(inactive?'Arbitration bypass + data isolation. Not a complete platform hot-swap procedure.':'Hardware arbitration: only one transmitter on the shared RBT interface.');
}

function m4(d,s) {
  if(s.scene==='control'||s.scene==='pass_through') trafficDiagram(d,s.scene==='pass_through',clamp(s.elapsed/2.5));
  else sharedBus(d,s);
}

function airflowCard(d,x,kind,{active=true,particles=0}={}) {
  const hot=kind==='hot',color=hot?C.hot:C.cold;
  d.text(x+410,183,hot?'Hot-aisle installation':'Cold-aisle installation',{size:38,weight:700,color,anchor:'middle'});
  d.text(x+410,243,hot?'Typical local inlet: 55 C':'Typical local inlet: 25-35 C',{size:30,color,anchor:'middle'});
  d.rect(x+80,345,650,355,{fill:active?C.greenTint:C.faint,stroke:C.lime,r:8});
  d.rect(x+50,345,30,355,{fill:C.muted,stroke:C.muted,r:0});
  for(let i=0;i<2;i++) d.rect(x+25,408+i*155,78,76,{fill:C.faint,stroke:C.muted,r:4});
  d.rect(x+730,453,45,136,{fill:'#d8b652',stroke:C.amber,r:0});
  d.rect(x+285,425,320,170,{fill:C.white,stroke:C.muted,r:4});
  for(let i=0;i<7;i++) d.line(x+295,440+i*22,x+595,440+i*22,C.muted,4);
  d.text(x+410,621,'Top-side heatsink',{size:30,weight:700,color:C.green,anchor:'middle'});
  d.text(x+90,715,'Faceplate / I-O side',{size:27,color:C.muted});
  d.text(x+555,715,'Card-edge side',{size:27,color:C.muted});
  if(hot) d.arrow(x+725,790,x+80,790,{color});
  else d.arrow(x+80,790,x+725,790,{color});
  d.text(x+410,827,hot?'Preheated approach air':'System-inlet approach air',{size:30,color,weight:700,anchor:'middle'});
  if(active&&particles>0&&particles<1) {
    for(let lane=0;lane<3;lane++) {
      const progress=clamp(particles*1.4-lane*.17);
      if(progress>0&&progress<1) {
        const px=hot?x+770-740*progress:x+30+740*progress;
        d.dot(px,[375,495,580][lane],8,color);
      }
    }
  }
}

function m5(d,s) {
  d.orientation('Fixed card orientation; opposite approach directions','Separate installation cases, not an operating fan reversing direction.');
  const hotActive=s.scene!=='cold',coldActive=s.scene!=='hot';
  const hotProgress=clamp((s.time-s.sceneStarts.hot)/6);
  const coldProgress=clamp((s.time-s.sceneStarts.cold)/6);
  airflowCard(d,70,'hot',{active:hotActive,particles:hotActive?hotProgress:0});
  airflowCard(d,1030,'cold',{active:coldActive,particles:coldActive?coldProgress:0});
  d.line(960,185,960,887,C.line,2);
  if(s.scene==='topside'||s.scene==='comparison') {
    d.text(80,908,'No bottom-side cooling airflow in either case.',{size:31,weight:700,color:C.blue});
  }
  d.note('Cooling capacity: local inlet temperature + velocity + card/system design. No universal headroom percentage.');
}

function m6(d,s) {
  const phase=['presence','fru','records','selection','checklist'].indexOf(s.scene);
  d.orientation('Presence detection is not configuration','Capability discovery and record-version checks in ID Mode.');
  d.text(80,185,phase===4?'Other v1.6 implementation checks':'SFF: predefined decoder',{size:37,weight:700,color:C.blue});
  d.text(930,185,'DSFF: card-declared capabilities',{size:37,weight:700,color:C.green});
  if(phase===4) {
    const checks=[['Gen 6 signal integrity','Use OCP-specific fixtures and insertion-loss context.'],['Power-state conditions','Verify which optional interfaces are supported in each state.'],['FRU allocation','Extended OEM: 0xD2. Flex I/O: 0xD3.'],['LFF deprecated','Appendix 9 preserves historical context.']];
    for(const [i,[head,body]] of checks.entries()) {
      const y=280+i*155;
      d.text(100,y,head,{size:33,color:C.blue,weight:700});
      d.paragraph(100,y+47,650,85,body,{size:29,color:C.muted});
    }
  } else {
    d.box(100,250,650,160,'PRSNTB presence encoding','',{size:35,color:C.blue,fill:C.blueTint});
    d.arrow(425,410,425,455,{color:C.blue});
    d.box(100,455,650,160,'Defined SFF lookup table','Card and baseboard capabilities',{size:35,detailSize:29,color:C.blue});
    d.arrow(425,615,425,670,{color:C.blue});
    d.box(100,670,650,135,'Supported lane grouping','',{size:35,color:C.blue});
  }
  d.box(930,250,870,160,'PRSNTB: DSFF detected','Presence is not a subdivision table',{size:35,detailSize:29,color:C.green,fill:C.greenTint,active:phase===0});
  const recordColor=phase>=1?C.green:C.line;
  d.line(1365,410,1365,430,recordColor,5);
  d.line(1067,430,1663,430,recordColor,5);
  for(const x of [1067,1365,1663]) d.arrow(x,430,x,455,{color:recordColor,head:14,sw:5});
  const recs=[['0xD0','Declared subdivision / BIF'],['0xD1','Where implemented'],['0xD2','Capabilities\nEncoding width']];
  for(let i=0;i<3;i++) d.box(930+i*298,455,274,190,recs[i][0],recs[i][1],{size:32,detailSize:27,color:C.green,fill:phase>=1?C.greenTint:C.faint,active:phase===2});
  for(const x of [1067,1365,1663]) d.line(x,645,x,658,recordColor,4);
  d.line(1067,658,1663,658,recordColor,4);
  d.text(1365,683,'Read relevant FRU records and check versions',{size:29,color:phase>=1?C.green:C.muted,weight:700,anchor:'middle'});
  d.arrow(1365,736,1365,775,{color:phase>=3?C.green:C.line});
  d.box(930,775,870,160,'Select a mutually supported subdivision','Drive the card-declared BIF encoding',{size:34,detailSize:29,color:C.green,fill:phase>=3?C.greenTint:C.faint,active:phase>=3});
  d.line(835,200,835,887,C.line,2);
  d.note('Mechanical fit alone does not establish DSFF encoding or lane-topology compatibility.');
}

export const renderers={
  m1_host_topologies:m1,
  m2_dsff_slot_conversion:m2,
  m3_power_states_synchronized:m3,
  m4_ncsi_arbitration:m4,
  m5_airflow_comparison:m5,
  m6_dsff_discovery:m6,
};

export function renderScene(id,time,timeline) {
  let index=0;
  for(let i=0;i<timeline.scenes.length;i++) if(time>=timeline.scenes[i].start) index=i;
  const scene=timeline.scenes[index];
  const d=new Drawing();
  renderers[id](d,{scene:scene.id,elapsed:time-scene.start,time,duration:timeline.duration,sceneDuration:(timeline.scenes[index+1]?.start??timeline.duration)-scene.start,sceneStarts:Object.fromEntries(timeline.scenes.map(scene=>[scene.id,scene.start]))});
  return {svg:d.svg(),texts:d.texts,bounds:d.bounds,scene:scene.id};
}

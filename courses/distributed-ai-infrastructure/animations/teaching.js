/* Deterministic, one-pass SVG teaching media. All motion is driven by measured WAV time. */
(() => {
  'use strict';
  const C={ink:'#23394D',gray:'#5F6062',muted:'#77828A',line:'#CAD2D7',pale:'#F3F6F7',green:'#8DC63F',light:'#EDF6E3',white:'#FFFFFF'};
  const cfg=window.TEACHING_CONFIG;
  const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  const clamp=x=>Math.max(0,Math.min(1,x));
  const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
  const fmt=x=>Math.round(x*1000)/1000;
  const text=(x,y,s,size=36,fill=C.ink,anchor='start',weight=500)=>`<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor}" font-weight="${weight}">${esc(s)}</text>`;
  const lines=(x,y,ss,size=34,fill=C.gray,anchor='start',gap=47)=>ss.map((s,i)=>text(x,y+i*gap,s,size,fill,anchor)).join('');
  const rect=(x,y,w,h,fill=C.pale,stroke='none',radius=18)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;
  const line=(x1,y1,x2,y2,color=C.line,width=3,dash='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
  // Explicit heads: path ends at flat-back center; tip touches the target boundary.
  const arrow=(x1,y1,x2,y2,color=C.ink,width=4)=>{
    const a=Math.atan2(y2-y1,x2-x1),bx=x2-15*Math.cos(a),by=y2-15*Math.sin(a),dx=7*Math.sin(a),dy=-7*Math.cos(a);
    return line(x1,y1,bx,by,color,width)+`<polygon points="${x2},${y2} ${bx+dx},${by+dy} ${bx-dx},${by-dy}" fill="${color}"/>`;
  };
  const circle=(x,y,r,fill=C.green,stroke='none')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="3"/>`;
  const pill=(x,y,w,label,fill=C.pale,color=C.ink,size=30)=>rect(x,y,w,60,fill,'none',30)+text(x+w/2,y+41,label,size,color,'middle',600);
  const card=(x,y,w,h,kicker,value,note='',fill=C.pale)=>rect(x,y,w,h,fill)+text(x+32,y+52,kicker,30,C.gray)+text(x+40,y+122,value,44,C.ink,'start',650)+(note?text(x+32,y+h-30,note,29,C.gray):'');
  const dots=(x,y,n,active=4,labels=true)=>Array.from({length:n},(_,i)=>circle(x+i*92,y,30,i<active?C.green:C.white,i<active?'none':C.line)+(labels?text(x+i*92,y+11,String(i+1),27,C.ink,'middle',600):'')).join('');
  const strip=(name)=>text(100,88,name,32,C.gray,'start',600)+pill(1460,40,360,'Illustrative example',C.pale,C.gray,28);
  const footer=(a,b='')=>line(100,945,1820,945)+text(100,1005,a,35,C.ink,'start',600)+(b?text(100,1048,b,27,C.gray):'');
  const ptime=(p,t)=>clamp((t-cfg.paragraphs[p].start)/(cfg.paragraphs[p].end-cfg.paragraphs[p].start));
  const para=t=>Math.max(0,cfg.paragraphs.findIndex(p=>t>=p.start&&t<p.end));
  const at=(p,f=0)=>cfg.paragraphs[p].start+(cfg.paragraphs[p].end-cfg.paragraphs[p].start)*f;
  const reached=(t,p,f=0)=>t>=at(p,f);
  const animate=(t,start,end)=>ease((t-start)/(end-start));
  const event=(name,fallback)=>cfg.events?.[name]??fallback;
  const timedReadiness=(t,name,p)=>{
    const start=event(name+'_start',at(p,.12)),early=event(name+'_early',at(p,.40)),late=event(name+'_late',at(p,.62));
    return t<early?100/140*animate(t,start,early):100/140+40/140*animate(t,early,late);
  };
  const bar=(x,y,w,h,fill=C.green)=>rect(x,y,Math.max(0.01,w),h,fill,'none',5);

  function m1(t){
    let s=strip('Independent requests  /  one required training group');
    const chartX=480,scale=8.15, top=226,bottom=610;
    const serving=timedReadiness(t,'serving',1);
    const training=timedReadiness(t,'training',2);
    const wait=training>=.9999,showMath=reached(t,3);
    s+=text(100,170,'Serving replicas',39,C.ink,'start',650)+text(100,215,'One request each',28,C.gray);
    s+=text(100,552,'Training group',39,C.ink,'start',650)+text(100,597,'All four required',28,C.gray);
    for(let i=0;i<4;i++){
      const val=i===3?140:100,yy=top+i*63,by=bottom+i*63;
      s+=text(380,yy+30,String.fromCharCode(65+i),30,C.gray,'end');
      s+=bar(chartX,yy,140*scale,34,C.pale)+bar(chartX,yy,Math.min(val,140*serving)*scale,34);
      if(140*serving>=val-.01)s+=text(1770,yy+29,`${val} ms`,29,C.ink,'end');
      s+=text(380,by+30,String.fromCharCode(65+i),30,C.gray,'end');
      s+=bar(chartX,by,140*scale,34,C.pale)+bar(chartX,by,Math.min(val,140*training)*scale,34);
      if(training>100/140&&i<3)s+=bar(chartX+100*scale,by,Math.min(40,140*training-100)*scale,34,'url(#wait)');
      if(140*training>=val-.01)s+=text(1770,by+29,`${val} ms`,29,C.ink,'end');
    }
    if(wait)s+=line(chartX+140*scale,bottom-16,chartX+140*scale,bottom+226,C.ink,3)+text(chartX+140*scale,bottom-35,'Group ready',29,C.ink,'middle',600);
    if(showMath){
      s+=pill(100,858,680,'3 × 40 ms = 120 GPU-ms waiting',C.light,C.ink,32);
      s+=pill(810,858,420,'Elapsed delay: +40 ms',C.pale,C.ink,32);
    }
    if(reached(t,4))s+=pill(1280,858,540,'Independent job: continues',C.light,C.ink,31);
    s+=footer(reached(t,5)?'The dependency defines the affected work.':'Timing shown in milliseconds (ms).', 'Teaching model: no communication duration or overlapping work.');
    return s;
  }

  function replica(x,y,i,updated=false,grad=null){
    let s=rect(x,y,380,235,C.pale)+text(x+30,y+48,`Rank ${i}`,30,C.gray)+pill(x+220,y+20,135,updated?'Step 43':'Step 42',C.white,C.gray,24);
    s+=text(x+190,y+124,updated?'w = 9.5':'w = 10',52,C.ink,'middle',650)+text(x+190,y+186,'Same model replica',28,C.gray,'middle');
    if(grad!==null)s+=arrow(x+190,y+235,x+190,y+292,C.ink)+circle(x+190,y+336,44,C.light,C.green)+text(x+190,y+348,String(grad),35,C.ink,'middle',650);
    return s;
  }
  function m2(t){
    const p=para(t); let s=strip('Data parallelism  /  declared reduction  /  valid state');
    if(p<=3){
      const grads=t>=event('gradients',at(1,.2)),sum=reached(t,2,.08),avg=t>=event('mean',at(2,.32)),updated=t>=event('updated',at(3,.6));
      for(let i=0;i<4;i++)s+=replica(100+i*440,190,i,updated,grads?[2,4,6,8][i]:null);
      if(!grads){
        for(let i=0;i<4;i++){
          const x=100+i*440;
          s+=rect(x+50,620,280,105,C.light)+text(x+190,685,`Input batch ${String.fromCharCode(65+i)}`,32,C.ink,'middle',600)+arrow(x+190,620,x+190,425,C.ink,3);
        }
        s+=text(960,825,'Same initial model · different input data',38,C.gray,'middle');
      }
      if(grads)s+=text(100,150,'Local gradients · step 42',31,C.gray);
      if(sum){
        s+=line(290,570,290,640,C.ink)+line(730,570,730,640,C.ink)+line(1170,570,1170,640,C.ink)+line(1610,570,1610,640,C.ink)+line(290,640,1610,640,C.ink);
        s+=arrow(950,640,950,690,C.ink)+rect(390,690,1120,140,C.light);
        s+=text(950,748,avg?'(2 + 4 + 6 + 8) ÷ 4 = 5':'2 + 4 + 6 + 8 = 20',49,C.ink,'middle',650);
        s+=text(950,799,avg?'Averaged gradient · same result for every participant':'Sum reduction · division is a separate declared step',29,C.gray,'middle');
      }
      if(p===3)s+=pill(590,856,720,'10 − (0.1 × 5) = 9.5',C.pale,C.ink,40);
      s+=footer('One scalar weight · equally weighted batches · simple SGD','Conceptual reduction path; no transport topology or overlap implied.');
    }else if(p===4){
      s+=text(100,185,'Replicated models',43,C.ink,'start',650)+text(1070,185,'Partitioned model',43,C.ink,'start',650);
      s+=rect(100,230,770,590,C.pale)+rect(1070,230,750,590,C.pale);
      for(let i=0;i<4;i++){
        const xx=150+(i%2)*350,yy=290+Math.floor(i/2)*250;
        s+=rect(xx,yy,300,180,C.white,C.line)+text(xx+150,yy+75,'Full model',38,C.ink,'middle',600)+text(xx+150,yy+133,'w = 9.5',39,C.ink,'middle');
      }
      const colors=[C.ink,C.gray,C.green,C.muted];
      for(let i=0;i<4;i++)s+=rect(1120+i*160,360,140,230,colors[i])+text(1190+i*160,455,`Part ${i+1}`,29,i===2?C.ink:C.white,'middle',600);
      s+=text(1450,690,'Tensor or pipeline partitions',32,C.gray,'middle');
      s+=footer('Distribution choices create different communication dependencies.');
    }else{
      s+=text(100,190,'Supported recovery boundary',43,C.ink,'start',650);
      s+=card(100,300,430,300,'Replacement worker','State missing','Candidate participant');
      s+=card(700,300,520,300,'Restore required state','Model + optimizer','Input progress + other state',C.light);
      s+=card(1390,300,430,300,'Membership checks','Admission held','Resume after validation');
      s+=arrow(530,450,700,450)+arrow(1220,450,1390,450);
      s+=rect(100,690,1720,160,C.pale)+text(960,751,'Aligned replicas:  w = 10  →  mean gradient 5  →  w = 9.5',40,C.ink,'middle',650)+text(960,809,'Operation identity and required state govern participation.',32,C.gray,'middle');
      s+=footer('An available device is not automatically a valid participant.');
    }
    return s;
  }

  function readinessPanel(x,label,values,showWait){
    const y=220,w=815,start=x+125,k=22;
    let s=rect(x,y,w,590,C.pale)+text(x+35,y+65,label,36,C.ink,'start',650);
    for(let i=0;i<4;i++){
      const yy=y+125+i*90,v=values[i];
      s+=text(x+65,yy+31,String.fromCharCode(65+i),30,C.gray,'middle');
      s+=bar(start,yy,v*k,40,C.green);
      if(showWait&&v<25)s+=bar(start+v*k,yy,(25-v)*k,40,'url(#wait)');
      s+=text(start+v*k,yy-12,`${v} ms`,28,C.ink,'middle');
    }
    s+=line(start,y+493,start+25*k,y+493,C.line,2);
    for(const v of [0,5,10,15,20,25])s+=text(start+v*k,y+531,String(v),25,C.gray,'middle');
    s+=text(start+275,y+571,'Time until required contribution is ready (ms)',24,C.gray,'middle');
    return s;
  }
  function m3(t){
    const p=para(t);let s=strip('Causal order  /  clock readings  /  group completion');
    if(p<=2){
      s+=pill(100,182,330,'Host A · sender',C.pale,C.ink,33)+pill(100,520,330,'Host B · receiver',C.pale,C.ink,33);
      s+=line(500,300,1740,300,C.line,4)+line(500,640,1740,640,C.line,4);
      s+=circle(770,300,20,C.ink)+circle(1390,640,20,C.green);
      s+=text(770,250,'Local clock: 100 ms',38,C.ink,'middle',600)+text(1790,600,'Local clock: 97 ms',38,C.ink,'end',600);
      if(p>=1){
        s+=pill(100,345,420,'Reference: 100 ms',C.pale,C.gray,31)+pill(1180,685,420,'Reference: 103 ms',C.light,C.ink,31);
        s+=text(1490,810,'B offset: −6 ms',35,C.gray,'middle');
      }
      if(p>=2){
        s+=arrow(787.539,309.618,1372.461,630.382,C.ink,5)+text(1240,430,'Message m7',32,C.ink,'middle',600);
        s+=circle(565,640,15,C.white,C.gray)+text(565,706,'Unrelated event',28,C.gray,'middle');
      }
      s+=footer(p>=2?'Matching message identity establishes send → receive.':'Local timestamps need offset and uncertainty context.', 'Timing values are illustrative; no backward message travel.');
    }else{
      const second=p>=4&&t>=event('second_case',at(4,.25)),wait=p>=5;
      s+=readinessPanel(100,'Case A · [10, 10, 10, 10]',[10,10,10,10],false);
      if(second)s+=readinessPanel(1005,'Case B · [5, 5, 5, 25]',[5,5,5,25],wait);
      else s+=rect(1005,220,815,590,C.white,C.line)+text(1412,460,'Same operation',43,C.ink,'middle',650)+lines(1412,530,['All four required','No overlapping work'],34,C.gray,'middle');
      s+=pill(140,835,735,'Mean: 10 ms   ·   Group ready: 10 ms',C.light,C.ink,31);
      if(second)s+=pill(1045,835,735,'Mean: 10 ms   ·   Group ready: 25 ms',C.light,C.ink,31);
      s+=footer(wait?'Elapsed difference: +15 ms     |     Waiting: 3 × 20 = 60 participant-ms':'Same mean does not establish the same group completion time.', p>=6?'Four samples do not establish a percentile or diagnose a cause.':'Illustrative readiness values; separate communication duration omitted.');
    }
    return s;
  }

  function regions(){return rect(100,220,640,580,C.pale)+rect(1180,220,640,580,C.pale)+text(140,285,'Region A',37,C.ink,'start',650)+text(1220,285,'Region B',37,C.ink,'start',650)+line(960,190,960,850,C.line,3,'10 12')}
  function m4(t){
    const p=para(t);let s=strip('One regional boundary  /  three dependency patterns');
    if(p<=1){
      s+=regions()+rect(280,405,290,180,C.white,C.line)+rect(1350,405,290,180,C.white,C.line);
      s+=text(425,485,'Request',39,C.ink,'middle',600)+text(425,538,'Waiting',30,C.gray,'middle')+text(1495,485,'Remote work',37,C.ink,'middle',600)+text(1495,538,'Response',30,C.gray,'middle');
      s+=arrow(570,465,1350,465,C.ink)+arrow(1350,535,570,535,C.green);
      s+=rect(755,360,410,68,C.white)+text(960,406,'1,000 km cable path',32,C.ink,'middle',600);
      if(p>=1){
        s+=rect(775,580,370,66,C.white)+text(960,625,'5 ms each way',35,C.ink,'middle',650);
        s+=text(420,697,'Blocking exchange',33,C.gray,'middle')+text(1500,697,'Propagation is only one part',29,C.gray,'middle');
        s+=pill(415,850,1090,'1,000 km ÷ 200,000 km/s = 0.005 s = 5 ms',C.light,C.ink,36);
      }
      s+=footer(reached(t,1,.85)?'Private connectivity does not remove propagation delay.':'Assumed optical propagation speed: 200,000 km/s', 'Illustrative path and speed; processing, queuing and other delays excluded.');
    }else if(p<=4){
      let count=8,sec=0;
      if(p>=3){sec=t<event('buffer_6',at(3,.30))?0:t<event('buffer_4',at(3,.48))?1:t<event('buffer_2',at(3,.66))?2:t<event('buffer_0',at(4,.35))?3:t<event('supply_limited',at(4,.64))?4:5;count=Math.max(0,8-2*sec)}
      const deficit=t>=event('supply_drop',at(2,.78));
      s+=text(100,190,'Buffered data supply',43,C.ink,'start',650);
      s+=card(100,325,390,290,'Region A · producer',deficit?'2 batches/s':'4 batches/s',deficit?'Supply during dip':'Initial supply');
      s+=rect(680,250,600,500,C.pale)+text(980,315,'Region B · buffer',37,C.ink,'middle',650);
      for(let i=0;i<8;i++){
        const xx=735+(i%4)*125,yy=360+Math.floor(i/4)*125;
        s+=rect(xx,yy,105,95,i<count?C.green:C.white,i<count?'none':C.line,12);
        if(i<count)s+=text(xx+52.5,yy+59,'1',32,C.ink,'middle',600);
      }
      s+=text(980,682,`${count} batches buffered`,43,C.ink,'middle',650);
      s+=card(1470,325,350,290,'Region B · consumer','4 batches/s',sec>=5?'Only 2 supplied/s':'Demand',sec>=5?C.pale:C.light);
      s+=arrow(490,470,680,470)+arrow(1280,470,1470,470);
      s+=pill(625,810,670,`Dip elapsed: ${sec} s   ·   Buffer: ${count}`,C.light,C.ink,38);
      s+=footer(sec>=5?'Buffer exhausted: consumer becomes supply-limited.':sec===3?'Three-second deficit uses six batches; two remain.':deficit?'Shortfall: 4 − 2 = 2 batches per second.':'Balanced flow: 4 supplied − 4 consumed = 0 deficit.', 'Equal-sized batches · simplified continuous flow · illustrative rates.');
    }else{
      s+=regions()+text(420,382,'Independent serving',37,C.ink,'middle',650)+text(1500,382,'Controlled test',37,C.ink,'middle',650);
      s+=rect(240,440,360,195,C.white,C.line)+text(420,520,'Model v1',48,C.ink,'middle',650)+text(420,580,'Approved traffic',31,C.gray,'middle');
      s+=rect(1320,440,360,195,C.light)+text(1500,520,'Model v2',48,C.ink,'middle',650)+text(1500,580,'Validate before promotion',28,C.gray,'middle');
      s+=pill(245,680,350,'Local requests',C.white,C.ink,30)+pill(1325,680,350,'Test traffic',C.white,C.ink,30);
      if(p>=6)s+=pill(100,850,520,'Blocking exchange',C.pale,C.ink,32)+pill(700,850,520,'Buffered supply',C.light,C.ink,32)+pill(1300,850,520,'Independent serving',C.pale,C.ink,32);
      s+=footer('Service rollout and session policies define the required consistency.');
    }
    return s;
  }

  function job(x,y,label,state,failed=false){
    let s=rect(x,y,760,255,C.pale)+text(x+35,y+57,label,38,C.ink,'start',650);
    for(let i=0;i<4;i++){
      const xx=x+80+i*170;
      s+=rect(xx,y+95,90,70,failed&&i===2?C.white:C.green,failed&&i===2?C.gray:'none',8)+text(xx+45,y+140,String(i+1),31,C.ink,'middle',650);
      if(failed&&i===2)s+=line(xx+20,y+110,xx+70,y+150,C.ink,4)+line(xx+70,y+110,xx+20,y+150,C.ink,4);
    }
    s+=text(x+35,y+218,state,32,C.gray);
    return s;
  }
  function m5(t){
    const p=para(t);let s=strip('Observe  /  bound the response  /  validate before action');
    if(p<=4){
      const failed=t>=event('failure',at(1,.56)),restored=p>=3,resumed=p>=4;
      s+=job(100,175,'Training group A',resumed?'Validated · resume at step 43':restored?'Restore committed state after step 42':failed?'Step 45 interrupted · group stopped':'Checkpoint after step 42',failed&&!restored);
      s+=job(1060,175,'Independent group B','Healthy · continues');
      s+=line(960,165,960,452,C.line,3,'10 12');
      const xx=[170,585,1000,1415],ww=335;
      const labels=['Checkpoint 42','Step 43','Step 44','Step 45'];
      for(let i=0;i<4;i++){
        const active=i===0||p>=1;
        s+=rect(xx[i],520,ww,145,active?(i===0?C.light:C.pale):C.white,C.line);
        s+=text(xx[i]+ww/2,574,labels[i],34,C.ink,'middle',650);
        s+=text(xx[i]+ww/2,626,i===0?'Committed':p===0?'Pending':i===3?(failed?'Partial work':'In progress'):'Completed',28,C.gray,'middle');
        if(i<3)s+=arrow(xx[i]+ww,592,xx[i+1],592,C.ink,3);
      }
      if(p===2){
        s+=pill(140,728,510,'Correlate failure evidence',C.pale,C.ink,30)+pill(710,728,510,'Check spare + capacity',C.pale,C.ink,30)+pill(1280,728,510,'Restore required state',C.light,C.ink,30);
        s+=text(960,868,'Health · communication · power · cooling',34,C.gray,'middle');
      }else if(restored){
        s+=rect(560,714,1215,140,C.light)+text(1167,768,'Replay: completed 43 + completed 44 + partial 45',35,C.ink,'middle',650)+text(1167,821,resumed?'Membership and restored state validated':'Explicit recovery to a known checkpoint',31,C.gray,'middle');
        s+=line(1700,700,337,700,C.gray,3)+arrow(337,700,337,665,C.gray,3)+text(337,750,'Restore 42',30,C.gray,'middle');
      }else s+=text(960,800,failed?'Recovery scope: group A':'Each group has its own state and progress.',39,C.ink,'middle',650);
      s+=footer(resumed?'Bound retries and provide an escalation path.':'Available resources still need readiness evidence.', 'Illustrative whole-group restart; shared failures may require a wider response.');
    }else{
      s+=text(100,185,'Expansion admission · same facility boundary',43,C.ink,'start',650);
      s+=card(100,270,750,270,'Approved remaining headroom','30 kW','Validated facility capacity',C.light);
      s+=card(1070,270,750,270,'Expansion request','40 kW','Additional required power',C.pale);
      const x=280,sc=30;
      s+=text(100,645,'Available',31,C.gray)+bar(x,610,30*sc,60,C.green)+text(x+30*sc+30,655,'30 kW',36,C.ink);
      s+=text(100,755,'Required',31,C.gray)+bar(x,720,40*sc,60,C.ink)+text(x+40*sc+30,765,'40 kW',36,C.ink);
      s+=pill(660,840,600,'Admission pending',C.pale,C.ink,40);
      s+=footer('Recovery scope + valid state + approved capacity', 'Illustrative power values; idle device count does not establish readiness.');
    }
    return s;
  }

  const functions={1:m1,2:m2,3:m3,4:m4,5:m5};
  window.setTeachingTime=ms=>{
    const t=Math.max(0,Math.min(cfg.durationMs-1,ms));
    document.querySelector('svg').innerHTML=`<defs><pattern id="wait" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="16" height="16" fill="#EDF0F2"/><line x1="0" y1="0" x2="0" y2="16" stroke="#9CA6AE" stroke-width="5"/></pattern></defs><rect width="1920" height="1080" fill="#FFFFFF"/>`+functions[cfg.module](t);
    document.body.dataset.currentMs=String(Math.round(t));
  };
  window.setTeachingTime(0);
  window.playTeaching=()=>{
    const start=performance.now();
    function tick(now){const t=Math.min(cfg.durationMs,now-start);window.setTeachingTime(t);if(t<cfg.durationMs)requestAnimationFrame(tick)}
    requestAnimationFrame(tick);
  };
})();

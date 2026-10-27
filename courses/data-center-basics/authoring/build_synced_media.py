"""Build deterministic, phrase-aligned instructional SVG animation sources.
Inputs are word timestamps from the final WAV, never equal time slices or loop counts.
"""
from pathlib import Path
import json,re,html,hashlib,wave,sys
PREVIEW_V2="--preview-v2" in sys.argv
P=Path(__file__).resolve().parents[1];Q=P/'authoring/qa/audio-video-update'
G='#8DC63F';B='#343895';I='#243244';C='#3B7FA8';H='#BA6545';L='#E5E9EE'
def txt(x,y,text,size=25,anchor='middle',fill=I,weight=500):
 lines=text.split('\n');return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.25}">{html.escape(v)}</tspan>' for i,v in enumerate(lines))+'</text>'
def box(id,x,y,w,h,label,fill='#F1F5ED',stroke=G,size=24):
 n=label.count('\n')+1;y0=y+h/2-(n-1)*size*.625+size*.34
 return f'<g id="{id}" data-box="true"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'+txt(x+w/2,y0,label,size)+'</g>'
def arrow(id,x1,y1,x2,y2,color=G,width=4):
 if y1==y2:
  s=1 if x2>x1 else -1;back=x2-s*13;path=f'M{x1},{y1}H{back}';points=f'{back},{y2-7} {x2},{y2} {back},{y2+7}'
 elif x1==x2:
  s=1 if y2>y1 else -1;back=y2-s*13;path=f'M{x1},{y1}V{back}';points=f'{x2-7},{back} {x2},{y2} {x2+7},{back}'
 else:raise ValueError('use explicit elbow path')
 return f'<g id="{id}"><path class="arrow-shaft" d="{path}" fill="none" stroke="{color}" stroke-width="{width}"/><polygon class="arrowhead" points="{points}" fill="{color}"/></g>'
def elbow(id,path,points,color=B):
 return f'<g id="{id}"><path class="arrow-shaft" d="{path}" fill="none" stroke="{color}" stroke-width="4"/><polygon class="arrowhead" points="{points}" fill="{color}"/></g>'
def tag(id,x,y,w,label,fill='#F0F1FA',stroke=B):return box(id,x,y,w,60,label,fill,stroke,22)
def norm(s):return re.sub(r'[^a-z0-9]+','',s.lower())
def alignment(m,s,anchors):
 data=json.loads((Q/f'alignment/m{m}-s{s}.json').read_text());words=data['words'];tokens=[norm(w['text']) for w in words];beats={};stream=''.join(tokens);offsets=[];offset=0
 for token in tokens:offsets.append((offset,offset+len(token)));offset+=len(token)
 for key,phrase in anchors.items():
  target=norm(phrase);hits=[x.start() for x in re.finditer(re.escape(target),stream)]
  if len(hits)!=1:raise ValueError((m,s,key,phrase,hits))
  start=hits[0];finish=start+len(target);i=next(i for i,(a,b) in enumerate(offsets) if a<=start<b);j=next(i for i,(a,b) in enumerate(offsets) if a<finish<=b)
  beats[key]={'phrase':phrase,'start':words[i]['start'],'end':words[j]['end'],'source':data['source']}
 return data,beats
COMMON='''const el=id=>document.getElementById(id);const clamp=v=>Math.max(0,Math.min(1,v));const ramp=(t,a,b)=>clamp((t-a)/Math.max(.01,b-a));const lerp=(a,b,f)=>a+(b-a)*f;const show=(id,on)=>el(id).style.opacity=on?1:0;const opacity=(id,v)=>el(id).style.opacity=v;const text=(id,v)=>el(id).textContent=v;const fill=(id,v)=>el(id).setAttribute('fill',v);const width=(id,v)=>el(id).setAttribute('width',Math.max(0,v));const cue=id=>TIMING.beats[id].start;const end=id=>TIMING.beats[id].end;const tone=(id,on)=>{const r=el(id).querySelector('rect');if(r)r.setAttribute('fill',on?'#DDEDC8':'#F1F5ED')};function dot(id,path,f,on=true){const p=el(path);const pt=p.getPointAtLength(p.getTotalLength()*clamp(f));el(id).setAttribute('cx',pt.x);el(id).setAttribute('cy',pt.y);show(id,on)};'''
def source(m,s,name,svg,anchors,logic,extra_text,poster_beat):
 data,beats=alignment(m,s,anchors);c=json.loads((P/'course.json').read_text());slide=next(s0 for mod in c['modules'] if mod['id']==m for s0 in mod['slides'] if s0['id']==s)
 a=slide['audio'];wav=(P.parent/'_baselines/2026-10-24-elevenlabs-v2' if PREVIEW_V2 else P)/a['wav_file'];assert hashlib.sha256(wav.read_bytes()).hexdigest()==data['audio_sha256']
 with wave.open(str(wav)) as r:D=r.getnframes()/r.getframerate()
 timing={'module':m,'slide':s,'duration_seconds':D,'fps':30,'audio_sha256':data['audio_sha256'],'script_sha256':data['script_sha256'],'stage':'interim v2 geometry review' if PREVIEW_V2 else 'final delivered WAV','beats':beats,'final_hold_starts':(beats['consequences']['end'] if (m,s)==(4,7) else max(beats['containment']['end'],beats['conditions']['start']) if (m,s)==(2,11) else beats['heat']['start'] if (m,s)==(1,4) else beats[poster_beat]['start'])}
 body=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675"><rect width="1200" height="675" fill="white"/>{svg}</svg>'
 js='const TIMING='+json.dumps(timing)+';window.TIMING=TIMING;'+COMMON+'\nwindow.renderAt=function(ms){const t=Math.max(0,Math.min(ms/1000,TIMING.duration_seconds));'+logic+'};window.renderAt(0);if(new URLSearchParams(location.search).has("play")){let start;function frame(ts){start??=ts;window.renderAt(ts-start);if(ts-start<TIMING.duration_seconds*1000)requestAnimationFrame(frame)}requestAnimationFrame(frame)}'
 out=P/f'animations/module{m}/{name}.html';out.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Editable narration-timed teaching animation</title><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:white}svg{width:100vw;height:100vh;display:block}text{font-family:Arial,sans-serif}g{transition:none}</style>'+f'<body data-duration-ms="{D*1000:.8f}" data-poster-ms="{min(D-.05,beats[poster_beat]["start"]+.8)*1000:.8f}">'+body+'<script>'+js+'</script></body></html>')
 (Q/f'timeline-m{m}-s{s}.json').write_text(json.dumps(timing,indent=2)+'\n')
 # Save all labels and timed state wording for later visible-text review.
 static=[html.unescape(' '.join(re.sub('<[^>]*>',' ',v).split())) for v in re.findall(r'<text\b[^>]*>(.*?)</text>',svg,re.S)]
 return {'module':m,'slide':s,'source':str(out.relative_to(P)),'timing':timing,'text':static+extra_text}

def service():
 b=box('device',50,200,220,175,'',size=27)+txt(160,244,'Your device',27)+box('network',390,225,200,125,'Network',size=27)
 b+='<rect x="710" y="95" width="440" height="325" rx="20" fill="#F8FAF7" stroke="#BCC8B3" stroke-width="2"/>'+txt(930,132,'Service systems',26,weight=700)
 b+=box('compute',755,225,170,125,'Compute',size=26)+box('storage',975,170,135,205,'',size=24)+txt(1042.5,211,'Storage',23)
 b+=arrow('outward',270,245,390,245,B)+arrow('outward-service',590,245,755,245,B)
 b+='<path id="request-path" d="M270,245H755" fill="none" stroke="none"/>'
 b+=arrow('return',755,330,590,330,C)
 b+=arrow('return-device',390,330,270,330,C)
 b+='<path id="response-path" d="M755,330H270" fill="none" stroke="none"/>'
 b+=arrow('read',975,240,925,240,B)+txt(490,175,'Request',23,fill=B)+txt(490,423,'Response',23,fill=C)
 b+='<g id="stored-document"><rect x="1010" y="265" width="56" height="67" rx="4" fill="white" stroke="#343895" stroke-width="2"/><path d="M1020,284H1056M1020,298H1056M1020,312H1045" stroke="#343895" stroke-width="3"/></g>'
 b+='<g id="opened-document"><rect x="127" y="285" width="66" height="54" rx="4" fill="white" stroke="#343895" stroke-width="2"/><path d="M140,301H180M140,314H180M140,327H166" stroke="#343895" stroke-width="3"/></g>'
 b+='<circle id="request-dot" r="10" fill="#343895"/><circle id="response-dot" r="10" fill="#3B7FA8"/>'
 b+=box('power',180,490,350,80,'Electricity powers equipment',fill='#F0F1FA',stroke=B,size=23)+box('heat',670,490,350,80,'Heat must be removed',fill='#FFF0E9',stroke=H,size=23)
 b+=elbow('power-link','M355,490V455H840V433','833,433 840,420 847,433',B)
 b+=elbow('heat-link','M1090,420V530H1033','1033,523 1020,530 1033,537',H)
 b+=txt(600,635,'A simple service action keeps its physical dependencies',27)
 anchors={'open':'Think about opening a shared document','request':'Your device sends a request through networks','compute':'Computing equipment handles the request','storage':'storage holds the information','response':'a response travels back','sequence':'The animation follows that sequence','electricity':'electricity powers the equipment','heat':'cooling removes the heat it produces','conclusion':'A simple action on your device'}
 logic='''const qr=ramp(t,cue('request'),cue('compute'));const rs=ramp(t,cue('response'),end('response'));dot('request-dot','request-path',qr,t>=cue('request')&&t<cue('compute'));dot('response-dot','response-path',rs,t>=cue('response')&&t<end('response'));tone('device',t>=end('response'));tone('network',t>=cue('request')&&t<cue('compute')||t>=cue('response')&&t<end('response'));tone('compute',t>=cue('compute')&&t<cue('response'));tone('storage',t>=cue('storage'));show('opened-document',t>=end('response'));opacity('stored-document',t>=cue('storage')?1:.3);opacity('read',t>=cue('storage')?1:.2);tone('power',t>=cue('electricity'));tone('heat',t>=cue('heat'));opacity('power-link',t>=cue('electricity')?1:.35);opacity('heat-link',t>=cue('heat')?1:.35);document.body.dataset.state=t<cue('request')?'orientation':t<cue('compute')?'request':t<cue('storage')?'processing':t<cue('response')?'storage-read':t<end('response')?'response':t<cue('electricity')?'service-complete':t<cue('heat')?'power-support':'physical-dependencies';'''
 return source(1,4,'service-journey',b,anchors,logic,[], 'conclusion')

def power():
 b=txt(600,48,'Illustrative functional path · event spacing expanded',23,fill='#5F6062')
 b+=box('utility',35,145,170,110,'Utility\nsupply',size=25)+box('transfer',290,145,230,110,'Distribution &\nsource selection',size=23)+box('ups',600,145,170,110,'UPS',size=30)+box('load',960,145,200,110,'Equipment',size=27)
 b+=box('generator',290,355,230,110,'Backup generator',fill='#F0F1FA',stroke=B,size=24)+box('reserve',600,355,220,110,'',size=23)+txt(710,398,'Stored energy',23)
 b+=arrow('utility-route',205,200,290,200,G)+arrow('selected-route',520,200,600,200,G)+arrow('output-route',770,200,960,200,G)
 b+=txt(865,290,'Downstream\ndistribution',22)
 b+=arrow('reserve-route',685,355,685,255,B)+arrow('backup-route',405,355,405,255,B)
 b+='<g id="failure"><path d="M235,183L263,217M263,183L235,217" stroke="#BA6545" stroke-width="6"/></g>'
 b+=txt(710,505,'Illustrative reserve',20)+f'<rect x="625" y="425" width="170" height="16" rx="4" fill="{L}"/><rect id="reserve-level" x="625" y="425" width="170" height="16" rx="4" fill="{B}"/>'
 b+='<text id="generator-caption" x="405" y="505" text-anchor="middle" font-size="24" fill="#343895">Standby</text>'
 b+=txt(70,575,'Equipment\nsupply',23,anchor='start')+'<path d="M250,570H1140" stroke="#DAE0E6" stroke-width="2"/><path id="load-trace" d="M250,555H250" stroke="#8DC63F" stroke-width="5" fill="none"/>'
 b+='<text id="state-label" x="600" y="105" text-anchor="middle" font-size="27" font-weight="700" fill="#243244"></text>'
 for i,label in enumerate(['Capacity','Fuel','Controls','Maintenance']):b+=tag('condition'+str(i),245+i*225,595,210,label)
 anchors={'normal':'the normal supply','equipment':'before reaching equipment','failure':'If the incoming source fails','bridge':'stored energy can bridge the transition','generator':'while a backup generator starts','sequence':'The animation illustrates that sequence','design':'Actual designs differ','capacity':'capacity fuel controls and maintenance','conclusion':'A generator alone'}
 logic='''const fail=end('failure')-.35,bridge=cue('bridge'),start=cue('generator'),ready=end('generator')+.2,transfer=ready+.8;const outage=t>=fail,backup=t>=transfer;opacity('utility-route',outage?.12:1);opacity('selected-route',outage&&!backup?.12:1);opacity('backup-route',backup?1:.12);opacity('reserve-route',outage&&!backup?1:.18);show('failure',outage);tone('utility',!outage);tone('ups',outage&&!backup);tone('generator',backup);text('generator-caption',t<start?'Standby':t<ready?'Starting':t<transfer?'Ready · not selected':'Ready · selected');width('reserve-level',170-55*ramp(t,fail,transfer));const x=250+890*clamp(t/cue('conclusion'));el('load-trace').setAttribute('d','M250,555H'+x);text('state-label',!outage?'Utility selected · equipment supplied':!backup?'UPS reserve bridges the source transition':'Ready backup selected · equipment supplied');for(let i=0;i<4;i++)opacity('condition'+i,t>=cue('capacity')?1:.18);document.body.dataset.state=!outage?'normal':t<bridge?'source-lost':t<start?'reserve-bridge':t<ready?'generator-starting':t<transfer?'generator-ready':'backup-selected';'''
 return source(2,6,'power-continuity',b,anchors,logic,['Utility selected · equipment supplied','UPS reserve bridges the source transition','Ready backup selected · equipment supplied','Standby','Starting','Ready · not selected','Ready · selected'], 'conclusion')

def containment():
 # This reviewed revision owns the editable source and final-WAV word map.
 import build_m2_room_cooling as updated
 previous=updated.core.Q
 try:return updated.animation()
 finally:updated.core.Q=previous

def budgets():
 b=txt(600,45,'Illustrative used share of independent allocations',24,fill='#5F6062')+'<rect x="70" y="100" width="300" height="440" rx="16" fill="#F7F9FB" stroke="#AEB8C5" stroke-width="3"/>'+txt(220,80,'Rack positions',26,weight=700)
 devices=''
 for i in range(8):
  y=125+i*46;b+=f'<rect id="slot{i}" x="98" y="{y}" width="244" height="32" rx="5" fill="white" stroke="#CAD2DC" stroke-width="2"/>'
  if i<2:devices+=f'<rect x="98" y="{y}" width="244" height="32" rx="5" fill="#343895"/>'
  elif i<4:devices+=f'<rect id="device{i}" x="98" y="{y}" width="244" height="32" rx="5" fill="#8DC63F"/>'
 b+='<g id="rack-devices">'+devices+'</g>'
 b+='<g id="space-label">'+txt(225,570,'Space remains',24,fill=B)+'</g>'
 for i,(label,color) in enumerate([('Space used',G),('Power used',B),('Cooling used',H)]):
  y=135+i*130;b+=txt(480,y+18,label,27,anchor='start',weight=700)+f'<rect x="480" y="{y+40}" width="630" height="42" rx="6" fill="{L}"/><rect id="budget{i}" x="480" y="{y+40}" width="0" height="42" rx="6" fill="{color}"/><path d="M1110,{y+32}V{y+90}" stroke="#697482" stroke-width="3"/>'+txt(1110,y+114,'100%',20)+f'<text id="value{i}" x="1075" y="{y+18}" text-anchor="end" font-size="25" fill="{color}"></text>'
 b+=tag('traffic',480,545,630,'Network traffic also changes',fill='#F0F1FA',stroke=B)
 b+=box('candidate',65,595,310,60,'Next device: review',fill='#FFF0E9',stroke=H,size=21)
 b+='<text id="decision" x="795" y="645" text-anchor="middle" font-size="26" font-weight="700" fill="#BA6545"></text>'
 anchors={'adding':'Adding equipment','demand':'electrical demand heatremoval requirements and network traffic','rates':'at different rates','illustrative':'In this illustrative animation','limit':'the cooling allocation reaches its limit','space':'while mounting space remains available','qualification':'not a recommended rack design','decision':'identify the limiting budget','conclusion':'before deciding that another device can be installed'}
 # Align against the hyphenated spoken token with normalized matching.
 anchors['demand']='electrical demand heat-removal requirements and network traffic'
 logic='''const first=ramp(t,cue('demand'),end('demand')),second=ramp(t,cue('limit'),end('limit'));const values=[lerp(25,37.5,first)+12.5*second,lerp(30,55,first)+27*second,lerp(35,65,first)+35*second];for(let i=0;i<3;i++){width('budget'+i,630*values[i]/100);text('value'+i,Math.round(values[i])+'%')}for(let i=2;i<4;i++){const f=i===2?first:second;el('device'+i).setAttribute('transform','translate(0,'+((1-f)*(550-(125+i*46)))+')');opacity('device'+i,t>=(i===2?cue('adding'):cue('illustrative'))?1:0)}show('space-label',t>=cue('space'));opacity('traffic',t>=cue('demand')?1:.15);show('candidate',t>=cue('decision'));text('decision',t>=end('limit')?'Cooling allocation full · review before adding':'');for(let i=4;i<8;i++)el('slot'+i).setAttribute('stroke',t>=cue('space')?'#8DC63F':'#CAD2DC');document.body.dataset.state=t<cue('adding')?'baseline':t<cue('limit')?'first-addition':t<end('limit')?'second-addition':t<cue('decision')?'cooling-limit':'capacity-review';'''
 return source(3,9,'rack-budgets',b,anchors,logic,['Cooling allocation full · review before adding','25%','38%','50%','30%','55%','82%','35%','65%','100%'], 'decision')

def virtual():
 b=txt(330,48,'Virtual-machine example',26,weight=700)+txt(925,48,'Alternative: containers',25,weight=700)
 b+='<g id="vm-example"><rect x="55" y="75" width="550" height="245" rx="18" fill="#F8FAF7" stroke="#AEBDA1" stroke-width="2"/>'
 for i,label in enumerate(['Guest VM A','Guest VM B']):b+=box('vm'+str(i),80+i*265,90,235,125,'' if i==0 else label,size=25)+(txt(197.5,126,'Guest VM A',24) if i==0 else '')
 b+=box('hypervisor',80,235,500,68,'Hypervisor mediates access',fill='#F0F1FA',stroke=B,size=25)+'</g>'
 b+='<g id="containers"><rect x="650" y="75" width="500" height="245" rx="18" fill="#F8FAFB" stroke="#BCC8D2" stroke-width="2"/>'
 for i in range(2):b+=box('container'+str(i),675+i*235,100,210,105,'Container '+('A' if i==0 else 'B'),fill='#EAF2FF',stroke=C,size=24)
 b+=box('kernel',675,235,445,68,'Shared host kernel',fill='#EAF2FF',stroke=C,size=24)+arrow('container-a-access',780,205,780,235,C)+arrow('container-b-access',1015,205,1015,235,C)+'</g>'
 b+=arrow('vm-work',197.5,215,197.5,235,B)+arrow('host-access',330,303,330,375,B)+arrow('vm-b-work',462.5,215,462.5,235,B)
 b+='<rect x="80" y="375" width="1040" height="120" rx="18" fill="#F3F6FA" stroke="#8391A5" stroke-width="2"/>'+txt(600,350,'Physical host · finite resources',26,weight=700)
 for i,label in enumerate(['Processors','Memory','Storage','Networks']):
  x=110+i*255;b+=txt(x,430,label,23,anchor='start')+f'<rect x="{x}" y="455" width="210" height="20" rx="5" fill="{L}"/><rect id="resource{i}" x="{x}" y="455" width="40" height="20" rx="5" fill="{B}"/>'
 b+=box('power',80,520,445,90,'',fill='#F0F1FA',stroke=B,size=25)+box('heat',675,520,445,90,'',fill='#FFF0E9',stroke=H,size=25)+txt(302.5,565,'Electrical power demand',25)+txt(897.5,565,'Heat-removal demand',25)
 b+=arrow('power-route',300,520,300,495,B)+arrow('heat-route',900,495,900,520,H)
 b+='<rect x="135" y="583" width="335" height="15" rx="4" fill="#DFE3EC"/><rect id="power-demand" x="135" y="583" width="100" height="15" rx="4" fill="#343895"/><rect x="730" y="583" width="335" height="15" rx="4" fill="#F1E2DC"/><rect id="heat-demand" x="730" y="583" width="100" height="15" rx="4" fill="#BA6545"/>'
 b+='<g id="workload">'+txt(197.5,159,'Application work',21)+''.join(f'<rect id="work{i}" x="{105+i*34}" y="180" width="24" height="12" rx="3" fill="#343895"/>' for i in range(5))+'</g>'
 b+='<circle id="work-dot" cx="330" cy="212" r="9" fill="#343895"/><path id="work-path" d="M330,303V375" fill="none" stroke="none"/>'
 b+='<text id="activity" x="600" y="650" text-anchor="middle" fill="#243244" font-size="23"></text>'
 anchors={'logical':'logical computing environments on physical resources','hypervisor':'a hypervisor manages the guest systems and their access','containers':'Containers provide another arrangement','kernel':'they share the kernel','trace':'The animation traces a virtual machines physical dependency','activity':'More activity in an application','processors':'processors memory storage and networks','consequences':'consequences for electricity and heat','conclusion':'it doesnt remove their physical limits'}
 logic='''const comparison=t>=cue('containers')&&t<cue('trace');opacity('containers',t>=cue('containers')?(comparison?1:.40):.08);opacity('vm-example',comparison?.35:1);opacity('vm-work',comparison?.3:1);opacity('vm-b-work',comparison?.3:1);opacity('host-access',comparison?.3:1);opacity('workload',comparison?.3:1);tone('hypervisor',t>=cue('hypervisor')&&!comparison);tone('kernel',comparison);const work=ramp(t,cue('activity'),end('activity')+.4),demand=ramp(t,cue('processors'),end('processors')),facility=ramp(t,cue('consequences'),end('consequences'));for(let i=0;i<5;i++)opacity('work'+i,i<2||work>(i-2)/3?1:.1);for(let i=0;i<4;i++)width('resource'+i,[42,53,31,38][i]+[102,72,57,83][i]*demand);tone('power',facility>.5);tone('heat',facility>.5);width('power-demand',100+155*facility);width('heat-demand',100+155*facility);for(const id of ['power-route','heat-route'])el(id).querySelector('path').setAttribute('stroke-width',4+4*facility);const med=ramp(t,cue('hypervisor'),end('hypervisor'));dot('work-dot','work-path',med,t>=cue('hypervisor')&&t<end('hypervisor'));text('activity',t<cue('activity')?'Logical separation keeps a shared physical dependency':t<cue('consequences')?'Application activity creates demand on distinct host resources':'Illustrative demand · physical limits remain');document.body.dataset.state=comparison?'container-comparison':t<cue('hypervisor')?'logical-guests':t<cue('activity')?'hypervisor-to-host':t<cue('consequences')?'higher-application-demand':'power-and-heat-demand';'''
 return source(4,7,'virtual-physical',b,anchors,logic,['Logical separation keeps a shared physical dependency','Application activity creates demand on distinct host resources','Illustrative demand · physical limits remain'], 'conclusion')

if __name__=='__main__':
 records=[service(),power(),containment(),budgets(),virtual()]
 (Q/'source-build-records.json').write_text(json.dumps(records,indent=2)+'\n');print('Built five final-WAV-aligned deterministic sources.')

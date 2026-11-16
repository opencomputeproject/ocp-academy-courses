"""Editable deterministic teaching sources. Timing remains provisional until narration is measured."""
from pathlib import Path
import json
out=Path(__file__).resolve().parent
C={'ink':'#253544','green':'#6b9e27','indigo':'#343895','gray':'#687781'}
def txt(x,y,s,size=34,fill='#253544',weight=400):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{s}</text>'
def card(id,x,y,w,h,title,lines,color='#343895'):
 return f'<g id="{id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#f5f7f8"/><rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{color}"/>'+txt(x+35,y+53,title,36,color,700)+''.join(txt(x+35,y+105+i*43,t,31) for i,t in enumerate(lines))+'</g>'
def write(stem,svg,logic,scenes):
 cp=out/(stem+'.timeline.json')
 if not cp.exists():raise FileNotFoundError(f'Missing authoritative narration timeline: {cp.name}')
 config=json.loads(cp.read_text());duration=config['duration_ms'];timing=config.get('timing_fractions',{})
 html='''<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:white}svg{display:block;font-family:Arial,Helvetica,sans-serif}text{font-kerning:normal}</style></head>'''+f'<body data-duration-ms="{duration}" data-poster-ms="{int(duration*.95)}"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="1080" fill="white"/>'+svg+'</svg><script>const D='+str(duration)+';const T='+json.dumps(timing)+''';const clamp=x=>Math.max(0,Math.min(1,x));const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};const el=id=>document.getElementById(id);const show=(id,p,start)=>el(id).style.opacity=smooth((p-start)/(600/D));window.setTeachingTime=function(ms){const p=clamp(ms/D);'''+logic+'''};setTeachingTime(0);</script></body></html>'''
 (out/(stem+'.html')).write_text(html)
svg='''<rect x="115" y="130" width="680" height="740" fill="none" stroke="#b8c3c9" stroke-width="3" stroke-dasharray="12 12"/>
<rect id="board" x="115" y="130" width="680" height="740" fill="#f5f7f8" stroke="#687781" stroke-width="4"/>
<g id="floating"><text x="812" y="175" font-size="27" fill="#687781">Far edge</text><rect x="140" y="155" width="230" height="125" rx="8" fill="#e4efcf" stroke="#6b9e27" stroke-width="3"/><rect x="430" y="155" width="340" height="125" rx="8" fill="#e4efcf" stroke="#6b9e27" stroke-width="3"/>'''+txt(160,205,'Control panel',29)+txt(160,247,'zone',29)+txt(452,205,'Far-edge power',29)+txt(452,247,'zone',29)+'''</g>
<g id="fixed"><rect x="592" y="572" width="48" height="182" rx="5" fill="#e4e5f5" stroke="#343895" stroke-width="4"/><rect x="670" y="572" width="48" height="182" rx="5" fill="#e4e5f5" stroke="#343895" stroke-width="4"/><circle cx="628" cy="803" r="12" fill="white" stroke="#343895" stroke-width="4"/>'''+txt(355,645,'Fixed riser',30,'#343895')+txt(355,685,'positions',30,'#343895')+txt(420,815,'Retention',29,'#343895')+'''</g>
<g id="datum"><path d="M160 803H220 M190 773V833" stroke="#343895" stroke-width="4"/><circle cx="190" cy="803" r="12" fill="white" stroke="#343895" stroke-width="4"/>'''+txt(140,927,'Common datum stays fixed',34,'#343895',700)+'''</g>'''
svg+=card('fixedCard',960,130,820,205,'Fixed → common datum',['Fixed positions do not move.','Some can become inapplicable on a smaller HPM.'])
svg+=card('floatCard',960,375,820,205,'Floating → board edge',['Zones follow the moving edge.','Floating features do not drop off.'],'#6b9e27')
svg+=card('checkCard',960,620,820,205,'A shorter outline is not the whole review',['Check mounting, cables and keep-out zones.','Reassess the proposed chassis integration.'])
svg+=txt(638,840,'Near edge',27,'#687781')
svg+=txt(115,1010,'Conceptual scaling example · not a dimensional model',28,'#687781')
logic="show('datum',p,T.datum??0);show('fixed',p,T.fixed??.16);show('fixedCard',p,T.fixed??.16);show('floatCard',p,T.floating??.44);show('checkCard',p,T.check??.72);const dy=140*smooth((p-(T.shorten??.20))/(T.shorten_duration??.12));el('board').setAttribute('y',130+dy);el('board').setAttribute('height',740-dy);el('floating').setAttribute('transform',`translate(0 ${dy})`);"
write('video_m1s6_fixed_floating',svg,logic,[{'fraction':0,'event':'outline'},{'fraction':0,'event':'datum and near/far'},{'fraction':.16,'event':'fixed features'},{'fraction':.20,'event':'shorten outline; fixed positions stay'},{'fraction':.44,'event':'floating zones explained'},{'fraction':.72,'event':'integration implications'}])
svg='<image href="cad_class_l_top.svg" x="120" y="115" width="590" height="730"/>'+txt(120,915,'L365 · supplied STEP geometry',33,'#343895',700)+txt(120,965,'Board and connectors only · no chassis',29,'#687781')
svg+='''<g id="datumMark"><circle cx="164" cy="785" r="24" fill="none" stroke="#6b9e27" stroke-width="5"/><path d="M130 785H198 M164 751V819" stroke="#6b9e27" stroke-width="3"/></g><g id="outlineMark"><rect x="120" y="115" width="590" height="730" fill="none" stroke="#6b9e27" stroke-width="5"/></g><g id="retentionMark"><circle cx="418.2" cy="781" r="23" fill="none" stroke="#6b9e27" stroke-width="5"/></g>'''
svg+=card('datumCard',850,65,950,160,'1  Establish the common datum',['Model axes are not automatically the board datum.'])
svg+=card('outlineCard',850,255,950,160,'2  Inspect mounting and retention',['Verify published hole, pad and keep-out requirements.'])
svg+=card('retainCard',850,445,950,160,'3  Check the handle-hole interface',['Required interface; a fitted handle is not mandatory.'])
svg+=card('negativeCard',850,635,950,160,'4  Review any negative board features',['Notches must preserve required interfaces.'])
svg+=card('limitCard',850,825,950,160,'5  Flag conflicting source evidence',['A model does not resolve the Class L hole-count conflict.'],'#6b9e27')
logic="show('datumMark',p,T.datum??.19);show('datumCard',p,0);show('outlineMark',p,T.outline??.27);show('outlineCard',p,T.outline??.27);show('retentionMark',p,T.retention??.32);show('retainCard',p,T.handle??.44);show('negativeCard',p,T.negative??.64);show('limitCard',p,T.conflict??.82);"
write('video_m2s3_datum_interfaces',svg,logic,[{'fraction':0,'event':'supplied L365 model'},{'fraction':0,'event':'datum versus model axes'},{'fraction':.19,'event':'datum highlight'},{'fraction':.27,'event':'mounting and retention'},{'fraction':.44,'event':'handle interface'},{'fraction':.64,'event':'negative board features'},{'fraction':.82,'event':'Class L source conflict'}])
svg=txt(100,100,'Check',34,'#343895',700)+txt(590,100,'Evidence in the review pack',34,'#343895',700)+txt(1370,100,'Disposition',34,'#343895',700)
rows=[
 ('architecture',150,['Shared chassis approach'],['Datum overlay and tray example','do not establish complete integration.'],['Insufficient evidence','for the complete system'],'#687781'),
 ('height',310,['Riser height zone'],['Riser implemented; 6 mm zone.','12 mm component; no applicable exception.'],['Does not conform','for this check'],'#a84c32'),
 ('connector',470,['Far-power connector'],['Only 2 × 3 bodies supplied.','At least one 2 × 6 body required.'],['Does not conform','for this check'],'#a84c32'),
 ('power',630,['Delivered riser power'],['75 W supplied.','87 W minimum per implemented fixed riser.'],['Does not conform','for this check'],'#a84c32'),
 ('conflict',790,['Class L hole-count claim'],['Compliance table and body disagree.','A matching model cannot resolve the text.'],['Clarification required','Conflicting evidence'],'#687781')]
for id,y,claim,evidence,result,color in rows:
 svg+=f'<g id="row_{id}"><rect x="70" y="{y}" width="1780" height="135" rx="14" fill="#f5f7f8"/>'+''.join(txt(100,y+58+i*40,t,31,'#253544',700) for i,t in enumerate(claim))
 svg+=f'<g id="evidence_{id}">'+''.join(txt(590,y+50+i*42,t,30) for i,t in enumerate(evidence))+'</g>'
 svg+=f'<g id="result_{id}"><rect x="1340" y="{y}" width="510" height="135" rx="14" fill="{color}"/>'+''.join(txt(1370,y+50+i*42,t,30,'white',700 if i==0 else 400) for i,t in enumerate(result))+'</g></g>'
svg+='<g id="scope">'+txt(100,1000,'Constructed examples · each finding applies to the stated check',30,'#687781')+'</g>'
logic="".join(f"show('row_{id}',p,T.{id}??{start});show('evidence_{id}',p,T.{id}_evidence??{start+.025});show('result_{id}',p,T.{id}_result??{start+.075});" for id,start in [('architecture',0),('height',.25),('connector',.44),('power',.55),('conflict',.71)])+"show('scope',p,T.scope??.85);"
write('video_m3s6_evidence_debrief',svg,logic,[{'fraction':0,'event':'architecture evidence gap'},{'fraction':.25,'event':'height mismatch'},{'fraction':.44,'event':'connector mismatch'},{'fraction':.55,'event':'delivered-power shortfall'},{'fraction':.71,'event':'source conflict'},{'fraction':.85,'event':'bounded findings'}])

"""Build approved static figures and final-WAV-aligned causal videos.
Requires Scribe word timestamps in qa/approved-content-build/alignment.
Existing five videos and their editable sources are left intact.
"""
from pathlib import Path
import json,sys,hashlib,xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).parent));import build_synced_media as core
from build_synced_media import txt,box,arrow,elbow,tag,G,B,C,H,I
P=Path(__file__).resolve().parents[1];Q=P/'authoring/qa/approved-content-build';core.Q=Q

def static(name,body):
 out=P/name;out.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675"><style>text{font-family:Arial,sans-serif}</style><rect width="1200" height="675" fill="white"/>'+body+'</svg>')

def statics():
 body=box('training',55,45,510,115,'Training: adjust a model using data',size=25)+box('inference',635,45,510,115,'Inference: use a trained model',size=25)
 body+=txt(600,215,'Coordinate the complete system around AI workloads',28,weight=700)
 for i,(label,col) in enumerate([('Accelerators & memory',G),('Storage & data movement',B),('Networks & software',C)]):body+=box('system'+str(i),55+i*375,265,340,115,label,stroke=col,size=23)
 body+=box('facility',55,445,1090,90,'Electrical power · heat removal · operating capacity',fill='#F0F1FA',stroke=B,size=27)
 for i in range(3):body+=arrow('support'+str(i),225+i*375,445,225+i*375,380,B)
 body+=txt(600,600,'Purpose and design can overlap enterprise, colocation and hyperscale',25)
 static('figures/module1/ai-factory-system.svg',body)
 body=''
 for k,(title,side) in enumerate([('Cold-aisle containment','supply'),('Hot-aisle containment','exhaust')]):
  x=15+k*600;body+=txt(x+265,65,title,28,weight=700)
  # Same left-to-right flow; only enclosed side changes.
  body+=box('supply'+str(k),x+25,190,150,160,'Cool\nsupply',fill='#EAF2FF',stroke=C,size=26)+box('rack'+str(k),x+235,190,120,160,'IT\nrow',size=27)+box('exhaust'+str(k),x+415,190,150,160,'Warm\nexhaust',fill='#FFF0E9',stroke=H,size=26)
  body+=arrow('in'+str(k),x+175,270,x+235,270,C)+arrow('out'+str(k),x+355,270,x+415,270,H)
  bx=x+10 if side=='supply' else x+400
  body+=f'<path d="M{bx},150h180v240h-180Z" fill="none" stroke="#719E2F" stroke-width="6" stroke-linejoin="round" stroke-dasharray="12 7"/>'
  body+=txt(x+290,455,'Enclose the '+('cool supply side' if side=='supply' else 'warm exhaust side'),24)
 body+=txt(600,555,'Both reduce mixing between supply and exhaust',28,weight=700)+txt(600,610,'Choose for the room paths, equipment and operating access',24)
 # Keep the reviewed CRAC/CRAH supply/return treatment on every rebuild.
 from build_m2_room_cooling import containment_comparison
 containment_comparison()

def ai():
 b=txt(600,45,'Industrial inspection · illustrative service constraints',25,weight=700)
 b+=box('camera',55,205,240,150,'Inspection\ncamera',size=28)+box('local',420,205,340,150,'Local model\ninference',size=28)
 b+=arrow('request',295,245,420,245,B)+arrow('response',420,315,295,315,C)
 b+='<path id="image-path" d="M295,245H420" fill="none" stroke="none"/><path id="result-path" d="M420,315H295" fill="none" stroke="none"/><circle id="image" r="9" fill="#343895"/><circle id="result" r="9" fill="#3B7FA8"/>'
 b+=box('deadline',850,205,290,150,'Respond before\ninspection point',fill='#F0F1FA',stroke=B,size=24)
 b+=txt(195,410,'Production line keeps its response',24,anchor='start')
 b+=box('queue',95,490,350,100,'Separate nonurgent\nanalysis queue',fill='#F0F1FA',stroke=B,size=25)+box('regional',845,490,300,100,'Regional analysis\ncapacity',fill='#F0F1FA',stroke=B,size=25)
 b+=arrow('wan',445,540,845,540,C)+txt(645,490,'Wide-area connection',23)
 b+='<path id="batch-path" d="M445,540H845" fill="none" stroke="none"/><circle id="batch" r="11" fill="#343895"/>'
 b+='<g id="outage"><path d="M625,521L665,559M665,521L625,559" stroke="#BA6545" stroke-width="6"/></g>'
 b+='<text id="status" x="600" y="130" text-anchor="middle" font-size="28" font-weight="700" fill="#243244"></text>'
 b+='<text id="queue-status" x="600" y="640" text-anchor="middle" font-size="23" fill="#343895"></text>'
 anchors={'camera':'A camera sends an image','response':'The response must arrive before the item passes','remote':'A remote connection cannot be assumed','outage':'Now the wide-area connection becomes unavailable','local':'Local inference can continue','wait':'Separate nonurgent analysis can wait','return':'When connectivity returns','regional':'that work can use regional capacity','decision':'This is a placement decision','edge':'Edge describes proximity','aicc':'AI Computing Continuum project','constraints':'Choose placement through response needs'}
 logic="""const failed=t>=cue('outage')&&t<cue('return'),ready=t>=cue('return');tone('camera',t>=cue('camera'));tone('local',t>=cue('camera'));tone('deadline',t>=cue('response'));opacity('wan',failed?.15:1);show('outage',failed);tone('queue',t>=cue('wait')&&!ready);tone('regional',t>=cue('regional'));const second=t>=cue('local');dot('image','image-path',second?ramp(t,cue('local'),end('local')):ramp(t,cue('camera'),end('camera')),second?t>=cue('local')&&t<end('local'):t>=cue('camera')&&t<end('camera'));dot('result','result-path',second?ramp(t,end('local'),end('local')+1.2):ramp(t,cue('response'),end('response')),second?t>=end('local')&&t<end('local')+1.2:t>=cue('response')&&t<end('response'));dot('batch','batch-path',ramp(t,cue('regional'),end('regional')),t>=cue('regional')&&t<end('regional'));text('status',t>=cue('aicc')?'OCP AICC · regional, enterprise, telco and industrial':failed?'Connection unavailable · local inference remains feasible':ready?'Connection restored · schedule eligible nonurgent work':'Short response deadline · local model and resources available');text('queue-status',t>=cue('constraints')?'Response needs · connectivity · data constraints · site capacity':t<cue('wait')?'Illustrative choice · remote service is not assumed to meet the deadline':!ready?'Nonurgent work waits; the running local task does not migrate':'Regional work requires connectivity, suitable data rules and available capacity');document.body.dataset.state=t<cue('outage')?'local-response':failed?'wan-outage-local-service':t<cue('regional')?'connection-restored':t<cue('decision')?'separate-batch-transfer':'placement-constraints';"""
 return core.source(1,10,'ai-placement',b,anchors,logic,['Connection unavailable · local inference remains feasible','Connection restored · schedule eligible nonurgent work','Short response deadline · local model and resources available','Nonurgent work waits; the running local task does not migrate','Regional work requires connectivity, suitable data rules and available capacity','OCP AICC · regional, enterprise, telco and industrial','Response needs · connectivity · data constraints · site capacity'], 'constraints')

def liquid():
 b=txt(600,45,'Follow energy transfer · fluid loops remain distinct',26,weight=700)
 b+=box('chip',45,170,160,140,'Hot\ncomponent',fill='#FFF0E9',stroke=H,size=24)+box('plate',270,170,180,140,'Cold plate',size=26)+box('interface',555,170,220,140,'Heat-transfer\ninterface',fill='#F0F1FA',stroke=B,size=25)
 b+=arrow('chipheat',205,240,270,240,H)+arrow('warm',450,215,555,215,H)+arrow('cool',555,280,450,280,C)
 b+=txt(505,150,'Equipment loop',22)+txt(505,350,'Coolant returns',21,fill=C)
 b+='<path id="equipment-hot" d="M450,215H555" fill="none" stroke="none"/><circle id="heat-dot" r="9" fill="#BA6545"/><path id="equipment-cool" d="M555,280H450" fill="none" stroke="none"/><circle id="return-dot" r="9" fill="#3B7FA8"/>'
 b+='<g id="l2l">'+box('facility',875,170,280,140,'Separate facility\ncoolant loop',fill='#EAF2FF',stroke=C,size=25)+arrow('facilitywarm',775,215,875,215,H)+arrow('facilitycool',875,280,775,280,C)+txt(975,365,'Heat continues through\nfacility heat rejection',23)+arrow('reject',1135,310,1135,420,H)+box('environment',875,420,280,85,'Environment',fill='#FFF0E9',stroke=H,size=26)+'</g>'
 b+='<g id="l2a">'+box('room',875,170,280,140,'Room air',fill='#FFF0E9',stroke=H,size=27)+arrow('airheat',775,240,875,240,H)+txt(975,365,'Room cooling must\nremove the added heat',23)+arrow('airreject',1135,310,1135,420,H)+box('airenv',875,420,280,85,'Environment',fill='#FFF0E9',stroke=H,size=26)+'</g>'
 b+='<text id="mode" x="600" y="105" text-anchor="middle" font-size="26" fill="#343895"></text>'
 b+='<text id="conclusion" x="600" y="590" text-anchor="middle" font-size="25" font-weight="700" fill="#243244"></text>'
 anchors={'component':'Follow the heat from a component','plate':'A cold plate transfers it','equipment':'The warmed coolant carries that heat','l2l':'In this liquid-to-liquid example','separate':'The two fluids remain separate','return':'The cooled equipment coolant returns','rejection':'while the facility system carries the heat onward','alternative':'An alternative liquid-to-air arrangement','room':'the room cooling system must still remove','distinct':'The alternatives are not simultaneous steps','cdu':'A coolant distribution unit','confirm':'Confirm equipment compatibility'}
 logic="""const air=t>=cue('alternative');show('l2l',!air);show('l2a',air);tone('chip',t>=cue('component'));tone('plate',t>=cue('plate'));tone('interface',t>=cue('equipment'));opacity('chipheat',t>=cue('plate')?1:.1);opacity('warm',t>=cue('equipment')?1:.1);opacity('cool',t>=cue('return')?1:.1);dot('heat-dot','equipment-hot',ramp(t,cue('equipment'),end('equipment')),t>=cue('equipment')&&t<end('equipment'));dot('return-dot','equipment-cool',ramp(t,cue('return'),end('return')),t>=cue('return')&&t<end('return'));opacity('facilitywarm',t>=cue('l2l')?1:.1);opacity('facilitycool',t>=cue('return')?1:.1);opacity('reject',t>=cue('rejection')?1:.1);opacity('airreject',t>=cue('room')?1:.1);text('mode',air?'Alternative: liquid-to-air heat transfer':'Example: liquid-to-liquid · separate fluid circuits');text('conclusion',t<cue('separate')?'Heat moves into coolant; it is not eliminated':t<cue('alternative')?'Heat crosses the exchanger; the two fluids do not mix':t<cue('confirm')?'Room cooling capacity remains part of the heat path':'Check compatibility, liquid and air capacity, and the full rejection path');document.body.dataset.state=t<cue('plate')?'component':t<cue('equipment')?'cold-plate':t<cue('l2l')?'equipment-loop':t<cue('return')?'separate-loops':t<cue('alternative')?'facility-heat-rejection':t<cue('confirm')?'liquid-to-air-alternative':'complete-path';"""
 return core.source(2,14,'liquid-heat-path',b,anchors,logic,['Alternative: liquid-to-air heat transfer','Example: liquid-to-liquid · separate fluid circuits','Heat crosses the exchanger; the two fluids do not mix','Check compatibility, liquid and air capacity, and the full rejection path'], 'confirm')

def pue():
 b=txt(600,45,'Illustrative consolidation · same useful work and service',26,weight=700)
 b+=txt(100,140,'Energy during a comparable period',26,anchor='start')
 b+=txt(100,255,'Before',28,anchor='start',weight=700)+txt(100,445,'After',28,anchor='start',weight=700)
 for row,y in enumerate([190,380]):
  b+=f'<rect x="265" y="{y}" width="700" height="90" rx="6" fill="white"/><rect id="it{row}" x="265" y="{y}" width="0" height="90" fill="{G}"/><rect id="over{row}" x="265" y="{y}" width="0" height="90" fill="{B}"/>'
  b+=f'<text id="it-label{row}" x="500" y="{y+55}" text-anchor="middle" font-size="27" fill="#243244"></text><text id="over-label{row}" x="900" y="{y+55}" text-anchor="middle" font-size="23" fill="white"></text><text id="total{row}" x="265" y="{y+135}" font-size="26" fill="#243244"></text><text id="ratio{row}" x="1140" y="{y+60}" text-anchor="end" font-size="30" font-weight="700" fill="#343895"></text>'
 b+=txt(265,550,'IT energy',24,anchor='start',fill='#496B20')+txt(540,550,'Facility overhead',24,anchor='start',fill=B)
 b+='<text id="outcome" x="600" y="620" text-anchor="middle" font-size="27" font-weight="700" fill="#243244"></text>'
 anchors={'context':'a controlled consolidation','before':'the starting system uses','overhead':'two hundred units of facility overhead','total':'Total energy is twelve hundred units','ratio':'one point two zero','after':'After consolidation','it':'IT energy falls to eight hundred units','fixed':'while overhead remains two hundred','newtotal':'Total energy is now one thousand units','newratio':'one point two five','denominator':'The denominator fell','saving':'does not erase the energy saving','evaluate':'Evaluate useful work'}
 logic="""const before=ramp(t,cue('before'),end('before')),over=ramp(t,cue('overhead'),end('overhead')),after=ramp(t,cue('it'),end('it'));width('it0',583.333*before);width('over0',116.667*over);el('over0').setAttribute('x',848.333);text('it-label0',t>=end('before')?'IT 1,000':'');text('over-label0',t>=end('overhead')?'200':'');text('total0',t>=cue('total')?'Total energy: 1,200 units':'');text('ratio0',t>=cue('ratio')?'PUE 1.20':'');width('it1',466.667*after);width('over1',t>=cue('fixed')?116.667:0);el('over1').setAttribute('x',731.667);el('it-label1').setAttribute('x',498);el('over-label1').setAttribute('x',790);text('it-label1',t>=end('it')?'IT 800':'');text('over-label1',t>=cue('fixed')?'200':'');text('total1',t>=cue('newtotal')?'Total energy: 1,000 units':'');text('ratio1',t>=cue('newratio')?'PUE 1.25':'');text('outcome',t<cue('after')?'Useful work and service requirements are held constant':t<cue('newratio')?'Consolidation reduces IT energy; overhead stays fixed':'Total energy falls by 200 units · PUE rises');document.body.dataset.state=t<cue('overhead')?'it-baseline':t<cue('ratio')?'overhead-baseline':t<cue('after')?'pue-baseline':t<cue('newratio')?'consolidation':'less-energy-higher-ratio';"""
 return core.source(4,11,'energy-ratio-change',b,anchors,logic,['IT 1,000','IT 800','200','Total energy: 1,200 units','Total energy: 1,000 units','PUE 1.20','PUE 1.25','Total energy falls by 200 units · PUE rises'], 'evaluate')

if __name__=='__main__':
 statics()
 if '--static-only' not in sys.argv:
  records=[ai(),liquid(),pue()];(Q/'source-build-records.json').write_text(json.dumps(records,indent=2)+'\n');print('Built three final-WAV-aligned causal sources.')

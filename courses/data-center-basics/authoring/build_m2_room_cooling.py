"""Editable CRAC/CRAH figures and the final-WAV-timed room-air circuit.

Static figures: --static. Motion source: --animation after refreshing the
Scribe word map in qa/m2-room-cooling/alignment/m2-s11.json.
"""
from pathlib import Path
import json, sys
import build_synced_media as core
from build_synced_media import txt, box, arrow, elbow, G, B, C, H, I
P = Path(__file__).resolve().parents[1]
Q = P / 'authoring/qa/m2-room-cooling'

def svg(name, body, height):
    (P/'figures/module2'/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}"><style>text{{font-family:Arial,sans-serif}}</style><rect width="1200" height="{height}" fill="white"/>'+body+'</svg>')

def heat_paths():
    b = ''
    for n, (name, expansion, coil, next_step, transport) in enumerate([
        ('CRAC', 'Computer room air conditioner', 'Fan + refrigerant coil', 'Compressor-driven circuit\n+ heat rejection', 'Heat carried by refrigerant'),
        ('CRAH', 'Computer room air handler', 'Fan + chilled-water coil', 'Facility cooling plant\n+ heat rejection', 'Heat carried by water'),
    ]):
        y = 100 + n*195
        b += txt(30,y-38,f'{name} · {expansion}',29,anchor='start',weight=700)
        b += box('it'+str(n),30,y,160,100,'Warm IT\nexhaust',fill='#FFF0E9',stroke=H,size=25)
        b += box('coil'+str(n),255,y,320,100,coil,fill='#EAF2FF',stroke=C,size=24)
        b += box('plant'+str(n),640,y,330,100,next_step,fill='#F1F5ED',stroke=G,size=25)
        b += box('outside'+str(n),1035,y,135,100,'Outdoors',fill='#F0F1FA',stroke=B,size=23)
        for k,x1,x2 in [('air',190,255),('fluid',575,640),('reject',970,1035)]:
            b += arrow(k+str(n),x1,y+50,x2,y+50,H)
        b += txt(805,y+138,transport,23,fill=H)
    b += txt(600,475,'Both return cooled room air to equipment inlets.',27,weight=700)
    svg('heat-path.svg',b,505)

def containment_comparison():
    b = ''
    for n, heading in enumerate(['Cold-aisle containment','Hot-aisle containment']):
        x=n*600
        b+=txt(x+300,50,heading,28,weight=700)
        b+=box('supply'+str(n),x+40,110,150,150,'Cool\nsupply',fill='#EAF2FF',stroke=C,size=26)
        b+=box('rack'+str(n),x+250,110,120,150,'IT\nrow',size=27)
        b+=box('exhaust'+str(n),x+430,110,150,150,'Warm\nreturn',fill='#FFF0E9',stroke=H,size=26)
        b+=arrow('in'+str(n),x+190,185,x+250,185,C)+arrow('out'+str(n),x+370,185,x+430,185,H)
        bx=x+(25 if n==0 else 415)
        b+=f'<path d="M{bx},85h180v200h-180Z" fill="none" stroke="#719E2F" stroke-width="6" stroke-linejoin="round" stroke-dasharray="12 7"/>'
        b+=txt(x+300,325,'Enclose the '+('cool supply side' if n==0 else 'warm exhaust side'),24)
    b+=box('unit',310,375,580,110,'CRAC or CRAH\nCoil removes heat · fan circulates air',fill='#F0F1FA',stroke=B,size=25)
    b+=txt(150,404,'Warm return',23,fill=H)+arrow('to-coil',45,435,310,435,H)
    b+=txt(1045,404,'Cooled supply',23,fill=C)+arrow('from-coil',890,435,1155,435,C)
    b+=txt(600,522,'Either containment approach can work with either room-unit type.',25,weight=700)
    b+=txt(600,566,'Select for room paths, equipment orientation and operating access.',23)
    svg('containment-comparison.svg',b,600)

def animation():
    core.Q=Q
    b=box('unit',35,220,240,230,'',fill='#F0F1FA',stroke=B,size=25)
    b+=txt(155,252,'CRAC or CRAH',25,weight=700)
    b+='<g id="coil"><rect x="70" y="280" width="170" height="75" rx="6" fill="#EAF2FF" stroke="#3B7FA8" stroke-width="2"/>'
    b+=txt(155,325,'Cooling coil',24)+'</g>'+txt(155,414,'Fan circulates air',21)
    b+=box('equipment',485,245,210,170,'Equipment\nrow',size=28)
    b+=box('return',905,270,245,110,'Warm return',fill='#FFF0E9',stroke=H,size=27)
    b+=txt(370,293,'Cool supply',25,fill=C)
    b+=arrow('supply-route',275,330,485,330,C)+arrow('exhaust-route',695,330,905,330,H)
    b+=elbow('return-route','M1027.5,380V495H155V463','148,463 155,450 162,463',H)
    b+='<path id="supply-path" d="M275,330H485" fill="none" stroke="none"/><path id="exhaust-path" d="M695,330H905" fill="none" stroke="none"/><path id="return-path" d="M1027.5,380V495H155V450" fill="none" stroke="none"/>'
    b+='<path id="recirc-path" d="M1027.5,270V190H455V330H472" fill="none" stroke="#BA6545" stroke-width="4" stroke-dasharray="10 8"/><polygon id="recirc-head" class="arrowhead" points="472,323 485,330 472,337" fill="#BA6545"/>'
    # Leave the return connection open through the containment boundary.
    b+='<path id="barrier" d="M720,275V205H1170V520H720 M720,395V472" fill="none" stroke="#719E2F" stroke-width="8" stroke-linejoin="round"/>'
    b+='<g id="barrier-title">'+txt(945,247,'Contained return side',22,fill='#496B20')+'</g>'
    b+=box('heat-out',360,95,795,70,'',fill='#FFF0E9',stroke=H,size=24)
    b+=txt(757.5,140,'Heat → connected system → outdoors',27)
    b+=elbow('coil-heat','M155,220V130H347','347,123 360,130 347,137',H)
    b+='<g id="heat-types">'+txt(345,562,'CRAC → refrigerant',27,fill=H,weight=700)+txt(855,562,'CRAH → chilled water',27,fill=C,weight=700)+'</g>'
    b+='<text id="state-label" x="600" y="48" text-anchor="middle" fill="#243244" font-size="28" font-weight="700"></text>'
    b+='<text id="inlet-label" x="600" y="616" text-anchor="middle" fill="#243244" font-size="25"></text>'
    b+='<g id="conditions">'+txt(600,654,'Verify IT inlets · airflow · cooling capacity · controls',23)+'</g>'
    for name,color in [('cool-dot',C),('exhaust-dot',H),('return-dot',H),('warm-dot',H)]: b+=f'<circle id="{name}" r="11" fill="{color}"/>'
    anchors={
        'orientation':'Follow the room air circuit',
        'supply':'sends cooled supply air to the equipment',
        'absorb':'air absorbs heat as it passes through the equipment',
        'return':'warm return air travels back to the unit',
        'coil':'At the coil heat leaves the air',
        'crac':'unit transfers it into refrigerant',
        'crah':'unit transfers it into chilled water',
        'outdoors':'connected system carries the heat onward for rejection outdoors',
        'resupply':'cooled air returns to the supply side',
        'mixing':'Now compare a mixing path',
        'recirc':'warm exhaust can recirculate toward equipment inlets',
        'containment':'Containment separates that exhaust from the supply stream',
        'guide':'guides it toward the cooling unit instead',
        'conditions':'A barrier creates no cooling capacity',
        'conclusion':'Verify equipment inlet conditions',
    }
    logic="""const compare=t>=cue('mixing'),install=ramp(t,cue('containment'),end('guide'));opacity('recirc-path',compare?1-install:0);opacity('recirc-head',compare?1-install:0);const wall=el('barrier'),length=wall.getTotalLength();wall.setAttribute('stroke-dasharray',length);wall.setAttribute('stroke-dashoffset',length*(1-install));opacity('barrier',install>0?1:0);show('barrier-title',install>.6);opacity('return-route',compare&&install<.1?.25:1);dot('cool-dot','supply-path',ramp(t,cue('supply'),end('supply')),t>=cue('supply')&&t<end('supply')||t>=cue('resupply')&&t<end('resupply'));if(t>=cue('resupply'))dot('cool-dot','supply-path',ramp(t,cue('resupply'),end('resupply')),t<end('resupply'));dot('exhaust-dot','exhaust-path',ramp(t,cue('absorb'),end('absorb')),t>=cue('absorb')&&t<end('absorb'));dot('return-dot','return-path',ramp(t,cue('return'),end('return')),t>=cue('return')&&t<end('return'));if(t>=cue('guide'))dot('return-dot','return-path',ramp(t,cue('guide'),end('guide')),t<end('guide'));dot('warm-dot','recirc-path',ramp(t,cue('recirc'),end('recirc')),t>=cue('recirc')&&t<end('recirc'));tone('coil',t>=cue('coil'));opacity('coil-heat',t>=cue('coil')?1:.12);opacity('heat-out',t>=cue('outdoors')?1:.25);opacity('heat-types',t>=cue('crac')?1:.15);show('conditions',t>=cue('conditions'));text('state-label',!compare?'Room air circuit · heat leaves at the coil':install<.99?'Comparison · exhaust mixing and containment':'Contained return · cooled supply kept separate');text('inlet-label',!compare?'Room air recirculates; heat travels onward':install<.99?'Warm exhaust can recirculate toward IT inlets':'Containment guides return air to the cooling unit');document.body.dataset.state=t<cue('supply')?'orientation':t<cue('absorb')?'cooled-supply':t<cue('return')?'equipment-heat-pickup':t<cue('coil')?'return-to-unit':t<cue('resupply')?'coil-heat-transfer':t<cue('mixing')?'resupply':t<cue('containment')?'mixing-comparison':install<.99?'containment-comparison':t<cue('conditions')?'contained-return':'verify-inlets';"""
    record=core.source(2,11,'containment-flow',b,anchors,logic,[
        'Room air circuit · heat leaves at the coil',
        'Comparison · exhaust mixing and containment',
        'Contained return · cooled supply kept separate',
        'Room air recirculates; heat travels onward',
        'Warm exhaust can recirculate toward IT inlets',
        'Containment guides return air to the cooling unit',
    ],'conclusion')
    (Q/'source-build-records.json').write_text(json.dumps([record],indent=2)+'\n')
    return record

if __name__=='__main__':
    if '--static' in sys.argv: heat_paths(); containment_comparison()
    elif '--animation' in sys.argv: animation()
    else: raise SystemExit('Choose --static or --animation (requires final-WAV word map).')

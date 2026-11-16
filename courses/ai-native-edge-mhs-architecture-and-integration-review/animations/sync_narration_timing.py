"""Set scene clocks from retained ElevenLabs alignment and measured pacing receipts."""
from pathlib import Path
import json,argparse
out=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--authoring-root',type=Path,required=True,help='External directory containing v4-masters/ and narration-alignments/')
parser.add_argument('stems',nargs='+')
args=parser.parse_args()
root=args.authoring_root.resolve()
configs={
 'video_m1s6_fixed_floating':('slide_06_fixed_floating.wav',{'datum':None,'fixed':'Now shorten the board','shorten':'Now shorten the board','floating':'Floating features follow','check':'This is a conceptual view'}),
 'video_m2s3_datum_interfaces':('slide_03_datum_interfaces.wav',{'datum':'Locate the near-side datum','outline':'Then inspect the mounting','retention':'the chassis-retention interface','handle':'The handle-hole interface is required','negative':'The source also permits','conflict':'For Class L'}),
 'video_m3s6_evidence_debrief':('slide_06_evidence_debrief.wav',{'architecture':None,'architecture_evidence':'The datum overlay','architecture_result':'The complete integration','height':'Now take the explicit','height_evidence':'In the constructed second case','height_result':'The disposition is','connector':'The far zone contains','connector_evidence':'The far zone contains','connector_result':'so that observation demonstrates','power':'The riser budget supplies','power_evidence':'The riser budget supplies','power_result':'That is a separate shortfall','conflict':'Finish with the disputed','conflict_evidence':'The Class L hole count','conflict_result':'The appropriate disposition','scope':'Each conclusion has a scope'})}
for stem in args.stems:
 basename,phrases=configs[stem];matches=[]
 for p in (root/'v4-masters').glob('*/receipt.json'):
  r=json.loads(p.read_text())
  if Path(r.get('output','')).name==basename:matches.append((p,r))
 if len(matches)!=1:raise RuntimeError(f'{stem}: expected unique receipt, got {len(matches)}')
 rp,r=matches[0];ap=root/'narration-alignments'/(r['text_sha256']+'.json');a=json.loads(ap.read_text())['alignment'];text=''.join(a['characters']);D=r['final_seconds'];tempo=r['tempo_factor'];events={}
 for key,phrase in phrases.items():
  if phrase is None:events[key]=0;continue
  index=text.find(phrase)
  if index<0:raise RuntimeError(f'{stem}: missing phrase {phrase}')
  events[key]=a['character_start_times_seconds'][index]/tempo
 if stem.endswith('fixed_floating'):
  events['fixed']=max(0,events['fixed']-.5);events['shorten']+=.4;events['shorten_duration']=3.5
 timing={k:sec/D for k,sec in events.items()}
 data={'duration_ms':D*1000,'timing_status':'FINAL_MEASURED_NARRATION','narration_master':str(Path('audio')/('module'+stem.split('_m')[1][0])/basename),'narration_sha256':r['output_sha256'],'receipt':'external-authoring/'+str(rp.relative_to(root)),'alignment':'external-authoring/'+str(ap.relative_to(root)),'tempo_factor':tempo,'timing_fractions':timing,'scene_seconds':events,'ending':'single pass; final state holds','encoding_fps':30}
 (out/(stem+'.timeline.json')).write_text(json.dumps(data,indent=2)+'\n');print(stem,D,events)

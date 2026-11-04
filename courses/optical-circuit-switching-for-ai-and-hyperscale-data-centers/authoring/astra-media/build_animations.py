from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
a=ROOT/'authoring/astra-media'; scenes=json.loads((a/'scene-scripts.json').read_text())
timing_path=a/'timing-manifest.json'
if timing_path.exists():timings=json.loads(timing_path.read_text())
else:timings={x['id']:{'duration_ms':x['provisional_duration_seconds']*1000,'scene_starts_ms':[round(x['provisional_duration_seconds']*1000*s['start_fraction']) for s in x['scenes']],'poster_ms':round(x['provisional_duration_seconds']*950),'status':'provisional; replace with measured narration and phrase cues'} for x in scenes};timing_path.write_text(json.dumps(timings,indent=2)+'\n')
for x in scenes:
 cfg={'id':x['id'],'module':x['module'],**timings[x['id']]}
 (ROOT/x['animation_source']).write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#fff}svg{display:block;width:100%;height:100%}text{font-family:Arial,Helvetica,sans-serif}*{box-sizing:border-box}</style></head><body data-duration-ms="'''+str(cfg['duration_ms'])+'" data-poster-ms="'+str(cfg['poster_ms'])+'"><svg id="canvas" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" role="img" aria-label="'+x['alt'].replace('"','&quot;')+'"></svg><script>window.MEDIA_CONFIG='+json.dumps(cfg)+'</script><script src="animation-engine.js"></script></body></html>\n')
print('Built five deterministic sources from timing manifest')

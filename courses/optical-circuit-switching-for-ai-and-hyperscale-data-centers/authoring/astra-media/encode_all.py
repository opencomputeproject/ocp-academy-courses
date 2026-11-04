from pathlib import Path
import json,subprocess,os,concurrent.futures,time
ROOT=Path(__file__).resolve().parents[2]; A=ROOT/'authoring/astra-media'; xs=json.loads((A/'scene-scripts.json').read_text());times=json.loads((A/'timing-manifest.json').read_text());env=os.environ.copy();rec=str(A/'record_animation_709.mjs')
def run(x):
 t=times[x['id']];cmd=['node',rec,str(ROOT/x['animation_source']),str(ROOT/x['video']),str(ROOT/x['poster']),str(t['duration_ms']),str(t['poster_ms']),'30'];start=time.time();p=subprocess.run(cmd,env=env,capture_output=True,text=True);(A/(x['id']+'-encode.log')).write_text(p.stdout+p.stderr);print(x['id'],p.returncode,round(time.time()-start,1),'seconds',p.stdout[-300:],flush=True);return p.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,xs))
raise SystemExit(max(results))

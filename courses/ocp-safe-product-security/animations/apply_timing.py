"""Apply measured timing JSON to its matching HTML; does not encode media.
Example: python3 animations/apply_timing.py animations/m1_reusable_evidence.timing.json
Set durationMs to final WAV milliseconds and optional beatMs mapping to actual
speech start times. beatMs overrides normalized beats, key by key.
"""
import json,re,sys
from pathlib import Path
for arg in sys.argv[1:]:
    timing=Path(arg);config=json.loads(timing.read_text())
    duration=float(config['durationMs'])
    assert duration>0
    for k,v in config.get('beatMs',{}).items():
        assert k in config['beats'] and 0<=v<duration,(k,v)
    html=timing.with_name(timing.name.replace('.timing.json','.html'))
    s=html.read_text()
    s=re.sub(r'data-duration-ms="[^"]+"',f'data-duration-ms="{duration}"',s)
    s=re.sub(r'data-poster-ms="[^"]+"',f'data-poster-ms="{round(duration*config["posterFraction"])}"',s)
    s=re.sub(r'(<script id="timeline" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps(config)+m[2],s,flags=re.S)
    html.write_text(s)
    print(html)

"""Maintain the specifically approved narration-synchronized figures."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]

def apply_approved_pilots(course):
    production=json.loads((ROOT/'tools/synced_video/production.json').read_text())
    for authorization in [production['authorization'],*production.get('additional_authorizations',[])]:
        if not any(a.get('id')==authorization['id'] for a in course['authorizations']):
            course['authorizations'].append(authorization)
    for row in production['figures']:
        module=next(m for m in course['modules'] if m['id']==row['module'])
        slide=next(s for s in module['slides'] if s['id']==row['slide'])
        figure=slide['figure']
        figure.update(row['figure'])
        for ref in row['reference_links']:
            if ref not in slide.setdefault('reference_links',[]):slide['reference_links'].append(ref)

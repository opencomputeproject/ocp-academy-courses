"""Build a local editorial inventory; never part of the SCORM runtime."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
import csv, html, json

P=Path(__file__).resolve().parents[1]
Q=P/'authoring/qa/reference-and-glossary-review'
C=json.loads((P/'course.json').read_text())
VENDORS={
 'delta-americas.com':'Delta','blog.stayonline.com':'StayOnline',
 'facebook.github.io':'Meta','eaton.com':'Eaton',
 'download.schneider-electric.com':'Schneider Electric','trane.com':'Trane',
 'metcaseusa.com':'Metcase','cyberpowersystems.com':'CyberPower',
 'canford.co.uk':'Canford','vertiv.com':'Vertiv',
 'blogs.cisco.com':'Cisco','cisco.com':'Cisco','docs.equinix.com':'Equinix',
 'arm.com':'Arm','ibm.com':'IBM','intel.com':'Intel','kingston.com':'Kingston',
 'macrium.com':'Macrium','micron.com':'Micron',
}
ORGS={
 'eia.gov':'EIA','uptimeinstitute.com':'Uptime Institute / Tier framework',
 'iea.org':'IEA','unavco.org':'UNAVCO research example','itu.int':'ITU',
 'nist.gov':'NIST','csrc.nist.gov':'NIST','nvlpubs.nist.gov':'NIST',
 'iso.org':'ISO','glossary.cncf.io':'CNCF','thegreengrid.org':'The Green Grid',
 'energy.gov':'US DOE','epa.gov':'US EPA','technav.ieee.org':'IEEE',
 'nvmexpress.org':'NVM Express','ats.uptimeinstitute.com':'Uptime Institute',
}

def classify(url):
 host=(urlparse(url).hostname or '').removeprefix('www.')
 if host=='opencompute.org' or host.endswith('.opencompute.org') or url.startswith('https://github.com/opencomputeproject/'):
  return 'OCP / Academy','OCP',host
 if host in VENDORS:return 'Vendor',VENDORS[host],host
 return 'Other non-OCP',ORGS.get(host,host),host

def link(label,url):
 return f'<a href="{html.escape(url,quote=True)}" target="_blank" rel="noopener">{html.escape(label)}</a>'

slides=[];references=[]
for module in C['modules']:
 for slide in module['slides']:
  sid=f'M{module["id"]}S{slide["id"]}';refs=[]
  items=list(slide.get('reference_links',[]))
  if slide.get('resource_callout',{}).get('url'):
   item=slide['resource_callout'];items.append({'label':item.get('title','Resource'),'url':item['url']})
  for item in items:
   kind,org,host=classify(item['url'])
   row={'slide':sid,'slide_title':slide.get('title',''),'label':item['label'],'url':item['url'],'category':kind,'organization':org,'domain':host,'status':'Pending review' if kind=='Vendor' else 'Active','recommendation':'Remove learner-facing pill; retain authoring evidence' if kind=='Vendor' else 'Review as needed'}
   refs.append(row);references.append(row)
  slides.append({'slide':sid,'title':slide.get('title',''),'module':module['id'],'references':refs})

titles={s['slide']:s['title'] for s in slides}
removed=[dict(slide=group['slide'],slide_title=group.get('slide_title',titles.get(group['slide'],'')),**r,status='Removed as requested') for group in C.get('learner_aids_editorial_policy',{}).get('reference_pills',{}).get('approved_removals',[]) for r in group.get('references',[])]
removed_terms=json.loads((Q/'removed-glossary-pills.json').read_text())
glossary=[]
for term in C['term_glossary']:
 kind,org,host=classify(term.get('url',''))
 places=[f'M{m["id"]}S{s["id"]}' for m in C['modules'] for s in m['slides'] if term['id'] in s.get('term_refs',[])]
 glossary.append({'term':term['term'],'source_url':term.get('url',''),'category':kind,'organization':org,'placements':places})
counts=Counter(r['category'] for r in references)
data={'slides':slides,'references':references,'removed_references':removed,'removed_glossary_pills':removed_terms,'glossary_source_register':glossary,'counts':{'all_slides':len(slides),'slides_with_references':sum(bool(s['references']) for s in slides),'reference_placements':len(references),'unique_urls':len({r['url'] for r in references}),'by_category':dict(counts),'glossary_definitions':len(glossary),'glossary_placements':sum(len(t['placements']) for t in glossary)}}
(Q/'Reference_Review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
with (Q/'Reference_Review.csv').open('w',newline='') as f:
 fields=['slide','slide_title','category','organization','label','url','status','recommendation'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in references:w.writerow({k:r.get(k,'') for k in fields})
 for r in removed:
  kind,org,_=classify(r['url']);w.writerow({k:dict(r,category=kind,organization=org,recommendation='Authoring source retained').get(k,'') for k in fields})

rows=[]
for slide in slides:
 items=[]
 for r in slide['references']:
  badge='vendor' if r['category']=='Vendor' else 'ocp' if r['category']=='OCP / Academy' else 'other'
  note='<span class="suggestion">Suggested: remove this pill; retain its source in authoring.</span>' if badge=='vendor' else ''
  items.append(f'<li>{link(r["label"],r["url"])} <span class="tag {badge}">{html.escape(r["organization"])}</span><small>{html.escape(r["domain"])}</small>{note}</li>')
 cats=' '.join(sorted({r['category'].split()[0].lower() for r in slide['references']}))
 search=' '.join([slide['slide'],slide['title']]+[r['label']+' '+r['organization']+' '+r['url'] for r in slide['references']]).lower()
 refs='<ul>'+''.join(items)+'</ul>' if items else '<span class="none">No reference pills</span>'
 rows.append(f'<tr data-categories="{cats}" data-has-refs="{str(bool(items)).lower()}" data-search="{html.escape(search,quote=True)}"><th>{slide["slide"]}</th><td>{html.escape(slide["title"])}</td><td>{refs}</td></tr>')
removed_html=''.join(f'<li>{r["slide"]}: {link(r["label"],r["url"])} — removed.</li>' for r in removed)
term_html=''.join(f'<tr><td>{r["slide"]}</td><td>{html.escape(r["term"])}</td><td>{html.escape(r["title"])}</td></tr>' for r in removed_terms)
source_html=''.join(f'<tr><td>{html.escape(t["term"])}</td><td>{", ".join(t["placements"])}</td><td>{link(t["organization"],t["source_url"])}</td><td>{html.escape(t["category"])}</td></tr>' for t in glossary)
out='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DC Basics — Reference Review</title><style>
*{box-sizing:border-box}body{margin:0;background:#f5f7fa;color:#243244;font:16px/1.55 system-ui,Arial,sans-serif}main{max-width:1280px;margin:auto;padding:32px 24px 64px}h1{font-size:30px;line-height:1.2;margin:0 0 16px}h2{font-size:21px;margin-top:32px}p{max-width:1000px}a{color:#343895;text-decoration-thickness:1px;text-underline-offset:3px;overflow-wrap:anywhere}a:hover{color:#496b20}.summary{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0}.summary span{padding:12px 16px;background:white;border:1px solid #dce3e9;border-radius:9px}.summary b{font-size:23px;margin-right:6px}.filters{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:20px 0}input[type=search]{flex:1;min-width:180px}input,select{font:inherit;padding:9px 12px;border:1px solid #aab6c4;border-radius:6px;background:white;color:inherit}.filters select{max-width:100%;min-width:0}.filters label{display:flex;align-items:center;gap:7px}.table-wrap{overflow:auto;background:white;border:1px solid #dce3e9;border-radius:9px}table{width:100%;border-collapse:collapse;min-width:700px;text-align:left}td,th{padding:13px 16px;vertical-align:top;border-bottom:1px solid #e4e9ee}thead{background:#edf1f6}tbody th{white-space:nowrap;width:90px}td:nth-child(2){width:30%}ul{margin:0;padding-left:20px}li+li{margin-top:12px}small,.suggestion{display:block;font-size:12px;color:#607082}.suggestion{color:#946113}.tag{display:inline-block;border-radius:20px;padding:2px 9px;margin:3px 0 0 6px;font-size:11px;border:1px solid #d2dae4;white-space:nowrap}.vendor{background:#fff0dd;border-color:#e7c38d}.ocp{background:#f1f8e6;border-color:#cce3a8}.other{background:#eef1f7}.none{color:#80909e}details{margin-top:28px}summary{cursor:pointer;font-size:19px;font-weight:650;margin-bottom:14px}.policy{background:#eef7e5;border-left:4px solid #8dc63f;padding:12px 18px;margin-top:24px}#resultCount{font-size:14px;color:#607082}@media(max-width:600px){main{padding:24px 16px}h1{font-size:26px}.summary{gap:8px}.summary span{padding:8px 10px}.summary b{font-size:20px}}
</style><main><h1>DC Basics: slide references for review</h1><p>The approved reference pills have been removed; see the removal list below. The remaining vendor pills are listed for your decision. External research remains available as authoring evidence.</p>'''
out+=f'<div class="summary"><span><b>{len(slides)}</b>slides</span><span><b>{len(references)}</b>active reference pills</span><span><b>{counts["Vendor"]}</b>vendor pills to review</span><span><b>{counts["Other non-OCP"]}</b>other non-OCP references</span><span><b>{counts["OCP / Academy"]}</b>OCP / Academy references</span></div>'
out+=f'<p><strong>Recommendation:</strong> remove the {counts["Vendor"]} remaining vendor pills from the learner slides while retaining those sources in the authoring records. Standards, government, research and OCP resources are shown separately for review. Uptime Institute is identified as the Tier-framework source rather than an equipment vendor.</p><p><a href="Reference_Review.csv">Download reference list (CSV)</a></p>'
out+='<div class="filters"><input id="search" type="search" aria-label="Search slides and references" placeholder="Search slide, organization or reference"><select id="category" aria-label="Reference category"><option value="all">All references</option><option value="vendor">Slides with vendor references</option><option value="other">Slides with other non-OCP references</option><option value="ocp">Slides with OCP / Academy references</option></select><label><input id="includeEmpty" type="checkbox">Include slides without references</label></div><p id="resultCount"></p><div class="table-wrap"><table id="references"><thead><tr><th>Slide</th><th>Slide title</th><th>Reference pills</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
out+='<h2>Already removed</h2><ul>'+removed_html+'</ul><h2>Glossary cleanup</h2><div class="policy">Basic words are defined at their first useful introduction in the course. A module change or passing mention does not trigger another pill. Useful acronym reminders and repeated technical concepts taught in depth can remain.</div>'
out+=f'<p>Removed {len(removed_terms)} repeated glossary placements: 72 → 59 pills. All 48 definitions remain available where they are useful. Focused repeats such as redundancy, colocation and rack units remain.</p><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Removed pill</th><th>Slide title</th></tr></thead><tbody>'+term_html+'</tbody></table></div>'
out+='<details><summary>Glossary source register — authoring evidence</summary><p>These URLs document the definitions’ sources. Glossary pills themselves are tooltips, not external navigation links. Vendor sources here can remain useful without becoming learner reference pills.</p><div class="table-wrap"><table><thead><tr><th>Term</th><th>Pill locations</th><th>Source</th><th>Category</th></tr></thead><tbody>'+source_html+'</tbody></table></div></details>'
out+='''<script>const rows=[...document.querySelectorAll('#references tbody tr')];function filter(){const query=document.getElementById('search').value.trim().toLowerCase(),category=document.getElementById('category').value,empty=document.getElementById('includeEmpty').checked;let n=0;for(const row of rows){const show=(empty||row.dataset.hasRefs==='true')&&(category==='all'||row.dataset.categories.split(' ').includes(category))&&row.dataset.search.includes(query);row.hidden=!show;if(show)n++}document.getElementById('resultCount').textContent=n+' of '+rows.length+' slides shown'}for(const id of ['search','category','includeEmpty'])document.getElementById(id).addEventListener('input',filter);filter();</script></main></html>'''
(Q/'Reference_Review.html').write_text(out)
print(json.dumps(data['counts']))

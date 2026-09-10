"""Readable offline learner resources and editor review entry points."""
from pathlib import Path
import argparse, json, wave, struct
from html import escape as e
SPEC_URL='https://www.opencompute.org/documents/open-data-center-spec-revision-0-7-0-4-pdf'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('course_json',type=Path,help='Staged build/course.json; outputs stay in its directory')
args=parser.parse_args()
OUT=args.course_json.resolve().parent
RES=OUT/'resources'; RES.mkdir(exist_ok=True)
course=json.loads((OUT/'course.json').read_text())
STYLE='''*{box-sizing:border-box}body{margin:0;background:#F3F5F0;color:#5F6062;font:17px/1.6 Arial,sans-serif}main{max-width:1120px;margin:32px auto;background:white;padding:42px;border-top:10px solid #8DC63F}h1{font-size:32px;line-height:1.2;margin:0 0 12px}h2{font-size:23px;margin:32px 0 12px;color:#5F6062}h3{font-size:19px}p{margin:12px 0}a{color:#527921;text-decoration:underline}table{border-collapse:collapse;width:100%;margin:18px 0;font-size:15px}th,td{padding:12px 14px;border:1px solid #D7DBD1;text-align:left;vertical-align:top}th{background:#EAF2DD}.note{padding:16px 20px;background:#F0F5E8;border-left:6px solid #8DC63F}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.field{border:1px solid #ccd2c5;padding:12px;min-height:100px}.muted{font-size:14px}button{font:inherit;border:1px solid #5F6062;background:white;padding:8px 16px;border-radius:8px;color:#5F6062;cursor:pointer}textarea,input{display:block;width:100%;font:inherit;border:1px solid #c9cec4;padding:8px;color:#5F6062}textarea{min-height:80px;resize:vertical}.figure{width:100%;height:auto}nav{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:20px}details{border:1px solid #d5dacd;padding:14px;margin:16px 0}summary{cursor:pointer;font-weight:700}@media(max-width:700px){main{margin:0;padding:24px 18px}.grid{grid-template-columns:1fr}table{font-size:13px}td,th{padding:8px}h1{font-size:27px}}@media print{@page{size:A4;margin:12mm}body{background:white;font-size:10pt;line-height:1.35}main{border:0;margin:0;padding:0;max-width:none}nav,button,.no-print{display:none}h1{font-size:20pt}h2{font-size:13pt;margin:14px 0 8px}.field{min-height:70px}textarea{min-height:55px}table{font-size:9pt}th,td{padding:6px}a{color:#5F6062}.print-break{break-before:page}}
'''
def page(title,body):
    body=body.replace('<table','<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable reference table"><table').replace('</table>','</table></div>')
    body='<style>.table-scroll{max-width:100%;overflow-x:auto}.table-scroll:focus-visible{outline:3px solid #6FA030}@media print{.table-scroll{overflow:visible}}</style>'+body
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{STYLE}</style></head><body><main><nav><a href="../index.html">Course home</a><a href="{SPEC_URL}" target="_blank" rel="noopener">Published 0.7 specification</a></nav><h1>{e(title)}</h1>{body}</main><script>const printButton=document.getElementById("printWorksheet");if(printButton)printButton.addEventListener("click",()=>window.print());</script></body></html>'

ledger=[
('Heaviest single rack','8,000 lb (3,629 kg); 28 × 48 in structural basis','Design target for heaviest rack; include handling equipment in moving load','§4.1 · p. 7'),
('Rack + sidecar example','8,000 + 7,000 = 15,000 lb (6,804 kg); 56 × 48 in','Before handling device; footprint average is not a wheel-load or route approval','§4.1 · p. 7'),
('Transport clearance','12 ft (3.7 m in prose; 3,658 mm in Table 1)','§4.2 calls this a design recommendation; Table 1 lists it among minimum dimensions. Ask authors/project reviewers to resolve application.','§4.2 · p. 7; Table 1 · p. 8'),
('Row geometry','Hot aisle 54 in; cold aisle 82 in face-to-face; rack height 100 in; rack depth 71 in','Table 1 is headed minimum dimensions. Course calls height/depth row-envelope targets, not invented maxima; clarify intended accommodation semantics.','Table 1 · p. 8'),
('Aisle pitch','24 ft (7.3 m); racks front-justified on cold aisle','Recommended; retain its datum and relationship to the listed dimensions','§4.2 · p. 7'),
('Two-busway ceiling','18 ft (5.5 m) minimum floor to beam underside, including air plenum','Four busways/additional tray tiers may require more height. Constrained sites need custom design variations; not automatic approval.','§4.2 · p. 7'),
('Row length','Modular power density, kW/ft','Fixed length prescriptions replaced; example course lengths are illustrative, not specified','§4.2 · p. 7'),
('Blended baseline','25 kW/ft (82 kW/m)','Mixed equipment planning; 15 kW/ft air and 25 kW/ft liquid are capabilities, not a universal additive 40 kW/ft load','§5.1 · Table 2 · p. 8'),
('Peak IT','350 kW/ft (1,148 kW/m); expected 2027 rack peak 125 kW/ft (410 kW/m)','Local high-density ML condition. Keep the expectation and horizon attached to 125.','§5.1 · Table 2 · p. 8'),
('Cluster baseline','12 MW minimum; 24 MW preferred','Cluster scale, not a rating for an individual hall power block','§5.1 · Table 2 · p. 8'),
('Power blocks','At least four per data hall','Count only; §5.2 does not define block rating, independence, redundancy or one-to-one row mapping. Busway count varies with design and row density.','§5.2 · p. 8'),
('Blended cooling horizon','By 2028: up to 25 kW/ft liquid, 15 kW/ft air','Row/wall manifold sized for entire row, with drops and multiple rack-loop connections','§§6.1–6.2 · p. 9'),
('Peak cooling split','335 liquid + 15 air = 350 kW/ft','Specifically the local peak condition, not a default for the whole facility','§6.3 · p. 9'),
('Quick-connect note','Publication notes industry availability at maximum 2 in','Dated August 27, 2026 source statement, not independent market verification. Confirm actual hardware and conditions.','Table 3 note 2 · p. 9'),
('Appendix concepts','Google and NVIDIA physical examples, pp. 10–18','Reference concepts, not normative construction drawings; actual designs need validation','Specification note · p. 4; Appendix · pp. 10–18'),
]
body='<p>Authority: published Revision 0.7.0, effective August 27, 2026. This ledger preserves scope and qualifications; it is a learning aid, not an engineering acceptance document.</p><table><thead><tr><th>Boundary</th><th>Value / statement</th><th>Qualification</th><th>Source</th></tr></thead><tbody>'
for row in ledger: body+='<tr>'+''.join('<td>'+e(v)+'</td>' for v in row)+'</tr>'
body+='</tbody></table><h2 id="table3">Table 3 — cooling-capacity screen</h2><p>Source assumption: fluid speed 3 m/s. Capacities below are kW. Do not discard the required lpm/kW ratio.</p><table><thead><tr><th>Diameter (in)</th><th>1 lpm/kW</th><th>1.5 lpm/kW</th></tr></thead><tbody>'
for row in [(1,91,61),(2,365,243),(3,820,547),(4,1459,972)]: body+='<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>'
body+='</tbody></table><p class="note">Worked illustration: a 300 kW liquid load clears the 2 in / 1 lpm/kW screen (365 kW), but fails the 2 in / 1.5 lpm/kW screen (243 kW). These results do not approve pressure loss, actual bore, fluid/temperature conditions, branches, valves, connectors, or operating margins.</p><h2>What this specification does not settle</h2><p>A shared facility target does not define all connector products, electrical topologies, hydraulic conditions, telemetry schemas or operating responsibilities. The broader OCP initiative and project-specific engineering supply additional inputs. Avoid declaring universal interoperability from the 0.7 baseline alone.</p>'
(RES/'requirements_ledger.html').write_text(page('Requirements ledger and capacity assumptions',body))

body='<p>A one-page review record. Fill it locally, then print or save as PDF. No values are sent to a server or stored automatically.</p><button id="printWorksheet">Print / save as PDF</button><div class="grid">'
fields=[('Project / equipment / date',''),('Source authority','Revision 0.7.0 · August 27, 2026 · section/page:'),('Requirement / target / recommendation + datum',''),('Measured site or equipment condition',''),('Proposed design / variation + assumptions',''),('Required evidence','Load and movement; clearance and access; electrical and liquid conditions; operations:'),('Owners + required reviewers',''),('Disposition + open actions','OPEN / accepted / rejected / superseded — record evidence, decision owner and date:')]
for label,value in fields: body+=f'<label class="field">{e(label)}<textarea aria-label="{e(label)}">{e(value)}</textarea></label>'
body+='</div><p class="note">Do not close the record on a drawing or a checkmark alone. Identify the evidence and accountable decision. Appendix examples do not replace the core text; custom-design language is not blanket permission to vary other requirements.</p><h2 class="print-break">Filled learning example — constrained overhead</h2><table><tbody>'
for a,b in [('Authority','§4.2, p. 7: 18 ft floor to beam underside for two busways, including plenum; custom designs for constrained facilities.'),('Site','Illustrative measured height: 17 ft 6 in floor to beam underside.'),('Proposal','Custom coordinated overhead arrangement, not yet accepted.'),('Evidence','Measured section and clearance study; plenum/thermal analysis; structural, fire-protection and maintenance reviews; actual equipment interfaces.'),('Owners','MEP lead coordinates accountable structural, electrical, mechanical, fire and operator reviewers.'),('Disposition','OPEN. Confirm scope, assumptions, evidence and required acceptance. No approved exception is implied.')]: body+='<tr><th>'+e(a)+'</th><td>'+e(b)+'</td></tr>'
body+='</tbody></table>'
(RES/'compatibility_review.html').write_text(page('Compatibility review worksheet',body))

body='<p>Complete narration text, with conventional acronym spelling. Use the slide’s Transcript control for the same text while studying. Technical figures remain illustrative unless specifically identified as source material.</p>'
durations={}
for m in course['modules']:
    body+=f'<h2 id="module{m["id"]}">Module {m["id"]}: {e(m["title"])}</h2>'
    duration=0
    audio_complete=True
    for s in m['slides']:
        audio_path=OUT/s['audio']['wav_file']
        if audio_path.is_file():
            with wave.open(str(audio_path)) as wav: duration+=wav.getnframes()/wav.getframerate()
        else:
            audio_complete=False
        body+=f'<h3 id="m{m["id"]}s{s["id"]}">M{m["id"]}S{s["id"]} · {e(s.get("title") or s.get("next_module_title") or s["slug"])}</h3>'
        body+=''.join('<p>'+e(p)+'</p>' for p in s['transcript'].split('\n\n'))
        if s.get('figure'): body+='<p class="muted">Visual: '+e(s['figure']['alt'])+' '+e(s['figure']['caption'])+'</p>'
        refs=s.get('reference_links',[])
        if refs: body+='<p class="muted">Resources: '+ ' · '.join(f'<a href="{e(r["url"] if r["url"].startswith("http") else "../"+r["url"])}">{e(r["label"])}</a>' for r in refs)+'</p>'
    durations[str(m['id'])]=round(duration,3) if audio_complete else None
(RES/'course_transcript.html').write_text(page('Open Data Center for AI — complete transcript',body))
(OUT/'narration_durations.json').write_text(json.dumps({'modules':durations,'total':round(sum(durations.values()),3) if all(v is not None for v in durations.values()) else None},indent=2)+'\n')
print('Built worksheet, requirements ledger, full transcript, and measured narration durations.')

figures=[
('source_fig01_row_envelope.png','Google · typical row layout with multiple rack depths',10),
('source_fig02_filler_panel.png','Google · filler panels at containment gaps',10),
('source_fig03_google_row_2028.png','Google · example 2028+ TPU row layout',11),
('source_fig04_google_row_2026.png','Google · example 2026–2027 TPU row layout',11),
('source_fig05_google_fanwall.png','Google · fanwall cooling cross-section',12),
('source_fig06_google_inrow.png','Google · in-row cooling and building columns',12),
('source_fig07_google_two_busway.png','Google · two-busway cross-section and isometric view',13),
('source_fig08_google_four_busway.png','Google · four-busway cross-section and isometric view',14),
('source_fig09_nvidia_hac.png','NVIDIA · four-busway containment concept',15),
('source_fig10_nvidia_cross_section.png','NVIDIA · four-busway cross-section',15),
('source_fig11_nvidia_inrow.png','NVIDIA · in-row cooling cross-section',16),
('source_fig12_power_manifold.png','NVIDIA · power network module and row manifolds',16),
('source_fig13_row_manifold.png','NVIDIA · row manifolds and 4 in tap location',17),
('source_fig14_busway_connectors.png','NVIDIA · busway with row-to-row connectors',17),
('source_fig15_hall_views.png','NVIDIA · busway configuration across two containment structures / four rows',18),
]
body='<p>Explore the physical source concepts at full width. Each image opens at its native resolution. These are reference examples, not independent requirements or construction approval.</p><p class="note">Edition note: these images were extracted from the supplied June 23, 2026 Revision 0.7 draft. The course’s numerical authority is the published August 27 edition linked above. Do not assume that every Appendix illustration is unchanged; final published-image reconciliation remains a release check.</p><nav>'
body+=' · '.join(f'<a href="#figure{i}">{i}</a>' for i in range(1,16))+'</nav>'
for i,(name,label,pageno) in enumerate(figures,1):
    # Reserve each PNG's exact aspect ratio BEFORE lazy loading. Otherwise the
    # browser resolves #figure14 against collapsed images, then earlier images
    # expand and leave the learner looking at the wrong figure on first load.
    with (OUT/'figures'/name).open('rb') as image:
        header=image.read(24)
    if header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
        raise ValueError(f'Expected PNG dimensions in {name}')
    width,height=struct.unpack('>II',header[16:24])
    body+=f'<section id="figure{i}" style="scroll-margin-top:20px;display:flow-root"><h2>Figure {i} — {e(label)}</h2><a href="../figures/{name}" target="_blank" rel="noopener"><img class="figure" style="display:block" loading="lazy" width="{width}" height="{height}" src="../figures/{name}" alt="{e(label)}"></a><p class="muted">Open Data Center Specification Revision 0.7.0 · supplied June 23 draft · extracted from PDF page {pageno}. Attribution: {e(label.split(" · ")[0])} / OCP source contribution.</p></section>'
(RES/'source_figures.html').write_text(page('Physical source-figure gallery',body))

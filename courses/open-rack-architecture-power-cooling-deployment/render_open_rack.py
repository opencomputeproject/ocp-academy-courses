"""Render with AcademyWizard, then add the two course-specific Module 1 interactions."""
import argparse, json, os, re, subprocess, sys
from pathlib import Path

cli=argparse.ArgumentParser()
cli.add_argument('course_json', type=Path)
scope=cli.add_mutually_exclusive_group(required=True)
scope.add_argument('--all',action='store_true')
scope.add_argument('--module',type=int)
args=cli.parse_args()
source=args.course_json.resolve()
root=source.parent
configured=os.environ.get('ACADEMY_WIZARD_SKILL_DIR') or os.environ.get('ACADEMY_WIZARD_DIR')
if configured:
    wizard=Path(configured).resolve()
else:
    wizard=next((p/'skills/academy-wizard' for p in root.parents if (p/'skills/academy-wizard/scripts/render_module.py').is_file()),None)
if not wizard or not (wizard/'scripts/render_module.py').is_file():
    cli.error('Set ACADEMY_WIZARD_SKILL_DIR to the AcademyWizard directory.')
sys.path.insert(0,str(wizard/'scripts'))
subprocess.run([sys.executable,str(wizard/'scripts/render_module.py'),str(source),*(['--all'] if args.all else ['--module',str(args.module)])],check=True)
if not args.all and args.module!=1: sys.exit(0)
m1=root/'module1.html'
t=m1.read_text()
opening=r'<div class="(slide(?: [^"]*)?)" data-slide="1"(?: [^>]*)?>'
m=re.search(opening,t);assert m,"Missing module 1 opening"
assert {"slide-hero","active"} <= set(m[1].split()), "Module 1 must open on its native welcome slide."
# Use the standard keyboard- and pointer-zoomable figure panel for the companion
# picture. Leave the primary video intact so it keeps its own narration clock.
if (root/'course.json').exists() and 'id="rack-interface-pair"' not in t:
    from render_module import _figure_html
    course=json.loads((root/'course.json').read_text())
    slide=next(s for s in course['modules'][0]['slides'] if s['id']==3)
    companion=slide['companion_figure']
    assert (root/companion['path']).is_file()
    main=_figure_html(slide['figure'],course)
    assert t.count(main)==1,'Primary teaching video markup changed'
    pair='<div id="rack-interface-pair">'+main+_figure_html(companion,course)+'</div>'
    t=t.replace(main,pair).replace('</head>','''<style>
#rack-interface-pair{display:grid;grid-template-columns:minmax(0,1.9fr) minmax(0,1fr);align-items:start;gap:clamp(16px,2vw,28px);max-width:1100px;margin:0 auto}
#rack-interface-pair>.figure-wrap{min-width:0;width:100%;max-width:100%;margin-inline:0}
@media(max-width:740px){#rack-interface-pair{grid-template-columns:minmax(0,1fr);gap:16px}#rack-interface-pair>.figure-wrap:nth-child(2){max-width:440px}}
</style></head>''',1)
    m1.write_text(t)
if (root/'course.json').exists() and 'id="interface-points"' not in t:
    from html import escape
    from render_module import _figure_html
    course=json.loads((root/'course.json').read_text())
    slides={s['id']:s for s in course['modules'][0]['slides']}
    s=slides[4]; cfg=s['timed_points']; points=cfg['points']
    first=t.index('data-slide="4"'); last=t.index('data-slide="5"',first); part=t[first:last]
    buttons=''.join(f'<li><button type="button" data-at="{p["at"]}" data-view="{escape(p["view"])}"'+
        (' aria-current="step"' if i==0 else '')+f'>{escape(p["text"])}</button></li>' for i,p in enumerate(points))
    agenda='<p class="interface-hint">Select a point to jump to it.</p><ul class="interface-agenda" aria-label="Narration points">'+buttons+'</ul>'
    part,n=re.subn(r'<ul class="bullet-list animate-in">.*?</ul>',lambda _:agenda,part,count=1,flags=re.S); assert n==1
    main=_figure_html(s['figure'],course)
    views={'connector':_figure_html(slides[3]['companion_figure'],course),'latch':main}
    for k,rows in cfg['comparisons'].items():
        views[k]='<dl class="interface-comparison">'+''.join(f'<div><dt>{escape(key)}</dt><dd>{escape(value)}</dd></div>' for key,value in rows)+'</dl>'
    assert part.count(main)==1 and part.count('<div class="two-column">')==1
    assert set(views)=={p['view'] for p in points}
    stage='<div class="interface-stage">'+''.join(f'<div data-panel="{k}"'+('' if k==points[0]['view'] else ' hidden')+'>'+v+'</div>' for k,v in views.items())+'</div>'
    part=part.replace(main,stage).replace('<div class="two-column">','<div class="two-column" id="interface-points">')
    t=t[:first]+part+t[last:]
    marker='let audioPlayer = new Audio();'
    assert t.count(marker)==1
    interface_js=r'''// The module's own narration element drives the highlights, including seeks and speed changes.
(() => {
  const root = document.getElementById('interface-points');
  const buttons = Array.from(root.querySelectorAll('button[data-at]'));
  const panels = Array.from(root.querySelectorAll('[data-panel]'));
  const times = buttons.map(b => Number(b.dataset.at));
  let active = -1;
  function show(i) {
    if (active === i) return;
    active = i;
    buttons.forEach((b, n) => n === i ? b.setAttribute('aria-current','step') : b.removeAttribute('aria-current'));
    panels.forEach(p => { p.hidden = p.dataset.panel !== buttons[i].dataset.view; });
  }
  function sync() {
    if (currentSlide !== 4) return;
    let i = 0;
    while (i + 1 < times.length && times[i + 1] <= audioPlayer.currentTime) i++;
    show(i);
  }
  ['loadedmetadata','play','timeupdate','seeking','seeked','ended'].forEach(e => audioPlayer.addEventListener(e, sync));
  window.addEventListener('academy:slide', e => { if (e.detail === 4) show(0); });
  buttons.forEach((b,i) => {
    b.addEventListener('keydown', e => { if (e.key === ' ' || e.key === 'Enter') e.stopPropagation(); });
    b.addEventListener('click', () => {
      if (currentSlide !== 4) return;
      audioPlayer.currentTime = times[i];
      show(i);
    });
  });
  show(0);
})();
'''
    interface_css=r'''#interface-points{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:clamp(18px,3vw,44px);align-items:start;width:100%;max-width:930px;margin-inline:auto}
#interface-points .interface-hint{font-size:.85rem;color:var(--text-secondary);margin:0 0 8px}
#interface-points .interface-agenda{list-style:none;margin:0;padding:0;display:grid;gap:3px}
#interface-points .interface-agenda button{display:flex;align-items:center;gap:.7em;width:100%;min-height:44px;padding:.45em .6em;border:1px solid transparent;border-radius:6px;color:var(--text-primary);background:transparent;font:inherit;font-size:clamp(.92rem,1.45vw,1.12rem);line-height:1.32;text-align:left;cursor:pointer}
#interface-points .interface-agenda button::before{content:"";width:8px;height:8px;flex:none;border:1px solid currentColor;border-radius:50%}
#interface-points .interface-agenda button[aria-current]{background:var(--ocp-green-subtle);font-weight:700}
#interface-points .interface-agenda button[aria-current]::before{background:var(--ocp-green);border-color:var(--ocp-green-dark)}
#interface-points .interface-agenda button:is(:hover,:focus-visible){border-color:var(--ocp-green-dark)}
#interface-points [hidden]{display:none!important}
#interface-points .interface-stage{max-width:360px;margin:0 auto}
#interface-points .figure-wrap{max-width:100%;row-gap:8px}
#interface-points .figure-panel{box-sizing:border-box;max-width:100%}
#interface-points .figure-panel img{max-width:100%;height:auto}
#interface-points .interface-comparison{display:grid;gap:20px;margin:8px 0;line-height:1.45}
#interface-points .interface-comparison div{padding-left:14px;border-left:3px solid var(--ocp-green)}
#interface-points dt{font-weight:700;color:var(--text-primary)}
#interface-points dd{margin:3px 0 0;color:var(--text-secondary)}
@media(max-width:740px){#interface-points{grid-template-columns:minmax(0,1fr);gap:12px}#interface-points .interface-stage{max-width:300px}#interface-points .interface-agenda{gap:0}}
'''
    t=t.replace(marker,marker+'\n'+interface_js)
    m1.write_text(t.replace('</head>','<style>'+interface_css+'</style></head>',1))

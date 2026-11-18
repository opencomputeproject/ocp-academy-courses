"""Apply course-specific interactions to the maintained Academy player."""
import argparse, html, json, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT/'assets/player'
SKILL=Path(os.getenv('ACADEMY_WIZARD_SKILL_DIR',Path.home()/'.codex/skills/academy-wizard'))
sys.path.insert(0,str(SKILL/'scripts'))
import render_module as academy
e=html.escape

def activity(s):
    a=s['activity'];n=s['id']
    if n==3:
        body='''<div class="guess-controls"><label for="forecastGuess">Estimated annual spending</label><output id="forecastValue" for="forecastGuess">$500B</output><input id="forecastGuess" aria-valuetext="500 billion dollars" type="range" min="300" max="1000" step="25" value="500"><div class="buttons"><button type="button" data-reveal="guess">Check my estimate</button><button type="button" data-reveal="skip">Skip the guess</button></div></div><p class="prediction-result" aria-live="polite" tabindex="-1" hidden></p><details class="market-extra extra-forecast"><summary>One year further</summary><p>For 2030, IDC projects $892 billion. That would be about 51% of spending in the infrastructure categories it measures.</p></details>'''
    else:
        buttons=''.join(f'<button type="button" aria-pressed="false" data-option="{i}">{e(v["label"])}</button>' for i,v in enumerate(a['options']))
        hint='<p class="market-seek-hint">Choose an option to jump to that moment in the video.</p>' if 'listen_at' in a['options'][0] else ''
        body=f'{hint}<div class="market-options">{buttons}</div><div class="activity-result" aria-live="polite" hidden><p></p><a target="_blank" rel="noopener" hidden></a></div>'
    return f'<section class="market-activity" data-activity="{n}" aria-labelledby="activity{n}"><h3 id="activity{n}">{e(a["prompt"])}</h3>{body}</section>'

def diagram(slide,course,module):
    n=slide['id'];fig=slide['figure']
    media=' data-video-slide="true"' if fig.get('media_type')=='video' else ''
    focus=' slide--media-focus' if slide.get('media_focus') else ''
    active=' active' if n==1 else ''
    return f'''<div class="slide market-slide{focus}{active}" data-slide="{n}"{media}><div class="slide-content"><span class="section-label">{e(slide["section_label"])}</span><h2 class="slide-title">{e(slide["title"])}</h2><div class="market-layout">{academy._figure_html(fig,course)}{activity(slide)}</div>{academy._learner_aids_html(slide,course)}</div></div>'''
def closing(slide,course,module):
    a=slide['activity'];default=academy.render_course_complete(slide,course,module)
    content=f'''<section class="market-closing" aria-label="Choose your next step"><h3>What will you bring?</h3><p>{e(a["prompt"])}</p><div class="actions"><a class="course-action secondary" href="{e(a["newsletter"])}" target="_blank" rel="noopener">Subscribe to the OCP newsletter</a><a class="course-action secondary" href="{e(a["catalog"])}" target="_blank" rel="noopener">Browse Data Center Technologies</a></div></section>'''
    pos=default.index('</p>',default.index('class="slide-subtitle'))+4
    return default[:pos]+content+default[pos:]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('course_json',type=Path);ap.add_argument('--all',action='store_true');ap.add_argument('--module',type=int,default=1)
    args=ap.parse_args();data=json.loads(args.course_json.read_text())
    academy.RENDERERS['content_diagram']=diagram
    academy.RENDERERS['course_complete']=closing
    player=academy.render_module(data,0)
    content={s['id']:s['activity'] for s in data['modules'][0]['slides'] if 'activity'in s}
    script=(AUTHOR/'activities.js').read_text().replace('MARKET_ACTIVITY_DATA',json.dumps(content,ensure_ascii=False).replace('</','<\\/'))
    still='const visualTime = !motionEnabled() ? video.duration - 1 / 24'
    if player.count(still)!=1:raise RuntimeError('Academy reduced-motion alignment changed')
    player=player.replace(still,'const visualTime = !motionEnabled() ? marketStillTime(video)')
    anchor='  syncSlideVideos(currentSlide, true);\n  updateControls();\n  loadSlideAudio(currentSlide);'
    if player.count(anchor)!=1:raise RuntimeError('Academy player initialization changed')
    player=player.replace(anchor,script+'\n'+anchor).replace('</head>','<style>'+ (AUTHOR/'activities.css').read_text()+'</style>\n</head>')
    (ROOT/'module1.html').write_text(player)
if __name__=='__main__':main()

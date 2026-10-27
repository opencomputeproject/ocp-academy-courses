"""Source-preserving Slides extensions for original videos and matching checks."""
import json
from html import escape
import random

def original_video_html(fig, course):
    from video_player import academy_video_html
    e=lambda value:escape(str(value or ''),quote=True)
    media=dict(fig)
    media['captions']=[dict(t,_cues=fig.get('caption_cues',[])) for t in fig.get('captions',[])]
    player=academy_video_html(media,ui_labels=course.get('ui_labels'),video_class='original-video')
    return f'<div class="figure-wrap original-video-wrap"><div class="figure-panel original-video-panel">{player}</div><p class="figure-caption">{e(fig.get("caption"))}</p></div>'

def matching_question_html(q, module, slide):
    e=lambda s:escape(str(s),quote=True)
    pairs=q['pairs'];options=list(pairs);random.Random(q['id']).shuffle(options)
    options_html='<option value="">Choose a match…</option>'+''.join(f'<option value="{e(p["id"])}">{e(p["match"])}</option>' for p in options)
    rows=''.join(f'''<div class="matching-row"><label for="{e(q['id']+'_'+p['id'])}">{e(p['prompt'])}</label><select id="{e(q['id']+'_'+p['id'])}" data-prompt-id="{e(p['id'])}">{options_html}</select></div>''' for p in pairs)
    data=e(json.dumps(pairs,ensure_ascii=False))
    return f'''<div class="quiz-card matching-card animate-in" data-question-id="{e(q['id'])}" data-matching="true" data-pairs="{data}" data-correct-feedback="{e(q['feedback_correct'])}" data-incorrect-feedback="{e(q['feedback_incorrect'])}"><p class="quiz-question">{e(q['prompt'])}</p><div class="matching-rows">{rows}</div><div class="quiz-actions"><button class="quiz-submit" type="button">Submit</button><button class="quiz-retry" type="button">Retry</button></div><div class="quiz-feedback" aria-live="polite"></div></div>'''

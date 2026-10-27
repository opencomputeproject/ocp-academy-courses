"""Move the question; keep the model. Final WAV: 42.679546485 s."""
from .primitives import *

def ownership(parts, policy=False, final=False):
    # Open corner boundaries convey organizational scope, not a security seal.
    parts += [text(370,180 if final else 200,'Integrator',60),text(1600,180 if final else 200,'Supplier',60),
              path('M1000 250 V820',GRAY,5,dash='14 14'),
              text(960,106,'Initial proof of concept',46,weight=500)]
    parts += [rect(145,285,325,395,WHITE,GRAY,5,0),
              line(180,720,520,720,GRAY,5),line(350,680,350,720,GRAY,5)]
    parts += [chip(1420,315,360,300,'Detailed\nmodel'),text(1600,820,'Supplier-controlled\nmodel',46)]
    if final:
        parts += [path('M1420 290 H1395 V655 H1420 M1780 290 H1805 V655 H1780',GRAY,5)]
    if final:
        parts += [bracket(120,1380,860,'Shared analysis',GRAY,'up')]

def policy_view(t):
    parts=[text(960,106,'Initial proof of concept',46,weight=500)]
    # Enlarged ownership relationship leaves room for three short policy questions.
    parts += [text(270,190,'Integrator',56),text(1450,190,'Supplier',56),
              path('M980 225 V835',GRAY,5,dash='14 14'),chip(1240,330,440,275,'Detailed\nmodel')]
    parts += [line(270,415,1240,415,GRAY,5),line(1240,730,270,730,GRAY,5)]
    parts += [text(500,345,'Request',48),text(500,800,'Permitted results',48)]
    if t<19.76:
        parts += [text(1460,280,'Which model / version?',48),
                  text(580,520,'Who may ask?\nWhich queries?',48),
                  text(1460,875,'Which outputs?',48)]
    else:
        parts += [text(1460,280,'Identity · version',50),
                  text(580,520,'Authorization\nQuery limits',50),
                  text(1460,875,'Permitted outputs',50)]
        if t<21.38:
            y=298; x1,x2=1210,1710
        elif t<23.18:
            y=597; x1,x2=355,805
        else:y=895;x1,x2=1200,1720
        parts += [line(x1,y,x2,y,GREEN,7)]
    return svg(parts)

def render(t):
    if 17.08<=t<27.42:return policy_view(t)
    parts=[];final=t>=33.24
    ownership(parts,final=final)
    # A request is a different object from the model. The model never moves.
    if t>=3.24:
        p=smooth(t,3.24,5.86)
        x=lerp(410,1020,p)
        parts += [arrow(470,405,1420,405,GRAY,5),
                  token(x,335,'Request',w=280,h=140)]
        if t<9.38:parts+=[text(780,830,'The model stays with the supplier',52)]
    if t>=9.38:
        p=smooth(t,10.2,11.74)
        x=lerp(260,1020,p)
        parts += [arrow(470,570,1420,570,GRAY,5),token(x,500,'Conditions',w=360,h=140,accent=False)]
    if t>=11.86:
        p=smooth(t,11.86,13.38)
        x=lerp(1050,600,p)
        parts += [line(1600,615,1600,770,GRAY,5),arrow(1600,770,470,770,GRAY,5),
                  token(x,700,'Results',w=290,h=140)]
        if t<33.24:parts += [text(800,965,'Permitted results return',52)]
    if t>=27.42:
        # A small set of marks recalls policy obligations, without miniature text.
        if t<33.24:
            for x,y in [(1805,315),(1400,570),(535,770)]:
                parts += [path(f'M{x} {y-22} V{y+22} M{x-12} {y-22} H{x+12} M{x-12} {y+22} H{x+12}',GRAY,4)]
        if t<30.20:parts += [line(710,122,1210,122,GREEN,6)]
    if t>=38.34:
        # The final requirement is established before the last spoken word.
        parts=[s for s in parts if 'Shared analysis' not in s]
        parts += [text(510,250,'Shared analysis',46),text(960,925,'Accuracy: policies + evidence',48),
                  text(960,995,'Confidentiality: policies + evidence',48)]
        if t>=41.36:parts += [underline_phrase(960,925,'Accuracy: policies + evidence','policies + evidence',gap=19,width=6),
                             underline_phrase(960,995,'Confidentiality: policies + evidence','policies + evidence',gap=19,width=6)]
    return svg(parts)

"""M4S4: local evidence, system appraisal, and explicit revalidation."""
from .fcsa_helpers import *
KEY='M4S4';DURATION=timing(KEY)[0];POSTER_SECONDS=DURATION-1


def anchors():
    return [chip(140,330,660,445),chip(1120,330,660,445),text(470,420,'Chiplet A · primary',48),
            text(1450,420,'Chiplet B',50),text(470,550,'System RoT',52),text(470,680,'CRoT-A support',48),text(1450,550,'CRoT-A',52),
            text(1450,680,'Local responsibility',46)]


def render(t):
    i,p=scene(t,KEY);out=[]
    if i==0:
        out+=title('Evidence leaves; local duties remain')+anchors()
        q=phase(p,.25,.8)
        out.append(paper(lerp(1160,180,q),835,580,160,'Identity + state',True))
        out.append(arrow(1120,550,800,550,GRAY,5,20))
    elif i==1:
        out+=title('System RoT appraises the composition')
        out += [paper(190,335,610,260,'Chiplet evidence'),paper(1120,335,610,260,'Composition\n+ policy'),
                tag(735,700,'Appraisal',450,180),
                arrow(495,595,735,790,GRAY,5,20),arrow(1425,595,1185,790,GRAY,5,20),
                text(470,985,'Freshness',52),text(1430,985,'Roles + topology',52)]
    elif i==2:
        out+=title('Additional services are a separate role')
        out += [unit(120,350,660,370,'System RoT'),unit(1140,350,660,370,'Secondary RoT\n(optional)'),
                arrow(1140,535,780,535,GRAY,5,20),text(960,850,'System RoT decides composition',52),
                text(1470,980,'CRoT-A evidenced',46)]
    elif i==3:
        out+=title('A state change reopens the decision','Chiplet B: debug state changed')
        # Old evidence remains present and is relabelled, never magically approved.
        q=phase(p,.18,.7)
        out += [paper(180,365,570,260,'Earlier state'),paper(lerp(1170,1080,q),365,570,260,'Changed state',True),
                text(960,790,'Revalidate',58),text(960,930,'Update · Reset · Recovery',48)]
    else:
        out+=title('Maintain the system trust decision')
        out += [paper(140,335,580,230,'Earlier evidence'),paper(1200,335,580,230,'Changed state'),
                text(960,675,'System RoT: revalidate',54),paper(610,735,700,170,'Composition + policy'),
                text(960,1005,'Defined response required',50)]
    return svg(out)

"""M1S3: partitioning exposes mutual expectations; reuse needs review."""
from .fcsa_helpers import *
KEY='M1S3'
DURATION=timing(KEY)[0]
POSTER_SECONDS=DURATION-1


def pair(gap=180):
    left,right=410-gap/2,960+gap/2
    return [unit(left,350,550,350,'Compute'),unit(right,350,550,350,'System resources\n+ control')],left,right


def render(t):
    i,p=scene(t,KEY); out=[]
    if i==0:
        q=phase(p,.18,.7)
        out+=title('One system, new boundaries')
        objs,a,b=pair(180*q);out+=objs
        # The adjacent units separate; their functional relation remains visible.
        if q>0:out.append(line(a+550,525,b,525,GRAY,6))
        out.append(open_scope(a,b+550,825,'Shared system behavior'))
        return svg(out)
    if i in (1,2):
        objs,a,b=pair();out+=objs
        out.append(line(a+550,525,b,525,GRAY,7))
        if i==1:
            out+=title('A connection leaves questions')
            for x,label in [(300,'Provides?'),(760,'Expects?'),(1220,'Behavior?')]:
                out.append(tag(x,770,label,400))
        else:
            out+=title('Make expectations explicit')
            out.append(open_scope(320,1600,775,'Roles + interfaces'))
            # Selective second detail is readable, rather than tiny layer cards.
            if p>.38:
                out.append(text(960,975,'Protocol / transport: some mappings remain undefined',46))
        return svg(out)
    out+=title('New configuration','Same compute; review the new context')
    q=phase(p,.12,.6) if i==3 else 1
    x=lerp(320,240,q)
    out.append(unit(x,335,550,350,'Compute'))
    out.append(unit(1130,335,550,350,'Different\nsystem resources'))
    out.append(line(x+550,510,1130,510,GRAY,6,dash='15 12'))
    out.append(text(960,750,'Integration review',52))
    labels=['Roles','Interfaces','Product\nrequirements'] if i==4 else ['Roles?','Interfaces?']
    if i==3:
        out += [paper(465,815,450,170,labels[0]),paper(1005,815,450,170,labels[1])]
    else:
        for x,label in zip((160,730,1300),labels):out.append(paper(x,805,460,190,label))
    return svg(out)

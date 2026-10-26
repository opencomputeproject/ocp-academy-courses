"""M5S3: adaptation before crossing; capacity reviewed at aggregate scope."""
from .fcsa_helpers import *
KEY='M5S3';DURATION=timing(KEY)[0];POSTER_SECONDS=DURATION-1


def txn(x,y,w=420):
    # One abstract transaction, with no implied actual field layout or bit count.
    return paper(x-w/2,y-80,w,160,'Transaction',True)


def traffic():
    return [chip(140,335,700,400),chip(1120,335,660,400),text(490,425,'Source fabric',52),text(1450,425,'Target fabric',52),
            line(840,570,1120,570,GRAY,6),line(980,310,980,790,GRAY,5,dash='12 12'),text(980,880,'Interface',48)]


def demand(extra=False,p=1):
    out=[]
    xs=[270,820]+([lerp(1570,1370,phase(p,.15,.6))] if extra else [])
    for k,x in enumerate(xs):
        out += [unit(x-200,285,400,180,'Requester '+chr(65+k)),line(x,465,x,585,GRAY,5)]
    out.append(line(xs[0],585,max(960,xs[-1]),585,GRAY,5))
    out += [line(960,585,960,700,GRAY,5),unit(600,700,720,200,'Snoop filter'),text(960,225,'Coherent cache demand',50)]
    return out


def render(t):
    i,p=scene(t,KEY);out=[]
    if i==0:
        out+=title('Different interconnect properties')+traffic()
        out += [txn(lerp(390,590,phase(p,.15,.7)),570),text(960,1000,'Address-field or ID-field width, for example',46)]
    elif i==1:
        out+=title('Adapt before transfer','Protocol-defined adaptation')+traffic()
        # A source-local adaptation seam, visibly BEFORE the interface at x980.
        out.append(line(780,455,780,700,GREEN,6))
        q=phase(p,.4,.85);x=lerp(500,1450,q)
        w=lerp(420,470,phase(p,.12,.35))
        out.append(txn(x,570,w))
        out.append(text(960,1000,'Preserve required protocol behavior',48))
    elif i==2:
        out+=title('Requirements need design evidence')+traffic()
        out += [txn(1450,570,470),paper(160,805,680,180,'Transmission + reception'),paper(1110,805,650,180,'Required performance')]
    elif i==3:
        out+=title('Scale review')+demand(p>=.28, max(0,(p-.28)/.72))
        out.append(text(960,1000,'Combined demand: review the expanded scope',46))
    else:
        out+=title('Two distinct system checks')
        out += [text(960,330,'Adapt before the interface',54),text(960,430,'Level 1',50),
                line(210,505,1710,505,GRAY,4),text(960,650,'Combined snoop-filter demand',54),text(960,750,'Full',50),
                paper(520,845,880,170,'Capacity evidence needed')]
    return svg(out)

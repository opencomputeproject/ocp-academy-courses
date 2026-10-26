"""M2S3: compare functional responsibilities, not physical tile count."""
from .fcsa_helpers import *
KEY='M2S3'; DURATION=timing(KEY)[0]; POSTER_SECONDS=DURATION-1


def split_view(optional=False):
    out=[chip(170,310,680,420),chip(1070,310,680,420),text(510,395,'Compute 1',54),text(1410,395,'Hub',54),
         role(235,505,'Application processing'),role(1135,505,'Memory + I/O access'),role(1135,610,'Primary coordination'),
         line(850,550,1070,550,GRAY,6)]
    if optional:
        out += [text(510,625,'May also have memory',46),line(510,730,510,825,GRAY,5,dash='13 11'),nvm(300,825,'Memory')]
    else:
        out += [line(1410,730,1410,825,GRAY,5),nvm(1200,825,'Memory')]
    return out


def render(t):
    i,p=scene(t,KEY)
    if i==0:
        out=title('Required architectural roles')
        out += [unit(170,330,680,400,'Compute 1'),unit(1070,330,680,400,'Hub'),
                open_scope(170,1750,815,'One or more of each')]
    elif i==1:
        out=title('Compute & Hub')+split_view()
        if .15<p<.65:out.append(pulse(850,550,1070,550,phase(p,.15,.65)))
    elif i==2:
        out=title('Compare: Compute Tile')
        out += [chip(160,320,760,505),text(540,410,'Compute 2 · primary',52),
                role(225,525,'Application processing'),role(225,630,'Memory + I/O access'),role(225,735,'Primary coordination')]
        # A second instance enters only after the multi-chiplet narration.
        q=phase(p,.50,.78)
        if p>=.5:
            x=lerp(1200,1120,q)
            out += [unit(x,340,620,260,'Compute 2'),line(920,470,x,470,GRAY,5)]
        out += [line(540,825,540,900,GRAY,5),text(540,980,'Direct memory access',48)]
    elif i==3:
        out=title('Roles do not exclude all extra capabilities')+split_view(True)
        out.append(text(1410,905,'Multiple types possible',46))
    else:
        out=title('Classify functions and interfaces')
        out += [text(200,330,'Compute & Hub',52,anchor='start'),
                unit(180,400,660,200,'Compute 1'),unit(1080,400,660,200,'Hub'),
                text(510,685,'Application processing',48),text(1410,685,'Resource access',48),
                line(180,740,1740,740,GRAY,4),
                text(200,855,'Compute Tile',52,anchor='start'),
                text(1180,850,'Compute 2',54),text(1180,950,'Processing + resource access',48)]
    return svg(out)

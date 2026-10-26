"""M3S5: second-stage image routes and directional sequence control."""
from .fcsa_helpers import *
KEY='M3S5'; DURATION=timing(KEY)[0]; POSTER_SECONDS=DURATION-1


def components():
    return [chip(150,505,650,300),chip(1120,505,650,300),text(475,750,'Manager component',48),text(1445,750,'Subordinate component',48)]


def image_at(cx,cy,label='Image'):
    return paper(cx-140,cy-75,280,150,label,True)


def route_image(p,points,label="Image B"):
    n=len(points)-1; q=min(n-.000001,max(0,p*n)); k=int(q); f=q-k
    if p>=1:k=n-1;f=1
    x,y=points[k];xx,yy=points[k+1]
    return image_at(lerp(x,xx,f),lerp(y,yy,f), label if p>=.999 else "")


def render(t):
    i,p=scene(t,KEY);out=[]
    if i<3:
        names=['Distributed','Shared','Independent'];out+=title('Compare: '+names[i],'Second-stage image loading')
        out+=components()
        if i==0:
            out.append(nvm(265,260,w=420))
            out += [line(330,405,330,505,GRAY,5),line(630,405,630,505,GRAY,5)]
            out.append(line(800,600,1120,600,GRAY,5))
            q=phase(p,.1,.4)
            out.append(image_at(330,lerp(350,600,q),'Image A' if q>=.999 else ''))
            if p>=.42:
                out.append(route_image(phase(p,.42,.87),[(630,350),(630,600),(1445,600)]))
            out.append(text(960,950,'Manager loads the subordinate image',48))
        elif i==1:
            out.append(nvm(750,260,'Shared NVM'))
            out.append(path('M750 335 H475 V505',GRAY,5))
            out.append(path('M1170 335 H1445 V505',GRAY,5))
            out.append(route_image(phase(p,.12,.4),[(960,335),(475,335),(475,600)],'Image A'))
            if p>=.48:out.append(route_image(phase(p,.48,.8),[(960,335),(1445,335),(1445,600)]))
            out.append(text(960,950,'Each fetches its own image',50))
        else:
            out += [nvm(265,260,'NVM A'),nvm(1235,260,'NVM B'),line(475,405,475,505,GRAY,5),line(1445,405,1445,505,GRAY,5)]
            q=phase(p,.12,.6)
            out += [image_at(475,lerp(350,600,q),'Image A' if q>=.999 else ''),image_at(1445,lerp(350,600,q),'Image B' if q>=.999 else '')]
            out.append(open_scope(475,1445,870,'Synchronize'))
        if i==0:out.append(nvm(265,260,w=420))
        elif i==1:out.append(nvm(750,260,'Shared NVM'))
        else:out += [nvm(265,260,'NVM A'),nvm(1235,260,'NVM B')]
        return svg(out)
    if i in (3,4):
        out+=title('Sequence-control view' if i==3 else 'Comparison: error case','Second-stage scope')
        # Narrower named components leave ample space for complete signal names.
        out += [unit(110,350,460,460,'Manager'),unit(1350,350,460,460,'Subordinate')]
        if i==3:
            out += [text(960,390,'Ready to proceed',50),arrow(1350,440,570,440,GRAY,6,20),
                    text(960,625,'Proceed',50),arrow(570,675,1350,675,GRAY,6,20),
                    text(960,960,'Loading, execution or synchronization',48)]
            if .12<p<.45:out.append(pulse(1350,440,570,440,phase(p,.12,.45)))
            if .55<p<.85:out.append(pulse(570,675,1350,675,phase(p,.55,.85)))
        else:
            out += [text(960,400,'Error',54),arrow(1350,450,570,450,GRAY,6,20),
                    text(960,650,'Load / verify issue',50),text(960,960,'Error does not grant permission',50)]
            if .15<p<.55:out.append(pulse(1350,450,570,450,phase(p,.15,.55)))
        return svg(out)
    out+=title('Image route and control are distinct','Second-stage scope')
    out += [text(280,340,'Image route',54,anchor='start'),
            text(960,455,'Manager · Shared NVM · Separate NVMs',48),
            line(180,515,1740,515,GRAY,4),text(280,600,'Sequence control',54,anchor='start'),
            unit(150,650,500,350,'Manager'),unit(1270,650,500,350,'Subordinate'),
            text(960,700,'Ready / Error',48),arrow(1270,750,650,750,GRAY,5,18),
            text(960,900,'Proceed',48),arrow(650,950,1270,950,GRAY,5,18)]
    return svg(out)

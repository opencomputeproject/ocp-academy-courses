"""Original vector illustrations and cue-based motion for OCP Market Impact."""
from html import escape
from math import cos, sin, pi
import re
PAPER='#F6F8F3'; WHITE='#FFFFFF'; INK='#182B36'; INDIGO='#343895'; BLUE='#5C62AC'
GREEN='#8DC63F'; TEAL='#14766F'; MINT='#CFE3D4'; GRID='#DCE5DC'; SUB='#405963'; AMBER='#AE692C'

def txt(x,y,s,size=22,fill=INK,weight=550,align='start'):
    return f'<text x="{x}" y="{y}" font-family="Helvetica Neue, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{align}">{escape(str(s))}</text>'
def box(x,y,w,h,fill=WHITE,stroke='none',r=10,sw=2):
    return f'<rect x="{x}" y="{y}" width="{max(w,0):.2f}" height="{max(h,0):.2f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def path(d,stroke=INK,sw=3,fill='none',extra=''):
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def line(x,y,a,b,color=INK,sw=3):
    return path(f'M{x} {y}L{a} {b}',color,sw)
def circle(x,y,r,fill,stroke='none',sw=2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def group(body,x=0,y=0,k=1,o=1):
    if o<=0:return ''
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({k})" opacity="{min(o,1):.3f}">{body}</g>'
def frame(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 960 540">{box(0,0,960,540,PAPER,r=0)}<defs><pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{GRID}"/></pattern></defs>{box(0,0,960,540,"url(#grid)",r=0)}{body}</svg>'
def title(label,sub):
    # Align the rule with the title's capitals and the subtitle's descenders.
    title_top = 29.25
    subtitle_bottom = 84.5
    rule = box(38, title_top, 7, subtitle_bottom - title_top, GREEN, r=3)
    return box(0,0,960,108,WHITE,r=0)+box(0,106,960,2,GRID,r=0)+rule+txt(62,51,label,30,INK,700)+txt(62,81,sub,18,SUB,450)
def foot(s):
    return box(0,476,960,64,'#E8EFE7',r=0)+txt(40,516,s,22,INK,600)
def building(x,y,k=1,variant=0):
    w=108+variant*8
    a=path(f'M0 27 L33 8 L{w+30} 8 L{w} 27 Z',INK,2,MINT)
    a+=path(f'M{w} 27 L{w+30} 8 L{w+30} 70 L{w} 89 Z',INK,2,'#A4BCBF')+box(0,27,w,62,WHITE,INK,r=0)
    for j in range(4):a+=box(8+j*22,42,14,10,'#668785',r=1)+box(8+j*22,60,14,12,'#BECFC9',r=1)
    a+=box(w-18,61,10,28,TEAL,r=1)
    return group(a,x,y,k)
def rack(x,y,k=1,wide=False,drawer=0):
    w=122 if wide else 101
    a=path(f'M0 8 L16 -4 L{w+16} -4 L{w} 8 Z',INDIGO,2,'#CDD1E8')+path(f'M{w} 8 L{w+16} -4 L{w+16} 165 L{w} 179 Z',INK,2,'#657587')
    a+=box(0,8,w,172,INK,INDIGO,r=3)+box(7,15,w-14,156,'#DFE7E4',r=2)
    for j in range(9):
        dx=drawer*23 if j==4 else 0; yy=23+j*15.5
        a+=box(13-dx,yy+dx*.25,w-26,12,WHITE,TEAL if j==4 else '#718488',r=2,sw=1.3)
        a+=box(20-dx,yy+4+dx*.25,w-53,2.2,MINT,r=1)+circle(w-24-dx,yy+6+dx*.25,2,GREEN if j%2 else TEAL)
    return group(a,x,y,k)
def people(x,y,k=1):
    a=box(-64,-32,128,70,'#D6E0D9',SUB,r=25)
    for xx,yy in [(-33,-51),(27,-51),(-32,57),(29,57),(-86,4)]:
        a+=circle(xx,yy,11,TEAL)+circle(xx,yy-2,5,'#B5E2CB')
    a+=circle(88,4,13,WHITE,INDIGO,3)
    return group(a,x,y,k)
def curve(d,p,color=TEAL):
    guide=path(d,GRID,8)
    if p<=0:return guide
    if p>=1:return guide+path(d,color,6)
    # These routes run left to right. A moving SVG clip works in the browser
    # and in the offline rasterizer, including on the long regional fiber runs.
    coords=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',d)]
    start=coords[0]
    end=coords[-1] if 'H' in d else coords[-2]
    clip='route'+str(int(start))+'x'+str(int(coords[1]))+'x'+str(int(end))
    mask=f'<defs><clipPath id="{clip}"><rect x="{start-5}" y="0" width="{(end-start+10)*p:.2f}" height="540"/></clipPath></defs>'
    return guide+mask+path(d,color,6,extra=f'clip-path="url(#{clip})"')
def plug(x,y,k=1,v=0):
    a=path('M-55 8H-15',TEAL,14)+box(-16,-23,56,63,WHITE,INDIGO,r=7)+box(40,-13,19,9,TEAL,r=2)+box(40,17,19,9,TEAL,r=2)
    a+=path(f'M{159-v:.2f} 8h45',TEAL,14)+box(102-v,-24,58,66,'#D6E9D2',INDIGO,r=7)
    for yy in [-11,18]:a+=box(102-v,yy,14,7,INK,r=2)
    return group(a,x,y,k)
def factory(x,y,k=1):
    a=path('M0 92V28L32 9V28L62 9V28L93 9V39H113V-5H128V39H145V92Z',INK,2,WHITE)
    for i in range(5):a+=box(10+26*i,52,17,14,MINT,SUB,r=1,sw=1)
    a+=box(92,72,27,20,TEAL,r=1)
    return group(a,x,y,k)
def book(x,y,k=1,color=INDIGO):
    a=path('M0 4 Q20 -4 44 6 Q67 -4 87 4V57Q65 50 44 61Q19 52 0 57Z',color,3,WHITE)+line(44,8,44,59,color,2)
    for i in range(3):a+=line(8,15+i*10,34,19+i*10,MINT,3)+line(55,19+i*10,78,15+i*10,MINT,3)
    return group(a,x,y,k)
def smooth(t):t=min(1,max(0,t));return t*t*(3-2*t)

CUES={
 1:['At Meta','More than thirty','Now picture','Forty-four hundred','seven thousand','Nearly eleven','fifteen thousand','one seat'],
 3:['In twenty twenty-three','A year later','seventy-three and a half','Now move','two hundred ninety-five','Make your guess.','About eight hundred billion','two point seven','One year further'],
 5:['Lisa Su','They used Open Rack Wide','power shelves','Now look at a different rack','Watch the tray','A buyer and a technician','The technician wants'],
 6:['Inside one building','another building','regional network','Follow the light','specify the fiber','Bloomberg Intelligence','second shopping list'],
 7:['room for another rack','A second supplier','example of a connector','Follow the power path','a drawing gives','actually been tested','I D C describes'],
 9:['camera above','crooked cap','One path leads','The other leads','little more distance','who will service','This is inference','three fronts','wherever inference'],
 11:['October Summit','six thousand','thirty thousand','By November','eight thousand','forty thousand','If the rack examples','Introduction to Liquid Cooling']
}

def artwork(n,time,cues,inventory=False):
    c=lambda i,d=1.15:smooth((time-cues[i])/d)
    def fade(i,body,d=1):return group(body,o=c(i,d))
    def scene(i,body,j=None):return group(body,o=c(i)*(1-c(j) if j is not None else 1))
    a=''
    if n==1:
        a+=title('How many roofs?','Prometheus and the people behind open infrastructure')
        campus=building(190,225,1.65)
        for x,y,k in [(475,180,1.08),(610,267,1.3),(390,322,.83)]:campus+=fade(1,building(x,y,k))
        a+=group(campus,o=1-c(2))
        chart=txt(64,165,'Global Summit attendance',26,INK,650)
        for j,(y,v,l) in enumerate([(2023,4401,'4,401'),(2024,7047,'7,047'),(2025,10835,'10,835'),(2026,15000,'15,000')]):
            h=182*v/15000*c(3+j); x=88+j*202
            chart+=line(x-10,409,x+130,409,SUB,2)+txt(x+60,445,y,20,SUB,600,'middle')
            if h>0:chart+=box(x,408-h,118,h,TEAL if j<3 else INDIGO,r=4)+txt(x+59,396-h,l,25,INK,700,'middle')
        a+=group(chart,o=c(2)*(1-c(7)))
        a+=scene(7,people(383,293,1.65)+txt(604,278,'An open seat',32,INK,700)+txt(604,316,'Who would you bring?',22,TEAL))
        a+=foot('One cluster brought together people from many disciplines.')
    if n==3:
        a+=title('What did IDC expect?','Forecast publication year and target spending year')
        early=txt(74,210,'2023',50,INDIGO,700)+txt(75,270,'Summit opening',28)+txt(75,318,'AI prompts a rethink of',23,SUB)+txt(75,348,'data center investment.',23,SUB)
        early+=fade(1,line(415,163,415,399,GRID,3)+txt(475,210,'2024 study',38,INDIGO,650)+txt(475,263,'Target year 2028',24,SUB)+fade(2,txt(475,358,'$73.5B',70,TEAL,700)))
        a+=group(early,o=1-c(3))
        bars=txt(65,156,'Annual spending forecast for 2029',25,INK,650)
        for j,(x,h,lbl,val) in enumerate([(220,77,'2025 study','$295B'),(515,208,'2026 study','≈ $800B')]):
            v=c(4 if j==0 else 6)
            bars+=txt(x+65,438,lbl,22,SUB,550,'middle')
            if v>0:bars+=box(x,398-h*v,134,h*v,TEAL if j==0 else INDIGO,r=3)+group(txt(x+67,383-h*v,val,27,INK,700,'middle'),o=v)
        bars+=line(93,399,870,399,SUB,2)+txt(66,405,'$0',16,SUB)+fade(7,txt(765,248,'2.7×',47,TEAL,700,'middle')+txt(765,278,'prior estimate',17,SUB,500,'middle'))
        a+=group(bars,o=c(3)*(1-c(8)))
        horizon=txt(68,180,'Beyond 2029',27,INK,650)+txt(70,299,'$892B',72,INDIGO,700)+txt(72,343,'IDC forecast for 2030',26,SUB)
        horizon+=line(455,182,455,372,GRID,3)+txt(505,274,'About 51%',50,TEAL,700)+txt(505,319,'of spending across the',23,SUB)+txt(505,352,'categories IDC measures',23,SUB)
        a+=scene(8,horizon)
        footer='Publication year and spending year are shown separately.' if time<cues[3] else 'Both bars estimate the same year. Values in US dollars.' if time<cues[8] else 'For 2029, IDC raised its forecast from $295B to about $800B.'
        a+=foot(footer)
    if n==5:
        a+=title('Two rack designs','What the shared details let other teams inspect')
        a+=box(43,138,420,309,WHITE,GRID)+box(498,138,420,309,WHITE,GRID)
        a+=txt(66,177,'AMD Helios',26,INK,700)+rack(87,221,1.05,True)+fade(1,txt(263,278,'Open Rack',24,INDIGO,650)+txt(263,310,'Wide',24,INDIGO,650))+fade(2,txt(263,357,'Power shelves',18,SUB))
        a+=fade(3,txt(522,177,'NVIDIA MGX 1.2',26,INK,700)+rack(563,220,1.05,False,c(4))+txt(709,286,'Rack and',23,INDIGO,650)+txt(709,316,'tray design',23,INDIGO,650))
        a+=foot('A buyer can compare an interface. A technician can inspect the service path.')
    if n==6:
        a+=title('One training job across buildings','An illustrative map of the regional network Meta described')
        a+=building(95,211,1.16)+fade(1,building(315,147,.92)+building(326,329,.86))
        a+=fade(2,building(703,162,1.1)+building(724,321,.9))
        a+=curve('M195 319 Q237 340 288 296 L467 296',c(3),TEAL)+curve('M413 236 Q449 249 468 292',c(3),TEAL)+curve('M420 358 Q447 350 468 297',c(3),TEAL)
        a+=fade(2,circle(489,295,19,INDIGO)+txt(489,301,'N',17,WHITE,700,'middle'))
        a+=curve('M511 295 C602 295 624 252 704 242',c(4),INDIGO)+curve('M511 295 C608 308 642 367 723 374',c(4),INDIGO)
        a+=fade(5,txt(549,451,'Fiber   /   Switching   /   Resilience',22,TEAL,650))
        a+=foot('Follow the links. Each one adds equipment and operating decisions.')
    if n==7:
        a+=title('Where two suppliers meet','Facility power, a rack, and the interface between them')
        a+=factory(80,248,1.13)+txt(150,405,'Facility',22,SUB,600,'middle')
        a+=rack(736,180,1.1,False)+txt(796,405,'Rack',22,SUB,600,'middle')
        a+=curve('M249 311H360',c(3))+curve('M615 311H722',c(3))+plug(409,305,1,30*c(4))
        a+=fade(2,txt(494,207,'Shared interface',26,INDIGO,650,'middle'))+fade(4,txt(471,402,'Check the drawing',20,TEAL,600,'middle'))+fade(5,txt(471,432,'Ask about tested combinations',18,SUB,450,'middle'))
        a+=foot('A shared drawing gives buyers a place to start checking alternatives.')
    if n==9:
        a+=title('Where should the model run?','An illustrative inspection on a factory line')
        # The opening depicts the actual object of the camera inspection.
        line_art=box(134,347,668,32,WHITE,SUB,r=15)+line(168,363,771,363,TEAL,3)
        for x in [176,289,403,517,631,756]:
            line_art+=circle(x,363,7,WHITE,SUB,2)
        line_art+=path('M561 219V153H467V181',SUB,6)+box(428,174,71,33,INDIGO,r=5)+circle(463,214,13,TEAL)+txt(578,176,'Inspection camera',22,INDIGO,650)
        def bottle(bx,tilt):
            return group(path('M-23 0V-57Q-23 -67 -11 -76V-87H11V-76Q23 -67 23 -57V0Z',TEAL,3,'#D5E8DF')+f'<g transform="rotate({tilt} 0 -88)">{box(-15,-96,30,11,INDIGO,r=2)}</g>',bx,345)
        shift=66*c(1,1.2)
        for bx,tilt in [(254,0),(394,-17),(534,0),(674,0)]:
            line_art+=bottle(bx+shift,tilt)
        line_art+=fade(1,path('M439 237L460 246L483 235',AMBER,3)+txt(171,423,'A crooked cap. How soon does the line need an answer?',23,INK,600))
        a+=group(line_art,o=1-c(2))
        engine=factory(75,235,1.0)+txt(146,370,'Factory camera',20,INK,650,'middle')
        engine+=curve('M227 290 C365 290 365 203 510 203',c(2))+curve('M227 290 C368 290 432 378 635 378',c(3),INDIGO)
        a+=fade(2,engine)
        a+=fade(2,box(512,163,300,79,WHITE,TEAL)+txt(540,211,'On-site computer',25,TEAL,650))
        a+=fade(3,box(634,338,276,79,WHITE,INDIGO)+txt(658,385,'Remote data center',23,INDIGO,650))
        a+=fade(4,txt(298,201,'Response time',19,TEAL))+fade(5,txt(327,389,'Who maintains it?',19,SUB))
        a+=foot('A deadline, a footprint and a maintenance plan shape the choice.')
    if n==11:
        a+=title('One year of OCP Academy','Two snapshots of the community learning together')
        for i,(x,tag,count,hours) in enumerate([(48,'October · Summit','Over 6,000','Over 30,000'),(493,'November · update','Over 8,000','Almost 40,000')]):
            cards=box(x,144,419,298,WHITE,GRID)+box(x+18,159,6,39,GREEN if i else TEAL,r=2)+txt(x+39,189,tag,25,INK,700)
            cards+=fade(4 if i else 1,txt(x+35,269,count,43,INDIGO,700)+txt(x+36,296,'users' if i else 'registered learners',18,SUB))
            cards+=fade(5 if i else 2,txt(x+35,364,hours,39,TEAL,700)+txt(x+36,393,'learner hours',18,SUB))
            a+=group(cards,o=(c(3) if i else 1)*(1-c(6)))
        subjects=txt(58,159,'Data Center Technologies catalog',26,INK,650)
        subjects+=box(55,185,403,241,WHITE,GRID)+rack(87,222,.77,True)+txt(215,282,'Open Rack',28,INDIGO,700)+txt(215,324,'Power and cooling',18,SUB)
        cooling=box(490,185,413,241,WHITE,GRID)+path('M585 219C577 242 548 268 548 290C548 339 620 339 620 290C620 269 597 240 585 219Z',TEAL,4,MINT)+txt(643,276,'Introduction to',22,SUB)+txt(643,312,'Liquid Cooling',26,INDIGO,700)
        subjects+=fade(7,cooling)
        a+=fade(6,subjects)
        a+=foot('Explore Open Rack and Introduction to Liquid Cooling in the technology catalog.')
    return frame(a)

"""M2S4. Source crops, drawn teaching sections, and narration-aligned cuts.

The EIA diagram is an illustrative cross-section, not a drawing of Google's
unspecified kit parts. Front geometry: 706.2 mm outside the frame, 482.6 mm
across a standard equipment panel, 465.1 mm between fastener centers.
"""
from pathlib import Path
from functools import lru_cache
from PIL import Image

HERE=Path(__file__).resolve().parent
CROPS={
    # Bounds on a 719×930 preview of each entire page, before resizing.
    'wall':('google-orv3',16,(168,239,534,498)),
    'stop':('google-orv3',9,(218,118,520,320)),
    'ortray':('orv3-it-guide',5,(83,275,698,483)),
}
CUES=['the mounting ears','Google’s contributed frame','21-inch equipment','19-inch EIA hardware',
      'turn the view','a cord inlet instead','standard and extended depth','front panel and handle',
      'a rear support','distance to that rear support','no such rear support','power interface and intended supply']
@lru_cache(None)
def crop(key):
    if key=='contact':return Image.open(HERE.parent/'figures/m1s3-connector-detail.png').convert('RGB')
    # Reviewed source crops; CROPS records the PDF, viewer page and bounds.
    with Image.open(HERE/'source-plates'/(key+'.png')) as img:
        return img.convert('RGB')

def draw(r,im,k,f):
    # Coordinates on a 960×540 teaching canvas, rasterized at 2×.
    ink='#253e4b'; steel='#536875'; navy='#145a78'; sky='#d5e8ee'
    green='#387044'; mint='#c4e0b7'; pale='#e6edef'; soft='#f3f6f7'
    def t(x,y,s,n=20,c=ink,b=False):r.txt(x,y,s,n,c,b)
    def box(x,y,w,h,fill,stroke=None):r.box(x,y,w,h,fill,stroke,0)
    def ln(x1,y1,x2,y2,c=steel,w=2):r.line([(x1,y1),(x2,y2)],c,w)
    def art(key,x,y,w,h):
        orig=crop(key); scale=min(w*2/orig.width,h*2/orig.height)
        a=orig.resize((round(orig.width*scale),round(orig.height*scale)),Image.Resampling.LANCZOS)
        im.paste(a,(round(x*2+(w*2-a.width)/2),round(y*2+(h*2-a.height)/2)))
    def label(x,y,s):t(x,y,s,16,steel,True)
    def lines(x,y,rows):
        for i,line in enumerate(rows):t(x,y+36*i,line,22)
    def rule(x1,x2,y,col):
        ln(x1,y,x2,y,col);ln(x1,y-8,x1,y+8,col);ln(x2,y-8,x2,y+8,col)
    def ear(x,y,w=30,h=60,fast=True):
        box(x,y,w,h,mint,green)
        # Bolt center on the mating rail, not on an empty gap.
        if fast:
            cx=x+w/2;cy=y+h/2;r.d.ellipse(r.xy([(cx-4,cy-4),(cx+4,cy+4)]),fill=ink)
    def front(x,y,wide,installed):
        # Crop one height band. Keep the frame, unloaded opening, and horizontal scale identical.
        mid=x+251; factor=502/706.2; rail=465.1/2*factor
        span=(533 if wide else 482.6)*factor; body=(span if wide else 444*factor)
        l=mid-body/2; rr=mid+body/2
        for xx in (x,x+490):box(xx,y,12,143,steel)
        if wide:
            for a,b in [(x+12,l+18),(rr-18,x+490)]:
                box(a,y+87,b-a,12,green)
            box(l,y+31,body,56,sky,navy)
        else:
            for a,b in [(x+12,mid-rail+6),(mid+rail-6,x+490)]:
                box(a,y+59,b-a,12,green)
            for cx in (mid-rail,mid+rail):box(cx-6,y+8,12,126,steel)
            if installed:
                lft=mid-span/2;end=mid+span/2;box(l,y+36,body,61,sky,navy)
                for a,b,cx in [(lft,l,mid-rail),(rr,end,mid+rail)]:
                    box(a,y+36,b-a,61,mint,green)
                    r.d.ellipse(r.xy([(cx-3,y+64),(cx+3,y+70)]),fill=ink)
        for xx in range(4):
            ln(l+34+xx*12,y+48,l+34+xx*12,y+72,navy,2)
    def bars(values,names,maxv):
        x=86
        label_x=x+20  # Inset the row names; the measurement bars still start at the axis.
        for i,(val,name) in enumerate(zip(values,names)):
            y=186+i*126
            t(label_x,y-47,name,23,ink,True)
            box(x,y,518*val/maxv,17,navy if i==0 else green)
            t(x+535,y-10,f'{val:g} mm',23,ink,True)
        ln(x,172,x,350,steel,2)
    def side(rear,extended=False):
        x,y=107,180;end=500 if extended else 418
        for xx in (x,end):box(xx-7,y-24,14,183,steel)
        box(x+8,y+37,310,61,sky,navy);box(x-11,y+28,19,78,mint,green)
        if rear:box(404,y+82,21,32,mint,green)
        return x,end
    if k in (0,1):
        label(60,68,'EIA INSTRUMENT  /  FRONT')
        # Standalone panel with enlarged readable end details; dimension line ends at ear tips.
        x,y=72,205; w=493;ew=18
        box(x+ew,y,w-2*ew,81,sky,navy)
        for a in (x,x+w-ew):ear(a,y,ew,81,True)
        for i in range(13):ln(147+i*10,229,147+i*10,256,navy,2)
        rule(x,x+w,168,navy);t(197,115,'19 in  /  482.6 mm',25,navy,True)
        if k==1:
            for a in (x+ew/2,x+w-ew/2):
                r.d.ellipse(r.xy([(a-13,y+27),(a+13,y+53)]),outline=green,width=5)
        t(603,182,'Mounting ears' if k else 'Front-panel width',26,ink,True)
        lines(603,238,['The bolt passes','through the ear','into the rack rail.'] if k else ['Measure from the','outside of one ear','to the other.'])
        t(72,382,'The chassis body is narrower than the front panel.',22)
    elif k==2:
        label(52,49,'INSIDE THE GOOGLE FRAME');art('wall',40,110,515,358)
        t(578,151,'The rack side',28,ink,True)
        lines(578,216,['Threads and cutouts','provide mounting','points inside the frame.'])
        t(578,363,'Figure 8 · inside wall',18,steel)
    elif k==3:
        label(52,51,'21-INCH OPEN RACK FORMAT')
        art('ortray',55,112,848,286)
        t(74,426,'The kit supports an Open Rack tray at OpenU positions.',23,ink,True)
    elif k==4:
        label(53,46,'TWO ALTERNATIVE FRONT SECTIONS  /  SAME GOOGLE FRAME')
        front(70,105,True,True);front(70,293,False,True)
        t(603,135,'21-inch Open Rack',24,ink,True);lines(603,182,['Tray rests on supports.'])
        t(603,315,'19-inch EIA',24,ink,True);lines(603,359,['Ears bolt to rails','inside the frame.'])
        t(70,468,'Mounting hardware is schematic; the outside frame width stays fixed.',17,steel)
    elif k in (5,6):
        label(52,54,'REAR POWER INTERFACE')
        if k==5:
            art('stop',46,110,500,322)
            t(573,121,'Stop and contact',27,ink,True)
            lines(573,187,['The shelf stop and the','busbar have distinct','reference positions.'])
            t(573,341,'Source detail shows an ORv2',17,steel);t(573,368,'busbar in the Google frame.',17,steel)
        else:
            art('contact',63,110,438,325)
            t(544,130,'Blind-mate or cord?',26,ink,True)
            lines(544,200,['This clip mates with a busbar.','A device with a cord inlet','still needs a cord and supply.'])
            t(64,458,'Tray-side clip at left; fixed busbar at right.',18,steel)
    elif k==7:
        label(64,63,'SIDE VIEW  /  EIA RAIL DEPTH');bars([586.15,742.95],['Standard depth','Extended depth'],742.95)
        t(86,421,'Two rail-depth options for the Google frame.',23,ink,True)
    elif k==8:
        label(64,63,'SIDE VIEW  /  TRAY DEPTH');bars([613,635],['To the front panel','To the handle'],635)
        t(86,421,'The handle projects beyond the front panel.',23,ink,True)
    elif k in (9,10,11):
        label(52,58,'EXAMPLE INSTRUMENT  /  SIDE VIEW')
        x,end=side(k!=11,False)
        if k==10:
            # Overlay the alternative rear rail at its longer distance, not a second device mount.
            alt=end+84*f
            for y in range(149,343,18):ln(alt,y,alt,y+8,green,3)
            rule(end,alt,355,green)
        t(562,153,['Front and rear support','Same front ears','Front-mounted example'][k-9],24,ink,True)
        lines(562,213,[['The ears fasten at the front.','This device also has a','rear attachment.'],['An extended rear rail sits','farther back. The device’s','rear attachment must reach.'],['Rear support is device-','specific. This example has','only front mounting ears.']][k-9])
        t(75,420,['Side view shows the support the front view hides.','Dashed line: alternative rear rail position.','Use the mounting arrangement specified for the device.'][k-9],21)
    else:
        label(62,67,'TWO SEPARATE QUESTIONS')
        front(62,117,False,True);art('contact',635,96,218,167)
        t(63,310,'How does it mount?',28,navy,True);t(557,310,'How does it get power?',28,green,True)
        lines(63,365,['Match the ears and supports','to the installed kit.'])
        lines(557,365,['Match the device inlet','to its intended supply.'])

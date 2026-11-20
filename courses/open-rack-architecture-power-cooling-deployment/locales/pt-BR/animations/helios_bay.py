"""Illustrative cutaway, not an HPE production drawing or slot map."""
def draw(r,k,f):
    # Orthographic cut through one bay. Positive z runs towards the rear;
    # every part of the tray moves along that one axis as it withdraws.
    def p(x,y,z): return (130+x+.47*z,355-y-.37*z)
    def face(points,fill,stroke):r.poly([p(*q) for q in points],fill,stroke)
    def solid(x,y,z,w,h,d,front,top,side):
        def q(a,b,c):return (x+a,y+b,z+c)
        face([q(w,0,0),q(w,0,d),q(w,h,d),q(w,h,0)],side,side)
        face([q(0,h,0),q(w,h,0),q(w,h,d),q(0,h,d)],top,side)
        face([q(0,0,0),q(w,0,0),q(w,h,0),q(0,h,0)],front,side)
    steel=('#b2c4cd','#dbe5e9','#8097a3')
    rail=('#087a70','#88d4c1','#216d62')
    for z in [225,0]:
        for x in [0,326]:solid(x,-68,z,13,166,12,*steel)
        solid(0,-66,z,339,11,12,*steel)
    for x in [0,326]:solid(x,-66,0,13,11,237,*steel)
    for x in [9,306]:solid(x,-7,0,24,7,232,*rail)
    if k:
        z=3-(130*f if k==2 else 130 if k>2 else 0)
        solid(14,0,z,311,13,225,'#596d7e','#d5e0e5','#526575')
        # Four GPU positions with cold plates, not a physical tubing layout.
        for dz in [30,126]:
            for dx in [44,179]:
                solid(dx,13,z+dz,87,4,62,'#384e61','#78909c','#384e61')
                solid(dx+8,17,z+dz+5,71,6,51,'#a87649','#e9c59a','#886340')
                for j in range(4):
                    r.line([p(dx+20+j*12,23,z+dz+12),p(dx+20+j*12,23,z+dz+48)],'#ba936b',1)
        for dx in [38,271]:solid(dx,3,z-3,28,5,3,'#d8e4e8','#e5f0f0','#7f959c')
    r.label(57,56,'ONE EQUIPMENT BAY   /   SCHEMATIC CUTAWAY')
    r.txt(590,115,'Open Rack Wide',26,r.INK,True)
    r.txt(590,154,'Double-wide equipment bay',18,r.GRAY)
    if k:
        r.txt(590,222,'AMD Helios',26,r.INK,True)
        r.txt(590,261,'Four GPUs on one tray',18,r.GRAY)
    if k>=3:
        r.txt(590,329,'HPE implementation',25,r.INK,True)
        r.txt(590,368,'Juniper scale-up switching',18,r.GRAY)
    x1,y1=p(13,-91,0);x2,y2=p(326,-91,0)
    r.line([(x1,y1-5),(x1,y1+4),(x2,y2+4),(x2,y2-5)],r.TEAL,2)
    r.txt(x1+59,y1+16,'Equipment opening',20,r.TEAL,True)

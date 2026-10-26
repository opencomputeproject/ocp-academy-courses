"""Check every 30 fps source frame for label overlap, bounds and box padding."""
from pathlib import Path
from PIL import ImageFont
import importlib,json,re,itertools,xml.etree.ElementTree as ET
from .produce import ITEMS,FPS,ROOT,AUDIT

def intersects(a,b):
    return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]

def uncovered(bounds,cover):
    """Visible rectangle fragments after a later opaque paper/die is painted."""
    if not intersects(bounds,cover):return [bounds]
    x1,y1,x2,y2=bounds;a,b,c,d=cover;out=[]
    if x1<a:out.append((x1,y1,a,y2))
    if x2>c:out.append((c,y1,x2,y2))
    left,right=max(x1,a),min(x2,c)
    if y1<b:out.append((left,y1,right,b))
    if y2>d:out.append((left,d,right,y2))
    return out

def main():
    fonts={};flags=[];count=0;minimum=999
    def font(size,weight):
        key=size,weight
        if key not in fonts:
            f=ImageFont.truetype(str(ROOT/'fonts/OpenSans[wdth,wght].ttf'),round(size))
            f.set_variation_by_axes([weight,100]);fonts[key]=f
        return fonts[key]
    for name,item in ITEMS.items():
        module=importlib.import_module(f'tools.synced_video.{name}')
        for frame in range(round(item['duration']*FPS)):
            t=frame/FPS;tree=ET.fromstring(module.render(t));texts=[];shapes=[]
            for index,node in enumerate(tree):
                if node.tag.endswith('}rect'):
                    x,y,w,h=[float(node.get(k,'0')) for k in ('x','y','width','height')]
                    if w<1900 and node.get('fill','none')!='none':shapes.append(((x,y,x+w,y+h),index))
                if node.tag.endswith('}path'):
                    match=re.fullmatch(r'M([-\d.]+) ([-\d.]+) H([-\d.]+) L([-\d.]+) ([-\d.]+) V([-\d.]+) H([-\d.]+) Z',node.get('d',''))
                    if match:
                        x,y,_,right,_,bottom,_=map(float,match.groups());shapes.append(((x,y,right,bottom),index))
                if not node.tag.endswith('}text'):continue
                size=float(node.get('font-size'));weight=float(node.get('font-weight'));f=font(size,weight)
                x=float(node.get('x'));y=float(node.get('y'));labels=[];bounds=[]
                for span in node:
                    y+=float(span.get('dy','0'));label=span.text or '';labels.append(label)
                    b=f.getbbox(label,anchor='ls');w=f.getlength(label);left=x-w/2
                    bounds.append((left+b[0],y+b[1],left+b[2],y+b[3]))
                b=(min(a[0] for a in bounds),min(a[1] for a in bounds),max(a[2] for a in bounds),max(a[3] for a in bounds))
                texts.append((b,' / '.join(labels),size,index))
            def flag(reason,labels):flags.append({'id':item['id'],'frame':frame,'seconds':t,'reason':reason,'labels':labels})
            visible=[]
            for b,label,size,index in texts:
                pieces=[b]
                for shape,painted in shapes:
                    if painted>index:pieces=[fragment for piece in pieces for fragment in uncovered(piece,shape)]
                visible.append((pieces,label))
            for (a,label),(b,other) in itertools.combinations(visible,2):
                if any(intersects(p,q) for p in a for q in b):flag('visible text overlap',[label,other])
            for b,label,size,index in texts:
                if b[0]<60 or b[1]<50 or b[2]>1860 or b[3]>1030:flag('frame bounds',[label])
                cx,cy=(b[0]+b[2])/2,(b[1]+b[3])/2
                containers=[(a,painted) for a,painted in shapes if painted<index and a[0]<cx<a[2] and a[1]<cy<a[3]]
                if containers:
                    # Use the text's frontmost painted owner; a paper sliding
                    # beneath it is not its container or a visible collision.
                    a,_=max(containers,key=lambda a:a[1])
                    gap=min(b[0]-a[0],b[1]-a[1],a[2]-b[2],a[3]-b[3])/size
                    minimum=min(minimum,gap)
                    if gap<.75-.01:flag(f'box clearance {gap:.3f}em',[label])
            count+=1
    result={'source_frames':count,'frames_per_second':FPS,'visibility_method':'Opaque die/document painter order; intended insertion under the shared paper is occluded. All frame bounds and label-to-own-container padding still checked.','minimum_label_box_clearance_em':minimum,'flags':flags}
    (AUDIT/'all-frame-source-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(count,'frames;',len(flags),'flags; minimum box clearance',round(minimum,3),'em')
    for flag in flags[:10]:print(flag)
    if flags:raise SystemExit(1)
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Rebuild translated artwork from reviewed labels, retaining canonical media.

Requires Pillow and ffmpeg/libx264. Set ACADEMY_MEDIA_FONT when the host does
not have Arial Unicode. Canonical course.json and English media are read-only.
The two intentionally cyclic, silent 6-second animations retain the approved
geometry and 44-unit flywheel arrows. Frames are drawn natively at 1920x1080,
then losslessly piped to ffmpeg; no intermediate JPEG or raster upscaling.
"""
from __future__ import annotations
import argparse,base64,hashlib,importlib.util,io,json,math,os,re,subprocess
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
FONT=os.environ.get('ACADEMY_MEDIA_FONT','/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
FONT_BOLD=FONT
GREEN='#8DC63F';BLUE='#343895';TEXT='#30313a';MUTED='#6b6c70'
SIZE=1.5
MEASURE=ImageDraw.Draw(Image.new('RGB',(1,1)))

def wrap(value,font,width):
    lines=[]
    for paragraph in value.split('\n'):
        cjk=bool(re.search('[\u3040-\u30ff\u3400-\u9fff]',paragraph))
        units=list(paragraph) if cjk else paragraph.split()
        separator='' if cjk else ' '
        line=''
        for unit in units:
            trial=line+separator+unit if line else unit
            if line and MEASURE.textlength(trial,font=font)>width:
                lines.append(line.strip());line=unit
            else:line=trial
        lines.append(line.strip())
    return lines

def layout(value,width,height,size,bold=True):
    for n in range(size,13,-1):
        f=ImageFont.truetype(FONT_BOLD if bold else FONT,n)
        lines=wrap(value,f,width-1.5*n)
        if len(lines)*n*1.22<=height-1.5*n and all(MEASURE.textlength(x,font=f)<=width-1.5*n for x in lines):
            return n,lines
    raise ValueError(f'Text does not fit {width}x{height}: {value}')

def svg_text(value,x,y,width,height,size=24,color=TEXT,weight='700',align='middle'):
    n,lines=layout(value,width,height,size)
    center=x+width/2 if align=='middle' else x+.75*n
    baseline=y+(height-len(lines)*n*1.22)/2+n
    spans=''.join(f'<tspan x="{center:g}" y="{baseline+i*n*1.22:g}">{escape(line)}</tspan>' for i,line in enumerate(lines))
    return f'<text data-fit-box="{x},{y},{width},{height}" text-anchor="{align}" font-size="{n}" font-weight="{weight}" fill="{color}">{spans}</text>'

def card(x,y,w,h,fill='#ffffff',stroke='#dfe3e8'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'

def arrow(x1,y1,x2,y2):
    # Shaft ends at the flat-back midpoint, triangle tip on target boundary.
    a=math.atan2(y2-y1,x2-x1);length=12
    bx=x2-math.cos(a)*length;by=y2-math.sin(a)*length
    px=-math.sin(a)*6;py=math.cos(a)*6
    return f'<path d="M{x1:g} {y1:g} L{bx:g} {by:g}" stroke="{GREEN}" stroke-width="5" fill="none"/><polygon class="arrowhead" points="{x2:g},{y2:g} {bx+px:g},{by+py:g} {bx-px:g},{by-py:g}" fill="{GREEN}"/>'

def svg_document(body,height,alt):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {height}" role="img" aria-labelledby="title"><title id="title">{escape(alt)}</title><rect class="bg" width="800" height="{height}" rx="28" fill="#fff"/><g font-family="Arial Unicode MS, Arial, sans-serif">{body}</g></svg>\n'

def containing_box(fragment,bounds):
    """Record the real containing shape separately from the text layout area."""
    import xml.etree.ElementTree as ET
    element=ET.fromstring(fragment)
    element.set('data-layout-box',element.get('data-fit-box'))
    element.set('data-fit-box',','.join(map(str,bounds)))
    return ET.tostring(element,encoding='unicode')

def static_figures(locale,labels,course):
    figures=locale/'figures'
    # Keep canonical icons and all approved checkmark geometry.
    src=(ROOT/'figures/trusted_community.svg').read_text()
    import xml.etree.ElementTree as ET
    ET.register_namespace('','http://www.w3.org/2000/svg')
    tree=ET.fromstring(src);ns='{http://www.w3.org/2000/svg}'
    tree.set('font-family','Arial Unicode MS, Arial, sans-serif')
    for parent in tree.iter():
        for child in list(parent):
            if child.tag in {ns+'text',ns+'title',ns+'desc'}:parent.remove(child)
    groups=[x for x in tree if x.tag==ns+'g']
    fragments=[svg_text(labels['trusted'][0],65,55,670,60,25,color='#6FA030',align='start'),
        svg_text(labels['trusted'][1],100,8,170,96,25,align='start'),
        svg_text(labels['trusted'][2],100,8,170,96,25,align='start'),
        svg_text(labels['trusted'][3],100,8,325,100,23,color='#ffffff',align='start'),
        svg_text(labels['trusted'][4],66,0,510,62,21,color=MUTED,align='start')]
    tree.insert(0,ET.fromstring(f'<title xmlns="http://www.w3.org/2000/svg" id="title">{escape(course[0][2]["alt"])}</title>'))
    heading=ET.fromstring('<g xmlns="http://www.w3.org/2000/svg">'+fragments[0]+'</g>')
    # The layout box reserves space beside each icon. Containment is measured
    # against the actual card/panel, rather than adding a second padding inset.
    heading[0].set('data-layout-box',heading[0].get('data-fit-box'))
    heading[0].set('data-fit-box','42,44,716,428')
    tree.append(heading)
    for group,fragment,bounds in zip(groups,fragments[1:],['0,0,276,112','0,0,276,112','0,0,430,116','0,0,584,62']):
        text=ET.fromstring(fragment);text.set('data-layout-box',text.get('data-fit-box'));text.set('data-fit-box',bounds);group.append(text)
    (figures/'trusted_community.svg').write_text(ET.tostring(tree,encoding='unicode')+'\n')

    body=''
    for i,label in enumerate(labels['listen']):
        y=34+112*i;fill=BLUE if i==4 else ('#f7fbf2' if i==0 else '#fff')
        body+=card(108,y,584,82,fill,GREEN if i==0 else '#dfe3e8')
        body+=f'<circle cx="157" cy="{y+41}" r="24" fill="{GREEN if i in (0,4) else BLUE}"/>'
        body+=svg_text(str(i+1),135,y+10,44,62,25,color='#fff')
        body+=svg_text(label,194,y,490,82,27,color='#fff' if i==4 else TEXT,align='start')
        if i<4:body+=arrow(400,y+82,400,y+112)
    (figures/'listen_first_sequence.svg').write_text(svg_document(body,600,course[0][4]['alt']))

    # Localized wrapper uses the original official logos without translating them.
    positions=[(38,80),(285,80),(532,80),(162,265),(410,265)]
    tiers=['Startup','Bronze','Silver','Gold','Platinum'];body=containing_box(svg_text(labels['membership'][0],30,5,740,65,26,color='#6FA030'),(0,0,800,510))
    for (x,y),tier in zip(positions,tiers):
        body+=card(x,y,230,160,'#fafafa')
        logo=ROOT/'scripts/membership-logos'/f'{tier.lower()}.png'
        data=base64.b64encode(logo.read_bytes()).decode()
        body+=f'<image href="data:image/png;base64,{data}" x="{x+20}" y="{y+12}" width="190" height="112"/>'
        body+=containing_box(svg_text(tier,x+10,y+119,210,40,22),(x,y,230,160))
    body+=svg_text(labels['membership'][1],25,430,750,70,22,color=BLUE)
    (figures/'membership_tiers.svg').write_text(svg_document(body,510,course[0][6]['alt']))

    body='';vals=labels['marketplace']
    for i,y in enumerate([20,180,340]):
        body+=card(100,y,600,116,BLUE if i==2 else ('#f7fbf2' if i==1 else '#fff'),GREEN if i==1 else '#dfe3e8')
        # Retain the same avatar / offering / provider visual roles.
        if i==0:
            body+=f'<circle cx="170" cy="{y+54}" r="28" fill="{BLUE}"/><circle cx="170" cy="{y+44}" r="9" fill="#fff"/><path d="M152 {y+74}q18-20 36 0" stroke="#fff" stroke-width="6" fill="none"/>'
        elif i==1:
            body+=f'<path d="M142 {y+44}h76v44h-76z" fill="{GREEN}"/><path d="M152 {y+34}h56l10 10h-76z" fill="#6FA030"/>'
        else:
            body+=f'<path d="M144 {y+34}h74v52h-74z" fill="#fff"/><path d="M156 {y+24}h50v18h-50z" fill="{GREEN}"/><path d="M161 {y+61}h16m10 0h16m-42 15h16m10 0h16" stroke="{BLUE}" stroke-width="5"/>'
        body+=containing_box(svg_text(vals[2*i],226,y+2,450,51,27,color='#fff' if i==2 else TEXT,align='start'),(100,y,600,116))
        body+=containing_box(svg_text(vals[2*i+1],226,y+45,450,69,20,color='#fff' if i==2 else MUTED,align='start'),(100,y,600,116))
        if i<2:body+=arrow(400,y+116,400,y+160)
    body+=svg_text(vals[6],30,472,740,65,21,color='#6FA030')
    (figures/'marketplace_referral.svg').write_text(svg_document(body,545,course[1][2]['alt']))

    vals=labels['academy'];body=''
    positions=[(58,40),(466,40),(466,330),(58,330)]
    for i,(x,y) in enumerate(positions):
        body+=card(x,y,276,175,BLUE if i==1 else ('#f7fbf2' if i==0 else '#fff'))
        if i==1:
            body+=f'<path d="M{x+26} {y+17}h46v54h-46z" fill="#fff"/><path d="M{x+35} {y+31}h28m-28 12h28m-28 12h20" stroke="{BLUE}" stroke-width="3"/><circle cx="{x+72}" cy="{y+70}" r="13" fill="{GREEN}"/>'
        else:
            body+=f'<circle cx="{x+48}" cy="{y+42}" r="23" fill="{GREEN if i!=2 else BLUE}"/>'
            if i==0:body+=f'<path d="M{x+35} {y+42}h26m-22-10h18m-15 20h12" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
            elif i==2:body+=f'<circle cx="{x+48}" cy="{y+35}" r="8" fill="#fff"/><path d="M{x+33} {y+58}q15-17 30 0" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
            else:body+=f'<path d="M{x+36} {y+42}l9 9 17-21" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
        title,sub=vals[2*i:2*i+2]
        body+=containing_box(svg_text(title,x+10,y+72,256,50,24,color='#fff' if i==1 else TEXT),(x,y,276,175))
        body+=containing_box(svg_text(sub,x+10,y+114,256,57,19,color='#fff' if i==1 else MUTED),(x,y,276,175))
    body+=arrow(334,127,466,127)+arrow(604,215,604,330)+arrow(466,417,334,417)+arrow(196,330,196,215)
    body+=svg_text(vals[8],25,515,750,80,23,color='#6FA030')
    (figures/'academy_learning_loop.svg').write_text(svg_document(body,600,course[1][5]['alt']))

def animations(locale,labels):
    spec=importlib.util.spec_from_file_location('canonical_brand_animation',ROOT/'animations/build_teaching_animations.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    original=ImageDraw.Draw;original_new=Image.new
    originals=json.loads((ROOT/'course.json').read_text())
    translations={}
    for m,s,key in [(0,7,'flywheel'),(1,7,'touchpoints')]:
        entries=originals['modules'][m]['slides'][s]['figure']['text_inventory']['entries']
        translations.update({' '.join(e['text'].split()).casefold():v for e,v in zip(entries,labels[key])})
    def tr(value):
        key=' '.join(value.split()).casefold()
        if key not in translations:raise ValueError(f'Untranslated animation label: {value}')
        return translations[key]
    module.font=lambda size,bold=False:ImageFont.truetype(FONT_BOLD if bold else FONT,round(size*SIZE))
    def scaled_box(box):return tuple(x*SIZE for x in box)
    class Draw:
        def __init__(self,image,*a,**kw):self.raw=original(image,*a,**kw)
        def textbbox(self,xy,text,**kw):return tuple(n/SIZE for n in self.raw.textbbox(scaled_box(xy),text,**kw))
        def text(self,xy,value,**kw):
            value=tr(value);font=kw.get('font');max_width=(1226-xy[0])*SIZE
            # Clear the top ring card even when a translated subtitle is long.
            if xy[1]==38:xy=(xy[0],8)
            elif xy[1]==76:xy=(xy[0],43)
            while self.raw.textlength(value,font=font)>max_width:
                font=font.font_variant(size=font.size-1)
            kw['font']=font;self.raw.text(scaled_box(xy),value,**kw)
        def __getattr__(self,name):
            func=getattr(self.raw,name)
            def draw(xy,**kw):
                if name=='polygon':xy=[scaled_box(p) for p in xy]
                else:xy=scaled_box(xy)
                for key in ['width','radius']:
                    if key in kw:kw[key]=round(kw[key]*SIZE)
                return func(xy,**kw)
            return draw
    def centered(draw,box,value,font,fill,spacing=4):
        is_bold='bold' in font.getname()[1].lower()
        text=tr(value);n,lines=layout(text,box[2]-box[0],box[3]-box[1],round(font.size/SIZE),is_bold)
        font=ImageFont.truetype(FONT_BOLD if is_bold else FONT,round(n*SIZE));height=n*1.22
        y=box[1]+((box[3]-box[1])-len(lines)*height)/2
        for line in lines:
            bbox=draw.raw.textbbox((0,0),line,font=font)
            width=(bbox[2]-bbox[0])/SIZE
            draw.raw.text(((box[0]+((box[2]-box[0])-width)/2)*SIZE,y*SIZE-bbox[1]),line,font=font,fill=fill)
            y+=height
    module.centered_text=centered
    ImageDraw.Draw=Draw
    Image.new=lambda mode,size,*a,**kw:original_new(mode,tuple(round(x*SIZE) for x in size),*a,**kw)
    module.FIGURES=locale/'figures';module.FRAMES=locale/'_media_frames'
    try:
        module.make_flywheel_frames();module.make_touchpoints_frames()
    finally:ImageDraw.Draw=original;Image.new=original_new
    ffmpeg=os.environ.get('FFMPEG_BIN','ffmpeg')
    for slug in ['credibility_flywheel','useful_touchpoints']:
        subprocess.run([ffmpeg,'-v','error','-y','-framerate','30','-i',str(module.FRAMES/slug/'frame_%04d.png'),'-frames:v','180','-an','-c:v','libx264','-preset','slow','-tune','animation','-crf','8','-pix_fmt','yuv420p','-movflags','+faststart',str(locale/'figures'/f'{slug}.mp4')],check=True)

def embed_svg_fonts(file):
    """An SVG loaded as an image cannot rely on the HTML page's fonts."""
    import xml.etree.ElementTree as ET
    from fontTools import subset
    from fontTools.ttLib import TTFont
    root=ET.fromstring(file.read_text());text=''.join(root.itertext());rules=[]
    for source,weight in [(FONT,400),(FONT_BOLD,700)]:
        font=TTFont(source);font.recalcTimestamp=False;options=subset.Options();options.layout_features=['*']
        missing={ord(c) for c in text if c.isprintable() and not c.isspace()}-set(font.getBestCmap())
        if missing:raise ValueError(f'Media font lacks glyphs: {sorted(missing)}')
        worker=subset.Subsetter(options=options);worker.populate(text=text);worker.subset(font)
        font.flavor='woff2';buffer=io.BytesIO();font.save(buffer)
        encoded=base64.b64encode(buffer.getvalue()).decode()
        rules.append(f'@font-face{{font-family:CourseMedia;font-style:normal;font-weight:{weight};src:url("data:font/woff2;base64,{encoded}") format("woff2");}}')
    style=ET.Element('{http://www.w3.org/2000/svg}style');style.text='\n'.join(rules);root.insert(0,style)
    root.set('font-family','CourseMedia')
    for node in root.iter():
        if 'font-family' in node.attrib:node.set('font-family','CourseMedia')
    file.write_text(ET.tostring(root,encoding='unicode')+'\n')

def main():
    global FONT,FONT_BOLD
    p=argparse.ArgumentParser();p.add_argument('language');p.add_argument('--static-only',action='store_true');args=p.parse_args()
    locale=ROOT/'locales'/args.language
    fonts=locale/'animations/fonts'
    extension='.otf' if (fonts/'media-regular.otf').exists() else '.ttf'
    FONT=os.environ.get('ACADEMY_MEDIA_FONT',str(fonts/('media-regular'+extension)))
    FONT_BOLD=os.environ.get('ACADEMY_MEDIA_FONT_BOLD',str(fonts/('media-bold'+extension)))
    labels=json.loads((locale/'animations/labels.json').read_text());path=locale/'course.json';c=json.loads(path.read_text())
    figures=[[s.get('figure',{}) for s in m['slides']] for m in c['modules']]
    static_figures(locale,labels,figures)
    for name in ['trusted_community','listen_first_sequence','membership_tiers','marketplace_referral','academy_learning_loop']:
        embed_svg_fonts(locale/'figures'/f'{name}.svg')
    if not args.static_only:animations(locale,labels)
    for m,s,key in [(0,2,'trusted'),(0,4,'listen'),(0,6,'membership'),(0,7,'flywheel'),(1,2,'marketplace'),(1,5,'academy'),(1,7,'touchpoints')]:
        fig=c['modules'][m]['slides'][s]['figure']
        if key=='membership':fig['path']='figures/membership_tiers.svg'
        values=labels[key]
        if key=='membership':values=[values[0]]+[f'OCP {tier.upper()} Member {tier}' for tier in ['Startup','Bronze','Silver','Gold','Platinum']]+[values[1]]
        if key=='listen':values=[f'{i+1} {v}' for i,v in enumerate(values)]
        fig['text_inventory']={'sha256':hashlib.sha256((locale/fig['path']).read_bytes()).hexdigest(),'entries':[{'text':v,**({'at_seconds':0} if key in ['flywheel','touchpoints'] else {})} for v in values]}
    c['localization']['media_review']='Text-bearing teaching artwork localized; official membership logos retained; silent 6-second cyclic animation geometry and flywheel centerline arrows preserved.'
    path.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    print(args.language,'localized media rebuilt')

if __name__=='__main__':main()

"""Assemble editable Academy course data, scripts, artwork and learner metadata."""
import json
from pathlib import Path
import re
from hashlib import sha256
from artwork import *
from record import HERE, COURSE, scripts

def write_json(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def refs(*entries):return [{'label':a,'url':b} for a,b in entries]
def watch(video,at):return f'https://www.youtube.com/watch?v={video}&t={at}s'
OCP='https://www.opencompute.org/'
NEWS=OCP+'news/'
CAT='https://academy.opencompute.org/pages/21/ocp-data-center-technologies'
NEWSLETTER='https://mailchi.mp/opencompute/subscribe-to-ocp'
MARKET=NEWS+'idc-raises-2029-forecast-for-ocp-recognized-infrastructure-spending-by-2-7x-to-800-billion/'
VISION=NEWS+'realizing-the-ocp-open-data-center-ecosystem-vision/'
ROI=NEWS+'new-study-finds-open-compute-project-delivers-up-to-150x-roi-and-accelerates-data-center-deployment-by-15/'
PROJECTS=OCP+'projects/'
public={
 1:refs(('Meta · one cluster, many roofs',watch('lvieN3sJTUk',175))),
 2:refs(('What the IDC study measures',MARKET)),
 3:refs(('2023 opening address',watch('1STnWL8fq30',252)),('2024 IDC forecast',watch('owDFiggisBo',113)),('2025 IDC forecast',OCP+'about/ocp-adoption/'),('2026 IDC forecast',MARKET)),
 4:refs(('OCP end-user value study',ROI)),
 5:refs(('Lisa Su · Helios and Open Rack Wide',watch('3nFDQMaoNKc',703)),('Ian Buck · MGX 1.2',watch('UR7kJy7X_nQ',225))),
 6:refs(('Santosh Janardhan · regional links',watch('lvieN3sJTUk',275))),
 7:refs(('ABB and Eaton · why connections matter',watch('mLM9hox-y48',712))),
 9:refs(('George Tchaparian · 2027 priorities',watch('ceCw7zzZMWw',810)),('OCP’s 2027 vision',VISION)),
 10:refs(('All OCP projects',PROJECTS)),
 11:refs(('Academy’s October milestone',VISION)),12:[]}
topic_choices=[
 ('Rack & Power','What detail would have helped before your last purchase? Look for the mailing list or next project call.','rack-and-power/'),
 ('Networking','What changed when your equipment moved into a second building? Bring one distance, reliability or operating constraint.','networking/'),
 ('Heat Reuse','Who nearby could use the heat? Compare the Economics, Policies and Reference Designs workstreams.','cooling-environments/heat-reuse/'),
 ('AI Computing Continuum','How much space, cooling and support are available at your site? Bring the constraint that shapes your choices.','aicc/')]
projects=[{'label':a,'text':b,'url':PROJECTS+c,'action':'Visit '+a} for a,b,c in topic_choices]

def choice(prompt, items):
    return {'prompt':prompt,'options':[{'label':a,'text':b} for a,b in items]}
activities={
 1:choice('Revisit a Summit year', [('2023','4,401 people gathered in San Jose.'),('2024','7,047 people attended the Global Summit.'),('2025','10,835 people attended, according to OCP’s 2026 comparison.'),('2026','15,000 people came to San Jose. Who would you bring to a project meeting?')]),
 2:choice('Follow the purchase', [('The buyer','A data center operator chooses equipment built to a recognized design. Buyers can use open designs outside OCP membership.'),('The supplier','The supplier receives payment for the equipment. IDC measures spending on these transactions worldwide.'),('The shared design','A drawing or specification helps teams build or choose equipment. The equipment purchase is what IDC counts.')]),
 3:{'kind':'prediction','prompt':'What was the new 2029 forecast?','pause_at':json.loads((HERE/'Scenes/slide_03.json').read_text())['prediction_pause']},
 4:choice('What would you check before delivery?', [('Room to work','Ask for the service clearances. A rack can fit the floor plan and still leave too little room to replace a tray.'),('Connections','Give the installation team the interface drawings early. Confirm which combinations have been tested.'),('Support','Agree on who owns the issue when it crosses two suppliers’ equipment. Put those contacts in the handover.')]),
 5:choice('Whose drawing is this?', [('I buy equipment','AMD’s Open Rack Wide example gives a buyer a defined rack architecture to discuss with suppliers. Ask which options they support.'),('I maintain it','NVIDIA’s MGX example brings the technician to the rear of the tray. Ask how to disconnect it, service it and restore the link.')]),
 6:choice('Inspect a network link', [('Between buildings','Distance matters. A team needs fiber routes and switching equipment to carry traffic from one roof to the next.'),('Across sites','Ask how the network brings paths together and what happens when a link fails. Listen to Meta’s regional network example.')]),
 7:choice('What would you request first?', [('Interface drawing','Compare the mechanical and electrical requirements. Next, ask which part combinations have passed a test.'),('Front-panel photo','A photo helps identify the part. Ask for the interface drawing and test results before committing to a purchase.')]),
 9:choice('Ask the factory team', [('When is the answer due?','Time the journey from camera to decision. Could the line divert the product before it passes the gate?'),('Who maintains the computer?','A local installation needs someone who can service it. The available space, cooling and support shape the choice.')]),
 10:{'kind':'project','prompt':'Which conversation would you like to join?','options':projects},
 11:{'prompt':'Pick a topic to explore','options':[{'label':'Open Rack','text':'Look for “Open Rack: Architecture, Power, Cooling and Deployment” in the catalog.','url':CAT,'action':'Browse Data Center Technologies'},{'label':'Liquid cooling','text':'Look for “Introduction to Liquid Cooling” in the catalog.','url':CAT,'action':'Browse Data Center Technologies'}]},
 12:{'kind':'close','prompt':'What question keeps coming up in your work that you could bring to the OCP community?','newsletter':NEWSLETTER,'catalog':CAT}}

# Each choice can also revisit the matching moment in the recorded explanation.
option_cues = {
    1: ['Forty-four hundred', 'seven thousand', 'Nearly eleven', 'fifteen thousand'],
    5: ['They used Open Rack Wide', 'Watch the tray'],
    6: ['Follow the light', 'specify the fiber'],
    7: ['a drawing gives', 'actually been tested'],
    9: ['little more distance', 'who will service'],
    11: ['If the rack examples', 'Introduction to Liquid Cooling'],
}
for n, cue_names in option_cues.items():
    cues = json.loads((HERE/'Scenes'/f'slide_{n:02}.json').read_text())['cues']
    for option, cue_name in zip(activities[n]['options'], cue_names):
        option['listen_at'] = cues[cue_name]
        option['look_at'] = cues[cue_name] + 1.2
activities[3]['reveal_at'] = json.loads((HERE/'Scenes/slide_03.json').read_text())['cues']['two point seven'] + 1.2
activities[3]['horizon_at'] = json.loads((HERE/'Scenes/slide_03.json').read_text())['cues']['One year further']
caps={1:'From 4,401 Summit attendees in 2023 to 15,000 in 2026.',3:'Pin the target year. Make a prediction before the second estimate appears.',5:'AMD’s Helios rack and NVIDIA’s MGX rack contribution illustrate two separate design decisions.',6:'A schematic of links between buildings and sites. Distances and building positions are illustrative.',7:'A shared interface gives buyers a starting point for checking fit and test evidence.',9:'Illustrative factory inspection. Response time and available support help determine where inference belongs.',11:'OCP’s October announcement and the Academy team’s November 2026 update.'}
def transcript(s):
    s=re.sub(r'\[[^\]]+\]\s*','',s)
    for a,b in [('O C P','OCP'),('I D C','IDC'),('S G Strategy','SG Strategy'),('A M D','AMD'),('A I C C','AICC'),('A I','AI'),('M G X one point two','MGX 1.2'),('Nvidia','NVIDIA'),('A B B','ABB'),('twenty twenty-three','2023'),('twenty twenty-four','2024'),('twenty twenty-five','2025'),('twenty twenty-six','2026'),('twenty twenty-seven','2027'),('twenty twenty-eight','2028'),('twenty twenty-nine','2029'),('twenty thirty','2030')]:s=s.replace(a,b)
    return s

def make_sources():
    title_text='OCP Market Impact: What We’re Building in 2027'
    mod_title='From the Summit to your first project call'
    pages=[]
    for n,t,body in scripts():
        audio=f'audio/module1/slide_{n:02}'
        label='How big did this get?' if n<=4 else 'Three moments from the Summit floor' if n<=8 else 'Where will you take this in 2027?'
        s={'id':n,'type':'content_diagram','slug':f'slide_{n:02}','section_label':label,'title':t,'transcript':transcript(body),'audio':{'script_file':audio+'.txt','wav_file':audio+'.wav','delivery_file':audio+'.mp3'}}
        if n in public:s['reference_links']=public[n]
        if n in activities:s['activity']=activities[n]
        if n in CUES:
            f=f'figures/scene_{n:02}';s['figure']={'media_type':'video','path':f+'.mp4','poster':f+'.png','alt':caps[n],'caption':caps[n],'source':'custom','sync_to_narration':True,'muted':True,'autoplay':False,'loop':False}
            mp=COURSE/(f+'.mp4')
            if mp.exists():s['figure']['text_inventory']={'sha256':sha256(mp.read_bytes()).hexdigest(),'entries':json.loads((HERE/'Scenes'/f'slide_{n:02}_labels.json').read_text())}
        if n==2:s['term_refs']=['recognized']
        if n==9:s['term_refs']=['inference']
        if n==8:
            s['type']='knowledge_check'
            s['subtitle']='Choose a headline, then two things you would ask a supplier.'
            s['questions']=[
               {'id':'headline','prompt':'Which headline would you run?','choices':[{'id':'forecast','text':'IDC lifts its 2029 forecast for OCP-recognized equipment to about $800 billion.','correct':True},{'id':'actual','text':'Buyers spent $800 billion on OCP-recognized equipment in 2026.','correct':False,'feedback_incorrect':'2026 is the study year. The forecast is for 2029.'},{'id':'fees','text':'OCP expects $800 billion in membership revenue.','correct':False,'feedback_incorrect':'The money changes hands between equipment buyers and sellers.'}],'feedback_correct':'Run it. The estimate changed, and the target year stayed put.','feedback_incorrect':'Check what changed, who spends the money and which year the forecast covers.'},
               {'id':'evidence','multiple':True,'prompt':'Which two requests help you check that a second supplier’s part fits and works?','choices':[{'id':'drawing','text':'The interface drawing','correct':True},{'id':'date','text':'The earliest ship date','correct':False},{'id':'test','text':'Results for tested part combinations','correct':True},{'id':'photo','text':'A photo of the front panel','correct':False}],'feedback_correct':'Exactly. The drawing gives you the requirements. Tests tell you which combinations worked.','feedback_incorrect':'Dates and photos are useful for other decisions. Here you need connection details and evidence that the parts worked together.'}]
        if n in [2,4,10]:
            s['figure']={'path':f'figures/still_{n:02}.svg','alt':{2:'Equipment spending flows from a buyer to a supplier.',4:'A shared drawing moves a conversation ahead of delivery day.',10:'Four paths lead from a person’s experience to an OCP project.'}[n]}
        if n==12:
            s['type']='course_complete';s['thank_you_message']='Bring one question to the next project call.';s['cert_message']='Follow the OCP newsletter or explore the technology catalog.'
        if s['type']=='content_diagram':
            s['media_focus']=True
        pages.append(s)
    course={'style':'Slides','authoring_renderer':'render_course.py','course_slug':'ocp-market-impact-2027','course_title':title_text,'course_subtitle':'A look back at the 2026 Global Summit and a place for you in the work ahead.','tagline':'Community-driven Hyperscale Innovation for All','language':'en-US','target_duration_minutes':22,'audience_level':'Introductory','spec_version_chip':'2026 Global Summit · 2027 outlook','standalone_course':True,'series_assignment':'OCP Orientation catalog','index_navigation_instruction':'In OCP Academy, you can also open the module from the syllabus.','index_module_links':False,'index_show_module_status':False,'index_start':{'enabled':True,'label':'Start the course','navigation':'direct'},'brand':{'primary_color':'#8DC63F','primary_color_dark':'#6FA030','gray':'#5F6062','course_logo':'market-impact.svg','academy_logo':'ocp_academy_white.svg'},'scorm':{'version':'1.2','organization':'multi-sco','include_home_sco':True,'expected_sco_count':2},'narration':{'engine':'elevenlabs','model_id':'eleven_v4','voice_id':'bbGtsRRKUfYO634UxSjz','voice_name':'Leo','speed':1.18,'teaching_video_mode':'narration-synchronized','delivery':{'format':'mp3','approved':True,'bitrate_kbps':96,'sample_rate_hz':44100,'channels':1,'bitrate_mode':'CBR'}},'term_glossary':[{'id':'recognized','term':'OCP-recognized','tooltip':'In the IDC market study, equipment based on designs recognized by OCP. Buyers may participate in the market without being OCP members.','url':MARKET,'reference_label':'OCP market study'},{'id':'inference','term':'Inference','tooltip':'Using a trained AI model to produce an answer from new input, such as a camera image.','url':VISION,'reference_label':'OCP ecosystem vision'}],'modules':[{'id':1,'slug':'module1','title':mod_title,'module_badge_text':'OCP Orientation','subtitle':'Market impact, Summit stories and a first project conversation','duration_estimate':'About 22 minutes','slides':pages}],'lms_catalog':{'title':title_text,'short_description':'Explore OCP’s market impact, meet the people building open AI infrastructure and find a project to join in 2027.','overview':'See how open designs travel from the Summit stage to an equipment purchase. Follow IDC’s changing forecast, explore three decisions about AI infrastructure, and find a project where your experience belongs.','duration_basis':'estimated_learner_time','duration_minutes':22,'home_duration_minutes':0.5,'duration_note':'Includes narration, exploration, comparison and two questions. Optional external recordings and project visits are additional.','modules':[{'id':1,'duration_minutes':21.5,'summary':'Explore the forecast, inspect rack and network designs, and choose an OCP project, Academy topic or newsletter to follow.'}]}}
    course['local_font_stylesheet']='assets/fonts/open-sans.css'
    course['resource_assets']=['assets/fonts/open-sans.css','assets/fonts/open-sans.ttf','assets/fonts/OFL.txt']
    write_json(COURSE/'poster.json',{'schema_version':1,'language':'en-US','badge':'OCP ORIENTATION','title_lines':['OCP MARKET IMPACT','WHAT WE’RE BUILDING','IN 2027'],'support_lines':['From the 2026 Global Summit','to your first project call'],'mark':'market-impact.svg','mark_alt':'Three connected buildings forming a community'})
    (COURSE/'market-impact.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'+circle(100,100,94,'#EDF4E9')+path('M42 134L96 79L159 118',TEAL,9)+group(building(17,92,.51)+building(66,35,.56)+building(119,82,.47))+circle(99,145,13,GREEN,INDIGO,3)+'</svg>')
    for n in [2,4,10]:
        if n==2:
            a=title('Follow one purchase','Worldwide equipment spending measured by IDC')+box(56,173,313,190,WHITE,GRID)+txt(90,229,'Buyer',36,INDIGO,700)+txt(90,283,'A data center operator',20,SUB)+box(593,173,313,190,WHITE,GRID)+txt(627,229,'Supplier',36,TEAL,700)+txt(627,283,'An equipment maker',20,SUB)+line(370,265,591,265,TEAL,5)+box(392,229,177,60,PAPER,TEAL)+txt(480,266,'Purchase order',18,TEAL,700,'middle')+foot('OCP-recognized equipment can be purchased by members and nonmembers.')
        if n==4:
            a=title('Before delivery day','A shared drawing lets teams ask the question earlier')+box(48,150,398,276,WHITE,GRID)+txt(76,202,'Design review',28,INK,700)+rack(95,240,.78)+txt(221,281,'Check fit',22,TEAL,600)+txt(221,326,'Plan service',22,TEAL,600)+box(476,150,438,276,INDIGO)+txt(510,213,'Deployment time',24,WHITE)+txt(510,309,'Up to 15%',58,WHITE,700)+txt(510,360,'acceleration reported',24,WHITE)+foot('SG Strategy end-user value study published by OCP, October 2026.')
        if n==10:
            a=title('A place for your question','Follow the work closest to your own experience')+people(202,294,1.15)
            for i,l in enumerate(['Rack & Power','Networking','Heat Reuse','AI Computing Continuum']):
                y=147+i*77
                a+=path(f'M320 294C405 294 400 {y+24} 496 {y+24}',TEAL,3)+box(500,y,391,54,WHITE,GRID)+txt(523,y+35,l,22,INDIGO,600)
            a+=foot('Project pages list ways to follow the discussion and get involved.')
        (COURSE/'figures'/f'still_{n:02}.svg').write_text(frame(a))
    for n in [2,4,10]:
        slide=pages[n-1]
        source=COURSE/slide['figure']['path']
        import xml.etree.ElementTree as ET
        texts=[{'text':node.text} for node in ET.fromstring(source.read_text()).iter('{http://www.w3.org/2000/svg}text') if node.text]
        slide['figure']['text_inventory']={'sha256':sha256(source.read_bytes()).hexdigest(),'entries':texts}
    write_json(COURSE/'course.json',course)
if __name__=='__main__':make_sources()

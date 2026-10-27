"""SCORM 2004 multi-SCO manifest extension, preserving module tracking boundaries."""
from copy import deepcopy
from xml.etree import ElementTree as ET
IMS='http://www.imsglobal.org/xsd/imscp_v1p1'
ADL='http://www.adlnet.org/xsd/adlcp_v1p3'
SEQ='http://www.imsglobal.org/xsd/imsss'

def render_manifest(course, out_dir, legacy_renderer):
    legacy=deepcopy(course);legacy['scorm']={'version':'1.2','organization':'multi-sco'}
    root=ET.fromstring(legacy_renderer(legacy,out_dir))
    old_ims=root.tag.split('}')[0][1:]
    # Do not carry the legacy 1.2 schema-location declarations into 2004.
    root.attrib.pop('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', None)
    if course.get('scorm_schema_assets'):
        root.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', ' '.join([IMS,'imscp_v1p1.xsd',ADL,'adlcp_v1p3.xsd','http://www.adlnet.org/xsd/adlseq_v1p3','adlseq_v1p3.xsd','http://www.adlnet.org/xsd/adlnav_v1p3','adlnav_v1p3.xsd',SEQ,'imsss_v1p0.xsd']))
    for node in root.iter():
        if node.tag.startswith('{'+old_ims+'}'):node.tag='{'+IMS+'}'+node.tag.split('}',1)[1]
        for key in list(node.attrib):
            if key.endswith('}scormtype'):
                node.set('{'+ADL+'}scormType',node.attrib.pop(key))
    root.find('{'+IMS+'}metadata/{'+IMS+'}schemaversion').text='2004 3rd Edition'
    org=root.find('{'+IMS+'}organizations/{'+IMS+'}organization')
    if not course['scorm'].get('include_course_home_sco',False):
        item=org.find("{*}item[@identifier='ITEM_LAUNCHER']")
        if item is not None:org.remove(item)
        launcher=root.find("{*}resources/{*}resource[@identifier='RES_LAUNCHER']")
        launcher.set('{'+ADL+'}scormType','asset')
    for item in org.findall('{'+IMS+'}item'):
        seq=ET.SubElement(item,'{'+SEQ+'}sequencing');ET.SubElement(seq,'{'+SEQ+'}deliveryControls',completionSetByContent='true',objectiveSetByContent='true')
    seq=ET.SubElement(org,'{'+SEQ+'}sequencing');ET.SubElement(seq,'{'+SEQ+'}controlMode',choice='true',flow='true')
    ET.register_namespace('',IMS);ET.register_namespace('adlcp',ADL);ET.register_namespace('imsss',SEQ);ET.indent(root,space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n'

def validate(course, tree):
    issues=[];root=tree.getroot();expected={f'module{m["id"]}.html' for m in course['modules']}
    resources=list(root.iter('{'+IMS+'}resource'));scos=[r for r in resources if r.get('{'+ADL+'}scormType')=='sco']
    if {r.get('href') for r in scos}!=expected or len(scos)!=len(expected):issues.append('2004 Slides must have exactly one tracked SCO per authored module')
    required=course['scorm'].get('required_sco_count',len(expected))
    if len(scos)!=required:issues.append(f'Expected exactly {required} tracked SCOs')
    if any(r.get('href')=='index.html' for r in scos):issues.append('Course Home must remain an untracked asset')
    items=list(root.iter('{'+IMS+'}item'))
    if {i.get('identifier') for i in items}!={f'ITEM_MODULE{m["id"]}' for m in course['modules']}:issues.append('Syllabus items must preserve exactly the module launch identifiers')
    return issues

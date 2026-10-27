"""Require the requested Course Home and four module syllabus entries."""
from xml.etree import ElementTree as ET

NS={'cp':'http://www.imsproject.org/xsd/imscp_rootv1p1p2'}
ADL='{http://www.adlnet.org/xsd/adlcp_rootv1p2}scormtype'

def validate_home_and_modules(manifest,course):
    tree=ET.fromstring(manifest) if isinstance(manifest,(str,bytes)) else manifest
    config=course['scorm']
    assert config['version']=='1.2' and config['organization']=='multi-sco'
    assert config.get('include_home_sco') is True, 'Course Home must be a tracked SCO in the editable source'
    assert [m['id'] for m in course['modules']]==[1,2,3,4], 'Preserve the four teaching modules'
    assert tree.findtext('cp:metadata/cp:schemaversion',namespaces=NS)=='1.2'
    expected=[('ITEM_LAUNCHER','RES_LAUNCHER','index.html')]+[(f'ITEM_MODULE{i}',f'RES_MODULE{i}',f'module{i}.html') for i in range(1,5)]
    orgs=tree.findall('cp:organizations/cp:organization',NS)
    assert len(orgs)==1
    items=orgs[0].findall('cp:item',NS)
    assert [(item.get('identifier'),item.get('identifierref')) for item in items]==[(item,resource) for item,resource,_ in expected], 'The syllabus must start with Course Home followed by four modules'
    resources=tree.findall('cp:resources/cp:resource',NS)
    scos=[resource for resource in resources if resource.get(ADL)=='sco']
    assert [(resource.get('identifier'),resource.get('href')) for resource in scos]==[(resource,href) for _,resource,href in expected], 'Course Home and each module must be SCO resources'
    assert items[0].findtext('cp:title',namespaces=NS)=='Course Home'
    assert len({resource.get('identifier') for resource in resources})==len(resources)
    assert len(orgs[0].findall('.//cp:item',NS))==5
    return scos

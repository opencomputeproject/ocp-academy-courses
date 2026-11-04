"""Keep Course Home and content-module syllabus counts explicit and consistent."""
import re

ADL='http://www.adlnet.org/xsd/adlcp_rootv1p2'

def is_multi_sco_slides(course):
    return (str(course.get('style') or 'Slides').casefold()=='slides'
            and (course.get('scorm') or {}).get('organization','multi-sco')=='multi-sco')

def include_home_sco(course):
    """Home is tracked by default; counts alone cannot authorize its removal."""
    config=course.get('scorm') or {}
    value=config.get('include_home_sco',True)
    if not isinstance(value,bool):raise ValueError('scorm.include_home_sco must be a boolean')
    if value is False and is_multi_sco_slides(course):
        approval=config.get('home_sco_omission') or {}
        instruction=approval.get('user_instruction','') if isinstance(approval,dict) else ''
        if (not isinstance(approval,dict) or approval.get('approved') is not True
                or not isinstance(instruction,str)
                or not re.search(r'\b(?:home|index(?:\.html)?)\b',instruction,re.I)):
            raise ValueError('Omitting Course Home requires scorm.home_sco_omission with approved: true and the actual Home/index-specific user instruction. A module count or SCO count is not a Home opt-out.')
    return value

def expected_syllabus_hrefs(course):
    if not is_multi_sco_slides(course):return []
    hrefs=(['index.html'] if include_home_sco(course) else [])+[f"module{m['id']}.html" for m in course.get('modules',[])]
    declared=(course.get('scorm') or {}).get('expected_sco_count')
    if declared is not None:
        if type(declared) is not int or declared<1:raise ValueError('scorm.expected_sco_count must be a positive integer')
        if declared!=len(hrefs):raise ValueError(f'scorm.expected_sco_count is {declared}, but Course Home plus the authored content modules requires {len(hrefs)} syllabus SCOs. Content-module count and total syllabus count are different.')
    return hrefs

def validate(course,tree,root=None):
    if not course or not is_multi_sco_slides(course):return []
    try:expected=expected_syllabus_hrefs(course)
    except ValueError as exc:return [str(exc)]
    manifest=tree.getroot();namespace=manifest.tag.split('}')[0].lstrip('{');q=lambda name:f'{{{namespace}}}{name}'
    resources={e.get('identifier'):e for e in manifest.iter(q('resource'))}
    org=manifest.find(f"{q('organizations')}/{q('organization')}")
    if org is None:return ['Slides manifest has no syllabus organization']
    items=org.findall(q('item'))
    actual=[resources[e.get('identifierref')].get('href') if e.get('identifierref') in resources else None for e in items]
    issues=[]
    if actual!=expected:issues.append(f'Slides syllabus order/count is wrong: expected {expected!r}; got {actual!r}. Course Home must be first unless its omission is specifically authorized.')
    scos=[e.get('href') for e in resources.values() if e.get(f'{{{ADL}}}scormtype')=='sco']
    if len(scos)!=len(expected) or set(scos)!=set(expected):issues.append(f'Slides tracked resources must match its {len(expected)} syllabus entries; got {scos!r}')
    home=next((e for e in resources.values() if e.get('href')=='index.html'),None)
    tracked=include_home_sco(course)
    if home is None or home.get(f'{{{ADL}}}scormtype')!=('sco' if tracked else 'asset'):issues.append('Course Home resource tracking does not match the authored Home setting')
    if root is not None and (root/'index.html').is_file():
        html=(root/'index.html').read_text(encoding='utf-8')
        calls=['SCORM.init()','SCORM.setCompleted()','SCORM.finish()']
        if tracked and any(call not in html for call in calls):issues.append('Tracked Course Home must initialize, complete and finish its own LMS session')
        if not tracked and any(call in html for call in calls):issues.append('An explicitly untracked Course Home must not write an LMS session')
    return issues

"""Explicit preservation of the reviewed HBF-style multi-SCO behavior.

This is a compatibility profile, not an LMS target-SCO navigation API. Keep
the normal wrapper and slide bookmarks unchanged for all other courses.
"""


def enabled(course: dict) -> bool:
    scorm = course.get('scorm') or {}
    profile = scorm.get('compatibility_profile')
    if profile is None:
        return False
    if profile != 'hbf-module-only':
        raise ValueError(f'Unknown SCORM compatibility profile: {profile!r}')
    if (str(course.get('style', 'Slides')).lower() != 'slides'
            or scorm.get('version') != '1.2'
            or scorm.get('organization') != 'multi-sco'
            or scorm.get('navigation') != 'direct'):
        raise ValueError('hbf-module-only requires explicitly selected Slides, SCORM 1.2, multi-sco and direct navigation')
    if scorm.get('docebo_navigation') or scorm.get('diagnostic_navigation'):
        raise ValueError('Do not combine the approved compatibility profile with deployment mappings or diagnostic modes')
    return True

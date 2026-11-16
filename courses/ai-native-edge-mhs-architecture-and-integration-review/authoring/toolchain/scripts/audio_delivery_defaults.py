"""MP3 defaults with explicit consent for legacy WAV-course migrations."""
import argparse
import json
from pathlib import Path
from pathlib import PurePosixPath

MP3_DELIVERY = {
    'format': 'mp3', 'approved': True, 'bitrate_kbps': 96,
    'sample_rate_hz': 44100, 'channels': 1, 'bitrate_mode': 'CBR',
}

def apply_delivery_defaults(course, migration_choice=None):
    """Record new-course defaults; never silently convert a WAV course.

    A source with narrated WAV paths but no delivery metadata is legacy/ambiguous.
    New authoring should declare MP3 delivery before adding narrated slides.
    Callers pass a choice only after the user's explicit agreement.
    """
    if str(course.get('style', 'Slides')).lower() != 'slides':
        return False
    if migration_choice not in (None, 'mp3', 'keep-wav'):
        raise ValueError('Audio delivery choice must be mp3 or keep-wav')
    narrated = [s for m in course.get('modules', []) for s in m.get('slides', [])
                if s.get('audio') and s.get('narration_enabled', True)
                and (s.get('figure') or {}).get('role') != 'original_video']
    current = (course.get('narration') or {}).get('delivery') or {}
    legacy_wav = current.get('format') == 'wav' or (
        not current and any((s['audio'].get('wav_file') or '').lower().endswith('.wav')
                            and not s['audio'].get('delivery_file') for s in narrated))
    if legacy_wav and migration_choice is None and current.get('migration_decision') != 'keep-wav':
        raise ValueError('This course uses or previously defaulted to WAV narration. '
                         'Ask the user: Convert all narration to 96 kbps MP3 for smaller files '
                         'and faster learner downloads, retaining WAV masters without new TTS charges? '
                         'After agreement use --audio-delivery-choice mp3; '
                         'if declined use --audio-delivery-choice keep-wav. No conversion was made.')
    narration = course.setdefault('narration', {})
    changed = False
    if legacy_wav and migration_choice is not None:
        narration['delivery'] = (dict(MP3_DELIVERY) if migration_choice == 'mp3'
                                 else {'format': 'wav', 'approved': True})
        narration['delivery']['migration_decision'] = migration_choice
        changed = True
        for slide in narrated:
            audio = slide['audio']
            if migration_choice == 'keep-wav':
                audio.pop('delivery_file', None)
            elif audio.get('wav_file'):
                audio['delivery_file'] = str(PurePosixPath(audio['wav_file']).with_suffix('.mp3'))
    if not narration.get('delivery'):
        narration['delivery'] = dict(MP3_DELIVERY)
        changed = True
    if narration.get('delivery', {}).get('format') != 'mp3':
        return changed
    for module in course.get('modules', []):
        for slide in module.get('slides', []):
            if not slide.get('narration_enabled', True) or (slide.get('figure') or {}).get('role') == 'original_video':
                continue
            audio = slide.get('audio')
            if audio and audio.get('wav_file') and 'delivery_file' not in audio:
                audio['delivery_file'] = str(PurePosixPath(audio['wav_file']).with_suffix('.mp3'))
                changed = True
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('course_json', type=Path)
    parser.add_argument('--audio-delivery-choice', choices=['mp3', 'keep-wav'],
                        help='Record an explicit user decision for this WAV course')
    args = parser.parse_args()
    course = json.loads(args.course_json.read_text(encoding='utf-8'))
    try:
        changed = apply_delivery_defaults(course, args.audio_delivery_choice)
    except ValueError as error:
        parser.exit(2, str(error)+'\n')
    if changed:
        args.course_json.write_text(json.dumps(course, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print('Audio delivery choice/defaults recorded.' if changed else 'Audio delivery unchanged.')


if __name__ == '__main__':
    main()

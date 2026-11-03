"""Full v4/Leo at the approved pace, measured against each existing VTT cue."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import base64
import array
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import urllib.request
import wave

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / 'skills/academy-wizard/scripts').is_dir())
SCRIPTS = ROOT / 'skills/academy-wizard/scripts'
sys.path.insert(0, str(SCRIPTS))
from audio_pacing import find_ffmpeg, synth_paced, wav_duration
from elevenlabs_model_support import validate_model_language, validate_voice_model, primary_language_code
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('course_json', type=Path)
parser.add_argument('--force', action='store_true')
parser.add_argument('--work-dir', type=Path)
args = parser.parse_args()
COURSE_FILE = args.course_json.resolve()
COURSE = json.loads(COURSE_FILE.read_text())
OUTPUT = COURSE_FILE.parent
WORK = args.work_dir or ROOT / 'build' / '_caption-narration' / COURSE['course_slug']
WORK.mkdir(parents=True, exist_ok=True)
PLAN = json.loads((HERE / 'narration-cue-plan.json').read_text())
MASTERS = WORK / 'masters'
FFMPEG = find_ffmpeg()
VOICE = (COURSE.get('narration') or {}).get('voice_id')
if VOICE != PLAN['voice_id'] or (COURSE.get('narration') or {}).get('model_id') != 'eleven_v4' or (COURSE.get('narration') or {}).get('speed') != PLAN['tempo_multiplier']:
    raise ValueError('Cue-plan voice/model/pace must match the course. Localize and review the cue plan before generating another locale.')
SLIDES = {s['id']: s for m in COURSE['modules'] for s in m['slides']}
PENDING = [c for c in PLAN['clips'] if args.force or not (OUTPUT / SLIDES[c['slide']]['audio']['wav_file']).exists()]
if PENDING:
    if PLAN.get('approved') is not True:
        raise SystemExit('Translate and approve the caption narration cue plan before any speech-generation request.')
    key = os.environ.get('ELEVENLABS_API_KEY')
    validate_model_language('eleven_v4', COURSE.get('language'), api_key=key)
    validate_voice_model('eleven_v4', VOICE, api_key=key)

def generate(clip):
    sid = clip['slide']
    folder = WORK / f'slide-{sid}'
    folder.mkdir(exist_ok=True)
    texts = [cue['recommended_spoken_text'] for cue in clip['cues']]
    text = '\n\n'.join(texts)
    (folder / 'script.txt').write_text(text + '\n')
    identity = {'engine': 'elevenlabs', 'model_id': 'eleven_v4', 'voice_id': VOICE,
                'language': primary_language_code(COURSE.get('language')), 'purpose': 'caption-timed-demonstration'}
    paced = folder / 'paced-continuous.wav'
    receipt_file = folder / 'continuous-receipt.json'
    if not receipt_file.exists() or json.loads(receipt_file.read_text())['text_sha256'] != hashlib.sha256(text.encode()).hexdigest():
        def synth_native(body, output):
            payload = {'text': body, 'model_id': 'eleven_v4',
                       'language_code': primary_language_code(COURSE.get('language')),
                       'voice_settings': {'stability': 0.55, 'similarity_boost': 0.75}}
            req = urllib.request.Request(
                f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_96',
                data=json.dumps(payload).encode(), method='POST',
                headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'content-type': 'application/json'})
            with urllib.request.urlopen(req, timeout=180) as response:
                result = json.load(response)
                request_id = response.headers.get('request-id')
            provider = output.with_suffix('.provider.mp3')
            provider.write_bytes(base64.b64decode(result.pop('audio_base64')))
            result['request_id'] = request_id
            (folder / 'provider-alignment.json').write_text(json.dumps(result, indent=2) + '\n')
            subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(provider),
                            '-ar', '22050', '-ac', '1', '-c:a', 'pcm_s16le', str(output)], check=True)
        receipt = synth_paced(text, paced, work_dir=MASTERS, identity=identity,
                              synth_native=synth_native, speed=1.18)
        receipt_file.write_text(json.dumps(receipt, indent=2) + '\n')
    receipt = json.loads(receipt_file.read_text())
    result = json.loads((folder / 'provider-alignment.json').read_text())
    alignment = result.get('alignment') or result.get('normalized_alignment')
    assert alignment, 'The provider must return measured character timestamps.'
    # Normalize whitespace while retaining character indices into provider time.
    chars = alignment['characters']
    normalized, indices = [], []
    for index, char in enumerate(chars):
        for c in char:
            if c.isspace():
                if normalized and normalized[-1] != ' ':
                    normalized.append(' '); indices.append(index)
            else:
                normalized.append(c); indices.append(index)
    aligned_text = ''.join(normalized)
    rate = receipt['final_seconds'] / receipt['native_seconds']
    with wave.open(str(paced)) as reader:
        sample_rate = reader.getframerate()
        pcm = reader.readframes(reader.getnframes())
    amplitudes = array.array('h', pcm)
    def quiet(position):
        segment = amplitudes[round(position * sample_rate):round((position + 0.02) * sample_rate)]
        return bool(segment) and math.sqrt(sum(x*x for x in segment) / len(segment)) / 32768 < 0.001
    target = bytearray(round(clip['duration_seconds'] * sample_rate) * 2)
    cues, cursor, previous_ending = [], 0, 0
    for cue, spoken in zip(clip['cues'], texts):
        needle = ' '.join(spoken.split())
        position = aligned_text.find(needle, cursor)
        assert position >= 0, (sid, spoken, aligned_text)
        cursor = position + len(needle)
        first, last = indices[position], indices[cursor - 1]
        onset = alignment['character_start_times_seconds'][first] * rate
        ending = alignment['character_end_times_seconds'][last] * rate
        # Provider marks guide the cut, but locate genuinely quiet sentence
        # boundaries in the PCM too: never cut a consonant at a character mark.
        start = max(0, onset - 0.045)
        while start > max(0, previous_ending + 0.02) and not quiet(start):
            start = max(0, start - 0.005)
        start = max(0, start - 0.02)
        end = min(wav_duration(paced), ending + 0.045)
        while end < min(wav_duration(paced) - 0.025, ending + 0.5) and not quiet(end):
            end += 0.005
        end = min(wav_duration(paced), end + 0.025)
        previous_ending = ending
        samples = pcm[round(start * sample_rate) * 2:round(end * sample_rate) * 2]
        measured_seconds = len(samples) / 2 / sample_rate
        available = cue['end_seconds'] - cue['start_seconds'] - 0.04
        fits = measured_seconds <= available
        if fits:
            offset = round((cue['start_seconds'] + 0.02) * sample_rate) * 2
            target[offset:offset + len(samples)] = samples
        cues.append({**cue, 'source_speech_start': onset, 'source_speech_end': ending,
                     'source_cut_start': start, 'source_cut_end': end,
                     'measured_seconds': measured_seconds, 'available_seconds': available,
                     'fits': fits, 'placed_clip_start': cue['start_seconds'] + 0.02,
                     'placed_speech_start': cue['start_seconds'] + 0.02 + onset - start,
                     'placed_speech_end': cue['start_seconds'] + 0.02 + ending - start})
    summary = {'slide': sid, 'video_seconds': clip['duration_seconds'],
               'all_cues_fit': all(cue['fits'] for cue in cues), 'cues': cues,
               'voice_id': VOICE, 'model_id': 'eleven_v4', 'tempo_multiplier': 1.18}
    if summary['all_cues_fit']:
        output = folder / 'caption-timed.wav'
        with wave.open(str(output), 'wb') as writer:
            writer.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
            writer.writeframes(target)
        destination = OUTPUT / SLIDES[sid]['audio']['wav_file']
        destination.parent.mkdir(parents=True, exist_ok=True)
        __import__('shutil').copy2(output, destination)
        summary['output'] = str(destination)
        summary['output_sha256'] = hashlib.sha256(output.read_bytes()).hexdigest()
        summary['duration_seconds'] = wav_duration(output)
        composite = {**receipt, 'output': str(output), 'output_sha256': summary['output_sha256'],
                     'cue_assembly': 'Approved 1.18-paced speech split at sentence boundaries using provider character timestamps. Silence places each phrase in its existing caption window. No additional speed change.',
                     'video_seconds': clip['duration_seconds'], 'cue_timing': cues}
        (folder / 'timed-receipt.json').write_text(json.dumps(composite, indent=2) + '\n')
    (folder / 'fit-report.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(generate, PENDING))
    (WORK / 'fit-report.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps([{'slide':r['slide'], 'all_cues_fit':r['all_cues_fit'],
                       'overruns':[{'cue':c['cue'], 'speech':round(c['measured_seconds'],3),
                                    'window':c['end_seconds']-c['start_seconds']} for c in r['cues'] if not c['fits']]}
                      for r in rows], indent=2))

    if any(not row['all_cues_fit'] for row in rows):
        raise SystemExit('Caption narration does not fit. Review the phrase plan; keep the original media and approved pace. No ordinary narration fallback is allowed.')

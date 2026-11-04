"""Align final delivered speech to the five editable scene storyboards."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os
import hashlib
import json
import re
import wave
import requests

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / 'authoring/astra-media/alignment'
DEST.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get('ELEVENLABS_API_KEY', '').strip()
MAPPING = json.loads((ROOT / 'authoring/content/animation-audio-map.json').read_text())
SCENES = json.loads((ROOT / 'authoring/astra-media/scene-scripts.json').read_text())

def normalized(text):
    return ''.join(c.lower() for c in text if c.isalnum())

def align(pair):
    entry, scenes = pair
    recording = ROOT / entry['delivery_file']
    script = ROOT / entry['script_file']
    text = '\n'.join(line for line in script.read_text().splitlines() if not line.startswith('#')).strip()
    digest = hashlib.sha256(recording.read_bytes()).hexdigest()
    cache = DEST / (scenes['id'] + '.json')
    if cache.exists():
        result = json.loads(cache.read_text())
        if result.get('audio_sha256') == digest:
            return result
    if not KEY:
        raise RuntimeError('Set ELEVENLABS_API_KEY to request a new speech alignment.')
    with recording.open('rb') as audio:
        response = requests.post('https://api.elevenlabs.io/v1/forced-alignment',
            headers={'xi-api-key': KEY}, files={'file': (recording.name, audio, 'audio/mpeg')},
            data={'text': text}, timeout=180)
    response.raise_for_status()
    data = response.json()
    words = data['words']
    sequence, clock = '', []
    for word in words:
        part = normalized(word['text'])
        sequence += part
        clock.extend([float(word['start'])] * len(part))
    with wave.open(str(ROOT / entry['wav_file'])) as w:
        duration = w.getnframes() / w.getframerate()
    starts = []
    previous = 0
    for i, scene in enumerate(scenes['scenes']):
        if i == 0:
            starts.append(0.0)
            continue
        phrase = normalized(scene['text'])[:55]
        at = sequence.find(phrase, previous)
        if at < 0:
            raise ValueError('Cannot locate verified scene phrase: ' + scene['label'])
        starts.append(round(clock[at], 4))
        previous = at
    result = {'module': entry['module'], 'slide': entry['slide'], 'id': scenes['id'],
        'audio': entry['delivery_file'], 'audio_sha256': digest,
        'duration_seconds': duration, 'alignment_loss': data.get('loss'),
        'scene_starts_seconds': starts,
        'scenes': [{'label': scene['label'], 'start_seconds': starts[i],
                    'end_seconds': starts[i + 1] if i + 1 < len(starts) else duration,
                    'text': scene['text']} for i, scene in enumerate(scenes['scenes'])],
        'method': 'ElevenLabs forced alignment of delivered MP3 against approved text; scene boundaries use matched spoken phrases.'}
    cache.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    (DEST / (scenes['id'] + '-raw.json')).write_text(json.dumps(data, ensure_ascii=False) + '\n')
    print(scenes['id'], 'seconds', round(duration, 3), 'scene starts', starts, flush=True)
    return result

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(align, zip(MAPPING, SCENES)))
    (DEST / 'timing-manifest.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
    print('Aligned all five teaching sequences.', flush=True)

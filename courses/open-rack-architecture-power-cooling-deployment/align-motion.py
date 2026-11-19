"""Align the requested slide's animation script against its final paced audio."""
import hashlib, json, os, sys, urllib.error, urllib.request, uuid, wave
from pathlib import Path

root = Path(__file__).resolve().parent
fresh = '--fresh' in sys.argv
if fresh: sys.argv.remove('--fresh')
if not sys.argv[1:]:
    raise SystemExit('Usage: align-motion.py m1s3, or align-motion.py --fresh m4s9 [more slide IDs]')
for target in sys.argv[1:]:
    allowed = {'m2s4','m2s5','m2s6','m2s8','m2s9','m3s6','m3s7','m4s9','m4s10'} if fresh else {'m1s3'}
    if target not in allowed: raise SystemExit('Not a synchronized slide in this group: '+target)
    m,s = map(int, target[1:].split('s'))
    stem = next((root / 'audio' / f'module{m}' / ('fresh' if fresh else '')).glob(f'slide_{s:02}_*.txt'))
    wav = stem.with_suffix('.wav')
    text = '\n'.join(line for line in stem.read_text().splitlines() if not line.startswith('#')).strip()
    audio = wav.read_bytes()
    digest = hashlib.sha256(audio + text.encode()).hexdigest()
    dst = root/('fresh' if fresh else 'animations')/'timing'/f'{target}.json'
    if dst.exists() and json.loads(dst.read_text()).get('input_sha256') == digest:
        print('cached', target); continue
    with wave.open(str(wav)) as stream:
        duration = stream.getnframes()/stream.getframerate()
    boundary = uuid.uuid4().hex
    pre = f'--{boundary}\r\nContent-Disposition: form-data; name="text"\r\n\r\n{text}\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="narration.wav"\r\nContent-Type: audio/wav\r\n\r\n'
    payload = pre.encode() + audio + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request('https://api.elevenlabs.io/v1/forced-alignment', data=payload, headers={'xi-api-key':os.environ['ELEVENLABS_API_KEY'], 'Content-Type':f'multipart/form-data; boundary={boundary}'})
    try:
        with urllib.request.urlopen(req, timeout=180) as res: data=json.load(res)
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{target}: HTTP {e.code}; '+e.read().decode()[:400])
    words = [{'word':w['text'], 'start':w['start'], 'end':w['end']} for w in data['words'] if w['text'].strip()]
    if not words or not all(0<=w['start']<=w['end']<=duration+.15 for w in words):
        raise ValueError(f'{target}: invalid word times')
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(dict(method='ElevenLabs forced alignment on paced WAV', input_sha256=digest, duration=duration, words=words), indent=2)+'\n')
    print(target, len(words), 'timed words;', round(duration,3), 'seconds',flush=True)

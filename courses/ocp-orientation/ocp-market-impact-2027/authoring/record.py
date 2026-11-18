"""Record the performance script with word timing, retaining provider originals for edits."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request
import urllib.error

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
SKILL = Path(os.getenv("ACADEMY_WIZARD_SKILL_DIR", Path.home()/".codex/skills/academy-wizard"))
sys.path.insert(0, str(SKILL / "scripts"))
from audio_pacing import find_ffmpeg, match_wav_duration, wav_duration
from elevenlabs_model_support import validate_model_language, validate_voice_model

MODEL = "eleven_v4"
VOICE = "bbGtsRRKUfYO634UxSjz"
SPEED = 1.18

def scripts():
    material = (HERE/"Narration.md").read_text()
    return [(int(n), title.strip(), body.strip()) for n, title, body in
            re.findall(r"^## (\d+) · ([^\n]+)\n\n(.*?)(?=^## |\Z)", material, re.M | re.S)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs="*", type=int)
    args = parser.parse_args()
    key = os.environ["ELEVENLABS_API_KEY"]
    ffmpeg = find_ffmpeg()
    validate_model_language(MODEL, "en-US", api_key=key)
    validate_voice_model(MODEL, VOICE, api_key=key)
    for n,title,body in scripts():
        if args.numbers and n not in args.numbers:
            continue
        prefix = f"slide_{n:02}"
        work = HERE/"Recordings"/prefix
        work.mkdir(parents=True, exist_ok=True)
        payload = {"text":body, "model_id":MODEL, "language_code":"en",
                   "voice_settings":{"stability":0.55,"similarity_boost":0.75}}
        signature = hashlib.sha256(json.dumps([VOICE,payload], sort_keys=True).encode()).hexdigest()
        packet = work/(signature+".json")
        if not packet.exists():
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_96"
            request=urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                headers={"xi-api-key":key,"Content-Type":"application/json"})
            try:
                with urllib.request.urlopen(request,timeout=200) as response:
                    data=json.load(response)
                    charge=response.headers.get("character-cost")
                    data["charged_credits"]=int(charge) if charge is not None else None
            except urllib.error.HTTPError as e:
                raise SystemExit(f"Slide {n}: HTTP {e.code}: "+e.read().decode()[:600]) from e
            tmp=packet.with_suffix(".partial")
            tmp.write_text(json.dumps(data)); tmp.replace(packet)
        data=json.loads(packet.read_text())
        alignment=data["alignment"]
        if not alignment or not alignment["characters"]:raise ValueError("No character timing returned")
        (work/"timing.json").write_text(json.dumps(alignment,ensure_ascii=False))
        original=work/"native.mp3"
        original.write_bytes(base64.b64decode(data["audio_base64"]))
        native=work/"native.wav"
        subprocess.run([ffmpeg,"-nostdin","-loglevel","error","-y","-i",str(original),"-ar","22050","-ac","1",str(native)],check=True)
        out=COURSE/"audio/module1"/(prefix+".wav")
        timing=match_wav_duration(native,out,wav_duration(native)/SPEED,ffmpeg=ffmpeg)
        receipt=dict(timing,model_id=MODEL,voice_id=VOICE,tempo_multiplier=SPEED,
            text_sha256=hashlib.sha256(body.encode()).hexdigest(),output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
            billed_characters=data.get("charged_credits"),submitted_characters=len(body),provider_cache=packet.name)
        (work/"receipt.json").write_text(json.dumps(receipt,indent=2))
        (out.with_suffix(".txt")).write_text('# pronunciation: OCP, IDC, AMD and AI are spoken as letters.\n'+body+'\n')
        print(f"Slide {n:02}: {len(body)} characters, {timing['final_seconds']:.2f} s, billing {receipt['billed_characters']}",flush=True)

if __name__=="__main__":main()

"""Synthesize, pace, and caption the three IceCube video voiceovers."""

import base64
import concurrent.futures
import getpass
import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "authoring" / "voiceovers"
CAPTIONS = ROOT / "resources" / "captions"
MODEL = "eleven_v4"
VOICE = "bbGtsRRKUfYO634UxSjz"
TEMPO = 1.18
SAMPLE_RATE = 48000
LEAD_IN = 0.25


def request_json(path, key, payload=None):
    request = urllib.request.Request(
        "https://api.elevenlabs.io/v1/" + path,
        data=None if payload is None else json.dumps(payload).encode("utf-8"),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=100) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        try:
            detail = json.load(error).get("detail", {})
            status = detail.get("status", "") if isinstance(detail, dict) else ""
        except (ValueError, AttributeError):
            status = ""
        status = re.sub(r"[^a-zA-Z0-9_]", "", status)[:80]
        raise RuntimeError(f"ElevenLabs returned HTTP {error.code} ({status})") from None


def synthesize(key, name, number, scene):
    script = scene["text"]
    stem = WORK / f"{name}-{number:02}"
    audio_path = stem.with_suffix(".mp3")
    alignment_path = stem.with_suffix(".json")
    signature = hashlib.sha256(f"{MODEL}:{VOICE}:{script}".encode()).hexdigest()
    if audio_path.exists() and alignment_path.exists():
        alignment = json.loads(alignment_path.read_text())
        if alignment["signature"] == signature:
            return audio_path, alignment["alignment"]

    response = request_json(
        f"text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_96",
        key,
        {
            "text": script,
            "model_id": MODEL,
            "language_code": "en",
            "voice_settings": {"stability": 0.55, "similarity_boost": 0.75},
        },
    )
    alignment = response["alignment"] or response["normalized_alignment"]
    audio_path.write_bytes(base64.b64decode(response["audio_base64"], validate=True))
    alignment_path.write_text(json.dumps({
        "signature": signature, "model": MODEL, "voice": VOICE, "alignment": alignment,
    }, indent=2) + "\n")
    return audio_path, alignment


def timestamp(value):
    minutes, remainder = divmod(round(value * 1000), 60000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"00:{minutes:02}:{seconds:02}.{milliseconds:03}"


def readable_caption(text):
    replacements = {
        "A sick": "ASIC",
        "Q S F P twenty-eight": "QSFP28",
        "O S F P": "OSFP",
        "B M C": "BMC",
        "D C": "DC",
        "E one dot S": "E1.S",
    }
    for spoken, spelling in replacements.items():
        text = text.replace(spoken, spelling)
    return text


def cue_ranges(alignment, start, limit):
    text = "".join(alignment["characters"])
    onset = alignment["character_start_times_seconds"]
    offset = alignment["character_end_times_seconds"]
    words = list(re.finditer(r"\S+", text))
    first = 0
    while first < len(words):
        last = first
        while last + 1 < len(words):
            ending = words[last].end()
            proposed = readable_caption(text[words[first].start():words[last + 1].end()])
            reading_time = offset[ending - 1] - onset[words[first].start()]
            if len(proposed) > 77 or (text[ending - 1] in ".?!" and reading_time > 0.95):
                break
            last += 1
        lo, hi = words[first].start(), words[last].end()
        payload = "\n".join(textwrap.wrap(readable_caption(text[lo:hi]), 41, break_on_hyphens=False))
        cue_start = start + LEAD_IN + onset[lo] / TEMPO
        cue_end = start + LEAD_IN + offset[hi - 1] / TEMPO
        next_onset = start + LEAD_IN + onset[words[last + 1].start()] / TEMPO if last + 1 < len(words) else limit
        cue_end = min(limit, next_onset, max(cue_start + 0.8, cue_end + 0.20))
        if cue_end > cue_start:
            yield f"{timestamp(cue_start)} --> {timestamp(cue_end)}\n{payload}\n"
        first = last + 1


def assemble(name, plan, sources, ffmpeg):
    sound = bytearray(plan["duration"] * SAMPLE_RATE * 2)
    captions = ["WEBVTT\n"]
    durations = []
    for index, scene in enumerate(plan["scenes"]):
        start = scene["start"]
        next_start = plan["scenes"][index + 1]["start"] if index + 1 < len(plan["scenes"]) else plan["duration"]
        audio_path, alignment = sources[index]
        paced = subprocess.check_output([
            ffmpeg, "-nostdin", "-v", "error", "-i", str(audio_path),
            "-af", f"atempo={TEMPO},alimiter=limit=0.89:level=0:latency=1",
            "-ac", "1", "-ar", str(SAMPLE_RATE), "-f", "s16le", "pipe:1",
        ])
        duration = len(paced) / (SAMPLE_RATE * 2)
        if duration + LEAD_IN > next_start - start:
            raise RuntimeError(f"{name} scene {index + 1} is {duration:.2f}s and overruns its scene; revise its script.")
        offset = round((start + LEAD_IN) * SAMPLE_RATE) * 2
        sound[offset:offset + len(paced)] = paced
        captions.extend(cue_ranges(alignment, start, next_start))
        durations.append(round(duration, 3))
    with wave.open(str(WORK / f"{name}.wav"), "wb") as output:
        output.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))
        output.writeframes(sound)
    CAPTIONS.joinpath(f"{name}.en-US.vtt").write_text("\n".join(captions))
    print(f"{name}: placed four voiced scenes at their storyboard cues ({durations}s)", flush=True)


def main():
    ffmpeg = os.environ.get("FFMPEG_BIN", "ffmpeg")
    subprocess.run([ffmpeg, "-version"], check=True, stdout=subprocess.DEVNULL)
    WORK.mkdir(parents=True, exist_ok=True)
    CAPTIONS.mkdir(parents=True, exist_ok=True)
    plan = json.loads((ROOT / "authoring" / "video-narration.json").read_text())
    key = getpass.getpass("ElevenLabs API key: ").strip()
    catalog = request_json("models", key)
    model = next((value for value in catalog if value["model_id"] == MODEL), {})
    assert model.get("can_do_text_to_speech") and any(x["language_id"] == "en" for x in model["languages"])
    assert request_json(f"voices/{VOICE}", key)["voice_id"] == VOICE
    print("Verified Eleven v4, English, and Leo.", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for name, video in plan.items():
            jobs = [pool.submit(synthesize, key, name, number, scene) for number, scene in enumerate(video["scenes"], 1)]
            assemble(name, video, [future.result() for future in jobs], ffmpeg)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, urllib.error.URLError) as error:
        sys.exit(str(error))

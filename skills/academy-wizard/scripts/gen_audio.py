#!/usr/bin/env python3
"""
gen_audio.py — turn approved narration .txt files into .wav files.

Usage:
    python gen_audio.py <course.json> [--module N] [--engine elevenlabs|openai|say]
                       [--voice <voice_id>] [--force]

Defaults: walk every module and every slide; pick the engine automatically based
on environment variables (ELEVENLABS_API_KEY, then OPENAI_API_KEY, otherwise
fall back to macOS `say`). Skip slides whose .wav already exists unless --force.

The narration script for each slide must already exist at the path declared in
course.json's `audio.script_file`. The output WAV is written to `audio.wav_file`.

Output format target: 22050 Hz, 16-bit PCM, mono. Most LMSes are happiest with
this. Cloud engines that return mp3 are converted with ffmpeg if available;
otherwise the .mp3 is left in place and the slide HTML must reference .mp3.
"""

from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def pick_engine(requested: str | None) -> str:
    if requested:
        return requested
    if os.getenv("ELEVENLABS_API_KEY"):
        return "elevenlabs"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return "say"


def need(cmd: str) -> str | None:
    return shutil.which(cmd)


def synth_say(text: str, out_wav: Path) -> None:
    """macOS `say` -> AIFF -> WAV. Quality is mediocre but free."""
    if not need("say"):
        raise RuntimeError("`say` not found; on macOS this should be at /usr/bin/say.")
    aiff = out_wav.with_suffix(".aiff")
    subprocess.run(["say", "-v", "Samantha", "-o", str(aiff), "--data-format=LEI16@22050", text], check=True)
    # Rename .aiff to .wav — the header is different, but many players are lenient.
    # If ffmpeg is available, convert properly.
    if need("ffmpeg"):
        subprocess.run(["ffmpeg", "-y", "-i", str(aiff), "-ar", "22050", "-ac", "1", "-acodec", "pcm_s16le", str(out_wav)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        aiff.unlink(missing_ok=True)
    else:
        # afconvert (macOS-only) is a reliable alternative.
        if need("afconvert"):
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@22050", str(aiff), str(out_wav)], check=True)
            aiff.unlink(missing_ok=True)
        else:
            # Last resort: just rename. Some players won't accept this.
            aiff.replace(out_wav)


def synth_elevenlabs(text: str, out_wav: Path, voice_id: str | None) -> None:
    import urllib.request
    api_key = os.environ["ELEVENLABS_API_KEY"]
    # Default voice: Leo v2 — reads measured and authoritative for technical
    # narration. Override per call with --voice, or globally with
    # ELEVENLABS_VOICE_ID. Rachel (21m00Tcm4TlvDq8ikWAM) is warmer/conversational.
    voice = voice_id or os.getenv("ELEVENLABS_VOICE_ID") or "bbGtsRRKUfYO634UxSjz"  # Leo v2, default
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=pcm_22050"
    # speed (0.7–1.2) controls pacing. 1.0 reads slowly for dense technical
    # material; 1.15–1.20 is a good range. Override with ELEVENLABS_SPEED.
    body = json.dumps({
        "text": text,
        "model_id": os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
        "voice_settings": {
            "stability":        float(os.getenv("ELEVENLABS_STABILITY",  "0.55")),
            "similarity_boost": float(os.getenv("ELEVENLABS_SIMILARITY", "0.75")),
            "speed":            float(os.getenv("ELEVENLABS_SPEED",      "1.18")),
        },
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "xi-api-key": api_key,
        "content-type": "application/json",
        "accept": "audio/pcm",
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        pcm = resp.read()
    # Wrap raw PCM into a WAV
    import wave
    with wave.open(str(out_wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(22050)
        w.writeframes(pcm)


def synth_openai(text: str, out_wav: Path, voice_id: str | None) -> None:
    """Uses OpenAI's TTS API. Returns mp3; we convert to wav if ffmpeg is here."""
    import urllib.request
    api_key = os.environ["OPENAI_API_KEY"]
    voice = voice_id or os.getenv("OPENAI_TTS_VOICE", "alloy")
    model = os.getenv("OPENAI_TTS_MODEL", "tts-1")
    url = "https://api.openai.com/v1/audio/speech"
    body = json.dumps({"model": model, "voice": voice, "input": text, "format": "wav"}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read()
    out_wav.write_bytes(raw)
    # Re-encode to 22050 Hz mono PCM_S16 if ffmpeg is available
    if need("ffmpeg"):
        tmp = out_wav.with_suffix(".raw.wav")
        out_wav.replace(tmp)
        subprocess.run(["ffmpeg", "-y", "-i", str(tmp), "-ar", "22050", "-ac", "1", "-acodec", "pcm_s16le", str(out_wav)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tmp.unlink(missing_ok=True)


SYNTHS = {"say": synth_say, "elevenlabs": synth_elevenlabs, "openai": synth_openai}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("course_json", type=Path)
    p.add_argument("--module", type=int)
    p.add_argument("--engine", choices=list(SYNTHS.keys()))
    p.add_argument("--voice", help="engine-specific voice id")
    p.add_argument("--force", action="store_true", help="re-synth even if .wav exists")
    args = p.parse_args()

    course = json.loads(args.course_json.read_text())
    out_dir = args.course_json.resolve().parent
    engine = pick_engine(args.engine)
    print(f"engine: {engine}")
    synth = SYNTHS[engine]

    n_done = 0
    n_skip = 0
    for mod in course["modules"]:
        if args.module and mod["id"] != args.module:
            continue
        for slide in mod["slides"]:
            audio = slide.get("audio") or {}
            script_rel = audio.get("script_file")
            wav_rel = audio.get("wav_file")
            if not script_rel or not wav_rel:
                continue
            script_path = out_dir / script_rel
            wav_path = out_dir / wav_rel
            if not script_path.exists():
                print(f"  MISS script: {script_path}")
                continue
            if wav_path.exists() and not args.force:
                n_skip += 1
                continue
            text = script_path.read_text().strip()
            # Strip pronunciation hint comments (lines starting with "#")
            text = "\n".join(line for line in text.splitlines() if not line.startswith("#")).strip()
            if not text:
                print(f"  EMPTY: {script_path}")
                continue
            wav_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                if engine in ("elevenlabs", "openai"):
                    synth(text, wav_path, args.voice)
                else:
                    synth(text, wav_path)
                n_done += 1
                print(f"  OK {wav_path.relative_to(out_dir)}")
            except Exception as e:
                msg = str(e)
                print(f"  FAIL {wav_path.relative_to(out_dir)}: {msg}", file=sys.stderr)
                # The Codex sandbox can block api.elevenlabs.io and OpenAI's TTS
                # endpoint at the egress proxy. Help the user route around it.
                if "403" in msg and ("Tunnel" in msg or "proxy" in msg.lower() or "allowlist" in msg.lower()):
                    print(
                        "\n  NOTE: It looks like this sandbox can't reach the TTS endpoint.\n"
                        "  Run this command on your Mac/Linux host instead:\n"
                        f"      cd {out_dir}\n"
                        "      export ELEVENLABS_API_KEY=<your key>\n"
                        f"      python3 {Path(__file__).resolve()} {args.course_json.name}"
                        + (f" --module {args.module}" if args.module else "")
                        + "\n",
                        file=sys.stderr,
                    )
                    sys.exit(2)

    print(f"\nsynthesized: {n_done}; skipped (already present): {n_skip}")


if __name__ == "__main__":
    main()

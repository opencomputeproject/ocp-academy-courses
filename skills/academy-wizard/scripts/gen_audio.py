#!/usr/bin/env python3
"""
gen_audio.py — turn approved narration .txt files into .wav files.

Usage:
    python gen_audio.py <course.json> [--module N] [--engine elevenlabs|openai|say]
                       [--voice <voice_id>] [--model <model_id>]
                       [--model-policy stable|expressive|balanced] [--force]
                       [--allow-local-fallback-for-partial]

Defaults: walk every module and every slide; use top-level `narration` engine and
voice metadata when present, otherwise pick the engine from environment variables
(ELEVENLABS_API_KEY, then OPENAI_API_KEY, otherwise macOS `say`). Command-line
engine/voice/model options are explicit overrides. Skip existing .wav files unless
--force.

The narration script for each slide must already exist at the path declared in
course.json's `audio.script_file`. The output WAV is written to `audio.wav_file`.
Knowledge-check slides are always narrated; the script fails if a
`knowledge_check` slide lacks audio metadata or its script/WAV cannot be
generated.

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
import tempfile
from pathlib import Path

from elevenlabs_model_support import (
    default_model_for_language,
    primary_language_code,
    should_send_language_code,
    validate_model_language,
    validate_voice_model,
)


def narration_config(course: dict) -> dict:
    value = course.get("narration") or {}
    return value if isinstance(value, dict) else {}


def pick_engine(requested: str | None, course: dict | None = None) -> str:
    if requested:
        return requested
    configured = str(narration_config(course or {}).get("engine") or "").strip().lower()
    if configured:
        if configured not in ("elevenlabs", "openai", "say"):
            raise ValueError(f"Unsupported course narration engine: {configured}")
        return configured
    if os.getenv("ELEVENLABS_API_KEY"):
        return "elevenlabs"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return "say"


def pick_voice_id(requested: str | None, course: dict, engine: str) -> str | None:
    if requested:
        return requested
    configured = narration_config(course)
    configured_engine = str(configured.get("engine") or "").strip().lower()
    configured_voice = str(configured.get("voice_id") or "").strip()
    if configured_voice and configured_engine in ("", engine):
        return configured_voice
    if engine == "elevenlabs":
        return os.getenv("ELEVENLABS_VOICE_ID") or "bbGtsRRKUfYO634UxSjz"
    if engine == "openai":
        return os.getenv("OPENAI_TTS_VOICE", "alloy")
    return None


def pick_model_id(
    course: dict,
    engine: str,
    requested: str | None = None,
    requested_policy: str | None = None,
) -> str | None:
    if engine != "elevenlabs":
        return None
    if requested:
        return requested
    configured = narration_config(course)
    configured_engine = str(configured.get("engine") or "").strip().lower()
    configured_model = str(configured.get("model_id") or "").strip()
    if configured_model and configured_engine in ("", engine):
        return configured_model
    environment_model = str(os.getenv("ELEVENLABS_MODEL") or "").strip()
    if environment_model:
        return environment_model
    configured_policy = str(configured.get("model_policy") or "").strip().lower()
    environment_policy = str(
        os.getenv("ELEVENLABS_MODEL_POLICY") or ""
    ).strip().lower()
    policy = requested_policy or configured_policy or environment_policy or "stable"
    return default_model_for_language(course.get("language"), policy)


def need(cmd: str) -> str | None:
    return shutil.which(cmd)


def synth_say(text: str, out_wav: Path) -> None:
    """macOS `say` -> AIFF -> WAV. Quality is mediocre but free."""
    if not need("say"):
        raise RuntimeError("`say` not found; on macOS this should be at /usr/bin/say.")
    aiff = out_wav.with_suffix(".aiff")
    text_file = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as tmp:
            tmp.write(text)
            text_file = Path(tmp.name)
        subprocess.run(["say", "-v", "Samantha", "-f", str(text_file), "-o", str(aiff)], check=True)
    finally:
        if text_file:
            text_file.unlink(missing_ok=True)
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


def synth_elevenlabs(
    text: str,
    out_wav: Path,
    voice_id: str | None,
    model_id: str | None,
    language_code: str | None,
) -> None:
    import urllib.request
    api_key = os.environ["ELEVENLABS_API_KEY"]
    # Default voice: Leo v2 — reads measured and authoritative for technical
    # narration. Override per call with --voice, or globally with
    # ELEVENLABS_VOICE_ID. Rachel (21m00Tcm4TlvDq8ikWAM) is warmer/conversational.
    voice = voice_id or os.getenv("ELEVENLABS_VOICE_ID") or "bbGtsRRKUfYO634UxSjz"  # Leo v2, default
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=pcm_22050"
    # speed (0.7–1.2) controls pacing. 1.0 reads slowly for dense technical
    # material; 1.15–1.20 is a good range. Override with ELEVENLABS_SPEED.
    payload = {
        "text": text,
        "model_id": model_id
        or os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
        "voice_settings": {
            "stability":        float(os.getenv("ELEVENLABS_STABILITY",  "0.55")),
            "similarity_boost": float(os.getenv("ELEVENLABS_SIMILARITY", "0.75")),
            "speed":            float(os.getenv("ELEVENLABS_SPEED",      "1.18")),
        },
    }
    if language_code and should_send_language_code(str(payload["model_id"])):
        payload["language_code"] = language_code
    body = json.dumps(payload).encode("utf-8")
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


def slide_ref(mod: dict, slide: dict) -> str:
    return f"M{mod.get('id')}S{slide.get('id')} ({slide.get('type')}, {slide.get('slug', 'no-slug')})"


def iter_module_slides(course: dict, module_filter: int | None):
    for mod in course.get("modules", []):
        if module_filter and mod.get("id") != module_filter:
            continue
        for slide in mod.get("slides", []):
            yield mod, slide


def main():
    p = argparse.ArgumentParser()
    p.add_argument("course_json", type=Path)
    p.add_argument("--module", type=int)
    p.add_argument("--engine", choices=list(SYNTHS.keys()))
    p.add_argument("--voice", help="engine-specific voice id")
    p.add_argument("--model", help="ElevenLabs model id")
    p.add_argument(
        "--model-policy",
        choices=("stable", "expressive", "balanced"),
        help=(
            "select a use-case model when no explicit model is configured; "
            "stable is the default for technical narration"
        ),
    )
    p.add_argument("--force", action="store_true", help="re-synth even if .wav exists")
    p.add_argument(
        "--allow-local-fallback-for-partial",
        action="store_true",
        help=(
            "allow macOS say to fill missing knowledge-check audio even when other "
            "WAVs already exist; use only after the user approves the voice mismatch"
        ),
    )
    args = p.parse_args()

    course = json.loads(args.course_json.read_text())
    if str(course.get("style") or "Slides").strip().casefold() == "scrolling":
        print("Scrolling style has no narration by default; no audio generated.")
        return
    out_dir = args.course_json.resolve().parent
    try:
        engine = pick_engine(args.engine, course)
        model_id = pick_model_id(
            course,
            engine,
            args.model,
            args.model_policy,
        )
    except ValueError as error:
        sys.exit(str(error))
    voice_id = pick_voice_id(args.voice, course, engine)
    language_code = (
        primary_language_code(course.get("language"))
        if engine == "elevenlabs"
        else None
    )
    print(f"engine: {engine}")
    if voice_id:
        print(f"voice: {voice_id}")
    if model_id:
        print(f"model: {model_id}")

    if engine == "elevenlabs":
        def synth(text: str, wav_path: Path) -> None:
            synth_elevenlabs(
                text,
                wav_path,
                voice_id,
                model_id,
                language_code,
            )
    elif engine == "openai":
        def synth(text: str, wav_path: Path) -> None:
            synth_openai(text, wav_path, voice_id)
    else:
        synth = synth_say

    jobs = []
    errors: list[str] = []
    existing_wavs = 0
    needs_synth_knowledge_check = False
    for mod, slide in iter_module_slides(course, args.module):
        audio = slide.get("audio") or {}
        script_rel = audio.get("script_file")
        wav_rel = audio.get("wav_file")
        is_knowledge_check = slide.get("type") == "knowledge_check"
        if is_knowledge_check and (not script_rel or not wav_rel):
            errors.append(f"{slide_ref(mod, slide)} missing audio.script_file/audio.wav_file")
            continue
        if not script_rel or not wav_rel:
            continue
        script_path = out_dir / script_rel
        wav_path = out_dir / wav_rel
        if wav_path.exists():
            existing_wavs += 1
        elif is_knowledge_check:
            needs_synth_knowledge_check = True
        if args.force and is_knowledge_check:
            needs_synth_knowledge_check = True
        jobs.append((mod, slide, script_path, wav_path))

    if (
        engine == "say"
        and existing_wavs
        and needs_synth_knowledge_check
        and not args.allow_local_fallback_for_partial
        and not args.force
    ):
        errors.append(
            "refusing to synthesize a missing knowledge-check narration with macOS "
            "`say` while other narration WAVs already exist; provide the same cloud "
            "TTS credentials/voice used for the course, or get explicit user approval "
            "and rerun with --allow-local-fallback-for-partial"
        )

    if errors:
        print("\nAudio generation blocked:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    needs_synthesis = any(args.force or not job[3].exists() for job in jobs)
    if engine == "elevenlabs" and needs_synthesis:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            sys.exit(
                "Audio generation blocked before synthesis: "
                "ELEVENLABS_API_KEY is not set."
            )
        try:
            validation_source = validate_model_language(
                str(model_id),
                course.get("language"),
                api_key=api_key,
            )
            voice_validation_source = validate_voice_model(
                str(model_id),
                voice_id,
                api_key=api_key,
            )
        except (RuntimeError, ValueError) as error:
            sys.exit(str(error))
        print(
            "model/language preflight: "
            f"{model_id} supports {language_code} ({validation_source})"
        )
        if model_id == "eleven_v3":
            print(
                "voice/model preflight: "
                f"{voice_id} supports {model_id} "
                f"({voice_validation_source})"
            )

    n_done = 0
    n_skip = 0
    for mod, slide, script_path, wav_path in jobs:
        if not script_path.exists():
            errors.append(f"{slide_ref(mod, slide)} missing script: {script_path}")
            continue
        if wav_path.exists() and not args.force:
            n_skip += 1
            continue
        text = script_path.read_text().strip()
        # Strip pronunciation hint comments (lines starting with "#")
        text = "\n".join(line for line in text.splitlines() if not line.startswith("#")).strip()
        if not text:
            errors.append(f"{slide_ref(mod, slide)} empty script: {script_path}")
            continue
        wav_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            synth(text, wav_path)
            n_done += 1
            print(f"  OK {wav_path.relative_to(out_dir)}")
        except Exception as e:
            msg = str(e)
            errors.append(f"{slide_ref(mod, slide)} failed {wav_path.relative_to(out_dir)}: {msg}")
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
    if errors:
        print("\nAudio generation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

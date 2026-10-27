#!/usr/bin/env python3
"""
gen_audio.py — turn approved narration .txt files into .wav files.

Usage:
    python gen_audio.py <course.json> [--module N] [--engine elevenlabs|openai|say]
                       [--voice <voice_id>] [--model <model_id>]
                       [--model-policy stable|expressive|balanced] [--force]
                       [--allow-local-fallback-for-partial]
                       [--pacing-reference-root <baseline-course-folder>]
                       [--audio-work-dir <working-folder>]

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
import shlex
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

from audio_pacing import (
    V4_MODELS,
    find_ffmpeg,
    reference_files,
    spoken_script,
    synth_duration_matched,
)
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


def pick_elevenlabs_speed(course: dict) -> tuple[float, str]:
    configured = narration_config(course)
    if "speed" in configured:
        raw = configured["speed"]
        source = "course narration.speed"
    elif os.getenv("ELEVENLABS_SPEED") is not None:
        raw = os.environ["ELEVENLABS_SPEED"]
        source = "ELEVENLABS_SPEED environment override"
    else:
        raw = 1.18
        source = "maintained default"
    try:
        value = float(raw)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid ElevenLabs speed from {source}: {raw!r}") from error
    if not 0.7 <= value <= 1.2:
        raise ValueError(f"ElevenLabs speed from {source} must be between 0.7 and 1.2; got {value}")
    return value, source


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
    speed: float,
) -> None:
    import urllib.request
    api_key = os.environ["ELEVENLABS_API_KEY"]
    # Default voice: Leo v2 — reads measured and authoritative for technical
    # narration. Override per call with --voice, or globally with
    # ELEVENLABS_VOICE_ID. Rachel (21m00Tcm4TlvDq8ikWAM) is warmer/conversational.
    voice = voice_id or os.getenv("ELEVENLABS_VOICE_ID") or "bbGtsRRKUfYO634UxSjz"  # Leo v2, default
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=pcm_22050"
    # v4 has no API speed control. Its final WAV is duration-matched by the
    # caller to a same-text v2 reference at narration.speed (default 1.18).
    payload = {
        "text": text,
        "model_id": model_id
        or os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
        "voice_settings": {
            "stability":        float(os.getenv("ELEVENLABS_STABILITY",  "0.55")),
            "similarity_boost": float(os.getenv("ELEVENLABS_SIMILARITY", "0.75")),
        },
    }
    if payload["model_id"] not in V4_MODELS:
        payload["voice_settings"]["speed"] = speed
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


def approved_chunks(text: str, audio: dict) -> list[str] | None:
    """Accept explicit same-text chunk plans; never invent chunk boundaries."""
    chunks = audio.get("synthesis_chunks")
    if chunks is None:
        return None
    if not isinstance(chunks, list) or len(chunks) < 2 or any(not isinstance(x, str) or not x.strip() for x in chunks):
        raise ValueError("audio.synthesis_chunks must contain at least two nonempty strings")
    if " ".join(" ".join(chunks).split()) != " ".join(text.split()):
        raise ValueError("audio.synthesis_chunks must preserve the complete script's spoken text and order")
    return chunks


def synth_chunks(chunks: list[str], out_wav: Path, synth) -> None:
    """Join native PCM with no trimming, gain changes, fades or time stretching.

    Keep the previous output until all requests have succeeded and all parts
    use the course's standard format. The same synthesis closure is used for
    every part, preserving provider, model, voice and pacing.
    """
    with tempfile.TemporaryDirectory(prefix="academy-narration-", dir=out_wav.parent) as directory:
        temporary = Path(directory)
        parts = []
        for index, text in enumerate(chunks):
            part = temporary / f"part_{index:02}.wav"
            synth(text, part)
            with wave.open(str(part), "rb") as reader:
                if (reader.getnchannels(), reader.getsampwidth(), reader.getframerate(), reader.getcomptype()) != (1, 2, 22050, "NONE"):
                    raise ValueError("Chunked narration requires 22050 Hz mono 16-bit PCM WAV parts")
                pcm = reader.readframes(reader.getnframes())
                if not pcm:
                    raise ValueError("Chunked narration returned an empty part")
                parts.append(pcm)
        assembled = temporary / "assembled.wav"
        with wave.open(str(assembled), "wb") as writer:
            writer.setparams((1, 2, 22050, 0, "NONE", "not compressed"))
            writer.writeframes(b"".join(parts))
        assembled.replace(out_wav)


def slide_ref(mod: dict, slide: dict) -> str:
    return f"M{mod.get('id')}S{slide.get('id')} ({slide.get('type')}, {slide.get('slug', 'no-slug')})"


def iter_module_slides(
    course: dict,
    module_filter: int | None,
    slide_filter: int | None,
):
    for mod in course.get("modules", []):
        if module_filter and mod.get("id") != module_filter:
            continue
        for slide in mod.get("slides", []):
            if slide_filter and slide.get("id") != slide_filter:
                continue
            yield mod, slide


def main():
    p = argparse.ArgumentParser()
    p.add_argument("course_json", type=Path)
    p.add_argument("--module", type=int)
    p.add_argument(
        "--slide",
        type=int,
        help="synthesize only this slide id (normally combined with --module)",
    )
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
    p.add_argument("--pacing-reference-root", type=Path,
                   help="snapshot of paired, unchanged v2 scripts/WAVs at narration.speed; paths mirror course.json")
    p.add_argument("--audio-work-dir", type=Path,
                   help="timing cache, native v4 masters and receipts (default: <course>/_narration_work)")
    args = p.parse_args()

    course = json.loads(args.course_json.read_text())
    if str(course.get("style") or "Slides").strip().casefold() == "scrolling":
        print("Scrolling style has no narration by default; no audio generated.")
        return
    out_dir = args.course_json.resolve().parent
    work_dir = (args.audio_work_dir or out_dir / "_narration_work").resolve()
    reference_root = args.pacing_reference_root
    if reference_root and reference_root.resolve() == out_dir:
        sys.exit("Snapshot the baseline course's paired scripts/WAVs to a separate reference root first")
    reference_course = None
    if reference_root:
        metadata = reference_root / "course.json"
        if not metadata.is_file():
            sys.exit("Pacing reference root must include the baseline course.json to verify voice/model/speed")
        reference_course = json.loads(metadata.read_text())
    plans = {}
    jobs = []
    errors: list[str] = []
    for mod, slide in iter_module_slides(course, args.module, args.slide):
        key = id(mod)
        if key not in plans:
            effective = {**course, "narration": {
                **narration_config(course), **narration_config(mod),
            }}
            try:
                engine = pick_engine(args.engine, effective)
                model = pick_model_id(effective, engine, args.model, args.model_policy)
                speed, speed_source = pick_elevenlabs_speed(effective) if engine == "elevenlabs" else (None, None)
                voice = pick_voice_id(args.voice, effective, engine)
                language = primary_language_code(course.get("language")) if engine == "elevenlabs" else None
            except ValueError as error:
                sys.exit(str(error))
            plans[key] = dict(engine=engine, model=model, voice=voice, speed=speed,
                              language=language, existing=0, missing_quiz=False)
            print(f"module {mod.get('id')}: engine={engine}; voice={voice}; model={model}; speed={speed} ({speed_source if speed is not None else 'not applicable'})")
            if model in V4_MODELS:
                print(f"  pacing: match same-text Multilingual v2 at {speed:g}; learner dial remains unchanged")
                if reference_course is not None:
                    reference_mod = next((m for m in reference_course.get("modules", []) if m.get("id") == mod.get("id")), {})
                    recorded = {**narration_config(reference_course), **narration_config(reference_mod)}
                    if (recorded.get("engine", "elevenlabs") != "elevenlabs"
                        or recorded.get("model_id") != "eleven_multilingual_v2"
                        or recorded.get("voice_id") != voice
                        or float(recorded.get("speed", 1.18)) != speed):
                        sys.exit(f"Module {mod.get('id')} timing reference must record the same ElevenLabs voice, Multilingual v2, and speed {speed:g}")
        plan = plans[key]
        audio = slide.get("audio") or {}
        script_rel, wav_rel = audio.get("script_file"), audio.get("wav_file")
        quiz = slide.get("type") == "knowledge_check"
        if quiz and (not script_rel or not wav_rel):
            errors.append(f"{slide_ref(mod, slide)} missing audio.script_file/audio.wav_file")
        if not script_rel or not wav_rel:
            continue
        script_path, wav_path = out_dir / script_rel, out_dir / wav_rel
        plan["existing"] += int(wav_path.exists())
        plan["missing_quiz"] |= quiz and (args.force or not wav_path.exists())
        jobs.append((mod, slide, script_path, wav_path))
    if not jobs:
        sys.exit("No narration jobs match the selected module/slide")
    for plan in plans.values():
        if plan["engine"] == "say" and any(p["existing"] for p in plans.values()) and plan["missing_quiz"] and not args.allow_local_fallback_for_partial and not args.force:
            errors.append("refusing local knowledge-check narration in a partially narrated module; use the same cloud voice or explicitly approve --allow-local-fallback-for-partial")
    # Validate every requested script, chunk plan and timing source before paid text.
    references = {}
    active_plans = {}
    for mod, slide, script_path, wav_path in jobs:
        if wav_path.exists() and not args.force:
            continue
        plan = plans[id(mod)]
        active_plans[id(mod)] = plan
        if not script_path.is_file():
            errors.append(f"{slide_ref(mod, slide)} missing script: {script_path}")
            continue
        try:
            text = spoken_script(script_path)
            if not text:
                raise ValueError("Empty narration script")
            chunks = approved_chunks(text, slide.get("audio") or {})
            if chunks and plan["engine"] == "say":
                raise ValueError("Chunked narration requires the approved cloud provider")
            if plan["model"] in V4_MODELS:
                find_ffmpeg()
                if reference_root:
                    audio = slide["audio"]
                    references[str(wav_path)] = reference_files(reference_root, audio["script_file"], audio["wav_file"], text)
        except (RuntimeError, ValueError, OSError, EOFError, wave.Error) as error:
            errors.append(f"{slide_ref(mod, slide)}: {error}")
    if errors:
        sys.exit("Audio generation blocked before synthesis:\n  - " + "\n  - ".join(errors))
    validated = set()
    for plan in active_plans.values():
        if plan["engine"] != "elevenlabs":
            continue
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            sys.exit("Audio generation blocked before synthesis: ELEVENLABS_API_KEY is not set")
        models = [plan["model"]]
        if plan["model"] in V4_MODELS:
            models.append("eleven_multilingual_v2")
        for model in models:
            key = (model, plan["language"], plan["voice"])
            if key in validated:
                continue
            try:
                source = validate_model_language(model, course.get("language"), api_key=api_key)
                voice_source = validate_voice_model(model, plan["voice"], api_key=api_key)
            except (RuntimeError, ValueError) as error:
                sys.exit(str(error))
            validated.add(key)
            print(f"preflight: {model}/{plan['language']}: {source}; {voice_source}")
    if any(plan["model"] in V4_MODELS for plan in active_plans.values()) and not reference_root:
        print("v4 timing: reuse a cached v2 reference or synthesize one extra v2 timing clip per new script; native masters/receipts: " + str(work_dir))

    def render_with_plan(text, path, plan, chunks, model=None):
        def request(part_text, part_path):
            if plan["engine"] == "elevenlabs":
                synth_elevenlabs(part_text, part_path, plan["voice"], model or plan["model"], plan["language"], plan["speed"])
            elif plan["engine"] == "openai":
                synth_openai(part_text, part_path, plan["voice"])
            else:
                synth_say(part_text, part_path)
        if chunks:
            synth_chunks(chunks, path, request)
        else:
            request(text, path)

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
            chunks = approved_chunks(text, slide.get("audio") or {})
            plan = plans[id(mod)]
            if plan["model"] in V4_MODELS:
                identity = {
                    "model_id": plan["model"], "voice_id": plan["voice"],
                    "reference_model_id": "eleven_multilingual_v2",
                    "reference_speed": plan["speed"], "language": plan["language"],
                    "stability": float(os.getenv("ELEVENLABS_STABILITY", "0.55")),
                    "similarity_boost": float(os.getenv("ELEVENLABS_SIMILARITY", "0.75")),
                    "chunks": chunks,
                }
                receipt = synth_duration_matched(
                    text, wav_path, work_dir=work_dir, identity=identity,
                    synth_native=lambda value, path: render_with_plan(value, path, plan, chunks),
                    synth_reference=lambda value, path: render_with_plan(value, path, plan, chunks, "eleven_multilingual_v2"),
                    reference=references.get(str(wav_path)),
                )
                print(f"  pacing: {receipt['native_seconds']:.3f}s native -> {receipt['final_seconds']:.3f}s; target {receipt['target_seconds']:.3f}s; atempo {receipt['tempo_factor']:.6f}")
            else:
                render_with_plan(text, wav_path, plan, chunks)
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
                    "      export ELEVENLABS_API_KEY=<your key>\n"
                    + "      " + shlex.join([sys.executable, str(Path(__file__).resolve()), str(args.course_json.resolve()), *sys.argv[2:]])
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

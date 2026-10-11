#!/usr/bin/env python3
"""Generate only the seven approved replacement clips, with timing alignment.

Run with --generate on the Mac when ElevenLabs is reachable. The key is read
from the environment or a hidden prompt, never written to the course project.
The default --check action makes no network requests and incurs no charges.
"""
from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import wave
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT
STAGE = Path(os.environ.get("ACADEMY_ANIMATION_COURSE_DIR", ROOT)).resolve()
PLAN_PATH = ROOT / "animations/plan.json"
SKILL = Path(os.environ.get("ACADEMY_WIZARD_SKILL_DIR", ROOT.parents[1] / "skills/academy-wizard")) / "scripts"
sys.path.insert(0, str(SKILL))
from elevenlabs_model_support import validate_model_language, validate_voice_model


def spoken_body(script: str) -> str:
    return "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("#")).strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clips(manifest: dict):
    for module in manifest["modules"]:
        for slide in module["slides"]:
            yield f"M{module['id']}S{slide['id']}", slide["audio"]


def provenance(text: str, config: dict) -> dict:
    return {
        "script_sha256": digest(text.encode()),
        "voice_id": config["voice_id"],
        "model_id": config["model_id"],
        "voice_settings": {key: config[key] for key in ("speed", "stability", "similarity_boost")},
        "output_format": "pcm_22050",
    }


def current(wav: Path, alignment: Path, expected: dict) -> bool:
    if not wav.exists() or not alignment.exists():
        return False
    try:
        data = json.loads(alignment.read_text())
    except (OSError, ValueError):
        return False
    return all(data.get(key) == value for key, value in expected.items()) and data.get("wav_sha256") == digest(wav.read_bytes())


def validate_alignment(data: dict, duration: float) -> None:
    alignment = data.get("alignment") or data.get("normalized_alignment")
    if not isinstance(alignment, dict):
        raise ValueError("The response contains no character alignment.")
    chars = alignment.get("characters", [])
    starts = alignment.get("character_start_times_seconds", [])
    ends = alignment.get("character_end_times_seconds", [])
    if not chars or len(chars) != len(starts) or len(chars) != len(ends):
        raise ValueError("Character alignment lengths do not match.")
    if any(start < 0 or end < start or end > duration + 0.1 for start, end in zip(starts, ends)):
        raise ValueError("Character timing is outside the audio duration.")
    if any(b < a for a, b in zip(starts, starts[1:])):
        raise ValueError("Character starts are not monotonic.")


def generate(text: str, config: dict, key: str) -> tuple[bytes, dict]:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config['voice_id']}/with-timestamps?output_format=pcm_22050"
    payload = {"text": text, "model_id": config["model_id"], "voice_settings": provenance(text, config)["voice_settings"]}
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST", headers={
        "xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json",
    })
    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.load(response)
    pcm = base64.b64decode(data["audio_base64"], validate=True)
    if len(pcm) < 44100 or len(pcm) % 2:
        raise ValueError("Invalid mono 16-bit PCM response.")
    validate_alignment(data, len(pcm) / 44100)
    return pcm, {key: data[key] for key in ("alignment", "normalized_alignment") if data.get(key)}


def approve(plan: dict, texts: dict) -> None:
    if plan["scripts_approved"] and plan["new_single_pass_mode_approved"]:
        if plan.get("approved_script_sha256") != texts:
            raise RuntimeError("Scripts changed after approval; review and approve the revisions again.")
        return
    print(f"Review the seven narration scripts under:\n{STAGE / 'audio'}")
    print("All six videos will follow narration pause, seek, replay and speed, then hold their final state.")
    if input("Type APPROVE to approve these exact scripts and all six synchronized videos: ").strip() != "APPROVE":
        raise RuntimeError("No approval recorded. No audio generated.")
    if any(digest(spoken_body((STAGE / path).read_text()).encode()) != sha for path, sha in texts.items()):
        raise RuntimeError("A script changed during review. Review the updated text and run the helper again.")
    record_approval(plan, texts, "Human confirmation in local narration helper", "APPROVE")


def record_approval(plan: dict, texts: dict, source: str, confirmation: str) -> None:
    plan.update(scripts_approved=True, new_single_pass_mode_approved=True,
                approved_script_sha256=texts, script_and_mode_approval={
                    "source": source,
                    "confirmation": confirmation, "date": datetime.now(timezone.utc).isoformat(),
                })
    PLAN_PATH.write_text(json.dumps(plan, indent=2) + "\n")
    for path in texts:
        script = STAGE / path
        lines = script.read_text().splitlines()
        lines = [f"# review_status: approved; {source}" if line.startswith("# review_status:") else line for line in lines]
        script.write_text("\n".join(lines) + "\n")
    for name in ("course.json",):
        course_path = STAGE / name
        course = json.loads(course_path.read_text())
        for module in course["modules"]:
            for slide in module["slides"]:
                if slide.get("audio", {}).get("script_file") in texts:
                    slide["audio"]["approved"] = True
        if name == "course.json":
            course["animation_upgrade"].update(script_approval=True, single_pass_mode_approved=True,
                                                script_and_mode_approval=plan["script_and_mode_approval"],
                                                status="approved; awaiting final narration and media QA")
        course_path.write_text(json.dumps(course, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--force", action="store_true", help="explicitly replace stale staged clips")
    args = parser.parse_args()
    plan = json.loads(PLAN_PATH.read_text())
    course = json.loads((STAGE / "course.json").read_text())
    wanted = {(video['module'], video['slide']) for video in plan['videos'] + plan['additional_narration']}
    manifest = {'language': course['language'], 'narration': course['narration'], 'modules': []}
    for module in course['modules']:
        slides = [slide for slide in module['slides'] if (module['id'], slide['id']) in wanted]
        if slides:
            manifest['modules'].append({'id': module['id'], 'slides': slides})
    config = plan["narration"]
    selected = list(clips(manifest))
    if len(selected) != 7:
        raise RuntimeError("The replacement manifest must contain exactly seven clips.")
    texts = {audio["script_file"]: digest(spoken_body((STAGE / audio["script_file"]).read_text()).encode()) for _, audio in selected}
    pending = []
    for label, audio in selected:
        text = spoken_body((STAGE / audio["script_file"]).read_text())
        wav = STAGE / audio["wav_file"]
        alignment = (STAGE / audio["script_file"]).with_suffix(".alignment.json")
        expected = provenance(text, config)
        valid = current(wav, alignment, expected)
        print(f"{label}: {'current' if valid else 'needs narration'}; {len(text.split())} words")
        if not valid:
            if wav.exists() and not args.force:
                raise RuntimeError(f"Stale staged clip: {label}. Use --force only after reviewing the replacement.")
            pending.append((label, text, wav, alignment, expected))
    if not args.generate:
        print("Check only: no network requests, no billable generation, no course changes.")
        return
    approve(plan, texts)
    if pending:
        key = os.environ.get("ELEVENLABS_API_KEY") or getpass.getpass("ElevenLabs API key (hidden, not saved): ")
        if not key.strip():
            raise RuntimeError("An ElevenLabs key is required. No fallback voice will be used.")
        print(validate_model_language(config["model_id"], manifest.get("language"), api_key=key))
        print(validate_voice_model(config["model_id"], config["voice_id"], api_key=key))
        for label, text, wav, alignment_path, expected in pending:
            script_path = next(STAGE / audio['script_file'] for current_label, audio in selected if current_label == label)
            if spoken_body(script_path.read_text()) != text:
                raise RuntimeError(f"{label} changed after approval; no replacement was generated for it.")
            print(f"Generating {label} with the approved Leo voice and 1.18 pacing...")
            pcm, alignment = generate(text, config, key)
            temporary = wav.with_suffix(".pending.wav")
            with wave.open(str(temporary), "wb") as output:
                output.setnchannels(1)
                output.setsampwidth(2)
                output.setframerate(22050)
                output.writeframes(pcm)
            record = {**expected, **alignment, "wav_sha256": digest(temporary.read_bytes()),
                      "generated_at": datetime.now(timezone.utc).isoformat()}
            temporary_alignment = alignment_path.with_suffix(".pending.json")
            temporary_alignment.write_text(json.dumps(record, indent=2) + "\n")
            temporary.replace(wav)
            temporary_alignment.replace(alignment_path)
    with tempfile.NamedTemporaryFile(mode='w', dir=STAGE, suffix='.json') as report:
        json.dump(manifest, report)
        report.flush()
        subprocess.run([sys.executable, str(SKILL / "audio_tail_report.py"), report.name, "--fail-on-flags"], check=True)
    print("Seven clips ready for listening and measured video rendering. No HTML or ZIP was built.")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        sys.exit(f"ElevenLabs request failed (HTTP {error.code}); no alternate voice or automatic retry used.")
    except urllib.error.URLError:
        sys.exit("ElevenLabs is unreachable. Resume from the same helper when the connection is available.")
    except (RuntimeError, ValueError) as error:
        sys.exit(str(error))

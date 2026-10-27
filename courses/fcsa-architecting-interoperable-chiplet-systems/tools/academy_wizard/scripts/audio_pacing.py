"""Match native v4 narration to a v2 timing reference without changing pitch.

Working masters and receipts stay outside the manifest's runtime file list.
Never pad or truncate speech to manufacture the target duration.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

V4_MODELS = frozenset({"eleven_v4", "eleven_v4_turbo"})
DURATION_TOLERANCE_SECONDS = 0.05


def find_ffmpeg() -> str:
    executable = shutil.which("ffmpeg")
    if executable:
        return executable
    try:
        import imageio_ffmpeg
        executable = imageio_ffmpeg.get_ffmpeg_exe()
        if Path(executable).is_file():
            return executable
    except (ImportError, RuntimeError):
        pass
    raise RuntimeError(
        "Duration-matched v4 requires ffmpeg (on PATH or provided by "
        "imageio_ffmpeg). Install it before sending billable text."
    )


def spoken_script(path: Path) -> str:
    return "\n".join(
        line for line in path.read_text(encoding="utf-8").splitlines()
        if not line.startswith("#")
    ).strip()


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as reader:
        duration = reader.getnframes() / reader.getframerate()
        if reader.getcomptype() != "NONE" or not math.isfinite(duration) or duration <= 0:
            raise ValueError(f"Invalid PCM timing reference: {path}")
        return duration


def reference_files(root: Path, script_rel: str, wav_rel: str, text: str) -> Path:
    """Require the unchanged paired script, not just a similarly named WAV."""
    root = root.resolve()
    script = (root / script_rel).resolve()
    wav = (root / wav_rel).resolve()
    if not script.is_relative_to(root) or not wav.is_relative_to(root):
        raise ValueError("Pacing reference paths must remain inside the reference root")
    if not script.is_file() or not wav.is_file():
        raise ValueError(f"Missing paired timing reference script/WAV: {wav}")
    if " ".join(spoken_script(script).split()) != " ".join(text.split()):
        raise ValueError(f"Timing reference script differs from the current narration: {script}")
    wav_duration(wav)
    return wav


def match_wav_duration(native: Path, output: Path, target_seconds: float, *, ffmpeg: str | None = None) -> dict:
    """Use atempo, iterating on encoder rounding; replace only on success."""
    executable = ffmpeg or find_ffmpeg()
    if not math.isfinite(target_seconds) or target_seconds <= 0:
        raise ValueError("Target narration duration must be positive and finite")
    native_seconds = wav_duration(native)
    factor = native_seconds / target_seconds
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".pacing-", dir=output.parent) as directory:
        candidate = Path(directory) / "matched.wav"
        for _ in range(3):
            # atempo is pitch preserving; chain modest factors for all ratios.
            remainder = factor
            filters = []
            while remainder > 2:
                filters.append("atempo=2")
                remainder /= 2
            while remainder < 0.5:
                filters.append("atempo=0.5")
                remainder /= 0.5
            filters.append(f"atempo={remainder:.12f}")
            result = subprocess.run(
                [executable, "-hide_banner", "-nostdin", "-loglevel", "error", "-y",
                 "-i", str(native), "-af", ",".join(filters), "-ar", "22050",
                 "-ac", "1", "-c:a", "pcm_s16le", str(candidate)],
                capture_output=True, text=True,
            )
            if result.returncode:
                raise RuntimeError(f"Pitch-preserving pacing failed: {result.stderr[-1000:]}")
            actual_seconds = wav_duration(candidate)
            if abs(actual_seconds - target_seconds) <= DURATION_TOLERANCE_SECONDS:
                candidate.replace(output)
                return {
                    "native_seconds": native_seconds,
                    "target_seconds": target_seconds,
                    "final_seconds": actual_seconds,
                    "duration_error_seconds": actual_seconds - target_seconds,
                    "tempo_factor": factor,
                    "method": "ffmpeg atempo; pitch preserved; no padding or trimming",
                }
            factor *= actual_seconds / target_seconds
    raise RuntimeError("Could not match narration within 50 ms; previous output preserved")


def synth_duration_matched(
    text: str, output: Path, *, work_dir: Path, identity: dict,
    synth_native, synth_reference, reference: Path | None = None,
) -> dict:
    """Cache a v2 reference, retain the native master, and pace the final WAV."""
    executable = find_ffmpeg()  # Must fail before either paid callback.
    settings = {**identity, "text_sha256": hashlib.sha256(text.encode()).hexdigest()}
    cache_key = hashlib.sha256(json.dumps(settings, sort_keys=True).encode()).hexdigest()
    cache = work_dir / cache_key
    cache.mkdir(parents=True, exist_ok=True)
    cached_reference = cache / "reference-v2.wav"
    if reference is not None:
        target_seconds = wav_duration(reference)
        # The timing reference must survive later retries or output replacement.
        if reference.resolve() != cached_reference.resolve():
            shutil.copy2(reference, cached_reference)
        reference_source = str(reference.resolve())
    elif cached_reference.is_file():
        target_seconds = wav_duration(cached_reference)
        reference_source = "cached v2 synthesis"
    else:
        with tempfile.TemporaryDirectory(prefix="reference-", dir=cache) as directory:
            temporary_reference = Path(directory) / "reference.wav"
            synth_reference(text, temporary_reference)
            target_seconds = wav_duration(temporary_reference)
            temporary_reference.replace(cached_reference)
        reference_source = "new v2 synthesis"
    with tempfile.TemporaryDirectory(prefix="native-", dir=cache) as directory:
        native = Path(directory) / "native.wav"
        synth_native(text, native)
        wav_duration(native)
        receipt = match_wav_duration(native, output, target_seconds, ffmpeg=executable)
        native.replace(cache / "native-v4.wav")
    receipt.update({
        **settings, "reference_source": reference_source,
        "reference_sha256": hashlib.sha256(cached_reference.read_bytes()).hexdigest(),
        "native_master": str((cache / "native-v4.wav").resolve()),
        "output": str(output.resolve()),
        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    })
    temporary_receipt = cache / f"receipt-{os.getpid()}.tmp"
    temporary_receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    temporary_receipt.replace(cache / "receipt.json")
    return receipt

#!/usr/bin/env python3
"""Mix localized narration with reusable AcademyWizard background music."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_FFMPEG = Path("/Applications/Logi Tune.app/Contents/Resources/ffmpeg/ffmpeg")


def find_ffmpeg() -> str:
    configured = os.environ.get("FFMPEG")
    if configured:
        return configured
    discovered = shutil.which("ffmpeg")
    if discovered:
        return discovered
    if DEFAULT_FFMPEG.exists():
        return str(DEFAULT_FFMPEG)
    raise FileNotFoundError("ffmpeg was not found; set FFMPEG or install ffmpeg")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True)


def media_duration(ffmpeg: str, path: Path) -> float:
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    match = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr)
    if not match:
        raise RuntimeError(f"Could not determine media duration: {path}")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=(
            "Replace a video's source audio with localized narration over a normalized, "
            "automatically ducked AcademyWizard music track."
        )
    )
    command.add_argument("--video", required=True, type=Path, help="Source video; only its video stream is mapped")
    command.add_argument("--voice", required=True, type=Path, help="Time-aligned localized voice-only master")
    command.add_argument("--music", required=True, type=Path, help="Background music asset")
    command.add_argument("--output", required=True, type=Path, help="Localized MP4 output")
    command.add_argument("--mixed-wav", type=Path, help="Optional PCM master for the final mixed audio")
    command.add_argument("--report-json", type=Path, help="Optional machine-readable production report")
    command.add_argument("--language-tag", required=True, help="ISO 639-2 audio tag, such as kor, jpn, or zho")
    command.add_argument("--audio-title", default="Localized narration with background music")
    command.add_argument("--target-lufs", type=float, default=-27.0)
    command.add_argument("--fade-in-seconds", type=float, default=1.5)
    command.add_argument("--fade-out-seconds", type=float, default=4.0)
    command.add_argument("--duck-threshold", type=float, default=0.03)
    command.add_argument("--duck-ratio", type=float, default=8.0)
    command.add_argument("--duck-attack-ms", type=float, default=150.0)
    command.add_argument("--duck-release-ms", type=float, default=650.0)
    return command


def main() -> None:
    args = parser().parse_args()
    ffmpeg = find_ffmpeg()
    video = args.video.resolve()
    voice = args.voice.resolve()
    music = args.music.resolve()
    output = args.output.resolve()
    for source in (video, voice, music):
        if not source.is_file():
            raise FileNotFoundError(source)
    if output == video:
        raise ValueError("Output must not overwrite the source video")

    video_duration = media_duration(ffmpeg, video)
    music_duration = media_duration(ffmpeg, music)
    repeat_music = music_duration + 0.05 < video_duration
    if repeat_music:
        print(
            f"WARNING: video is {video_duration:.2f}s but {music.name} is "
            f"{music_duration:.2f}s; repeating the complete track without a crossfade.",
            file=sys.stderr,
        )

    fade_out = min(max(args.fade_out_seconds, 0.0), video_duration)
    fade_out_start = max(0.0, video_duration - fade_out)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.mixed_wav:
        args.mixed_wav.resolve().parent.mkdir(parents=True, exist_ok=True)
    if args.report_json:
        args.report_json.resolve().parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="academy-video-mix-") as temp:
        mixed_audio = Path(temp) / "localized-mix.wav"
        music_input = ["-stream_loop", "-1"] if repeat_music else []
        filter_graph = (
            f"[0:a]atrim=0:{video_duration:.3f},asetpts=N/SR/TB,aresample=48000,"
            f"loudnorm=I={args.target_lufs}:TP=-3:LRA=7,"
            f"afade=t=in:st=0:d={args.fade_in_seconds},"
            f"afade=t=out:st={fade_out_start:.3f}:d={fade_out},"
            "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[music];"
            "[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,"
            "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            "asplit=2[voice_mix][voice_sc];"
            f"[music][voice_sc]sidechaincompress=threshold={args.duck_threshold}:"
            f"ratio={args.duck_ratio}:attack={args.duck_attack_ms}:"
            f"release={args.duck_release_ms}:knee=4:link=maximum[ducked];"
            "[ducked][voice_mix]amix=inputs=2:normalize=0:duration=first,"
            "alimiter=limit=0.95:attack=5:release=50:level=false[final]"
        )
        run([
            ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
            *music_input, "-i", str(music), "-i", str(voice),
            "-filter_complex", filter_graph, "-map", "[final]", "-t", f"{video_duration:.3f}",
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(mixed_audio),
        ])
        run([
            ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(video), "-i", str(mixed_audio), "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-metadata:s:a:0", f"language={args.language_tag}",
            "-metadata:s:a:0", f"title={args.audio_title}", "-movflags", "+faststart",
            "-shortest", str(output),
        ])
        if args.mixed_wav:
            shutil.copy2(mixed_audio, args.mixed_wav.resolve())

    report = {
        "schema_version": 1,
        "method": "localized narration over normalized sidechain-ducked background music",
        "video": str(video),
        "video_duration_seconds": round(video_duration, 3),
        "voice": str(voice),
        "voice_sha256": sha256(voice),
        "music": str(music),
        "music_sha256": sha256(music),
        "music_duration_seconds": round(music_duration, 3),
        "music_repeated": repeat_music,
        "repeat_method": "complete-track end-to-start without crossfade" if repeat_music else None,
        "mix": {
            "music_target_lufs": args.target_lufs,
            "fade_in_seconds": args.fade_in_seconds,
            "fade_out_seconds": fade_out,
            "duck_threshold": args.duck_threshold,
            "duck_ratio": args.duck_ratio,
            "duck_attack_ms": args.duck_attack_ms,
            "duck_release_ms": args.duck_release_ms,
            "source_audio_streams_mapped": 0,
        },
        "output": str(output),
        "output_sha256": sha256(output),
        "output_bytes": output.stat().st_size,
    }
    if args.mixed_wav:
        report["mixed_wav"] = str(args.mixed_wav.resolve())
        report["mixed_wav_sha256"] = sha256(args.mixed_wav.resolve())
    if args.report_json:
        args.report_json.resolve().write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

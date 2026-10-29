"""Pace full Eleven v4 narration with pitch preserved and no reference synthesis."""
from __future__ import annotations
import hashlib,json,math,os,shutil,subprocess,tempfile,wave
from pathlib import Path
V4_MODELS=frozenset({'eleven_v4'})
DURATION_TOLERANCE_SECONDS=0.05

def find_ffmpeg():
    executable=shutil.which('ffmpeg')
    if executable:return executable
    try:
        import imageio_ffmpeg
        executable=imageio_ffmpeg.get_ffmpeg_exe()
        if Path(executable).is_file():return executable
    except (ImportError,RuntimeError):pass
    raise RuntimeError('Paced narration requires ffmpeg before synthesis.')

def spoken_script(path):
    return '\n'.join(line for line in path.read_text(encoding='utf-8').splitlines() if not line.startswith('#')).strip()

def wav_duration(path):
    with wave.open(str(path),'rb') as reader:
        duration=reader.getnframes()/reader.getframerate()
        if reader.getcomptype()!='NONE' or not math.isfinite(duration) or duration<=0:
            raise ValueError(f'Invalid PCM narration: {path}')
        return duration

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


def synth_paced(text,output,*,work_dir,identity,synth_native,speed=1.18):
    """Make one full-model master, then apply the recorded tempo multiplier."""
    executable=find_ffmpeg()
    if not 0.7<=speed<=1.2:raise ValueError('Narration tempo must be between 0.7 and 1.2')
    if identity.get('model_id')!='eleven_v4':raise ValueError('Narration requires eleven_v4')
    settings={**identity,'tempo_multiplier':speed,'text_sha256':hashlib.sha256(text.encode()).hexdigest()}
    key=hashlib.sha256(json.dumps(settings,sort_keys=True).encode()).hexdigest()
    cache=work_dir/key;cache.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='native-',dir=cache) as directory:
        native=Path(directory)/'native.wav'
        synth_native(text,native)
        duration=wav_duration(native)
        receipt=match_wav_duration(native,output,duration/speed,ffmpeg=executable)
        native.replace(cache/'native-v4.wav')
    receipt.update({**settings,'native_master':str((cache/'native-v4.wav').resolve()),
        'native_sha256':hashlib.sha256((cache/'native-v4.wav').read_bytes()).hexdigest(),
        'output':str(output.resolve()),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'synthesis_calls':'Full Eleven v4 only; no reference model or fallback.'})
    temp=cache/f'receipt-{os.getpid()}.tmp';temp.write_text(json.dumps(receipt,indent=2)+'\n');temp.replace(cache/'receipt.json')
    return receipt

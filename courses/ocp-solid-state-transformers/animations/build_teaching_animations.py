#!/usr/bin/env python3
"""Regenerate the four silent SST teaching animations and their posters."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FIGURES = ROOT.parent / "figures"
FONT_PATHS = [
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("/Library/Fonts/Arial.ttf"),
]
FONT_BOLD_PATHS = [
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/Library/Fonts/Arial Bold.ttf"),
]


def font(size: int, bold: bool = False):
    for path in FONT_BOLD_PATHS if bold else FONT_PATHS:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def rounded(draw, xy, fill, outline=None, width=2, radius=20):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def make_video(name: str, draw_frame, seconds: float = 8.0, fps: int = 20) -> None:
    width, height = 1280, 720
    FIGURES.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        try:
            import imageio_ffmpeg

            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError as error:
            raise RuntimeError("ffmpeg or imageio-ffmpeg is required") from error

    output = FIGURES / name
    proc = subprocess.Popen(
        [
            ffmpeg,
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            "-r",
            str(fps),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    first = None
    for frame_number in range(int(seconds * fps)):
        t = frame_number / fps
        image = Image.new("RGB", (width, height), "#121b31")
        draw_frame(ImageDraw.Draw(image), t, seconds)

        # Remove the former slide-like heading band without distorting the art.
        cropped = image.crop((0, 140, width, height))
        framed = Image.new("RGB", (width, height), "#121b31")
        framed.paste(cropped, (0, 60))
        image = framed

        if first is None:
            first = image.copy()
        proc.stdin.write(image.tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed while rendering {name}")
    first.save(FIGURES / f"{Path(name).stem}_poster.png")


def voltage_current_copper(draw, t, _seconds):
    phase = (t % 4.0) / 4.0
    lanes = [
        ("54 VDC", "18.5 kA", "Relative I²R: 219×", 235, "#f4b13d", 34),
        ("800 VDC", "1.25 kA", "Relative I²R: 1×", 470, "#8DC63F", 7),
    ]
    for label, current, loss, y, color, thickness in lanes:
        rounded(draw, (70, y - 55, 290, y + 80), "#ffffff")
        draw.text((95, y - 30), label, font=font(29, True), fill="#18283b")
        draw.text((95, y + 12), current, font=font(22), fill="#4b5b6b")
        draw.text((95, y + 44), loss, font=font(18), fill="#4b5b6b")
        draw.line((330, y, 1120, y), fill="#41546a", width=thickness)
        x = 350 + int(730 * phase)
        draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=color)
        rounded(draw, (1110, y - 48, 1220, y + 48), "#ffffff")
        draw.text((1136, y - 13), "1 MW", font=font(24, True), fill="#18283b")
    draw.text(
        (640, 650),
        "Idealized comparison · same power and resistance · not a conductor-sizing calculation",
        anchor="mm",
        font=font(18),
        fill="#d9e2eb",
    )


def conversion_path(draw, t, seconds):
    blocks = [
        ("MVAC", "13.8 or 34.5 kV"),
        ("Active input", "AC → controlled DC"),
        ("HF isolation", "MFT / HFT"),
        ("Output stage", "regulated DC"),
        ("800 VDC", "to distribution"),
    ]
    notes = [
        "MVAC establishes the grid-facing input",
        "The active stage shapes current and creates a DC link",
        "High-frequency isolation separates the voltage domains",
        "The output stage regulates the DC interface",
        "The 800 VDC interface feeds the downstream distribution",
    ]
    xs = [45, 285, 525, 765, 1005]
    stage_position = ((t % seconds) / seconds) * len(blocks)
    active = min(len(blocks) - 1, int(stage_position))

    for index, (title, subtitle) in enumerate(blocks):
        is_active = index == active
        rounded(
            draw,
            (xs[index], 255, xs[index] + 190, 430),
            "#edf8e3" if is_active else "#ffffff",
            outline="#8DC63F" if is_active or index in (1, 2, 3) else "#4aa3df",
            width=5 if is_active else 3,
        )
        draw.text((xs[index] + 95, 300), title, anchor="mm", font=font(25, True), fill="#18283b")
        draw.text((xs[index] + 95, 350), subtitle, anchor="mm", font=font(17), fill="#4b5b6b")
        if index < 4:
            start = xs[index] + 198
            end = xs[index + 1] - 12
            color = "#8DC63F" if index == active else "#52657a"
            draw.line((start, 342, end, 342), fill=color, width=4)
            draw.polygon([(end, 342), (end - 12, 334), (end - 12, 350)], fill=color)
            if index == active:
                local = stage_position - index
                for offset in (0.0, 0.33, 0.66):
                    progress = local - offset
                    if 0.05 <= progress <= 0.95:
                        px = int(start + (end - start) * progress)
                        draw.ellipse((px - 8, 334, px + 8, 350), fill="#8DC63F")

    rounded(draw, (210, 500, 1070, 610), "#253b50", outline="#8DC63F", width=2)
    draw.text((640, 532), f"ACTIVE STEP  {active + 1} / {len(blocks)}", anchor="mm", font=font(20, True), fill="#8DC63F")
    draw.text((640, 570), notes[active], anchor="mm", font=font(18), fill="#d9e2eb")
    draw.text(
        (640, 650),
        "Representative instructional topology · OCP v0.3 remains black-box and topology-neutral",
        anchor="mm",
        font=font(18),
        fill="#d9e2eb",
    )


def vrt_ess_response(draw, t, seconds):
    x0, y0, x1, y1 = 90, 240, 1190, 450
    draw.line((x0, y1, x1, y1), fill="#93a4b5", width=3)
    draw.line((x0, y0, x0, y1), fill="#93a4b5", width=3)
    points = []
    for x in range(x0, x1 + 1, 10):
        u = (x - x0) / (x1 - x0)
        sag = max(0, 1 - abs(u - 0.5) / 0.23)
        points.append((x, y1 - (1 - 0.72 * sag) * 170))
    draw.line(points, fill="#4aa3df", width=7)

    px = x0 + int((x1 - x0) * ((t % seconds) / seconds))
    u = (px - x0) / (x1 - x0)
    sag = max(0, 1 - abs(u - 0.5) / 0.23)
    voltage = 1 - 0.72 * sag
    py = y1 - voltage * 170
    draw.ellipse((px - 14, py - 14, px + 14, py + 14), fill="#8DC63F")

    region = "ACCEPTABLE" if voltage >= 0.9 else ("LVRT RANGE 1" if voltage >= 0.55 else "LVRT RANGE 2")
    sst = "SST supplies output" if voltage >= 0.9 else ("SST current ≤ nominal" if voltage >= 0.55 else "SST input current = 0")
    ess = "ESS idle / charging" if voltage >= 0.9 else ("ESS fills shortfall" if voltage >= 0.55 else "ESS supplies 100%")
    rounded(draw, (230, 500, 1050, 610), "#ffffff")
    draw.text((300, 530), region, font=font(25, True), fill="#18283b")
    draw.text((300, 570), sst, font=font(20), fill="#4b5b6b")
    draw.text((720, 570), ess, font=font(20, True), fill="#6FA030")
    draw.text(
        (640, 660),
        "Output remains supported · acceptable voltage/frequency return enables immediate recovery",
        anchor="mm",
        font=font(18),
        fill="#d9e2eb",
    )


def redundancy_fault_response(draw, t, seconds):
    fault_on = 2.8 < (t % seconds) < 6.3
    sst_xs = (70, 350, 630)
    bus_y = 455
    load_x = 1060

    for index, x in enumerate(sst_xs):
        bad = fault_on and index == 1
        rounded(
            draw,
            (x, 235, x + 220, 385),
            "#5c6674" if bad else "#ffffff",
            outline="#d95b61" if bad else "#8DC63F",
            width=5,
        )
        draw.text((x + 110, 280), f"SST {index + 1}", anchor="mm", font=font(27, True), fill="white" if bad else "#18283b")
        draw.text((x + 110, 330), "FAULT · ISOLATED" if bad else "AVAILABLE", anchor="mm", font=font(18, True), fill="#ffccd0" if bad else "#6FA030")

    draw.line((150, bus_y, 1070, bus_y), fill="#4aa3df", width=18)
    draw.line((load_x, 395, load_x, bus_y), fill="#4aa3df", width=18)
    for index, x in enumerate(sst_xs):
        draw.line((x + 110, 385, x + 110, bus_y), fill="#d95b61" if fault_on and index == 1 else "#8DC63F", width=8)

    rounded(draw, (930, 255, 1190, 395), "#ffffff")
    draw.text((1060, 300), "800 VDC LOAD", anchor="mm", font=font(24, True), fill="#18283b")
    draw.text((1060, 344), "supported" if fault_on else "normal", anchor="mm", font=font(20, True), fill="#6FA030")

    cycle = (t % 2.6) / 2.6
    for index, x in enumerate(sst_xs):
        if fault_on and index == 1:
            continue
        phase = (cycle + index * 0.28) % 1.0
        junction = x + 110
        if phase < 0.24:
            progress = phase / 0.24
            px = junction
            py = 385 + int((bus_y - 385) * progress)
        else:
            progress = (phase - 0.24) / 0.76
            px = junction + int((load_x - junction) * progress)
            py = bus_y
        draw.ellipse((px - 12, py - 12, px + 12, py + 12), fill="#8DC63F")

    draw.text((640, 565), "Fault isolation changes the active capacity path", anchor="mm", font=font(25, True), fill="#d9e2eb")
    draw.text(
        (640, 650),
        "Conceptual only · capacity, bus segmentation, clearing time, and load ride-through must be validated",
        anchor="mm",
        font=font(18),
        fill="#d9e2eb",
    )


def main() -> None:
    make_video("voltage_current_copper.mp4", voltage_current_copper)
    make_video("sst_conversion_path.mp4", conversion_path)
    make_video("vrt_ess_response.mp4", vrt_ess_response)
    make_video("redundancy_fault_response.mp4", redundancy_fault_response)


if __name__ == "__main__":
    main()

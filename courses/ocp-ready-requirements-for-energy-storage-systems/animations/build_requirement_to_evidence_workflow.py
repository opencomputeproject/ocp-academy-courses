#!/usr/bin/env python3
"""Build the silent Module 4 ESS deployment workflow animation."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

try:
    import imageio_ffmpeg
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError as exc:
    raise SystemExit("Install Pillow, NumPy, and imageio-ffmpeg before rendering this animation.") from exc


WIDTH, HEIGHT = 1280, 720
FPS = 24
DURATION = 14.0

WHITE = "#FFFFFF"
INK = "#343895"
GREEN = "#8DC63F"
GREEN_DARK = "#6FA030"
GREEN_PALE = "#F4F8F1"
MUTED = "#5F6062"
LINE = "#D8DCE8"
PALE_BLUE = "#F2F3FA"
AMBER = "#E6A23C"
RED = "#C7534F"

def available_font(*candidates: str) -> str:
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("Install Arial or DejaVu Sans, or update the font candidates in this script.")


FONT_REGULAR = available_font(
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
)
FONT_BOLD = available_font(
    "/System/Library/Fonts/Supplement/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
)

TITLE_FONT = ImageFont.truetype(FONT_BOLD, 40)
SUBTITLE_FONT = ImageFont.truetype(FONT_REGULAR, 21)
LABEL_FONT = ImageFont.truetype(FONT_BOLD, 24)
DETAIL_FONT = ImageFont.truetype(FONT_REGULAR, 17)
STEP_FONT = ImageFont.truetype(FONT_BOLD, 17)
LOOP_FONT = ImageFont.truetype(FONT_BOLD, 18)

CARD_W, CARD_H = 242, 122
TOP_Y, BOTTOM_Y = 170, 430
XS = [55, 364, 673, 982]

STEPS = [
    (1, "Use case", "business need", XS[0], TOP_Y, INK),
    (2, "Deployment", "location + topology", XS[1], TOP_Y, GREEN_DARK),
    (3, "Hazards", "credible risks", XS[2], TOP_Y, RED),
    (4, "Standards", "applicable stack", XS[3], TOP_Y, INK),
    (5, "Early review", "AHJ + insurer", XS[3], BOTTOM_Y, AMBER),
    (6, "Evidence", "tests + plans", XS[2], BOTTOM_Y, GREEN_DARK),
    (7, "Operations", "procedures", XS[1], BOTTOM_Y, INK),
    (8, "OCP feedback", "lessons learned", XS[0], BOTTOM_Y, GREEN_DARK),
]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def ease(value: float) -> float:
    value = clamp(value)
    return value * value * (3.0 - 2.0 * value)


def centered_text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=font, fill=fill)


def blend(hex_a: str, hex_b: str, amount: float) -> tuple[int, int, int]:
    amount = clamp(amount)
    a = tuple(int(hex_a[i : i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(hex_b[i : i + 2], 16) for i in (1, 3, 5))
    return tuple(round(a[i] + (b[i] - a[i]) * amount) for i in range(3))


def arrow_geometry(
    start: tuple[float, float], end: tuple[float, float], head_length: float = 18
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    back = (end[0] - math.cos(angle) * head_length, end[1] - math.sin(angle) * head_length)
    normal = (-math.sin(angle), math.cos(angle))
    return end, back, normal


def arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], progress: float, color: str = GREEN) -> None:
    progress = ease(progress)
    if progress <= 0:
        return
    x1, y1 = start
    tip, back, normal = arrow_geometry(start, end)
    line_progress = ease(clamp(progress / 0.8))
    px = x1 + (back[0] - x1) * line_progress
    py = y1 + (back[1] - y1) * line_progress
    draw.line((x1, y1, px, py), fill=color, width=8)
    head_progress = ease(clamp((progress - 0.8) / 0.2))
    if head_progress <= 0:
        return
    animated_tip = (
        back[0] + (tip[0] - back[0]) * head_progress,
        back[1] + (tip[1] - back[1]) * head_progress,
    )
    half_width = 10 * head_progress
    draw.polygon(
        [
            animated_tip,
            (back[0] + normal[0] * half_width, back[1] + normal[1] * half_width),
            (back[0] - normal[0] * half_width, back[1] - normal[1] * half_width),
        ],
        fill=color,
    )


def feedback_path(draw: ImageDraw.ImageDraw, progress: float) -> None:
    progress = ease(progress)
    if progress <= 0:
        return
    points = []
    for i in range(101):
        u = i / 100
        inv = 1 - u
        x = inv**3 * 55 + 3 * inv**2 * u * 2 + 3 * inv * u**2 * 2 + u**3 * 37
        y = inv**3 * 491 + 3 * inv**2 * u * 445 + 3 * inv * u**2 * 231 + u**3 * 231
        points.append((x, y))
    line_progress = ease(clamp(progress / 0.82))
    count = max(2, round((len(points) - 1) * line_progress) + 1)
    partial = points[:count]
    draw.line(partial, fill=GREEN, width=8, joint="curve")
    head_progress = ease(clamp((progress - 0.82) / 0.18))
    if head_progress > 0:
        tip_x = 37 + 18 * head_progress
        half_width = 10 * head_progress
        draw.polygon([(tip_x, 231), (37, 231 - half_width), (37, 231 + half_width)], fill=GREEN)


def draw_card(base: Image.Image, step: tuple, reveal: float, active: bool, pulse: float) -> None:
    number, label, detail, x, y, accent = step
    alpha = int(255 * (0.22 + 0.78 * ease(reveal)))
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    if active:
        glow_alpha = int(42 + 25 * pulse)
        draw.rounded_rectangle((x - 8, y - 8, x + CARD_W + 8, y + CARD_H + 8), radius=18, fill=(141, 198, 63, glow_alpha))

    fill = blend(WHITE, GREEN_PALE, ease(reveal) * 0.9)
    border = blend(LINE, accent, ease(reveal))
    draw.rounded_rectangle(
        (x, y, x + CARD_W, y + CARD_H),
        radius=12,
        fill=(*fill, alpha),
        outline=(*border, alpha),
        width=4 if active else 3,
    )

    circle_fill = blend(PALE_BLUE, accent, ease(reveal))
    draw.ellipse((x + 16, y + 16, x + 58, y + 58), fill=(*circle_fill, alpha))
    centered_text(draw, (x + 37, y + 37), str(number), STEP_FONT, WHITE if reveal > 0.5 else INK)
    draw.text((x + 72, y + 23), label, font=LABEL_FONT, fill=(*blend(MUTED, INK, ease(reveal)), alpha))
    draw.text((x + 72, y + 65), detail, font=DETAIL_FONT, fill=(*blend("#A4A7AE", MUTED, ease(reveal)), alpha))
    base.alpha_composite(layer)


def make_frame(t: float) -> Image.Image:
    base = Image.new("RGBA", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(base)

    draw.rectangle((0, 0, WIDTH, 11), fill=GREEN)
    draw.text((55, 44), "From Use Case to Approval-Ready Design", font=TITLE_FONT, fill=INK)
    draw.text((57, 99), "Each decision produces the evidence needed for the next.", font=SUBTITLE_FONT, fill=MUTED)

    connectors = [
        ((XS[0] + CARD_W, TOP_Y + CARD_H / 2), (XS[1], TOP_Y + CARD_H / 2)),
        ((XS[1] + CARD_W, TOP_Y + CARD_H / 2), (XS[2], TOP_Y + CARD_H / 2)),
        ((XS[2] + CARD_W, TOP_Y + CARD_H / 2), (XS[3], TOP_Y + CARD_H / 2)),
        ((XS[3] + CARD_W / 2, TOP_Y + CARD_H), (XS[3] + CARD_W / 2, BOTTOM_Y)),
        ((XS[3], BOTTOM_Y + CARD_H / 2), (XS[2] + CARD_W, BOTTOM_Y + CARD_H / 2)),
        ((XS[2], BOTTOM_Y + CARD_H / 2), (XS[1] + CARD_W, BOTTOM_Y + CARD_H / 2)),
        ((XS[1], BOTTOM_Y + CARD_H / 2), (XS[0] + CARD_W, BOTTOM_Y + CARD_H / 2)),
    ]

    for start, end in connectors:
        _, back, _ = arrow_geometry(start, end)
        draw.line((*start, *back), fill=LINE, width=5)

    start_time = 0.9
    step_span = 1.15
    reveals = [clamp((t - (start_time + i * step_span)) / 0.55) for i in range(len(STEPS))]

    for i, (start, end) in enumerate(connectors):
        connector_progress = clamp((t - (start_time + i * step_span + 0.48)) / 0.56)
        arrow(draw, start, end, connector_progress)

    active_index = min(len(STEPS) - 1, max(0, int((t - start_time) / step_span)))
    for i, step in enumerate(STEPS):
        active = start_time <= t < start_time + len(STEPS) * step_span and i == active_index
        pulse = (math.sin(t * math.pi * 3) + 1) / 2
        draw_card(base, step, reveals[i], active, pulse)

    feedback_start = start_time + len(STEPS) * step_span - 0.2
    feedback_progress = clamp((t - feedback_start) / 1.65)
    feedback_path(draw, feedback_progress)

    loop_alpha = int(255 * ease(clamp((t - (feedback_start + 0.85)) / 0.7)))
    if loop_alpha:
        layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        loop_draw = ImageDraw.Draw(layer)
        loop_draw.rounded_rectangle((55, 615, 382, 666), radius=25, fill=(244, 248, 241, loop_alpha), outline=(141, 198, 63, loop_alpha), width=2)
        loop_draw.text((82, 630), "Continuous community learning", font=LOOP_FONT, fill=(52, 56, 149, loop_alpha))
        base.alpha_composite(layer)

    draw = ImageDraw.Draw(base)
    draw.text((982, 659), "OCP Academy", font=STEP_FONT, fill=INK)
    draw.rectangle((1173, 659, 1225, 665), fill=GREEN)
    return base.convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "figures",
        help="Destination for the MP4 and poster (defaults to the course figures directory).",
    )
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    video_path = output_dir / "ess_requirement_to_evidence_workflow.mp4"
    poster_path = output_dir / "ess_requirement_to_evidence_workflow_poster.png"

    poster = make_frame(DURATION - 0.1)
    poster.save(poster_path, optimize=True)

    writer = imageio_ffmpeg.write_frames(
        str(video_path),
        (WIDTH, HEIGHT),
        fps=FPS,
        codec="libx264",
        pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p",
        output_params=["-crf", "21", "-preset", "medium", "-movflags", "+faststart", "-an"],
    )
    writer.send(None)
    for frame_number in range(round(DURATION * FPS)):
        writer.send(np.asarray(make_frame(frame_number / FPS)))
    writer.close()

    print(video_path)
    print(poster_path)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the silent ESUN header-efficiency teaching animation."""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1280
HEIGHT = 720
FPS = 30
DURATION = 10.0

BG = (247, 249, 245)
WHITE = (255, 255, 255)
BLUE = (52, 56, 149)
BLUE_SOFT = (230, 232, 247)
GREEN = (141, 198, 63)
GREEN_DARK = (95, 145, 42)
GREEN_SOFT = (238, 247, 226)
GRAY = (95, 96, 98)
GRAY_DARK = (55, 58, 61)
GRAY_LIGHT = (219, 224, 224)
AMBER = (242, 184, 75)
AMBER_SOFT = (255, 244, 217)

REGULAR_FONT = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD_FONT = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def smoothstep(start: float, end: float, value: float) -> float:
    if end == start:
        return 1.0 if value >= end else 0.0
    x = clamp((value - start) / (end - start))
    return x * x * (3.0 - 2.0 * x)


def lerp(start: float, end: float, amount: float) -> float:
    return start + (end - start) * amount


def mix_color(start: tuple[int, int, int], end: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(lerp(a, b, amount)) for a, b in zip(start, end))


def rgba(color: tuple[int, int, int], alpha: float = 1.0) -> tuple[int, int, int]:
    """Blend a color against the canvas background for deterministic fades."""
    return mix_color(BG, color, clamp(alpha))


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(BOLD_FONT if bold else REGULAR_FONT), size)


def draw_centered(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    spacing: int = 5,
) -> None:
    bbox = draw.multiline_textbbox((0, 0), text, font=text_font, spacing=spacing, align="center")
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.multiline_text(
        (xy[0] - width / 2, xy[1] - height / 2 - bbox[1]),
        text,
        font=text_font,
        fill=fill,
        spacing=spacing,
        align="center",
    )


def draw_pill(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    text: str,
    alpha: float,
) -> None:
    if alpha <= 0.01:
        return
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=rgba(GREEN_SOFT, alpha), outline=rgba(GREEN, alpha), width=2)
    draw_centered(draw, ((x0 + x1) / 2, (y0 + y1) / 2), text, font(20, True), rgba(GREEN_DARK, alpha))


def draw_segment(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    fill_color: tuple[int, int, int],
    label: str,
    text_color: tuple[int, int, int],
    alpha: float,
    outline_color: tuple[int, int, int] = WHITE,
    outline_width: int = 3,
    label_size: int = 22,
) -> None:
    draw.rounded_rectangle(
        box,
        radius=12,
        fill=rgba(fill_color, alpha),
        outline=rgba(outline_color, alpha),
        width=outline_width,
    )
    x0, y0, x1, y1 = box
    draw_centered(
        draw,
        ((x0 + x1) / 2, (y0 + y1) / 2),
        label,
        font(label_size, True),
        rgba(text_color, alpha),
        spacing=4,
    )


def build_frame(time_seconds: float) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    # The fade-to-background makes the loop restart cleanly.
    content_alpha = smoothstep(0.05, 0.55, time_seconds) * (1.0 - smoothstep(9.45, 9.95, time_seconds))

    for x in range(0, WIDTH + 1, 64):
        draw.line((x, 0, x, HEIGHT), fill=rgba(GRAY_LIGHT, 0.22 * content_alpha), width=1)
    for y in range(0, HEIGHT + 1, 64):
        draw.line((0, y, WIDTH, y), fill=rgba(GRAY_LIGHT, 0.22 * content_alpha), width=1)

    draw.text((72, 40), "OCP ACADEMY", font=font(17, True), fill=rgba(GREEN_DARK, content_alpha))
    draw.rounded_rectangle((225, 31, 306, 62), radius=15, fill=rgba(BLUE, content_alpha))
    draw_centered(draw, (265.5, 46.5), "ESUN", font(15, True), rgba(WHITE, content_alpha))
    draw.text(
        (72, 80),
        "Cách ESUN thu hồi overhead của gói tin",
        font=font(40, True),
        fill=rgba(GRAY_DARK, content_alpha),
    )
    draw.text(
        (74, 132),
        "Payload giữ nguyên. Header mạng được tối ưu cho scale-up.",
        font=font(23),
        fill=rgba(GRAY, content_alpha),
    )

    if time_seconds < 1.6:
        stage_index = 0
        stage_label = "1  KHUNG ETHERNET / IP TIÊU CHUẨN"
    elif time_seconds < 3.8:
        stage_index = 1
        stage_label = "2  XÁC ĐỊNH OVERHEAD DÙNG CHUNG"
    elif time_seconds < 5.9:
        stage_index = 2
        stage_label = "3  THAY IP HEADER"
    else:
        stage_index = 3
        stage_label = "4  GIỮ ĐIỀU KHIỂN SCALE-UP CẦN"

    stage_x = [83, 452, 821, 1190]
    draw.line((stage_x[0], 188, stage_x[-1], 188), fill=rgba(GRAY_LIGHT, content_alpha), width=4)
    for index, x in enumerate(stage_x):
        active = index <= stage_index
        color = GREEN if active else GRAY_LIGHT
        draw.ellipse((x - 9, 179, x + 9, 197), fill=rgba(color, content_alpha), outline=rgba(WHITE, content_alpha), width=2)
    draw.text((72, 207), stage_label, font=font(16, True), fill=rgba(GREEN_DARK, content_alpha))

    replace_progress = smoothstep(3.8, 5.8, time_seconds)
    header_width = lerp(330, 102, replace_progress)
    widths = [150.0, 150.0, 112.0, header_width, 360.0, 84.0]
    total_width = sum(widths)
    x = (WIDTH - total_width) / 2
    y0 = 260.0
    y1 = 390.0

    segment_specs = [
        (BLUE, "MAC\nđích", WHITE, 21),
        (BLUE, "MAC\nnguồn", WHITE, 21),
        (BLUE_SOFT, "", BLUE, 18),
        (mix_color(AMBER, GREEN, replace_progress), "", GRAY_DARK, 22),
        ((233, 236, 239), "Giao vận + Payload\ngiữ nguyên", GRAY_DARK, 22),
        ((205, 210, 214), "FCS", GRAY_DARK, 20),
    ]

    boxes: list[tuple[float, float, float, float]] = []
    for width, (fill_color, label, text_color, label_size) in zip(widths, segment_specs):
        box = (x, y0, x + width, y1)
        boxes.append(box)
        draw_segment(
            draw,
            box,
            fill_color,
            label,
            text_color,
            content_alpha,
            label_size=label_size,
        )
        x += width

    ether_box = boxes[2]
    header_box = boxes[3]
    if replace_progress < 0.5:
        draw_centered(
            draw,
            ((ether_box[0] + ether_box[2]) / 2, (ether_box[1] + ether_box[3]) / 2),
            "EtherType\nIP",
            font(18, True),
            rgba(BLUE, content_alpha),
        )
        draw_centered(
            draw,
            ((header_box[0] + header_box[2]) / 2, (header_box[1] + header_box[3]) / 2),
            "IP Header\n20–40 B",
            font(24, True),
            rgba(GRAY_DARK, content_alpha),
        )
    else:
        draw_centered(
            draw,
            ((ether_box[0] + ether_box[2]) / 2, (ether_box[1] + ether_box[3]) / 2),
            "EH-ET",
            font(19, True),
            rgba(BLUE, content_alpha),
        )
        draw_centered(
            draw,
            ((header_box[0] + header_box[2]) / 2, (header_box[1] + header_box[3]) / 2),
            "ESUN\nHeader\n4 B",
            font(20, True),
            rgba(GRAY_DARK, content_alpha),
            spacing=2,
        )

    if 1.4 <= time_seconds < 4.1:
        pulse = 0.65 + 0.35 * math.sin((time_seconds - 1.4) * math.pi * 2.0)
        pad = 8 + 3 * pulse
        draw.rounded_rectangle(
            (header_box[0] - pad, header_box[1] - pad, header_box[2] + pad, header_box[3] + pad),
            radius=18,
            outline=rgba(AMBER, content_alpha * (0.6 + 0.35 * pulse)),
            width=5,
        )

    connector_alpha = content_alpha * smoothstep(1.5, 2.2, time_seconds)
    header_center = (header_box[0] + header_box[2]) / 2
    draw.line((header_center, y1 + 3, header_center, 440), fill=rgba(GRAY, connector_alpha), width=3)
    draw.polygon(
        [(header_center - 8, 431), (header_center + 8, 431), (header_center, 443)],
        fill=rgba(GRAY, connector_alpha),
    )

    pre_replace_alpha = (
        content_alpha
        * smoothstep(1.5, 2.2, time_seconds)
        * (1.0 - smoothstep(5.3, 5.9, time_seconds))
    )
    pre_replace_text = (
        "Các trường định tuyến và điều khiển dùng chung"
        if time_seconds < 3.8
        else "Chỉ giữ những gì miền scale-up cần"
    )
    draw_centered(draw, (header_center, 468), pre_replace_text, font(21, True), rgba(GRAY, pre_replace_alpha))

    controls_alpha = content_alpha * smoothstep(5.7, 6.5, time_seconds)
    pill_labels = ["EH-CoS", "EH-ECN", "Flow Label", "TTL"]
    pill_widths = [150, 150, 180, 116]
    gap = 18
    total_pill_width = sum(pill_widths) + gap * (len(pill_widths) - 1)
    pill_x = (WIDTH - total_pill_width) / 2
    for index, (label, pill_width) in enumerate(zip(pill_labels, pill_widths)):
        stagger = smoothstep(5.85 + index * 0.18, 6.45 + index * 0.18, time_seconds)
        draw_pill(draw, (pill_x, 438, pill_x + pill_width, 486), label, controls_alpha * stagger)
        pill_x += pill_width + gap

    takeaway_alpha = content_alpha * smoothstep(6.25, 7.0, time_seconds)
    draw.rounded_rectangle(
        (176, 530, 1104, 646),
        radius=18,
        fill=rgba(WHITE, takeaway_alpha),
        outline=rgba(GREEN, takeaway_alpha),
        width=3,
    )
    draw_centered(
        draw,
        (640, 566),
        "Giữ khung Ethernet. Giảm overhead của header.",
        font(29, True),
        rgba(GRAY_DARK, takeaway_alpha),
    )
    draw_centered(
        draw,
        (640, 612),
        "Loại bỏ 20–40 B  ·  thêm lại 4 B",
        font(22, True),
        rgba(GREEN_DARK, takeaway_alpha),
    )

    return image


def generate_video(output: Path, poster: Path, ffmpeg: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    poster.parent.mkdir(parents=True, exist_ok=True)
    build_frame(7.8).save(poster, optimize=True)

    # A numbered image sequence keeps every transition deterministic across
    # the older ffmpeg builds commonly bundled with desktop applications.
    with tempfile.TemporaryDirectory(prefix="esun-video-") as temp_dir:
        frames_dir = Path(temp_dir)
        for frame_index in range(round(FPS * DURATION)):
            timestamp = frame_index / FPS
            build_frame(timestamp).save(frames_dir / f"frame_{frame_index:04d}.png", compress_level=1)

        command = [
            str(ffmpeg),
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(frames_dir / "frame_%04d.png"),
            "-an",
            "-c:v",
            "libx264",
            "-profile:v",
            "baseline",
            "-level",
            "3.1",
            "-tune",
            "animation",
            "-bf",
            "0",
            "-g",
            str(FPS),
            "-keyint_min",
            str(FPS),
            "-sc_threshold",
            "0",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ]
        subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--poster", type=Path, required=True)
    parser.add_argument(
        "--ffmpeg",
        type=Path,
        help="Path to ffmpeg. Defaults to ffmpeg on PATH, with a macOS app fallback.",
    )
    args = parser.parse_args()
    ffmpeg = args.ffmpeg
    if ffmpeg is None:
        discovered = shutil.which("ffmpeg")
        ffmpeg = Path(discovered) if discovered else Path(
            "/Applications/Logi Tune.app/Contents/Resources/ffmpeg/ffmpeg"
        )
    if not ffmpeg.exists():
        raise SystemExit("ffmpeg not found; install it or pass --ffmpeg /path/to/ffmpeg")
    generate_video(args.output.resolve(), args.poster.resolve(), ffmpeg.resolve())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
FRAMES = ROOT / "tmp" / "animation_frames"


def first_existing(*paths: str) -> Path:
    for path in paths:
        candidate = Path(path)
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"No supported font found: {', '.join(paths)}")


REGULAR = first_existing(
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
BOLD = first_existing(
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)

GREEN = "#8DC63F"
GREEN_DARK = "#6FA030"
GREEN_PALE = "#F3F8EB"
BLUE = "#343895"
TEXT = "#30313A"
MUTED = "#6B6C70"
BORDER = "#DFE3E8"
WHITE = "#FFFFFF"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(BOLD if bold else REGULAR), size)


def text_size(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), value, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def centered_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str,
                  fnt: ImageFont.FreeTypeFont, fill: str, spacing: int = 4) -> None:
    lines = value.split("\n")
    heights = [text_size(draw, line, fnt)[1] for line in lines]
    total = sum(heights) + spacing * (len(lines) - 1)
    y = box[1] + (box[3] - box[1] - total) / 2
    for line, height in zip(lines, heights):
        width, _ = text_size(draw, line, fnt)
        x = box[0] + (box[2] - box[0] - width) / 2
        draw.text((x, y), line, font=fnt, fill=fill)
        y += height + spacing


def arrowhead(draw: ImageDraw.ImageDraw, tip: tuple[float, float], angle: float,
              color: str, size: float = 18) -> None:
    tx, ty = tip
    back_x = tx - math.cos(angle) * size
    back_y = ty - math.sin(angle) * size
    perp_x = -math.sin(angle) * size * 0.55
    perp_y = math.cos(angle) * size * 0.55
    draw.polygon([(tx, ty), (back_x + perp_x, back_y + perp_y), (back_x - perp_x, back_y - perp_y)], fill=color)


def path_arrowhead(draw: ImageDraw.ImageDraw, center: tuple[float, float], angle: float,
                   color: str, size: float = 22) -> None:
    """Center an arrowhead's visual mass on a stroked path."""
    cx, cy = center
    tip_x = cx + math.cos(angle) * size * (2 / 3)
    tip_y = cy + math.sin(angle) * size * (2 / 3)
    back_x = cx - math.cos(angle) * size * (1 / 3)
    back_y = cy - math.sin(angle) * size * (1 / 3)
    perp_x = -math.sin(angle) * size * 0.62
    perp_y = math.cos(angle) * size * 0.62
    draw.polygon([(tip_x, tip_y), (back_x + perp_x, back_y + perp_y),
                  (back_x - perp_x, back_y - perp_y)], fill=color)


def make_flywheel_frames() -> None:
    out = FRAMES / "credibility_flywheel"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    total = 180
    labels = ["LISTEN", "PARTICIPATE", "CONTRIBUTE", "COLLABORATE", "EARN TRUST", "LEAD"]
    angles = [-90, -30, 30, 90, 150, 210]
    cx, cy, rx, ry = 640, 370, 410, 238
    ring_width = 16
    centerline_rx = rx - ring_width / 2
    centerline_ry = ry - ring_width / 2
    positions = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in angles]

    for frame in range(total):
        canvas = Image.new("RGB", (1280, 720), WHITE)
        draw = ImageDraw.Draw(canvas)
        draw.text((54, 38), "THE CREDIBILITY FLYWHEEL", font=font(26, True), fill=GREEN_DARK)
        draw.text((54, 76), "Useful participation becomes a repeatable cycle of trust.", font=font(22), fill=MUTED)
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline="#DDE7D1", width=ring_width)
        for a in [-60, 0, 60, 120, 180, 240]:
            rad = math.radians(a)
            center = (cx + centerline_rx * math.cos(rad), cy + centerline_ry * math.sin(rad))
            tangent = math.atan2(centerline_ry * math.cos(rad), -centerline_rx * math.sin(rad))
            path_arrowhead(draw, center, tangent, GREEN, 44)

        phase = (frame / (total - 1)) * len(labels)
        for idx, (label, pos) in enumerate(zip(labels, positions)):
            distance = abs(((phase - idx + len(labels) / 2) % len(labels)) - len(labels) / 2)
            strength = max(0.0, 1.0 - distance / 0.82)
            width, height = (210, 82) if label != "EARN TRUST" else (226, 82)
            x0, y0 = int(pos[0] - width / 2), int(pos[1] - height / 2)
            fill = GREEN if strength > 0.35 else WHITE
            outline = GREEN_DARK if strength > 0.35 else BORDER
            draw.rounded_rectangle((x0, y0, x0 + width, y0 + height), radius=20,
                                   fill=fill, outline=outline, width=4 if strength > 0.35 else 3)
            centered_text(draw, (x0, y0, x0 + width, y0 + height), label, font(22, True),
                          WHITE if strength > 0.35 else TEXT)

        draw.ellipse((cx - 150, cy - 122, cx + 150, cy + 122), fill=BLUE)
        centered_text(draw, (cx - 138, cy - 104, cx + 138, cy + 104),
                      "CREDIBILITY\nCOMPOUNDS\nWHEN YOU KEEP\nLISTENING", font(24, True), WHITE, 7)
        draw.text((54, 677), "Lead through service—then return to listening.", font=font(21, True), fill=BLUE)
        canvas.save(out / f"frame_{frame:04d}.png", optimize=True)
    shutil.copy2(out / "frame_0000.png", FIGURES / "credibility_flywheel_poster.png")


def make_touchpoints_frames() -> None:
    out = FRAMES / "useful_touchpoints"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    total = 180
    main_cards = [
        ("REAL\nPROBLEM", (52, 270, 224, 390)),
        ("USEFUL\nEVIDENCE", (276, 270, 448, 390)),
        ("WORKSTREAM\nVALIDATION", (500, 270, 692, 390)),
        ("NEXT\nPARTICIPANT", (1052, 270, 1228, 390)),
    ]
    channels = [
        ("EVENT", (760, 142, 942, 196)),
        ("BLOG", (804, 214, 986, 268)),
        ("PODCAST", (826, 288, 1008, 342)),
        ("WEBINAR", (804, 362, 986, 416)),
        ("ACADEMY", (760, 434, 942, 488)),
    ]
    sequence_len = 3 + len(channels) + 1

    for frame in range(total):
        canvas = Image.new("RGB", (1280, 720), WHITE)
        draw = ImageDraw.Draw(canvas)
        draw.text((54, 38), "ONE CONTRIBUTION, MANY USEFUL TOUCHPOINTS", font=font(25, True), fill=GREEN_DARK)
        draw.text((54, 76), "Choose the place that best serves the audience and the story.", font=font(22), fill=MUTED)
        phase = (frame / (total - 1)) * sequence_len

        # Baseline relationships.
        draw.line((224, 330, 276, 330), fill="#DDE7D1", width=12)
        arrowhead(draw, (276, 330), 0, GREEN, 16)
        draw.line((448, 330, 500, 330), fill="#DDE7D1", width=12)
        arrowhead(draw, (500, 330), 0, GREEN, 16)
        for _, box in channels:
            cy = (box[1] + box[3]) / 2
            draw.line((692, 330, box[0], cy), fill="#DDE7D1", width=7)
            arrowhead(draw, (box[0], cy), math.atan2(cy - 330, box[0] - 692), GREEN, 13)
            draw.line((box[2], cy, 1052, 330), fill="#E6E7EA", width=6)
            arrowhead(draw, (1052, 330), math.atan2(330 - cy, 1052 - box[2]), "#A9ABB0", 12)

        for idx, (label, box) in enumerate(main_cards):
            seq_index = idx if idx < 3 else sequence_len - 1
            distance = abs(((phase - seq_index + sequence_len / 2) % sequence_len) - sequence_len / 2)
            active = distance < 0.72
            fill = GREEN if active else (BLUE if idx == 3 else WHITE)
            text_fill = WHITE if active or idx == 3 else TEXT
            outline = GREEN_DARK if active else (BLUE if idx == 3 else BORDER)
            draw.rounded_rectangle(box, radius=22, fill=fill, outline=outline, width=4 if active else 3)
            centered_text(draw, box, label, font(21, True), text_fill, 5)

        for cidx, (label, box) in enumerate(channels):
            seq_index = 3 + cidx
            distance = abs(((phase - seq_index + sequence_len / 2) % sequence_len) - sequence_len / 2)
            active = distance < 0.72
            draw.rounded_rectangle(box, radius=18, fill=GREEN if active else GREEN_PALE,
                                   outline=GREEN_DARK if active else "#C7DCAF", width=3)
            centered_text(draw, box, label, font(18, True), WHITE if active else GREEN_DARK)

        draw.rounded_rectangle((726, 518, 1018, 578), radius=20, fill="#F4F4F5", outline=BORDER, width=2)
        centered_text(draw, (726, 518, 1018, 578), "THE RIGHT CHANNEL", font(20, True), BLUE)
        draw.text((54, 656), "Useful work earns reach. The channel extends its value.", font=font(21, True), fill=BLUE)
        canvas.save(out / f"frame_{frame:04d}.png", optimize=True)
    shutil.copy2(out / "frame_0000.png", FIGURES / "useful_touchpoints_poster.png")


def main() -> None:
    FIGURES.mkdir(exist_ok=True)
    make_flywheel_frames()
    make_touchpoints_frames()
    print("Built teaching-animation frames and posters.")


if __name__ == "__main__":
    main()

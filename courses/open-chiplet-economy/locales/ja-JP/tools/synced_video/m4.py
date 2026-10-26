"""M4S3: one request, three compatibility questions.

Deterministic vector source for the approved, unchanged final narration.
All clock values are narration seconds, not electrical timing.  The final
comparison deliberately remains unresolved; no compatibility result is implied.
"""
from .primitives import *

DURATION = 39.52285714285714


def _circle(x, y, r, fill=GREEN, stroke=None, width=4):
    return (f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" '
            f'fill="{fill}" stroke="{stroke or fill}" stroke-width="{width}"/>')


def _read(cx, cy, surround=0.0):
    """One consistent abstract request, with no packet fields or bit layout."""
    w, h = 460, 150
    x, y = cx - w / 2, cy - h / 2
    parts = []
    if surround > 0:
        # The outline describes a transport representation, not added fields.
        inset = 13 + 13 * surround
        parts.append(rect(x - inset, y - inset, w + 2 * inset,
                          h + 2 * inset, fill=WHITE, stroke=GRAY,
                          width=4, rx=28))
    parts.append(rect(x, y, w, h, fill=PALE, stroke=GREEN, width=5, rx=18))
    parts.append(text(cx, cy + 13, 'Read memory', size=52, weight=600))
    return ''.join(parts)


def _physical(t, small=False, labels=True, y_offset=0):
    """Persistent left/right die identities and one actual connection."""
    if small:
        p = 1.0
    else:
        p = smooth(t, 9.04, 9.72)
    x1 = lerp(160, 180, p)
    x2 = lerp(1320, 1380, p)
    w = lerp(440, 360, p)
    y = lerp(300, 650, p) + y_offset
    h = lerp(400, 210, p)
    cy = y + h / 2
    parts = [chip(x1, y, w, h, label=''),
             chip(x2, y, w, h, label='')]
    # Both endpoints use the same notation. They are illustrative PHY locations.
    parts += [line(x1 + w, cy, x2, cy, color=GRAY, width=7),
              _circle(x1 + w, cy, 12, WHITE, INK),
              _circle(x2, cy, 12, WHITE, INK)]
    if labels:
        parts += [text(x1 + w / 2, cy + 18, 'Sender', size=60),
                  text(x2 + w / 2, cy + 18, 'Receiver', size=60)]
    if t < 9.04:
        parts += [text(x1 + w / 2, y + h + 78, 'PHY', size=54),
                  text(x2 + w / 2, y + h + 78, 'PHY', size=54)]
    else:
        parts.append(text(960, cy + 104, 'Electrical connection', size=49))
    # One pedagogical highlight, not a periodic waveform or a handshake.
    if 2.84 <= t < 4.10:
        q = smooth(t, 2.84, 4.10)
        end = lerp(x1 + w + 16, x2 - 16, q)
        parts.append(line(x1 + w + 16, cy, end, cy, color=GREEN, width=10))
    elif 4.10 <= t < 9.04:
        parts.append(line(x1 + w + 16, cy, x2 - 16, cy, color=GREEN, width=8))
    elif 29.24 <= t < 30.62:
        q = smooth(t, 29.24, 30.62)
        cx = lerp(x1 + w + 25, x2 - 25, q)
        parts.append(line(max(x1 + w + 16, cx - 85), cy,
                          min(x2 - 16, cx + 25), cy, color=GREEN, width=10))
    return parts


def _unit(cx, cy, closing=1.0):
    """Open brackets organize undifferentiated information, without fields."""
    gap = lerp(235, 155, closing)
    parts = [rect(cx - 125, cy - 32, 250, 64, fill=PALE,
                  stroke=PALE, width=1, rx=5),
             line(cx - 95, cy, cx + 95, cy, color=INK, width=12)]
    parts += [path(f'M {cx-gap+32} {cy-66} H {cx-gap} V {cy+66} H {cx-gap+32}',
                   color=GREEN, width=6),
              path(f'M {cx+gap-32} {cy-66} H {cx+gap} V {cy+66} H {cx+gap-32}',
                   color=GREEN, width=6)]
    return ''.join(parts)


def _meaning_halves(y=315):
    # Two ends of a conceptual comparison deliberately do not meet.
    return [path(f'M 600 {y-24} V {y} H 875', color=GRAY, width=5),
            path(f'M 1320 {y-24} V {y} H 1045', color=GRAY, width=5)]


def render(t: float) -> str:
    t = max(0.0, min(float(t), DURATION))
    parts = []

    if t < 9.04:
        # First inspect the physical relationship.  No higher layer precedes it.
        parts += _physical(t)
        if t < 4.84:
            parts += [text(960, 140, 'Physical layer', size=62),
                      text(960, 875, 'Electrical connection', size=58)]
        else:
            term = ('Pinout' if t < 5.48 else 'Voltages' if t < 6.22
                    else 'Timing' if t < 7.04 else 'Channel' if t < 7.94
                    else 'Must be compatible')
            parts += [text(960, 140, term, size=62),
                      path('M 660 280 V 235 H 1260 V 280', color=GRAY, width=5),
                      text(960, 875, 'Electrical connection', size=58)]
            if t >= 7.94:
                parts.append(underline_phrase(960,140,'Must be compatible','Must be compatible',size=62,gap=34,width=6))

    elif t < 16.94:
        # Widen the same pair to make room for a conceptual transfer view.
        parts += _physical(t)
        parts.append(text(960, 120, 'Link', size=62))
        if t < 12.26:
            close = smooth(t, 9.45, 10.08)
            q = smooth(t, 10.08, 11.40)
            cx = lerp(420, 1500, q)
            parts.append(_unit(cx, 340, close))
            parts.append(text(960, 495, 'Organized transfer', size=58))
        else:
            # Terms are a single stable annotation. Only their underline moves.
            # The applicability qualifier remains present throughout.
            parts.append(text(960, 220, 'Interface-dependent', size=58))
            parts.append(_unit(1535, 385))
            parts += [text(790, 355, 'Framing · error protection', size=53),
                      text(790, 455, 'Flow control', size=53)]
            if 14.16 <= t < 14.78:
                parts.append(underline_phrase(790,355,'Framing · error protection','Framing',size=53,gap=24,width=6))
            elif 14.78 <= t < 15.84:
                parts.append(underline_phrase(790,355,'Framing · error protection','error protection',size=53,gap=24,width=6))
            elif t >= 15.84:
                parts.append(underline_phrase(790,455,'Flow control','Flow control',size=53,gap=24,width=6))

    elif t < 24.56:
        # The lower physical pair remains as context; meaning is compared above.
        parts += _physical(t, small=True)
        parts += [text(960, 120, 'Protocol', size=62),
                  text(960, 215, 'Shared meaning', size=56)]
        if t < 19.8:
            parts.append(_unit(360, 365))
            parts += [path('M 175 280 H 545', color=GRAY, width=4),
                      path('M 1375 280 H 1745', color=GRAY, width=4)]
        else:
            q = smooth(t, 19.88, 22.04)
            cx = lerp(360, 1560, q)
            # The left word remains the sender's meaning after the token departs.
            if cx > 805:
                parts.append(text(360, 383, 'Read memory', size=54))
            parts.append(_read(cx, 365))
            if t >= 22.04:
                parts += [path('M 360 460 V 505 H 1560 V 460', color=GRAY, width=5),
                          text(960, 585, 'Same interpretation', size=54)]

    elif t < 29.16:
        # Explicit conceptual inset: representation mapping, not a second read.
        parts += _physical(t, small=True)
        parts += [text(960, 115, 'Sender-side mapping', size=60),
                  text(360, 245, 'On-chip bus', size=54),
                  text(960, 245, 'Adapter', size=54),
                  text(1560, 245, 'D2D transport', size=54)]
        # These are a diagram's mapping rails, not die pinouts or real wires.
        parts += [line(150, 565, 720, 565, color=GRAY, width=5),
                  line(1200, 565, 1770, 565, color=GRAY, width=5),
                  path('M 890 305 V 565 H 1030 V 305', color=GRAY, width=5)]
        q = smooth(t, 25.80, 27.52)
        cx = lerp(360, 1560, q)
        surround = smooth(t, 26.72, 27.36)
        parts.append(_read(cx, 420, surround))
        # The unchanged word inside the transport surround supplies the hold.

    else:
        # A deliberately labelled comparison cut.  This pair is NOT shown
        # changing from an accepted transaction to a failure without explanation.
        parts += _physical(t, small=True, y_offset=-65)
        parts.append(text(960, 115, 'Illustrative mismatch', size=60))
        parts += [text(360, 265, 'Read memory', size=54),
                  text(1560, 265, 'Meaning differs', size=54)]
        parts += _meaning_halves()
        cx = lerp(360, 1560, smooth(t, 29.24, 31.60))
        parts.append(_read(cx, 455))
        if t >= 33.06:
            p = smooth(t, 33.06, 34.24)
            # Bracket grows around the complete pair. It never closes as a seal.
            bracket_length = 3070.0
            parts += [f'<path d="M 155 205 H 100 V 825 H 1820 V 205 H 1765" '
                      f'fill="none" stroke="{GRAY}" stroke-width="5" '
                      f'stroke-dasharray="{p * bracket_length:.3f} {bracket_length}"/>',
                      text(960, 910, 'All applicable layers + options', size=54),
                      text(960, 1000, 'Initialization · errors', size=48)]
            if t >= 37.80:
                # Labels have been readable since 33.06; these are just cues.
                parts.append(underline_phrase(960,1000,'Initialization · errors','Initialization'))
            if t >= 38.96:
                parts.append(underline_phrase(960,1000,'Initialization · errors','errors'))
    return svg(parts)

# Retain approved scene logic and use measured Japanese narration time.
from .japanese_timing import english_time
_source_render=render
def render(t):
    return _source_render(english_time('m4',float(t)))

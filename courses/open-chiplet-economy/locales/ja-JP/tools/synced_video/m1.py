"""M1S3: shared work supports integration; accountability stays with the integrator.

Pure deterministic vector sequence against the locked final-v4 narration.
The papers are conceptual design information/agreements, not source-code files,
certificates or completed qualification evidence. No enclosing scene frame.
"""
from .primitives import *

DURATION = 43.748662131519275
POSTER_SECONDS = 42.8


def _paper(cx, cy, w=420, h=150, label='', size=50, accent=False, ruled=True):
    """Folded paper is a semantic document object, never a scene border."""
    x, y, fold = cx - w / 2, cy - h / 2, 28
    color = GREEN if accent else GRAY
    parts = [path(f'M{x} {y} H{x+w-fold} L{x+w} {y+fold} V{y+h} H{x} Z',
                  color, 5, WHITE),
             path(f'M{x+w-fold} {y} V{y+fold} H{x+w}', color, 4)]
    if label:
        lines = label.split('\n')
        baseline = cy + 13 - (len(lines) - 1) * size * .625
        parts.append(text(cx, baseline, label, size=size))
    elif ruled:
        for yy in (cy - 16, cy + 18):
            parts.append(line(cx-w*.28, yy, cx+w*.23, yy, color=GRAY, width=5))
    return ''.join(parts)


def _die(cx, y, label, supplier, w=360, h=240):
    return [text(cx, y-60, supplier, size=48),
            chip(cx-w/2, y, w, h, ''),
            text(cx, y+h/2+13, label, size=52)]


def _scope(left, right, y=930, label='Integrator'):
    # One bottom bracket denotes product responsibility, not a container/frame.
    return [path(f'M{left} {y-22} V{y} H{right} V{y-22}', GRAY, 5),
            text(960, 1008, label, size=50)]


def _early_pair(t):
    p = smooth(t, 4.44, 6.68)
    a, b = lerp(330, 430, p), lerp(1590, 1490, p)
    return _die(a, 500, 'Compute', 'Supplier A') + _die(b, 500, 'I/O', 'Supplier B'), a, b


def _integrating_pair(t):
    # At the narrated buying example, each same die moves in its own spoken turn.
    qa, qb = smooth(t, 20.38, 21.44), smooth(t, 22.26, 23.40)
    a, b = lerp(430, 695, qa), lerp(1490, 1225, qb)
    ya, yb = lerp(500, 560, qa), lerp(500, 560, qb)
    return (_die(a, ya, 'Compute', 'Supplier A', 350, 220)
            + _die(b, yb, 'I/O', 'Supplier B', 350, 220)), a, b


def _final_pair(y=690, h=220):
    return (_die(695, y, 'Compute', 'Supplier A', 350, h)
            + _die(1225, y, 'I/O', 'Supplier B', 350, h))


def _shared_sheet(full=False):
    if not full:
        return _paper(960, 415, 620, 230, 'Shared\nagreements', 54)
    out = [_paper(960, 405, 1200, 450, ruled=False), text(960, 270, 'Shared agreements', size=54)]
    for y, label in [(365, 'Package compatibility'), (435, 'Test access'),
                     (505, 'Startup behavior'), (575, 'Commercial responsibilities')]:
        out.append(text(960, y, label, size=48))
    return ''.join(out)


def _note(cx, cy, label):
    widths = {'Review': 300, 'Model': 280, 'Test': 240}
    return _paper(cx, cy, widths[label], 150, label, 48, accent=True)


def render(t: float) -> str:
    t = max(0.0, min(float(t), DURATION))
    out = []

    if t < 19.60:
        pair, a, b = _early_pair(t)
        out += pair
        if t < 7.86:
            out.append(text(960, 140, 'Shared work', size=60))
            out += [path(f'M{a-180} 815 V840 H{b+180} V815', GRAY, 5),
                    text(960, 920, 'System to integrate', size=56)]
        else:
            # The only physical connection is the neutral line between die edges.
            out += [line(a+180, 620, b-180, 620, GRAY, 7),
                    text(960, 850, 'Electrical connection', size=52)]
            if t < 10.50:
                out.append(text(960, 140, 'More than a connection', size=60))
                # A wide, open scope grows beyond the physical channel.
                p = smooth(t, 8.32, 9.60)
                x1, x2 = lerp(700, 210, p), lerp(1220, 1710, p)
                out.append(path(f'M{x1} 350 V300 H{x2} V350', GRAY, 5))
            elif t < 13.78:
                out.append(text(960, 140, 'Tools + flows', size=60))
                q = smooth(t, 11.74, 12.84)
                # Design information moves between supplier teams, not through a PHY.
                out.append(_paper(lerp(a, b, q), 295, 420, 150, 'Design info', 50, True))
            elif t < 16.76:
                out.append(text(960, 140, 'Ecosystem standards', size=60))
                q = smooth(t, 14.34, 15.02)
                out += [_paper(a, lerp(235, 270, q), 270, 130),
                        _paper(b, lerp(305, 270, q), 270, 130),
                        text(960, 292, 'Shared expectations', size=52)]
                if t >= 15.02:
                    out.append(path(f'M{a} 350 V370 H{b} V350', GRAY, 5))
            else:
                out += [text(960, 140, 'Open interfaces', size=60),
                        text(960, 300, 'Communication', size=54)]
                if 17.72 <= t <= 18.65:
                    q = smooth(t, 17.72, 18.65)
                    cx = lerp(a+180+25, b-180-25, q)
                    out.append(line(max(a+180+12, cx-65), 620,
                                    min(b-180-12, cx+25), 620, GREEN, 10))
        return svg(out)

    if t < 24.22:
        # A labelled conceptual view change, not a previously validated assembly.
        out += [text(960, 140, 'Illustrative supplier pair', size=58)]
        pair, a, b = _integrating_pair(t)
        out += pair + _scope(a-200, b+200)
        return svg(out)

    if t < 30.56:
        pair, a, b = _integrating_pair(t)
        out += pair + _scope(480, 1440)
        out += [text(960, 140, 'To establish', size=58),
                text(960, 670, '?', size=72, weight=500)]
        # All questions are readable before the rapid list. Cue emphasis is weight,
        # not a passing state, a checkmark, a mechanism, or a fabricated test result.
        questions = [
            (960, 275, 'Package compatibility', 25.62, 26.88),
            (270, 650, 'Test access', 26.88, 27.84),
            (1630, 650, 'Startup behavior', 27.84, 28.94),
            (960, 880, 'Commercial responsibilities', 28.94, 30.56),
        ]
        for x, y, label, start, end in questions:
            out.append(text(x, y, label, size=48, weight=700 if start <= t < end else 500))
        return svg(out)

    if t < 33.78:
        # A labelled regrouping view collects the same four unresolved questions.
        # A clean cut avoids sending text through die silhouettes during a reframe.
        out += _final_pair(765, 145) + _scope(480, 1440)
        out.append(text(960, 105, 'Develop together', size=54))
        out.append(_shared_sheet(full=True))
        return svg(out)

    if t < 39.32:
        out += [text(960, 110, 'Participation', size=58)]
        if t < 35.0:
            action = 'Contribute to the shared work'
        elif t < 36.42:
            action = 'Review a specification'
        elif t < 37.72:
            action = 'Supply a model'
        else:
            action = 'Test an implementation'
        out.append(text(960, 205, action, size=52))
        out += _final_pair() + _scope(480,1440)
        # Contribution notes slide under the shared paper. This is accumulation
        # of work, not an approval pipeline or transfer of product accountability.
        if 35.0 <= t < 36.42:
            out.append(_note(lerp(300,850,smooth(t,35.0,35.95)),415,'Review'))
        elif 36.42 <= t < 37.72:
            out.append(_note(lerp(1620,1070,smooth(t,36.42,37.25)),415,'Model'))
        elif t >= 37.72:
            out.append(_note(lerp(300,850,smooth(t,37.72,38.60)),415,'Test'))
        # Small offset sheets retain the contributions without tiny text/counts.
        if t >= 35.95:out.append(_paper(945,430,620,230))
        if t >= 37.25:out.append(_paper(930,445,620,230))
        out.append(_shared_sheet())
        return svg(out)

    # The final state is present for the entire closing sentence, with no loop.
    out += [text(960, 110, 'Shared work supports integration', size=56),
            text(960, 205, 'Tools + flows · Standards · Interfaces', size=50),
            arrow(960, 240, 960, 300, GRAY, 5, 20)]
    out += _final_pair()
    out += [_paper(945,430,620,230), _paper(930,445,620,230), _shared_sheet()]
    # Shared agreements relate to both suppliers; the open lower bracket assigns
    # complete-product responsibility to the integrator, not to a contribution.
    out += _scope(480,1440,label='Integrator: complete product responsibility')
    return svg(out)

# Retain approved scene logic and use measured Japanese narration time.
from .japanese_timing import english_time
_source_render=render
def render(t):
    return _source_render(english_time('m1',float(t)))

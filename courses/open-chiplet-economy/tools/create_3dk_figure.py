"""Editable 3DK family and workflow, adapted from ADK v1.0, pages 7–8."""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[1]
FIGURE = "figures/m7-3dk-family-and-workflow.svg"


def build_svg():
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="512" viewBox="0 0 1200 512">',
             '<rect width="1200" height="512" fill="white"/>',
             '<rect x="20" y="16" width="1160" height="374" rx="22" fill="#F3F8EB" stroke="#8DC63F" stroke-width="2"/>',
             '<text x="48" y="54" font-family="Arial,sans-serif" font-size="27" font-weight="700" fill="#343895">3DK</text>']
    cards = [
        ("CDK", ["Chiplet Design Kit"], "Component descriptions"),
        ("ADK", ["Assembly Design Kit"], "Assembly rules"),
        ("DRM", ["Package Design Rule Manual"], "Stack-up and design rules"),
        ("MDK", ["Material Design Kit"], "Material properties"),
        ("TDK", ["Test Design Kit"], "Test pins and connectivity"),
        ("SI/PI Design Kit", ["Signal / Power Integrity"], "Design and sign-off targets"),
    ]
    for index, (label, names, role) in enumerate(cards):
        x = 44 + (index % 3) * 388
        y = 76 + (index // 3) * 153
        center = x + 168
        parts.append(f'<g data-card="{html.escape(label)}"><rect x="{x}" y="{y}" width="336" height="137" rx="13" fill="white" stroke="#CAD5BF" stroke-width="2"/>')
        parts.append(f'<text x="{center}" y="{y+44}" text-anchor="middle" font-family="Arial,sans-serif" font-size="26" font-weight="700" fill="#343895">{html.escape(label)}</text>')
        for line, name in enumerate(names):
            parts.append(f'<text x="{center}" y="{y+76+line*24}" text-anchor="middle" font-family="Arial,sans-serif" font-size="21" fill="#5F6062">{html.escape(name)}</text>')
        parts.append(f'<text x="{center}" y="{y+112}" text-anchor="middle" font-family="Arial,sans-serif" font-size="22" fill="#5F6062">{html.escape(role)}</text></g>')
    for x, label in [(40, "Architecture"), (430, "Design"), (820, "Sign-off")]:
        parts.append(f'<g data-stage="{label}"><rect x="{x}" y="416" width="340" height="72" rx="12" fill="#ECEFF4" stroke="#CAD0DA" stroke-width="2"/><text x="{x+170}" y="460" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" font-weight="700" fill="#343895">{label}</text></g>')
    for start, tip in [(380, 430), (770, 820)]:
        back = tip - 14
        parts.append(f'<line x1="{start}" y1="452" x2="{back}" y2="452" stroke="#8DC63F" stroke-width="4"/><polygon class="arrowhead" points="{back},445 {back},459 {tip},452" fill="#8DC63F"/>')
    parts.append('</svg>')
    return ''.join(parts)


if __name__ == "__main__":
    (ROOT / FIGURE).write_text(build_svg())
    print(FIGURE)

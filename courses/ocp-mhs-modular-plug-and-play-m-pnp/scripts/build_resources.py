#!/usr/bin/env python3
"""Generate offline learner resource HTML into the build, not source control."""
import html
import json
import shutil
import sys
from pathlib import Path


def examples_page(inventory: dict) -> str:
    groups = [
        ("hpm", "HPM hardware description", lambda name: name.startswith("hpm-fru-")),
        ("peripheral", "Peripheral hardware descriptions", lambda name: name.startswith("peripherals-")),
        ("pd", "Programmable-device descriptions", lambda name: not name.startswith(("hpm-fru-", "peripherals-"))),
    ]
    sections = []
    for anchor, title, belongs in groups:
        rows = []
        for item in inventory["mockups"]:
            if not belongs(item["filename"]):
                continue
            status = "Course-adapted example" if item["course_adapted"] else "Release-package example"
            rows.append(
                '<tr><td><a href="' + html.escape(item["url"], quote=True) + '" target="_blank" rel="noopener">'
                + html.escape(item["filename"]) + "</a></td><td>"
                + html.escape(item["SchemaVersion"]) + "</td><td>" + status + "</td></tr>"
            )
        sections.append(
            f'<section id="{anchor}"><h2>{title}</h2><div class="table-wrap"><table>'
            '<thead><tr><th>JSON example</th><th>Declared schema</th><th>Provenance</th></tr></thead>'
            '<tbody>' + "".join(rows) + '</tbody></table></div></section>'
        )
    return '''<!DOCTYPE html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>M-PNP v0.7 Course Examples</title><style>
body{margin:0;background:#f4f6f2;color:#252a24;font:16px/1.6 system-ui,sans-serif}
header,main{max-width:1100px;margin:auto;padding:24px}header{background:#343895;color:white;border-radius:0 0 16px 16px}
header a{color:white}h1{margin:8px 0}h2{font-size:1.3rem}section{margin-top:30px}
.table-wrap{overflow:auto;background:white;border-radius:12px;border:1px solid #dce3d5}
table{border-collapse:collapse;width:100%;font-size:.85rem}th,td{text-align:left;padding:14px;border-bottom:1px solid #dce3d5}
th{background:#eaf2df}a{color:#343895}td:first-child{overflow-wrap:anywhere;min-width:220px}
.note{padding:18px;border-left:4px solid #8dc63f;background:white;border-radius:8px}
</style></head><body><header><a href="index.html">Course home</a><h1>M-PNP v0.7 Course Examples</h1></header>
<main><p class="note">All nine hardware examples supplied with this course declare <strong>hardware-component.v0_7_3</strong>.
The eight peripheral files are course-adapted examples; consult the source inventory for provenance before reuse.
The two programmable-device examples retain <strong>programmable-device.v0_7_2</strong>.
Example filenames have their own versions. These adaptations do not assert a validation pass.</p>
''' + "".join(sections) + "</main></body></html>\n"


def main():
    source = Path(__file__).resolve().parents[1]
    output = Path(sys.argv[1]).resolve().parent
    if source == output:
        raise SystemExit("Build resources into a separate staged package, not the source tree.")
    inventory = json.loads((source / "authoring/source-inventory.json").read_text())
    for example in inventory["mockups"]:
        if not (output / example["url"]).is_file():
            raise SystemExit(f'Missing staged example: {example["url"]}')
    for asset in ("mpnp_course_icon.svg", "thumbnail.png", "thumbnail.svg"):
        shutil.copy2(source / asset, output / asset)
    (output / "examples.html").write_text(examples_page(inventory), encoding="utf-8")
    print("Generated offline examples page; current text-free mark and poster copied.")


if __name__ == "__main__":
    main()

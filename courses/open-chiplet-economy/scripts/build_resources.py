"""Build offline learner resources from editable source; no audio or course edits."""
from pathlib import Path
import html,json,sys
R=Path(sys.argv[1]).resolve().parent
course=json.loads(Path(sys.argv[1]).read_text())
items=''.join(f'<article id="{g["id"]}"><h2>{html.escape(g["term"])}</h2><p>{html.escape(g["definition"])}</p></article>' for g in sorted(course['term_glossary'],key=lambda g:g['term'].lower()))
(R/"glossary.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Chiplet Economy — Course glossary</title><link rel="stylesheet" href="fonts/fonts.css"><style>body{font:18px/1.65 "Open Sans",Arial;color:#5f6062;background:#f6f8f5;margin:0}main{max-width:900px;margin:auto;padding:40px 24px}h1{color:#343895}article{background:white;border-left:4px solid #8dc63f;padding:12px 24px;margin:20px 0;border-radius:8px}h2{color:#343895;margin:0;font-size:22px}a{color:#343895}</style><main><h1>Open Chiplet Economy glossary</h1><p>Definitions for the nine-module Slides series. The architecture modules distinguish homogeneous and heterogeneous disaggregation by process node.</p>'+items+'</main></html>')

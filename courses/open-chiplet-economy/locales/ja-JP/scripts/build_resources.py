"""Build offline learner resources from editable source; no audio or course edits."""
from pathlib import Path
import html,json,sys
R=Path(sys.argv[1]).resolve().parent
course=json.loads(Path(sys.argv[1]).read_text())
items=''.join(f'<article id="{g["id"]}"><h2>{html.escape(g["term"])}</h2><p>{html.escape(g["definition"])}</p></article>' for g in sorted(course['term_glossary'],key=lambda g:g['term'].lower()))
(R/"glossary.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Chiplet Economy \u7528\u8a9e\u96c6</title><link rel="stylesheet" href="fonts/fonts.css"><style>body{font:18px/1.65 "Open Sans",Arial;color:#5f6062;background:#f6f8f5;margin:0}main{max-width:900px;margin:auto;padding:40px 24px}h1{color:#343895}article{background:white;border-left:4px solid #8dc63f;padding:12px 24px;margin:20px 0;border-radius:8px}h2{color:#343895;margin:0;font-size:22px}a{color:#343895}</style><main><h1>Open Chiplet Economy \u7528\u8a9e\u96c6</h1><p>\u51689\u30e2\u30b8\u30e5\u30fc\u30eb\u3067\u4f7f\u3046\u7528\u8a9e\u306e\u5b9a\u7fa9\u3067\u3059\u3002\u540c\u7a2e\u30fb\u7570\u7a2e\u306e\u6a5f\u80fd\u5206\u5272\u306f\u3001\u3053\u306e\u8b1b\u5ea7\u3067\u306f\u30d7\u30ed\u30bb\u30b9\u30ce\u30fc\u30c9\u3067\u533a\u5225\u3057\u307e\u3059\u3002</p>'+items+'</main></html>')

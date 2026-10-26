# FCSA: Architecting Interoperable Chiplet Systems

Editable English Slides source for five independently tracked SCORM 1.2 modules.
The course contains 45 narrated slides, ten questions, five workbook exercises,
and five narration-synchronized teaching videos. Course Home is an untracked
asset. The approved formal LMS catalog copy and learner-time estimates are in
[lms-catalog.md](lms-catalog.md).

## Source layout

- `course.json`: complete slide content, questions, feedback, narration settings,
  glossary, media inventories, primary references, and LMS catalog fields.
- `audio/module*/`: all 45 approved narration scripts.
- `figures/`: editable SVG diagrams, five teaching videos, and their posters.
- `tools/synced_video/`: deterministic vector scene implementations and encoders.
- `video_source/`: final measured scene timing, approved storyboards, and technical
  source constraints. See [video production](tools/synced_video/README.md).
- `scripts/build_resources.py`: editable workbook exercises and offline glossary
  generation. The workbook is a teaching aid rather than a compliance checklist.
- `tools/academy_wizard/`: validated build sources and tests; see its `SOURCE.md`.
- `thumbnail.svg` and `thumbnail.png`: editable poster and 800 × 400 LMS image.

## Rebuild

Run from the repository root to reuse approved narration already on disk:

```sh
EXISTING_AUDIO_DIR=/path/to/approved/audio bash scripts/build-course.sh fcsa-architecting-interoperable-chiplet-systems
```

To generate missing narration, run `python3 tools/generate_narration.py` from this
course folder, then point `EXISTING_AUDIO_DIR` at its generated `audio/` folder.
The key comes from the environment or a hidden prompt. The recorded setup is
ElevenLabs v4 with the same Leo voice and same-text Multilingual v2 pacing at
1.18. Generated WAVs, runtime pages, and ZIPs stay in ignored output folders.
`SKIP_AUDIO=1` supports a render-only build without publishing a ZIP.

Output is `build/fcsa-architecting-interoperable-chiplet-systems/` and its sibling
ZIP, accompanied by LMS catalog JSON, Markdown, and HTML. Source catalog exports
remain beside `course.json`, separately from this maintenance README.

To preview the built pages with byte-range video seeking:

```sh
python3 courses/fcsa-architecting-interoperable-chiplet-systems/tools/preview.py --port 8880
```

Open `http://127.0.0.1:8880/index.html?review=1`. Review mode starts paused and
isolates saved learner progress. Keep automated review muted.

## Media and evidence

Primary authority is [FCSA 1.1.0](https://www.opencompute.org/wp-content/uploads/2026/10/FCSA-1.1.0.pdf).
The course references both FCSA presentations in the 2026 Global Summit's
[Server: Open Chiplet Economy track](https://www.opencompute.org/events/ocp-summit/2026-ocp-global-summit/recorded-content/),
with timestamp links and source constraints in `course.json` and the storyboards.
The Physical AI workstream is identified as a proposal, distinct from published
FCSA requirements. Research PDFs and raw working transcripts are maintained
outside the source repository.

All five silent teaching videos follow measured narration timing through pause,
seek, replay, and speed changes, then hold the final frame. Install `npm install`
and `python3 -m pip install -r requirements-media.txt` from the course folder to
edit their sources. Encoding requires FFmpeg with libx264. Normal builds use the
checked-in videos directly.

Source QA and full package validation verified the repository build. The workbook
print action uses an event listener for strict LMS compatibility. Target-LMS
launch, resume, completion, and separate module reporting remain deployment
acceptance checks.

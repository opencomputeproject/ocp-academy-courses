# Open Chiplet Economy: Business and Technology of Chiplet-based Systems

Editable English Slides source for nine independently tracked SCORM 1.2 modules.
The course contains 114 slides, 100 narration scripts, nine teaching animations,
four narration-synchronized sequences, fourteen captioned recordings, and nineteen
knowledge checks. Course Home is an untracked asset. The approved LMS catalog
copy and learner-time estimates are in [lms-catalog.md](lms-catalog.md).

## Source layout

- `course.json`: slide content, questions, feedback, narration settings,
  glossary, media inventories, source references, and LMS catalog fields.
- `audio/module*/`: approved narration scripts paired with generated WAV names.
- `figures/`: editable diagrams, video posters, teaching videos, and the fourteen
  Academy recordings under `figures/original/`.
- `captions/`: fourteen optional English VTT tracks; full recording transcripts
  are also stored with the slides in `course.json`.
- `animation_sources/`: five browser-native teaching animation sources.
- `tools/synced_video/`: four deterministic vector sequences, timing, measured
  text bounds, and production metadata. Approved storyboards and constraints
  are in `video_source/storyboards/`.
- `tools/academy_wizard/`: the validated course toolchain; see its `SOURCE.md`.
- `scripts/build_resources.py`: generates the offline glossary.
- `thumbnail.svg` and `thumbnail.png`: editable poster and 800 × 400 LMS image.

## Rebuild

Run from the repository root. To reuse approved narration already on disk:

```sh
EXISTING_AUDIO_DIR=/path/to/approved/audio bash scripts/build-course.sh open-chiplet-economy
```

To generate missing narration, use the secure prompt from the course folder:

```sh
python3 tools/generate_narration.py
```

Then point `EXISTING_AUDIO_DIR` at that generated `audio/` folder and rebuild.
The recorded setting is ElevenLabs v4 with Leo, paced against same-text
Multilingual v2 at 1.18. A key is read from the environment or a hidden prompt.
Generated narration, SCORM ZIPs, and rendered runtime pages stay in ignored output
folders. A render-only build can use `SKIP_AUDIO=1`; it does not publish a ZIP.

Output is `build/open-chiplet-economy/` and its sibling ZIP. Matching LMS catalog
JSON, Markdown, and HTML files accompany the ZIP. Source JSON/Markdown catalog
exports remain beside `course.json`, separately from this maintenance README.

Preview the built course with byte-range video support:

```sh
python3 courses/open-chiplet-economy/tools/preview.py --port 8879
```

Open `http://127.0.0.1:8879/index.html?review=1`. Review mode starts paused and
isolates saved learner progress. Keep audio muted during automated review.

## Media and evidence

The recordings originate from the [Open Chiplet Economy learning plan](https://academy.opencompute.org/learn/learning-plans/1/open-chiplet-economy-business-and-technology-of-chiplet-based-systems).
They preserve their original video and sound. VTT captions were transcribed with
ElevenLabs Scribe v2 and reviewed for recognition spelling and cue quality;
captions are off by default. Source names and links are retained in `course.json`.
Primary OCP contribution and 2026 Summit references remain attached to the
relevant slides. Research PDFs and raw transcript-service responses are working
materials outside the source repository.

Install media-authoring dependencies with `npm install` and
`python3 -m pip install -r requirements-media.txt` from this course folder.
FFmpeg with libx264 is required to encode changed videos. The checked-in videos
can be used directly for normal course builds. See
[video production](tools/synced_video/README.md) before changing a sequence.

Source QA, full package validation, and byte comparisons verified the repository
build against the approved local delivery. Target-LMS launch, resume, completion,
and separate module reporting remain deployment acceptance checks.

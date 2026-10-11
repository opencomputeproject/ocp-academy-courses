# Integrating Quantum Processing Units into Data Center Infrastructure

An OCP Academy course on deploying QPUs as hybrid data center infrastructure. This standalone, four-module Slides course has approximately 40 minutes of approved narration, plus time for the knowledge checks and learner resources. The OCP whitepaper is the primary source, supported by the selected 2026 OCP EMEA Summit Quantum presentations.

This course source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and figure assets in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Narrated Time | Summary |
|---|---|---|---|
| 1 | Why Quantum Belongs in the Data Center | ~8 min | Establishes the market context and OCP workstream goals, explains why quantum computing depends on classical infrastructure, and connects modality choices to deployment decisions. |
| 2 | The Logical QPU and Its Classical Stack | ~10 min | Explores the reference architecture and logical QPU components, follows the classical control and feedback loop, and examines error-correction data growth and deployment coupling. |
| 3 | Facility Readiness by Modality | ~12 min | Assesses site selection, service boundaries, vibration and electromagnetic conditions, power and cooling, and the different operating requirements of cryogenic, laser/vacuum, and photonic systems. |
| 4 | From Pilot Deployment to OCP Practice | ~10 min | Moves from bespoke pilots toward repeatable operations, monitoring and service, shared infrastructure, relevant OCP domains, and a practical readiness checklist. |

Each module includes a two-question knowledge check before the final wrap-up slide: one single-choice question followed by one multi-select question.

## Current Skill Refresh

- One silent, ten-second teaching animation per module: hybrid infrastructure, the quantum-classical feedback loop, site readiness, and repeatable operations.
- Page-specific whitepaper links on teaching slides and whole-document links at course completion. Reused paper images retain their figure-number captions.
- First-use glossary references backed by reviewed, hash-bound visible-media text inventories.
- Current shared Slides player and resume behavior, with informational home tiles and the default first-module action.
- Exact 800x400 LMS thumbnail with the approved `OCP QUANTUM` badge. Editable artwork and renderer are in `poster/`.

Approved narration scripts and all eight knowledge-check questions are unchanged. This refresh retains SCORM 1.2, the separate Course Home/module SCOs, and the existing deployment identifiers. Use the LMS syllabus to select tracked modules; a direct home-page link is not proof of a target-SCO handoff.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh integrating-quantum-processing-units-into-data-center-infrastructure
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh integrating-quantum-processing-units-into-data-center-infrastructure
```

The build uses the repository's bundled AcademyWizard skill. Run the source gates from the repository root before opening a PR:

```bash
python3 skills/academy-wizard/scripts/slides_course_qa.py \
  courses/integrating-quantum-processing-units-into-data-center-infrastructure/course.json \
  --repo-root . --fail-on-flags
python3 skills/academy-wizard/scripts/check_svg_arrows.py \
  courses/integrating-quantum-processing-units-into-data-center-infrastructure/course.json \
  --fail-on-flags
```

Animation reproduction and media-review details are documented in `animations/README.md`. To reproduce the thumbnail, install Sharp for Node.js, then run `node poster/render_thumbnail.cjs` from this course folder. The artwork uses Avenir Next with Arial as a fallback; font availability can affect rasterized text.

## Verification

The October 2026 refresh passed source, glossary, PDF-link, arrow-geometry, package, archive-integrity, and all 40 audio-tail checks. Rendered-page inspection confirms 40 slides, eight questions, four silent looping videos, valid inline JavaScript, and the preserved SCORM identifiers. The approved audio and question blocks were compared with the previous source.

File-based media review included full-size SVGs and posters, decoded frames at the beginning, quarter points, end, and state transitions, plus lossless-source comparisons at native size and 200% detail. All four videos are 1920x1080 VP9, 150 frames at 15 fps, exactly ten seconds, with no audio stream. Normalized YUV SSIM was 1.000; RGB PSNR exceeded 56 dB for every clip.

Browser playback, responsive layout, a complete real-time loop, and target-LMS resume/completion were not verified in this environment. Test a separate LMS upload before replacing deployed training, especially the first-module action and per-module tracking. No LMS format migration is included.

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- OCP whitepaper: Integrating Quantum Processing Units into Data Center Infrastructure: https://www.opencompute.org/documents/integrating-qpus-into-dc-infrastructure-pdf
- OCP FTI workstream: Data Center Integration of Quantum Information Infrastructure: https://www.opencompute.org/community/data-center-integration-of-quantum-information-infrastructure
- 2026 OCP EMEA Summit FTS Quantum Track: https://www.opencompute.org/events/past-events/2026-ocp-emea-summit#fts-quantum
- YouTube playlist: 2026 OCP EMEA Summit FTS Quantum Track: https://www.youtube.com/playlist?list=PLAG-eekRQBSgWit1dUFGB4vbjs7FstsXy

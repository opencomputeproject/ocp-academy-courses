# LVDC Power Distribution for Data Centers

Narrated OCP Academy Slides course based on the **DCF Power Distribution LVDC white paper v1.1.0**. Ten modules contain 100 slides, 20 knowledge-check questions, 19 static teaching figures and nine approved narration-synchronized videos. Module 9 deliberately uses a worked evidence matrix. Recorded narration totals approximately 105.2 minutes; the 180-minute learning plan also allows for questions, references and the optional review worksheet.

## Learning sequence

1. LVDC adoption and system architecture
2. Voltage and interface compatibility
3. Polarity, earthing and midpoint behavior
4. Fault behavior and protection coordination
5. Main components and energy storage
6. Rack and equipment interfaces
7. Sequence of operations and control
8. Electromagnetic compatibility
9. Verification, certification and evidence
10. Integrated system review

The primary paper is cited by page on teaching slides. The public 2026 OCP EMEA Summit presentation and six companion Academy courses provide context: Grid Disturbance Performance, Open Data Center for AI, Solid State Transformers, Energy Storage Systems, Diablo 400 and Project Deschutes CDU. Companion courses are optional and do not add completion gates. Internal webinar materials informed authoring and are not learner references.

## Editable source

- `course.json`: slides, assessment, transcripts, glossary, references and recorded approval decisions.
- `audio/moduleN/*.txt`: the 100 narration scripts; generated WAVs are excluded from Git.
- `figures/`: course-owned static figures, silent MP4s and posters.
- `animations/` and [video production notes](animations/enhanced/README.md): deterministic diagrams, editable storyboards and an exporter. `poster.json` produces the 800 × 400 course poster.
- `figure-plan.json` and [video enhancement plan](video-enhancement-plan.md): media intent and source mapping.
- `resources/templates/*.html.template`: editable source templates for related learning, the review worksheet and attribution. The build stages these as runtime HTML; the home page lists only the external paper, related-learning guide and worksheet.
- `assets/fonts/`: local Open Sans files and font licenses; Lato resource fonts reside under `resources/`.

Do not regenerate narration or videos unless their source changes. Changing narration duration requires updating the relevant scene timings and video duration, transcript and reviewed text inventory. The paired audio remains the single audible track. This course explicitly opts into synchronized playback; rebuilding another course does not opt it in.

## Build

Use Python 3.9+ and the repository's bundled AcademyWizard skill. Supply the original v1.1.0 PDF locally so the 50 teaching-slide page references retain their exact edition. Research PDFs are not committed. `scripts/build_resources.py` verifies the supplied paper's SHA-256 before staging it:

`bf540bad775551dc48c8119f2a23eea193a3ec4e4bf45576b7bf369337326c07`

From the repository root, reuse reviewed narration:

```sh
export LVDC_PAPER_PATH="/path/to/DCF Power Distribution LVDC white paper version 1.1.0.pdf"
export EXISTING_AUDIO_DIR="/path/to/reviewed/package/audio"
./scripts/build-course.sh lvdc-power-distribution-for-data-centers
```

To generate new narration, omit `EXISTING_AUDIO_DIR` and supply `ELEVENLABS_API_KEY` through your environment. This invokes paid speech generation. The recorded settings are Leo v2, ElevenLabs Multilingual v2 and speed 1.18. No credential is included in this source.

The build writes a complete package and ZIP beneath `build/`. The paper's official link is retained in `course.json`; it may require access that prevents unattended fetching. Local page anchors depend on the PDF viewer.

## Validation and release

See [QA.md](QA.md) for checks, reproduction commands and limits. Keep SCORM **1.2 multi-SCO**, separate Course Home/module syllabus activities and informational module tiles. The user-approved Start with MODULE 1 action sits above the tile grid. Target-LMS navigation, resume and completion require a separate deployment test; browser tests with mock SCORM do not establish LMS acceptance.

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/lvdc-power-distribution-for-data-centers
```

See [the poster standard](../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.

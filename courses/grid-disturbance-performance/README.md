# Grid Disturbance Performance for Hyperscale Data Centers

A standalone OCP Academy Slides course on the *Interface Specification Between Hyperscalers and Utility Grid for Disturbance Performance*, OCP v1.0.0, effective September 17, 2026. It connects voltage ride-through, active-power recovery and facility coordination to equipment reviews and implementation discussions. It is not part of a larger course series.

The course contains **40 narrated slides, four 1080p teaching videos, twelve technical diagrams and eight knowledge-check questions**. Allow approximately **60–65 minutes**, including **35.8 minutes of narration**, examples, questions and review. Fresh synthesis and actual learner time may vary.

| Module | Topic | Narration | Estimated learning time |
|---|---|---:|---:|
| 1 | Define the Grid–Data Center Interface | 8:57 | 15 minutes |
| 2 | Read and Apply the Voltage Ride-Through Envelope | 8:51 | 17 minutes |
| 3 | Recover Active Power and Coordinate the Facility | 9:01 | 16 minutes |
| 4 | Choose Mitigations and Plan Implementation | 8:57 | 16 minutes |

Each knowledge check has one single-answer question and one multi-select question. Learners must attempt both to continue; feedback and retries support learning, and correctness is not required for progression.

## Source and learning aids

[Official specification](https://www.opencompute.org/documents/ocp-base-spec-interface-specification-between-hyperscalers-and-utility-grid-for-disturbance-performance-pdf). The public URL and source filename preserve provenance; the research PDF is not committed. Slide-level `source_refs` retain page references for editorial review.

The general specification link appears in the opening overview and final course closing. Interior references are selective deeper-reading links; explicit Table 1 discussions link to page 15. Nine glossary terms have fifteen evidence-backed first-use placements. Module 2 previews the 80 MW worked example in Module 3.

The course preserves Table 1 boundaries, durations, computational-load scope and footnote 5. It labels the implementation timeline as an OCP proposal and the worked traces as illustrations. It does not invent frequency/phase-jump limits, a universal cooling-autonomy duration or a certification procedure.

## Editable source

- `course.json`: authoritative slide content, transcripts, glossary evidence, media inventory, source links and approved presentation/navigation settings.
- `audio/moduleN/*.txt`: all 40 narration scripts, paired with the WAV paths declared in the course source. Keep scripts and authored transcripts synchronized.
- `figures/`: twelve SVG diagrams, four silent H.264 teaching videos and their PNG posters.
- `animations/`: editable finite HTML/SVG/CSS video masters with declared duration and poster time. Re-record using the shared `record_css_animation.mjs` workflow and renew visual review and inventory hashes after media changes.
- `thumbnail.png`, `artwork/thumbnail.html`, `grid_disturbance_mark.svg`: approved 800×400 LMS poster, self-contained editable poster artwork and course mark. The poster artwork embeds the authoritative OCP logo and Lato Bold font; render its 800×400 browser canvas after fonts load.
- `LMS_UPLOAD_COPY.md`: title, short description and module-by-module LMS overview.

Generated narration, rendered course pages, SCORM ZIPs, credentials and research documents are excluded from source control. The HTML files under `animations/` and `artwork/` are editable media masters, not generated learner pages.

## Build

From the repository root, with an authorized ElevenLabs key in the environment:

```bash
./scripts/build-course.sh grid-disturbance-performance
```

Narration pins ElevenLabs Leo v2, `eleven_multilingual_v2` and speed **1.18**. Regenerate only changed clips with these settings. To rebuild using already approved narration without paid synthesis:

```bash
EXISTING_AUDIO_DIR=/path/to/approved/audio ./scripts/build-course.sh grid-disturbance-performance
python3 skills/academy-wizard/scripts/slides_course_qa.py \
  courses/grid-disturbance-performance/course.json --repo-root . --fail-on-flags
python3 skills/academy-wizard/scripts/check_svg_arrows.py \
  courses/grid-disturbance-performance/course.json --fail-on-flags
```

Output is written beneath `build/grid-disturbance-performance/`, with the strict upload ZIP alongside it. `SKIP_AUDIO=1` produces an incomplete visual preview, not a validated upload package. Open `index.html?review=1` for quiet home review; its Start action opens Module 1 at slide 1 with narration off and no LMS writes.

## Approved home and LMS navigation

Preserve **SCORM 1.2 multi-SCO**, Course Home and four separate module syllabus entries, and the original launch identifiers. The September 23 home uses informational numbered tiles with no status labels, inferred progress, links or hover lift. Its instruction reads **Navigate modules in any order using the Syllabus in the left sidebar.** Below it, an indigo **Start with MODULE 1** label sits beside the canonical green circular double-chevron control.

The course records the user's approved SST-style direct Start/Next/Home links as `scorm.navigation: direct`. This is an explicit compatibility choice: ordinary page links do not ask an LMS to launch a different SCO. Use the LMS Syllabus for separate module tracking. This course retains the standard slide-resume behavior; it does not select the separate HBF module-only compatibility profile.

## September 24 player refresh

Rebuild with the current repository-bundled AcademyWizard player. Quiz answers, feedback and attempted state survive module revisits in the LMS and ordinary local playback. Retry clears the saved question. Unfinished modules resume at their own last-viewed slide; completed modules reopen at their final slide, including after browsing backward or retrying a quiz.

The upper-left course mark links to Course Home. Editorial `?review=1` navigation retains review mode through Next and Home; Next starts the following module at slide 1 without reading or changing learner progress. Looping teaching videos seek to the corresponding point within their cycle when narration is resumed or scrubbed. The maintained mobile title layout prevents narrow-screen clipping.

This refresh preserves the course content, forty narration clips, teaching media, poster, syllabus-led home and SCORM 1.2 manifest. Compared with the September 23 delivery, only the four module HTML files change; the other 65 runtime files are byte-identical. Generated pages, narration and the delivery ZIP remain outside source control.

The refreshed build passes source QA, diagram checks, all forty acoustic checks, package validation, 55 Python tests, 103 maintained player browser assertions and 46 home/navigation browser assertions. Run the player and home checks from the repository root after a build:

```bash
node skills/academy-wizard/scripts/test_slide_resume_browser.mjs build/grid-disturbance-performance
node skills/academy-wizard/scripts/test_syllabus_home_browser.mjs build/grid-disturbance-performance
```

All narration passed acoustic checks, every video and diagram was visually reviewed, and desktop/mobile layouts and player interactions passed local browser checks. Target-LMS navigation, resume and separate completion/reporting still require acceptance testing. Local simulation does not establish Docebo tracking compatibility; this contribution does not upload or replace live LMS material.

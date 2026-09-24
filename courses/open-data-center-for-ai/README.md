# Open Data Center for AI

A standalone, four-module OCP Academy Slides course applying Open Data Center Specification Revision 0.7. It connects heavier equipment, facility interfaces, power and cooling density, and supplier flexibility to practical project-review decisions. It is not part of an existing meta-series.

The course uses the published specification as its technical baseline, with the Open Data Center for AI Strategic Initiative whitepaper and OCP EMEA Summit panel for context. The collaboration discussion includes AMD, Google, Meta, and NVIDIA.

## Modules

| Module | Title | Narration | Learner focus |
|---|---|---:|---|
| 1 | Why Open Data Center for AI? | 6:04 | Recognize deployment blockers, understand the specification's evolution, and preserve supplier choice through common interfaces. |
| 2 | The Facility Compatibility Envelope | 5:02 | Check rack movement, structural loads, dimension datums, overhead capacity, and modular row density. |
| 3 | Power and Cooling at AI Density | 5:52 | Separate blended and peak density, apply capacity values at the correct scale, and distinguish manifold reach from rack connections. |
| 4 | Apply 0.7 Without Freezing Innovation | 5:03 | Evaluate design examples, assemble compatibility evidence, and record site-specific questions for accountable reviewers. |

There are 37 slides, four narrated two-question knowledge checks, and nine silent teaching videos. Measured narration totals **22:01**; estimated completion time is **45 minutes** including interaction and reference review, pending a learner pilot. Times are rounded to the nearest second from the reviewed narration; fresh TTS can vary.

## Editable source

- `course.json`: slide content, glossary evidence, source links, transcripts, media assignments and explicit narration settings.
- `audio/moduleN/*.txt`: narration scripts. Keep the associated `transcript` in `course.json` synchronized when editing narration; scripts use pronunciation spelling while transcripts use conventional acronyms.
- `figures/`: source-native SVG diagrams, nine 1080p H.264 silent videos and posters, and 15 attributed source-figure extracts.
- `animations/`: editable finite HTML/SVG/CSS masters, with declared duration and poster time. Use the shared `record_css_animation.mjs` recorder after reviewing changes; re-review hash-bound media text inventories whenever an encoded asset changes.
- `scripts/build_resources.py`: builds the compatibility worksheet, requirements ledger, full transcript and source-figure gallery in the staged package. The gallery reserves source-image dimensions for reliable initial fragment navigation.
- `thumbnail.png`, `LMS_Open_DC_800x400.svg`, `open_dc_course_mark.svg`: approved LMS art and simplified rack-row course mark.
- `LMS_UPLOAD_COPY.md`: title, short description and incentive-led, module-by-module LMS overview.

No generated WAVs, rendered course/resource pages, SCORM ZIPs, credentials or original research documents are committed. Public source URLs and source filenames retain provenance without workstation paths.

## Build

From the repository root, with an authorized ElevenLabs key in the environment:

```bash
./scripts/build-course.sh open-data-center-for-ai
```

The course pins Leo v2, `eleven_multilingual_v2`, and speed **1.18**. Do not change these without explicit approval. No key belongs in a source file or commit.

To verify with already generated narration without paid synthesis or audible playback:

```bash
EXISTING_AUDIO_DIR=/path/to/approved/audio ./scripts/build-course.sh open-data-center-for-ai
python3 skills/academy-wizard/scripts/slides_course_qa.py \
  courses/open-data-center-for-ai/course.json --repo-root . --fail-on-flags
```

Output is a **SCORM 1.2 multi-SCO** package under `build/open-data-center-for-ai/`, plus its strict manifest-only ZIP. It preserves five original syllabus entries and launch identifiers: Course Home plus four modules. There is no single-session `launch.html` shell. The learner-resource builder writes only beneath this output directory. `SKIP_AUDIO=1` permits an incomplete visual preview but not a validated upload package.

For quiet home review, open `index.html?review=1`. The Start button opens Module 1 at slide 1 with narration off and no LMS writes. A module's `?review=1&slide=N` link permits direct editorial review; Home/Next links carry review mode forward. Normal LMS launches retain authored narration defaults. No browser or system audio settings are changed by the build or tests.

### Approved September 23 syllabus-led navigation

Home uses informational numbered tiles without progress labels, inferred completion colors, links or misleading hover effects. Below them it says **Navigate modules in any order using the Syllabus in the left sidebar.** The instruction matches normal tile body text. **Start with MODULE 1**, in OCP indigo, sits left of the same green 46px circular double-chevron control used at non-final module endings.

The source records `scorm.organization: multi-sco` and the approved `navigation: direct`. On September 24 the user explicitly retired the earlier module-only exception and requested the maintained AcademyWizard behavior. The course now uses the shared `learner_features.js` player and `scorm_api.js` wrapper, without a compatibility-profile selection. Unfinished modules resume at their saved slide. Completed modules return to their final slide, retaining quiz answers and feedback even after a backward visit. The existing five syllabus entries, module identifiers and ordinary Start/Next/Home links remain. There are no course-specific LMS IDs, private APIs, deployment mappings or SCORM 2004 conversion.

Use the **LMS Syllabus** to select arbitrary modules. Direct Start/Next/Home links preserve the approved compatibility behavior; they are not standard SCORM 1.2 target-SCO requests and cannot themselves change the LMS tracking context. Actual LMS handoff, module completion and close/reopen behavior still require deployment testing. The final home design was browser-approved; local tests are not new Docebo acceptance. Test a separate upload before changing live training material. No live LMS upload, deletion, reset or progress migration is performed by this contribution.

Run the local regression tests with:

```bash
python3 -m unittest discover -s skills/academy-wizard/scripts -p 'test_*.py'
node skills/academy-wizard/scripts/test_syllabus_home_browser.mjs build/open-data-center-for-ai
node skills/academy-wizard/scripts/test_slide_resume_browser.mjs build/open-data-center-for-ai
node skills/academy-wizard/scripts/test_quiz_resume_browser.mjs build/open-data-center-for-ai
```

The disposable browser tests block external network calls and audio playback. They check informational tiles, exact wording and styling, canonical button parity, keyboard focus, mobile layout down to 320px, first-module review navigation, zero home progress reads, and per-slide bookmarking for all four modules. Resume tests cover abandoning/reopening unfinished modules, independent module bookmarks, completed-module revisits, answers/feedback/Retry, and review-state isolation. The separate single-SCO regression tests remain for courses that explicitly select that organization; they do not describe this course.

The refreshed rebuild was compared with the approved September 23 delivery: 83 of 88 runtime files are byte-identical. The four module pages use the maintained player, and the wrapper is now the maintained shared wrapper. All learner content, audio, media, the home page, resources and manifest are unchanged. A second source render reproduces all 88 refreshed runtime files exactly. Generated WAVs and ZIPs remain outside source control.

### September 24 player refresh — approved

The refresh builds on current shared code rather than replacing it with an older installed copy. The maintained player restores the narration-on hint, seeks looping videos within their cycle while holding finite videos on their last frame, resumes unfinished modules at the saved slide and completed modules at the ending, and carries editorial Next links to `?review=1&slide=1`. Shared quiz state restores answers and feedback before navigation; Retry persistently clears only the selected question. Editorial review does not read or write slide, quiz or completion state. Mobile titles now scale within narrow screens and scroll clear of the badge and controls; desktop styling is unchanged. The five-entry SCORM 1.2 organization, home styling, content, voice, synthesis speed, and approved media remain unchanged.

The user approved the local review on September 24 and authorized packaging that exact build and opening a signed source-only follow-up PR. For future refreshes, use the scaffold, resource builder and renderers with approved audio for the unzipped review copy, then wait for explicit local approval before ZIP or PR delivery. No LMS access or deployment testing is part of this refresh.

## Approved presentation choices

OCP green/gray/white remain the main palette. Blue supply (`#2474C4`) and red return (`#C8453D`) are explicit, course-specific thermal overrides, not new global brand defaults. Source artwork retains its original colors. Narration and Transcript controls sit beside playback speed; fullscreen is at the left. Glossary pills occur only at actual first teaching use, never on quizzes or module opening/closing slides. M4S9 closes with thanks and encouragement, not a spoken branding slogan.

## Sources and review limits

- [Published Revision 0.7 specification](https://www.opencompute.org/documents/open-data-center-spec-revision-0-7-0-4-pdf), effective August 27, 2026.
- [Revision 0.5 specification](https://www.opencompute.org/documents/open-data-center-spec-version-0-5-0-pdf), used for historical comparison.
- [Open Data Center for AI whitepaper](https://www.opencompute.org/documents/ocp-open-data-center-for-ai-whitepaper-final-pdf).
- [OCP EMEA Summit panel recording](https://www.youtube.com/watch?v=Riz5RgwzUzo).
- [Call for collaboration](https://www.opencompute.org/about/a-call-for-collaboration-on-ai-data-center-infrastructure-standards).

The published cover/authors and technical pages 7–9 were checked. Full published-PDF reconciliation remains open: the supplied physical-figure extracts are explicitly labeled as from the June 23 draft. Their Google/NVIDIA attribution is retained in the gallery; Appendix reuse terms need confirmation by the release owner. Engineering schematics are teaching models, not validated construction details. Expert review, headphone pronunciation/naturalness review, actual-LMS testing, and a learner/accessibility pilot remain distinct from local automated checks.

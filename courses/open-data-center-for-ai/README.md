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

Output is a **SCORM 1.2 single-SCO** package under `build/open-data-center-for-ai/`, plus its strict manifest-only ZIP. `launch.html` keeps one LMS session open while the learner uses the existing home page and four modules. The learner-resource builder writes only beneath this output directory. `SKIP_AUDIO=1` permits an incomplete visual preview but not a validated upload package.

For quiet review, open a generated module using `?review=1&slide=N`; narration starts off and no LMS progress is written. To test the entire session outside an LMS, serve the package over HTTP and open `launch.html`; add `?review=1` for untracked review with narration off. Normal LMS launches retain authored narration defaults. Home cards and next-module buttons navigate inside the course, and the course mark links back to its home. Module bookmarks, quiz attempts and completion marks are retained internally. Docebo records overall completion only when all four modules and their quiz gates are complete.

### September 10 navigation repair and upload warning

The September 9 multi-SCO package blocked home-card and next-module clicks in LMS mode. The repair keeps **SCORM 1.2** and explicitly selects `scorm.organization: single-sco`. It avoids both direct navigation between separately tracked SCOs and reliance on unsupported SCORM 2004 sequencing. Existing courses without this option remain multi-SCO; no global default or SCORM-version conversion is imposed.

**The syllabus changes from five separately tracked entries to one course activity, despite keeping version 1.2. Existing attempts/bookmarks may not transfer.** Test a separate Docebo upload and export any needed reports before replacing the old material. Do not treat this as a guaranteed progress-preserving overwrite. No live LMS deletion, reset or upload is part of this repository change. Deleting old Docebo material deletes its tracking.

Run the local regression tests with:

```bash
python3 -m unittest discover -s skills/academy-wizard/scripts -p 'test_*.py'
node skills/academy-wizard/scripts/test_single_sco_browser.mjs build/open-data-center-for-ai
```

The browser test uses a strict local SCORM 1.2 simulation and disables media playback. It covers every home card, all next-module links, course-home return, quiz gates and records, persistent bookmarks, one-session lifecycle, overall completion, failure warnings, untracked review and a 320px viewport. Actual Docebo acceptance remains required, including player sizing and close/reopen tracking. The package uses an internal iframe; test Docebo's new-window mode if inline playback has sizing or frame restrictions.

## Approved presentation choices

OCP green/gray/white remain the main palette. Blue supply (`#2474C4`) and red return (`#C8453D`) are explicit, course-specific thermal overrides, not new global brand defaults. Source artwork retains its original colors. Narration and Transcript controls sit beside playback speed; fullscreen is at the left. Glossary pills occur only at actual first teaching use, never on quizzes or module opening/closing slides. M4S9 closes with thanks and encouragement, not a spoken branding slogan.

## Sources and review limits

- [Published Revision 0.7 specification](https://www.opencompute.org/documents/open-data-center-spec-revision-0-7-0-4-pdf), effective August 27, 2026.
- [Revision 0.5 specification](https://www.opencompute.org/documents/open-data-center-spec-version-0-5-0-pdf), used for historical comparison.
- [Open Data Center for AI whitepaper](https://www.opencompute.org/documents/ocp-open-data-center-for-ai-whitepaper-final-pdf).
- [OCP EMEA Summit panel recording](https://www.youtube.com/watch?v=Riz5RgwzUzo).
- [Call for collaboration](https://www.opencompute.org/about/a-call-for-collaboration-on-ai-data-center-infrastructure-standards).

The published cover/authors and technical pages 7–9 were checked. Full published-PDF reconciliation remains open: the supplied physical-figure extracts are explicitly labeled as from the June 23 draft. Their Google/NVIDIA attribution is retained in the gallery; Appendix reuse terms need confirmation by the release owner. Engineering schematics are teaching models, not validated construction details. Expert review, headphone pronunciation/naturalness review, actual-LMS testing, and a learner/accessibility pilot remain distinct from local automated checks.

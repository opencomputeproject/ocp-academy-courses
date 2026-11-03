# OCP Project Brazos: Liquid Cooling in Air-Cooled Data Centers

A standalone, intermediate OCP Academy Slides course for data-center engineers, thermal engineers, rack integrators, and operations teams. It explains how Brazos moves IT heat from a closed liquid loop into facility air and how to assess a proposed deployment against specification v0.75.4, effective September 11, 2026.

The course has **40 narrated slides, four synchronized teaching videos, and eight knowledge-check questions**. Allow approximately **53 minutes** within a 45–60-minute learning-time target. The reviewed narration totals **32:54**; reading, reflection, questions, and feedback account for the rest. Optional reference study and companion courses add time. There are no forced slide timers.

| Module | Planned learner time | Reviewed narration |
|---|---:|---:|
| Follow the Heat Through Brazos | 12 min | 7:22 |
| Cooling Performance | 14 min | 8:14 |
| Integrate and Service the Rack | 13 min | 8:07 |
| Control, Monitor, and Validate | 14 min | 9:12 |

Each module has one single-answer and one multi-select question. Both require an attempt, correctness is not required, and retries are available. Glossary aids are placed at eligible first substantive uses. Optional companion links lead to [Cooling Fluids in DLC](https://academy.opencompute.org/learn/courses/52/cooling-fluids-in-direct-liquid-cooling-dlc) and [Project Deschutes CDU](https://academy.opencompute.org/learn/courses/48/ocp-project-deschutes-coolant-distribution-unit-cdu-v10).

## Sources and scope

The [official Brazos v0.75.4 specification](https://www.opencompute.org/documents/ocp-specification-project-brazos-v-0-75-4-final-pdf) governs the technical content. [Google's June 16, 2026 announcement](https://cloud.google.com/blog/topics/systems/brazos-liquid-cooling-system-for-air-cooled-data-centers) supplies historical context; June 30 is the separate initial specification-release date. `SOURCE_NOTES.md` records page coverage, key requirements, and source ambiguities.

The course preserves the conditions behind ratings, distinguishes chassis and rack quantities, flags the Table 4.1 flow inconsistency, and does not infer failed-chassis capacity from a nominal rating. Flow-marker speeds and the approach-temperature arithmetic are illustrative. The exact research PDF is excluded from Git and supplied at build time so learners retain offline page links.

## Editable source

- `course.json`: authoritative content, transcripts, source references, glossary evidence, and media settings.
- `audio/moduleN/*.txt`: forty narration scripts; generated WAV files stay outside source control.
- `figures/`: source illustrations, three SVG explanations, four H.264 teaching videos, and final-state posters.
- `animations/`: editable deterministic scene sources, measured storyboards, HTML previews, and a portable exporter.
- `assets/fonts/`: the licensed Open Sans font set for offline use.
- `brazos_mark.svg`, `thumbnail.png`, and `poster.json`: the liquid-to-air course mark and editable 800×400 catalog poster.
- `LMS_UPLOAD_COPY.md`: title, short description, and module-by-module course overview.
- `QA.md`: reviewed-build checks and the target-LMS acceptance boundary.

## Build the reviewed package

From the repository root, supply the exact specification and approved narration:

```bash
BRAZOS_SPEC_PATH=/path/to/ocp-brazos-v0.75.4.pdf \
EXISTING_AUDIO_DIR=/path/to/approved/brazos/audio \
./scripts/build-course.sh ocp-project-brazos-liquid-to-air-cooling
```

The build hook checks the PDF digest, stages fonts and the poster, and verifies that synchronized-video narration matches the measured storyboard. The PDF SHA-256 is `ae0f339816a6fbe416d1b6478bfe434216805b39081eb0b292c406a2af5cfbfb`. Outputs appear under `build/ocp-project-brazos-liquid-to-air-cooling/`; its strict SCORM ZIP is adjacent. Generated narration, learner HTML, ZIPs, and original research PDFs are not committed.

To create new narration, use the course-specific `scripts/generate_narration.py` so the four video slides are generated in measured chapter groups. It reads `ELEVENLABS_API_KEY` or prompts without echo and preserves Leo v2, Multilingual v2, and speed 1.18. Run `--preflight` first. New audio requires re-exporting the synchronized videos and renewing the reviewed media inventories; see `animations/README.md`. Do not reuse an old video with a new narration timing or stretch narration to fit it.

For a local browser review with working media seeks:

```bash
python3 courses/ocp-project-brazos-liquid-to-air-cooling/scripts/serve_review.py \
  --directory build/ocp-project-brazos-liquid-to-air-cooling --port 8765
```

Open `http://127.0.0.1:8765/index.html?review=1`, or a specific `moduleN.html?review=1&slide=S`. The server binds only to localhost and supports byte ranges. Review mode starts paused and does not change learner progress.

## SCORM and LMS acceptance

The reviewed architecture remains SCORM 1.2 multi-SCO: Course Home and four separate module syllabus entries. Home tiles are informational, and the instruction directs learners to the LMS syllabus. The reviewed first-module start action is retained; direct page links are not standard SCORM target-SCO launch requests.

The ZIP is packaged for target-LMS acceptance testing. Home/Start/Next navigation, resume, and independent module completion still need verification on the actual LMS before learner release. Browser checks do not establish target-LMS tracking compatibility. This contribution does not upload, replace, or merge live LMS material.

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/ocp-project-brazos-liquid-to-air-cooling
```

See [the poster standard](../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.

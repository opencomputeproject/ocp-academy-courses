# AI Native Edge-MHS: Architecture and Integration Review

A 55-minute intermediate hardware-engineering course based on **AI Native Edge-MHS Base Specification v1.0.0** and its supplied 3D assemblies. The narrated Slides package has a tracked Course Home and three content SCOs in SCORM 1.2:

| Syllabus entry | Estimated learner time |
|---|---:|
| Course Home | 1 minute |
| Architecture and Class N/L | 16 minutes |
| Mechanical interfaces and compatibility | 20 minutes |
| Integration review exercises | 18 minutes |

The estimate includes narration, reading, review and exercises. Recorded narration runs 27.35 minutes. Optional Summit recordings are external resources and are excluded from the estimate.

## Editable source

- `course.json`: all 30 slides, six knowledge-check questions, glossary, page citations, media inventories, narration settings and approved LMS catalog copy.
- `audio/module*/slide_*.txt`: the 30 narration scripts. Generated MP3/WAV files stay outside Git.
- `figures/`: editable SVG figures, specification crops, three Astra-authored synchronized teaching videos and their posters.
- `animations/`: editable video HTML/SVG/timelines and portable production instructions.
- `assets/fonts/`: locally bundled Open Sans, license and provenance for offline playback.
- `poster.json`, `thumbnail.png`, `edge_mhs_mark.svg`: the shared 800×400 Academy poster and course artwork.
- `lms-catalog.json`, `lms-catalog.md`: prepared LMS fields, separate from this README.
- `authoring/outline.md`, `authoring/source-analysis.md`: scope, adjacent-course overlap and source-conflict decisions.
- `authoring/validation.json`: compact production and publication evidence.

## Sources and boundaries

The primary source is the [98-page Base Specification v1.0.0](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf). [The supplied 3D archive](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-V1.0.0-3D-Files.zip) provides illustrative geometry, rather than complete chassis qualification evidence. Source files remain outside Git.

The course labels requirements, recommendations, examples and excluded scope. It does not infer complete interoperability from outline fit or a matching CAD model. The Class L mounting-hole disagreement (table p. 14 versus body p. 44) and DC-SCM connector-reference disagreement remain explicit and are excluded from definitive numerical quiz answers.

The [AICC course](../ai-computing-continuum/README.md) supplies distributed-inference architecture context. The [MHS M-PNP course](../ocp-mhs-modular-plug-and-play-m-pnp/README.md) covers discovery, FRU data, boot coordination and management behavior. This course concentrates on Edge-MHS form factors and interface review, with links back to the adjacent material. Summit references and page-specific specification links are retained where used in `course.json`.

## Rebuild

`authoring/toolchain/` pins the validated AcademyWizard scripts, templates and brand assets. The repository build command selects that snapshot via `authoring_toolchain`, preserving the published player and tracking structure. Its provenance file records file hashes. The catalog exporter includes Course Home orientation time without changing the approved module estimates.

From the repository root, use an existing generated audio folder:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/audio bash scripts/build-course.sh ai-native-edge-mhs-architecture-and-integration-review
```

For a fresh narration job, follow the maintained AcademyWizard setup and provide credentials through the environment. Full Eleven v4, Leo voice, 1.18 pitch-preserving pacing and 96 kbps mono MP3 delivery are recorded in `course.json`. New synthesis can change timing: Astra's video timings must be reviewed and synchronized before release. See `animations/README.md` for video production. Do not treat an audio provider's word timing or a signal check as human pronunciation approval.

To check source metadata:

```sh
python3 skills/academy-wizard/scripts/course_delivery_summary.py courses/ai-native-edge-mhs-architecture-and-integration-review/course.json --check
python3 skills/academy-wizard/scripts/slides_course_qa.py courses/ai-native-edge-mhs-architecture-and-integration-review/course.json --repo-root . --fail-on-flags
```

## Validation and publication

The production review covered all slides at desktop and mobile sizes, offline local-file audio/video, quiz gates and resume behavior, synchronized video seeking and final-frame hold, manifest structure, poster dimensions, audio parity and script receipts. The release ZIP contains Course Home plus three tracked content entries and no authoring source or catalog sidecars.

Published on 16 November 2026 as [Docebo course 100](https://academy.opencompute.org/course/edit/100), linked to library material 364 V1 in **Docebo / Courses Made with AI** and assigned to **OCP Data Center Technologies**. Category: **DC Technologies**. Average time: **55 minutes**. Course code: blank. The poster and prepared summary were read back after saving.

Local mock-LMS checks do not establish target-LMS completion acceptance. In SCORM 1.2, the Home start and module-end links do not switch the LMS tracking context; the LMS must launch each syllabus entry for its own completion session. Hardware compliance and OCP recognition are outside this training's scope.

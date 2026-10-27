# Thermal Boundaries in AI Infrastructure

A standalone, intermediate OCP Academy Slides course based on the published OCP whitepaper, version 1.00, October 12, 2026. It teaches cooling-boundary diagnosis, architecture choices, and the evidence needed for deployment readiness.

The course contains **three modules, thirty narrated slides, three silent teaching animations, and six knowledge-check questions**. Allow approximately **50–55 minutes** including narration, diagram inspection, questions, and review. Generated narration totals **32.5 minutes**.

| Module | Estimated learner time | Generated narration |
|---|---:|---:|
| Why Cooling Transitions Happen | 18 min | 10:18 |
| Diagnosing the Heat and Matching the Architecture | 18 min | 10:51 |
| Economics, Reliability, and Readiness | 18 min | 11:18 |

Each module has one single-answer and one multi-select question. Both require an attempt; correctness is not required, and feedback and retry are available. The course assumes basic server, rack, and facility vocabulary. Companion Academy courses are optional.

## Sources and curriculum role

The [OCP whitepaper](https://www.opencompute.org/wp-content/uploads/2026/10/Thermal-Boundaries-in-AI-Infrastructure.pdf) governs the technical framework. Its authors are Rolf Brink, Mohan J. Kumar, Steve Mills, and Kelley Mullick. The reviewed 104-page PDF has SHA-256 `30f98ae4d788ef57f6665a707d0eedcb37dfc2c474a70b5a663b59ecd6288d48`.

The course distinguishes efficiency, economic, and physics boundaries; the avoidance zone; agency mismatch; preparation and complexity debt; concentrated and distributed heat; and acquisition, transport, and rejection. Its reference cold-plate envelope and modeled cost and reliability comparisons retain their stated conditions. Fictional teaching cases and conceptual animation quantities are identified; they are not measured site performance or universal technology ceilings.

`CURRICULUM_ALIGNMENT.md` records the cooling-course audit and cross-reference plan. Teaching slides link to Fluids, Two-Phase DLC, Deschutes, Brazos, Open Rack, and Open Data Center for AI where specialist detail becomes useful. Reciprocal additions to existing courses remain proposed until this course has a verified public Academy URL.

## Editable source

- `course.json`: authoritative slide content, transcripts, source references, glossary evidence, media, narration settings, and SCORM configuration.
- `audio/moduleN/*.txt`: thirty narration scripts. Generated WAV files remain outside source control.
- `figures/`: six SVG diagrams, two cropped source charts, three H.264 teaching videos, and their posters. M1S5 uses equal illustrative x-axis intervals and a green/yellow/red operating point. M2S5 keeps its top text clear of the circles and protects the central label from outline collisions.
- `animations/`: three finite HTML/CSS master timelines; see its README for re-export instructions.
- `thermal_boundaries_mark.svg`, `thumbnail.png`, and `artwork/thumbnail.html`: course mark, exact 800×400 LMS poster, and editable poster artwork with its licensed Lato font.
- `scripts/build_resources.py`: generates the source-credit and license page in the staged build and copies the catalog poster.
- `course.json.lms_catalog`, `lms-catalog.json`, and `lms-catalog.md`: formal LMS title, short description, and module-by-module overview with approximate learner durations. `LMS_METADATA.md` retains the delivery and upload notes.
- `OUTLINE.md`, `SOURCE_FIGURES.json`, and `QA.md`: course structure, complete source-visual inventory, and verification record.

## Rebuild

From the repository root, reuse the generated narration retained in the course-development workspace:

```bash
EXISTING_AUDIO_DIR=/path/to/thermal-boundaries/audio \
./scripts/build-course.sh thermal-boundaries-in-ai-infrastructure
```

The standard build uses the repository's AcademyWizard copy, generates the credits page, validates audio and runtime files, and writes the package and strict ZIP under `build/`. No original PDF is required for a normal rebuild: the extracted teaching charts are course-owned assets, and paper links use the canonical public URL.

The refreshed configuration is ElevenLabs **Leo v2** with model **`eleven_v4`**. Keep `narration.speed: 1.18`: v4 has no synthesis-speed parameter, so AcademyWizard matches each native v4 clip to the actual duration of its unchanged Multilingual v2 recording generated at 1.18, preserving pitch. The learner speed dial still starts at 1.0 and retains saved preferences. Learner-time estimates remain 18 minutes per module, approximately 50–55 minutes overall.

To regenerate narration, preserve the verified original v2 `course.json` and paired scripts/WAVs in a separate baseline directory, then run:

```bash
python skills/academy-wizard/scripts/gen_audio.py /path/to/staged/course.json \
  --force --pacing-reference-root /path/to/original-v2-baseline \
  --audio-work-dir /path/to/narration-work
```

Supply `ELEVENLABS_API_KEY` through the environment. Never use already processed v4 audio as the original baseline. Changed scripts require newly generated, cached v2 timing references; omitting the baseline option generates one additional billable reference request per new script. Native v4 masters and timing receipts stay in the separate work directory. Reuse the finished WAVs through `EXISTING_AUDIO_DIR` for subsequent builds. Credentials, masters, references, and generated narration are excluded from Git and the strict ZIP. Run the audio report and review pronunciation after regeneration.

Review the actual `index.html` and `module1.html` through `module3.html`; `?review=1` provides an editorial pass without saved progress. No separate review site is generated. The refresh also fits five static SVG artboards to their artwork; the approved M1S5 animation and M2S5 diagram geometry remain intact.

## Verification and LMS acceptance

The source QA, geometry checks, audio signal checks, package validator, local resume/quiz checks, and desktop/mobile visual reviews pass; see `QA.md`. Automated audio checks do not establish pronunciation. A human listening review and actual LMS acceptance remain unverified.

The course retains SCORM 1.2 multi-SCO: Course Home and three separate syllabus entries. Use the LMS Syllabus for tracked launches. The maintained first-module start link does not switch tracking to another SCO. Confirm launch, resume, and independent completion in the target LMS before learner release.

## Attribution and license

The adapted teaching content, scripts, and course-owned instructional media are provided under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), matching the primary source. `LICENSE.md` and the generated attribution page identify the original authors and adaptation. OCP marks retain their respective trademark rights; the poster font has its own SIL Open Font License.

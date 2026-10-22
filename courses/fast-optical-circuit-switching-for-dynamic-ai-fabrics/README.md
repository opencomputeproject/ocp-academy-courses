# Fast Optical Circuit Switching for Dynamic AI Fabrics

A standalone OCP Academy Slides course for an intermediate audience with a working knowledge of data center networks. The course examines workload timing, complete reconfiguration latency, switching mechanisms, and evidence for AI-fabric benefits.

Estimated learning time is 60 minutes, including 41 minutes of narration, knowledge checks, and diagram review. The course contains 45 slides, four narration-synchronized teaching videos, 15 static figures, and eight questions.

| Module | Focus | Estimated learning time |
|---|---|---:|
| 1. When Fast Optical Switching Matters | Communication windows, timescales, and conditions for benefit. | 12 minutes |
| 2. Making the Whole Reconfiguration Path Fast | Scheduling, control, settling, receiver recovery, endpoint readiness, and the critical path. | 17 minutes |
| 3. Switching Technologies and Deployment Constraints | Seven mechanism families, endurance, optical loss, port count, and integration. | 14 minutes |
| 4. AI Workloads, Evidence, and Evaluation | Hybrid fabrics, recovery, collective and expert traffic, compute utilization, and fair evaluation. | 17 minutes |

## Reference and attribution

The authoritative reference is [*Fast-Switching OCS: Benefits, Technologies, System-Level Considerations, and Emerging Applications for Dynamic AI Fabrics*](https://www.opencompute.org/wp-content/uploads/2026/10/OCP-OCS__Fast_Switching_OCS_October-19-2026_Final.pdf), by Iwan Kartawira, Michael DeMerchant, Swapna Nannapaneni, Spencer Giacalone, Shawn Chen, James Burch, Seema Mehta, and Zibo Hu, dated October 19, 2026. The published document identifies a [Creative Commons Attribution-ShareAlike 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/). This course adapts its explanations into a teaching sequence, quizzes, original diagrams, and animations.

The contributing community is the [OCP Optical Circuit Switching subproject](https://www.opencompute.org/community/optical-circuit-switching).

Teaching-slide citations link to verified pages in the 46-page published PDF. The final course slide links to the whole paper without a page reference. The page map and source SHA-256 are retained in `references/paper-pages.json` and `course.json`. Course Home also offers the identical bundled PDF for offline reading.

The published PDF and original development manuscript are not committed. During a build, `scripts/build_resources.py` downloads the public PDF into the staged package and verifies its recorded SHA-256. A changed upstream file stops the build for page-map review.

## Evidence treatment

The five-contributor latency example is illustrative, not a measured product. Device transitions, usable-path readiness, and application latency retain distinct boundaries. MixNet's millisecond switching is described as hidden during computation. The course distinguishes production systems, research prototypes, and simulated proposals; the MFU gap is not presented as entirely network-caused or recoverable. The evaluation sequence is a teaching framework, not an OCP certification.

## Editable source and build

`course.json` is the canonical source. Paired narration scripts live under `audio/`; pronunciation substitutions are documented in script comments while display transcripts retain normal spelling. Narration uses ElevenLabs Leo v2, `eleven_multilingual_v2`, at speed 1.18. M1S3 retains its volume repair, and M4S11 retains the `ree-tries` pronunciation cue.

`figures/` contains course-owned media. `animations/` retains deterministic source scenes and exact narration chapter timings. `thumbnail.png` is the 800 × 400 Academy poster; `thumbnail.svg` is its editable source. The official Academy logo is embedded without modification, with its visible artwork aligned to the poster's 40-pixel left margin.

From the repository root:

```bash
./scripts/build-course.sh fast-optical-circuit-switching-for-dynamic-ai-fabrics
```

Provide `ELEVENLABS_API_KEY` for narration generation, or set `EXISTING_AUDIO_DIR` to previously generated course audio when reproducing the reviewed narration. The shared build stages resources, renders modules, validates the package, and produces a strict SCORM ZIP. Generated WAV files, rendered runtime HTML, ZIPs, credentials, and research documents are excluded from source control.

## Navigation and validation

The course retains SCORM 1.2 with separate Course Home and module activities. Course Home has informational module tiles and a direct first-module action, with an instruction to use the LMS syllabus. Direct links cannot switch the SCORM tracking context; target-LMS navigation and tracking must be tested before learner release.

Source QA, glossary media evidence, PDF page citations, local package validation, and browser review are checked in the local authoring project. Repository builds should rerun these checks. OCS is introduced in Module 1 only; the user requested no CDR glossary entry.

The October 22 reference-only rebuild preserved all 45 user-reviewed narration clips. The current audio checker additionally flags a pre-existing spoken-level decline in M4S7 (about 3.9 dB). Package/source validation passes; this automated level flag is recorded for a future listening review rather than changing the approved narration during a citation update.

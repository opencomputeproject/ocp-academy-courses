# OCP Academy - MRC Technical Overview

Multipath Reliable Connection (MRC), an open RDMA transport for AI training fabrics.

This folder contains the editable course source for the SCORM package. It includes the course definition, narration scripts, and lightweight SVG assets, but not generated audio, rendered HTML, or LMS package outputs.

## Modules

| Module | Title | Focus |
|---|---|---|
| 1 | Why MRC | AI training tail latency, RoCE limits, and the role MRC plays in multipath RDMA fabrics. |
| 2 | Inside MRC | Packet spraying, SRv6/uSID source routing, out-of-order receive, SACK/NACK recovery, and congestion response. |
| 3 | Deploying MRC | Multi-plane topologies, production evidence, performance results, API modes, and deployment tradeoffs. |

Each module includes a knowledge check before its final transition or completion slide.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh multipath-reliable-connection-mrc
```

For local QA using previously generated audio:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh multipath-reliable-connection-mrc
```

## Maintained Slides Refresh

The course retains SCORM 1.2 with Course Home and three separately tracked module entries. The home uses informational module tiles, the syllabus navigation instruction, and the maintained first-module start action. The current Slides player supplies the narration controls, per-slide resume, persistent knowledge-check attempts, and module completion behavior.

The approved narration scripts and the existing Module 2 failure-bypass video are retained. This is a rebuild of the approved one-video edition; Modules 1 and 3 retain their static teaching media. Run source QA with those existing media choices recorded explicitly:

```bash
python skills/academy-wizard/scripts/slides_course_qa.py \
  courses/multipath-reliable-connection-mrc/course.json --repo-root . \
  --allow-missing-module-video 1 --allow-missing-module-video 3 --fail-on-flags
python skills/academy-wizard/scripts/check_svg_arrows.py \
  courses/multipath-reliable-connection-mrc/course.json --fail-on-flags
```

Previously inline diagrams are saved as editable SVG assets. Reviewed media text inventories and verified pronunciation aliases support first-use glossary placement. Teaching references open verified one-based PDF pages; the course-complete slide links to the whole specification and companion paper.

The latest audio scan passes all three knowledge-check clips. The unchanged recordings for Module 1 slide 6 and Module 3 slides 7 and 8 produce borderline spoken-level review prompts (2.6-2.9 dB lower than the opening), without sustained-drop, weak-tail, or post-speech-burst flags. Keep those approved clips for the refresh and spot-listen to their endings during learner review.

A second volume check across all 32 WAVs found zero full-scale PCM samples. Sample peaks range from -1.53 to -0.43 dBFS; speech-active RMS levels range from -21.02 to -19.73 dBFS (about 1.3 dB between clips). These are signal measurements, not LUFS, true-peak, or perceptual listening approval. No normalization or new synthesis was applied.

### Review Validation

The October 11, 2026 review build passes package validation, source QA with zero flags, and the SVG arrow check. Browser QA covers all 32 slides at desktop, tablet, and 390px/320px phone sizes: 1,330 course-specific assertions plus 87 enlarged-media/transcript assertions. Maintained regression checks pass 26 quiz-resume, 81 slide-resume, and 43 slide-control assertions. The control regression test now checks the current syllabus handoff instead of expecting the removed blocked button.

Core teaching and quiz content are unchanged, apart from learner-aid placement and resource labels. All 32 WAV files are byte-identical to the approved edition. The existing course mark, catalog poster, and teaching video are retained.

These are isolated local/mock-SCORM checks, not target-LMS acceptance. The Home start action is a direct first-module page link and cannot switch a SCORM 1.2 LMS tracking context. Verify its behavior in the target LMS; later module changes use the syllabus handoff. The user approved ZIP packaging and a source PR on October 11, 2026, with human audio review deferred. The delivery retains SCORM 1.2 and the existing separate module tracking; no live LMS material was replaced or reset.

## Public References

- OCP Multipath Reliable Connection (MRC) Specification Revision 1.0: https://www.opencompute.org/documents/ocp-mrc-1-0-pdf
- Resilient AI Supercomputer Networking using MRC and SRv6: https://cdn.openai.com/pdf/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf
- Supercomputer networking to accelerate large scale AI training: https://openai.com/index/mrc-supercomputer-networking/

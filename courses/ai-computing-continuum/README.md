# AI Computing Continuum

An OCP Academy course on the open infrastructure, distributed inference, and ecosystem collaboration behind the OCP AI Computing Continuum.

This course source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and figure assets in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Editable animation sources are under `animations/`; their encoded course videos and posters are under `figures/`. Generated narration and SCORM runtime files are not checked in.

## Modules

| Module | Title | Narrated time | Summary |
|---|---|---:|---|
| 1 | Why the Continuum Exists | 7:55 | Why inference is expanding beyond centralized hyperscale data centers and why useful remote compute requires both capacity and connectivity. |
| 2 | Open Infrastructure Across the Continuum | 9:04 | AICC project domains, differing site constraints, and the distributed anatomy of inference, including within-site specialization of prefill, decode, and KV-cache functions. |
| 3 | Three Ways to Compute Across Distance | 7:34 | Scale-Across, Sync-Across, and Reach-Across, with the workload and service objectives that distinguish them. |
| 4 | From Architecture to Ecosystem Action | 8:09 | Complementary OCP and IOWN roles, a research-park use case, examples of related ecosystem work, and ways to participate. |

The total narrated runtime is approximately 33 minutes. Each module includes a two-question knowledge check before the final wrap-up slide: one single-choice question followed by one multi-select question.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ai-computing-continuum
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh ai-computing-continuum
```

## Public references

The original research files are not included in this repository. Public learner and source references used by the course include:

- OCP AICC project: https://www.opencompute.org/community/aicc
- 2026 OCP EMEA Summit AICC track: https://www.opencompute.org/events/past-events/2026-ocp-emea-summit#the-ai-computing-continuum-extending-ai-from-data-center-to-the-user
- AICC Core talk: https://www.youtube.com/watch?v=82SWBzASQjo
- AICC Introduction talk: https://www.youtube.com/watch?v=b5WS5fg2Ylg
- IOWN Global Forum, “AI Computing Continuum: Why It Matters and What We Discussed at OCP EMEA 2026”: https://iowngf.org/ai-computing-continuum-why-it-matters-and-what-we-discussed-at-ocp-emea-2026/
- IOWN Global Forum and OCP collaboration announcement: https://iowngf.org/iown-global-forum-and-open-compute-project-join-forces-to-deliver-on-the-next-wave-of-ai/
- AICC mailing list: https://ocp-all.groups.io/g/ocp-aicc

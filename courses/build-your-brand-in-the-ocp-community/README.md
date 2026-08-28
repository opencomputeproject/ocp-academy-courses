# How to Build Your Brand in the OCP Community

This two-module OCP Academy course is based on Dirk Van Slyke's April 2025 presentation and updated for current OCP membership terminology and durable Community channels. It explains how organizations and individuals earn trust through useful participation, then extend credible work through the OCP Marketplace, events, communications, and OCP Academy.

## Modules

| Module | Narrated duration | Description |
|---|---:|---|
| 1. Earn Trust Before You Amplify | 10.1 minutes | Build credibility by listening first, participating consistently, contributing useful work, and collaborating openly. Membership is a signal, not an entry ticket; the credibility flywheel turns service into trust. |
| 2. Turn Useful Work into Reach | 11.4 minutes | Choose the right channel for work that already helps the Community: the Marketplace and Solution Provider program, events, communications, and OCP Academy. Apply the editorial filter and turn one contribution into several useful touchpoints. |

The total narrated runtime is approximately 21.5 minutes. Allow 25–30 minutes for the complete learner experience, including reflection and knowledge checks.

## Editable source

- Change slides, interactions, references, and course metadata in `course.json`.
- Change narration in `audio/module1/` and `audio/module2/`.
- Course-owned visual media, including two silent teaching animations and their poster images, lives in `figures/`.
- The animation source is `animations/build_teaching_animations.py`.
- The course mark is `build_your_brand_mark.svg`; the LMS poster is `thumbnail.png` at 800 × 400 pixels.

Generated narration WAVs, rendered HTML, SCORM packages, and original research files are intentionally not checked in.

## Build

Generate narration and the LMS-ready package:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh build-your-brand-in-the-ocp-community
```

For local QA with previously generated narration, point `EXISTING_AUDIO_DIR` to an `audio/` directory with matching `module1/` and `module2/` subfolders:

```bash
EXISTING_AUDIO_DIR=/path/to/audio \
  ./scripts/build-course.sh build-your-brand-in-the-ocp-community
```

## Public resources

- [Dirk Van Slyke's presentation](https://www.youtube.com/watch?v=k6pL1WJLXAI)
- [OCP upcoming events](https://www.opencompute.org/events/upcoming-events) and [past events](https://www.opencompute.org/events/past-events)
- [OCP Podcast](https://www.opencompute.org/ocp-podcast)
- [OCP Educational Webinar Program](https://www.opencompute.org/summit/ocp-educational-webinar-program)
- [OCP News and Blog](https://www.opencompute.org/blog)
- [Subscribe to the OCP Newsletter](https://mailchi.mp/opencompute/subscribe-to-ocp)
- [OCP Academy](https://academy.opencompute.org/learn)
- [OCP Orientation catalog](https://academy.opencompute.org/learn/public/catalog/view/5)
- [Introduction to the OCP Solution Provider Program](https://academy.opencompute.org/learn/courses/14/introduction-to-the-ocp-solution-provider-program)

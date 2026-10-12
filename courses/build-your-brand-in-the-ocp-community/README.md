# How to Build Your Brand in the OCP Community

This two-module OCP Academy course combines Dirk Van Slyke's original April 2025 recording with his updated 2026 slides and current OCP program rules. There is no replacement recording: the original video is retained and explicitly labelled. The course explains how organizations and individuals earn trust through useful participation, then extend credible work through the OCP Marketplace, events, communications, and OCP Academy.

## Modules

| Module | Narrated duration | Description |
|---|---:|---|
| 1. Earn Trust Before You Amplify | 10.7 minutes | Build credibility by listening first, participating consistently, contributing useful work, and collaborating openly. Distinguish open participation from tier-dependent program benefits and formal eligibility; the credibility flywheel turns service into trust. |
| 2. Turn Useful Work into Reach | 12.9 minutes | Choose the right channel for useful Community work: the Marketplace and Solution Provider program, Summits, Tech Days, FTS, communications, webinars, and OCP Academy. Understand hosting/exhibit logistics and webinar-specific reporting, apply the editorial filter, and turn one contribution into useful touchpoints. |

The total narrated runtime is approximately 23.6 minutes. Allow 26–30 minutes for the complete learner experience, including reflection and knowledge checks.

## LMS navigation

This remains a SCORM 1.2 multi-SCO course with separate Course Home, Module 1, and Module 2 syllabus entries. The home uses informational module tiles, directs learners to the LMS Syllabus for either module, and includes a dedicated **Start with MODULE 1** control. It does not infer cross-module completion from the Course Home session.

The Start, next-module, and course-home controls retain this course's approved direct-page compatibility behavior. A relative page link is not a standard SCORM request to launch another SCO, so actual module handoff, separate completion, and resume must be verified in the target LMS before replacing a live course. This refresh does not change the SCORM version or syllabus organization.

Unfinished modules resume their own saved slide. Completed modules reopen their final slide even after visiting earlier content or retrying a quiz. Submitted quiz choices and feedback are remembered; Retry clears only that question's attempt. Editorial `?review=1` navigation stays untracked through Start, Next Module, and Home links.

## October 2026 player refresh

Rebuild with the repository's maintained AcademyWizard templates, retaining the approved course source, Leo v2 narration at speed 1.18, and all existing media. The current shared runtime supplies quiz memory, completion-aware slide resume, transcript/narration controls, and legacy loop-video timing. Mobile teaching content now clears the fixed module badge; glossary definitions clear the taller mobile control bar. This course keeps its silent short-loop animations and does not opt into narration-synchronized single-pass video.

The 2026 content refresh adds verified, page-specific links to Dirk's published PDF on teaching slides. The user explicitly requested whole-document links on the course opening and closing slides; the opening reference records this narrow exception with `whole_document: true`. The original video remains labelled April 2025, and the updated deck is never described as a new recording.

The refresh clarifies membership versus Solution Provider enrollment, tier-dependent benefits, the historical 1.68%/0.6% click-through comparison, hosting workshops/plugfests, turnkey Summit exhibit logistics, FTS's research audience, webinar-specific attendee reporting, and social/targeted outreach. Allie Bodnar is added as a second contact. Current canonical resource destinations replace redirects. The approved broad Marketplace scale wording is retained; the deck's ~600 listing snapshot is not misrepresented as evidence for the course's around-1,000 approximation. No venue calendar, website screenshots, fee amounts, or lead guarantees are frozen into learner content.

Only M1S2, M1S7, M2S3, M2S4, M2S5, and M2S11 need regenerated narration. Reuse the other 16 clips and all approved visual media with the recorded voice, model, and speed. The updated audio is checked without audible playback; perceptual listening approval remains with the reviewer.

M1S7 uses three two-paragraph groups joined with 180ms pauses after a full-request synthesis developed a sustained closing fade. The groups use the same voice/model/settings, preserve every sentence, and are joined as mono 16-bit PCM at 22050 Hz without gain changes. Only 0.224 seconds of surplus quiet tail was removed after the last active speech window, with a 70ms guard retained. The full clip passes the current speech-level and tail checks; its recipe is recorded in `content_revision.narration_chunking`. Reuse the verified WAV when reproducing the reviewed pages. Its media-first layout keeps the membership artwork and the added reference pills clear of the fixed controls without changing the image asset.

## Editable source

- Change slides, interactions, references, and course metadata in `course.json`.
- Change narration in `audio/module1/` and `audio/module2/`.
- Course-owned visual media, including two silent teaching animations and their poster images, lives in `figures/`.
- The animation source is `animations/build_teaching_animations.py`.
- The course mark is `build_your_brand_mark.svg`; the LMS poster is `thumbnail.png` at 800 × 400 pixels.

Generated narration WAVs, rendered HTML, SCORM packages, and original research files are intentionally not checked in.
The source records the approved Leo v2 narration settings and playback pace, display transcripts, and reviewed text inventories for relevant media; rebuilding the player does not require new narration.

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

- [Dirk Van Slyke's original April 2025 recording](https://www.youtube.com/watch?v=k6pL1WJLXAI)
- [Dirk Van Slyke's updated 2026 slides (PDF)](https://www.opencompute.org/documents/how-to-build-your-brand-in-ocp/)
- [OCP upcoming events](https://www.opencompute.org/events/) and [past events](https://www.opencompute.org/events/past-events/)
- [OCP Future Technologies Symposium](https://www.opencompute.org/events/future-tech-symposium/ocp-future-technologies-symposium/)
- [OCP Podcast](https://www.opencompute.org/podcast/)
- [OCP Educational Webinar Program](https://www.opencompute.org/events/ocp-educational-webinar/ocp-educational-webinar-program/)
- [OCP News and guest blogs](https://www.opencompute.org/news/)
- [Subscribe to the OCP Newsletter](https://mailchi.mp/opencompute/subscribe-to-ocp)
- [OCP Academy](https://academy.opencompute.org/learn)
- [OCP Orientation catalog](https://academy.opencompute.org/learn/public/catalog/view/5)
- [Introduction to the OCP Solution Provider Program](https://academy.opencompute.org/learn/courses/14/introduction-to-the-ocp-solution-provider-program)

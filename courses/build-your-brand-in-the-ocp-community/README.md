# How to Build Your Brand in the OCP Community

This two-module OCP Academy course combines Dirk Van Slyke's original April 2025 recording with his updated 2026 slides and current OCP program rules. There is no replacement recording: the original video is retained and explicitly labelled. The course explains how organizations and individuals earn trust through useful participation, then extend credible work through the OCP Marketplace, events, communications, and OCP Academy.

## Modules

| Module | Narrated duration | Description |
|---|---:|---|
| 1. Earn Trust Before You Amplify | 10.7 minutes | Build credibility by listening first, participating consistently, contributing useful work, and collaborating openly. Distinguish open participation from tier-dependent program benefits and formal eligibility; the credibility flywheel turns service into trust. |
| 2. Turn Useful Work into Reach | 12.6 minutes | Choose the right channel for useful Community work: the Marketplace and Solution Provider program, Summits, Tech Days, FTS, communications, webinars, and OCP Academy. Understand hosting/exhibit logistics and webinar-specific reporting, apply the editorial filter, and turn one contribution into useful touchpoints. |

The table above records the November full-v4 performance: 23.4 minutes of narration in total. The approved learner estimate remains 26–30 minutes, including reflection and knowledge checks.

## November 2026 audio and player refresh

The user explicitly requested the current AcademyWizard audio model and MP3 compression. All 22 slides are re-recorded with full `eleven_v4`, retaining the approved Leo voice ID `bbGtsRRKUfYO634UxSjz` and a pitch-preserving `1.18` tempo multiplier. Native v4 is generated without an API speed field; the learner speed dial remains `1.0` and preserves saved preferences. This does not claim to reproduce the old model's exact cadence or runtime.

Delivery uses 44.1 kHz, 96 kbps CBR mono MP3. The provider MP3, decoded native WAV, paced authoring WAV, and per-clip pacing receipts are retained outside the runtime package. The provider recording is already compressed; its decoded WAV is not a lossless provider original. The learner MP3 is re-encoded after pacing and fully decoded to verify duration parity. No WAV is included in the runtime manifest.

The approved scripts, quiz gates, 2026 slide-page links, original April 2025 recording references, course mark, poster, and teaching media are unchanged. Both teaching videos remain independent silent loops; they do not require narration-length matching and are tested against MP3 seeking without conversion to single-pass video. Current shared templates supply media/caption spacing, glossary placement, navigation, bookmarks, transcript and narration controls, and quiz memory. Newer repository fixes are retained instead of replacing the shared toolchain with an older installed copy.

The reviewed source snapshot is based on repository main `7d7a2597adc726b34f94d8b6e7411acb7c80f769`; publication uses a clean worktree so the original checkout's unrelated missing files are untouched. Review uses the actual generated `index.html`, `module1.html`, and `module2.html`, not a separate review site. Automated audio checks and browser playback are muted and do not establish perceptual listening quality. The user approved the local copy for ZIP creation and repository publication on November 3, 2026. Live LMS acceptance remains a separate test.

Formal LMS copy is maintained separately in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json), generated from `course.json.lms_catalog`. The 26-minute nominal learner estimate (12 + 14 minutes) is not replaced with measured narration runtime.

The reviewed MP3 assets total 16,840,847 bytes versus 61,824,910 bytes for the paced WAVs (72.76% smaller). All 22 MP3s fully decode, with a maximum timing difference of 0.862 ms. Provider/native/paced/script hashes and the full-v4 receipts match. All 22 clips pass speech-level and tail QA. The complete review folder contains 39 declared runtime files and no WAVs; a clean source reconstruction is byte-identical.

Validation passed: 157 shared Python regressions, 300 course-specific browser assertions, 310 real-MP3/control/media-layout assertions, 59 resume assertions, 26 quiz-memory assertions, 50 shared-control assertions, and 64 real-media loop-video assertions across desktop and phone checks. All playback is muted. Source QA validates 12 PDF references and 5 glossary placements; the 4 static SVG artboards need no trim, and arrow geometry passes for all 5 SVG assets. The approved strict ZIP contains only its 39 declared runtime files, with separate LMS catalog JSON/Markdown/HTML sidecars. Its SHA-256 is `25d0838db7dfc16a926b5ba648e8a22f6abc7feb1f1533fff203dcbef767627f`.

## LMS navigation

This remains a SCORM 1.2 multi-SCO course with separate Course Home, Module 1, and Module 2 syllabus entries. The home uses informational module tiles, directs learners to the LMS Syllabus for either module, and includes a dedicated **Start with MODULE 1** control. It does not infer cross-module completion from the Course Home session.

The Start, next-module, and course-home controls retain this course's approved direct-page compatibility behavior. A relative page link is not a standard SCORM request to launch another SCO, so actual module handoff, separate completion, and resume must be verified in the target LMS before replacing a live course. This refresh does not change the SCORM version or syllabus organization.

Unfinished modules resume their own saved slide. Completed modules reopen their final slide even after visiting earlier content or retrying a quiz. Submitted quiz choices and feedback are remembered; Retry clears only that question's attempt. Editorial `?review=1` navigation stays untracked through Start, Next Module, and Home links.

## October 2026 player refresh

The October refresh used the repository's maintained AcademyWizard templates, the approved Leo voice at speed 1.18, and all existing media. The shared runtime supplies quiz memory, completion-aware slide resume, transcript/narration controls, and legacy loop-video timing. Mobile teaching content clears the fixed module badge; glossary definitions clear the taller mobile control bar. This course keeps its silent short-loop animations and does not opt into narration-synchronized single-pass video. The November full-v4 performance supersedes the October audio.

The 2026 content refresh adds verified, page-specific links to Dirk's published PDF on teaching slides. The user explicitly requested whole-document links on the course opening and closing slides; the opening reference records this narrow exception with `whole_document: true`. The original video remains labelled April 2025, and the updated deck is never described as a new recording.

The refresh clarifies membership versus Solution Provider enrollment, tier-dependent benefits, the historical 1.68%/0.6% click-through comparison, hosting workshops/plugfests, turnkey Summit exhibit logistics, FTS's research audience, webinar-specific attendee reporting, and social/targeted outreach. Allie Bodnar is added as a second contact. Current canonical resource destinations replace redirects. The approved broad Marketplace scale wording is retained; the deck's ~600 listing snapshot is not misrepresented as evidence for the course's around-1,000 approximation. No venue calendar, website screenshots, fee amounts, or lead guarantees are frozen into learner content.

The October content refresh regenerated only M1S2, M1S7, M2S3, M2S4, M2S5, and M2S11 and reused the other 16 clips. The November model upgrade replaces all 22 performances while preserving those approved scripts and all visual media.

The October M1S7 performance used three two-paragraph groups joined with 180ms pauses after a full-request synthesis developed a sustained closing fade. That historical repair and its 0.224-second post-speech tail trim remain documented in `content_revision.narration_chunking`; they do not describe the new recording. November M1S7 is a complete single-request full-v4 performance and passes current speech-level and tail QA without that repair. Reuse the verified full-v4 WAV/MP3 cache when reproducing this release. The media-first layout keeps the membership artwork and reference pills clear of the fixed controls without changing the image asset.

## Editable source

- Change slides, interactions, references, and course metadata in `course.json`.
- Change narration in `audio/module1/` and `audio/module2/`.
- Course-owned visual media, including two silent teaching animations and their poster images, lives in `figures/`.
- The animation source is `animations/build_teaching_animations.py`.
- The course mark is `build_your_brand_mark.svg`; the LMS poster is `thumbnail.png` at 800 × 400 pixels.

Generated narration WAVs/MP3s, rendered HTML, SCORM packages, and original research files are intentionally not checked in.
The source records the approved Leo voice ID, full-v4 model, MP3 delivery settings, playback pace, display transcripts, and reviewed text inventories for relevant media; rebuilding the player or compressing approved masters does not require new narration.

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

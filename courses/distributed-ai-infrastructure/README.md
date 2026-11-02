# Distributed AI Infrastructure

A five-module OCP Academy Slides course connecting workload coordination, distributed state, timing, geographic placement and bounded recovery to infrastructure decisions. [Open the Academy course](https://academy.opencompute.org/learn/courses/94/ai-infra/).

The course contains **57 slides**, **49 narration clips**, **eight original recordings**, **five narration-synchronized teaching animations** and **ten knowledge-check questions**. Estimated learner time is **80 minutes**, including media, reading, reflection and questions. Narration alone runs 36.36 minutes. Optional external courses and Summit viewing are excluded from the learner-time estimate. Formal LMS fields are in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json); `thumbnail.png` is the approved 800×400 poster.

The SCORM **1.2** package contains **six tracked syllabus entries: Course Home first, then the five content-module SCOs**. Course Home retains informational module tiles and the maintained Start Module 1 control. Keep the LMS syllabus available for module selection and verify launch, resume and completion in the target LMS. Direct page links do not switch the LMS tracking context.

## Edit and build

`course.json` is canonical. Narration scripts are under `audio/moduleN/`; visible transcripts retain conventional spelling while spoken scripts contain pronunciation substitutions. SVG diagrams are editable in `figures/`. Original recordings, posters and VTT captions are under `resources/`. Five finite animation sources, timing configurations and their shared JavaScript are in `animations/`.

From the repository root, reuse the matching delivered narration kept outside Git:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/delivered-course/audio bash scripts/build-course.sh distributed-ai-infrastructure
python3 courses/distributed-ai-infrastructure/scripts/verify_course.py build/distributed-ai-infrastructure
```

The build stages resources, embeds caption cues, renders Home and all five modules, checks narration levels and the package, and produces the strict LMS ZIP plus separate LMS catalog exports. To synthesize changed narration, use the maintained `gen_audio.py` with an ElevenLabs credential supplied privately through the environment. Preserve full `eleven_v4`, Leo (`bbGtsRRKUfYO634UxSjz`), pitch-preserving tempo 1.18 and the learner dial at 1.0. Generated WAVs and native synthesis masters are not in Git.

The supplied VTT files are the editable source for video captions. The Slides renderer loads them into per-track embedded cues so overlays work when opening files locally and when served through HTTP/LMS. All eight English tracks retain their original bytes and timing. See [QA](QA.md) for caption playback checks.

## Teaching video maintenance

All five new videos use `sync_to_narration: true`, `autoplay: false`, `loop: false` and `muted: true`: they play once with narration and hold the final picture, including in the enlarged view. The eight original recordings retain their own audio and use the shared black player.

After changing animation narration, regenerate its audio and refresh the ASR timing evidence under `authoring/alignment` before retiming. The retiming helper rejects an alignment file whose WAV hash is stale:

```sh
python3 courses/distributed-ai-infrastructure/scripts/retime_animation_sources.py --runtime build/distributed-ai-infrastructure --require-audio
FFMPEG_BIN=/path/to/full/ffmpeg python3 courses/distributed-ai-infrastructure/scripts/render_animations.py
```

The recording helper uses the maintained lossless-PNG recorder at 1920×1080 and 30 fps, followed by the verified lossless matrix-metadata correction. Paragraph openings and selected quantities use ASR timestamps; remaining within-paragraph cues are proportional estimates, not forced alignment. Review changed cues against speech and inspect the resulting encoded video before updating reviewed hashes. If no timing change is needed, reuse the committed MP4s and posters.

The original Rise ZIPs and recovered research workspace remain outside this repository. Their resource hashes, lesson mappings, source topics and reference provenance are retained in [the source audit](authoring/source-audit.json). The optional Lamport paper link was added for the Slides explanation of causality. See [attribution](NOTICE.md) and [reviewed media integrity](authoring/media-integrity.json).

This course is a standalone series. It links selectively to Open Systems for AI, Open Cluster Designs for AI, AICC and the 2026 Global Summit AI Clusters track; it is not part of those other courses.

The original five Rise packages were SCORM 2004 3rd Edition. The requested delivery combines them into one SCORM 1.2 item with Course Home plus five content-module SCOs. Test a separate LMS upload and retain needed reports before retiring prior materials; existing bookmarks, attempts and completion history may not transfer.

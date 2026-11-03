# OCP Community Orientation

Five independent narrated Slides courses for a nontechnical audience. Each replaces its previous Scrolling edition at the same course path. Build and upload each course separately; they are not modules inside a shared package.

| Course | Content modules | Estimated learner time |
|---|---:|---:|
| [Introduction to the OCP Solution Provider Program](introduction-to-the-ocp-solution-provider-program/README.md) | 1 | 7 min |
| [OCP Contribution Process](ocp-contribution-process/README.md) | 1 | 8 min |
| [OCP Ready™ Data Center Recognition Program](ocp-ready-data-center-recognition-program/README.md) | 1 | 6 min |
| [OCP's Volunteer Leadership Guide](ocp-volunteer-leadership-guide/README.md) | 1 | 10 min |
| [Understanding and Procuring Open Technologies and Products](understanding-and-procuring-open-technologies-and-products/README.md) | 1 | 7 min |

The English set contains 84 slides, 81 narrated sections, ten narration-synchronized teaching videos, 35 screenshot placements and six retained original-video placements. Contribution Process adds caption-timed narration to its three originally silent demonstrations. The other original recordings retain their own soundtracks and shared player.

Each course uses SCORM 1.2 with one tracked course activity, including Course Home and one teaching module. Course marks and 800 × 400 posters are approved; Ready and Solution Provider posters retain the supplied official program logos. The user confirmed synchronization to OCP Academy on November 3, 2026.

## Editable sources

Each course owns its `course.json`, current narration scripts, figures, animation sources, original media, captions, course mark, `thumbnail.png`, `poster.html`, poster assets and separate LMS catalog exports. Generated narration, rendered runtime pages and ZIPs remain outside Git under repository policy.

Use `./scripts/build-course.sh ocp-orientation/<course-folder>` from the repository root. `EXISTING_AUDIO_DIR` reuses approved narration without paid regeneration. The Contribution Process cue generator preserves its authored caption windows and fails when a new phrase does not fit.

## Translations

The 15 superseded Scrolling locale editions have been retired from the current catalog and remain recoverable in Git history. Create replacement Slides locales from the current approved English sources. The maintained target choices are Korean, Japanese, Simplified Chinese, Traditional Chinese, Vietnamese, Brazilian Portuguese and Latin American Spanish: 35 independent course editions.

[Live voice compatibility record](../../docs/orientation-v4-language-compatibility.json) verifies every selected language and professional voice against full `eleven_v4`. Locale scaffolding preserves MP3 delivery, pacing, media and narration hooks while resetting script, cue-plan and LMS-copy approval. Use native-language editorial review before generating new speech.

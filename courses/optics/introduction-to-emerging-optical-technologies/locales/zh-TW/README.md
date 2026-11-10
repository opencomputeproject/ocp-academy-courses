# 新興光學技術導論

Editable zh-TW edition of introduction-to-emerging-optical-technologies. The canonical English course is `../../course.json`.

## LMS Catalog

The localized formal title, short description, overview and module descriptions are in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json). They are separate from these maintenance notes.

## Course Structure

Estimated learner time: **60 minutes**. This includes narration, diagrams, checks and review; it is not the narration runtime.

| Module | Title | Estimated Learner Time |
|---|---|---:|
| 1 | AI 基礎設施為何正在改變光學技術 | 13 min |
| 2 | 功耗、散熱與可維護性的轉變 | 17 min |
| 3 | 光纖基礎設施的密度與可測試性 | 15 min |
| 4 | 延遲、量子計算與技術採用前景 | 15 min |

SCORM 1.2, multi-SCO: Course Home first, followed by four independently tracked modules. The existing syllabus and content identifiers are preserved.

## Editing And Rebuilding

Edit `course.json` for learner text, interactions, glossary and resource links. Narration scripts remain in `audio/moduleN/*.txt`; editable teaching animations are in `animations/`. The text-free expanded-beam comparison video is shared unchanged with English.

Delivery narration is 96 kbps CBR mono MP3 at 44.1 kHz, approved for this rebuild. Approved recordings are reused where the script and voice match; WAV authoring masters are retained outside Git and outside the LMS package. Revised narration uses ElevenLabs `eleven_v4` with the maintained pitch-preserving pacing. Per-slide `audio.generation_provenance` distinguishes reused legacy recordings from new recordings; unknown legacy model IDs remain unknown.

From the repository root, use `./scripts/build-course.sh optics/introduction-to-emerging-optical-technologies/locales/zh-TW` with the retained narration available through the maintained build workflow. Do not commit narration, generated runtime pages, package ZIPs, API credentials or temporary review artifacts.

Use the shared English LMS poster; no translated poster variant is required. Before release, validate sources, first-use glossary evidence, complete localized media, playback, quiz resume, five-entry syllabus and strict manifest packaging.

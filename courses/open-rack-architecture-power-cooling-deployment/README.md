# Open Rack: Architecture, Power, Cooling and Deployment

One narrated, seven-module **Slides** course for OCP Academy, maintained in English and seven additional languages. Each edition retains 112 slides, 100 narration scripts, 16 narration-synchronized teaching videos, 20 static figures, 12 embedded expert recordings, and 35 glossary entries. Estimated learner time is **145 minutes**, including the recordings and knowledge checks; linked external study is additional.

![Open Rack course poster](thumbnail.png)

## Replacement of the scrolling series

This course replaces the seven independent Scrolling courses formerly under `courses/open-rack-v3/`. Those English course folders and their 49 translated editions are retired, not retained as parallel active courses. The canonical English Slides source and the seven new locale branches below represent the revised curriculum; the retired translations do not. Earlier source remains recoverable from Git history. See [replacement provenance](provenance/replacement.json) and [translation issue #124](https://github.com/opencomputeproject/ocp-academy-courses/issues/124).

This consolidates seven separately uploaded courses into one SCORM 1.2 package with separately tracked content modules. Do not assume old bookmarks, attempts or completions transfer. Export needed LMS reports and test a separate upload before retiring prior LMS material. Repository replacement does not delete or modify live LMS content.

The approved LMS syllabus has **eight entries: Course Home first, then Modules 1–7**. Course Home completes on launch; content-module completion and quiz gates remain independent. This Home choice was explicitly confirmed on 2 November 2026.

## Course modules

| Module | Topic | Learner time |
|---:|---|---:|
| 1 | Open Rack Architecture and the Open Ecosystem | 18 min |
| 2 | ORv3: Mechanical, Power and Cooling Interfaces | 25 min |
| 3 | Selecting, Integrating and Validating an ORv3 Deployment | 17 min |
| 4 | High-Power Racks: Capacity, Resilience and Control | 24 min |
| 5 | Scaling Power: Sidecars, Higher Voltage and Workload Dynamics | 19 min |
| 6 | Open Rack Wide: Frame, Payload and Facility Integration | 20 min |
| 7 | Liquid Cooling, Serviceability and the Integrated Design Review | 22 min |

Formal LMS title, short description and long description are maintained separately in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json), generated from `course.json.lms_catalog`.

## Language editions

The course root remains the canonical English source. Seven additional Slides editions are maintained as independently editable, self-contained branches:

| Language | Locale source |
|---|---|
| Chinese (Simplified) | [`zh-CN`](locales/zh-CN/) |
| Chinese (Traditional) | [`zh-TW`](locales/zh-TW/) |
| Japanese | [`ja-JP`](locales/ja-JP/) |
| Korean | [`ko-KR`](locales/ko-KR/) |
| Portuguese (Brazil) | [`pt-BR`](locales/pt-BR/) |
| Spanish (Latin America) | [`es-419`](locales/es-419/) |
| Vietnamese | [`vi-VN`](locales/vi-VN/) |

Each locale owns its translated `course.json`, 100 narration scripts, learner UI, quizzes and feedback, glossary, editable teaching-media labels, captions, and LMS catalog exports. IDs, answer logic, engineering facts, authoritative URLs, 145-minute learner time, and the eight-SCO SCORM 1.2 organization remain aligned with English. The visible course title stays localized without a language suffix; the manifest adds the English language name to identify the edition in the LMS.

Each translated edition uses its own native-language narration and dubbed soundtracks for the 12 original recordings, with editable native-language transcripts and measured caption tracks. The recordings retain their original encoded visual streams and English labels; localized notices disclose that distinction. English labels inside source engineering drawings also remain where the original plate is preserved, with localized caption and alt-text notices. A dubbed soundtrack is not a translated drawing or a new expert recording.

All seven editions have passed their source, audio, media, desktop/phone browser and strict-package checks. The [language-release receipt](provenance/localization-validation-2026-11-10.json) records package checksums and per-edition results. Native human editorial/listening review and target-LMS acceptance remain pending; no live LMS content was changed. Discretionary Home-title word breaks affect presentation only, not formal course or LMS titles.

## Catalog poster

`thumbnail.png` is the single shared English 800×400 Academy catalog poster for all editions, matching the SST/AICC navy-and-green treatment and using the approved Open Structure mark. Do not create or duplicate locale-specific catalog posters. The editable source is [poster.json](poster.json); it reuses the repository's authoritative Academy logo and bundled Lato font rather than rasterized rack artwork. Localized teaching-video posters are separate course media, not catalog posters.

With Playwright available, regenerate it from the repository root:

```bash
node courses/open-rack-architecture-power-cooling-deployment/poster/render.mjs
```

The renderer checks text bounds and local asset loading, writes the course thumbnail, and saves 400×200 and 240×120 inspection previews under the ignored `build/poster-qa/` directory. The catalog poster is delivered separately from the SCORM runtime; replacing it does not change the existing ZIP.

## Editable source and rebuilding

`course.json` is authoritative. `content/` contains the English manuscripts, and `audio/module*/` contains the scripts and editable narration VTTs. All editions use full **Eleven v4 (`eleven_v4`)**, with Leo for English and the approved locale-specific voice recorded in each translated source. Native generation is followed by pitch-preserving **1.18× pacing**; the learner speed dial remains **1.0×**. Learner narration delivery is **44.1 kHz, 96 kbps CBR mono MP3**. `audio.wav_file` retains the paced authoring-master path; `audio.delivery_file` selects MP3 playback and packaging.

Approved narration WAV/MP3 files, provider recordings, runtime HTML, manifests and SCORM ZIPs are kept outside Git. Retain the native and paced masters and receipts in authoring storage; a WAV decoded from provider MP3 is not a lossless provider recording. Course-owned localized recording MP4s, editable VTTs, diagrams and animation sources remain course assets. Never reuse English narration as a locale's audio, and do not regenerate approved audio solely to refresh player code.

From the repository root, use the normal build command when packaging is authorized. Supply approved paced WAV masters to avoid new synthesis; fresh narration requires separately approved ElevenLabs access and settings:

```bash
FFMPEG_BIN=/path/to/ffmpeg EXISTING_AUDIO_DIR=/path/to/approved/audio ./scripts/build-course.sh open-rack-architecture-power-cooling-deployment
```

Build a locale independently using the same wrapper and that locale's approved audio:

```bash
FFMPEG_BIN=/path/to/ffmpeg EXISTING_AUDIO_DIR=/path/to/approved/ja-JP/audio ./scripts/build-course.sh open-rack-architecture-power-cooling-deployment/locales/ja-JP
```

The wrapper stages source assets, creates or validates MP3 delivery copies from paced masters, renders the course, and packages only manifest-listed runtime assets with matching LMS JSON/Markdown/HTML sidecars. Encode receipts stay beside the build, not in its SCORM runtime. The wrapper uses the repository's skill by default; set `ACADEMY_WIZARD_SKILL_DIR` explicitly when reproducing a separately validated maintained-player revision. No API key is stored here.

For a byte-preserving runtime-only refresh, stage the approved MP3s and media unchanged and render with the validated maintained player; do not regenerate narration or run delivery encoding unnecessarily. The English language-edition refresh followed this path: existing full-v4 English audio and all approved media stayed byte-identical while the module player was refreshed to correct stale quiz-feedback state. It was not a new English narration job.

Open generated `index.html` and `module1.html` through `module7.html` directly from disk for review; no server is needed. `?review=1` isolates editorial playback from saved progress. Original recordings use their own players, sound and caption overlays; slide narration is disabled on those slides. In translated editions that sound is the locale's dubbed soundtrack. Do not run an additional slide narration track over a recording.

## Media and source evidence

`figures/` contains editable SVG figures, the reviewed finite videos and their posters. `animations/` retains self-contained editable HTML timelines, cue maps and source plates. Videos follow the narration clock, play once and hold their completed picture in embedded and enlarged views. Regenerating narration can change semantic timing: review the cue maps, retime and re-encode affected videos with the maintained `record_css_animation.mjs`, then review geometry, legibility and final-frame hold before refreshing media inventories.

The canonical `resources/` retains the 12 English original recordings, posters and editable captions. Their source hashes and prior repository revision are recorded in [original-recordings.json](provenance/original-recordings.json). Four supplied English VTTs are byte-preserved; eight missing English tracks were locally transcribed and reviewed. Locale copies carry their native dubbing and measured VTTs while preserving the source video stream. Recorded earlier implementations and roadmaps are distinguished from current specification requirements in slide context.

Each locale's source-safe reproduction plan is in `locales/<tag>/localization/dubbing.json`. The seven plans cover 84 recordings, 927 clean native utterances and 2,903 measured caption cues. They record exact synthesized text, source windows, measured placements, full-v4 voice/model/pacing settings, hashes, and balanced Academy background music with ducking and fades. References are relative; credentials, absolute machine paths and native audio masters are omitted. Plans preserve complete words and glossary/brand phrases rather than synthesizing approximately split caption fragments. Eleven legacy whole-second Portuguese source-duration estimates are distinguished from freshly measured source-file durations; one narrow scene-reviewed scheduling exception preserves the approved pacing and exact video stream. These plans are authoring metadata, not a listening approval, and do not enter the SCORM manifest or ZIP. Full transcripts and VTT tracks remain editable in the locale source.

Each locale includes licensed offline fonts under `fonts/`, with `locale.css`, WOFF2 subsets, license files and any needed Unicode-range supplement registered in `resource_assets`. Native-font fitting and semantic line groups apply to teaching labels; source drawings retain their engineering geometry. Preserve the font licenses and check glyph coverage after text changes. Caption-only glyph additions belong in the global stylesheet/supplement, not a rewrite of animation or SVG font data.

PDF source evidence remains in `source_refs`. All opencompute.org page-specific links are preserved. Learner-facing Summit references use official OCP YouTube recordings rather than Dropbox page downloads; full recordings are used when concept timestamps cannot be verified. See [the recording mapping](provenance/summit-video-references.json). The source includes related Academy courses, including Open Data Center for AI and Grid Disturbance Performance, at the relevant teaching points.

## Validation and LMS testing

Validate each edition independently. Source QA covers glossary first use, media inventories, references and arrow geometry. Check every generated narration clip, delivery decode and master hash, then review synchronized video playback, seeking, speed, enlargement, final hold and replay at desktop and phone sizes. Original-video captions, native dub timing, quiz feedback/retry/persistence, bookmarks, local font loading and scroll-safe layout need their own checks. Automated signal or browser passes do not constitute native-speaker or human listening approval. The approved Open Structure mark is `open-rack-mark.svg`.

Local checks do not establish target-LMS tracking. Verify syllabus launches, bookmarks, quiz attempts, module completion and direct Start/Next handoffs in the LMS. SCORM version or tracking changes require a separate migration decision; do not delete old LMS material as part of a repository build.

The **English 2 November 2026** delivery passed package validation and strict ZIP integrity checks: 200 runtime files, 100 MP3 clips, and the eight ordered syllabus entries. Its release-page checks included all 12 recordings and 92 visible-caption checks at desktop/phone sizes, Home/resume behavior, and representative synchronized-video checks. See [the historical validation receipt and delivery checksum](provenance/validation.json); it does not certify later translated builds. The English player refresh was checked separately without changing approved audio/media bytes. Final translated packaging and release status must be supported by each locale's current receipts. Generated ZIPs and LMS HTML delivery copies remain outside Git.

The **10 November 2026** language release verifies 700 native slide-narration script/receipt/master/delivery pairs, all 84 localized recording soundtracks and complete caption texts, 140 static figures, and 112 finite teaching sequences. Each locale passed 224 desktop/phone slide-layout cases, all 12 original players at both widths, and all 16 synchronized sequences at both widths, including pause/seek/speed/enlargement/end-hold/replay. Bounded decoder waits observe real MP3 ending and decoded 4K seek completion without relaxing the synchronization tolerance. The English refresh made zero synthesis requests and preserved all 190 approved media assets byte-for-byte. See the language-release receipt above for checksums, coverage and limitations.

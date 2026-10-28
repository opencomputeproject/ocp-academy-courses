# Validation and acceptance

The approved local course was exported as editable repository source on October 27, 2026, and rebuilt using the current repository AcademyWizard with the existing narration. No narration was regenerated. `authoring/qa/source-rebuild.json` records archive comparison and source normalization; `authoring/qa/audio-audit.json` records the 48 verified v4 output hashes and timing measurements.

The fresh build passes repository-aware source QA with zero flags, including 34 grounded glossary placements and both root catalog entries. All 21 SVG/animation sources pass arrow checks. The catalog exports pass their consistency check. All 48 reused narration clips pass the audio signal report. Folder validation, ZIP CRC and declared-resource checks pass for 103 runtime files.

Course Home is the first of five SCOs, followed by the four teaching modules. The manifest, API wrapper, narration and every media/font/caption asset are byte-identical to the approved local delivery. Five HTML pages differ because the source contribution uses the current shared repository renderer; teaching text, scripts, quiz content, original recordings and final-slide edits are preserved. The course's small renderer retains its reviewed enlarged-video control styling.

The maintained home and video unit suites pass (22 and 6 tests). Fresh-build browser checks pass 95 home assertions, 409 navigation assertions with 24 actual next-module clicks, 525 recording assertions including four native playback cases and 24 layouts, and 120 behavior/mobile assertions covering all 52 slides. File-based browser checks on the fresh repository build cover home initialization/completion/exit, review isolation, module navigation, quiz attempts, mobile scrolling, recording controls, captions and prevention of simultaneous narration. Their summaries are in `authoring/qa/repository-browser-summary.json`. Earlier approved home guard evidence is retained separately in `home-browser-results.json` and `home-regression-results.json`. These checks simulate an LMS API and do not establish acceptance in the target LMS.

Browser harnesses are portable and require Playwright. Each takes the built folder and an output folder outside source control:

```sh
node courses/introduction-to-liquid-cooling/scripts/check_home.mjs build/introduction-to-liquid-cooling build/qa/home
node courses/introduction-to-liquid-cooling/scripts/check_navigation.mjs build/introduction-to-liquid-cooling build/qa/navigation
node courses/introduction-to-liquid-cooling/scripts/check_recordings.mjs build/introduction-to-liquid-cooling build/qa/recordings
node courses/introduction-to-liquid-cooling/scripts/check_behavior.mjs build/introduction-to-liquid-cooling build/qa/behavior
```

Set `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` only when the host needs a specific Chromium binary. The harnesses open generated local files and use muted or stubbed audio; they do not start a localhost server. Recording styling is compared with the retained DC Basics reference values in `recording-player-reference.json`; this is not a new playback test of that separate course.

Remaining acceptance work: human listening/caption review and live target-LMS navigation, tracking, completion and resume checks. Direct links cannot establish a new SCORM 1.2 tracking context. No LMS upload, replacement, deletion, tracking reset or source-version migration was performed during this contribution. The historical four-SCO plan is superseded by the approved Course Home-plus-four-module organization.

## Coolant terminology update — October 28, 2026

M2S5 now introduces DI (deionized water), EG25 (ethylene glycol), PG25 and PG55 (propylene glycol), including nominal concentrations and product-specific qualification. New glossary entries cover DI water, EG25 and PG55; the PG25 definition is expanded. The script speaks every letter acronym and its full expansion. Only this slide’s ElevenLabs v4 narration was regenerated, with the same voice and same-text v2 pacing reference. All 47 other narration clips, all nine videos, other media, Home and manifest are unchanged. Source QA validates 34 glossary placements. The new audio passes signal checks and speech-recognition completeness review; 155 desktop/phone tooltip, transcript and layout assertions pass. Human listening approval remains pending. The dated coolant update record preserves these results separately from the original source-build baseline.

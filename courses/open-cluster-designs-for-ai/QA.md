# Review-build verification — 29 October 2026

The review folder contains Course Home and four narrated module pages: 45 slides, twenty editable teaching SVGs and five finite teaching videos. Estimated learner time is 55 minutes; measured narration is 23.81 minutes. The SCORM 1.2 manifest contains five SCOs: tracked Home plus four modules.

## Completed

- Source quality audit: no flags; video coverage in every module, 22 supported first-use glossary placements, 24 PDF resource links with page-specific teaching labels, whole-document closing links, course README, 800×400 poster and both repository catalog locations.
- Source review: five published contributions extracted page by page, with rendered checks of critical endpoint, arithmetic and maturity claims. The source audit records conflicting published tables and the course's reconciliations rather than silently treating every summary quantity as authoritative.
- Narration: all 45 clips generated using Leo, full `eleven_v4`, native masters and pitch-preserving 1.18 tempo. All 45 automated level/tail checks passed. A separate silence scan found no detected gaps of 0.8 seconds or longer at the recorded threshold. These signal checks do not establish pronunciation or editorial approval.
- Static figures: all twenty rendered at 1600×900, with zero out-of-canvas SVG text bounds and visual inspection. The eight-pod-group composition was revised to use one aggregate group connection. Poster and desktop/phone Home were visually inspected.
- Animation sources and encoded media: Astra reviewed 34 source checkpoints and 232 decoded timeline samples spanning all five complete timelines, including cue transitions, native final frames and paired 200% text/connector comparisons. All decode checks passed, endpoint identities and final states remained complete, and encoded duration differences were less than one 24 fps frame. RGB PSNR was 37.70–41.50 dB; minor chroma/edge differences were reviewed and accepted as nonblocking. See `authoring/encoded-review.md` and its JSON evidence.
- Geometry: 27 SVG/inline-animation source files passed the shared arrow checks.
- Runtime videos: ten desktop/phone cases passed 230 real-media assertions covering synchronized playback, pause, seeking, speed, enlargement, completion, final-picture hold without repeat, replay and reduced-motion opt-in. Two initial M1S4 fixed-delay seek assertions failed while encoding/browser work competed for resources; isolated and then full sequential reruns passed without media/player changes. Initial and final reports remain in the local authoring evidence.
- Course pages: 92 actual desktop/phone pages passed active-slide, media-loading and horizontal-overflow checks; all were captured after the motion intro and transitions settled. A further six-page check verified the shortened M1S4/M4S5 titles and Home. Visual review covered all modules and media.
- Saved state: 103 maintained slide-resume, control, review-isolation and video assertions, plus 34 quiz-resume/review-navigation assertions, passed using isolated browser storage and a mock SCORM API.
- Learner controls: 95 desktop/phone assertions passed for immediate slide-one playback attempts during the intro, default/saved playback speed, narration off/on hints after reload, keyboard-visible glossary definitions and viewport bounds. Representative long tooltips were inspected above the fixed controls.
- Integrity: 235 current script/media, narration-duration and five-SCO structure checks passed. The current source and review folder have matching course definitions. No credential tokens were found in the new course source.
- Shared unit suite: 130 tests passed. The shared changes preserve Home/index in every Slides course, allow the recorder's finite JS/SVG master clock and root duration attributes, and recognize OCP PDF document routes with trailing slashes in reference checks.
- Generated runtime package validation and formal LMS metadata export checks passed. The resource hook stages local fonts/branding; the owner subsequently requested the ZIP. Its 92 members match the manifest exactly; archive CRC passed, with 45 WAVs, five teaching videos and five SCOs. No new PR was created.

## Acceptance still pending

Human listening and editorial review remain pending, particularly pronunciation and fine narration-to-animation cue alignment. Cue positions are editorial estimates from the actual pronunciation-aware text and measured WAV duration, not forced alignment.

Mock SCORM checks are not target-LMS acceptance. Before publication, verify syllabus launches, separate module bookmarks, assessment persistence and completion in the actual LMS. Direct Home/module HTML links cannot switch SCORM 1.2 tracking context. Courses 92/93 may remain unpublished until the owner releases them.

The final review is through the generated `index.html` and `module1.html`–`module4.html` pages using `?review=1`, which pauses automatic narration and avoids saved learner progress. Normal playback separately retains immediate slide-one narration attempts, browser-policy fallback, learner speed preferences and bookmarks.

## 30 October 2026 — M1S3 alignment correction

Centered the five-box requirement row with equal 65px outer margins. Traffic, the downward arrow and Candidate design share x=800 on the 1600px canvas. The row label is centered on that axis as well. Verified the actual slide at desktop and phone widths and refreshed the reviewed SVG hash and delivery ZIP.

## 30 October 2026 — original XOC-N figures in Module 2

M2S6 now reproduces Figure 6 (Clos, PDF viewer p.24); M2S7 reproduces Figure 7 (rail-optimized, p.33). The 400dpi crops preserve the complete figure regions, original labels and colors, excluding page headers/body/caption/footer. Source attribution and CC BY-SA4.0 notice appear in the course captions and source inventory. The two replaced simplified SVGs are preserved under `authoring/retired-figures/`. A source-PDF hash check and repeatable extraction helper are retained.

Both slides were re-recorded with Leo, full Eleven v4 and pitch-preserving 1.18 tempo. The narration walks through each original plan and preserves the distinction between January equipment quantities and April's same-platform comparison. The rail glossary moved to M2S7. Module count, slide IDs, assessment rules and the approximate 55-minute learner-time estimate remain unchanged; total narration is now 24.40 minutes. No teaching video was changed.

The two new clips passed automated level/tail checks (all twelve Module 2 clips checked, zero flags). Actual desktop/phone course checks cover figure loading, original-resolution enlargement, playback/pause and matching WAV durations. The source audit and runtime package validator passed with zero flags, and 235 current script/media/timing/structure checks passed. Human listening review is still pending. The delivered ZIP is byte-for-byte unchanged, in accordance with the user's instruction to hold packaging until the wider review ends.

## 30 October 2026 — Clos pronunciation

Replaced all four spoken occurrences of Clos with the pronunciation-aware spelling `Kloh`, rhyming with go/slow and with a silent s, on M2S6 and M3S4. Formal display transcripts and every visible Clos label remain unchanged. Both WAVs were regenerated using full Eleven v4, the same Leo voice and 1.18 pitch-preserving pacing. All twelve clips in each affected module passed the automated level/tail checks. Human pronunciation listening remains pending user review.

M3S4's unchanged animation design was retimed and encoded to its new 47.933696s WAV; the encoded video differs by less than one frame. Six source/encoded checkpoints were inspected. Four stable checkpoints are pixel-identical to the prior accepted frames, carrying forward their native/200% visual comparison; the two in-transition checkpoints differ with the retimed reveal progression. Layout, legibility and visible wording remain unchanged. Desktop and phone cases passed all 46 real-media synchronization, seek, speed, enlargement and final-picture-hold assertions. Current reviewed media hashes and cue phrases are saved. The ZIP remains byte-for-byte unchanged.

## Repository delivery — 30 October 2026

At the user's subsequent explicit request, the delivery ZIP was refreshed with all review corrections. Its 92 runtime members exactly match the manifest, CRC checks pass, and current figures, narration and teaching video bytes match the review build. The repository source was then rebuilt with the maintained pipeline and existing full-v4 audio: all 45 audio level/tail checks, strict package validation, catalog exports and 130 shared tests passed. Generated narration, rendered runtime pages and ZIPs remain outside Git.

The repository rebuild preserves the course definition and all 87 non-HTML runtime files byte-for-byte. Its five HTML pages use the repository's maintained wrapping and glossary styles; 95 learner-control/glossary assertions and fourteen desktop/phone page checks passed against that rebuild. The retiming helper was exercised in a disposable fixture and preserved all five measured PCM durations, metadata and final-picture holds.

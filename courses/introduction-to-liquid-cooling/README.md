# Introduction to Liquid Cooling

An introductory Slides course in four modules: Why Liquid Cooling Now?; Direct Liquid Cooling (DLC); Immersion Cooling Essentials; and Operations, Planning & Strategic Value. Each module has 13 slides, one original recording on slide 9 and a two-question knowledge check. Estimated learner time is 68 minutes, or 17 minutes per module. The course includes 48 ElevenLabs v4 narration scripts, four intact recordings and five silent teaching animations.

One SCORM **1.2** package has **five syllabus SCOs**: Course Home (`index.html`) first, followed by the four teaching modules. Home completes on launch; each module saves its own bookmark, quiz attempts and completion. Both quiz questions require an attempt; correctness is not a completion gate. Green next-module controls remain visible and clickable locally, in review and in LMS playback. Direct page links do not switch LMS tracking contexts; use LMS syllabus launches for separately tracked module selection and verify the target LMS behavior.

Formal LMS copy is in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json). `thumbnail.png` is the 800×400 LMS poster; its editable SVG is in `authoring/thumbnail.svg`.

## Edit and build

`course.json` is canonical; narration scripts are in `audio/moduleN/`. Static SVGs remain editable in `figures/`, and the five finite teaching animations retain their HTML/SVG sources in `animations/`. Imported MP4s, posters and editable English captions are in `resources/`. Fonts include their license. Original contributor recognition is rendered from `authoring/credits.json`.

From the repository root, reuse approved narration extracted outside the checkout:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio bash scripts/build-course.sh introduction-to-liquid-cooling
python3 courses/introduction-to-liquid-cooling/scripts/verify_package.py build/introduction-to-liquid-cooling
```

The course resource hook stages fonts, the poster and contributor credits. The small course renderer preserves the reviewed enlarged-video control styling while using the shared player. The shared index renderer supplies Course Home and its SCO unchanged; do not remove `ITEM_LAUNCHER`, convert `RES_LAUNCHER` to an asset, or disable Home's session lifecycle. `scripts/verify_package.py` checks the same five-SCO contract in the built folder and ZIP.

Generated narration, rendered pages, original Rise archives and SCORM ZIPs remain outside source control. Reusing the approved audio avoids synthesis. Generating new narration requires the recorded Leo voice, ElevenLabs v4 and same-text v2 pacing references at 1.18 with pitch preserved; changing audio requires fresh listening and signal checks. The learner speed default is 1.0×. Review generated local files from `index.html`, or use `moduleN.html?review=1&slide=1` for an isolated editorial pass. No localhost server is required.

## Editorial and source notes

The four original Rise modules were recovered independently and retained locally. Their four video binaries are included byte for byte in their corresponding modules. On recordings, the black player owns audio; slide narration Play and speed controls are disabled and the prior narration source is cleared. The next narrated slide restores normal controls. The English captions were transcribed because the original exports contained no timed-text tracks; human caption/listening approval remains pending.

The course teaches introductory choices and evidence questions, with selective live Academy links to Brazos, Deschutes, MGX/MQD, fluids, phase behavior and Thermal Boundaries. Important resources recur on the closing slide. M2S3's visible resource supports its single-phase cold-plate example. The two closing summary bullets removed during review remain absent. All learner references point to live official resources, not repository source.

The historical approved narration plan is in `authoring/approved-narration-plan.json`. Its original four-SCO packaging choice was superseded by the user's October 27 correction to include Course Home as its own SCO. The four original SCORM 2004 source packages were consolidated into this user-selected SCORM 1.2 architecture; deployed attempts and bookmarks may require a separate LMS migration review. No LMS upload or deletion is part of this contribution.

See [QA.md](QA.md) for validation scope and remaining acceptance work.

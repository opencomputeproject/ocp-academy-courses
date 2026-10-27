# Rebuild the approved course

The deliverable is a SCORM 1.2 course with Course Home as first SCO followed by four module SCOs (five total). Do not compress the whole authoring folder. All runtime files are listed by `imsmanifest.xml`; authoring sources and QA records stay outside that runtime inventory.

## HTML and catalog

From the course folder:

```sh
python3 authoring/toolchain/academy-wizard/scripts/render_module.py course.json --all
python3 authoring/toolchain/academy-wizard/scripts/render_index.py course.json
python3 authoring/toolchain/academy-wizard/scripts/course_delivery_summary.py course.json --write
python3 authoring/toolchain/academy-wizard/scripts/course_delivery_summary.py course.json --check
```

The editable local renderer/templates preserve independent Home/module tracking, matching checks, manual imported recordings, captions, exposed imported-video controls, standard generated-video figure controls, top alignment, frame-aligned captions, 16px media spacing and 24px pill spacing. `technical_note` is an optional titled paragraph panel rendered before media. It provides written context without adding separate narration to imported videos. Maintain normal wrapping, slide scrolling and fixed-control clearance.

The local patch records differences from the installed skill. The shared-player patch documents earlier shared skill updates. Do not replace course-local extensions with an unmerged global snapshot.

## Narration

All 68 clips use Leo (`bbGtsRRKUfYO634UxSjz`) and `eleven_v4`. The approved pacing reference is Multilingual v2 at 1.18; the learner dial remains 1.0. New or changed text requires a fresh same-text v2 reference, never an old different-text WAV. The local `gen_audio.py` synthesizes native v4, then uses pitch-preserving atempo to match the verified reference within 50ms. Native masters, references and receipts are in the parent `_narration_work/`; delivery receipts are copied under QA. Supply credentials transiently; none are stored here.

## Teaching media

The first five videos retain `authoring/build_synced_media.py` and dated final-WAV maps under `qa/audio-video-update/`. The approved additions use `authoring/build_approved_media.py` and `qa/approved-content-build/alignment/`. All sources expose `renderAt(ms)` and a finite duration. Regenerate changed media from the final delivered WAV timestamps; equal clip lengths do not prove equal phrase timing.

```sh
python3 authoring/build_approved_media.py
node authoring/toolchain/academy-wizard/scripts/record_css_animation.mjs animations/module1/ai-placement.html figures/module1/ai-placement.mp4 figures/module1/ai-placement-poster.png
```

Repeat the recorder for liquid-heat-path (module2) and energy-ratio-change (module4). Check native text clearance and arrow geometry before encoding. Videos are silent, 1920×1080, 30fps, H.264 CRF8 with BT.709 conversion. Require source/decoded PSNR≥45dB and SSIM≥0.995, duration within one frame, meaningful phrase events and final holds. Generated Slides clips use standard figure Play/Pause and Enlarge controls, not the imported recording’s black player. Every generated figure opts into narration synchronization with no autoplay or loop. Imported videos keep their own audio and null slide narration.

After visually reviewing changed media, run `python3 authoring/refresh_m2_room_cooling.py` to refresh hash-bound media text evidence, glossary evidence, readable content exports and measured times. Never treat a fresh hash alone as visual review.

## Validation

```sh
python3 authoring/toolchain/academy-wizard/scripts/audio_tail_report.py course.json --fail-on-flags
python3 authoring/toolchain/academy-wizard/scripts/slides_course_qa.py course.json --fail-on-flags
python3 authoring/toolchain/academy-wizard/scripts/check_svg_arrows.py course.json --fail-on-flags
python3 authoring/toolchain/academy-wizard/scripts/validate_package.py .
xmllint --noout --schema authoring/qa/scorm12-delivery/manifest-validation.xsd imsmanifest.xml
```

Current browser checks and screenshots are in `authoring/qa/approved-content-build/`. Run those Node scripts with Playwright available. They open the actual module files through file URLs and mute audio. Check every media slide at desktop, phone and small-phone widths in both themes, all video controls, full synchronized passes, checks/retries, bookmarks, review isolation and independent Home/module tracking. Do not play audio aloud during automated QA.

Begin human review from `module1.html`; localhost is off. Human listening and a real target-LMS session remain release checks. Keep Course Home as the first tracked SCO and the four independently tracked modules. Final packaging and PR publication are authorized by the user. Keep generated ZIPs and WAVs outside Git.

The latest static Module 2 diagrams are owned by `authoring/build_m2_power_spaces.py`. Rebuild them with that script and visually review them before refreshing their media-text inventories. M2S4, M2S7 and M2S17 have revised same-text v4 pacing receipts under `qa/m2-power-and-spaces/`; native masters and v2 references are in the parent `_narration_work/2026-10-26-m2-power-spaces-v4/`.

## Compact static figure canvases

After generating or editing static SVGs, audit and fit their source artboards before refreshing reviewed text hashes and rebuilding HTML:

```sh
node authoring/toolchain/academy-wizard/scripts/fit_svg_artboards.mjs course.json --report authoring/qa/compact-figures/bounds.json
node authoring/toolchain/academy-wizard/scripts/fit_svg_artboards.mjs course.json --apply --report authoring/qa/compact-figures/applied.json
```

Inspect proposed bounds before applying. The current course uses a 24-source-unit artwork margin and trims only substantial excess (96 units or more); displayed frame padding remains unchanged. Three existing Module 1 teaching-note gaps were tightened in the editable SVGs and original source helper. The SVGs are canonical editable sources. New M2 diagrams continue to use `build_m2_power_spaces.py`; the fit step after any builder prevents padding regressions. Keep current glossary stacking styles when merging templates: `.learner-aids` must be above media controls, with the active glossary pill above its siblings.

`academy-wizard-compact-figures.patch` is incremental to the installed skill state after the earlier shared video/tooltip changes. Preserve those earlier changes when applying it; the delivered toolchain snapshot contains the complete current implementation.

## Room air cooling: M2S9–11

The current editable figures and complete room-air circuit belong to `authoring/build_m2_room_cooling.py`. Earlier builders delegate their overlapping outputs to it. Preserve the distinction between refrigerant-based CRAC and chilled-water CRAH, plus the supply/return roles and heat rejection beyond the room. Keep the deliberate opening in the containment boundary for its return connection.

```sh
python3 authoring/build_m2_room_cooling.py --static
python3 authoring/build_m2_room_cooling.py --animation
```

The animation build requires the final M2S11 WAV and its matching word map under `authoring/qa/m2-room-cooling/alignment/`. Regenerate that map whenever narration changes, inspect full-size native scenes and transitions, run the arrow checker, then encode the single finite pass with the maintained recorder. Review timing and decoded frames before refreshing current records and rebuilding HTML. M2S9–11 narration receipts and current targeted QA are under `authoring/qa/m2-room-cooling/`; native masters and same-text references remain outside the runtime in the parent `_narration_work/2026-10-27-m2-room-cooling-v4/`.

## Clean generated-video edges and rack-space glossary

The maintained `module_styles.css` uses a square, white, borderless inner surface for generated teaching videos in both normal and enlarged views. The outer card owns padding, rounding and shadow. Do not restore a dark video underpaint or inner corner radius: these produced faint corner arcs and a right-side seam even with clean encoded frames. Imported-recording surfaces retain their separate player styling. The installed skill also requires checking actual player edges alongside decoded video frames; its focused source patch is `academy-wizard-clean-video-edges.patch`.

Current surface, glossary, role and layout checks are in `qa/video-edge-rack-glossary/`. They inspect all eight generated clips in both views, three viewport sizes and two themes, including pixel checks along white margins. Rack-unit tooltips explain U/RU versus OU/OpenU with source links. The M2S14 Brazos pill targets the user-supplied OCP Academy course. All media and narration binaries retain their hashes.

## Reference and glossary editorial policy

The user approved removing both M3S4 vendor reference pills and reducing repeated basic glossary terms. Preserve `course.json.learner_aids_editorial_policy`: useful external evidence can remain in authoring without a learner-facing vendor link. The six other vendor pills remain after the user’s review; do not remove those automatically or restore the removed M3S4 links during a rebuild.

Basic words such as Power and Energy do not receive another pill merely because a new module begins or the word occurs in passing. Keep first useful course introductions. Useful acronyms and specialized terminology can retain reminders; repeated word definitions need a focused teaching purpose. The source review records 13 removals, leaving 59 pill placements across 48 definitions. The existing first-use audit still applies to retained placements; absence of a pill at a module’s first mention is intentional and does not require restoring one.

Build the complete review inventory from the editable source with `python3 authoring/build_reference_review.py`. Its HTML includes all 78 slides, selectable reference categories, removed links, glossary changes and a separate glossary-source register. CSV rows include active links and all approved removed links with explicit status. Outputs stay under `authoring/qa/reference-and-glossary-review/`, outside the runtime manifest.

## M3S15 installation-fit check

Keep the explicit 2U/continuous-4U scenario and the two justified selections in `course.json`. Do not infer chassis height from processor or compute-node count. The replacement ID is `m3_installation_fit`; `M3-KC2` is provenance for the retired matching item, not an answer-state key to reuse. First question `m3_kc1` remains unchanged. There are now two matching interactions, 13 questions total, ten retained source-check concepts and three new or replacement checks.

Two ordinary question cards use the maintained desktop grid automatically and stack on narrow screens. Preserve this preference without splitting approved single or three-question groups. M3S15’s revised paired script/WAV uses Leo / Eleven v4 and a fresh same-text v2 reference at 1.18. Its receipt, complete answer-combination tests, responsive screenshots, four-SCO harness and saved-answer migration check are under `qa/m3-rack-quiz-revision/`. Native masters and timing references are outside runtime in the parent `_narration_work/2026-10-27-m3-rack-quiz-v4/`.

## Final delivery

Use the pinned strict zipper, never a recursive archive of this working folder:

```sh
python3 authoring/toolchain/academy-wizard/scripts/zip_for_lms.py . --course-json course.json -o ../DC_Basics_OCP_Academy_SCORM_1_2.zip
```

The ZIP contains only manifest-listed runtime files. Catalog JSON/Markdown/HTML sidecars and `thumbnail.png` are supplied separately for LMS setup. Preserve Course Home as the first tracked SCO followed by the four module SCOs. In SCORM 1.2 the LMS syllabus launches modules; direct page links cannot switch tracking context. The adapter enforces the 4096-character saved-state budget and exposes save failures. See `qa/scorm12-delivery/` for the strict API simulation, schema check and final audit. Earlier dated 2004 checks are historical.

The XML helper schema’s reserved XML namespace declaration uses an explicit `xml` prefix for namespace-aware validator compatibility; its original annotations and type declarations are retained. The previous 2004 local delivery is archived outside this course folder. Changing format can require a new LMS upload and may not preserve deployed bookmarks, attempts or completions. Test a separate upload before retiring any existing item; no LMS action has been taken.

## Green next-module buttons

The current pinned `templates/learner_features.js` matches the installed AcademyWizard navigation policy. Do not restore the older LMS-only replacement of next-module links with syllabus instructions. Keep green links visible and clickable in local, review and API-present playback. Preserve review parameters and the next module’s first-slide entry. The Course Home guard remains the maintained compatibility policy. The five-SCO manifest and SCORM 1.2 API are unchanged. Run the portable `qa/green-navigation-refresh/navigation_parity.mjs` against the built course and the updated tracking harness under `qa/scorm12-delivery/`. No new synthesis or video encoding is needed.

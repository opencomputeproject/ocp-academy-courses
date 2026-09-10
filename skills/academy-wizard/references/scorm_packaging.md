# SCORM version selection and packaging

AcademyWizard supports two package organizations:

- **Slides:** multi-SCO package with Course Home plus one SCO per narrated module.
- **Scrolling:** single-SCO package where `index.html` contains the course cover and every lesson. Lesson progress and Continue-gate state live in `cmi.suspend_data`; the SCO completes after all lessons complete.

## New courses versus existing deployments

SCORM 2004 3rd Edition is allowed for new courses without requiring an exception to a universal 1.2 default. Prefer it when the target LMS supports the features the course needs: it provides more saved-state capacity and defines content-to-LMS navigation requests. Do not call it universally better, select 4th Edition for a 3rd-Edition-only LMS, or equate accepting an uploaded version with implementing its sequencing. Announce and record the selected version. Keep 1.2 where compatibility, the selected single-SCO design or an existing deployment calls for it.

The maintained `new_course.py`, `render_index.py` and `assets/scorm_api.js` currently build SCORM 1.2. Before delivering a 2004 course, implement and verify the corresponding runtime adapter, manifest namespaces/organization, interaction data and validator support. Merely changing `<schemaversion>` or adding course metadata does not convert a package. Existing source without explicit version metadata retains 1.2 behavior; a fresh build directory is not a new-course migration authorization.

For an existing course, inspect its source and delivered manifest and preserve that version unless the user explicitly approves changing it after hearing the migration consequences. Warn **before** conversion, and repeat at delivery:

> This changes the SCORM version. The LMS may require retiring/deleting the old material and uploading a new item rather than an overwrite. Existing bookmarks, attempts and completion history may not transfer. Export any needed reports and test a separate upload before retiring the old material.

For Docebo, make the warning definite: **a 1.2 material cannot be overwritten with 2004**. A new upload is required; replacing the old material means retiring/removing that item separately. **Deleting a SCORM package deletes its tracking, which Docebo says is not recoverable.** Building or delivering a ZIP does not authorize deletion, reset or upload in the live LMS.

## Docebo navigation limitations

Docebo accepts SCORM 1.2 and 2004 3rd Edition, but its documentation explicitly says sequencing is not supported. It can convert simple sequencing/linear navigation to platform prerequisites at upload; that is not proof that arbitrary in-course choice requests work. Do not promise that changing to 2004 fixes home-page cards or next-module buttons. Require target-LMS verification of those actions and their tracking before calling a multi-SCO package release-ready.

If the LMS cannot launch the correct next SCO from a course button, retain LMS syllabus navigation with honest UI, or propose a single-SCO course whose own home and module buttons control the pages. The latter keeps internal module organization but changes the LMS syllabus and completion reporting to one tracked activity. Obtain approval for that tradeoff; do not silently collapse modules or record later-module progress against the originally launched SCO.

Primary reference: [Docebo — Uploading and managing SCORM as training material](https://help.docebo.com/hc/en-us/articles/360020128479-Uploading-and-managing-SCORM-as-training-material), especially Introduction, Updating SCORM content and Tracking the progress of SCORM content. Recheck the target LMS documentation when selecting a format; support can change.

## Current SCORM 1.2 build contract

The following describes the current 1.2 implementation, not a substitute for a verified 2004 implementation.

## Required files at the package root

- `imsmanifest.xml` — the package descriptor.
- `index.html` — the launcher (the SCO that runs first).
- Slides only: one or more `moduleN.html` additional SCOs.
- Scrolling only: learner media under `resources/`; no `moduleN.html` files.
- `scorm_api.js` — wrapper that finds the LMS API and shims it. Copied verbatim from `assets/scorm_api.js`.
- All audio under `audio/moduleN/`.
- All figures under `figures/`.
- Brand assets at the root (logos).

## Manifest essentials

The manifest declares:

- One `<organization>` with one `<item>` per page (home + each module).
- One `<resource>` per page, listing every file that page needs (HTML + JS + every image and audio file referenced by the slide markup).

The XML uses three namespaces (IMS content packaging, ADL SCORM, XSI). Copy them from the reference manifest verbatim — they're not optional. Mis-declaring a namespace causes silent LMS failures.

`adlcp:scormtype="sco"` is set on every resource. `"asset"` is also valid but `"sco"` is what the reference uses and what most LMSes expect.

## What the LMS sees

- The LMS can expose `index.html` and each `moduleN.html` as separate SCO syllabus items. Each SCO must manage its own completion status.
- The Course Home launcher calls `SCORM.init()`, immediately sets `cmi.core.lesson_status` to `completed`, then reads `suspend_data` only to display completion state on module cards.
- Each module page calls `SCORM.init()`, preserves a prior `completed` or `passed` status on revisit, otherwise marks itself `incomplete`, and sets its `lesson_location`.
- When the learner reaches that module's final slide, the module updates `suspend_data.modules` for visual state and immediately sets its own `cmi.core.lesson_status` to `completed`. Do not wait for all modules before completing the current SCO.

Keep the slide count and `audioMap` accurate per module. SCORM 1.2 tracking is attached to the SCO the LMS launched. Direct hyperlinks between separately tracked module HTML files cannot replace LMS-controlled launches. Never claim separate module completion based only on a mock API or a shared local browser bookmark.

## Common pitfalls

- **Missing files in the manifest.** Every file referenced from HTML (every audio .wav, every figure .png) MUST appear in that module's `<resource>` block. The validator script enforces this.
- **Path mismatches.** All paths are relative to the package root, forward-slash style. No leading `./`. No `../`.
- **Spaces in filenames.** Don't. Use `slide_03_form_factors.wav`, not `slide 03 form factors.wav`.
- **Case sensitivity.** Some LMSes run on case-sensitive filesystems. `Module1.html` and `module1.html` are different files. Use lowercase consistently.
- **Audio file format.** `.wav` is widely supported. The reference uses 16-bit PCM at 22050 Hz. Some LMSes balk at 48 kHz files. The TTS script outputs 22050 Hz by default.

## Packaging for upload

Most LMSes accept the package as a `.zip` of the folder. **Use `scripts/zip_for_lms.py` to build a strict zip** containing only the files listed in `imsmanifest.xml`:

```
python scripts/zip_for_lms.py <package-folder>
```

This excludes working files (`course.json`, `.txt` narration scripts, `_outline.md`, `_figure_plan.md`, `gen_audio_standalone.py`, `.DS_Store`) which strict LMSes reject because they aren't declared in the manifest. The script also verifies every referenced file exists on disk before writing the zip — if anything is missing, it fails loudly rather than silently producing a broken package.

The wizard does **not** zip automatically — it delivers the folder. Run the script when the user is ready to upload.

### Why strict zipping matters

Some LMSes (and SCORM Cloud) scan the zip and reject any file not declared in `imsmanifest.xml`'s resource blocks. A `zip -r ... <folder>` or right-click → Compress picks up every working file. This is the single most common reason a SCORM zip is rejected after a clean validator run. Always use the strict zipper for delivery zips.

If you must zip manually for some reason, the equivalent shell command is:

```
cd <output-folder>/..
zip -r <TopicSlug>_OCP_Academy_SCORM.zip <TopicSlug>_OCP_Academy_SCORM \
    -x '*/.DS_Store' '*/course.json' '*/_*.md' '*/_*.py' \
       '*/audio/*/slide_*.txt' '*/gen_audio_standalone.py'
```


### No inline JavaScript event handlers

Strict LMS content scanners reject HTML containing inline JS event handlers — `onmouseover="..."`, `onclick="..."`, `onload="..."`, etc. The error often surfaces as a generic "file may not be formatted correctly" message with no detail. Always use `addEventListener` or CSS pseudo-classes (`:hover`, `:focus`) instead. The `survey-btn` hover state in `render_course_complete` is implemented as `.slide .survey-btn:hover` in `module_styles.css` for this reason. If you add new interactive elements, follow the same pattern.

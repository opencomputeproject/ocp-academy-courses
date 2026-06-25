# SCORM 1.2 packaging

The reference OCP NIC 3.0 package is SCORM 1.2. Stick with 1.2 unless the user specifically requests 2004 — most LMSes accept both, and 1.2 has fewer foot-guns.

## Required files at the package root

- `imsmanifest.xml` — the package descriptor.
- `index.html` — the launcher (the SCO that runs first).
- One or more `moduleN.html` — additional SCOs.
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

Don't reinvent this wiring. The template handles it; just keep the slide count and `audioMap` accurate per module. SCORM 1.2 tracking is attached to the SCO the LMS launched; in-course links between module HTML files are learner conveniences, not a replacement for LMS-controlled sequencing when a customer needs per-syllabus-item tracking.

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
zip -r <TopicSlug>_Academy_SCORM.zip <TopicSlug>_Academy_SCORM \
    -x '*/.DS_Store' '*/course.json' '*/_*.md' '*/_*.py' \
       '*/audio/*/slide_*.txt' '*/gen_audio_standalone.py'
```


### No inline JavaScript event handlers

Strict LMS content scanners reject HTML containing inline JS event handlers — `onmouseover="..."`, `onclick="..."`, `onload="..."`, etc. The error often surfaces as a generic "file may not be formatted correctly" message with no detail. Always use `addEventListener` or CSS pseudo-classes (`:hover`, `:focus`) instead. The `survey-btn` hover state in `render_course_complete` is implemented as `.slide .survey-btn:hover` in `module_styles.css` for this reason. If you add new interactive elements, follow the same pattern.
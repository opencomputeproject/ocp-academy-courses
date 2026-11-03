# Understanding and Procuring Open Technologies and Products

One narrated Slides course in OCP Community Orientation, written for a nontechnical audience. Understand what is open, what it costs, and who will keep it working.

The course has one content module, 19 slides and 19 narrated sections. Narration runs 5:16; narration plus original recordings runs 5:16. Estimated learner time is 7 minutes, including reading and the final two-question check. Optional resource exploration takes longer.

## Source and delivery

- `course.json` is the editable course definition. It replaces the previous Scrolling course at the same path.
- `audio/module1/*.txt` contains the current narration scripts. Generated MP3/WAV audio and SCORM ZIPs remain outside Git under repository policy.
- `figures/` and `animations/` contain course-owned media and editable teaching-video sources. Teaching videos play once on the narration clock and hold the completed final scene.
- `resources/` preserves original recordings, screenshots, captions and supporting documents. Screenshot galleries retain the original image bytes and can be updated as the OCP website changes.
- `course-mark.svg` is the approved course mark. [Catalog poster](thumbnail.png) is exactly 800 × 400; [poster.json](poster.json) and `poster-assets/` retain its editable design and authoritative branding.
- [LMS catalog fields](lms-catalog.md) and [structured metadata](lms-catalog.json) are separate from the README and runtime ZIP.

Narration uses full Eleven v4 (`eleven_v4`), Leo (`bbGtsRRKUfYO634UxSjz`), pitch-preserving 1.18 pacing, and 44.1 kHz, 96 kbps CBR mono MP3 delivery. The learner speed dial starts at 1.0.

SCORM delivery is 1.2 with one tracked course activity containing Course Home and the single teaching module. Completion requires the final check to be attempted and the final slide reached. The user confirmed LMS synchronization on November 3, 2026.

## Rebuild

From the repository root:

```bash
./scripts/build-course.sh ocp-orientation/understanding-and-procuring-open-technologies-and-products
```

Use the approved existing audio masters with `EXISTING_AUDIO_DIR` to avoid paid regeneration. Without those masters, the wrapper generates narration through the configured ElevenLabs voice and retains authoring receipts outside the runtime package. Preserve the approved voice, pacing, narration timing and SCORM organization.

## Language editions

Previous Scrolling translations were retired because they describe the superseded course. They remain recoverable in Git history. Replacement Slides translations must branch from this approved English source, preserving the one-module structure, media scope and authoritative links. The maintained voice choices are verified in [the live v4 compatibility record](../../../docs/orientation-v4-language-compatibility.json).

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/ocp-orientation/understanding-and-procuring-open-technologies-and-products
```

See [the poster standard](../../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.

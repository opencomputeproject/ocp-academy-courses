# Falcon animation sources

These nine silent 1920×1080 scenes explain distinct protocol relationships. Each HTML file contains a finite master duration and exposes `window.setTeachingTime(milliseconds)` for deterministic rendering. Module 1 embeds its reviewed runtime; module 2 loads `teaching.js`; module 3 embeds its timelines. Adjacent JSON files retain measured cue times and narration hashes.

| Module/slide | HTML master | Delivered media |
|---|---|---|
| M1S5 | `module1/push_flow.html` | `../figures/module1/push_flow.mp4` |
| M1S6 | `module1/pull_flow.html` | `../figures/module1/pull_flow.mp4` |
| M1S7 | `module1/pull_resources.html` | `../figures/module1/pull_resources.mp4` |
| M2S4 | `module2/a4_selective_repair.html` | `../figures/module2/a4_selective_repair.mp4` |
| M2S5 | `module2/a5a_rack.html` | `../figures/module2/a5a_rack.mp4` |
| M2S6 | `module2/a5b_tlp.html` | `../figures/module2/a5b_tlp.mp4` |
| M3S3 | `module3/a6-timestamps.html` | `../figures/module3/a6-timestamps.mp4` |
| M3S7 | `module3/a7-max-open-window.html` | `../figures/module3/a7-max-open-window.mp4` |
| M3S8 | `module3/a8-plb.html` | `../figures/module3/a8-plb.mp4` |

The frozen browser scenes are sufficient for video-only rebuilding. Paths prefixed `external-authoring/` in cue metadata identify the original external alignment evidence; that evidence and generated narration are not committed or required for rendering the existing timeline. Do not rerun historical draft generators over these reviewed scenes.

## Render a scene

Install the dependencies described in the repository's AcademyWizard instructions, including Playwright/Chromium and a full FFmpeg build with libx264. Set `FFMPEG_BIN` if FFmpeg is not on PATH. From the repository root, an example rebuild is:

```sh
node skills/academy-wizard/scripts/record_css_animation.mjs \
  courses/falcon-transport/animations/module1/push_flow.html \
  courses/falcon-transport/figures/module1/push_flow.mp4 \
  courses/falcon-transport/figures/module1/push_flow_poster.png
```

Use the matching paths in the table for other scenes. Keep each existing poster filename from `course.json`; module 3 uses `-poster.png`, while modules 1 and 2 use `_poster.png`. The recorder reads the declared timeline and poster time from the page and samples one pass at 30 fps. Do not substitute an arbitrary capture duration or enable looping.

Font rendering and encode bytes can differ by host. Review the encoded first, quarter, middle, three-quarter and final frames, transition-adjacent frames and a complete playback pass. Check containment, labels, arrows, continuity and the final hold. Preserve narration-synchronized playback in both the slide and enlarged view, including seeking and changed learner speed.

`../qa/media-review.json` and each figure's `text_inventory` bind the reviewed visible text to the current MP4 hash. After changing a scene or encode, perform the review before updating those hashes; a fresh digest alone is not review evidence. If narration changes, retime the substantive events to the new final audio and verify duration agreement within one encoded frame.

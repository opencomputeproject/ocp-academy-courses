# Teaching animation sources

These HTML/CSS sources each contain one finite master pass. The maintained course player owns loop resets; narration remains separate.

| Source | Duration | Poster time | Instructional purpose |
|---|---:|---:|---|
| `avoidance_zone.html` | 14 s | 8.5 s | Equal illustrative demand intervals; the operating point changes from green to yellow at the economic boundary and to red at the physics boundary. |
| `thermal_path.html` | 16 s | 12.5 s | Contrast an acquisition constraint with an unresolved distributed remainder. |
| `commissioning.html` | 16 s | 14.5 s | Connect agreed criteria, an illustrative load change, observed response, and a witnessed record. |

The sources use `data-duration-ms`, `data-poster-ms`, finite CSS animations, and fill-both ending behavior. Encode exactly one master pass. None supplies numerical deployment limits or required response times.

From the repository root, use the maintained recorder with Playwright and a full ffmpeg build available:

```bash
node skills/academy-wizard/scripts/record_css_animation.mjs \
  courses/thermal-boundaries-in-ai-infrastructure/animations/avoidance_zone.html \
  courses/thermal-boundaries-in-ai-infrastructure/figures/avoidance_zone.mp4 \
  courses/thermal-boundaries-in-ai-infrastructure/figures/avoidance_zone_poster.png
```

Repeat for the other two matching names. `FFMPEG_BIN` can select a full H.264-capable ffmpeg build. The default recorder captures lossless 1920×1080 PNG frames and produces high-quality H.264 at 30 fps.

After changing an asset, review first, quarter, half, three-quarter, final, and transition-adjacent frames, then scrub a complete muted pass. Check continuity, label clearance, and final-frame behavior. Compare the decode with the source at native size and 200% detail. Update that figure's reviewed `text_inventory.sha256` in `course.json` only after visual review, then run source QA and rebuild.

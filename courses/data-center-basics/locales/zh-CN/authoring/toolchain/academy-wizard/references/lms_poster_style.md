# OCP Academy LMS poster standard

All catalog posters use the single maintained [HTML/CSS template](../templates/poster/poster.html) and [renderer](../scripts/render_lms_posters.mjs). Maintain exactly one English `thumbnail.png` per course or series, shared by every language edition. Do not create translated posters or duplicate them under `locales/`. Do not create a separate composition per course or use image generation for the poster's text, logo, frame or background. Topic artwork is the variable part.

## Fixed design

Coordinates are CSS pixels measured from the top-left of an 800 × 400 artboard.

| Element | Maintained specification |
|---|---|
| Background | 115° gradient: `#1D2258` at 0%, `#252A6B` at 48%, `#343895` at 100% |
| Green rail | 115° gradient: `#A8D95C`, `#8DC63F`, `#72A52F`; left edge from (604, 0) to (684, 400) |
| Translucent band / accents | Shared template only; no course-specific geometry or opacity |
| Academy logo | Exact `assets/ocp_academy_white.svg`; x=42, y=26, width=145, height=71.08; contain without distortion |
| Green pill | x=42, y=118, height=28, radius=14; minimum width=100; width grows with label, 14px horizontal padding |
| Pill type | Bundled Lato Bold 700, 13px, 18px line height, 1.4px tracking; navy on OCP green |
| Title | x=42, y=163, width=458, height=144; bundled Lato Bold 700, uppercase, 40px, line height 1.1, normal tracking |
| Long-title exceptions | Try word wrapping at 40px first, then 36px, then 32px. Use the largest fitting tier; no arbitrary sizes, condensed fonts or horizontal scaling |
| Divider | x=42, y=318, width=60, height=4; OCP green |
| Supporting copy | x=42, y=337, width=458; Lato Bold 700, 18px, 23px line height; at most two lines |
| White graphic area | x=528, y=78, 244 × 244 circle; 3px indigo border; shared white-to-cool-gray face and restrained shadow |
| Course artwork | Centered 176 × 176 contain box at (562, 112); preserve artwork aspect ratio and clear space |

The rail always slopes down to the right. Do not move the logo, pill, title, divider or circle to fit a long title. Only the title's wrapping and the three defined size tiers can change. Pill width may grow; its anchor and height stay fixed. Short titles retain the same size as other titles, even when that leaves additional space below them. Qualifiers belong in the title at the same weight and size, rather than introducing another course-specific hierarchy.

Use bundled Lato Bold for all catalog poster text, which stays in English regardless of course translations. See [font provenance](poster_fonts.md).

## Editable course source

Store `poster.json` beside `thumbnail.png`. It is the source of poster copy and the artwork path; `course.json` remains authoritative for teaching content and LMS metadata. Preserve approved catalog wording when migrating. Resolve the artwork path relative to `poster.json`.

```json
{
  "schema_version": 1,
  "language": "en-US",
  "badge": "OCP SST",
  "title_lines": ["SOLID STATE", "TRANSFORMERS"],
  "support_lines": ["From medium voltage to a", "regulated 800 VDC bus"],
  "mark": "sst_course_icon.svg",
  "mark_alt": "Solid state transformer course mark"
}
```

Use `title_lines` for preferred editorial line breaks. The renderer preserves them when they fit at the current size; otherwise it balances word wrapping before trying a smaller tier. It never truncates text. `™` in titles renders as superscript TM. Set `language` to `en-US` (or another English locale). Translated course content and LMS descriptions remain independent; they reuse the canonical English poster.

Prefer the course's existing vector mark or supplied official program logo. Keep official trademark artwork exact. A series may reuse a relevant course mark. Keep symbolic graphics simple and readable, inside the artwork box. Do not add vendor logos, tiny schematic labels, or invented branding. New artwork may use appropriate vector or image-generation tools, but composition and typography always come from the template.

## Build and check

From the repository root, install the pinned renderer dependency once:

```sh
npm ci --prefix skills/academy-wizard
npx --prefix skills/academy-wizard playwright install chromium
```

Rebuild every catalog poster, including nested series, excluding locale folders:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root .
```

Rebuild only one course (also works with an installed skill and an external course):

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/ocp-solid-state-transformers
```

Verify the committed outputs without replacing them:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --check
```

The renderer skips `locales/` and discovers both canonical `poster.json` and existing `thumbnail.png` files, so missing metadata cannot silently omit a poster. It loads bundled assets offline, checks fonts, measured text bounds, fixed geometry, PNG format/dimensions, and reports the chosen title tier. `--check` compares PNG bytes first, then decoded pixels if necessary. It tolerates only isolated native text-smoothing rounding: at most 16 of 320,000 pixels (0.005%), each at most 16/255 per channel. Comparison metrics are recorded in the QA report; larger changes fail and save a drift PNG. Use the pinned dependencies on the same platform when checking exact raster reproduction. A platform difference still needs visual review, not automatic replacement of accepted output.

The fixed background, rail, accents and circle are authored in `templates/poster/background.svg` and rasterized once with pinned resvg into `background.png`. Every poster embeds that same asset, avoiding browser-specific curve smoothing differences between cards. The renderer verifies that the PNG matches its SVG on every run. After an intentional shell edit, run `node skills/academy-wizard/scripts/render_poster_background.mjs`, then rebuild the full catalog. Keep both background files in source control.

QA output goes to ignored `build/poster-qa/` by default (override with `--qa-dir`): full-size standalone HTML/PNG, 400 × 200 and 240 × 120 PNG previews, a gallery and `report.json`. Review every poster at full size and both reduced sizes for correct copy, clear glyphs, artwork containment and readable hierarchy. Technical bounds checks cannot establish editorial correctness or the appearance of the artwork.

Commit `poster.json`, the course artwork when new, `thumbnail.png`, and any shared template changes. The bundled [SST](posters/sst.png) and [AICC](posters/aicc.png) references must match the rebuilt course posters. Historical per-course SVG/HTML compositions have been retired; retained compatibility scripts call this renderer. Do not revive the old compositions or copy screenshots as editable sources. Changes to this standard belong in the shared template and this reference, followed by a complete catalog rebuild.

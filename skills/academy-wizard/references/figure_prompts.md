# Figures: reuse, generate, or draw inline

A great technical course illustrates almost every content slide. The reference OCP NIC 3.0 course only uses figures on module 5 (airflow + thermal/shock fixtures); aim higher — at least half the content slides should have a figure.

## Decide the figure source

**Reuse first.** Source PDFs and PPTX usually contain better, more accurate diagrams than anything AI generation can produce. Architecture diagrams, pinouts, mechanical drawings, photos of hardware — extract them.

**Inline SVG for simple structure diagrams.** Three labeled boxes with arrows? A timeline? A simple flow? Build it inline. SVG renders crisp at any size, scales for accessibility, and edits in seconds.

**AI-generate only when neither works.** Examples: an icon banner for a module, a stylized illustration of a concept (e.g., "ecosystem of vendors collaborating"), a placeholder hero image. Never AI-generate a *technical* diagram — they will be wrong in subtle ways and embarrass the course.

## OCP visual style

When AI-generating, anchor the prompt to this style.

- **Palette**: OCP green `#8DC63F` for accents. Neutral grays `#5F6062`, `#757577`, `#9ca3af`. White background. Avoid bright colors except for emphasis.
- **Style**: Clean, minimal, flat-vector look. Thin strokes (1–2px). Generous whitespace.
- **Typography in figures**: Sans-serif. Match Open Sans where possible.
- **Avoid**: photorealism, 3D renders, drop shadows, glossy reflections, anime, stock-photo feel.

## Prompt template for AI figure generation

```
A clean, flat vector illustration on a white background, in the style of a modern
technical infographic. Subject: <describe what's shown>. Composition: <layout —
left/right, top/bottom, central, grid>. Color palette: mostly neutral grays
(#5F6062, #757577) with OCP green (#8DC63F) used to highlight <which element>.
Typography: thin sans-serif labels. No 3D, no shadows, no photoreal elements.
Aspect ratio: 16:9.
```

### Example

For "an icon depicting the multi-vendor ecosystem of OCP NIC contributors":

```
A clean, flat vector illustration on a white background, in the style of a modern
technical infographic. Subject: a hexagonal grid of 16 generic company logo
placeholders connected by thin lines to a central node labeled "OCP NIC 3.0."
Composition: central node larger than the surrounding hexagons. Color palette:
neutral gray (#757577) for the placeholder hexes, OCP green (#8DC63F) for the
central node and the connecting lines. Typography: thin sans-serif labels.
No 3D, no shadows, no photoreal elements. Aspect ratio: 16:9.
```

## Inline SVG patterns

For programmatic diagrams, the renderer can drop raw SVG into the slide HTML. Common patterns:

- **Box-and-arrow flow**: a row of three rounded rectangles connected by arrows.
- **Stacked layer diagram**: e.g., the firmware/management stack — labeled horizontal bars.
- **Timeline**: a horizontal line with milestone markers.
- **Pinout grid**: a labeled rectangular grid for connector pinouts (faster than reproducing a CAD figure).

When the course.json says `figure: { type: "svg_inline", template: "box_flow", data: {...} }`, the renderer assembles SVG from a small template library. Keep these helpers in `templates/svg_helpers.html` and update them as needed.

### Inline SVG QA rules

Run this checklist before rendering a module final:

- Give each colored arrow family its own `<marker>` with the same fill or stroke color as the line. A green line uses a green marker; an orange warning line uses an orange marker; a blue line uses a blue marker.
- For curved or diagonal arrows, the line must flow into the center of the arrowhead's flat back side. Do not let the path terminate at the point of the arrowhead; that makes the line look attached to the wrong end unless the arrow is perfectly straight and aligned.
- Prefer explicit arrowhead polygons for curved or diagonal arrows: end the `<path>` at the flat-back center point, then draw a same-color triangle whose flat side is centered on that endpoint and whose point extends forward. If using an SVG `<marker>`, set `refX`/`refY` to the flat-back center or shorten the path so the visible line meets the back of the head, not the tip.
- Stop the arrowhead point exactly at the target object's boundary line. The point may touch the stroke of a box, card, callout, connector, or diagram object, but it must not extend into that shape.
- Prefer modest arrowheads. If a marker looks like a detached triangle, reduce `markerWidth`, `markerHeight`, or switch to `markerUnits="userSpaceOnUse"` with an open arrow path.
- Make labels avoid paths. A label describing the entire top loop belongs above the line, centered to the overall figure; side callout labels should sit outside the diagram and align with their subtext.
- Align grouped objects as groups, not one element at a time. Repeated bars, wicks, bubbles, cards, or nodes should visually center within their parent shape.
- Use wrapped `<tspan>` lines or wider shapes when text risks escaping boxes, pills, or badges.
- Run `scripts/check_svg_arrows.py course.json --fail-on-flags` before rendering modules that reference custom SVGs.
- Render and inspect at desktop and mobile widths when a diagram has many labels. SVG source that looks reasonable in code can still overlap after font rendering.

## Caption rules

Every figure has a caption. Captions are not bullet lists — they're one or two sentences that explain *what the figure is showing* and *what the learner should take from it*. The narration may reference the figure, but the caption is the silent fallback for learners skimming.

## Banner and thumbnail exports

When the user asks for a course banner, thumbnail, or LMS image at an exact size, verify the generated file dimensions after saving. If the image generator returns the right aspect ratio but a different pixel size, resize a copy to the requested width and height and deliver the exact-size PNG/JPG requested.

# Figures: reuse, generate, or draw inline

A great technical course illustrates almost every content slide. The reference OCP NIC 3.0 course only uses figures on module 5 (airflow + thermal/shock fixtures); aim higher — at least half the content slides should have a figure.

## Decide the figure source

**Reuse first.** Source PDFs and PPTX usually contain better, more accurate diagrams than anything AI generation can produce. Architecture diagrams, pinouts, mechanical drawings, photos of hardware — extract them.

**Inline SVG for simple structure diagrams.** Three labeled boxes with arrows? A timeline? A simple flow? Build it inline. SVG renders crisp at any size, scales for accessibility, and edits in seconds.

**AI-generate only when neither works.** Examples: an icon banner for a module, a stylized illustration of a concept (e.g., "ecosystem of vendors collaborating"), a placeholder hero image. Never AI-generate a *technical* diagram — they will be wrong in subtle ways and embarrass the course.

## Teaching-animation coverage

For every newly authored narrated Slides course, include at least one silent teaching animation or short video in each module unless the user explicitly opts out. Put it on the slide whose explanation benefits most from motion: a changing boundary, sequence, state transition, topology reconfiguration, cause-and-effect chain, or tradeoff. It may replace that slide's static figure, but do not force it onto an unsuitable slide. Add more than one in a module only when each animation teaches a distinct relationship.

Animations must earn their motion. Do not animate decorative progress bars, counters, arrows, or state changes that imply an event the narration never explains. Quantities that represent accumulation, reach, completion, or capacity must move monotonically unless a visible and narrated reset, failure, rollback, or comparison boundary causes the reversal. A seamless loop may reset only at the loop boundary, where the restart is visually unmistakable.

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
- Keep semantically contained objects physically contained. Gauges, thermometers, icons, markers, and badges that belong inside a circle or card must remain within that boundary at every animation state.
- Make every line and connector carry a relationship the learner can explain. Remove decorative or ambiguous connectors, especially lines between major boxes that do not show flow, dependency, containment, or comparison.
- Use the broadest accurate system label. If a placement can apply to a switch, server, accelerator tray, or another host, label it `system` or `compute/network system` rather than narrowing it to a switch unless the source explicitly does so.
- Run `scripts/check_svg_arrows.py course.json --fail-on-flags` before rendering modules that reference custom SVGs.
- Render every static figure and poster at its final slide size. Inspect at desktop and mobile widths, then inspect the original-resolution render. Check text-to-box clearance, text-to-axis and text-to-line collisions, diagram-to-caption collisions, icon containment, chart labels, and overlap between neighboring major elements. SVG source that looks reasonable in code can still overlap after font rendering.

### Animation QA rules

- Render and inspect at least five evenly spaced frames: first, 25%, 50%, 75%, and final. Add frames immediately before and after any transition that changes layout or state.
- Watch or scrub one complete loop in real time. Five static frames do not reveal backward jumps, flicker, momentary overlap, or an unexplained reset between checkpoints.
- Compare every animated text element and object with its containing shape at every distinct layout state. Require the same 0.75em text clearance used for static SVGs.
- Keep labels, axes, trend lines, callouts, and chart panels disjoint unless the overlap intentionally encodes a data relationship. Move explanatory cards outside plotting areas rather than covering the chart.
- Verify that the poster is a clean, representative frame and that the video is silent, muted, loopable, and free of a jarring end-to-start discontinuity.
- Run visual QA with browser or system playback muted so testing does not compete with a learner or reviewer listening nearby.

## Caption rules

Every figure has a caption. Captions are not bullet lists — they're one or two sentences that explain *what the figure is showing* and *what the learner should take from it*. The narration may reference the figure, but the caption is the silent fallback for learners skimming.

## Banner and thumbnail exports

When the user asks for a course banner, thumbnail, or LMS image at an exact size, verify the generated file dimensions after saving. If the image generator returns the right aspect ratio but a different pixel size, resize a copy to the requested width and height and deliver the exact-size PNG/JPG requested.

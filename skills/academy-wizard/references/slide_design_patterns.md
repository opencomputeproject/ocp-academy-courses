# Slide design patterns

Every module in the reference course follows the same skeleton. Match it — learners build muscle memory across modules, and the SCORM completion logic depends on the last slide being the "next module" pattern.

## Module skeleton

| Position | Type | Purpose |
|---|---|---|
| 1 | `title` | Module name + module number badge. Half-minute. |
| 2 | `objectives` (or `course_overview` in module 1) | What the learner will know by the end. |
| 3 to N-3 | `content` (various layouts) | The actual teaching slides. |
| N-2 | `takeaways` | 4-6 checkmarked summary bullets. |
| N-1 | `knowledge_check` | SCORM-friendly multiple-choice check. Requires an attempt, allows retry, does not require correctness to advance. |
| N | `up_next` or `course_complete` | One-liner pointing to the next module, or completion banner on the final module. |

## Slide types and when to use each

### `title`
The first slide of every module. Bold hero treatment, big module title, course logo, version chip.
- Fields: `title`, `subtitle`, `module_number`, optional `version_chip`.
- The course logo comes from top-level `brand.course_logo`; set it before rendering so the title slide is not missing its floating icon.
- The fixed course tagline appears below the play instruction, at the bottom of the title-slide text stack.

### `course_overview` (module 1, slide 2)
The full list of modules with metadata chips (duration, audience, basis).
- Fields: `title`, `subtitle`, `modules[]` (just titles), `chips[]`.

### `objectives` (every other module, slide 2)
"By the end of this module, you will…" plus 3–5 numbered objectives.
- Fields: `title`, `subtitle`, `objectives[]`.
- The renderer label is already `Learning Objectives`; use a descriptive title such as `Deployment Choices You Will Classify`, not `Learning Objectives`.

### `content_bullets`
Standard slide: section label, title, intro sentence, bulleted list with check icons. Use for definitions, properties, lists.
- Fields: `section_label`, `title`, `subtitle`, `bullets[]` (each bullet has `text` and optional `bold_lead`).

### `content_two_column`
Bullets on the left, figure on the right (or vice versa). Use for "concept + diagram" pairs.
- Fields: `section_label`, `title`, `subtitle`, `bullets[]`, `figure` (path + alt + caption).

### `content_grid`
Card grid (2x2 or 2x3) for comparing options or showing parallel concepts. Use for form factors, modes, variants.
- Fields: `section_label`, `title`, `subtitle`, `cards[]` (each card has `title`, `body`, optional `icon`).

### `content_table`
A real HTML table for specs, pinouts, dimensions, values. Use sparingly — tables are dense.
- Fields: `section_label`, `title`, `subtitle`, `columns[]`, `rows[]` (each row is an array).

### `content_diagram`
Slide built around a single large figure with a one-paragraph caption underneath. Use when the figure carries the entire message (e.g., airflow diagrams).
- Fields: `section_label`, `title`, `figure`, `caption`.

### `takeaways`
4-6 check-iconed summary bullets. Put it immediately before the knowledge check when a module includes one.
- Fields: `title`, `items[]`.
- The renderer label is already `Key Takeaways`; use a distinct title such as `Module 2 Summary`, not `Key Takeaways`.

### `knowledge_check`
Multiple-choice knowledge check shown immediately before the final module slide. Use exactly two questions that can be answered from the slide text, narration, figures, or tooltips in the same module: first a single-answer radio question, then a multi-select checkbox question.
- Fields: `title`, `subtitle`, `questions[]`.
- Question 1: omit `multiple` or set it to `false`; use one correct choice and answer-specific `feedback_incorrect` on each incorrect choice.
- Question 2: set `multiple: true`; use two or more correct choices when the content supports it, and keep incorrect feedback at the question level because there are too many possible wrong answer combinations.
- Each question: `id`, `prompt`, optional `multiple: true`, `choices[]`, `feedback_correct`, `feedback_incorrect`.
- Each choice: `id`, `text`, `correct: true|false`.
- The renderer requires one submit attempt on both questions before advancing, shows feedback, allows retry, and lets the learner continue even when answers are incorrect.

### `up_next`
End-of-module slide. The last slide of every module *except* the final one. It shows a "Module N Complete" badge, introduces the next module by number/title, places a pulsing round double-arrow link beside the visible "Module N" heading, then thanks the learner for finishing the module by name. Don't leave it as a bare next-module teaser — the example reference course made that slide feel blank, and learners deserve acknowledgement.
- Fields: `next_module_number`, `next_module_title`, optional `thank_you_message` (overrides the auto-generated "Thank you for completing Module N: <title>.").

### `course_complete`
Replaces `up_next` on the final module's final slide. Thanks the learner for finishing the final module AND wraps the whole course — these are two distinct beats, not one. The renderer shows the per-module completion badge, the per-module thank-you, then a "Course Complete" headline with the course title and a closing message, then an "All Modules Complete" badge.
- Fields: `course_title` (defaults to the course-level title), `cert_message` (the closing line; defaults to a sensible wrap-up), optional `thank_you_message` (per-module thanks override).

## Animation

All slides use `.animate-in` to fade their content in on slide change. The template handles this; you don't need to opt in or out per slide.

## Figures inside slides

Figures should live in `figures/` and be referenced by relative path:
```
figure: { path: "figures/airflow_diagram.png", alt: "...", caption: "..." }
```
Captions render below the figure in muted text. Alt text is required for accessibility. Figures render inside clickable zoom panels by default; do not add separate "click to zoom" instructional text on the slide.

For inline SVG figures, make labels fit inside their shapes. Center text in boxes when the layout is symmetrical, wrap long labels with `<tspan>` lines, or widen the box or pill. Do not leave text spilling outside the drawn shape.

Before delivery, visually check every diagram:
- Arrowheads are visible, proportional, and attached to real lines.
- Arrowhead color matches the line color. Do not reuse a blue/default marker on green, orange, warning, or other colored paths.
- Curved or diagonal arrow lines flow into the center of the flat back side of the arrowhead. If the visible line connects to the point of the arrowhead, redraw it; explicit arrowhead polygons are preferred for these arrows.
- Arrowhead points stop on the target object's boundary line. Do not let the point extend into the box, card, callout, connector, or object it is pointing to.
- Lines connect cleanly without awkward kinks at the arrowhead, and the final path tangent is aligned with the arrowhead centerline.
- Labels do not overlap lines, arrowheads, bubbles, or bounding boxes.
- Repeated objects are centered as a group.
- Long labels are centered to the diagram when they describe the whole figure, or wrapped/placed outside the flow when they describe a side callout.
- Run `scripts/check_svg_arrows.py course.json --fail-on-flags` as part of SVG QA for new or revised diagrams.

## Anti-patterns

- **Don't put narration text on the slide.** The narration plays automatically — duplicating it on screen makes the listener choose which to read. Use the slide for keywords, not paragraphs.
- **Don't invite learners to skip slide 1 narration.** Title-slide hint text should direct learners to press play first, then advance with arrow or Space.
- **Don't exceed 6 bullets per slide.** If you have more, split.
- **Don't mix figure + grid + table on one slide.** Pick one heavy element.
- **Don't write headers on every slide that just say "More info" or "Continued."** Each title should be specific.
- **Don't duplicate the label as the title.** If the small label says `Learning Objectives`, `Key Takeaways`, `Technology Landscape`, or similar, the large slide title must say something more descriptive.
- **Don't add glossary chips for absent terms.** A tooltip belongs only where the term appears in the slide text or narration, preferably the first such slide in the module. Place glossary/reference pills inside the slide content flow, left-aligned below the last text/table/image content; never in a floating "Terms" area near the controls.
- **Don't bury key sources until the end.** If a slide clearly leans on a spec, white paper, video, or project page, add the resource link on that slide.
- **Don't hand-size resource pills as squares.** Use the renderer's flexible pills for learner links so labels like `OCP`, `60`, and `Video` have enough width and never overflow.

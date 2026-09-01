# OCP Academy LMS poster style

Use this reference whenever creating or replacing a course `thumbnail.png`. It defines the maintained high-level catalog treatment used by recent OCP Academy posters. Match the visual family while tailoring the title, badge, supporting line, and technical emblem to the course.

## Required output

- Export an exact 800 x 400 PNG named `thumbnail.png` in the course source folder.
- Design directly for a 2:1 landscape canvas. Do not stretch a different aspect ratio into place.
- Keep the image readable when shown at roughly 400 x 200 and 240 x 120 pixels.
- Use the exact OCP Academy logo from `assets/ocp_academy_white.svg` or an authoritative repository asset. Never ask an image model to redraw or reinterpret the logo.

## Catalog composition

Use the following shared structure unless an existing series poster establishes a more specific maintained variant:

1. A deep navy or indigo full-bleed background.
2. The white OCP Academy logo in the upper-left corner with generous clear space.
3. A compact OCP-green course badge below the logo. Use `OCP` plus a short, recognizable course acronym or topic label in dark navy uppercase text.
4. A large, bold, uppercase white course title in the left text field. Break long titles into balanced lines; preserve clear separation from the emblem.
5. An optional uppercase white subtitle for a meaningful title qualifier, set smaller than the main title.
6. A short OCP-green divider followed by a concise white supporting line near the lower left.
7. A large white circular emblem on the right, outlined in indigo, containing one simplified technical icon or concept illustration.
8. A bright OCP-green angled rail or wedge at the far right, partially behind the circular emblem.
9. Sparse thin circuit, connector, or signal-line accents around the emblem in muted indigo, gray, white, or green.

Aim for roughly 56-60 percent of the canvas for the left text field and 40-44 percent for the emblem field. The title, emblem, and green rail are the dominant elements; accents stay quiet.

## Visual language

- Primary accent: OCP green `#8DC63F`.
- Background family: deep navy and indigo, such as `#1D2258`, `#252A6B`, and `#343A86`.
- Foreground: white, with cool neutral gray for secondary icon structure.
- Typography: Lato Bold or a close geometric sans-serif. Use uppercase for the badge, title, and title qualifier. Letter spacing must remain natural and legible.
- Emblem: flat vector-like geometry with bold, readable forms. Use green for the course's key active element and one restrained secondary accent only when it clarifies the concept.
- Lighting and texture: mostly flat. Very subtle depth inside the emblem is acceptable, but the poster must still read as a branded technical graphic rather than a rendered scene.

Avoid photography, server-room hero images, stock-photo treatment, glossy 3D rendering, complex diagrams, decorative gradients, tiny labels, multiple competing icons, text-heavy emblems, and palettes dominated by purple, orange, beige, or slate.

## Choosing the emblem

Reduce the course to one inspectable visual idea. Good emblems show the central object, mechanism, or relationship rather than attempting to summarize the entire curriculum.

- Prefer a processor, connector, rack element, optical path, power component, cooling loop, storage stack, or other topic-specific object.
- Show motion or flow with a few clear arrows, bubbles, rays, traces, or layered elements.
- Keep every emblem element inside the white circle with comfortable edge clearance.
- Do not include vendor logos or unverifiable technical detail.
- Treat the emblem as symbolic instruction, not as an engineering schematic.

## Reference workflow

When working in the Academy source repository, inspect two or three recent posters before drafting. The maintained family is exemplified by:

- `courses/ocp-solid-state-transformers/thumbnail.png`
- `courses/high-bandwidth-flash/thumbnail.png`
- `courses/short-reach-optical-interconnects-sroi-for-ai-scale-up-fabrics/thumbnail.png`

Use available examples as style and composition references only. Do not carry their topic icon, title, acronym, or supporting copy into another course. If these files are unavailable, follow the written composition above.

For bitmap generation, use the image-generation skill with the available recent posters as referenced images. State each image's role as a style reference. Preserve exact text in the prompt, then inspect the output for spelling and logo accuracy. If generated branding or text is imperfect, retain only the useful visual concept and assemble the logo and typography from authoritative assets rather than accepting a near match.

## Prompt skeleton

```text
Asset type: 800 x 400 OCP Academy LMS course poster, 2:1 landscape.
Style references: recent OCP Academy catalog posters; preserve their high-level composition and visual hierarchy.
Course badge: "<OCP + short acronym>".
Main title, exact text: "<TITLE>".
Optional qualifier, exact text: "<QUALIFIER>".
Supporting line, exact text: "<SHORT LEARNER VALUE>".
Right emblem: <one simplified technical object or mechanism> inside a white indigo-outlined circle.
Composition: white OCP Academy logo upper left; green badge; large white title in the left field; short green divider; supporting line; circular emblem on the right; angled OCP-green rail at the far right; sparse circuit-line accents.
Palette: deep navy and indigo, OCP green #8DC63F, white, cool gray, and at most one restrained topic accent.
Constraints: exact spelling; no clipped text; no overlap between title and emblem; readable at thumbnail size; no vendor logos; no photorealism; no watermark.
```

## Final QA

Before delivery and before committing:

- Confirm PNG format and exactly 800 x 400 pixels.
- Inspect the original-resolution file and a reduced thumbnail preview.
- Verify every word, acronym, and hyphen against the course title and approved terminology.
- Verify the OCP Academy logo is authoritative and undistorted.
- Check that all text stays inside the canvas and does not collide with the emblem.
- Check that the circular emblem and its contents stay clear of the canvas edges.
- Confirm visual alignment with the recent catalog references at a glance.
- Save the final source-repository file as `<course-folder>/thumbnail.png` and run repository course QA.

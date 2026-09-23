# OCP Academy LMS poster style

Use this reference whenever creating or replacing a course `thumbnail.png`. It defines the maintained high-level catalog treatment used by recent OCP Academy posters. Match the visual family while tailoring the title, badge, supporting line, and technical emblem to the course.

## Required output

- Export an exact 800 x 400 PNG named `thumbnail.png` in the course source folder.
- Design directly for a 2:1 landscape canvas. Do not stretch a different aspect ratio into place.
- Keep the image readable when shown at roughly 400 x 200 and 240 x 120 pixels.
- Use the exact OCP Academy logo from `assets/ocp_academy_white.svg` or an authoritative repository asset. Never ask an image model to redraw or reinterpret the logo.

## Catalog composition

Use the following shared structure unless an existing series poster establishes a more specific maintained variant:

1. A full-bleed background with a restrained deep-navy-to-indigo gradient, as in the SST and AICC references.
2. The white OCP Academy logo in the upper-left corner with generous clear space.
3. A compact OCP-green course badge below the logo. Use `OCP` plus a short, recognizable course acronym or topic label in dark navy uppercase text.
4. A large, bold, uppercase white course title in the left text field. Break long titles into balanced lines; preserve clear separation from the emblem.
5. An optional uppercase white subtitle for a meaningful title qualifier, set smaller than the main title.
6. A short OCP-green divider followed by a concise white supporting line near the lower left.
7. A large white circular emblem on the right, outlined in indigo, containing one simplified technical icon or concept illustration. Give the emblem restrained depth through a softly shaded face or edge; an indigo-to-green gradient icon tile is appropriate when it strengthens the topic symbol, as in SST.
8. A bright OCP-green angled rail or wedge at the far right, partially behind the circular emblem, with a gentle green tonal gradient and an adjacent translucent indigo band.
9. Sparse thin arcs, circuit or signal-line segments, and small connector dots around the emblem in muted indigo, gray, white, or green. Keep these clear of the text field.

Aim for roughly 56-60 percent of the canvas for the left text field and 40-44 percent for the emblem field. The title, emblem, and green rail are the dominant elements; accents stay quiet.

## Visual language

- Primary accent: OCP green `#8DC63F`.
- Background family: deep navy and indigo, such as `#1D2258`, `#252A6B`, and `#343A86`.
- Foreground: white, with cool neutral gray for secondary icon structure.
- Typography: Lato Bold or a close geometric sans-serif. Use uppercase for the badge, title, and title qualifier. Letter spacing must remain natural and legible.
- Emblem: crisp vector-like geometry with bold, readable forms. Use green for the course's key active element or gradient tile; a white symbol can provide contrast within a shaded tile. Use one restrained secondary accent only when it clarifies the concept.
- Depth and accents are part of the default catalog style: use visible but restrained tonal gradients in the background and green rail, translucent layering, and a few simple arcs or connector dots. Follow SST and AICC rather than flattening the composition into solid-color blocks. Keep the result a clean branded technical graphic.

Avoid photography, server-room hero images, stock-photo treatment, glossy 3D rendering, complex diagrams, competing multicolor gradients, heavy shadows, tiny labels, multiple competing icons, text-heavy emblems, and palettes dominated by purple, orange, beige, or slate.

## Choosing the emblem

Reduce the course to one inspectable visual idea. Good emblems show the central object, mechanism, or relationship rather than attempting to summarize the entire curriculum.

- Prefer a processor, connector, rack element, optical path, power component, cooling loop, storage stack, or other topic-specific object.
- Show motion or flow with a few clear arrows, bubbles, rays, traces, or layered elements.
- Keep every emblem element inside the white circle with comfortable edge clearance.
- Do not include vendor logos or unverifiable technical detail.
- Treat the emblem as symbolic instruction, not as an engineering schematic.

## Reference workflow

Inspect the SST and AICC style references before drafting. Copies are bundled here so the visual standard remains available outside the source repository:

- [SST poster](posters/sst.png)
- [AICC poster](posters/aicc.png)

When working in the Academy source repository, prefer its newest matching versions. The maintained family is exemplified by:

- `courses/ocp-solid-state-transformers/thumbnail.png`
- `courses/ai-computing-continuum/thumbnail.png`
- `courses/high-bandwidth-flash/thumbnail.png`
- `courses/short-reach-optical-interconnects-sroi-for-ai-scale-up-fabrics/thumbnail.png`

Use these examples as style and composition references only. Do not carry their topic icon, title, acronym, or supporting copy into another course. For an existing editable SVG or HTML/CSS poster, update that source and re-render it so exact typography and brand assets stay reproducible. If the reference images are unavailable, follow the written composition above.

For bitmap generation, use the image-generation skill with the available recent posters as referenced images. State each image's role as a style reference. Preserve exact text in the prompt, then inspect the output for spelling and logo accuracy. If generated branding or text is imperfect, retain only the useful visual concept and assemble the logo and typography from authoritative assets rather than accepting a near match.

## Prompt skeleton

```text
Asset type: 800 x 400 OCP Academy LMS course poster, 2:1 landscape.
Style references: SST and AICC OCP Academy catalog posters; preserve their composition, tonal gradients, translucent layers, simple accents, and visual hierarchy.
Course badge: "<OCP + short acronym>".
Main title, exact text: "<TITLE>".
Optional qualifier, exact text: "<QUALIFIER>".
Supporting line, exact text: "<SHORT LEARNER VALUE>".
Right emblem: <one simplified technical object or mechanism> inside a white indigo-outlined circle.
Composition: navy-to-indigo gradient background; white OCP Academy logo upper left; green badge; large white title in the left field; short green divider; supporting line; softly shaded circular emblem on the right; angled OCP-green gradient rail with a translucent indigo band at the far right; sparse arcs, connector lines and dots around the emblem.
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
- Confirm the tonal gradients and simple accents are present and visible at reduced card size without distracting from the title or topic symbol.
- Save the final source-repository file as `<course-folder>/thumbnail.png` and run repository course QA.

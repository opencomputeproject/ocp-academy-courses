# course.json schema

The wizard maintains a single `course.json` in the working area. It's the source of truth for everything — outline, scripts, figures, manifest. Every render script consumes it.

## Top-level shape

```json
{
  "course_slug": "ocp_nic_3_0_academy",
  "course_title": "OCP NIC 3.0 Academy",
  "course_subtitle": "A Comprehensive Course on the OCP NIC 3.0 Design Specification",
  "tagline": "Community-driven Hyperscale Innovation for All",     // FIXED phrase — never invent; CSS renders all caps
  "spec_version_chip": "Specification v1.6.0 · March 2025",
  "target_duration_minutes": 35,
  "audience_level": "intermediate",
  "brand": {
    "primary_color": "#8DC63F",
    "primary_color_dark": "#6FA030",
    "gray": "#5F6062",
    "course_logo": "OCP-Open-compute-NIC-3-v2-3x-v1-42a.png",
    "academy_logo": "ocp_academy_white.svg",
    "motion_intro_logo": "ocp_academy_white.svg",
    "badge_text": "NIC"
  },
  "motion_intro": {
    "enabled": true,
    "duration_ms": 8000,
    "logo": "ocp_academy_white.svg",
    "index": {
      "enabled": true,
      "eyebrow": "OCP Academy"
    },
    "modules": {
      "enabled": true
    }
  },
  "sources": [
    {"path": "/Users/.../OCP_NIC_3.0_v1.6.0.pdf", "kind": "spec"},
    {"path": "/Users/.../summit_2024_nic_overview.pptx", "kind": "summit_slides"}
  ],
  "modules": [ /* see below */ ]
}
```

For OCP branded text, render `OCP Ready` with a superscript `TM` in learner-facing HTML. Use the `™` glyph in metadata, manifest titles, image alt text, and other plain-text fields where HTML tags are not valid. Do not change source filenames or local source paths to add trademarks.

The optional `brand.badge_text` sets the small label shown under the course logo in each module's top-left badge. Set it to the course's short slug — "NIC", "CDU", "RDMA", etc. — when that's a useful abbreviation. If it is omitted or blank, the renderer leaves the small label out; it does not invent one from the course title.

`brand.course_logo` is required for a polished Academy course. It appears to the right of the OCP Academy logo on `index.html`, above `badge_text` in each module's top-left badge, and as the floating/glowing hero icon on every module title slide. If the user does not provide an asset, generate a simple course-specific SVG mark and place it at the package root. Keep the SVG mark graphical; do not embed acronym text in the logo itself.

## Motion intro shape

The OCP Academy motion intro is **default-on** for both `index.html` and every `moduleN.html`.
It is rendered as a CSS animation overlay, not a pre-rendered MP4, so it adds only one SVG logo
asset and no video-rendering dependency. The default background sweeps diagonally from OCP blue
`#343895` to OCP green `#8DC63F`, using the white OCP Academy SVG lockup.

For the course home, the renderer defaults to:

- eyebrow: `"OCP Academy"`
- title: `course_title`
- subtitle: `course_subtitle`, falling back to the fixed tagline

For module pages, the renderer defaults to:

- eyebrow: `module_badge_text`, falling back to `"Module N"`
- title: `module.title`
- subtitle: `module.subtitle`, falling back to `course_subtitle`

Override only when needed:

```json
{
  "motion_intro": {
    "enabled": true,
    "duration_ms": 8000,
    "logo": "ocp_academy_white.svg",
    "index": {
      "title": "OCP NIC 3.0 Academy",
      "subtitle": "A Comprehensive Course on the OCP NIC 3.0 Design Specification"
    },
    "modules": {
      "enabled": true
    }
  }
}
```

Disable globally with `"motion_intro": {"enabled": false}`. Disable only the course-home intro
with `"motion_intro": {"index": {"enabled": false}}`. Disable module intros with
`"motion_intro": {"modules": {"enabled": false}}`.

## Module shape

```json
{
  "id": 1,
  "slug": "introduction",
  "title": "Introduction to OCP NIC 3.0",
  "subtitle": "Overview, tenets, form factors, capabilities, and the multi-vendor ecosystem.",
  "module_badge_text": "Module 1",
  "motion_intro": {
    "eyebrow": "Module 1",
    "title": "Introduction to OCP NIC 3.0",
    "subtitle": "Overview, tenets, form factors, capabilities, and the multi-vendor ecosystem."
  },
  "next_module_title": "Form Factors & Mechanical Design",
  "slides": [ /* see below */ ]
}
```

The final module's last slide should be `course_complete` instead of `up_next`, and `next_module_title` can be omitted.

## Slide shape

Every slide has:

```json
{
  "id": 1,
  "type": "title|course_overview|objectives|content_bullets|content_two_column|content_grid|content_table|content_diagram|takeaways|knowledge_check|up_next|course_complete",
  "slug": "title",
  "audio": {
    "script_file": "audio/module1/slide_01_title.txt",
    "wav_file":   "audio/module1/slide_01_title.wav",
    "approved": false
  },
  "source_refs": [
    {"source": "OCP_NIC_3.0_v1.6.0.pdf", "page": 12}
  ]
}
```

Plus type-specific fields. See `slide_design_patterns.md` for what each type needs.

Optional learner-aid fields accepted on slides:

```json
{
  "reference_links": [
    {"label": "OCP Rack & Power project", "url": "https://www.opencompute.org/community/rack-and-power"}
  ],
  "resource_callout": {
    "title": "Implementation comparison",
    "text": "Short learner-facing context for why this link is useful.",
    "button_text": "Watch from 12:17",
    "url": "https://youtu.be/example?t=737"
  },
  "term_refs": ["ride_through", "arc_flash"]
}
```

Use `reference_links` for small bottom-of-slide link pills. Use `resource_callout` for a larger learner resource box when the resource deserves more context. These learner aids render inside `.slide-content`, left-aligned, below the slide's last text/table/image element. Do not place them in a separate floating "Terms" region, fixed footer, or control-adjacent panel. Use `term_refs` with a top-level `term_glossary`:

```json
{
  "term_glossary": [
    {
      "id": "arc_flash",
      "term": "Arc flash",
      "tooltip": "Hazard from release of energy caused by an electric arc; it can injure people and damage equipment.",
      "reference_label": "NFPA 70E definition source",
      "url": "https://..."
    }
  ]
}
```

Attach a term to the first substantive slide in each module where it appears in visible text or narration. Do not add tooltips for terms that are absent from both. If a slide has bullets, a table, a figure, or a diagram, place the learner-aid block after that content so the pills read as part of the slide, not as a separate navigation/footer area.

### `title`

```json
{ "type": "title", "title": "Introduction to OCP NIC 3.0", "subtitle": "...", "version_chip": "v1.6.0 · March 2025" }
```

### `course_overview`

```json
{
  "type": "course_overview",
  "title": "Six Modules, One Complete Picture",
  "subtitle": "...",
  "modules_listed": ["Introduction to OCP NIC 3.0", "Form Factors & Mechanical Design", "..."],
  "chips": [
    {"icon": "⏱", "text": "30-40 min total duration"},
    {"icon": "🎓", "text": "Broad OCP community audience"},
    {"icon": "📄", "text": "Based on Spec v1.6.0", "url": "https://www.opencompute.org/documents/..."}
  ]
}
```

Each chip can take an optional `url` — when present, the chip renders as a clickable `<a>` opening in a new tab. Useful for pointing the "Based on Spec vX.Y.Z" chip at the canonical specification PDF.

The optional `media_embed` field accepts either a raw HTML string OR a dict to embed a YouTube teaser below the chips:

```json
{
  "type": "course_overview",
  "...": "...",
  "media_embed": {
    "type": "youtube",
    "id": "bIePDFht0uU",
    "title": "OCP Academy: Liquid Cooling primer (teaser)",
    "label": "Optional Primer Teaser"
  }
}
```

Useful for adding a brief preview video alongside the module roadmap. Falls back gracefully if the LMS blocks iframes — the equivalent chip in `chips[]` should still link to the same URL as a backup.

### `objectives`

```json
{
  "type": "objectives",
  "title": "What You Will Learn",
  "subtitle": "By the end of this module you will…",
  "objectives": [
    "Identify the four OCP NIC 3.0 active form factors and their pin counts.",
    "Explain how the common connector enables a multi-vendor ecosystem.",
    "..."
  ]
}
```

### `content_bullets`

```json
{
  "type": "content_bullets",
  "section_label": "Definition",
  "title": "What is OCP NIC 3.0?",
  "subtitle": "Optional one-line intro.",
  "bullets": [
    {"bold_lead": "Open, standardized", "text": "NIC specification purpose-built for hyperscale data centers."},
    {"bold_lead": "Hot-swappable", "text": "field-replaceable unit (FRU) enabling a multi-vendor ecosystem."}
  ]
}
```

### `content_two_column`

```json
{
  "type": "content_two_column",
  "section_label": "Airflow",
  "title": "Cold and Hot Aisle Cooling",
  "bullets": [ /* same shape as content_bullets */ ],
  "figure": { "path": "figures/cold_aisle_airflow.png", "alt": "Cold aisle airflow", "caption": "Cool air enters the front…" }
}
```

### `content_grid`

```json
{
  "type": "content_grid",
  "section_label": "Form Factors",
  "title": "Four Active Form Factors",
  "grid_cols": 4,
  "cards": [
    {"title": "SFF",  "body": "16 PCIe lanes, 80W envelope, 76mm.",  "icon": "🔲"},
    {"title": "TSFF", "body": "16 PCIe lanes, 80W envelope, tall.",  "icon": "🔲"},
    {"title": "OCP MRC 1.0", "body": "Open RDMA transport spec.", "icon": "📄",
     "url": "https://www.opencompute.org/documents/ocp-mrc-1-0-pdf",
     "link_text": "opencompute.org/documents/ocp-mrc-1-0-pdf"}
  ]
}
```

Optional fields:

- `grid_cols` — pin the column count explicitly. Without it the renderer auto-picks `min(5, card_count)`, which puts a 6-card grid into 5+1. Common values: 3 (for 6-card grids), 2, or 4.
- `cards[].url` — makes a card a clickable `<a>` opening in a new tab.
- `cards[].link_text` — when set together with `url`, renders a short visible URL line in OCP-green underneath the card body. If only `url` is set, the URL itself is shown.

### `content_table`

```json
{
  "type": "content_table",
  "section_label": "Pinout",
  "title": "Primary Connector Pin Allocation",
  "columns": ["Pin range", "Function", "Lanes"],
  "rows": [
    ["A1-A8",   "Power",        "—"],
    ["A9-B16",  "PCIe lanes",   "8"]
  ]
}
```

### `content_diagram`

```json
{
  "type": "content_diagram",
  "section_label": "Mechanical",
  "title": "DSFF Card Assembly",
  "figure": { "path": "figures/dsff_exploded.png", "alt": "DSFF exploded view", "caption": "..." }
}
```

### `takeaways`

```json
{
  "type": "takeaways",
  "title": "Module Summary",
  "items": [
    "The spec defines mechanical, electrical, thermal, and management in one document.",
    "..."
  ]
}
```

### `knowledge_check`

Place one `knowledge_check` slide before the final `up_next` or `course_complete` slide in each module unless the user opts out. The renderer supports single-answer radio questions and multiple-answer checkbox questions. The learner must submit each question once before advancing, but a correct answer is not required; retry remains available after feedback. Choice order is deterministically shuffled by default so authored answer order does not leak into the learner view. For multi-select questions, the renderer also avoids placing every correct answer as a single obvious block at the front or back. Set `"shuffle_choices": false` on a question only when the displayed order is meaningful.

```json
{
  "type": "knowledge_check",
  "title": "Check Your Loop Mental Model",
  "subtitle": "Answer once to continue. Correctness is not required, and you can retry.",
  "questions": [
    {
      "id": "m2_q1",
      "prompt": "Which signal most directly indicates whether purging may be required?",
      "shuffle_choices": true,
      "choices": [
        {"id": "a", "text": "Actual vapor pressure versus theoretical vapor pressure", "correct": true},
        {"id": "b", "text": "The rack nameplate power", "correct": false},
        {"id": "c", "text": "The outside-air temperature alone", "correct": false}
      ],
      "feedback_correct": "Correct. Pressure behavior can indicate non-condensables or another anomaly.",
      "feedback_incorrect": "Review the monitoring threshold. The key comparison is actual vapor pressure against the theoretical value for the boiling temperature."
    },
    {
      "id": "m2_q2",
      "multiple": true,
      "prompt": "Which items belong in a fluid compatibility review?",
      "choices": [
        {"id": "a", "text": "Seals and quick disconnects", "correct": true},
        {"id": "b", "text": "Cold plate wetted metals", "correct": true},
        {"id": "c", "text": "Only the fluid brand name", "correct": false}
      ],
      "feedback_correct": "Correct. Compatibility is a system material decision.",
      "feedback_incorrect": "Include the exact fluid and the exact wetted materials, not only a generic fluid label."
    }
  ]
}
```

### `up_next`

The end-of-module slide on every module *except* the final one. Carries the "Module N Complete" badge, a per-module thank-you line, and the next-module teaser. The renderer places a pulsing round double-arrow link beside the visible "Module N" heading, pointing to `moduleN.html` for the next module. The `thank_you_message` is optional — if omitted, the renderer auto-generates "Thank you for completing Module N: <module title>."

```json
{
  "type": "up_next",
  "next_module_number": 2,
  "next_module_title": "Form Factors & Mechanical Design",
  "thank_you_message": "Nice work — you've finished Module 1: Introduction to OCP NIC 3.0."
}
```

### `course_complete`

The end-of-final-module slide. Two beats: thanks the learner for finishing the final module AND wraps up the whole course. Both messages have sensible auto-defaults if omitted.

Optionally add a `survey` object to attach a feedback CTA card below the "All Modules Complete" badge. The card has a body paragraph and a button that opens the survey URL in a new tab. Omit `survey` entirely to render the slide without any CTA. `button_text` defaults to "Share Feedback".

```json
{
  "type": "course_complete",
  "course_title": "OCP NIC 3.0 Academy",
  "thank_you_message": "Thank you for completing Module 6: Compliance, Ecosystem & Future.",
  "cert_message": "You've completed every module of the OCP NIC 3.0 Academy. We hope this course leaves you ready to put what you've learned into practice.",
  "survey": {
    "body": "Got a couple minutes to help us improve? Help us shape improvements and our future courses by sharing your feedback with the course development team. We periodically select submitters at random for great giveaways!",
    "button_text": "Share Feedback",
    "url": "https://forms.gle/..."
  }
}
```

## Figure shape (when referenced by a slide)

```json
{
  "path": "figures/airflow.png",       // relative to package root
  "alt": "Airflow diagram",
  "caption": "Cool air enters the front…",
  "source": "reuse" | "ai_generated" | "svg_inline",
  "extract_from": { "source": "summit_2024.pdf", "page": 17 },   // if reuse
  "generate_prompt": "A clean, flat vector illustration…"        // if ai_generated
}
```

`extract_figures.py` reads `extract_from`. The image-gen step reads `generate_prompt`. The renderer just embeds `path`, `alt`, `caption` into the HTML.

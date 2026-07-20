# course.json schema

The wizard maintains a single `course.json` in the working area. It's the source of truth for everything — outline, scripts, figures, manifest. Every render script consumes it.

## Top-level shape

```json
{
  "style": "Slides",
  "course_slug": "ocp_academy_nic_3_0",
  "course_title": "OCP Academy: NIC 3.0",
  "language": "en-US",
  "scorm_title": "Optional exact manifest-only title override",
  "metadata_language_name": "Optional language label for the manifest suffix",
  "narration": {
    "engine": "elevenlabs",
    "voice_id": "Course-specific ElevenLabs voice ID",
    "voice_name": "Human-readable voice name"
  },
  "course_subtitle": "A Comprehensive Course on the OCP NIC 3.0 Design Specification",
  "tagline": "Community-driven Hyperscale Innovation for All",     // FIXED phrase — never invent; CSS renders all caps
  "spec_version_chip": "Specification v1.6.0 · March 2025",
  "index_footer_line": "Optional exact footer line for the course home page.",
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

`course_title` is learner-facing and appears inside the rendered course.
`language` is a BCP 47 tag. English packages use `course_title` unchanged in
`imsmanifest.xml`; non-English packages append the English language name in
parentheses, such as `OCP ESUN (Korean)`. Use `scorm_title` only for an exact
manifest-only override. Use `metadata_language_name` to override the automatic
language label without changing course content.

For narrated Slides courses, optional top-level `narration` makes the TTS engine
and voice reproducible. `gen_audio.py` uses this course-specific configuration
before environment defaults; `--engine` and `--voice` remain explicit command
overrides. Maintained locale scaffolds set Korean `Chris - Warm and clear`
(`PDoCXqBQFGsvfO0hNkEs`), Japanese `b34JylakFZPlGS0BnwyY`, Chinese `Lan Chen`
(`bZtjnyJAFD0Cp3lfNG5g`), Brazilian Portuguese `Carla`
(`m151rjrbWXbBqyq56tly`), and Latin American Spanish `Ninoska`
(`zl1Ut8dvwcVSuQSB9XkG`).

## Presentation style

`style` accepts exactly `"Slides"` or `"Scrolling"`. If omitted, renderers assume Slides so existing courses remain compatible.

- Slides uses `modules[].slides[]`, narration, and multiple SCO pages.
- Scrolling uses top-level `lessons[].blocks[]`, a persistent left table of contents, progressive Continue gates, and one `index.html` SCO. Narration is false by default.

### Scrolling top-level shape

```json
{
  "schema_version": "2.0",
  "style": "Scrolling",
  "course_slug": "module-1-the-ocp-origins",
  "course_title": "Module 1: The OCP Origins",
  "course_subtitle": "A concise plain-text description.",
  "course_description_html": "<p>The full learner-facing description.</p>",
  "target_duration_minutes": null,
  "audience_level": "introductory",
  "brand": {
    "primary_color": "#8cc53f",
    "primary_color_dark": "#6fa030",
    "course_logo": "resources/images/module-banner.png"
  },
  "theme": {
    "source_theme": "classic",
    "accent_color": "#8cc53f",
    "sidebar_style": "Light",
    "corner_style": "Rounded",
    "cover_image": "resources/images/cover.jpg",
    "cover_width": 1680,
    "cover_height": 737,
    "cover_overlay": 0,
    "cover_page_type": "full",
    "navigation_type": "sidebar",
    "lesson_header_style": "accent",
    "lesson_header_size": "medium",
    "lesson_header_color": "#8cc53f",
    "lesson_header_hidden": false,
    "button_scheme": "accent",
    "block_padding": 30,
    "animate_block_entrance": true,
    "font_families": {
      "heading": "Be Vietnam",
      "body": "Be Vietnam",
      "ui": "Lato"
    },
    "font_faces": [
      {
        "family": "Be Vietnam",
        "weight": 400,
        "style": "normal",
        "path": "resources/fonts/be-vietnam-regular.woff2"
      }
    ]
  },
  "scrolling": {
    "toc_position": "left",
    "toc_initially_open": true,
    "show_search": true,
    "show_lesson_count": true,
    "show_cover_lesson_list": true,
    "lesson_transition": "directional_vertical",
    "continue_gates": true,
    "narration": false
  },
  "lessons": []
}
```

Each lesson has sequential `id`, stable `slug`, learner-facing `title`, optional `description_html`, and ordered `blocks`. Supported block types are `text`, `list`, `image`, `video`, `attachment`, `divider`, `continue`, `quote`, `buttons`, `accordion`, `tabs`, `process`, `labeled_graphic`, `flashcards`, and `knowledge_check`. A Scrolling `process` block is rendered as a numbered, one-step-at-a-time carousel; each item may include a title, `description_html`, and media. Store course-owned binary media under `resources/images`, `resources/videos`, `resources/captions`, or `resources/documents` and reference those paths from block `media` objects. Blocks may set `style.entrance_animation`; false keeps that block static even when `theme.animate_block_entrance` is enabled.

Quote blocks may include structured `avatar` media. Classic quote variant `d` renders that image as an 80px circle beside transparent quote content on the block's own background; retain its responsive width and authored typography instead of substituting a generic callout card. Scrolling videos use the maintained custom player: transparent letterboxing, a centered 98px play circle, no browser-native controls before activation, and the configured control order after activation—play/pause, seek/loaded progress, remaining time, seven-choice speed menu, caption-language menu, picture-in-picture, fullscreen, and expandable volume. Use the canonical Video.js-compatible glyph outlines rather than substitute art. Scrolling accordions use right-aligned plus/minus controls rather than native disclosure triangles; light block surfaces render adjoining bordered white cards with a 4px accent rule on expanded content, while dark surfaces retain the configured borderless treatment.

A captioned video declares editable VTT resources in `media.captions[]`:

```json
{
  "type": "video",
  "media": {
    "path": "resources/videos/origin-story.mp4",
    "poster": "resources/images/origin-story.jpg",
    "captions": [
      {"path": "resources/captions/origin-story.en-US.vtt", "language": "en-US", "label": "English (US)"},
      {"path": "resources/captions/origin-story.fr.vtt", "language": "fr", "label": "Français"}
    ]
  }
}
```

The renderer parses those files into generated cue fallback data so CC works from `file://` as well as an LMS, but `course.json` retains only the VTT paths and language metadata. Add translated subtitle tracks as additional VTT entries; never duplicate or hard-code cues in course authoring data.

Every `continue` block has a `label` and optional `complete_hint`. It reveals following blocks until the next Continue gate. A nearby `knowledge_check` does not disable Continue; progression may happen before or after answering it. The final gate completes that lesson and immediately opens the next lesson. Revisiting a completed lesson hides its Continue controls and shows a full-pane 61px gray bar linking to the next lesson; do not add a separate generic Next Lesson button. A final `buttons` item with `type: "exit-course"` completes its zero-gate lesson only when the learner clicks Exit; entering that lesson must not mark it complete or expose a completion message. Completing every lesson completes the single SCO.

`show_cover_lesson_list` defaults to true and renders the ordered lesson overview below the cover's lesson count. The classic centered cover title uses responsive sizes: 32px/38px by default, 45px/52px from 480px, 60px/70px from 992px, and 80px/90px from 1440px. `lesson_transition` accepts `"directional_vertical"` (default) or `"none"`; the default brings later lessons in from below and earlier lessons in from above while respecting reduced-motion preferences. The desktop lesson pane is a viewport-height scrolling region. Each lesson includes a 61px gray previous-navigation strip above its hero (`Home` for lesson 1), and lesson entry starts at a 62px pane offset so scrolling upward reveals that strip. Preserve the configured lesson-header grid, including its 160px by 5px post-title rule, two-pixel white separation before the first body block, and wide-screen 950px-grid cap; at a 1440px viewport its inner header is 761.667px rather than a percentage that keeps growing. The desktop TOC is 280px wide; lesson rows use bold 13px/16px text, 18px 41px 18px 43px padding, 52px height for one-line titles, natural 68px height for two-line titles, and a `#f3f3f3` active fill. A completed row uses the canonical 30px status wrapper with an inset 20px, 16-unit progress-circle SVG and check path. Scrolling block backgrounds span the lesson pane, but their inner content widths are type-specific: do not apply one global side margin to text, lists, media, interactions, and Continue controls. Full-width cropped images have a 200px minimum height and retain enough intrinsic height to avoid clipping an image taller than that threshold. Text-aside blocks use the maintained content width, medium videos cap at 1100px on wide screens, and dividers retain the 920px content-box cap, responsive padding, and negative 8.333% line margins on wide panes.

When `theme.animate_block_entrance` is true, observe eligible blocks as they enter the viewport. Text-aside media fades and moves 50px from its outside edge over 1 second after a 0.12-second delay. List items use the same horizontal entrance staggered by 0.25 seconds. Full media, videos, and Continue controls fade without translation. Honor reduced motion. `show_search` provides submit-on-Enter full-course content search with lesson-grouped occurrence counts, not live title filtering.

The `theme` object is authoritative learner-facing source. Preserve the configured cover (including dimensions and overlay), typography through local `font_faces`, navigation and lesson-header treatment, button scheme, block padding, and animation preference. The renderer must reproduce that presentation using readable AcademyWizard HTML/CSS rather than replacing the authored design with generic defaults. Omitted values use the maintained Scrolling defaults.

Render classic Scrolling heading and heading-paragraph blocks with a bold 32px/40px heading line box and 8px vertical padding. If `heading_html` contains an author-sized `font-size: 2rem` span, retain bold inheritance but give that span a 20px/25px line box; do not style it as regular body text.

Classic Scrolling interactions retain their authored geometry. Numbered lists use 40px accent-green number circles and a 100px gap to the text column; at a 1440px viewport the item and text widths are 760px and 660px. Description-style flashcards omit placeholder media, render as 252px white cards, use the canonical 36px top-right control and SVG icon, and flip to a `#fafafa` text back. A three-card group stays in one row with 28px gaps on wide screens. Accordion headers use the maintained 715.828px medium width and expand to the 761.667px wide-grid cap, with 30px padding, 18px/25.2px bold type, and 87px header height. Process interactions use an 830px card at 1440px, horizontal 0.5-second directional transitions, and 56px circular chevrons. Description button blocks use a centered 620px row with a 450px description column (80px right padding) and a 170px by 40px pill button; do not stack the text and button on desktop. Knowledge checks use a 760px white card with 64px/56px padding, 646px answer rows, a 20px radio ring with centered 6px selected dot, and configured submitted feedback. Submission disables the choices and hides Submit; correct/incorrect answer glyphs replace the selected dot, feedback fades from scale 1.1 after the configured delay, incorrect feedback offers Take Again, and correct feedback does not.

For OCP branded text, render `OCP Ready` with a superscript `TM` in learner-facing HTML. Use the `™` glyph in metadata, manifest titles, image alt text, and other plain-text fields where HTML tags are not valid. Do not change source filenames or local source paths to add trademarks.

The optional `brand.badge_text` sets the small label shown under the course logo in each module's top-left badge. Set it to the course's short slug — "NIC", "CDU", "RDMA", etc. — when that's a useful abbreviation. If it is omitted or blank, the renderer leaves the small label out; it does not invent one from the course title.

`brand.course_logo` is required for a polished OCP Academy course. It appears to the right of the OCP Academy logo on `index.html`, above `badge_text` in each module's top-left badge, and as the floating/glowing hero icon on every module title slide. If the user does not provide an asset, generate a simple course-specific SVG mark and place it at the package root. Keep the SVG mark graphical; do not embed acronym text in the logo itself.

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
      "title": "OCP Academy: NIC 3.0",
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

For narrated Slides modules, slide 1 audio starts during module-page initialization and runs independently of this overlay. Do not delay narration until the motion intro ends. When browser autoplay policy blocks audible playback, retain the loaded clip and retry on the learner's first pointer, touch, or keyboard interaction while pulsing the play control as the fallback cue.

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
  "type": "title|course_overview|objectives|content_bullets|content_two_column|content_grid|content_table|content_diagram|full_slide_image|takeaways|knowledge_check|up_next|course_complete",
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

`knowledge_check` slides are always narrated. They must include the same `audio.script_file` and `audio.wav_file` fields as content slides, and the corresponding script/WAV must be generated before rendering a module. `course_complete` may remain silent unless the approved design says otherwise.

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

Use `reference_links` for small bottom-of-slide link pills. Every resource pill opens in a new tab and includes the inline external-page icon on its right edge. Use `resource_callout` for a larger learner resource box when the resource deserves more context. Use `term_refs` for tooltip-only glossary pills; they include the inline terminology/book icon on the right and never become links, even when the glossary metadata retains a source URL for authoring or audit purposes. These learner aids render inside `.slide-content`, left-aligned, below the slide's last text/table/image element. The one alignment exception is the final module's final `course_complete` slide, where its resource strip is centered. Do not place learner aids in a separate floating "Terms" region, fixed footer, or control-adjacent panel. Use `term_refs` with a top-level `term_glossary`:

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
  "mobile_scroll": true,
  "bullets": [
    {"bold_lead": "Open, standardized", "text": "NIC specification purpose-built for hyperscale data centers."},
    {"bold_lead": "Hot-swappable", "text": "field-replaceable unit (FRU) enabling a multi-vendor ecosystem."}
  ]
}
```

Set `mobile_scroll` only when a content-heavy slide cannot fit above the fixed
controls on a narrow viewport. It keeps desktop layout unchanged and top-aligns
the slide below the module badge with vertical scrolling on mobile.

### `content_two_column`

```json
{
  "type": "content_two_column",
  "section_label": "Airflow",
  "title": "Cold and Hot Aisle Cooling",
  "bullets": [ /* same shape as content_bullets */ ],
  "compact_table": {
    "title": "Optional compact comparison",
    "columns": ["Material", "Index", "Speed"],
    "rows": [["Air", "1.00", "3.0 x 10^8 m/s"]]
  },
  "figure": { "path": "figures/cold_aisle_airflow.png", "alt": "Cold aisle airflow", "caption": "Cool air enters the front…" }
}
```

`compact_table` is optional. Use it below the bullet list when a short source table
fills otherwise unused space in the text column and directly supports the figure.
Keep it to a few columns and rows; the renderer makes these slides vertically
scrollable on small screens so the table and figure remain accessible.

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
    {"title": "Baseline", "body": "Current operating model.", "tone": "blue"},
    {"title": "Constraint", "body": "Design limit or risk to manage.", "tone": "amber"},
    {"title": "OCP MRC 1.0", "body": "Open RDMA transport spec.", "icon": "📄",
     "url": "https://www.opencompute.org/documents/ocp-mrc-1-0-pdf",
     "link_text": "opencompute.org/documents/ocp-mrc-1-0-pdf"}
  ]
}
```

Optional fields:

- `grid_cols` — pin the column count explicitly. Without it the renderer auto-picks `min(5, card_count)`, which puts a 6-card grid into 5+1. Common values: 3 (for 6-card grids), 2, or 4.
- `cards[].tone` — optional visual tone for a card. Use it when cards intentionally contrast distinct ideas, sides, states, risks, priorities, or categories. Leave it out for a normal collection of related concepts. Supported tones and aliases: `blue`/`baseline`/`traditional`, `green`/`accent`/`positive`/`ai`, `slate`/`neutral`/`context`, `amber`/`warning`/`tradeoff`, and `red`/`risk`/`constraint`. Tones are theme-aware in the renderer; do not hard-code tone colors in slide content.
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

### `full_slide_image`

Use this for a narrated source image that should occupy the slide without an added title, caption, section label, or learner-facing text.

```json
{
  "type": "full_slide_image",
  "slug": "source_image_context",
  "figure": {
    "path": "figures/source_slide_09.png",
    "alt": "Source slide image showing fiber-count growth across front-end and back-end network generations."
  },
  "audio": {
    "script_file": "audio/module1/slide_06_source_image_context.txt",
    "wav_file": "audio/module1/slide_06_source_image_context.wav"
  }
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

Place one `knowledge_check` slide before the final `up_next` or `course_complete` slide in each module unless the user opts out. Treat it as a narrated interaction slide, not a silent quiz: add a concise orientation script and the matching `audio` block. Each knowledge check must contain exactly two questions: question 1 is a single-answer radio question that checks the core concept, and question 2 is a multi-select checkbox question that asks learners to apply, classify, or compare that concept. The learner must submit both questions once before advancing, but correct answers are not required; retry remains available after feedback. Choice order is deterministically shuffled by default so authored answer order does not leak into the learner view. For multi-select questions, the renderer also avoids placing every correct answer as a single obvious block at the front or back. Set `"shuffle_choices": false` on a question only when the displayed order is meaningful.

For the single-answer radio question, put `feedback_incorrect` on each incorrect choice when possible. The rendered feedback should explain why that selected answer is wrong compared with the correct concept. Keep the question-level `feedback_incorrect` as a fallback for older renderers or unspecified choices. For the multi-select question, use the question-level `feedback_incorrect`; do not try to author separate feedback for every possible wrong combination.

```json
{
  "type": "knowledge_check",
  "title": "Check Your Loop Mental Model",
  "subtitle": "Answer once to continue. Correctness is not required, and you can retry.",
  "audio": {
    "script_file": "audio/module2/slide_09_knowledge_check.txt",
    "wav_file": "audio/module2/slide_09_knowledge_check.wav",
    "approved": true
  },
  "questions": [
    {
      "id": "m2_q1",
      "prompt": "Which signal most directly indicates whether purging may be required?",
      "shuffle_choices": true,
      "choices": [
        {"id": "a", "text": "Actual vapor pressure versus theoretical vapor pressure", "correct": true},
        {
          "id": "b",
          "text": "The rack nameplate power",
          "correct": false,
          "feedback_incorrect": "Rack power may shape cooling demand, but it does not reveal whether vapor pressure is drifting from the expected value."
        },
        {
          "id": "c",
          "text": "The outside-air temperature alone",
          "correct": false,
          "feedback_incorrect": "Outside-air temperature is too indirect. The monitoring signal is the actual vapor pressure compared with the theoretical value."
        }
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

The end-of-final-module slide. Two beats: thanks the learner for finishing the final module AND wraps up the whole course. Both messages have sensible auto-defaults if omitted. Add useful `reference_links` as the learner's continuing resources; the renderer centers that resource strip with the rest of the completion content. Do not add a redundant "All Modules Complete" badge below the course-complete message.

Optionally add a `survey` object to attach a feedback CTA card below the centered resources. The card has a body paragraph and a button that opens the survey URL in a new tab. Omit `survey` entirely to render the slide without any CTA. `button_text` defaults to "Share Feedback".

```json
{
  "type": "course_complete",
  "course_title": "OCP Academy: NIC 3.0",
  "thank_you_message": "Thank you for completing Module 6: Compliance, Ecosystem & Future.",
  "cert_message": "You've completed every module of the OCP Academy NIC 3.0 course. We hope this course leaves you ready to put what you've learned into practice.",
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

For local video or animation clips, use the same `figure` field and set the media path to an
MP4, WebM, MOV, or M4V file:

```json
{
  "path": "figures/expanded_beam_dust_compare.mp4",
  "media_type": "video",
  "poster": "figures/expanded_beam_dust_compare_frame.png",
  "alt": "Silent animation comparing dust impact on physical-contact and expanded-beam connectors.",
  "caption": "Expanded beam spreads the optical spot so the same contaminant blocks less of the path.",
  "source": "custom",
  "autoplay": true,
  "loop": true,
  "muted": true
}
```

`extract_figures.py` reads `extract_from`. The image-gen step reads `generate_prompt`.
The renderer embeds image figures as zoomable images and embeds video figures with hover/focus
Play/Pause and Zoom controls. `render_index.py` lists both the video and `poster` in the SCORM
manifest.

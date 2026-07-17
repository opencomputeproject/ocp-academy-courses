# Translating Slides courses

Use this workflow when an approved narrated Slides course needs one or more
language editions. Keep the original course immutable and build every locale as
an independent SCORM package.

## Contents

1. Source and folder convention
2. Scaffold a locale
3. Translation rules
4. Narration and media
5. Metadata and final resources
6. Review, validation, and delivery

## Source and folder convention

Keep the existing English course at the course root for backward compatibility.
Treat its `course.json`, structure, source references, and technical facts as the
canonical source. Put each translation under a BCP 47 locale tag:

```text
courses/<course-slug>/
├── course.json                    # canonical English source
├── audio/                         # English scripts; WAVs stay uncommitted
├── figures/                       # English/shared figures
├── animations/                    # optional editable animation sources
├── <course-logo>.svg
└── locales/
    ├── ko-KR/
    │   ├── course.json            # complete Korean authoring source
    │   ├── audio/module1/         # Korean narration scripts
    │   ├── figures/               # copied neutral + localized figures
    │   ├── animations/            # localized animation sources when needed
    │   └── <course-logo>.svg
    ├── fr-FR/
    └── ja-JP/
```

Do not commit generated WAVs, HTML, manifests, or ZIPs. Keep builds separate:

```text
build/<course-slug>/
├── en-US/<package-folder>/
├── ko-KR/<package-folder>/
└── fr-FR/<package-folder>/
```

This is intentionally a full locale source branch, not a generated HTML copy.
It keeps each language independently editable and packageable while leaving the
English source untouched.

## Scaffold a locale

Run:

```bash
python scripts/scaffold_slides_translation.py \
  courses/<course-slug>/course.json ko-KR \
  --language-name Korean
```

The scaffold:

- refuses to overwrite a non-empty locale;
- copies figures, animations, and referenced brand assets;
- preserves module, slide, quiz, glossary, source-reference, and URL structure;
- sets `language` and a locale-specific `course_slug`;
- applies any maintained locale narration default to top-level `narration`;
- records the source path and SHA-256 under `localization`;
- creates empty locale narration folders; and
- resets every narration approval to `false`.

Use `--output-dir` only when the repository has a different convention. Use
`--scorm-title` only when the automatic manifest title is unsuitable.

## Translation rules

Translate every learner-facing string, including:

- course, module, and slide titles and subtitles;
- labels, bullets, cards, tables, captions, alt text, and inline SVG text;
- knowledge-check prompts, choices, feedback, retry/gate text, and completion text;
- glossary terms, definitions, and learner-facing reference labels;
- `ui_labels`, narration hints, accessibility labels, and survey copy; and
- resource-pill labels while preserving their authoritative URLs.

Keep structure and identity stable: module IDs, slide IDs/types, question IDs,
choice IDs/correctness, glossary IDs, source references, URLs, numeric values,
standards, versions, and technical requirements must match the canonical course.

Do not translate technology acronyms word-for-word. Keep `OCP` and other
standard Latin-letter forms such as `ESUN`, `CPU`, `AI`, `GPU`, `PFC`, and `ECN`
in visible text and TTS scripts unless an approved glossary explicitly requires
another convention.
Let the selected native-language voice pronounce those letters with its natural
accent. Translate the explanation around the acronym.

Keep `course_title` learner-facing. Do not add a language suffix inside the
course. The manifest renderer automatically changes a non-English LMS title to
`<course_title> (<English language name>)`; for example, `OCP ESUN (Korean)`.

## Narration and media

Write new scripts for every narrated slide. Never reuse English WAVs. Use one
approved voice, model, and speed consistently across the locale. Keep a narrated
knowledge check narrated, and preserve final-slide narration when the approved
course design includes it.

For every Korean locale (`ko` and its regional variants), use ElevenLabs
`Chris - Warm and clear`, voice ID `PDoCXqBQFGsvfO0hNkEs`. The translation
scaffold records this under top-level `narration`, and `gen_audio.py` honors that
course-specific engine and voice automatically. Do not substitute another voice
unless the user explicitly selects one; use `--voice` for an intentional
one-time override.

After editorial approval, synthesize the locale audio and run
`audio_tail_report.py --fail-on-flags`. Regenerate only flagged clips. Do not
render or package after a required knowledge-check audio failure.

Classify every visual:

- copy language-neutral diagrams unchanged;
- translate labels, legends, axes, captions, posters, and alt text on
  text-bearing visuals;
- rebuild animations or videos when visible text changes; and
- retain technical symbols, dimensions, and acronym spelling exactly.

Run the SVG arrow check before encoding localized animation video.

## Metadata and final resources

Set a valid BCP 47 `language` such as `ko-KR`, `fr-FR`, or `ja-JP`. Use
`metadata_language_name` only to override the automatic English language label.
Use `scorm_title` only for an exact manifest-only title override.

The final slide of the final module must repeat the course's key continuing
resources as centered `reference_links` pills above the Share Feedback block.
Localize only the pill labels. Keep the authoritative URLs, external-link icons,
new-tab behavior, and resource order consistent across languages.

## Review, validation, and delivery

Review a locale in this order:

1. technical facts and acronym policy;
2. complete learner-facing text and UI localization;
3. narration script approval and voice consistency;
4. localized media and accessibility text;
5. quiz behavior, completion tracking, and final resource pills;
6. desktop and narrow mobile layouts, including scroll-safe tall slides;
7. audio-tail, package, manifest, and ZIP integrity checks.

Render and validate each locale independently. The strict ZIP must contain only
manifest-declared runtime files. Confirm that the manifest title contains the
language suffix, the visible HTML title does not, and the canonical English
source hashes remain unchanged throughout the translation build.

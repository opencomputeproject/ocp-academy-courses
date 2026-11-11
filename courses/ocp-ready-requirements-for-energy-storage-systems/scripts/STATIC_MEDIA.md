# ESS Static Figures

Scope: 11 editable SVGs in each of eight editions. The six original PNGs remain
untouched as source references. No course metadata, animations, video/poster, or
audio files are modified by these tools.

## Rebuild And Inspect

From this course directory:

```sh
node scripts/build_static_figures.mjs --output /tmp/ess-static-review
```

The local Playwright package is used, with no network or paid service. Set
`PLAYWRIGHT_MODULE` to another installed Playwright package path if needed.
The builder measures text in Chromium, wraps it with locale-aware segmentation,
checks 0.75em clearance, and renders native-size, 1000px, and 390px PNG evidence.
Phone contact sheets and an **unreviewed** `candidates.json` go outside the repo.
For a targeted revision, preserve other editions and merge one newly rendered
candidate into the existing external candidate file:

```sh
node scripts/build_static_figures.mjs --locale es-419 --figure m3_evidence_chain
```

Approved language-audit corrections live in `static_language_fixes.json` and
are applied before measuring and wrapping labels. Rebuild only its listed assets
with `node scripts/build_static_figures.mjs --corrections-only`. Any additional
recommendations must be added explicitly, regenerated, and visually reviewed
before changing the accepted inventory. QA files remain outside the repository.
Successive corrections are resolved in order to their final phrase, retaining
each review step in provenance. Physical-row wording is corrected with explicit
whole phrases rather than a global replacement of electrical-line terminology.
The correction source also records overlaps between the language audits. Existing
approved CN/TW regional terms are retained when a later recommendation is an
equivalent wording rather than a new semantic repair. Animation recommendations
are excluded from this static source.

`static_labels.mjs` contains faithful translations of the six source PNGs.
`static_inline_text.json` preserves the original five inline diagrams' text so
the assets remain regenerable after integration removes `figure.svg`.
The builder documents reversible encoding repairs and substitutions taken
verbatim from the same slide's existing learner text, plus explicit user-approved
semantic corrections in `INLINE_CORRECTIONS`. It does not rewrite that
learner text. Numeric values, standards, hierarchy, storage modes, and schematic
branches are retained. White-paper pages 26-27 restore the cropped location
legend; page 44 confirms matrix rows 2.3-A through 2.3-E. Empty row 2.3-F is not
an authored requirement and is omitted. Presentation headings, duplicate labels,
logos, credits, and branded footers are not teaching-diagram content.

## Review Inventory

Inspect every native render and the scaled renders before accepting candidates.
An approval file must name a reviewer and method, bind the SHA-256 of the exact
candidate manifest in `candidates_sha256`, and explicitly list every accepted key
in `accepted_keys` (for example, `en-US/M1S5`). Optional `notes` are retained.
Do not create an approval from text extraction alone.

```sh
node scripts/finalize_static_review.mjs \
  /tmp/ess-static-review/candidates.json \
  /tmp/ess_static_visual_approval.json \
  /tmp/ess_static_media_manifest.json
```

The finalizer rejects unapproved, changed, or text-invalid assets. Static
`text_inventory.entries` contain distinct visible phrases without `at_seconds`,
and `sha256` binds the exact reviewed SVG, matching `glossary_audit.py` and
`course_schema.md`. A hash proves freshness, not visual correctness.

The main integrator merges each manifest `figure` object, removes `figure.svg`,
and retains the localized alt text and caption. `source: custom` makes the new
SVG file authoritative. Review actual course pages after that integration;
standalone asset checks do not validate the player or caption layout. Dense
source schematics and tables require the course's enlarged-media view on phones.

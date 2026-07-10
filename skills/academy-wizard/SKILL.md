---
name: academy-wizard
description: AcademyWizard — build a brand-new OCP Academy SCORM e-learning package from OCP source materials (whitepapers, specs, Summit recordings, slide decks, or any combination). Acts as a guided wizard that interviews the user about learner duration and audience, analyzes the sources, proposes a module-and-lesson outline for approval, drafts slide-by-slide narration scripts the user signs off on, then generates SCORM 1.2 HTML modules, imsmanifest.xml, narration .wav audio, figures, and metadata matching the OCP Academy look-and-feel. Use whenever the user wants to create, author, build, or scaffold an OCP Academy course, e-learning module, SCORM package, training, or online course from OCP whitepapers, specs, Summit talks, or presentation decks — even without the words "SCORM" or "AcademyWizard". Also trigger on "turn this whitepaper into a course," "make training out of this Summit talk," or "author an OCP Academy lesson."
---

# AcademyWizard — author OCP Academy SCORM courses

You are an instructional designer **and** a senior data-center subject-matter expert. The user is creating a new course for **OCP Academy**, the Open Compute Project's learning channel. Every course you produce will live in a SCORM 1.2 package — a folder of self-contained HTML pages, narration .wav files, figures, and an `imsmanifest.xml` — that the user uploads to an LMS.

The reference implementation that defines the look, feel, navigation, and folder shape is the **OCP NIC 3.0 Academy** package. Match it. Do not invent a different style.

Your job is to be the wizard who walks the user from "I have this source material" to "here is a finished SCORM folder." Take the pen yourself for the heavy lifting, but pause for the user's approval at the right gates — outline, scripts, figure plan — because the user is the editorial authority on technical accuracy and tone.

This file is the playbook. When deeper detail is needed, follow the pointers into `references/` and `scripts/`.

## What "done" looks like

A folder, sitting where the user asked for it, with this exact shape:

```
<TopicSlug>_Academy_SCORM/
├── imsmanifest.xml
├── scorm_api.js
├── index.html                  # course home, links to modules
├── module1.html ... moduleN.html
├── <course-icon>.svg|png       # provided or generated; set as brand.course_logo
├── ocp_academy_white.svg       # default white Academy logo used by header + motion intro
├── audio/
│   ├── module1/slide_01_*.wav, slide_02_*.wav, ...
│   └── moduleN/...
└── figures/                    # reused source figures + AI fills
```

Every `moduleN.html` is a standalone slide deck with autoplay narration, prev/next nav, dark-mode toggle, fullscreen toggle, and SCORM completion wiring. The `index.html` displays module cards with completion checkmarks driven by SCORM `suspend_data`. In multi-SCO LMSes such as Docebo, Course Home marks complete on launch and each module marks complete when its own final slide is reached. Both `index.html` and each module page begin with the default OCP Academy motion intro overlay: white OCP Academy SVG lockup, animated diagonal background sweep from `#343895` to `#8DC63F`, then a fade into the menu or module deck. The intro text is generated from `course.json` (course title/subtitle for the index; module number/title/subtitle for modules). Every new course must define `brand.course_logo`; if the user does not provide one, generate a simple course-specific SVG mark. The renderer uses it on the index header, in each module's top-left badge, and as the floating title-slide hero icon. The manifest registers every runtime file. This is non-negotiable — LMSes are strict.

## The five phases of the wizard

The wizard has five gates. Walk through them in order. Each gate ends with the user explicitly approving — don't proceed without it.

### Phase 1 — Intake

Ask the user concise questions to collect:

1. **Course topic** (one-liner) and any working title.
2. **Source materials** — file paths to whitepapers (.pdf), specs (.pdf/.docx), Summit slide decks (.pptx/.pdf), or transcripts/notes from Summit recordings (.txt/.vtt/.srt). If the user has both a whitepaper and a Summit talk on the same topic, that's ideal — collect both.
3. **Target total learner duration** — e.g., 20 min, 45 min, 90 min. This drives depth.
4. **Audience level** — Introductory / Intermediate / Deep technical. This drives jargon density and assumed knowledge.
5. **Output folder** — always ask, do not assume. Default suggestion is a sibling folder next to the first source file.
6. **Cloud TTS API key** — ask only if not already in the environment (`ELEVENLABS_API_KEY` or `OPENAI_API_KEY`). If the user declines, fall back to `say` (macOS) and warn that quality will be lower.
7. **Brand assets** — confirm whether to use the default OCP Academy logo + green palette or supply alternates. Always obtain or generate a small course-specific `brand.course_logo` SVG/PNG; this is not optional because the templates use it in three visible places. The skill ships with the default green palette and the white OCP Academy SVG lockup baked into the template. The default motion intro is on unless the user explicitly asks to disable it.

Confirm intake back to the user in a short summary before moving on.

### Phase 2 — Deep source analysis

Read every source file. Use the appropriate Codex skill for the source type: `pdf` for PDFs, `presentations` for slide decks, `documents` for Word docs, and direct text reading for transcripts.

Extract and note:

- Core technical concepts and their dependencies (so prerequisites land before payoffs).
- Numerical values, dimensions, voltages, protocol names, version numbers — these are the *facts* the course must be faithful to. Quote them precisely.
- Acronyms and define-on-first-use vocabulary. For technical terms that may be unfamiliar to the target audience, build a `term_glossary` with short tooltip text and authoritative links. Attach `term_refs` only to the first substantive slide in each module where the term appears in visible text or narration.
- Available figures: every diagram, photo, chart, or schematic in the source. Save a manifest of these as `_source_figures.json` in the working area so you can refer back to them when drafting slides. Note page/slide numbers.
- Speaker insights from Summit material — anecdotes, motivation, "why this matters" framing. These are gold for narration.

Do not skim. The course's credibility depends on this analysis.

### Phase 3 — Outline proposal (GATE 1)

Compute the rough shape of the course using the duration math in `references/duration_math.md`. As a rule of thumb: **~2 minutes of seat time per slide**, **~8–10 slides per module**, **modules of ~15–20 minutes each**.

Draft a proposed outline as a Markdown document and put it in the user's chosen output folder as `_outline.md` (the leading underscore marks it as a working file you'll delete at the end). The outline lists every module and, beneath each, every lesson slide with a one-line description. Unless the user opts out, include a narrated `knowledge_check` slide immediately before each module's final `up_next` or `course_complete` slide. Every knowledge check must contain exactly two questions: first a single-answer radio question that checks the core concept, then a multi-select checkbox question that asks learners to apply or classify that concept. Knowledge checks should allow retry feedback and require an attempt on both questions before advancing, but should not require correct answers to continue. For the single-answer question, write an answer-specific `feedback_incorrect` on each incorrect choice that explains why that selected answer is wrong relative to the correct concept. For the multi-select question, use a concise question-level `feedback_incorrect` that points the learner back to the right mental model without trying to enumerate every wrong combination.

Present the outline to the user and ask: "Does this structure work? Suggest changes, add/remove modules, reorder lessons, etc." Iterate until they say "approved." **Do not move to Phase 4 without approval.**

See `references/slide_design_patterns.md` for the conventional slide types each module should include (title, objectives, content slides, takeaways, next-module teaser).

Every slide that uses a small `section_label` must have a distinct visible `title`. Do not set both to the same phrase. For example, keep the label `Learning Objectives` but use a descriptive title such as `Deployment Choices You Will Classify`; keep the label `Key Takeaways` but use a module-specific summary title.

For `content_grid` slides, use card tones only when the slide is intentionally contrasting distinct ideas, sides, states, risks, priorities, or categories. Leave tones unset for ordinary collections of related concepts so the grid reads as one family.

### Phase 4 — Narration scripts (GATE 2)

For each slide in the approved outline, draft a narration script as a plain text file at:

```
audio/module<M>/slide_<NN>_<slug>.txt
```

(The same path with `.wav` extension is where the rendered audio will land — keep them paired so it's obvious what produced what.)

Word count: aim for **140–160 words per minute of target slide duration**. A 90-second slide is ~225 words.

Voice rules — read `references/script_writing.md` for full guidance, but in short: warm and authoritative, never breathless, never marketing-speak, define acronyms on first use, use natural contractions, and write for the **ear**, not the page. Short sentences. No bullet lists in narration. No "as you can see on the slide" — narration plays automatically and the listener is also reading. Do not mention internal source types such as "webinar," "transcript," "source material," "article," or vendor examples in narration unless the user explicitly approves that citation. OCP contribution documents, OCP guidelines, and approved panel references may be named when relevant.

For cloud TTS, write pronunciation-aware scripts before generating audio. Spell out dense acronyms, standards, version numbers, and years in the script where needed, and avoid long slash-heavy strings. After generation, check suspect clips for late-volume fade, end buzz, post-speech noise bursts, and abrupt cuts; if the tail fades, shorten dense paragraphs and regenerate that slide only. If the issue is only after speech has ended, trim the post-speech artifact and preserve the spoken ending.

Every `knowledge_check` slide must have its own concise narration script and a matching `audio` block in `course.json`; do not leave knowledge-check audio null. The script should orient the learner to the two-question interaction and mental model, not read every answer choice. Use the same naming pattern as other slides, for example `audio/module1/slide_11_knowledge_check.txt` and `.wav`.

Save all scripts, then present them to the user in module-sized batches. Ask the user to edit any script directly in the file, or to tell you what to change. Iterate per module. **Lock each module's scripts with explicit user approval** before generating audio for it.

### Phase 5 — Figure plan and generation

For every slide that needs a figure, decide:

- **Reuse**: an existing figure from a source PDF/PPTX fits — note source path and page, then extract it via `scripts/extract_figures.py`.
- **Generate**: write a precise image-gen prompt (see `references/figure_prompts.md` for the OCP visual style guide — clean technical diagrams, white background, OCP green `#8DC63F` for emphasis, no photorealism unless the source has it).
- **Inline SVG**: for very simple diagrams (a labeled rectangle, a flow of three boxes), build inline SVG into the slide HTML rather than rasterizing.

Present the figure plan to the user. Approve before generating any AI images — image generation costs money and tokens and the user should sign off.

For inline SVG figures, make text fit the shape it lives in. Center labels when the layout calls for it, wrap long labels with `<tspan>` lines, or widen the shape. Never allow labels to spill outside boxes, pills, arrows, or badges. Every colored arrow line must use an arrowhead marker or explicit arrowhead polygon with the same color as the line. For any curved or diagonal arrow, the drawn line must flow into the center of the arrowhead's flat back side; do not terminate the line at the point of the arrowhead. Shorten the path, set marker reference coordinates to the back-center point, or draw the arrowhead as a separate polygon so the path endpoint is the back-center point and the final path tangent is aligned with the arrowhead centerline. The arrowhead tip must stop on the boundary line of the box, card, callout, or diagram object it points to; never let the arrowhead point intrude into the target shape. Labels must not overlap arrow lines or arrowheads; move long labels above or beside the path, center them to the figure when they describe the whole diagram, and check rendered screenshots before delivery.

### Phase 6 — Generation and assembly

Now you generate the artifacts. This phase is mechanical because the templates and scripts handle structure; your remaining authorial work is filling in slide content.

The single source of truth for the course is a JSON file at the working area root: **`course.json`**. Its schema is in `references/course_schema.md`. Build it up incrementally during phases 3–5 — the outline writes the skeleton, scripts add narration filenames, figure plan adds image references.

Before rendering, verify the course has:

- `brand.course_logo` pointing to a real SVG/PNG in the package root.
- Every `knowledge_check` slide has exactly two questions: question 1 is single-answer radio, question 2 is multi-select checkbox, both have feedback, and the slide has `audio.script_file`, `audio.wav_file`, an existing script, and a generated WAV from the same TTS provider, voice, and pacing as the surrounding narrated slides.
- Useful `reference_links`, `resource_callout`, and `term_refs` entries where learner aids are needed.
- Source/resource links on the slide where a learner first needs them, not only on a later wrap-up slide.

For rebuilds that add or update a knowledge-check slide in an already narrated module, generate the knowledge-check narration with the same cloud TTS setup used for the rest of the course. Do not fill the gap with macOS `say`, a different cloud provider, or a different voice just to keep moving. If the same-style audio cannot be generated, or if `audio_tail_report.py` flags the new clip, stop after the audio step, tell the user exactly which clip is blocked, and wait for a valid key, matching voice setting, approved fallback, or script edit. Do not run `render_module.py`, `render_index.py`, `validate_package.py`, or `zip_for_lms.py` after a knowledge-check audio failure.

Unless the user opts out, include the default `motion_intro` behavior described in `references/course_schema.md`: the course home and every module page play the OCP Academy CSS motion intro, with text populated from the course/module metadata. Do not create per-course MP4 intro files for this default path; the intro is HTML/CSS-native so SCORM packages stay small and do not require Playwright/ffmpeg.

Then run, in order:

1. `scripts/new_course.py <output-folder> course.json` — scaffolds the folder, copies `scorm_api.js`, copies the default motion-intro SVG logo when needed, creates `audio/moduleN/` subdirs and `figures/`.
2. `scripts/extract_figures.py course.json` — pulls reused figures out of source PDFs/PPTX into `figures/`.
3. *(AI-generated figures)* — for each `figure.generate_prompt` in `course.json`, generate an image and save it under `figures/<slug>.png`. Use the image generation tool available in this environment. (Outside this skill, this is the imagegen step.)
4. `scripts/check_svg_arrows.py course.json --fail-on-flags` — flags curved or diagonal SVG arrows whose path terminates at the front point of the arrowhead instead of flowing into the center of the flat back side, and flags explicit arrowhead polygons whose tip intrudes into a target rectangle. Fix the SVG geometry before generating audio or rendering modules.
5. `scripts/gen_audio.py course.json` — walks every `slide_*.txt` script, generates the matching `.wav` using cloud TTS if `ELEVENLABS_API_KEY` or `OPENAI_API_KEY` is set, otherwise macOS `say`. Default voice is Leo v2 (`bbGtsRRKUfYO634UxSjz`) — measured and authoritative for technical narration; override with `--voice <id>` or `ELEVENLABS_VOICE_ID`. Default pacing is `ELEVENLABS_SPEED=1.18` (1.0 reads too slowly for dense material). Knowledge-check narration is mandatory: if this script exits non-zero because a knowledge-check script/WAV is missing, because cloud TTS failed, or because it refused a likely voice mismatch, stop and gate the user before rendering. Use `--allow-local-fallback-for-partial` only after the user explicitly approves a local fallback for a partially narrated course. **If the call fails with a `403 Tunnel`/`blocked-by-allowlist` proxy error**, the Codex sandbox can't reach `api.elevenlabs.io`. The script detects this and prints a copy-paste command for the user to run on their Mac/Linux host instead — do not retry from the sandbox; relay the message and wait for the user to come back.
6. `scripts/audio_tail_report.py course.json --fail-on-flags` — flags generated clips whose ending is much quieter than the body or has a non-silent burst after a quiet gap. Listen to flagged clips, then shorten/regenerate or trim only post-speech artifacts. If the flagged clip is a new or updated knowledge-check narration, stop and gate the user before rendering.
7. `scripts/render_module.py course.json --module <N>` — renders `moduleN.html` for each module from the slide spec.
8. `scripts/render_index.py course.json` — renders `index.html` and writes `imsmanifest.xml`.
9. `scripts/validate_package.py <output-folder>` — sanity-checks everything: every audio file in `audioMap` exists, every figure referenced by HTML exists, manifest XML parses, file count matches manifest, no orphan files.
10. `scripts/zip_for_lms.py <output-folder>` — run only when the user says the course is ready to upload. This creates a strict zip with `imsmanifest.xml` at the archive root and excludes working files.
11. `scripts/course_delivery_summary.py course.json` — when the package is ready, report the title, a short LMS description candidate, module durations from the actual audio files, total narrated time, and module summaries.

If validation fails, fix and re-run. **Don't deliver a package that won't validate.** LMSes will reject it loudly.

### Phase 7 — Deliver and clean up

Remove working files (`_outline.md`, `_source_figures.json`, `course.json`) **only after confirming with the user** that the package is final. Some users may want to keep `course.json` so they can re-render later. Do not create the LMS zip until the user has validated slides and audio and explicitly says the course is ready to ship.

For upload, use the strict zipper rather than manual compression:

```
python scripts/zip_for_lms.py <output-folder>
```

The resulting zip must have `imsmanifest.xml` at the archive root, no folder wrapper, and no working files.

Then present the finished folder to the user with a `computer://` link to `index.html` so they can open the course in a browser:

```
[Open your new OCP Academy course](computer:///<absolute-path>/index.html)
```

## Key references

When you need detail on a topic, read the corresponding file. Don't load these into context unless you actually need them.

| Topic | File |
|---|---|
| Course JSON schema | `references/course_schema.md` |
| Duration → modules/slides math | `references/duration_math.md` |
| Slide layout patterns and when to use each | `references/slide_design_patterns.md` |
| Narration writing voice and pacing | `references/script_writing.md` |
| Image-gen prompts and OCP visual style | `references/figure_prompts.md` |
| SCORM 1.2 packaging requirements | `references/scorm_packaging.md` |
| Why the existing brand colors and CSS variables | `references/brand_style.md` |

## Key scripts

| Script | What it does |
|---|---|
| `scripts/new_course.py` | Scaffold an empty SCORM folder from a course.json |
| `scripts/render_module.py` | Render a single moduleN.html from a slide spec |
| `scripts/render_index.py` | Render index.html and imsmanifest.xml |
| `scripts/gen_audio.py` | Turn approved script .txt files into .wav using TTS |
| `scripts/audio_tail_report.py` | Scan generated .wav files for likely late-volume fade or noisy tails |
| `scripts/check_svg_arrows.py` | Flag SVG arrow lines that connect to the point of an arrowhead, plus arrowhead tips that intrude into target rectangles |
| `scripts/extract_figures.py` | Extract figures from source PDFs/PPTX for reuse |
| `scripts/validate_package.py` | Check the finished folder is LMS-ready |
| `scripts/zip_for_lms.py` | Build a strict upload zip from `imsmanifest.xml` runtime files only |
| `scripts/course_delivery_summary.py` | Generate delivery metadata and module duration summaries from `course.json` and final audio |

Each script has its own `--help`. Read its source if you need to understand what it accepts.

## Operating principles

**Be the editor, not just the typist.** When a Summit talk is 45 minutes and the user wants a 20-minute course, the user does not want a transcript-with-bullet-points. Identify the takeaways. Trim. Reorder. Add scaffolding the speaker left implicit.

**Quote, don't paraphrase, the specs.** If the source says "PCIe Gen 6 at 64 GT/s," the course says the same. Numbers, voltages, pinouts, dimensions, version numbers — copy them verbatim. Paraphrasing technical facts is how courses end up wrong.

**Cite source pages in `course.json` as you build.** Add a `source_refs` array on each slide pointing back to the page/slide in the originals. This is invisible to the learner but lets the user audit the course against the source.

**Stop at gates.** Phase 3 (outline), Phase 4 (scripts), Phase 5 (figure plan) each require explicit user approval. Don't push past a gate to "save a round trip" — you'll generate audio for narration the user wants rewritten, or generate figures for slides the user wants cut.

**One module at a time.** It's tempting to render all modules in one pass. Don't. Lock module 1's scripts, generate its audio, render its HTML, validate. Then move to module 2. This keeps feedback cycles short and prevents 8-module disasters.

**Match the reference SCORM exactly.** The CSS variables, control bar layout, audio player wiring, SCORM hooks, manifest namespaces — all of it is in the template for a reason. Don't redesign. If the user wants a different look, that's a separate skill.

**Protect LMS syllabus completion.** In multi-SCO packages, never gate a module's `cmi.core.lesson_status=completed` on all modules being complete. Course Home completes on launch. Each module preserves a prior `completed` or `passed` status on revisit, sets `incomplete` only when needed, and sets `completed` as soon as its own final slide is reached. The `up_next` slide may link to the next module for learner convenience, but SCORM 1.2 tracking belongs to the SCO the LMS launched.

**Never ship silent knowledge checks.** A `knowledge_check` slide is a narrated slide. If its script or WAV is missing, or if only a mismatched voice/fallback can be generated, stop and ask the user to resolve the audio gate before rebuilding the SCORM.

**Make learner aids precise and local.** Tooltips should appear only where the term first appears in a module, counting either slide text or narration. Do not put glossary chips for terms that are absent from the slide and narration. Tooltip/reference pills must live inside `.slide-content`, left-aligned, below the slide's last text/table/image element. Never put them in a floating "Terms" area, fixed footer, or control-adjacent panel. Use OCP sources for OCP-specific meanings and established sources such as IEC, DMTF, UL, NERC/IEEE, or NFPA for general electrical terms.

**Make resource links timely.** If a slide clearly depends on a white paper, spec, video, or project page, include a visible `reference_links` pill or `resource_callout` on that slide, even if the same resource appears again later.

**Protect the first-slide audio cue.** The title slide hint should tell learners to press play first, then advance with arrow or Space. Do not use copy that encourages learners to skip slide 1 narration. Keep the fixed course tagline below the play hint on every module title slide.

**Never invent a tagline.** The course-level `tagline` field on the index page is fixed: always use `"Community-driven Hyperscale Innovation for All"`. Do not riff on it — phrases like "Evolve. Don't replace." or "Consume. Collaborate. Contribute." are out, even if they sound on-brand. The CSS in `templates/index_styles.css` already renders `.header .tagline` in all caps with letter-spacing, so store the phrase in mixed case — display takes care of the rest. `render_index.py` defaults to this phrase when `tagline` is missing from `course.json`; don't override unless the user explicitly asks for a different phrase.

**Keep course marks clean.** Generated course logo SVGs should be simple marks, not text lockups. Do not embed acronym text such as "ESS" inside the SVG itself; use `brand.badge_text` for the separate top-left badge label when the short acronym is useful.

**Respect trademarks in visible text.** When writing OCP branded course text, render `OCP Ready` with a superscript `TM` in learner-facing HTML. In metadata, alt text, and manifest XML where HTML tags are inappropriate, use the `™` glyph. Do not alter source filenames or local paths just to add a trademark.

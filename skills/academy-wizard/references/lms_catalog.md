# Formal LMS catalog metadata

These fields are for the LMS catalog or course setup screen. They are **not the
course folder's README.md**. The README documents maintenance, rebuilding,
resources, and provenance. Do not derive LMS copy by summarizing that README.
A README may link to the separate LMS catalog files.

## Author and preserve the source

Store approved editorial values in `course.json.lms_catalog`. Use the full formal
course/series title for `title`, not a module title, badge, abbreviated visible
heading, or README heading. Preserve approved wording on rebuilds; authoring
recipes must carry this object forward rather than regenerate it from subtitles.

```json
{
  "style": "Slides",
  "course_title": "A Course Series",
  "target_duration_minutes": 30,
  "modules": [
    {"id": 1, "title": "System context"},
    {"id": 2, "title": "Design review"}
  ],
  "lms_catalog": {
    "title": "A Course Series",
    "short_description": "Explore the system context and the evidence needed for a design review.",
    "overview": "This series connects system requirements to a practical design review.",
    "duration_minutes": 30,
    "duration_basis": "estimated_learner_time",
    "duration_note": "Includes media, reading, questions, and activities.",
    "modules": [
      {"id": 1, "duration_minutes": 15, "summary": "Define the system boundary and its requirements."},
      {"id": 2, "duration_minutes": 15, "summary": "Review the evidence supporting the design."}
    ]
  }
}
```

For Scrolling use `lms_catalog.lessons` and the authored lesson IDs instead of
`modules`. Unit titles come from the authored modules/lessons; descriptions and
learner-time estimates come from this LMS object. Keep IDs and unit order tied to
the course. A series has one overall formal title and a paragraph for each module;
do not substitute individual module titles for the series-level Title field.

Requirements:

- Short Description: one line, **at most 130 Unicode characters**, including
  spaces and punctuation. Edit overlong copy; never silently truncate it.
- Long Description: one overview paragraph, then overall duration in minutes,
  then one small paragraph per module/lesson in authored order.
- Start each unit paragraph with its **bold title and duration**. Put its short
  summary on the **next line**, using a Markdown hard break or HTML `<br>`.
- Durations are estimated learner time, including relevant media, reading,
  checks, and activities. Do not replace them with WAV runtime or change them
  because a voice/model changed. Reconcile unit estimates with the overall
  estimate and `target_duration_minutes`. State optional-viewing exclusions in
  `duration_note` when appropriate; keep the approved public copy intact.
- Review LMS copy whenever scope, unit order, titles, or learner time changes.
  Keep editorial history and internal build information out of LMS descriptions.

`course_delivery_summary.py` validates these constraints and derives the formal
long description. Its output JSON contains explicit `title`, `short_description`,
`long_description` (Markdown), and `long_description_html` fields, plus the unit
records and duration basis. It does not read README.md or infer copy from audio.

## Generate, track, and deliver

```bash
python scripts/course_delivery_summary.py /path/to/course/course.json --write
python scripts/course_delivery_summary.py /path/to/course/course.json --check
python scripts/zip_for_lms.py /path/to/runtime \
  --course-json /path/to/course/course.json -o /path/to/delivery/course.zip
```

The source command writes `lms-catalog.json` and `lms-catalog.md` beside
`course.json`. Commit the LMS object and both text exports to the course source
repository, separate from its README. Run `--check` before a commit or PR so
reviewers see the exact approved copy corresponding to the source. If the source
is maintained outside the repository, version an explicitly metadata-only source
record and its exports; do not advertise that record as a runnable course.

The strict zipper validates the LMS source before replacing a ZIP. It accepts
`--course-json` or finds `course.json` in the runtime folder or its parent. It
refreshes the source exports and creates three **sidecars beside the ZIP**:

- `course.lms-catalog.json`: structured LMS fields.
- `course.lms-catalog.md`: readable/copyable approved copy.
- `course.lms-catalog.html`: the same copy with bold headings and line breaks for
  LMS rich-text fields.

These exports are separate from the README **and from the SCORM runtime**.
Keep them out of `imsmanifest.xml` and out of the strict runtime ZIP. Do not add
working metadata files to a package just to carry catalog descriptions. Missing,
overlong, inconsistent, or stale metadata must be resolved before delivery.
ZIP authorization does not authorize an LMS upload or a GitHub merge. When the
user requests repository publication, include the source/export changes in the
normal reviewable branch/PR workflow. Do not commit generated narration, runtime
HTML, catalog HTML delivery copies, or ZIPs.

## Language editions

Translate the LMS title, short description, overview, unit summaries, and label
templates in each locale's `lms_catalog`. Regenerate that locale's exports and
sidecars independently; do not reuse the English catalog or README. Keep the
formal learner-facing title free of an automatic language suffix; the manifest's
language-label policy remains independent.

English uses maintained labels by default. Non-English sources must provide all
five `lms_catalog.labels` values, for example:

```json
"labels": {
  "title": "タイトル",
  "short_description": "短い説明",
  "long_description": "詳しい説明",
  "overall_duration": "合計所要時間: {duration}分",
  "unit_heading": "モジュール {number}: {title} — {duration}分"
}
```

Keep the placeholders intact. The label templates control wording and punctuation
without changing the module summaries or approved learner-time estimates.

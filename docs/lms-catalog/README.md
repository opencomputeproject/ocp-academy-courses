# LMS catalog records

These are formal fields for LMS course setup, separate from the course folder's
maintenance README. They contain the full series title, a short description of at
most 130 characters, and a long description with an overview, overall duration,
and module summaries. Each summary starts on the line after its bold module title
and duration.

| Series | Approved LMS copy | Short description | Learner duration |
|---|---|---|---|
| Open Chiplet Economy: Business and Technology of Chiplet-based Systems | [Catalog fields](open-chiplet-economy/lms-catalog.md) | 126 characters | 150 minutes |
| FCSA: Architecting Interoperable Chiplet Systems | [Catalog fields](fcsa-architecting-interoperable-chiplet-systems/lms-catalog.md) | 114 characters | 85 minutes |

The copy was approved on 26 October 2026. Durations are estimated learner time,
not narration runtime. Optional full Summit recordings are excluded from the FCSA
estimate.

Each folder contains an editable `source.json` and generated `lms-catalog.json`
and `lms-catalog.md`. These source records are explicitly **metadata only**, not
runnable course definitions. Complete source projects are maintained outside
this repository. When a complete course is contributed, move its LMS source
object and exports into that course folder rather than maintaining two editable
copies.

Regenerate and check a record with:

```bash
python skills/academy-wizard/scripts/course_delivery_summary.py \
  docs/lms-catalog/open-chiplet-economy/source.json --write
python skills/academy-wizard/scripts/course_delivery_summary.py \
  docs/lms-catalog/open-chiplet-economy/source.json --check
```

Use the same commands for the FCSA folder. See the
[LMS metadata contract](../../skills/academy-wizard/references/lms_catalog.md)
for authoring, localization, source tracking, and ZIP-sidecar delivery.

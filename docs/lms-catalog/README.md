# LMS catalog fields

Formal LMS titles and descriptions are maintained with their complete course
sources, separately from maintenance README documentation. Each course has a
full series title, a short description of at most 130 characters, and a long
description with an overview, overall duration, and module summaries. Every
summary starts on the line after its bold module title and duration.

| Series | Approved LMS copy | Short description | Learner duration |
|---|---|---|---|
| Distributed AI Infrastructure | [Catalog fields](../../courses/distributed-ai-infrastructure/lms-catalog.md) | 104 characters | 80 minutes |
| Open Chiplet Economy: Business and Technology of Chiplet-based Systems | [Catalog fields](../../courses/open-chiplet-economy/lms-catalog.md) | 126 characters | 150 minutes |
| FCSA: Architecting Interoperable Chiplet Systems | [Catalog fields](../../courses/fcsa-architecting-interoperable-chiplet-systems/lms-catalog.md) | 114 characters | 85 minutes |

The Open Chiplet Economy and FCSA copy was approved on 26 October 2026; Distributed AI Infrastructure was prepared for delivery on 2 November 2026. Durations are estimated learner time;
optional full Summit recordings are excluded from the FCSA estimate.

Edit each course's `course.json.lms_catalog`, then regenerate and check its
`lms-catalog.json` and `lms-catalog.md` with
`skills/academy-wizard/scripts/course_delivery_summary.py <course.json> --write`
and `--check`. Packaging exports matching JSON, Markdown, and HTML files beside
the ZIP. See the [metadata contract](../../skills/academy-wizard/references/lms_catalog.md).

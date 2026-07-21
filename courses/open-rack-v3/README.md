# Open Rack v3

Readable source for the seven-course **Open Rack v3** learning series. Each child folder is an independent OCP Academy course using the Scrolling style, with its own `course.json`, course resources, and LMS-ready build output.

The seven courses are grouped here for source management, but they are not modules inside one SCORM package. Build and upload each course separately, then order them in the LMS learning plan.

## Course sources

| Order | Folder | Course | Status |
|---:|---|---|---|
| 1 | `module-1-ocp-orv3-history-and-impact` | Module 1: OCP & ORv3: History and Impact | Recovered and ready for source review. |
| 2 | `module-2-orv3-core-specifications` | Module 2: ORv3 Core Specifications | Recovered and ready for source review. |
| 3 | `module-3-orv3-real-world-implementations` | Module 3: ORv3 Real World Implementations | Recovered and ready for source review. |
| 4 | `module-4-orv3-high-power-racks` | Module 4: ORv3 High Power Racks | Recovered and ready for source review. |
| 5 | `module-5-orv3-future-trends` | Module 5: ORv3 Future Trends | Recovered and ready for source review. |
| 6 | `module-6-the-open-rack-wide-orw-expansion` | Module 6 - The Open Rack Wide (ORW) Expansion | Recovered and ready for source review. |
| 7 | `module-7-advanced-orw-liquid-cooling-practice` | Module 7 - Advanced ORW Liquid Cooling & Practice | Recovered and ready for source review. |

## Source contract

- `course.json` is the human-readable Scrolling course definition used by AcademyWizard.
- `conversion.json` records the source archive fingerprint, recovered block inventory, and media-integrity audit for inspection.
- `resources/` contains only course-owned learner media that cannot be reconstructed from readable code, including images, video, fonts, and documents.
- Rendered HTML, manifests, runtime files, and SCORM zips are generated and are not committed.

## Series authoring rules

- Keep `theme.navigation_restricted` set to `false` in all seven courses. Every lesson must remain available and use the normal, non-disabled treatment in both the cover lesson plan and the table of contents, even when an original Rise package used restricted navigation.

See [OCP Academy course styles](../../docs/course-styles.md) for the Scrolling format and fidelity rules.

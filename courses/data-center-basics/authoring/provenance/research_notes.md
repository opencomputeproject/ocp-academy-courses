# Research and source-analysis notes

Research date: October 23, 2026. Status: outline support; narration, teaching text and glossary placements have not yet been approved.

## Source recovery

AcademyEditor recovered the four supplied archives without executing their bundled JavaScript. All use the older `index.html` embedded-state Rise export and SCORM 2004 3rd Edition. Their editable recovery files remain under the project's `_recovered/` directory, independently preserving each original archive boundary. The final Slides adaptation will combine those boundaries into four modules in one manifest, as explicitly requested.

Recovery totals: 31 lessons and 125 resource records. Exported resource hashes were checked against both the recovery audit and the archive binary content. All four conversions report zero unresolved media and zero unsupported block types. The output includes 83 raster images plus other retained media/font resources; 94 image placements were indexed, and OCR was performed on the raster images to identify embedded teaching claims. The OCR record is a discovery aid; it does not replace visual QA.

Ten non-descriptive video captions were suppressed by the converter: `Module 1 - Video 1`, `Module 1 - Video 2`; `M2 Video 1` through `M2 Video 4`; `M3 Video 1`; and `M4 Video 1` through `M4 Video 3`. These are sequence labels, not accessibility caption tracks. None of the ten recovered video media objects declares a source timed-text caption track. All original video binaries and posters were retained; new descriptive slide titles will identify them.

The source has no dedicated reference lesson. Only two explicit external links were recovered in the structured content, so useful new references should be attached to the teaching slides that use them rather than collected into a references-only slide.

## Recent sources selected for teaching updates

### R1 — IEA, Key Questions on Energy and AI

- Published April 16, 2026.
- [Report](https://www.iea.org/reports/key-questions-on-energy-and-ai), [executive summary](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary).
- Teaching use: distinguish current estimates and projections. The updated analysis puts global data-center electricity use around 485 TWh in 2025 and projects roughly 950 TWh in 2030. The course should connect growth to local power and planning constraints rather than assume an unconstrained global buildout.
- Placement: M4/15. Optional context in M1 narration without duplicating the chart.
- Limits: projected consumption is not installed capacity; TWh is energy, not power. Do not blend this estimate with a different organization's forecast.

### R2 — OCP, Powering the Next Era of AI

- Published August 11, 2026, as listed on the OCP news index.
- [Article](https://www.opencompute.org/news/powering-the-next-era-of-ai-how-google-microsoft-and-nvidia-are-standardizing-and-accelerating-the-industry-transition-to-lvdc/).
- Teaching use: OCP participants are aligning 800 VDC interfaces and requirements for high-density AI facilities. Retrofit side power racks and direct facility conversion are distinct paths. This is a developing architecture that can coexist with AC infrastructure, rather than a universal replacement claim.
- Placement: M2/15, with the general topic revisited for a different systems-design purpose in M4/17 if useful.
- Limits: no electrical installation instructions or universal readiness claim. The news article is suitable for orientation, not a substitute for a design specification.

### R3 — OCP, Realizing the OCP Open Data Center Ecosystem Vision

- Published October 12, 2026, as listed on the OCP news index.
- [Article](https://www.opencompute.org/news/realizing-the-ocp-open-data-center-ecosystem-vision/).
- Teaching use: open infrastructure coordination now spans facility power, thermal systems, racks, accelerators and management. The introductory lesson is that equipment choices create dependencies across the entire facility and grid interface.
- Placement: M4/17 and the transition to Intro to OCP.
- Limits: roadmap statements and extreme-density examples are not industry averages. Avoid duplicating detailed technical course content already available elsewhere.

### R4 — Google, Introducing Brazos

- Published June 16, 2026.
- [Article](https://cloud.google.com/blog/topics/systems/brazos-liquid-cooling-system-for-air-cooled-data-centers).
- Teaching use: a closed-loop liquid-to-air rack system illustrates how liquid-cooled IT can operate in an existing air-cooled environment. The facility still needs enough power and air-side heat rejection.
- Placement: M2/14.
- Limits: a specific retrofit example, not a claim that every dense workload can fit every existing room or that all liquid cooling consumes site water through evaporation.

### R5 — OCP, Introducing OSPA

- Published October 8, 2026, as listed on the OCP news index.
- [Article](https://www.opencompute.org/news/introducing-ospa-unifying-the-switch-platform-layer-for-open-networking/).
- Teaching use: optional example of common platform-management interfaces for inventory, power and environmental monitoring.
- Placement: M4/8 only if it helps an introductory explanation; do not add detail solely because the publication is new.
- Limits: the announced work is in progress and concerns switch platform management. It does not define the switch forwarding plane or a whole-facility management platform.

## Authoritative supporting sources

- [NIST cloud definition](https://www.nist.gov/publications/nist-definition-cloud-computing?pub_id=909616) and [private cloud glossary](https://csrc.nist.gov/glossary/term/Private_cloud): use the service characteristics and avoid requiring many facilities or public internet access.
- [Uptime Tier classification](https://uptimeinstitute.com/tiers) and [Tier explanation](https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/): use infrastructure capabilities; current Tier definitions do not predict annual availability. The explanatory article was readable in a primary-source search excerpt; direct retrieval returned 403.
- [METCASE 19-inch front panel](https://www.metcaseusa.com/en/19-Front-Panels/M6019010.htm): manufacturer's standard front-panel width example, 482.6 mm. [CyberPower rack hole-spacing FAQ](https://www.cyberpowersystems.com/faqs/what-is-the-standard-rack-horizontal-hole-spacing/): 18.312 inches / 465.1 mm hole-center spacing, available in the primary-source search excerpt; direct retrieval returned 405.
- [Green Grid PUE definition](https://www.thegreengrid.org/node/372): energy ratio, not a complete environmental or useful-work metric.
- [OCP Cooling Environments](https://www.opencompute.org/projects/cooling-environments/): current cooling context and relevant component/interface roles.
- [OCP Heat Reuse](https://www.opencompute.org/projects/cooling-environments/heat-reuse/): treat excess heat as a potential asset with technical, economic and policy constraints.
- [DOE energy-efficient data-center design guide](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design.pdf): search discovery confirms site versus source water-accounting distinction. Downloaded and visually checked PDF viewer pages 39–40 (printed pages 30–31): WUE accounting and CUE units. M4 slide 10 links directly to viewer page 39 and labels the relevant range.

## Intro to OCP continuity

Read the current main-branch repository README and the four canonical course definitions through the GitHub connector. Local copies from the neighboring Intro to OCP project were also inspected to identify the established course family. Repository snapshots are saved under the project's `_research/intro-to-ocp/` folder.

Repository: [opencomputeproject/ocp-academy-courses](https://github.com/opencomputeproject/ocp-academy-courses). [Intro to OCP series source](https://github.com/opencomputeproject/ocp-academy-courses/tree/main/courses/intro-to-ocp).

| Canonical course | Topics reserved for the next series | Snapshot blob SHA |
|---|---|---|
| The OCP Origins | Efficiency crisis, OCP history, Open Rack evolution and open-infrastructure impact. | `a91e6e030ca4a7f5454a7e958cadb50f3c59e588` |
| The OCP Ecosystem & Governance | Community participants, governance, projects and contribution lifecycle. | `9c992d6df625a932821e5b4a10806c909c6fcc12` |
| OCP Technologies (Open Rack & Cooling) | ORv3 architecture and advanced cooling details. | `39fa439483f74c8ca2322109d29fcfb5146b021f` |
| Today and Tomorrow (The Journey) | Hardware tiers, Marketplace and adoption framework. | `a380831d092dcb9106bc2c186bda827ce804773a` |

DC Basics should establish the vocabulary and physical reasoning needed for those courses. Introduce Open Rack and shared interfaces briefly, then close with the question of how the community develops, contributes and adopts them. Do not merge the existing series into this package or rewrite it.

## Final implementation and verification

The 76-slide, four-SCO build is complete for final review. All narration scripts and WAVs, all ten unchanged videos, twelve checked interactions, forty glossary definitions, five new teaching animations and twenty-four new static diagrams are retained. OSPA was researched but omitted because its detail was unnecessary for this introductory course. The IEA, OCP LVDC and ecosystem-vision articles and Google Brazos example appear only on relevant teaching slides.

The user accepted all narration and waived intermediate production stops on 23 October 2026. Local package, schema, layout and runtime tests are documented in `qa/`. Human listening approval and a real target-LMS import/session test remain final-review tasks. No ZIP or repository push was made.

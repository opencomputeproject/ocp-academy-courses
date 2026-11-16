# AI Native Edge-MHS architecture and integration review

Approved outline, 13 November 2026. **One narrated Slides course, approximately 55 minutes total, with three content SCOs and a separate tracked Course Home.** The course develops Class N/L selection, interface-review judgment and concise integration findings for intermediate hardware engineers.

## Course structure and duration

| LMS syllabus entry | Planned learner time | Slides | Learner outcome |
|---|---:|---:|---|
| Course Home | 1 minute | Home page | Understand the course outcomes and module structure. |
| Module 1 — Architecture and Class N/L | 16 minutes | 10 | Explain the HPM boundary, choose a class/depth, and identify compatibility conditions. |
| Module 2 — Mechanical interfaces and compatibility | 20 minutes | 11 | Locate the critical mounting, clearance, connector and power checks. |
| Module 3 — Integration review exercises | 18 minutes | 9 | Evaluate two guided examples and record an evidence-backed disposition. |
| **Total** | **55 minutes** | **30 content-module slides plus Home** | Within the requested 45–60-minute total. |

The time budget includes narration, reading/thinking, all three two-question knowledge checks, guided exercises and teaching videos. Videos run alongside their teaching narration and do not add a second time allowance. Full Summit recordings and adjacent Academy courses are optional continuing resources, outside the core duration. Preserve maintained narration voice/pacing; reach the target by focusing content and script length.

Use the usual AcademyWizard Slides organization: **Course Home first, then Modules 1–3**, in one SCORM 1.2 package. Home is its own SCO, in addition to the three content SCOs: **four tracked syllabus entries total**. The eventual course source will record `style: Slides`, `scorm.version: 1.2`, `scorm.organization: multi-sco`, `scorm.include_home_sco: true` and `scorm.expected_sco_count: 4`. Standard Home, module navigation, bookmarks and knowledge-check behavior apply; verify the final package in the target LMS before release.

## Module 1 — Architecture and Class N/L

**16 minutes; 10 slides.** Retain a short AICC/MHS context bridge and the form-factor decisions learners need for the review exercises.

| Slide | Visible title / teaching purpose | Minutes | Actual base-spec pages |
|---|---|---:|---|
| 1 | Architecture and Class N/L — module title | 0.5 | — |
| 2 | Three decisions this course will prepare you to make — course overview | 0.5 | — |
| 3 | The HPM contract and its boundaries — modular role; requirement, recommendation, example and delegated scope | 2 | §§5–9, pp. 12–20 |
| 4 | Compare Class N and Class L — widths, depth range and fixed riser positions | 2 | pp. 21–22, 31–38; §12.9.2 p. 70 |
| 5 | Choose depth with CCIs in mind — designators and chassis-depth distinction | 2 | pp. 22–24, 37–38 |
| 6 | Keep fixed and floating features in their reference frames — Astra teaching animation V1 | 3 | §§10.7–10.9, pp. 27–30 |
| 7 | Compatibility still needs an integration review — common-chassis example and companion-spec handoff | 2 | pp. 17–18, 24, 30, 34, 88 |
| 8 | Carry these architecture decisions forward — key takeaways | 1 | — |
| 9 | Check your architecture decisions — one single-answer and one multi-select question | 2.5 | Supporting pages above |
| 10 | Next: review the interfaces — module transition | 0.5 | — |

Technical anchors: Class N 168mm, Class L 295mm; allowed depth 250mm–365mm; five CCI planning points 260mm, 280mm, 305mm, 350mm and 365mm. Explain the 305.59mm table entry/rounded-down designator briefly. Use [§10.1–10.3, pp. 21–24](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=21) and [§12.1, pp. 37–38](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=37).

## Module 2 — Mechanical interfaces and compatibility

**20 minutes; 11 slides.** Teach a compact review sequence and a usable reference checklist. Detailed tolerances, hole dimensions, connector tables and stack-up arithmetic remain page-linked references rather than separate lessons.

| Slide | Visible title / teaching purpose | Minutes | Actual base-spec pages |
|---|---|---:|---|
| 1 | Mechanical interfaces and compatibility — module title | 0.5 | — |
| 2 | The interface checks you will make — objectives | 0.5 | — |
| 3 | Start at the datum — outline, mounting, retention and handle interfaces; Astra CAD/interface animation V2 | 3 | §§12–12.2, pp. 36–46; §§12.5–12.6 pp. 59–61 |
| 4 | Read the underside envelope — secondary-side zones and board/backplate stack-up | 3 | §§12.3–12.4, pp. 47–58 |
| 5 | Apply height limits to the actual configuration — required conditions, recommendations and exemptions | 2 | §12.10, pp. 74–77 |
| 6 | Check management and infrastructure placement — DC-SCM/NIC, M-PIC zones and CFF interference risk | 3 | §§12.7–12.8, pp. 62–67 |
| 7 | Review HSIO and fixed risers — connector/position requirements and M-XIO boundary | 2 | §12.9, pp. 67–73 |
| 8 | Separate connector ratings from power delivery — far-zone requirement, fixed-riser minimum and electrical dependencies | 3 | §§13–14, pp. 80–88, especially pp. 83 and 86 |
| 9 | Use one interface review checklist — key takeaways | 1 | — |
| 10 | Check your interface judgment — one single-answer and one multi-select question | 1.5 | Supporting pages above |
| 11 | Next: put the review into practice — module transition | 0.5 | — |

Keep mandatory conditions intact when compressing: the recommended 12mm height zone differs from the conditional 11.3mm/6mm requirements; optional peripherals can trigger mandatory interface conditions. The far-zone body requirement and minimum power per implemented fixed riser remain explicit. Cite [height restrictions, p. 74](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=74), [far power, p. 83](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=83) and [riser power, p. 86](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=86).

## Module 3 — Integration review exercises

**18 minutes; 9 slides.** Use two bounded, guided examples with narrated debriefs. The exercises require source selection and judgment, rather than lengthy submissions or a full CAD workstation lab.

| Slide | Visible title / teaching purpose | Minutes | Actual base-spec pages |
|---|---|---:|---|
| 1 | Integration review exercises — module title | 0.5 | — |
| 2 | Turn observations into review findings — objectives | 0.5 | — |
| 3 | Record a claim, evidence and disposition — review method and source-conflict flags | 1.5 | §§5–6, pp. 12–16; conflict evidence pp. 44, 62, 86, 89 |
| 4 | Case 1: can N350 use a chassis planned for L365? — outline/tray example, fixed/floating features and far-edge KOZ obligations | 4.5 | §§10.7–10.9, pp. 27–30; p. 34; §§12.3.2, pp. 49–54 |
| 5 | Case 2: what blocks this proposed integration? — a constructed Class L review pack with conditional clearance, far-power and riser-power findings | 4.5 | §§12.9–13.3, pp. 69–86, especially pp. 74, 83, 86 |
| 6 | Reveal the evidence behind the decision — Astra debrief animation V3; distinguish a finding from a whole-system compliance claim | 2 | Source pages for both cases |
| 7 | Carry the review method into your next design — key takeaways | 1 | — |
| 8 | Check your review decisions — one single-answer and one multi-select question using the cases | 3 | Supporting pages above |
| 9 | Apply the method and keep the references — course completion and optional resources | 0.5 | Whole-document/resource links |

Review dispositions are: conforms on available evidence; does not conform on available evidence; not applicable with a reason; or insufficient/conflicting evidence. Source citation, conditional applicability and correct escalation matter. An unresolved contradiction never receives an invented definitive compliance answer.

The supplied STEP models are N365/L365 examples. Use their verified geometry for orientation; any N350 teaching derivative is explicitly labeled. Chassis/tray examples on [pp. 29–30](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=29) and supplemental renderings on [pp. 90–97](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=90) illustrate possibilities and cannot establish full system interoperability.

## Overlap, scope and source controls

**AICC:** retain a short architecture/context bridge in Module 1 and optional links to the existing Academy course. Leave inference deployment, scale/sync/reach-across and ecosystem surveys there.

**MHS M-PNP:** retain a brief distinction between mechanical/electrical fit and logical interoperability. Link the existing v0.7 course for FRU/discovery/boot, programmable devices, schemas and tools. Neither adjacent course is required viewing to complete this 55-minute course. The detailed overlap evidence is retained in `planning/_source_analysis.md`.

Use visible requirement, recommendation, example, companion-spec and excluded/future distinctions. Section 6 is a navigation aid, explicitly not a standalone compliance checklist. Detailed compute-core, cooling, reliability, chassis/riser, firmware/security and environmental implementation remains excluded. Timing, native blind-mate and 162mm HPM support remain potential future material. See [scope, pp. 12–16](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=12) and [future material, p. 98](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf#page=98).

Preserve the documented Class L hole-count conflict (p. 14 versus p. 44), DC-SCM R3.2/R2.2 reference conflict (pp. 16/86 versus 26/62/89), stale figure references and the Summit dimension discrepancy. Explain how to flag them without turning them into lengthy extra lessons. Exclude disputed numerical values from definitive quiz answers pending clarification.

## Videos and narration

The user-authorized **Astra sub-agent owns all video work**. Plan one teaching animation in each module, with a provisional 90-second allocation included in the slide time. For narrated Slides, storyboard against the approved final narration; play one synchronized pass and hold the final frame. Preserve editable sources and static/accessibility equivalents. Exact video lengths follow approved scripts rather than forcing narration into a clip duration. Video production waits for script/storyboard approval.

The direct Summit match, [AI-Native Edge MHS 1.0](https://www.youtube.com/watch?v=NtcCQE-pXQg), is an optional 16:35 resource. Its class/mechanical deck pages support context; future-direction slides stay excluded from requirements. AICC and M-PNP recordings are also optional continuing links. Full deck text and selected visuals were reviewed; recording excerpts/timestamps remain unverified. See `planning/_video_plan.md` and `planning/_summit_video_sources.json`.

Every slide, including each knowledge check, receives its own narration. Each module check has exactly two questions: single-answer first, multi-select second, with feedback. The course retains the maintained AcademyWizard narration and player defaults. Keep formal learner time separate from audio runtime.

## Review gate

This approved outline defines one course, three content modules, tracked Course Home and a 55-minute estimated learner duration. The user authorized the full narrated review build, videos, LMS information and poster without intermediate editorial gates. The review build is prepared in `AI_Native_Edge_MHS_OCP_Academy_SCORM/`; ZIP creation remains pending the user’s review and request.

# Thermal Boundaries course alignment

## Position in the OCP Academy cooling curriculum

Thermal Boundaries should teach learners to diagnose the limiting constraint, explain why a cooling transition is delayed, evaluate its economic and reliability implications, and prepare the interfaces and evidence needed to make it deployable. Those decisions connect the existing introductory, fluid, and implementation courses.

The strongest overlap in the first outline was with Modules 1–2 of **Two-Phase Direct Liquid Cooling Efficiencies and Fluids**. Those modules already discuss rising heat flux, nested loops, coexistence, adoption constraints, and interoperability. Brazos also already teaches full-path review, qualified performance claims, common service dependencies, and dynamic acceptance evidence. The new course therefore needs to develop the paper's specific framework and apply it across architectures.

Keep the proposed 3 modules and 30 slides, with approximately 50–55 minutes of learner time. Replace general introductory teaching with diagnostic examples; retain only the reminders needed to make this course understandable on its own. No other course is a mandatory prerequisite.

## Evidence reviewed

- Public [cooling catalog](https://academy.opencompute.org/learn/public/catalog/view/3?ctldoc-catalog-0=category_id-4), individual course descriptions, and the older overview's public learning-plan syllabus, checked October 12, 2026.
- Current `main` of [ocp-academy-courses](https://github.com/opencomputeproject/ocp-academy-courses/tree/4cc285f9a30540e07e5a3edf09c2329787f8c0f3), commit `4cc285f9a30540e07e5a3edf09c2329787f8c0f3`, dated October 12, 2026. The audit used this snapshot rather than the older local branch checkout.
- Slide content, media text inventories, and relevant narration for Fluids, Two-Phase DLC, Brazos, Deschutes, and Open Data Center for AI; relevant lesson text and cooling-video captions for Intro to OCP Module 3 and Open Rack Module 7.
- The downloaded Thermal Boundaries paper, version 1.00.

The older Liquid Cooling Technologies Overview is assessed from its public descriptions and four-course syllabus; its lesson media were not inspected. Public descriptions can also lag source revisions: for example, Deschutes currently advertises 25 narrated slides while the current source contains 29 slides including its knowledge checks. These differences do not change the scope comparison.

## Where each existing course belongs

| Existing course | Established teaching role | What Thermal Boundaries adds | Detail to keep in the existing course |
|---|---|---|---|
| [Liquid Cooling Technologies Overview](https://academy.opencompute.org/learn/learning-plans/5/liquid-cooling-technologies-overview) — 35-minute learning plan | Four introductory courses: Why Liquid Cooling Now; Direct Liquid Cooling (Introduction); Immersion Cooling Essentials; Operations, Planning & Strategic Value. | A more structured diagnosis using the three boundaries, avoidance zone, agency mismatch, and ecosystem readiness. | A broad first introduction to direct-to-chip and immersion methods. |
| [Cooling Fluids in Direct Liquid Cooling (DLC)](https://academy.opencompute.org/learn/courses/52/cooling-fluids-in-direct-liquid-cooling-dlc) — catalog: 36 minutes | Selection, qualification, chemistry, material compatibility, commissioning, sampling, filtration, monitoring, mixing, and documentation for single-phase fluids. | Why fluid qualification and service capability affect the economics and readiness of an architecture. | Chemistry targets, treatment choices, cleaning/filling steps, sampling practices, and monitoring schedules. |
| [Two-Phase Direct Liquid Cooling Efficiencies and Fluids](https://academy.opencompute.org/learn/courses/53/two-phase-direct-liquid-cooling-efficiencies-and-fluids) — catalog: 60 minutes | Phase-change efficiency, loop architecture and controls, fluid qualification, purging, monitoring, maintenance, and lifecycle. | The three-boundary model, adoption incentives, concentrated versus distributed loads, and comparison of reference design envelopes across methods. | Detailed boiling mechanisms, circuit design, pressure budgets, fluid criteria, purge procedures, and operational thresholds. |
| [OCP Project Deschutes: Coolant Distribution Unit (CDU) v1.0](https://academy.opencompute.org/learn/courses/48/ocp-project-deschutes-coolant-distribution-unit-cdu-v10) — catalog: 40 minutes | A specific open liquid-to-liquid CDU: performance curves, physical interfaces, component design, controls, supply chain, and maintenance. | The IT/facility lifecycle mismatch, incentives at the transport seam, shared failure domains, and supply-chain preparation debt. | Deschutes ratings, pump curves, approach-temperature targets, components, supplier tiers, and service procedures. |
| [OCP Project Brazos: Liquid Cooling in Air-Cooled Data Centers](https://academy.opencompute.org/learn/courses/78/ocp-project-brazos-liquid-cooling-in-air-cooled-data-centers) — catalog: 55 minutes | A specific liquid-to-air deployment: end-to-end heat path, conditional ratings, airflow/pump tradeoffs, integration, service continuity, controls, and acceptance. | Use Brazos as a brief example of preserving upstream infrastructure while changing chip-level acquisition; examine the tradeoff in the paper's framework. | Rack/chassis ratings, installed-condition checks, controller states, service conditions, and implementation-specific validation. |

Two adjacent courses also deserve routes from the new course:

- [Open Rack and ORv3: Past, Present, and Future](https://academy.opencompute.org/learn/learning-plans/4/open-rack-and-orv3-past-present-and-future), **Module 7 — Advanced ORW Liquid Cooling & Practice:** rack/manifold integration, canisters, Pivoting Blind Mate Coupling mechanics, and implementation examples. Thermal Boundaries discusses the value and risk of interfaces; this course owns the mechanical integration detail.
- [Open Data Center for AI: Applying Specification 0.7](https://academy.opencompute.org/learn/courses/69/open-data-center-for-ai-applying-the-specification): physical compatibility, facility power/cooling envelopes, peak versus blended density, and documented site variations. Thermal Boundaries explains how site constraints change the architecture decision; Open DC owns its specification-specific facility targets.

**Intro to OCP Module 3 — OCP Technologies (Open Rack & Cooling)** already offers a broad technology survey. Refer learners who need that orientation there; avoid creating another full air/cold-plate/immersion introduction.

## Distinctive content to protect

The four dedicated cooling-course sources already teach many relevant concepts, but the explicit terms efficiency boundary, economic boundary, physics boundary, avoidance zone, least-disruption law, agency mismatch, preparation debt, and complexity debt did not appear in the reviewed course-text/narration exports. This is a vocabulary check, not proof that related ideas are absent.

Use that framework to add depth in five places:

1. **Diagnosis:** distinguish a cooling-energy penalty, a total-cost disadvantage, and an inability to hold the device within specification.
2. **Adoption:** explain why the person paying the operating cost may not control the design, and how preparation debt differs from complexity accumulated by extending the incumbent.
3. **Load coverage:** demonstrate how solving the accelerator hotspot can leave the distributed load as the next binding constraint.
4. **Evidence:** interpret the paper's cold-plate boundary, reliability estimates, fleet observations, and TCO case using their actual assumptions and fault domains.
5. **Readiness:** connect interfaces across different owners and lifecycles, with jointly agreed and witnessed evidence for the assembled thermal system.

## Changes to the first outline

| Original emphasis | Revised emphasis |
|---|---|
| Separate broad heat-balance/flow tutorial | A compact reminder inside a diagnostic example; give the freed slide to the avoidance zone. |
| General explanation that constraints trigger adoption | Develop the authors' least-disruption law, agency mismatch, and distinct preparation/complexity debts. |
| Two slides surveying cold plates and immersion | Compare what their surface and volume approaches cover, which boundary binds, and which dependencies each introduces. |
| Generic chip-to-facility heat-path animation | Show an acquisition limit or residual distributed load persisting despite sufficient downstream transport/rejection. |
| General readiness and operating checklist | Test the economic evidence, fault-domain assumptions, cross-owner handoffs, and witnessed dynamic behavior. |

The checks should ask learners to classify a boundary, diagnose a coverage gap, interpret model assumptions, or identify missing evidence. They should not repeat fluid-property recall, controller states, connector engagement, purge thresholds, or product specification questions from the specialist courses.

## Cross references from the revised course

Use public Academy course pages, with a visible label naming the relevant module or topic. No module-specific LMS URL or SCORM-page anchor has been verified. Links open in a new tab and remain optional; knowledge checks must be answerable within Thermal Boundaries itself.

| New course location | Destination | Reason for the reference |
|---|---|---|
| M1 S2, course overview | Liquid Cooling Technologies Overview | Optional preparation for learners unfamiliar with direct-to-chip and immersion. |
| M1 S7, preparation versus complexity debt | Deschutes, Module 3: supplier model | A concrete supply-chain readiness example without reproducing its vendor-tier table. |
| M2 S4, locate the limiting thermal step | Brazos, Module 1; Deschutes, Module 1 | Two different upstream interfaces serving liquid-cooled IT. Keep this as a brief example of the thermal-path framework. |
| M2 S5, single-phase design envelope | Two-Phase DLC, Module 2 | Follow-on depth in phase-change architecture, loop control, flow, and pressure budgets. |
| M2 S6, surface and volume methods | Overview learning plan, Course 3: Immersion Cooling Essentials | Optional basic immersion orientation. |
| M2 S7, complementary architectures and interfaces | [Open Rack learning plan](https://academy.opencompute.org/learn/learning-plans/4/open-rack-and-orv3-past-present-and-future), Module 7, Lessons 2–3 | Mechanical manifold/coupling detail. The verified destination is the learning plan; the visible link label should direct learners to Module 7. |
| M3 S3, full cost across lifecycle and ownership | Fluids, Modules 2–4 | The qualification, operating work, and records that belong in the cost/readiness estimate; no chemistry tutorial here. |
| M3 S4, component versus shared failure domains | Deschutes, Modules 2–3 | An implementation example for redundancy and service requirements; do not assign the paper's generic CDU failure rate to it. |
| M3 S6, site constraints and candidate architectures | Brazos, Modules 2 and 4; [Open Data Center for AI](https://academy.opencompute.org/learn/courses/69/open-data-center-for-ai-applying-the-specification), Modules 3–4 | Refer to detailed implementation and facility review after the framework identifies the open question. |
| M3 S7, system-level commissioning evidence | Fluids, Module 3; Two-Phase DLC, Module 4 | The procedure-level startup and fluid-operation detail belongs in those courses. |
| M3 S10, course completion | The full paper plus a choice of the four specialist courses and introductory overview | A needs-based next step: fluid operations, two-phase mechanics, facility-water CDU, or air-cooled-site retrofit. |

Put each link on the teaching slide where it becomes useful. Avoid repeating the same destination twice on one slide. Keep detailed paper references page-specific; the completion slide links to the full paper.

## Current and reciprocal references

The live specialist course pages already show one another in their **Suggested for you** areas. Those platform recommendations are separate from authored references inside a course.

Current authored references in the repository:

- **Fluids M1 S7** links to the dedicated Two-Phase DLC course.
- **Brazos M1 S7** links to Deschutes; **M3 S4** links to Fluids; its final slide offers both.
- **Deschutes M3 S7** links to the introductory overview learning plan.
- **Two-Phase DLC** currently has no direct Academy course references in its course source.
- **Intro to OCP Module 3** links to the broad catalog rather than individual specialist courses.

When Thermal Boundaries has a verified public course URL, propose these small reciprocal additions:

- Two-Phase DLC M1 S7: a boundary/adoption-framework reference; consider a Fluids link at its single-phase comparison in M1 S6.
- Fluids M1 S3 or its final slide: a reference for deciding the cooling architecture before specifying its fluid.
- Deschutes M3 S7: a reference for lifecycle, shared-domain reliability, and ecosystem readiness.
- Brazos M4 S10: a reference for comparing the retrofit choice with other architectures and interpreting the economic case.
- Intro to OCP Module 3, Cooling Solutions: a route to the comparative decision course after the technology overview.
- Open Rack Module 7 summary and Open DC final resources: optional links for the architecture rationale behind their mechanical/facility decisions.

These are proposed source additions, not changes applied to the existing courses. Do not invent a future Thermal Boundaries URL or place a local preview path in an LMS course.

## Consistency items to address

1. **Air limits in the introductory course.** Intro to OCP Module 3, Lesson 5 currently presents 20–30 kW as an unqualified physical/economic ceiling for air. The new paper uses a different reference envelope and distinguishes acquisition from rejection. Qualify the introductory statement by configuration and thermal conditions rather than substituting another universal number. Its broad efficiency comparisons should likewise be tied to their use-case/date basis.
2. **Malformed catalog link.** Intro to OCP Module 3, Lesson 4 contains a catalog URL ending in `view/3 )`. The source should use the valid catalog URL or verified specific course pages. Repository source line 743 records the malformed value; line 848 contains the air-limit statement.
3. **Shared reliability assumptions.** Deschutes has broad redundancy language, while the paper models shared CDU failure modes in a generic rack. Keep design-specific redundancy and generic annual outage assumptions separate, and qualify claims at the actual component/system fault boundary.
4. **Boiling regimes.** Two-Phase DLC teaches a pool-boiling cold-plate concept and also explicitly acknowledges flow-boiling designs. The paper uses flow boiling as its representative two-phase cold plate and pool boiling for immersion. Teach these as different architectures rather than treating the paper's example as the definition of every two-phase cold plate.
5. **Facility reuse.** The paper emphasizes the new dependencies a boiling-fluid architecture introduces; Two-Phase DLC explains how a CDU can preserve a familiar FWS. State that the TCS/CDU changes and upstream compatibility must be verified. Do not imply the entire facility loop always needs replacement.

This alignment pass establishes curriculum boundaries and identifies source issues; it does not requalify each existing specification or verify the media currently installed inside the LMS.

## Suggested learner path

Learners who need orientation can take the introductory overview first. Thermal Boundaries then supplies the comparative decision framework. Learners choose a specialist course according to their actual next task:

- select, qualify, commission, or maintain single-phase coolant: **Fluids**;
- design or operate a phase-change technology loop: **Two-Phase DLC**;
- assess an open facility-water CDU implementation: **Deschutes**;
- assess liquid-cooled IT in an existing air-cooled site: **Brazos**;
- integrate the rack mechanics or facility envelope: **Open Rack / Open DC**.

Existing specialist-course graduates can take Thermal Boundaries afterward as a synthesis course. There is no need to require every cooling course in sequence.

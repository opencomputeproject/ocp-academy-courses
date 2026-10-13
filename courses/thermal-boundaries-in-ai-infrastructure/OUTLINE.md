# Thermal Boundaries in AI Infrastructure

## Built AcademyWizard Slides course

Build a standalone, narrated course that helps learners diagnose the limiting cooling constraint, explain transition timing, evaluate the economic and reliability evidence, and prepare a deployment across the IT/facility boundary. The organizing idea is the paper's three boundaries and multi-technology toolbox. The curriculum comparison and cross-reference plan are recorded in [CURRICULUM_ALIGNMENT.md](CURRICULUM_ALIGNMENT.md).

- **Shape:** 3 modules, 10 slides each, 30 slides total.
- **Duration:** 32.5 minutes of generated narration; estimate approximately 50–55 minutes of learner time including questions, diagram inspection, and review. Actual module narration is 10:18, 10:51, and 11:18.
- **Audience:** intermediate data-center designers, platform engineers, operators, and technical decision-makers. Assume basic server, rack, and facility vocabulary; introduce cooling-specific terms when first used.
- **Style:** AcademyWizard `Slides`, with the maintained OCP Academy branding and narration settings.
- **Placement:** standalone course. Recommend related cooling courses as follow-on resources without assigning this course to an existing series.
- **Basis:** *Thermal Boundaries in AI Infrastructure*, published version 1.00, October 12, 2026, by Rolf Brink, Mohan J. Kumar, Steve Mills, and Kelley Mullick. Source: [OCP whitepaper](https://www.opencompute.org/wp-content/uploads/2026/10/Thermal-Boundaries-in-AI-Infrastructure.pdf).
- **Status:** course built. The user explicitly waived editorial approval gates and authorized the complete course, ElevenLabs audio, and LMS ZIP on October 12, 2026.

All page numbers below are PDF viewer pages, including the cover. The downloaded PDF has 104 pages.

## Learning outcomes

After completing the course, learners should be able to:

1. Distinguish efficiency, economic, and physics limits, and explain why an incumbent cooling method can remain in use after its economics weaken.
2. Separate package power from heat flux, concentrated heat from distributed heat, and acquisition from transport and rejection.
3. Diagnose which concentrated or distributed load a cooling architecture covers, what remains unresolved, and where complementary methods can help.
4. Evaluate cooling proposals using total cost, failure mechanisms, site constraints, interoperability, and system-level commissioning evidence.

## Module 1 — Why Cooling Transitions Happen

**Approximately 18 minutes.** Explain the paper's boundary framework and adoption argument. Main source: pp. 7–26.

| Slide | Visible title | Teaching purpose | Source |
|---|---|---|---|
| 1 | Why Cooling Transitions Happen | Module title and orientation. | pp. 3, 7 |
| 2 | From Thermal Limits to Deployment Readiness | Course overview: the three modules and the practical decisions they support. | pp. 11, 61–70 |
| 3 | Locate the Binding Thermal Limit | Use a diagnostic example to distinguish total power, local flux, and junction-temperature margin. Briefly recall heat balance and flow penalties only as needed to classify the problem. | pp. 14–17, 32–33 |
| 4 | Three Different Reasons a Method Reaches Its Limit | Classify efficiency, economic, and physics boundaries using the same proposed deployment. Identify the efficiency boundary as a curve's knee rather than a universal percentage. | pp. 18–20 |
| 5 | Read the Avoidance Zone | Interpret the span between economic disadvantage and physical infeasibility; show how its width changes the opportunity and cost of extending the incumbent. | pp. 19–20, 24–25 |
| 6 | Why the Business Case Does Not Set the Clock | Develop the authors' least-disruption law and agency mismatch. Compare the adoption incentives of separate silicon suppliers/operators with vertically integrated organizations. | pp. 21–25 |
| 7 | Preparation Debt and Complexity Debt | Distinguish ecosystem readiness that was deferred from the compounding cost of adding plumbing to cover more components. Use Deschutes' supplier model as an optional follow-on example. | pp. 24–26, 63–64 |
| 8 | Recognize the Limit Before Planning the Transition | Module takeaways. | Module 1 teaching slides |
| 9 | Check Your Boundary and Adoption Reasoning | Narrated, two-question knowledge check. | Module 1 teaching slides |
| 10 | Next: Diagnose the Heat and Match the Architecture | Module completion and introduction to Module 2. | — |

**Knowledge-check concepts:**

- Single-answer: a method holds temperature but loses its total-cost advantage. Which boundary has been crossed?
- Multi-select: which actions reduce preparation debt before a transition? Use supplier readiness, shared interfaces, and trained service capability; distinguish them from simply adding more hardware to extend the incumbent.

**Teaching animation:** on slide 5, move an operating point across a conceptual boundary diagram to show when a method becomes less efficient, less economic, and finally infeasible. Highlight the avoidance zone and the increasing cost of extending the incumbent. A silent short loop supplements the narration; axes and positions are conceptual, not universal thresholds.

## Module 2 — Diagnosing the Heat and Matching the Architecture

**Approximately 18 minutes.** Match the method to the thermal job and explain what each method leaves unresolved. Main source: pp. 27–53, with Appendix B for the cold-plate boundary qualification.

| Slide | Visible title | Teaching purpose | Source |
|---|---|---|---|
| 1 | Diagnosing the Heat and Matching the Architecture | Module title and orientation. | pp. 27, 32 |
| 2 | Thermal Coverage Gaps You Will Diagnose | Objectives: identify the remaining load, locate the limiting thermal step, read a reference design envelope, and propose complementary methods. | pp. 27–53 |
| 3 | A Cooler Processor Can Leave a Growing System Problem | Diagnose the distributed load left after the processor hotspot moves to cold plates; explain how its coverage can become the next constraint. | pp. 27–28, 34–35 |
| 4 | Locate the Limit Along the Thermal Path | Classify acquisition, transport, and rejection problems. Explain why additional downstream capacity cannot fix a failing chip-level acquisition step; locate owners and lifecycle boundaries. Use Brazos and Deschutes only as short contrasting interface examples. | pp. 29–31 |
| 5 | What the Single-Phase Boundary Actually Means | Explain the coupled thermal, hydraulic, and mechanical reference envelope in Appendix B; qualify the approximately 4-kW discussion and identify what must change to extend the architecture. Refer detailed phase-change mechanics to Two-Phase DLC. | pp. 35–44, 84–98 |
| 6 | Match Surface and Volume Methods to Different Loads | Compare load coverage, limiting conditions, and new dependencies across the cold-plate and immersion families. Introduce sensible/latent behavior briefly as needed; keep fluid properties and detailed loop operation in the specialist courses. | pp. 35–52 |
| 7 | Choose Combinations Without Declaring a Winner | Apply the toolbox to a mixed load: retain suitable air cooling, pair surface/volume methods where justified, and introduce microfluidics as an emerging extension. Refer rack manifold and coupling mechanics to Open Rack Module 7. | pp. 35, 52–53, 61 |
| 8 | Match the Tool to the Thermal Job | Module takeaways. | Module 2 teaching slides |
| 9 | Check Your Thermal Architecture Reasoning | Narrated, two-question knowledge check. | Module 2 teaching slides |
| 10 | Next: Evaluate Economics and Readiness | Module completion and introduction to Module 3. | — |

**Knowledge-check concepts:**

- Single-answer: a rear-door heat exchanger accepts more rack exhaust heat. Which step of the paper's thermal path does it help, and which chip-level problem remains?
- Multi-select: which proposed combinations or roles correctly match concentrated heat, distributed heat, and an emerging reduction of the junction-to-coolant resistance stack?

**Teaching animation:** on slide 4, show an acquisition limit persisting while downstream transport and rejection still have capacity, then show the residual distributed load remaining after a cold plate solves the processor hotspot. This diagnostic silent short loop uses the thermal-path framework and avoids recreating the generic nested-loop animations in the existing courses.

## Module 3 — Economics, Reliability, and Readiness

**Approximately 18 minutes.** Evaluate a proposed architecture beyond its ability to hold temperature and identify evidence needed before deployment. Main source: pp. 54–70, with the reliability discussion and Appendix A for model assumptions.

| Slide | Visible title | Teaching purpose | Source |
|---|---|---|---|
| 1 | Economics, Reliability, and Readiness | Module title and orientation. | pp. 54, 61, 65 |
| 2 | Deployment Evidence You Will Evaluate | Objectives: compare full costs, distinguish component failures from common infrastructure outages, read model assumptions, and identify readiness evidence. | pp. 54–70 |
| 3 | Cooling Cost Spans Two Budgets and Two Lifecycles | Trace capital, energy, maintenance, space, repair cost, and possible heat-reuse value across acquisition, transport, and rejection. | pp. 54–60 |
| 4 | Fewer Component Failures Can Still Mean Shared Outage Risk | Explain the cold-plate design-point benefit, the cost of increasing connector count, and shared CDU or tank/row infrastructure dependencies. Separate component failure counts from rack or shared-domain availability. | pp. 37–41, 45–49, 58 |
| 5 | Read the Cost and Reliability Models with Their Assumptions | Use the paper's results to identify what changes the comparison: hypothetical deployment, assumed failure rates, coverage, repair costs, and modeled versus reported fleet evidence. | pp. 39–40, 47–48, 54–60, 79–83 |
| 6 | Match the Toolbox to the Site and the Supply Chain | Apply the framework to a compact AI-rack scenario with a growing residual load and constrained site resources. Identify the decision, evidence, and accountable party. Route Brazos-specific sizing/control and Open DC facility targets to their dedicated courses. | pp. 61–64 |
| 7 | Commission the Handoffs and the Dynamic Response | Evaluate an assembled thermal system across supplier boundaries: realistic faults, balanced flow/pressure, telemetry visibility, load-step response, and jointly agreed, witnessed records. Refer startup/fill/purge procedures to Fluids and Two-Phase DLC. | pp. 65–68 |
| 8 | Prepare the Option Before the Transition Forces It | Course takeaways and a practical decision sequence. | pp. 61–70 |
| 9 | Check Your Deployment Judgment | Narrated, two-question knowledge check. | Module 3 teaching slides |
| 10 | Apply the Framework to Your Next Cooling Decision | Module and course completion, with the complete paper and related Academy courses as continuing resources. | pp. 69–70 |

**Knowledge-check concepts:**

- Single-answer: component tests and a stable full-load temperature have passed. What system behavior remains unproven?
- Multi-select: which evidence supports readiness for a deployment using several cooling methods? Include shared-interface acceptance criteria, materials qualification, observable fault response, and witnessed load-step results.

**Teaching animation:** on slide 7, a conceptual load-step trace connects agreed criteria, the applied change, observed response, and a witnessed record. Fault-response evidence is explained in narration as a separate architecture-specific test. No response time or temperature excursion is asserted as a required numerical criterion.

## Visual approach

The finished course uses source Figure 5 (p. 28), source Figure 19 (p. 60), six original instructional SVG diagrams, a surface/volume comparison table, and three silent teaching animations. Models and reported observations are distinguished in the narration and captions. Animations retain AcademyWizard's default short-loop playback. Source credits and the CC BY-SA 4.0 adaptation notice are linked from the course overview.

The source inventory in `_source_figures.json` records all 19 figures and 13 tables. Final selection, cropping, redraws, and generation are figure-plan decisions.

## Scope and technical treatment

- Teach the paper's least-disruption law as the authors' explanatory framework, with its agency-mismatch exception and facility forcing function. Do not present it as a universal physical law or an exact adoption forecast.
- Use the approximately 4-kW cold-plate discussion only with Appendix B's qualification: it is an architectural transition region for the specified reference configuration, not an intrinsic ceiling on all single-phase liquid cooling. The reference uses 5 L/min water flow, a 35°C inlet, a 30-mm flow length, and a 10°C coolant-rise constraint.
- Treat reliability improvements, failure rates, rack-power trajectories, and TCO values according to their declared evidence basis. Do not turn model outputs, estimates, extrapolations, or reported fleet ceilings into deployment guarantees.
- Keep regulatory and working-fluid constraints at the decision-factor level. Any current region-specific requirements would need separate verification when writing the course.
- Keep the commissioning coverage at the paper's system-readiness level; detailed procedures and numeric acceptance criteria require additional sources.
- Explain the heat-balance and heat-flux equations conceptually. Keep the historical device catalog, probability derivations, detailed cold-plate geometries, and complete cost-input tables as optional reading.
- Refer learners to existing **Cooling Fluids in Direct Liquid Cooling (DLC)** and **Two-Phase Direct Liquid Cooling Efficiencies and Fluids** courses for fluid selection, chemistry, and operating practices.
- Treat **Project Deschutes** and **Project Brazos** as brief contrasting implementation examples. Keep their performance tables, component designs, control behavior, and service procedures in their own courses.
- Use the specific cross references in [CURRICULUM_ALIGNMENT.md](CURRICULUM_ALIGNMENT.md) at the teaching point where they help. The older overview is optional preparation, and external courses are not required to answer the new course's checks.
- Preserve architecture distinctions across sources: the existing Two-Phase course covers both pool- and flow-boiling cold-plate designs; the paper describes representative regimes. A changed TCS/CDU does not automatically require replacement of the upstream FWS.
- Keep component redundancy, shared failure domains, and modeled annual outage rates separate. The paper's generic CDU assumptions are not measurements of Deschutes or Brazos.
- Each module retains the standard title/overview-or-objectives, five teaching slides, takeaways, narrated two-question knowledge check, and completion pattern. Checks require an attempt on both questions and permit retry.

## Build intake still to confirm

The proposal assumes an intermediate audience, roughly 50–55 minutes, and the standard OCP Academy palette. Before scaffolding the course, confirm those choices and the course output folder. The build's narration availability and target-LMS packaging/navigation must also be established at intake. No narration scripts, paid media, rendered course, or upload package have been generated by this proposal.

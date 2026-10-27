# Thermal Boundaries in AI Infrastructure

**Placement:** standalone OCP Academy course.

The formal catalog fields are stored in `course.json.lms_catalog` and exported separately in [lms-catalog.md](lms-catalog.md) and `lms-catalog.json`. Use those exports for LMS catalog entry; the notes below also describe the upload assets and behavior.

**Short description**

Diagnose AI cooling limits, evaluate architecture tradeoffs, and prepare for a cooling transition.

**Overview**

Cooling choices affect the compute you can deploy, the sites that can support it, and the cost of operating it. Based on the OCP whitepaper *Thermal Boundaries in AI Infrastructure*, this intermediate course helps you diagnose limits, compare architectures, and prepare a supported cooling transition.

**Module 1 — Why Cooling Transitions Happen | Approximately 18 minutes**

Distinguish efficiency, economic, and physics limits. Explore the avoidance zone and explain why an ecosystem can delay a cooling transition. Examine who controls the design, who bears the cost, and how preparation debt differs from the complexity of extending an incumbent architecture.

**Module 2 — Diagnosing the Heat and Matching the Architecture | Approximately 18 minutes**

Trace heat acquisition, transport, and rejection to find the limiting step. Distinguish processor hotspots from distributed system heat, interpret the paper's reference cold-plate envelope, and match surface and volume methods to the loads they cover. Consider how complementary approaches can solve remaining gaps.

**Module 3 — Economics, Reliability, and Readiness | Approximately 18 minutes**

Evaluate full ownership cost across IT and facility lifecycles. Separate component reliability from shared outage exposure and assess modeled results against their assumptions. Identify the interfaces, responsibilities, and witnessed load and fault tests needed to demonstrate deployment readiness.

**Total estimated learning time: 50–55 minutes**, including narration, knowledge checks, diagram inspection, and review. Narration alone totals 32.5 minutes.

Designed for data-center designers, platform engineers, operators, and technical decision-makers with basic server, rack, and facility knowledge. Links to related OCP Academy courses provide optional routes to specialist detail; no other course is mandatory.

**Upload assets**

- LMS package: `build/thermal-boundaries-in-ai-infrastructure.zip` (from the repository root)
- Catalog poster: `thumbnail.png` — exactly 800 × 400 pixels.
- Format: SCORM 1.2, with Course Home and three separately tracked module entries.
- In Docebo, leave forced sequencing disabled to retain unrestricted syllabus order.

Use the LMS Syllabus to open each tracked module. The maintained first-module start action is a direct page link; it does not switch the SCORM tracking session to a different SCO. Verify the intended launch and completion behavior in the actual LMS before release.

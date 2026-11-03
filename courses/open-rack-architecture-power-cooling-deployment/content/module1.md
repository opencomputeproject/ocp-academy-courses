# Module 1 — Open Rack Architecture and the Open Ecosystem

## 1 | Open Rack Architecture and the Open Ecosystem
- An open platform for data center racks, power and cooling.
Narration:
Welcome to Open Rack. Developed through the Open Compute Project, Open Rack is an open platform for data center racks, power distribution, and equipment interfaces. Its shared designs help organizations build efficient, scalable computing infrastructure.

We'll begin with Open Rack's origins and the ideas behind it, then explore its key features and the power and cooling systems that support today's demanding workloads.

## 2 | Your Route Through the Seven Modules
- Architecture → ORv3 interfaces → deployment evidence
- High-power racks → scaling power → Open Rack Wide
- Liquid cooling → integrated readiness review
Narration:
The seven modules follow one engineering review, from defining the workload to deciding whether a complete rack is ready. You'll examine interfaces, calculate usable power, compare architectures, and identify missing evidence. Expert walkthroughs and technical animations bring these ideas to life. The core path is designed for about two hours and twenty-five minutes. Specialist Academy courses offer optional deeper study.

## 3 | Start with the Workload, Then Define the Rack
- Specify sustained demand, excursions and operating conditions.
- Include equipment mix, service access and growth.
- Convert requirements into verifiable interface limits.
Narration:
A rack choice starts with what the deployment must do. Specify the equipment population and its expected operating envelope, rather than choosing a frame and hoping the workload fits. Sustained demand, short excursions, cooling conditions and acceptable behavior during a fault can lead to different designs even at the same advertised rack power.

Next, identify the constraints that equipment creates. Weight and center of gravity affect support and handling. Cable and hose routes affect installation and service. Heat that isn't captured by liquid still needs an air path. A maintenance strategy may require access that an otherwise compatible layout obstructs.

Turn these needs into a requirements sheet with measurable conditions and an owner for every unresolved item. For example, a cooling requirement should identify the permitted operating conditions and the interface where they're guaranteed, not just say liquid cooled. Keep the initial design envelope explicit. Later modules will use it to distinguish a product that looks suitable from a deployment with enough evidence to proceed.

## 4 | From ORv1 to ORv3 and ORW
- Shared interfaces enable equipment and infrastructure to evolve.
- ORv3, high-power designs and ORW address different constraints.
- A generation label is not a universal capacity rating.
Narration:
Open Rack evolved as operators sought shared interfaces and more flexible infrastructure. The useful history is the sequence of constraints, not a list of dates. A shared mechanical arrangement helps equipment integrate. Rack-level power distribution changes where conversion and distribution hardware sit. Increasing density makes electrical, thermal and service boundaries more demanding.

Open Rack version three, or O R V three, is our main starting point. High-power rack implementations extend the power architecture for heavier loads. Open Rack Wide, or O R W, expands the mechanical envelope to support different equipment packaging and integration needs. These are related developments, not interchangeable names for one rack with ever-larger ratings.

The animation builds this progression around the constraint each step addresses. Notice that changing the frame doesn't automatically validate its electrical system, and adding power doesn't establish cooling capacity. We will use version and implementation names precisely throughout the course. When a claim includes dimensions, mass or power, the next question is which document, configuration and revision make that claim true.

## 5 | The Rack as a System of Interfaces
- Mechanical: locate, support and retain equipment.
- Electrical and thermal: deliver energy and remove heat.
- Management and service: observe, control and maintain the system.
Narration:
Think of the rack as a system of interfaces. The mechanical interface locates and supports equipment, but also reserves clearance for connections and removal. Electrical interfaces define how power reaches that equipment and what behavior is permitted during connection, operation and faults. Thermal interfaces define the conditions under which heat can leave.

Management adds another boundary: what is measured, which controller can request a change, and who owns the response. Service ties the interfaces together. A replaceable item isn't practically serviceable if removing it strains an energized connection or blocks an adjacent cooling circuit.

The figure reveals each boundary separately, then brings them together. This is a conceptual map, not a wiring drawing. Use it to ask a precise question at each handoff: what does one side provide, what does the other side require, and what evidence shows agreement? A shared rack family can reduce integration work, but it doesn't eliminate these questions. The resulting interface review is the organizing tool we'll carry through the remaining modules.

## 6 | Base Specifications, Implementations and IT Gear
- Base specification: shared interface requirements.
- Implementation specification: a particular design and its limits.
- IT gear guide: integration guidance, not a replacement for requirements.
Narration:
Not every document in a rack project has the same authority. The base specification establishes shared interfaces within its scope. An implementation specification describes a particular design, including choices that the base leaves open. A design guide helps equipment authors apply those interfaces, but its guidance isn't automatically a new mandatory requirement.

The O R V three I T Gear Design Guide makes this distinction explicitly: firm requirements reside in the base specification. Read the relevant requirement and its applicability before treating advice as a pass or fail criterion. Likewise, don't transfer a dimension or payload from an implementation document to the entire Open Rack family.

During a review, record the exact document, revision and supporting page. Then connect the claim to the supplied product and its configuration. A supplier can reasonably implement an allowed option without matching another operator's design. The task is to establish which interfaces must agree, which choices are permitted, and whether the selected equipment is qualified together. This prevents both unnecessary rejection and unsupported compatibility claims.

## 7 | Follow Energy In and Heat Out
- Follow power across the facility, rack and equipment boundaries.
- Trace liquid and residual air heat to their receiving systems.
- Assign an owner and an acceptance condition to each handoff.
Narration:
Follow the energy path into the rack, then follow the heat out. Power passes through conversion and distribution stages before reaching the workload. Each stage has limits, losses, protection behavior and an operating envelope. A rating at one stage doesn't establish what reaches the equipment after every other constraint is applied.

For cooling, identify both the liquid path and the residual air path. The rack may connect to a coolant distribution unit, or C D U, with a separate facility-side loop. Don't assume those fluids, pressures or temperatures are interchangeable. A thermal boundary needs a defined condition and a responsible party on each side.

This first map doesn't require detailed electrical or hydraulic calculations. It requires the boundaries to be visible. Mark where the facility commitment ends, where the rack integrator's responsibility begins, and what the equipment supplier assumes. If two parties each assume the other provides the same function, the diagram has exposed a real integration risk. Resolve that gap before turning individual component ratings into a system claim.

## 8 | One Rack Family, Different Implementations
- ORv3 identifies an interface family, not one bill of materials.
- HPR and ORW choices change the review envelope.
- Compare actual configurations and document revisions.
Narration:
Two racks can share an interface family and still differ in consequential ways. External dimensions, equipment supports, power-shelf arrangements, cooling integration and handling features may depend on the implementation. A compatible connection in one location doesn't make every part of the two systems interchangeable.

High-power designs may separate power equipment from the I T rack or use different distribution arrangements. A wider rack can change equipment packaging, but it also changes the site route and service envelope. These choices have to be reviewed as a configuration, not assembled from the most attractive rating in each document.

For a useful comparison, hold the deployment requirements constant. Ask each supplier to identify the product revision, supported equipment population, operating conditions and evidence for those conditions. Record deliberate differences rather than hiding them beneath a common O R V three label. A family name helps you find the right starting documents. It cannot replace the configuration-specific review needed to accept a rack into service.

## 9 | Modularity Becomes an Operational Benefit
- Shared boundaries can separate upgrade and replacement cycles.
- Multiple sources still require qualification and revision control.
- Reuse benefits depend on condition, compatibility and service evidence.
Narration:
Modularity matters when it changes an operational decision. If equipment can evolve without replacing the supporting infrastructure, an operator may extend useful life or choose between qualified suppliers. Shared interfaces also make repair and staged upgrades easier to plan.

These benefits are conditional. A replacement part must meet the relevant mechanical, electrical, thermal and management requirements. A later revision can change behavior even when the connector still fits. Reuse therefore needs condition assessment and documented compatibility, not just the absence of visible damage.

Consider replacing one equipment generation while retaining the rack and power distribution. Mechanical fit is only the first check. The new equipment may draw a different peak current, reject heat differently or need additional telemetry. The retained infrastructure must support the new envelope, including the agreed fault case. Treat modularity as a way to create options with evidence. It is not permission to mix unqualified assemblies, and it doesn't remove the need to control revisions throughout the deployment's life.

## 10 | Read the Evidence Before the Marketing
- Requirement, guidance, product claim and roadmap are different evidence classes.
- Recognition applies to a named product and status.
- Verify the configuration, conditions and limits behind a result.
Narration:
A requirement, a product claim and a roadmap answer different questions. A requirement states what a scoped design must meet. A test report describes observed behavior under particular conditions. A roadmap describes intended future work. None should silently substitute for another.

The same discipline applies to recognition. Use the precise status recorded for the named product in the O C P Marketplace or contribution record. Don't turn recognition into a blanket certification of every possible rack configuration or supplier combination. Check what was actually reviewed and what remains the integrator's responsibility.

Summit material is especially useful for understanding emerging constraints and engineering approaches. We'll use twenty twenty-six examples, but distinguish published contributions from reference designs, prototypes and future plans. When a result matters to acceptance, ask for the current design revision, test configuration, boundary conditions and outstanding limitations. That information makes the evidence actionable. A compelling diagram or a large headline rating alone doesn't establish readiness for your deployment.

## 11 | Design Review Case: Define the Deployment Envelope
- Case: a dense accelerator deployment with liquid cooling and a growth requirement.
- Review power, thermal, payload, route and service evidence separately.
- Use Go, Conditional Go or Hold only with explicit reasons and owners.
Narration:
Our running case is a dense accelerator deployment with liquid cooling, constrained site access and a requirement to grow. It is a teaching scenario, not a specification for a real installation. The team has a rack proposal and several attractive component ratings, but hasn't yet demonstrated that the complete configuration meets its operating envelope.

Start an evidence record with five headings: mechanical and payload, power, thermal, site route, and service and control. For each, record the requirement, proposed solution, supporting evidence and unresolved issue. An unresolved issue needs an owner and a closure condition, not a vague assurance that it will be handled later.

At each stage we'll choose go, conditional go or hold. Conditional go means a bounded next activity is permitted with explicit restrictions; it doesn't mean commissioning is approved. Hold means a missing or conflicting item blocks the requested activity. Pause and identify one question you'd ask under each heading. We'll refine those questions as the interfaces and failure cases become concrete.

## 12 | The Rack Decisions You Can Now Frame
- Select the governing document before accepting a claim.
- Review the complete configuration, not its family label.
- Make every boundary and unresolved assumption visible.
Narration:
The essential habit is to connect every important claim to a defined configuration and its evidence. Keep the workload envelope, interface boundaries and document authority visible. That gives the next review a concrete starting point rather than a collection of unrelated ratings.

## 13 | Check the Architecture Mental Model
- Submit both questions to continue; retry after reviewing the explanations.
Narration:
Apply the distinction between a shared interface and a validated deployment. Submit each question once to continue. Correctness isn't required, and you can retry after reading the explanations.

## 14 | Next: ORv3 Interfaces
- Trace the mechanical, power and cooling interfaces that must agree.
Narration:
You've established the review framework. Next, we'll use it to examine the O R V three interfaces and the mismatches a family label can hide.

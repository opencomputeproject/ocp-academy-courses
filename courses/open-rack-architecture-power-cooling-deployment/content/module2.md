# Module 2 — ORv3: Mechanical, Power and Cooling Interfaces

## 1 | ORv3: Mechanical, Power and Cooling Interfaces
- Support fit, power delivery and cooling compatibility are separate checks.
Narration:
We'll trace the interfaces that make an O R V three configuration work. The goal is to recognize what must agree, where the requirements live, and which evidence is still missing after equipment appears to fit.

## 2 | The Interface Checks You Will Make
- Read the reference geometry and distinguish OpenU from RU.
- Trace power entry, protective bonding and thermal handoffs.
- Identify a mismatch before it becomes an integration failure.
Narration:
You'll review mechanical reference geometry, trace the power and thermal paths, and evaluate a mixed-equipment proposal. Keep each interface check independent. Passing one doesn't automatically pass the others.

## 3 | Read the Frame from Its Datums
- Datum: the reference used to locate a feature.
- Check the specified option, tolerances and mating geometry.
- Reserve keep-outs for connections, tools and service movement.
Narration:
Mechanical compatibility depends on reference geometry, not just overall width. A datum is the reference used to locate a feature. When two drawings use different references, apparently similar dimensions can describe different positions. Read the datum, orientation and tolerance before comparing numbers.

The O R V three base specification allows alternative frame geometries and leaves external dimensions to the rack developer. The shared interfaces still have to agree. Identify the selected option and use its drawing consistently. Don't combine one option's support geometry with another option's connection location.

A keep-out is reserved space, not unused space available for an extra bracket. It can protect connector travel, tubing movement, tools or a replacement path. Check the equipment in its installed and service positions, including accumulated tolerances and allowable deflection. A tray can rest on its supports while its rear interfaces are outside their permitted alignment. Treat the source drawing as the controlling geometry; the simplified course figure is a reading aid, not a fabrication drawing.

## 4 | OpenU and RU Are Different Grids
- OpenU pitch: 48 mm.
- EIA rack-unit pitch: 44.45 mm.
- Supports, mounting patterns and occupied height must agree with the selected grid.
Narration:
Open U and the conventional rack unit are different vertical grids. The O R V three base specification describes forty-eight millimeter Open U spacing and forty-four point four-five millimeter rack-unit spacing. The difference accumulates across a stack, so these labels aren't interchangeable ways to count height.

The selected rack features, supports and equipment mounting arrangement determine what can be installed. An adapter can address a defined mechanical interface, but it doesn't automatically establish the power connector location, service access or cooling arrangement. Review those separately.

For a mixed-equipment proposal, mark the grid used by each item and the reference used to locate its connections. Check both the occupied envelope and the required installation movement. Avoid inferring compatibility from the number printed next to U on a product sheet. The practical outcome is a stack arrangement that is supported and aligned at every required interface, rather than a height total that happens to fit inside the frame.

## 5 | From Power Shelf to IT Gear
- Conversion feeds rack distribution, then the equipment's power-entry circuitry.
- The 48 V architecture has revision- and design-specific operating values.
- Review the complete path; do not add unrelated ratings.
Narration:
Follow power from the shelf into rack distribution and then into the equipment. A power shelf converts its input and supplies the distribution path. The busbar carries current to the equipment connection. Power-entry circuitry controls how the equipment accepts that input. Every part has an operating envelope.

The forty-eight volt architecture name doesn't mean every cited design uses exactly forty-eight volts as its nominal output. The base specification includes defined voltage options; the high-power shelf example we'll use later specifies a fifty volt output. Match the equipment's accepted range to the actual source and revision rather than substituting the architecture label for a voltage requirement.

As the path builds in the animation, notice that the available capacity is constrained by more than the supply units. Connections, busbars, thermal conditions and the equipment entry can impose tighter limits. A larger source can't make an underspecified downstream connection adequate. Record power at a defined boundary, together with the stated operating and fault conditions. We'll use that same discipline when calculating usable capacity.

## 6 | Blind-Mate Power Needs a Sequence
- Blind mate means the connection is made without direct access to the mating interface.
- Alignment and retention remain required.
- Power-entry control must follow the specified connection and removal behavior.
Narration:
Blind mating removes the need to reach the connection directly, but it doesn't remove the need to control alignment or electrical behavior. The equipment must reach the permitted mating condition, remain retained, and leave that condition in a controlled way.

For the O R V three input interface, the specification describes use of the power-sense line to control power-entry circuitry. Equipment must not begin powering on before the connector is fully asserted, and it must power off before removal to prevent arcing events. This is a requirement-level sequence, not an instruction to reproduce an unspecified internal circuit.

Check the equipment implementation against the actual connector and power-entry requirements. Don't infer a particular precharge circuit, contact timing or safe live-service procedure from a conceptual sequence. Connector and power-monitoring specifications provide supporting detail, but the rack-level decision is whether the selected interfaces and controls establish the required behavior together. Mechanical fit alone can't prove it. The responsible electrical review and qualification remain necessary.

## 7 | Protective Bonding Is Not the DC Return
- Protective earth and chassis bonding serve a protective function.
- DC return belongs to the operating power circuit.
- Follow the cited implementation; never infer an arbitrary bond.
Narration:
Protective bonding and the direct-current return are different functions. Protective earth and chassis bonding establish protective connections among accessible conductive parts. The D C return carries operating current in the power circuit. A common word such as ground can hide that distinction.

The high-power shelf implementation includes a specific grounding scheme. Read that scheme and the applicable rack requirements together; don't invent a connection between the return and chassis simply because the frame is bonded. A simplified diagram that merges the two paths would teach the wrong mental model.

In an integration review, identify the conductors, their intended functions, the connection points and the responsible design authority. Verify continuity and fault behavior through the approved engineering and acceptance process. This course doesn't provide installation or live-work instructions. The key decision is to stop an ambiguous grounding claim before it becomes an undocumented wiring choice. If the proposed assembly differs from the cited implementation, obtain a design-specific review rather than assuming the original diagram still applies.

## 8 | A Rack Needs an Air Path as Well as a Liquid Path
- Liquid cooling does not imply zero air-side heat.
- Preserve airflow, blanking and containment where required.
- Check cable routing and service states for obstructions.
Narration:
A liquid-cooled rack can still reject substantial heat to air. Components outside the liquid-cooled path, power conversion and other equipment may depend on airflow. Determine the actual heat split from the selected equipment and operating conditions; don't assume a universal percentage.

Follow the air from its intended inlet to its outlet. Blanking and containment can prevent bypass or recirculation, but only if the installed configuration preserves those boundaries. Cable bundles, accessories and temporary service arrangements can obstruct the path or open unintended gaps.

Review normal operation and the allowed degraded conditions. A cooling proposal must state what remains supported if a fan, liquid path or receiving system changes state. Neither a liquid connection nor a rack-level heat rating proves that each component remains within its limits. Ask for the equipment heat-rejection requirements and the site's commitment at the relevant boundary. The aim is a complete thermal path, including the air-side remainder, rather than a liquid-only diagram that leaves some heat with nowhere demonstrated to go.

## 9 | Trace the Rack Cooling Interfaces
- Equipment ↔ couplings ↔ manifold ↔ CDU or receiving loop.
- Distinguish technology-side and facility-side fluid conditions.
- Match materials, temperature, flow and pressure requirements.
Narration:
Trace the cooling path from the equipment through its connections and manifold to the receiving loop. A coolant distribution unit may separate a technology cooling system from a facility water system. Those boundaries can have different fluid chemistry, pressure and temperature conditions.

The animation reveals each handoff without implying that every installation has the same topology. At each connection, identify which side provides the required conditions and how they are verified. Matching a coupling size isn't enough: materials, fluid specification, pressure limits and the operating temperature range must also agree.

Flow requirements apply at defined conditions. The receiving system must provide the required hydraulic performance for the configured circuit, while heat rejection must support the permitted operating envelope. Avoid swapping a pump rating for evidence at the equipment boundary. We'll study the cooling interfaces and service evidence in more depth in module seven. For now, the essential result is a complete loop map with no hidden assumption about where the heat, pressure or fluid-compatibility responsibility goes.

## 10 | Preserve Access While Routing Cables and Hoses
- Keep installation, replacement and tool envelopes clear.
- Respect routing, bend, support and strain requirements.
- Evaluate the complete populated rack, not an empty-frame picture.
Narration:
A clean empty-frame layout can become unserviceable when populated. Cables and hoses occupy volume, need support and move during installation or replacement. Their permitted routing and bend conditions belong in the configuration review, not in an improvised field arrangement.

The I T Gear Design Guide includes access and keep-out guidance around blind-mate equipment and tubing. Use the relevant drawing and supplier limits to check the actual layout. Reserve the tool and hand access required by the approved service method. Don't route a new bundle through an envelope needed to remove another item.

Review the densest permitted configuration and the service movement, not only the final resting position. Check that strain isn't transferred into a coupling or electrical connection when adjacent equipment moves. Then identify who owns changes after deployment. A routing improvement for one subsystem can undermine another subsystem's access or airflow. Serviceability is therefore a shared interface requirement, not a cosmetic preference to consider after all capacity decisions are complete.

## 11 | Interface Review: Does This Mixed Equipment Fit?
- The tray rests correctly, but a rear connection is outside its allowed position.
- The hose route occupies the replacement envelope.
- Resolve both mismatches before declaring the configuration compatible.
Narration:
Consider a mixed-equipment proposal. The tray sits on the correct supports and its height fits the selected grid. The proposal calls that compatible. A closer review finds the rear connection outside its permitted location, and a hose occupies space needed to remove an adjacent item.

The animation separates support fit, connection fit and service fit. The first passes; the others don't. Increasing insertion force doesn't correct the reference geometry. Moving the hose into an electrical keep-out would merely exchange one mismatch for another.

The supported decision is to hold this integration activity until the connection and routing are resolved through an approved design. Record the drawing revisions and the evidence needed to close each issue. A revised arrangement may be acceptable, but it must be checked across all affected interfaces. Pause and state what evidence would change your decision. That habit prevents an appealing physical fit from standing in for a complete integration review.

## 12 | The Interfaces That Must Agree
- Geometry establishes more than overall dimensions.
- Power-entry behavior, bonding and cooling need their own evidence.
- Service access must survive the populated configuration.
Narration:
Keep support, connection and service fit separate. Match the actual voltage and thermal envelopes, preserve the intended bonding functions, and verify access with the rack populated. A passed check narrows uncertainty; it doesn't waive the remaining checks.

## 13 | Check the Interface Decision
- Submit both questions, then use the feedback to examine the missing evidence.
Narration:
Decide which mismatch blocks integration and which checks remain after mechanical fit. Submit both questions once. You can retry after feedback; correctness isn't required to continue.

## 14 | Next: Deploying ORv3
- Turn interface requirements into a defensible supplier and acceptance review.
Narration:
Next, we'll use these interface checks to compare implementations and build a traceable deployment evidence record.

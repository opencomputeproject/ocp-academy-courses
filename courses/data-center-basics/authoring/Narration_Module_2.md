# Module 2: Data Center Physical Infrastructure — approved narration

## Slide 1: Data Center Physical Infrastructure

Module two: Data Center Physical Infrastructure. Computing equipment needs a continuous supply of power and a way to release heat. You'll follow those supporting systems through the facility and see why electrical, thermal and physical constraints have to be considered together.

## Slide 2: Trace Power, Heat and Physical Constraints

By the end of this module, you'll be able to trace a conventional power path, explain the purpose of backup systems, and describe how cooling moves heat out of the equipment. You'll also compare hot and cold aisle containment and recognize why free floor space doesn't guarantee room for another workload.

The goal is a system view: a deployment works only when the supporting systems can accommodate it together.

## Slide 3: A Tour of the Physical Systems

Imported recording: uses its own audio; no separate slide narration.

## Slide 4: White, Grey and Black Space

# Approved editorial revision · Leo / Eleven v4
White space is the area used for information technology equipment: servers, storage and networks. It can include equipment close to the load, such as rack power connections and cooling distribution units. A raised floor is not required. Grey space usually describes the electrical and mechanical infrastructure that supports that equipment, such as switchgear, uninterruptible power systems, pumps and cooling plant. Black space is less consistently defined. In the three-zone example here, it means the site and utility interface, including substations and site energy infrastructure. Other organizations use the label differently, including for connectivity or broader support areas. Confirm the site's definitions. The important relationship is practical: power must reach the equipment, and heat must leave it through the cooling system. A system's function does not change simply because it sits across a color boundary.

## Slide 5: How Power Reaches the Data Hall

Imported recording: uses its own audio; no separate slide narration.

## Slide 6: Follow the Power Path

In a conventional example, the normal supply passes through distribution and an uninterruptible power supply, or U P S, before reaching equipment. If the incoming source fails, stored energy can bridge the transition while a backup generator starts.

The animation illustrates that sequence. Actual designs differ, and backup operation depends on capacity, fuel, controls and maintenance. A generator alone doesn't mean there can be no interruption at the equipment.

## Slide 7: Power Shelves Feed Rack DC Busbars

# Approved editorial revision · Leo / Eleven v4
Alternating current and direct current describe electrical current, not where conversion must happen. In many hyperscale and Open Rack deployments, conversion is centralized in a rack power shelf. Modular rectifiers convert the incoming A C supply into D C. In the Open Rack version three example, a nominal forty-eight-volt D C busbar runs along the rear of the rack. A busbar is a substantial conductor that distributes power; it does not perform the conversion. Compatible servers connect through blind-mate contacts as they slide into position. Equipment then uses D C to D C regulation to produce the lower voltages its components require. This architecture removes individual server power cords, simplifies installation and front-access servicing, and pools rectifier capacity across equipment. That can reduce stranded capacity and improve utilization and conversion efficiency at suitable operating loads. Higher distribution voltage also reduces current and resistive loss compared with lower-voltage D C at the same power and conductor resistance. Conventional A C-fed racks still supply A C to each server's own power supply, which converts it there. Both architectures exist. Check the voltage, connector, capacity and redundancy design; a busbar alone does not guarantee efficiency or availability.

## Slide 8: How Cooling Removes the Heat

Imported recording: uses its own audio; no separate slide narration.

## Slide 9: CRAC and CRAH Move Room Heat Out

# pronunciation: CRAC = crack; CRAH = craw; D X = direct expansion
Cooling moves heat from equipment to the outdoor environment. Two common room-cooling units handle the air, but pass its heat into different systems.

A computer room air conditioner, or crack unit, commonly uses direct expansion. Warm return air passes over a refrigerant coil. A compressor-driven refrigerant circuit carries that heat to its heat-rejection arrangement, such as an outdoor condenser.

A computer room air handler, or craw unit, passes return air over a chilled-water coil. The water carries heat back to the facility cooling plant. There is no refrigeration compressor in the air handler itself. The plant must still reject the heat outdoors.

Both units use fans to deliver cooled supply air back toward equipment inlets. They recirculate room air; the air doesn't have to leave the building. Follow the actual heat path, because equipment names alone can be imprecise.

## Slide 10: Keep Supply Air Apart from Exhaust

# pronunciation: CRAC = crack; CRAH = craw
A crack or craw unit supplies cooled air and receives warm return air. Containment helps those two streams reach their intended destinations.

Cold-aisle containment encloses the cool supply side between equipment fronts. Warm exhaust leaves the equipment into the surrounding return space. Hot-aisle containment encloses the warm exhaust side behind equipment, guiding it toward the cooling unit's return path. Cool supply reaches equipment fronts from outside that enclosure.

Either arrangement can work with a crack or craw system. Choose for the room's airflow paths, equipment orientation and operating access. Containment reduces mixing; the cooling coil, fans and connected heat-rejection system still have to do their jobs.

## Slide 11: Containment Reduces Air Mixing

# pronunciation: CRAC = crack; CRAH = craw
Follow the room air circuit. A crack or craw unit sends cooled supply air to the equipment. The air absorbs heat as it passes through the equipment, then warm return air travels back to the unit.

At the coil, heat leaves the air. A crack unit transfers it into refrigerant; a craw unit transfers it into chilled water. The connected system carries the heat onward for rejection outdoors. The cooled air returns to the supply side.

Now compare a mixing path. Some warm exhaust can recirculate toward equipment inlets. Containment separates that exhaust from the supply stream and guides it toward the cooling unit instead.

A barrier creates no cooling capacity. Verify equipment inlet conditions, adequate airflow and working cooling controls.

## Slide 12: Effective Infrastructure Works as a System

Imported recording: uses its own audio; no separate slide narration.

## Slide 13: An Empty Rack Is Not Spare Capacity

A rack may have open slots while its available electrical or thermal capacity is already committed. It may also lack suitable network connections, weight capacity or service access for the proposed equipment.

Before adding a workload, check the budgets together. Space tells you where equipment might fit. Power, heat removal, connectivity and access tell you whether it can operate and be maintained there. The first exhausted constraint can limit the whole deployment.

## Slide 14: Liquid Cooling Adds a Heat-Transfer Path

# Approved Astra content update · Leo / Eleven v4
Follow the heat from a component. A cold plate transfers it into circulating equipment coolant. The warmed coolant carries that heat to a heat-transfer interface. In this liquid-to-liquid example, a heat exchanger transfers energy into a separate facility coolant loop. The two fluids remain separate. The cooled equipment coolant returns to the cold plate, while the facility system carries the heat onward for rejection to the environment. An alternative liquid-to-air arrangement transfers the equipment-loop heat into room air. That can support some retrofits, but the room cooling system must still remove the added heat. The alternatives are not simultaneous steps in one route. A coolant distribution unit may manage circulation and heat exchange; it is not a place where heat disappears. Confirm equipment compatibility, liquid and air capacity, and the complete heat-rejection path.

## Slide 15: Open Interfaces Help Teams Coordinate

A rack's requirements cross organizational boundaries. Equipment designers, facility teams and suppliers need compatible electrical, mechanical and thermal interfaces.

Current community work on eight hundred volts direct current is an example of aligning requirements for demanding deployments. It is a developing option, not a statement that every facility should replace its existing alternating-current infrastructure. The broader lesson is that common interfaces can make different parts of a system easier to coordinate.

## Slide 16: Reliable Operation Requires the Whole Chain

Power delivery and heat removal are connected parts of one system. Backup sources and energy storage have different roles. Airflow separation helps cooling do useful work, and liquid cooling adds another path for moving heat.

Free space is only one part of deployment capacity. Before changing the equipment, consider electrical delivery, thermal conditions, connectivity and service access together. That system view is the foundation for understanding what happens inside a rack.

## Slide 17: Check Power Conversion, Distribution and Continuity

# Approved editorial revision · Leo / Eleven v4
Use three questions to check the power path. First, identify the function of a conventional A C-input server power supply. Then distinguish conversion in a rack power shelf from distribution through a D C busbar. Finally, recall what supports equipment while a backup generator starts. Submit each answer and read the explanation. Match each component to its job and evaluate the complete design, rather than assuming one piece of hardware guarantees continuity.

## Slide 18: Next: Inside the Rack

Thank you for completing Data Center Physical Infrastructure. You can now follow the power and heat-removal paths and recognize why deployment constraints belong together.

Module three brings that understanding into the rack. You'll interpret equipment dimensions, compare its roles and consider how a practical layout supports operation and maintenance.

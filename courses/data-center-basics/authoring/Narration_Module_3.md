# Module 3: Inside the Rack — approved narration

## Slide 1: Inside the Rack

Module three: Inside the Rack. A rack organizes equipment into a practical physical system. You'll use its dimensions to interpret a layout, distinguish equipment roles and recognize the constraints that remain even when there are empty mounting positions.

## Slide 2: Read a Rack Layout and Its Constraints

By the end of this module, you'll be able to distinguish rack width from vertical rack units, recognize common compute and storage arrangements, and explain why power, cooling, cabling and access shape a layout.

You'll also see how Open Rack uses a different mechanical system. This module introduces the vocabulary. The Intro to OCP courses provide the broader architecture and community context. For a deeper look at rack design, mechanical interfaces and power delivery, continue with the Open Rack course series on OCP Academy.

## Slide 3: Rack Equipment Overview

Imported recording: uses its own audio; no separate slide narration.

## Slide 4: What the 19-Inch Dimension Measures

In the conventional nineteen-inch system, the nominal dimension describes the equipment front-panel width, including its mounting ears. It doesn't describe the cabinet's outside width, its depth or the distance between the centers of its mounting holes.

Those are different dimensions. The common horizontal hole-center spacing is about eighteen point three one two inches. When checking fit, use the equipment and rack drawings rather than treating every measurement as nineteen inches.

## Slide 5: Rack Units Measure Vertical Allocation

A rack unit, written U, describes vertical allocation. One U has a pitch of one point seven five inches, or forty-four point four five millimeters. Two U and four U reserve two and four times that vertical pitch.

Actual front panels include clearance, so their manufactured height is slightly smaller than the nominal allocation. The unit tells you how much vertical space is reserved. It doesn't tell you the equipment's compute performance, drive count, power demand or workload.

## Slide 6: Compute Comes in Many Chassis

A compact server may use one U, while other designs place multiple independent nodes in a shared chassis. General-purpose and accelerator systems can reserve more space for processors, memory, devices, airflow or liquid-cooling connections.

The illustrated one U, two U and four U arrangements are examples. A two-node chassis doesn't automatically deliver twice the useful performance of another system. Workload behavior and the actual processor, memory, storage and interface configuration determine what the equipment can accomplish.

## Slide 7: Storage Designs Balance Access and Capacity

Storage equipment is organized around the information it must hold and how it must be accessed. N V M E, short for Non-Volatile Memory Express, defines how host software communicates with non-volatile memory. Compatible enclosures support fast access to solid-state storage. Capacity-focused servers can provide many drive positions for large datasets, backup or archives.

The illustrated layout includes a high-bay enclosure of four U or more. That is one design example, not a rule for every storage system. Compare capacity, access performance, interfaces, protection and service needs rather than choosing by height alone.

## Slide 8: Shared Chassis and Utility Nodes Have Distinct Roles

A blade system groups replaceable compute modules within a shared chassis. Power, cooling or other supporting functions may be shared, depending on the product. That arrangement affects both density and the consequences of a shared-component problem.

A utility or management node is identified by its role: monitoring, backup coordination or another service. Its physical appearance alone doesn't establish what it controls. Read the system function and its dependencies alongside the rack position.

## Slide 9: Equipment Choice Consumes Several Budgets

Adding equipment changes more than the number of empty rack positions. It can increase electrical demand, heat-removal requirements and network traffic at different rates.

In this illustrative animation, the cooling allocation reaches its limit while mounting space remains available. The values explain a relationship, not a recommended rack design. The practical lesson is to identify the limiting budget before deciding that another device can be installed.

## Slide 10: Cables and Airflow Need Their Own Space

# Approved Astra content update · Leo / Eleven v4
A layout must support the equipment's intake and exhaust directions and leave room for the cables and connections it needs. Crowded cabling can obstruct airflow or make a component difficult to reach.

Service access also matters when equipment moves on rails or a connection must be replaced. Follow the equipment's physical requirements rather than assuming every device has the same front-to-rear arrangement. A tidy-looking layout still needs to work during maintenance. A network interface connects the server to a network. Switches connect devices and carry traffic within the facility. Routing moves traffic between networks, and some equipment combines these functions. Check compatible interfaces, link capacity and the complete path as well as the physical cable route.

## Slide 11: Physical Security Supports Serviceability

Racks can help control access to equipment, especially where several customers share a facility. Doors, access permissions, asset identification and service procedures work together to support that control.

A locked rack doesn't replace system security, monitoring or authorization for changes. People still need a safe, traceable way to perform legitimate work. Consider who can enter the area, reach each device and connect to its management interfaces, and how their work is recorded.

## Slide 12: Open Rack Is a Different Mechanical System

Open Rack uses a different equipment-space and mechanical approach from the conventional nineteen-inch system. Its commonly described twenty-one-inch equipment space should not be confused with the cabinet's outside width.

Open Rack also uses the Open Unit, which is distinct from the conventional U. Shared power and service arrangements are part of the broader architecture. This vocabulary prepares you for the Intro to OCP series, where the evolution and version-specific design receive a fuller explanation.

## Slide 13: Interpret the Layout Before Adding Hardware

A team finds several unused positions in a rack and proposes adding a compute system. The new equipment fits mechanically, but the cooling allocation is already committed and its network connection requires a different interface.

What should the team investigate before proceeding? Check the proposed system's electrical, thermal, connectivity and service requirements against the available capacity. The right response may involve another rack, a changed configuration or an infrastructure upgrade. Empty positions alone don't resolve those constraints.

## Slide 14: A Rack Is More Than a Stack of Servers

Rack dimensions make equipment arrangements repeatable, but they don't determine what every device does. Front-panel width, vertical allocation and cabinet dimensions answer different questions. Compute, storage and shared-chassis designs come in many sizes.

A workable layout also respects power, cooling, cabling, service access and authorized entry. Carry those constraints together when interpreting a rack. They connect the equipment's physical arrangement to the reliable service the facility must support.

## Slide 15: Check Rack Dimensions and Installation Fit

First, distinguish a rack's nominal panel width from its other dimensions. Then consider a server whose stated height fits the available rack space. Decide what that height allocation establishes and which installation checks still remain.

Use specified product dimensions and the rack's power, cooling and access constraints. Submit both questions and review the explanations before continuing.

## Slide 16: Next: Management and Trends

Thank you for completing Inside the Rack. You can now interpret dimensions and equipment roles while keeping deployment constraints in view.

Module four connects that physical system to ownership, day-to-day management and resource efficiency. You'll consider how teams decide what to improve and how emerging technologies change those decisions.

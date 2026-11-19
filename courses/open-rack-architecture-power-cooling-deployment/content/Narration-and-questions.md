# Open Rack · English narration and questions

Each heading is a learner-controlled slide; the linked text is its spoken script. The quiz questions and their feedback appear below the quiz narration.

## Module 1 · Inside Open Rack

10 slides · approximately 16 minutes including figure study and the knowledge check.

### 1.1 · Welcome to Open Rack

Welcome to Open Rack, from OCP Academy. Picture a row of servers in a data center. What holds them up? Where do they get their power? The answers start with the rack. Open Rack is the Open Compute Project's approach to designing that shared space. It publishes the dimensions and connections so different teams can design servers, switches, and power equipment for the same rack.

In this course, you'll meet two members of the family: Open Rack version three and Open Rack Wide. We'll start with the frame, then explore what people have built inside it.

[Recording script](../audio/module1/slide_01_welcome_to_open_rack.txt)

### 1.2 · Four views of the rack

We'll look at the same hardware from four angles. First we'll take the equipment out so we can see what the frame provides. Then we'll put a server and a network switch back in and look at the space each one needs. Once the equipment is running, we'll follow electricity to it and heat away from it. Finally we'll compare real designs, from an empty frame to a system with dozens of connected processors. A good question to carry through all four views is this: which decisions did the equipment designer inherit, and which were still theirs to make?

[Recording script](../audio/module1/slide_02_course_overview.txt)

### 1.3 · Read the front and rear views

Stand at the open front of our example rack. Most of what you see is empty air. Now pick one rail and follow it toward the back. There's a partner at the same height on the opposite side. Together they carry the tray's weight as it moves in. The vertical members carry that load down through the frame. The electrical connector at the back has another job entirely. It isn't a shelf for the tray to rest on.

Now turn the rack around in your mind. From the rear you can see a vertical busbar assembly, with a supply path and a return path. From this angle it's easier to picture how trays at several heights can draw power from the same assembly. At the end of its travel, our tray makes its electrical connection out of sight of the person at the front. That's what blind mating means here. It describes how two parts meet, not whether a tray can be removed while energized.

Come back around to the front. The tray face is still within reach. A person can get to the handle and to connections placed on that face. That's why a side view alone tells only part of the story: it can show where the tray lands, but a front view can show whether another cable lies right across the handle.

[Recording script](../audio/module1/slide_03_front_and_rear.txt)

**Visual:** The rails carry the tray; the rear contacts carry current.

### 1.4 · One connection, two designers

Suppose one team builds the frame and a second team designs a server. Give the frame team a drawing of the place where the server gets its power. A dimension on that drawing makes sense only if both teams measure from the same reference. Think of marking a position on a bookshelf: “ten centimeters in” is ambiguous until you say which edge you started from.

The frame team positions the rack-side assembly relative to the equipment opening. The server team positions the mating connector relative to the surfaces that locate its tray. Put the two drawings together at those reference surfaces. When the tray reaches its intended position, the two halves should line up. A drawing also has to allow for small variations in manufactured parts; lining up two perfectly drawn centerlines is only the beginning.

Consider a part that never appears on either drawing of the power connector: the latch on the front of the tray. A technician needs to reach that latch when the rack is full. On a bench, the designer can put a hand on it from almost any angle. Put another tray immediately above it and dress the network cables across the front, and the same latch can be hard to reach. The tray hasn't moved, and the electrical drawing is still correct. What changed is the space available to the person doing the work.

The version-three IT gear design guide makes just this distinction. It shows a recommended latch area, but tells the developer to consider the actual cabling and access to neighboring equipment. A suggested latch position is not a requirement to buy a particular latch. A team comparing two proposals can ask each designer to show how someone would release the tray with the neighboring slots occupied. That gives both teams the same problem to solve without demanding identical hardware.

There are two useful documents on the table now. For a disputed interface requirement, go to the base specification. For help understanding why a shape or clearance might work, turn to the design guide and check its assumptions. That distinction matters when a designer has a better way to solve a problem: departing from an example and departing from a requirement are very different decisions.

That's the useful meaning of open in this example. Both teams can consult a published description of the boundary between their designs. The server team can change the layout of a board inside the tray without asking the frame team to move the busbar, provided the equipment still meets the relevant requirements. Conversely, a frame maker can change a detail outside the equipment opening without giving every server designer a new connection point. Sharing an interface preserves some choices precisely by settling others.

[Recording script](../audio/module1/slide_04_shared_interface.txt)

**Visual:** The front latch helps seat the chassis in the rack. The insets show the latch and the release. ORv3 IT Gear Design Guide, Fig. 2.3.1 (upper view, cropped), CC BY-SA 4.0.

### 1.5 · A family of equipment spaces

Open Rack version one and version two are earlier chapters in the same story: treat the rack as a place where equipment can share infrastructure, and publish the boundaries that let different contributors work on it. Version three carries that idea forward. The family resemblance is useful, but it doesn't mean a tray from an earlier generation automatically fits or takes power from the next one. For a specific pairing, the relevant interface is more informative than the family name.

Now look at the wider opening. Imagine laying out several processor boards side by side. If you can spread them across a broader tray, you have a different set of choices about their neighbors, their connections, and how much vertical space the assembly occupies. You also have a wider piece of equipment to support and service. Width provides an option; the equipment designer decides how to use it.

One way to make the change across generations tangible is to consider liquid cooling. The version-three design guide describes a solution in which the connections for coolant meet as the tray goes into position. That's called blind mating: the technician isn't reaching behind the tray to join those connections by hand. For that to work, the tray, its valves, and the rack's coolant manifold have to agree on where they meet. Specifying the frame alone wouldn't give an older tray the missing valves, or turn an unplumbed rack into a liquid-cooled one.

Now picture a team moving existing equipment into a wider frame. The new opening offers more space, but the old tray doesn't get wider with it. What carries the tray on either side? Where does it stop when fully inserted? At that point, does its connector actually meet the power connection? Those questions apply even if there is generous room all around the equipment. Empty space is not a mounting arrangement.

Treat reuse as a question about particular parts, not a yes or no judgment about a whole generation. A design might retain a familiar electrical interface while changing the brackets needed to reach it. Another team might develop a new full-width tray specifically for the wider format. In the first case the evidence you want is a supported mounting arrangement for that equipment. In the second it's the drawing for the new tray.

Keep two questions separate as we go. How much physical room is there for equipment? And how much power can the assembled system deliver to it? A wider equipment envelope answers the first question. The second depends on actual electrical components and their configuration. A high-power version-three design needn't have a wide opening, and the width of an Open Rack Wide drawing doesn't tell you the available kilowatts.

[Recording script](../audio/module1/slide_05_family_lineage.txt)

**Visual:** Extra width and extra electrical capacity answer different design questions.

### 1.6 · Three frames you can compare

Here are the names behind three actual frame drawings. The first is Meta's Open Rack version three implementation. The second is Google's Open Rack version three implementation. Both are approved frame contributions to the Open Compute Project. These are concrete designs, with dimensions you can measure, rather than two names for the base specification. The third drawing shows the Open Rack Wide frame developed by Meta and Rittal.

Look first for something all three have to do. Find the opening for the equipment, then the structure on either side. Each frame has to support its intended payload and position it where it can meet the other parts of the rack. Now compare the outside edges of the Meta and Google version-three frames. They don't have the same width. That can be true even when the two frames provide for the same equipment interface: the outer edge of the base isn't the edge of the tray.

Imagine two people using these drawings for different jobs. One lays out a row of racks. The other works out whether a technician can bring a replacement tray to the front of one rack and slide it home. Give the first person only the equipment opening and they can't lay out the row. Give the second person only the outside width and they can't decide whether the tray will seat. Both people asked for the width of the rack; neither made a mistake. They needed dimensions between different surfaces.

Depth makes the distinction especially clear in Google's contribution. Its table gives dimensions for the base rack and distinguishes two depth options. The text also explains that accessories can change the overall depth and height. Suppose a proposed installation has a fixed clearance behind the row. A dimension labeled base rack depth is a useful starting point, but it doesn't describe the assembled rack in front of you. Identify the option, establish which accessories are fitted, then use the outline of that assembly to check the clearance.

Meta's contribution offers a way to practice the same reasoning from the other direction. Side panels, cable management, and doors appear in its section on optional accessories. Seeing a door illustrated there tells you a door is described for that design. It doesn't tell you that the rack someone ordered will arrive with one. For that answer, you need the selected configuration.

In the third drawing, look inside the uprights again. This time the equipment space itself is wider. That's a different kind of difference. One comparison was between two manufacturers' implementations of version three. The other crosses from version three into Open Rack Wide. We'll return to the dimensions and mounting options later; for now, notice which pair of edges you're comparing.

[Recording script](../audio/module1/slide_06_contributed_frames.txt)

**Visual:** Compare the outside edges first, then the openings inside the uprights.

### 1.7 · From a frame to AMD Helios

Take the equipment away from a frame drawing and you can still learn about the opening, the supports, and the places where assemblies attach. Now look at AMD's Helios rack-scale reference design, which is based on Open Rack Wide. Rack-scale means that the designers are treating the equipment in the rack as one coordinated system. Several trays doing useful work together are a different subject from the structure carrying those trays.

Start at the compute trays, where processors perform the calculations. If the work spans processors, the processors need connections to exchange data. That's why networking belongs in the system picture. The running equipment also releases heat, so the design has to provide a path to carry that heat away. These relationships would be invisible in a drawing that showed nothing but the frame.

Take a single calculation and imagine dividing it among several processors. Each processor can work on its own portion. At some point the partial results need to come together before the next stage can begin. A processor that's finished early may have to wait for data from elsewhere in the rack. If you had only a list of processors and their individual speeds, you would know something about the arithmetic each could do. You wouldn't yet know how quickly this particular job could advance from one stage to the next.

That's a useful reason to distinguish a physical arrangement from a connection diagram. The physical arrangement shows which trays occupy which positions. The connection diagram shows which devices exchange data and through what equipment. Two devices can sit next to one another and still exchange data through a switch somewhere else. Moving their labels closer together on a drawing doesn't eliminate that trip. For a question about communication, follow the connections, not the distance between labels.

Cooling calls for yet another view of those same trays. Follow the heat from a device into its cooling hardware and ask where it goes next. In a liquid-cooled system the coolant carries heat away from the device; the heat still has to pass onward to a system that can remove it. The useful handoff on this drawing is between cooling systems, not between processors. Each view explains a different part of what makes the rack work as a whole.

Read the labels in order. Open Rack Wide describes shared interfaces. The Meta and Rittal drawing illustrates a particular frame. Helios describes a rack-scale design based on the wider architecture. Don't read those labels as a parts list: the frame we just examined is an example, not a claim that every Helios supplier uses that exact model.

[Recording script](../audio/module1/slide_07_helios_system.txt)

**Visual:** An interface locates equipment; a rack-scale design explains how that equipment works together.

### 1.8 · What does the drawing describe?

Before you read a dimension, ask what the drawing describes. On a frame drawing, trace the structure that carries the equipment. On an equipment drawing, trace the outline of the item that goes into the frame. On a populated system drawing, trace a connection between two items and ask why the system needs it. A rail location, a tray outline, and a connection between processors can all appear in the same picture. They answer different questions. The shared interface is the part of the agreement that lets those drawings meet.

[Recording script](../audio/module1/slide_08_three_drawing_types.txt)

### 1.9 · Check your understanding

First, choose the detail that two independent teams need to share for a tray to meet its frame. Then compare two frame drawings and select all the features that can differ while preserving the specified equipment interface. Submit an answer to both questions to complete the check. You don't need to get them right to continue. Read the feedback after each submission, and try again if you'd like to test your reasoning.

[Recording script](../audio/module1/slide_09_knowledge_check.txt)

**Question 1:** Which measurement locates the tray’s power connector?

- Where the processor sits on the server board
- Its position relative to the tray supports **(correct)**
- The overall width across the outside of the frame base

Yes. A common reference lets each team position its half of the connection so the two halves meet when the tray is seated.

**If incorrect:** Look for the measurement that locates one mating part relative to the other, not an unrelated dimension.

- Where the processor sits on the server board: The processor can move within the tray without moving the tray’s mating connector. Think about where the two teams’ parts touch.
- The overall width across the outside of the frame base: The base can extend beyond the equipment opening. Its outside width alone does not locate the tray connector.

**Question 2:** Two racks fit the same tray. What can differ? Pick two.

- The rack’s outside width **(correct)**
- The rail spacing the tray needs
- Whether the rack has a front door **(correct)**
- Where the tray’s power contacts must meet

Yes. The Meta and Google frames have different outside widths, and Meta offers a front door as an option. Neither feature sets where the tray sits or plugs in.

**If incorrect:** Think back to the frame drawings: the tray needs its rails and power contacts in the right places. The frame can be wider on the outside, and a front door is optional.


### 1.10 · Next, design from the tray outward

Next we'll move to the equipment designer's side of the drawing. We'll slide in a server tray, then put a network switch in position and fill its ports with cables. Watch for the moment when an item fits neatly in the rack but the person who needs to reach it runs out of room.

[Recording script](../audio/module1/slide_10_equipment_designers_view.txt)

## Module 2 · How servers and switches fit into the rack

17 slides · approximately 15 minutes including figure study and the knowledge check.

### 2.1 · One server tray, one network switch

Welcome to module two. What makes a server or a network switch fit a rack? A metal box can slide neatly into an opening and still miss its power connection. A switch can bolt up perfectly, yet leave a cable that's nearly impossible to unplug. We'll follow the equipment through those moments. First comes the tray on its way into the rack. Later we'll look at what happens when everything around it is in use.

[Recording script](../audio/module2/fresh/slide_01_server_and_switch.txt)

### 2.2 · Four questions about fit

Think of the front, side and overhead drawings as three views of the same machine. Each lets you answer a question the others leave open. What carries the weight? Where do the electrical contacts meet? Which openings have to stay clear for cooling? And what space does a hand or a piece of equipment need when it moves?

You don't need to memorize a list of rack dimensions. The useful skill is knowing when to turn the drawing. A front view tells you a great deal about the face of a switch. It tells you very little about the connector at the far end of a server.

[Recording script](../audio/module2/fresh/slide_02_four_questions.txt)

### 2.3 · Where the tray stops

Follow the small contact at the back of the blue tray. Its partner, the busbar, stays with the rack. The rails can already carry the weight of the server while there is still daylight between those two pieces. It's the last part of the tray's travel that brings them together.

Compare the two stops. On the left, the tray reaches the position where its clip engages the busbar. On the right, the stop catches the tray a little earlier. The server still feels firmly seated, but its connector hasn't traveled far enough. That's why a blind-mate connection uses a common mechanical reference. Nobody has to reach behind the tray to join the contacts by hand; the guides and the final position have to do that work.

[Recording script](../audio/module2/fresh/slide_03_where_the_tray_stops.txt)

**Visual:** The rails support the tray before the clip reaches the busbar. Compare the two stop positions.

### 2.4 · Where do the mounting ears land?

The nineteen inches in a conventional rack-mount instrument are measured across its front panel, from the outside of one mounting ear to the outside of the other. The box behind that panel is narrower. Look at the small bolt holes in the ears. They sit in from the ends. Those holes need rails immediately behind them, not a cabinet wall nineteen inches away.

Google's version-three frame has mounting features inside its walls for add-on kits. With the Open Rack kit, a twenty-one-inch-format tray sits on supports arranged at OpenU positions. With the EIA kit, the instrument's ears fasten to rails inside that same frame. Follow the outside posts as the view changes: they stay put. It's the hardware between the posts and the equipment that changes. The ears themselves stay nineteen inches across.

[Recording script](../audio/module2/fresh/slide_04_where_do_the_mounting_ears_land.txt)

**Visual:** A 19-inch panel spans its ears. An EIA kit brings mounting rails to those ears inside the same Google frame. Chassis drawing: ORv3 IT Gear Design Guide, Fig. 1.1 (cropped), CC BY-SA 4.0.

### 2.5 · Turn the drawing: contact and depth

Look at the shelf stop from the side. Google marks one reference for the stop and another for the busbar. The stop limits a tray's travel. A tray designed for blind mating has its electrical contact positioned to meet the busbar at that point. The close-up shows the two halves: the clip belongs to the equipment, the bar to the rack. A device with a cord inlet keeps that inlet, regardless of which rails support it.

Depth needs a pair of endpoints, too. Google's table gives standard and extended depths for its EIA rails. The tray dimensions below use different endpoints: six hundred thirteen millimeters to the front panel, six hundred thirty-five to the handle. That extra twenty-two millimeters describes a projecting handle. It doesn't make the supporting rails longer.

[Recording script](../audio/module2/fresh/slide_05_turn_the_drawing_contact_and_depth.txt)

**Visual:** Google’s example tray is 613 mm deep to the front panel and 635 mm to the handle. Neither measurement is the depth of its supporting rails.

### 2.6 · Does the rear support reach?

Imagine holding this instrument by its front panel. The front ears tell you exactly where the face will sit, but not how the weight at the far end is carried. This particular instrument has a rear attachment. In the side view, you can trace a line from that attachment to the rear rail.

Now compare the extended rail position. The face still lands in the same place. The rear rail is farther away, and the instrument hasn't grown a longer attachment to reach it. A device designed to mount only at the front is a different case: there is no rear attachment to line up. Start with the way that particular enclosure is supported. Then ask a separate question about power: what inlet is on the device, and what supplies it?

[Recording script](../audio/module2/fresh/slide_06_does_the_rear_support_reach.txt)

**Visual:** An instrument can match at the front and still miss its rear support. Check the device’s own mounting arrangement.

### 2.7 · Two rulers: OpenU and rack units

Start both rulers at zero. The next mark on the Open Rack ruler is forty-eight millimeters up. That's one OpenU. The next mark on the conventional rack-unit ruler is forty-four point four five millimeters up. Those numbers describe the repeat distance between mounting positions. They aren't measurements of the sheet metal that forms a server.

Now follow the fourth marks across. Four OpenU pitches reach one hundred ninety-two millimeters. Four conventional rack units reach one hundred seventy-seven point eight. The difference is fourteen point two millimeters, even though the starting positions matched exactly. Align the tops instead and the mismatch moves to the bottoms. When a drawing says a chassis uses four units, knowing which ruler the designer used is part of knowing where the next chassis can go.

[Recording script](../audio/module2/fresh/slide_07_two_rulers_openu_and_rack_units.txt)

**Visual:** Align the two zero marks. After four positions the grids are already 14.2 mm apart.

### 2.8 · When cables hide the middle latch

Pick out the center plug. With one cable connected, the release latch is easy to see and there's room to press it. Fill the neighboring ports and the plugs still sit neatly in a row. The trouble starts a little farther from the switch face, where the cables turn toward their guide.

In the first route, the bundle crosses the middle latch. The center link can keep working perfectly well, so the problem might only show up when someone needs to change that cable. What if we give the cable a sharp corner to clear the latch? A line on a drawing will take that turn. A real cable needs a curve at least as broad as its specified minimum bend radius. A better route has to make room for both the curve and the release.

[Recording script](../audio/module2/fresh/slide_08_when_cables_hide_the_middle_latch.txt)

**Visual:** Populating the adjacent ports changes what a hand can reach.

### 2.9 · Give the plug a way out

Follow the two groups of cables out toward opposite sides of the switch. Between them is a clear approach to the middle plug. There's room to press the release, the cable bends are broad, and the air opening below the ports is still exposed.

Now watch the plug move. It's possible to leave enough space for a fingertip but too little for the connector body as it slides out. Here the whole plug travels clear while the neighboring links stay in place. That moving outline is a useful way to compare two otherwise tidy-looking cable layouts. The point isn't that every switch needs a left guide and a right guide. It's that the connector, its release, the nearby cables and the vent all need room in the installed arrangement.

[Recording script](../audio/module2/fresh/slide_09_give_the_plug_a_way_out.txt)

**Visual:** Follow the middle plug as it comes free. Its neighbors and the air opening stay clear.

### 2.10 · How much space moves with a canister?

A canister is a removable carrier. In this Open Rack Wide example, the carrier holds several pieces of equipment, and they move together. Look first at the solid outline: that's where it sits in the rack. The dashed region marks space it can occupy on the way out.

Choose one corner of the front handle and follow it toward the aisle. It starts farther forward than the box, and it stays ahead of the box throughout the movement. A neighboring part can be clear of the seated equipment and still lie directly in that corner's path. The useful drawing is therefore bigger than the equipment footprint. It includes the handle and the intermediate positions of the populated carrier, not just a rectangle at each end of its travel.

[Recording script](../audio/module2/fresh/slide_10_how_much_space_moves_with_a_canister.txt)

**Visual:** In this example, the dashed region shows where the entire carrier, including its handle, travels during withdrawal.

### 2.11 · Does the neighbor’s hose cross that path?

From above, the blue hose crosses the carrier's withdrawal path. That tells us where to look, but not yet whether the two touch. Open the side view at that crossing. Here the hose passes above the moving assembly. Two lines that intersect on paper are separated in height.

Try the opposite case in your mind: lower the hose until it sits at the same height as the projecting handle. The overhead picture barely changes, but now the handle meets the hose partway out. That's the value of keeping the two views together. The plan locates the crossing. The side view tells you whether the clearance is real at that place in the motion. The hose belongs to the neighbor, so it doesn't travel out with this canister.

[Recording script](../audio/module2/fresh/slide_11_does_the_neighbor_s_hose_cross_that_path.txt)

**Visual:** Trace the hose in plan, then check its height at the crossing. Crossing lines on paper need not mean a collision.

### 2.12 · Can a finger release the neighboring plug?

Shift your attention from the whole carrier to one small moving part: the release latch on the neighboring plug. The hose can clear the carrier's withdrawal path and still sit right above that latch.

In the blocked arrangement, you can see the top of the plug. What's missing is the room to bring a finger in and operate the release. In the other arrangement the plug hasn't moved, but the hose passes farther away, leaving the space above it clear. One test was about the path of a loaded carrier. This one is about a hand and a few millimeters of latch movement. Both belong in a service view, even though they're quite different in scale.

[Recording script](../audio/module2/fresh/slide_12_can_a_finger_release_the_neighboring_plug.txt)

**Visual:** A plug can be visible while the space needed to operate its latch is occupied.

### 2.13 · Why a compute job needs a switch

Why does a compute job need a switch? Imagine two accelerators working on different parts of the same calculation. The first has finished its part, but the second needs that result before it can continue. The result is ready. It just isn’t where it’s needed yet.

Follow the result from the first accelerator to the switch. The switch forwards the data along the link to the second accelerator, which can now use it. That’s the distinction between the two jobs: the accelerators do the calculation, and the switch gets data to the participant that needs it. In a tightly coupled group, that exchange is what the scale-up network is for.

[Recording script](../audio/module2/fresh/slide_13_why_a_compute_job_needs_a_switch.txt)

**Visual:** One accelerator sends a partial result through a switch to the accelerator that needs it.

### 2.14 · Scale up inside; scale out between systems

Look inside one of the outlined groups. Its accelerators exchange data to work together closely on a job. That's the scale-up network. Now follow the link across the gap to the other group. Each group already has its own internal connections. Joining separate systems or groups so work can extend across them is the scale-out role.

The distinction is easier to remember by naming the endpoints than by memorizing the names of switches. Are we connecting participants inside one tightly coupled group, or connecting that group to another system? An Ethernet link can serve either kind of conversation. Its location in a wide rack, or the fact that it uses Ethernet, doesn't decide which one we're looking at.

[Recording script](../audio/module2/fresh/slide_14_scale_up_inside_scale_out_between_systems.txt)

**Visual:** Follow the endpoints: a link within an accelerator group does a different job from one joining separate systems.

### 2.15 · Three views of equipment fit

Here's a quick way to read an unfamiliar equipment drawing. Start at the front: find the mounting points, the ports and the openings for air. Turn to the side: follow the supports to the stop and see what meets at the back. Then pick one thing that has to move and trace it all the way out.

Those three views can lead to three different answers. A tray can mount correctly, miss its rear contact, and leave its front ports perfectly accessible. Being precise about which part fits is more useful than a simple yes or no.

[Recording script](../audio/module2/fresh/slide_15_three_views_of_equipment_fit.txt)

### 2.16 · Knowledge check: stops and access

One question puts you beside a tray at its stop. The other puts you in front of a cabled switch. Use the view that matters in each case. Submit both answers to continue. You can read the feedback and try again; you don't need a perfect score to move on.

[Recording script](../audio/module2/fresh/slide_16_knowledge_check.txt)

**Question 1:** A tray is correctly supported and guided, but the stop is too close to the aisle. What is the likely consequence?

- The rear power connector may stop short of full engagement. **(correct)**
- The vertical pitch between the supports becomes smaller.
- The connector will be fully engaged because the tray is supported.

Yes. The stop ends travel before the rear connector reaches its designed position.

**If incorrect:** Follow the tray along the rails: the change is to its final position, not its height.

- The vertical pitch between the supports becomes smaller.: The stop sets travel along the supports. It doesn't move the supports closer together vertically.
- The connector will be fully engaged because the tray is supported.: Support carries the weight. It does not prove that the contacts reached their mating position.

**Question 2:** Which two parts move when you unplug a latched cable?

- The release latch **(correct)**
- The plug you’re removing **(correct)**
- The plugs in nearby ports
- The switch chassis

Yes. Press the latch, then pull the plug straight out. The switch and nearby plugs stay in place.

**If incorrect:** First press the latch to release the plug. Then slide that plug out without moving the switch or the plugs beside it.


### 2.17 · Next: follow the power and the heat

You've followed a tray into place and a cable back out. Next we'll follow two things that move while the equipment stays still: the electricity that reaches a processor, and the heat that leaves it.

[Recording script](../audio/module2/fresh/slide_17_next_power_and_heat.txt)

## Module 3 · What changes as racks carry more power and heat?

21 slides · approximately 17 minutes including figure study and the knowledge check.

### 3.1 · Power in, heat out

Welcome to module three. Picture a processor halfway up a rack, about to start a job. Its power arrives through a chain of equipment that reaches all the way back to the building. Its heat leaves by a different chain. We'll follow both. Along the way, we'll look at why a high-power rack might have a neighbor devoted entirely to power, and why a liquid-cooled server can still need air.

[Recording script](../audio/module3/fresh/slide_01_power_in_heat_out.txt)

### 3.2 · What you’ll be able to trace

Three questions will guide us. Where does alternating current become direct current? How much output can the power shelf sustain if one supply is unavailable? And once that power reaches the electronics, where does the heat go?

Try to keep track of what actually crosses each boundary. A cable carries electrical current. A coolant line carries warm fluid. At a heat exchanger, heat can cross from one circuit into another even though the fluids stay on their own sides. Following what crosses is often more revealing than memorizing the names on the boxes.

[Recording script](../audio/module3/fresh/slide_02_objectives.txt)

### 3.3 · From the AC whip to the tray

Start at the cable entering the shelf. It's an AC whip: a cable assembly that carries alternating current from the facility to the rack's power equipment. Meta's sixty-amp high-power whip is one example for Open Rack version three. The sixty amps describe the cable assembly's current rating. To know the output available to equipment, we need to go farther along the drawing.

Inside the shelf, power supplies convert the input to direct current, or DC. The shelf delivers that output to the busbar. Each tray makes its own connection to that shared conductor assembly. Conversion inside the tray then provides the voltages its electronics need. Trace the route backward and you'll encounter two quite different connections: the tray contact that takes DC from the busbar, and the whip that brings AC into the shelf.

[Recording script](../audio/module3/fresh/slide_03_from_the_ac_whip_to_the_tray.txt)

**Visual:** The whip carries AC. The supplies convert it; the busbar distributes DC.

### 3.4 · Same energy, different peak power

Suppose each of two jobs draws one kilowatt for an hour. Give them an hour together and each still uses one kilowatt-hour of energy. But during that hour, the shared supply has to deliver two kilowatts. That's the taller stack in the picture.

Now run the jobs one after the other. The work takes two hours, and each job still uses one kilowatt-hour. The two jobs together still consume two kilowatt-hours. Their combined demand just never rises above one kilowatt in this example. Think of the height of each block as power and the width as time. The total area stays the same when the blocks move apart. The height of the stack does not. A daily energy total alone can't tell you the peak output a rack supply had to deliver.

[Recording script](../audio/module3/fresh/slide_04_same_energy_different_peak_power.txt)

**Visual:** Two example jobs consume the same energy whether their run times overlap or not. Their peak combined demand changes.

### 3.5 · Where are you measuring power?

A meter at the input to the shelf and a meter at the tray can both be working correctly and report different numbers. The shelf converts power, and some of the input becomes heat in the converter. The busbar and contacts deliver power onward. By the time it reaches the tray, you're looking at a different boundary. To estimate losses, compare input and output over the same interval and account for all the loads between the two meters.

Don't add the shelf input to the tray reading to find the total: much of that energy went past both meters. And notice the separate line from the shelf chassis. That's a protective bond for exposed conductive metal. The drawing separates it from the path carrying the equipment's normal load current.

[Recording script](../audio/module3/fresh/slide_05_where_are_you_measuring_power.txt)

**Visual:** The same energy passes several measurement points. Protective bonding is separate from the normal load-current path.

### 3.6 · Six supplies, five required

Count the supply positions in the high-power rack version-two shelf. There are six installed units, and each is rated at twelve kilowatts. Add up all six nameplates and you get seventy-two kilowatts of installed capacity.

The specified dual-cord configuration is rated for sixty kilowatts of sustained output with N plus one redundancy. Here's why the arithmetic changes. Set one twelve-kilowatt block aside in the count. Five remain, and five times twelve gives sixty. The sixth unit provides one supply's worth of margin. It doesn't have to sit idle in normal operation; the installed units can share the load. The question isn't which physical unit is called the spare. It's whether the remaining units can still carry the specified output when one is unavailable.

[Recording script](../audio/module3/fresh/slide_06_six_supplies_five_required.txt)

**Visual:** Six 12 kW supplies are installed. The specified dual-cord N+1 output is 60 kW.

### 3.7 · Monitoring is not another power supply

Find the smaller position alongside the six supplies. It's the power monitoring module, often called the PMM. It reports conditions at the shelf. Its measurements can help explain what the supplies are doing, but they don't add a seventh block of power to the capacity calculation.

A buffer has a third job. When the load briefly wants more power than the incoming path is providing, stored energy can help cover the difference. Watch what happens to the energy reserve while that mismatch continues: it goes down. Once spent, it must be replenished. So read a shelf drawing three ways. Count supplies for sustained output. Locate monitoring for information. Look for a store of energy when the question is how long a temporary mismatch can be covered.

[Recording script](../audio/module3/fresh/slide_07_monitoring_is_not_another_power_supply.txt)

**Visual:** The monitoring module reports conditions. Stored energy covers a temporary mismatch, not a higher sustained load.

### 3.8 · What ORv3 HPR and ORW share

Put the mounting detail for the high-power version of Open Rack version three beside the one for Open Rack Wide. Focus on the attachment points, rather than on the entire outline of each assembly. The Wide base specification shares the busbar mounting interface with the version-three high-power rack. A frame designer and a busbar designer can therefore work from a common set of attachment features.

Now move your attention away from the mounting holes and along the conductor. The shared interface hasn't told you its cross-section, its operating temperature, or how much current that particular assembly can carry. That's a useful distinction in an open design: two teams can agree exactly where one part fastens to another without having to make all the metal on either side identical.

[Recording script](../audio/module3/fresh/slide_08_what_orv3_hpr_and_orw_share.txt)

**Visual:** Compare the attachment points, not the whole conductor assembly.

### 3.9 · Same mounts, different conductors

The copper-colored rectangles represent cross-sections: imagine looking straight at the cut end of each conductor. Make the second one twice as wide while keeping its thickness the same. It now has twice the cross-sectional area. For this comparison, hold the material, length and temperature constant.

The larger conductor has about half the electrical resistance. At the same current, it would produce about half as much resistive heat along that length. None of that required the frame's mounting holes to move. It also doesn't establish a new current rating on its own. To assign a rating, a designer needs to know how hot the assembly gets in service and how that heat can escape. A pair of familiar mounting points answers a mechanical question; the conductor and its surroundings answer the thermal one.

[Recording script](../audio/module3/fresh/slide_09_same_mounts_different_conductors.txt)

**Visual:** In this example only cross-sectional area changes. Matching the mounting holes does not establish a current rating.

### 3.10 · Mt. Diablo moves conversion next door

Which rack contains the power shelves? So far, we've pictured the shelves in the same frame as the servers. Mount Diablo separates those jobs. The rack on the left holds power equipment. The one on the right holds the computing equipment it serves. The neighboring power rack is often called a sidecar.

Start at the incoming feed, follow it into the conversion shelves, then cross the link between the two racks. That link delivers direct current to the IT rack. Power still has to reach each tray, and local electronics still provide the voltages the processors use. What changed is the address of the upstream converter. If you look only at the photograph of the computing rack, some of the equipment that makes it work is literally out of the picture.

[Recording script](../audio/module3/fresh/slide_10_mt_diablo_moves_conversion_next_door.txt)

**Visual:** The sidecar feeds DC across to the IT rack. The processors stay in the IT trays.

### 3.11 · What changes on the floor plan?

Look at the space shaded for conversion equipment. In the first layout, that space is inside the IT rack. A power shelf and a server tray are different pieces of equipment, but both draw on the available space in that frame. In the second layout, the conversion shelves occupy a neighboring floor position. More positions inside the IT frame can now be available for compute equipment.

Which layout makes better use of space? It depends on what space you're counting. Measuring only the height freed up inside one rack leaves out the footprint of the sidecar. Counting only rack footprints leaves out what each populated rack can hold. To compare the layouts fairly, keep the computing workload the same and include the power equipment serving it in both drawings.

[Recording script](../audio/module3/fresh/slide_11_what_changes_on_the_floor_plan.txt)

**Visual:** Moving shelves can free tray positions, but the neighboring power rack still occupies floor space.

### 3.12 · Where the conversion heat goes

A converter gives off heat where the conversion takes place. Move the shelves to a sidecar and some of that heat moves with them. The processors haven't moved, though. Their heat still has to leave the trays in the IT rack. The two sets of wavy lines belong in different places for a reason.

There's a real example behind this separation. Bosch and Rittal presented a sidecar that uses an Open Rack version-three frame for power equipment. The familiar frame is carrying shelves rather than compute trays. That's one physical implementation, not a requirement that every Mount Diablo design use that frame. To explore how that power rack works, try the Mount Diablo course on OCP Academy.

[Recording script](../audio/module3/fresh/slide_12_where_the_conversion_heat_goes.txt)

**Visual:** Conversion losses follow the converter. Processor heat stays with the IT tray. Bosch and Rittal illustrate one sidecar implementation.

### 3.13 · From cold plate to facility loop

Start at the cold plate. It is in thermal contact with the processor. Heat passes through the contact materials and the plate into coolant moving through its internal passages. Follow the warmer fluid away from the tray. A return manifold brings flow from multiple branches together on its way to the coolant distribution unit, or CDU.

At the heat exchanger, follow the heat rather than the fluid. Heat passes into a separate facility circuit. The equipment-side coolant can then circulate back through the supply manifold to the cold plates; it doesn't have to mix with facility water. That's why the drawing has two loops meeting at one box. Follow a parcel of coolant and it stays in its circuit. Follow the processor's heat and its journey continues on the other side.

[Recording script](../audio/module3/fresh/slide_13_from_cold_plate_to_facility_loop.txt)

**Visual:** The CDU’s heat exchanger transfers heat from the secondary loop to the primary loop without mixing the fluids. A chiller cools the facility water in this example.

### 3.14 · Flow matters as well as temperature

Two branches use the same coolant and pick up the same amount of heat each second. The branch on the left has a smaller flow. Each portion of fluid spends its share of the journey carrying more heat and returns with a larger temperature rise. More fluid passes through the branch on the right over the same interval, so a smaller rise can carry the same heat.

That's why a return temperature on its own isn't a measurement of chip power. You need the flow and the temperature change from supply to return, as well as the properties of the coolant. And branches on the same manifold need not receive identical flow: narrow passages and fittings resist flow and cause pressure drop. Count what actually moves through the branch you're interested in.

[Recording script](../audio/module3/fresh/slide_14_flow_matters_as_well_as_temperature.txt)

**Visual:** For the same coolant and heat load, a larger flow needs a smaller temperature rise.

### 3.15 · One tray, two heat paths

Imagine a tray producing a steady one thousand watts of heat. In this example the liquid loop picks up eight hundred watts through the cold plate. Follow the rest of the bar: two hundred watts leaves through air flowing over other components. The numbers are illustrative, not a specified target for a rack.

If you put a meter on the liquid path and use it to estimate all of the tray's heat, you'd miss one fifth of the total. Measure only the warmed exhaust air and you'd miss the larger part. The same distinction matters when looking at the hardware. Improving contact at the processor's cold plate helps its liquid path. It doesn't restore airflow to a heat sink behind a blocked vent. Even in one enclosure, different components can depend on different ways out.

[Recording script](../audio/module3/fresh/slide_15_one_tray_two_heat_paths.txt)

**Visual:** Illustrative 1,000 W tray: 800 W leaves in liquid and 200 W in air. The split is an example, not a target.

### 3.16 · One coupling serves one branch

A manifold and a coupling both carry coolant, but look at how many paths each one serves. The manifold is the common passage down the left. It distributes supply flow to several trays or collects returning flow from them. The small connector in each horizontal line joins just that branch across the rack-to-tray interface.

Now picture one tray moving into the frame. In a blind-mate design, the two connector halves come together with that motion, without someone reaching between their faces to join them. A pivoting blind-mate coupling is one published OCP design for this job. Its plug and socket can accommodate a limited mismatch as they approach. That adjustment belongs at one connection; the entire manifold doesn't have to shift each time a different tray arrives.

[Recording script](../audio/module3/fresh/slide_16_one_coupling_serves_one_branch.txt)

**Visual:** A manifold serves several branches. Each coupling joins a single branch across the removable interface.

### 3.17 · Offset, angle and mating travel

Hold one connector face still in your mind and move the other in three ways. First, slide it sideways without tipping it. The two centerlines stay parallel, but they're offset. Next, tip one face. Now the centerlines meet at an angle. Finally, line them up perfectly but leave some space between the faces. That's a shortfall in travel, not a sideways or angular error.

Watch the plug and socket bodies in the pivoting design. Their mounts let the bodies tilt as the two halves approach. That movement can help the mating faces accommodate a limited offset or angle. It doesn't supply missing forward travel. Even perfectly aligned faces have to come far enough together. On the plug side, the pivoting body and hose connection are distinct; the design doesn't rely on bending a hose to force the faces into line.

[Recording script](../audio/module3/fresh/slide_17_offset_angle_and_mating_travel.txt)

**Visual:** The plug and socket bodies can pivot at their mounts. They still need enough travel to engage.

### 3.18 · After the tray pulls away

The next mating starts with what the previous one leaves behind. Suppose the last tray approached a little to the left and the connector body tilted to meet it. If the body stayed in that position after separation, the next tray would inherit a starting angle chosen by a different piece of equipment.

In the published design, spring features help the unmated plug and socket bodies return toward center. Compare the tilted body on the left with the centered body on the right. The next tray approaches a more predictable starting region, while neighboring branches keep their own positions. Centering is one part of the design, not a guarantee for any arbitrary plug and socket. The specified mating partners, travel and permitted range of movement still matter.

[Recording script](../audio/module3/fresh/slide_18_after_the_tray_pulls_away.txt)

**Visual:** The unmated valve bodies return toward center. The published design has a limited mating range.

### 3.19 · Where conversion and heat capture happen

Put a finger on the converter in a rack drawing. That tells you where facility power changes form and where the converter's losses turn up as heat. Now put a finger on the processor. Its heat starts at the tray, even when a different rack supplied the electricity.

Between those two points you can name the equipment that carries power. Beyond the processor you can trace one or more cooling paths. That's a useful way to read a high-power system without assuming every power shelf sits inside the computing frame or every watt of heat leaves through the liquid loop.

[Recording script](../audio/module3/fresh/slide_19_takeaway.txt)

### 3.20 · Knowledge check: trace the paths

For the first question, count the capacity that remains under the shelf's stated redundancy condition. For the second, follow power and cooling across the two racks. Submit both answers to continue. The feedback explains the reasoning, and you can retry either question without needing a perfect score.

[Recording script](../audio/module3/fresh/slide_20_knowledge_check.txt)

**Question 1:** A dual-cord HPR V2 shelf has six installed 12 kW supplies. What sustained output does the specification state when one supply’s worth of capacity is reserved for redundancy?

- 60 kW **(correct)**
- 72 kW
- 48 kW

Five times 12 kW is 60 kW. The sixth supply provides one supply’s worth of margin.

**If incorrect:** Count the supplies needed after one becomes unavailable, then multiply by 12 kW.

- 72 kW: 72 kW counts all six nameplates. Redundant output must still be available with one supply unavailable.
- 48 kW: 48 kW counts only four supplies. Reserving one supply’s capacity leaves five, not four.

**Question 2:** A neighboring power rack supplies a compute tray. Its processor has a cold plate, while other devices have air-cooled heat sinks. Which paths still serve this tray? Select all that apply.

- DC power travels from the power rack toward the compute tray. **(correct)**
- Coolant leaving the processor’s cold plate carries heat toward the return manifold and CDU. **(correct)**
- Air passing over the other heat sinks carries heat away from those devices. **(correct)**
- The facility AC whip carries converted DC from the power rack to the tray.

The tray receives DC from its neighboring power rack and rejects heat by two paths: coolant from the cold plate and air from other heat sinks.

**If incorrect:** Locate the conversion step first: the AC whip is upstream of it. Then follow the processor’s heat and the other devices’ heat separately.


### 3.21 · Next: Open Rack in practice

You've followed electricity to a tray and heat away from it. In module four, we'll put names to the drawings: contributed frames from Meta and Google, a rack-scale design from AMD, and two manufacturers that use the available space in quite different ways.

[Recording script](../audio/module3/fresh/slide_21_next.txt)

## Module 4 · Open Rack in practice

16 slides · approximately 14 minutes including figure study and the knowledge check.

### 4.1 · Open Rack in practice

Welcome to module four. Meta and Google both contributed Open Rack version-three frame designs. Put their drawings side by side and the frames don't have the same outside width. That's our starting puzzle: how can two machines share an architecture and still look different?

We'll use real frames, switches and servers to separate the features designers share from the choices they make for a particular system. At the end, we'll take the rack out of the drawing and follow it through a building.

[Recording script](../audio/module4/fresh/slide_01_design_families.txt)

### 4.2 · Which drawing answers the question?

Imagine choosing one drawing to answer each of three questions. Where must the equipment meet its frame? Start with the interface specification. How do these graphics processors exchange data? Open the system connection diagram. Will the populated rack clear a corner on its way into the hall? Put its transported outline onto the room plan.

Now consider outside width. It might sound like an interface question, but for a particular frame the dimension you want is on its implementation drawing. Keeping those drawings distinct lets a server designer, a network designer and someone simply curious about the architecture all read the same rack without expecting one picture to tell the whole story.

[Recording script](../audio/module4/fresh/slide_02_which_drawing.txt)

### 4.3 · Two contributed frames, one equipment format

Start at the outside edges of the two front views. Meta's version-three frame has a nominal outside width of six hundred millimeters. Google's specification gives a base width of seven hundred six point two millimeters. The drawings use the same scale. The visual difference is real; it isn't a wider image of the same piece of hardware.

Now look inward at the supports. The relevant measurement for a piece of equipment begins at the surfaces that locate it, not at an arbitrary outer edge of steel. That's how two frame implementations can serve the same equipment format while using different amounts of floor space. Meta and Google each contributed a frame design. The common base specification describes shared interfaces; neither implementation drawing turns its own outside width into a universal Open Rack dimension.

[Recording script](../audio/module4/fresh/slide_03_two_contributed_frames_one_equipment_format.txt)

**Visual:** Meta specifies 600 mm nominal outside width; Google specifies a 706.2 mm base width.

### 4.4 · What happens across four rack positions?

Picture a row on a floor plan. The upper row in this example contains four six-hundred-millimeter frames. Its bases take up two thousand four hundred millimeters. Replace just the first base with Google's seven-hundred-six-point-two-millimeter base. The very next position starts a little farther along the floor.

Now make the same substitution four times. The lower row takes up two thousand eight hundred twenty-four point eight millimeters. The difference at the end is four hundred twenty-four point eight millimeters, before adding gaps or end clearances. That's more than forty centimeters from a difference that was barely over ten centimeters at one position. The equipment format hasn't changed. Measuring the row at the outside edges, instead of multiplying a tray width, is what makes the floor plan add up.

[Recording script](../audio/module4/fresh/slide_04_what_happens_across_four_rack_positions.txt)

**Visual:** Using the two frame widths from slide 3, four Google bases take up 424.8 mm more than four Meta bases, before gaps or end clearances.

### 4.5 · Will the rear door clear the cables?

Start with the left-hand side view. The switch body fits between the mounting plane and the rear door. Now add the power plug and the first bend in its cable. Those parts extend past the rear panel of the switch. Closing the door can take away exactly the space the cable needs to turn.

The useful depth therefore has two endpoints: the installed mounting position and the nearest obstruction in the fitted rack. Google's description distinguishes depth with and without a door. On the equipment side you need more than the published chassis depth: include the actual connector and room for the permitted bend. This is a different question from whether the switch can be bolted to the rails. A switch can pass the front mounting check and still leave its rear connections with nowhere to go.

[Recording script](../audio/module4/fresh/slide_05_will_the_rear_door_clear_the_cables.txt)

**Visual:** Use the configured enclosure, including cable exits and the fitted door, not just chassis depth.

### 4.6 · The ORW interface and the Meta/Rittal frame

Open Rack Wide gives equipment a wider format and defines interfaces that several designers can use. One of those interfaces specifies how the busbar assembly mounts to the frame. Now look at a particular implementation: the frame design contributed by Meta and Rittal.

The dimension line spans the outside of that frame. Its nominal width is twelve hundred millimeters. A tray designer is interested in a different width, measured inside at the equipment supports. And a room planner who wants service access beside the rack needs space beyond the outside edges. All three measurements can belong on drawings of the same installation. Keep the twelve-hundred-millimeter label attached to the thing it actually measures: the outside of the Meta and Rittal frame, not the tray and not every implementation of Open Rack Wide.

[Recording script](../audio/module4/fresh/slide_06_the_orw_interface_and_the_meta_rittal_frame.txt)

**Visual:** Nominal outside dimensions of the Meta/Rittal ORW frame. The width spans the outer uprights, not the tray opening; height is measured from the floor to the canopy.

### 4.7 · What AMD Helios adds to a frame

Take all the trays out of a frame drawing and you can still identify an opening and a set of mounting points. What you can no longer tell is which processors will cooperate or where their network links will go. AMD Helios addresses those questions at the scale of a whole computing system.

Helios is a rack-scale reference design based on Open Rack Wide. It brings compute, networking and cooling into one system design. A manufacturer can build on that design and make choices about its own implementation. Think of three different drawings: the Wide interface tells you where parts can meet, the contributed frame puts steel around those interfaces, and the system design gives the equipment jobs to do. Sharing the first drawing doesn't require every product to share the other two.

[Recording script](../audio/module4/fresh/slide_07_what_amd_helios_adds_to_a_frame.txt)

**Visual:** Helios is a rack-scale reference design. A tray that fits the opening still has a system job to do.

### 4.8 · Can a different tray do the same job?

Here are two switch trays with the same outer outline. Imagine replacing the left one with the right. The first check is mechanical: the enclosure is supported and seats where it should. Now follow one cable from the neighboring equipment. The port it needs is in a different position on the proposed tray. Can that cable reach the new port along a usable route?

Even two plugs that mate don't establish that the endpoints can communicate as the system expects. That question belongs to the system connection diagram and the equipment specification. A tray can fit the opening perfectly and still be the wrong switch for that connection.

[Recording script](../audio/module4/fresh/slide_08_can_a_different_tray_do_the_same_job.txt)

**Visual:** Matching the physical opening does not establish port location, cable reach or communication between endpoints.

### 4.9 · HPE builds AMD Helios on Open Rack Wide

Start at the frame of HPE’s version of AMD Helios. Its double-wide opening comes from Open Rack Wide. What does that width buy you? A single Helios compute tray carries four graphics processors along with the cold plates that draw heat away from them.

Pull that tray forward and you can see the distinction. The frame provides the supports. AMD’s reference design specifies what rides on them. HPE makes a further choice: Juniper switches connect the accelerators over a scale-up network. Another Helios builder can choose different switches while keeping the same mechanical format.

[Recording script](../audio/module4/fresh/slide_09_hpe_helios_connect_72_gpus.txt)

**Visual:** One wide compute tray holds four GPUs in AMD’s Helios design. HPE implements that design in an ORW rack; its choice of switching is separate from the mechanical format.

### 4.10 · Supermicro: four nodes in less height

Supermicro offers two chassis for four liquid-cooled Arm server nodes. Start with the twenty-one-inch chassis. It occupies two OpenU of rack height. The two drawings share a baseline so you can compare their widths and heights at the same scale.

Now look at the forty-two-inch chassis. The same four nodes occupy one OpenU of height. Count the processors as well: two in each node, eight in either chassis. The wider chassis saves one OpenU of vertical space while holding the same number of nodes and processors.

[Recording script](../audio/module4/fresh/slide_10_supermicro_four_nodes_in_less_height.txt)

**Visual:** Four dual-processor nodes occupy 2 OU in the 21-inch chassis or 1 OU in the 42-inch chassis.

### 4.11 · A doorway and a turn are different tests

Imagine walking beside a rack as it comes off the receiving area and approaches an open doorway. On a straight path, the left and right edges can pass the jambs with daylight to spare. Now move just beyond the doorway and begin a turn. A leading corner swings sideways into a part of the corridor that the rack never occupied on the straight approach.

The overhead view lets you follow that corner, not just check the final position. Start with the outline of what actually travels. A projecting handle, shipping protection or handling equipment can be part of the moving assembly even though none appears on a bare-frame dimension drawing. The door measurement may have been exactly right. It was the measurement for straight passage, not for the entire turn.

[Recording script](../audio/module4/fresh/slide_11_a_doorway_and_a_turn_are_different_tests.txt)

**Visual:** Trace the transported outline, including any handling equipment that moves with the rack.

### 4.12 · Watch the opposite corners at 45 degrees

Try a small geometry experiment with a paper rectangle. Give it a width of six tenths of a meter and a length of one point two meters. Held straight, it spans six tenths of a meter from left to right. Turn it forty-five degrees and look for the farthest point on each side. Those points are now opposite corners.

Both dimensions contribute to the new span. At this angle, the short side contributes about forty-two centimeters across the page and the long side about eighty-five. Together that's about one point two seven meters. This number describes the rectangle's width in one direction at one instant. It isn't a minimum corridor width: the center moves during a real turn, and part of the rack may already be in the intersecting corridor. That's why the path matters as well as the angle.

[Recording script](../audio/module4/fresh/slide_12_watch_the_opposite_corners_at_45_degrees.txt)

**Visual:** A 0.6 m by 1.2 m example spans about 1.27 m at 45°. That is a projected width, not a corridor requirement.

### 4.13 · Trace the route from receiving to the hall

Mark the inside corner and the two sides of the doorway. Move a scaled rack outline along one possible approach. First check the leading corner as it starts to turn. Then check the trailing corner while the front half moves into the next corridor. A clash can occur halfway through even when the start and finish positions both look clear.

This sketch is a way to find questions for the actual route, not a handling procedure or a clearance certification. The Academy course Open Data Center for AI: Applying the Specification looks at the building side of this same journey, from receiving equipment to providing a usable path into the data hall. If the turn caught your interest, that course is a good place to follow the rack beyond the edge of this drawing.

[Recording script](../audio/module4/fresh/slide_13_trace_the_route_from_receiving_to_the_hall.txt)

**Visual:** Check intermediate positions as well as start and finish. The Open Data Center for AI course follows the building side of this journey.

### 4.14 · Which drawing would you open next?

Imagine somebody asks for “the Open Rack drawing.” Before you send one, ask what they want to find. A shared mounting feature belongs in the base specification. The width of four particular frames comes from the dimensions of those frame implementations. For a network link, open the system diagram and name the two endpoints. For a turn, put the transported outline on the room plan.

Choosing the drawing is already part of the answer. It tells you whether you're looking at an agreement between designers, a choice one manufacturer made, or a constraint imposed by the building around the rack.

[Recording script](../audio/module4/fresh/slide_14_which_drawing_would_you_open_next.txt)

### 4.15 · Read the design, then trace the turn

The first question asks you to distinguish a feature of one computing system from a shared rack interface. The second asks you to reason about a moving rack at a corner. Submit each answer to continue. The feedback explains the distinction, and you can retry either one.

[Recording script](../audio/module4/fresh/slide_15_knowledge_check.txt)

**Question 1:** Which Helios detail is a system design choice?

- The frame’s busbar mounting interface.
- Four graphics processors on a compute tray. **(correct)**
- The frame’s attachment points for equipment supports.

Yes. AMD specifies four GPUs on a Helios compute tray. Open Rack Wide defines how equipment fits, not how many processors it contains.

**If incorrect:** Separate what mounts to the frame from what the designer puts inside the tray.

- The frame’s busbar mounting interface.: The ORW base defines that mounting interface. Think about what AMD puts on a tray.
- The frame’s attachment points for equipment supports.: Those attachment points belong to the rack interface. The tray’s contents are a system design choice.

**Question 2:** A loaded rack fits through a doorway straight on, but its leading corner strikes a wall as it turns. Which changes could alter clearance at that turn? Select all that apply.

- Provide more free floor space on the outside of the turn. **(correct)**
- Increase network bandwidth inside the rack without changing its exterior.
- Use a handling configuration with a different overall length, including equipment traveling with the rack. **(correct)**
- Make the final destination aisle wider while leaving the corner and its approach unchanged.

Right. The space available at the corner and the moving object’s complete outline both affect clearance. Check the resulting path; a change alone does not guarantee a fit.

**If incorrect:** Trace the outside corner of the complete moving assembly. Both its length and the clear space at the turn matter; internal bandwidth and space only at the destination do not.


### 4.16 · Keep exploring Open Rack

Thank you for exploring Open Rack. The next time you see a populated rack, pick one detail you recognize: a tray support, a power contact, a coolant coupling or a switch tray. Follow it to the part it meets. Then ask which details the designers needed to agree on and which they were free to choose.

That's a useful way into the Rack and Power project's contributions and Summit recordings linked here. You can start with one familiar interface and discover just how many different systems it helps make possible.

[Recording script](../audio/module4/fresh/slide_16_course_complete.txt)

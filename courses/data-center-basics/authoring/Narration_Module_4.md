# Module 4: Management and Trends — approved narration

## Slide 1: Management and Trends

Module four: Management and Trends. Physical infrastructure delivers value through the services people operate. You'll connect ownership and responsibility to resource efficiency, then examine how changing workloads influence facility choices and the need for shared approaches.

## Slide 2: Connect Ownership, Metrics and Technology Choices

By the end of this module, you'll be able to distinguish facility and service responsibilities, explain how virtual workloads depend on physical resources, and interpret basic efficiency metrics without treating one number as the whole goal.

You'll apply that reasoning to a deployment scenario and consider current trends in power, cooling and distributed computing. Those questions lead naturally into the Intro to OCP learning path.

## Slide 3: The Changing Data Center Landscape

Imported recording: uses its own audio; no separate slide narration.

## Slide 4: Who Owns and Manages What?

Imported recording: uses its own audio; no separate slide narration.

## Slide 5: Responsibility Follows the Service Contract

A facility operator, equipment owner and service operator can be different organizations. In colocation, the provider commonly supplies contracted space, power and supporting infrastructure while the customer operates its equipment. A cloud service can shift more of the stack to the provider.

The exact responsibilities depend on the contract and service model. Customers still need to understand their obligations for areas such as identities, data and configuration. An ownership label alone isn't a complete responsibility map.

## Slide 6: Physical Versus Virtual Infrastructure

Imported recording: uses its own audio; no separate slide narration.

## Slide 7: Virtual Services Still Consume Physical Resources

Virtualization lets software present and manage logical computing environments on physical resources. In a virtual-machine example, a hypervisor manages the guest systems and their access to the host hardware.

Containers provide another arrangement: they share the kernel of their host operating environment. The animation traces a virtual machine’s physical dependency. More activity in an application can create more demand on processors, memory, storage and networks, with consequences for electricity and heat. Abstraction makes resources easier to use and manage; it doesn't remove their physical limits.

## Slide 8: Monitor Before You Optimize

Data center infrastructure management, or D C I M, brings information about physical assets, power, cooling and capacity into operational decisions. Telemetry and trends can reveal patterns that a single reading misses.

Useful monitoring needs a clear question and reliable context. An alarm doesn't by itself establish a root cause or authorize a change. Connect the measurement to the affected service, operating limits and responsible team, then verify the result of any improvement.

## Slide 9: PUE Measures Facility Overhead

Power Usage Effectiveness, or P U E, compares total facility energy with the energy used by IT equipment over the same period and boundary. If a facility uses twelve hundred units while its IT equipment uses one thousand, the ratio is one point two.

The ratio describes overhead. It doesn't tell you how much useful computing was delivered or capture every environmental effect. Compare like boundaries and operating conditions, and consider total energy as well as the ratio.

## Slide 10: Water and Carbon Need Explicit Boundaries

Water Usage Effectiveness, or W U E, relates water use to IT energy. A site-based value counts water used at the facility. A source-inclusive approach can also account for water associated with producing its energy. Those boundaries must not be mixed silently.

Carbon Usage Effectiveness, or C U E, relates the defined energy-related emissions to IT energy. State the emissions scope, period and units. Neither a low water ratio nor a renewable-energy claim establishes the whole environmental outcome.

## Slide 11: Remove Waste Without Misreading the Ratio

# Approved Astra content update · Leo / Eleven v4
Consider a controlled consolidation that preserves the same useful work and service requirements. During one comparable period, the starting system uses one thousand units of IT energy and two hundred units of facility overhead. Total energy is twelve hundred units, and power usage effectiveness is one point two zero. After consolidation, IT energy falls to eight hundred units, while overhead remains two hundred. Total energy is now one thousand units, but PUE rises to one point two five. The denominator fell while overhead stayed fixed. The higher ratio does not erase the energy saving. Evaluate useful work, service requirements and total energy alongside the ratio.

## Slide 12: Improve Cooling and Power Together

Several practical actions can improve resource use. Airflow separation and suitable economizer operation can reduce unnecessary cooling effort. Efficient power conversion and appropriately operated backup systems can reduce electrical losses.

Workload consolidation and real-time monitoring address another part of the system. Each action needs context: climate, operating load, resilience requirements and equipment capabilities can change the result. Verify both the service outcome and resource consumption rather than assuming every improvement must lower every metric.

## Slide 13: Heat Reuse Needs a Useful Heat Customer

Heat that would otherwise be rejected can sometimes serve a nearby building, district heating system or another process. A viable arrangement needs a suitable temperature, transport path and customer whose demand matches the available heat.

Recovering useful heat can improve wider-system outcomes, but it doesn't automatically reduce the data center's electricity use or P U E. Pumps, heat pumps and other supporting equipment may add energy requirements. Evaluate the complete heat-reuse system and its local context.

## Slide 14: Clean Energy Claims Need More Than a Contract Label

Renewable energy certificates represent energy attributes that can be transferred separately from electricity. A power purchase agreement, or P P A, is a contract to buy power under agreed terms; the treatment of its energy attributes matters too.

An annual purchase or certificate balance doesn't by itself demonstrate that the facility used matching clean generation at every hour and location. Check the accounting boundary, attribute ownership and timing behind a claim. Procurement and physical supply are related questions that need clear evidence.

## Slide 15: Demand Growth Raises Local Infrastructure Questions

The International Energy Agency's April twenty twenty-six update puts global data-center electricity use around four hundred eighty-five terawatt hours in twenty twenty-five. Its projection reaches roughly nine hundred fifty terawatt hours in twenty thirty.

These are an estimate and a projection of energy use, not a promise of completed facilities or a measure of installed power capacity. For a particular site, power availability, grid connections and supporting infrastructure can determine when and how new capacity can operate.

## Slide 16: Plan for Mixed Workloads and Cooling

# Approved Astra content update · Leo / Eleven v4
Different workloads call for different deployment choices. Centralized facilities support large coordinated deployments. Regional and edge placements can serve activities closer to where data is produced or a response is needed. OCP's AI Computing Continuum connects these choices across enterprise, telecommunications and industrial settings. Evaluate response needs, connectivity, data constraints and the site's available resources. Air and liquid cooling must fit the actual equipment and heat path. Modular approaches can help a deployment plan, but still depend on local power, cooling and operating constraints.

## Slide 17: Co-Design from Chip to Grid

An accelerator choice can change board design, rack power, heat removal, facility distribution and the relationship with the electricity grid. Those dependencies explain why current open-infrastructure work reaches beyond individual servers.

Community efforts on power interfaces, cooling and telemetry illustrate the need to coordinate requirements across the system. Eight hundred volts direct current and very high-density racks are specific developing architectures, not descriptions of every installed facility. The transferable skill is to trace the dependencies before choosing a solution.

## Slide 18: Emerging Technologies Need a Readiness Test

Quantum, photonic and other emerging technologies may create new capabilities and infrastructure needs. An interesting demonstration doesn't establish a general deployment timetable or prove that conventional facilities will disappear.

Ask what problem the technology solves, what has been demonstrated, which supporting systems it requires and how it can be maintained. Separate a published design, a pilot and a repeatable operating service. That habit helps you explore innovation without presenting speculation as a guaranteed roadmap.

## Slide 19: Choose an Improvement That Fits the Site

# Approved Astra content update · Leo / Eleven v4
Suppose equipment inlet temperature rises after new hardware is added. Identify the affected assets and confirm the reading before treating it as a room-wide condition. The responsible teams review airflow, cooling capacity, equipment limits and any service impact. Agree who owns the equipment and the facility response. Follow the site's authorized change or recovery procedure. Then verify both inlet conditions and the service result. This simple sequence connects monitoring, responsibility and physical capacity. A promising improvement still needs a measured outcome.

## Slide 20: Keep the Goal Larger Than One Metric

Responsibility follows the actual service arrangement. Virtual services still depend on physical capacity. Resource metrics are useful only when their boundaries and limits are understood.

Look for useful work and reliable service alongside energy, water and emissions outcomes. Evaluate new technology against a defined problem and evidence of readiness. These habits connect the digital world, facility and rack into one operating system, and prepare you to explore how a community develops common approaches to its challenges.

## Slide 21: Check Efficiency and Operational Concepts

These questions connect operational choices to their purpose. Consider what makes rejected heat useful, what an energy-management team means by a zombie server, and why different workloads can need different cooling paths.

Submit each question once to continue. Correct answers aren't required. Use the explanation for your selected choice to check the underlying concept, then retry if useful.

## Slide 22: Match Planning Choices to Their Purpose

# Approved Astra content update · Leo / Eleven v4
Use this final matching exercise to connect five planning considerations with their purpose. Think across the course: where work belongs, how facilities are deployed, when heat can be useful, what energy contracts establish and what storage must provide. These are practical planning principles, rather than forecasts for every data center. Match all five and read the explanation for each pair.

## Slide 23: Continue with Intro to OCP

# Approved Astra content update · Leo / Eleven v4
Your main next step is the Intro to OCP course series. It connects the physical foundations learned here to the community's origins, ecosystem and governance, open rack and cooling technologies, and the adoption journey. You now have the vocabulary to ask how shared interfaces support a real deployment. If workload placement especially interests you, the AI Computing Continuum course is an optional technical continuation. It explores AI infrastructure beyond hyperscale facilities in greater depth. Choose the path that supports the questions you need to answer.

## Slide 24: Apply the System View

Thank you for completing Management and Trends and for working through Data Centers: From Digital Services to Physical Infrastructure. You've connected services to facilities, equipment and the decisions that support them.

Use that system view to ask clearer questions about capacity, responsibility and resource use. Continue with Intro to OCP when you're ready to explore shared designs and community participation. Thank you, and put these connections to work in your next infrastructure conversation.

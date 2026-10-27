# Module 1: The Digital World — approved narration

## Slide 1: The Digital World

Module one: The Digital World. Every digital service depends on physical infrastructure. You'll follow that connection from a familiar application to the facility, equipment, electricity and networks behind it. You'll also distinguish facility types, resilience capabilities and cloud services, so the terms describe something concrete.

## Slide 2: Follow the Service, Facility, Rack and Operations

This course follows four connected questions. What does a data center do? What keeps its equipment running? How does that equipment fit into a rack? And how do people operate and improve the whole system?

You'll work through those questions in four modules. Short narrated explanations connect the concepts, while the videos provide longer examples. Knowledge checks give you feedback and a chance to retry. Together, the modules prepare you to explore how the Open Compute Project develops shared approaches to infrastructure.

## Slide 3: A First Look at Physical Infrastructure

Imported recording: uses its own audio; no separate slide narration.

## Slide 4: One Request Depends on Many Systems

Think about opening a shared document. Your device sends a request through networks to the systems providing that service. Computing equipment handles the request, storage holds the information, and a response travels back.

The animation follows that sequence. The physical systems underneath stay necessary throughout: electricity powers the equipment, and cooling removes the heat it produces. A simple action on your device can depend on many connected systems, even though the service hides most of that complexity.

## Slide 5: What Is a Data Center?

Imported recording: uses its own audio; no separate slide narration.

## Slide 6: Capacity Is More Than Floor Space

# pronunciation: kW -> kilowatts; MW -> megawatts; kWh -> kilowatt hours
A data center needs several kinds of capacity. Servers process information, storage retains it, and networks move it. The facility must supply enough electrical power and remove the resulting heat. Available floor space alone doesn't tell you what equipment a site can support.

Keep power and energy separate. Kilowatts and megawatts describe the rate of electrical use or available capacity. Kilowatt hours measure energy used over time. A constant load of one kilowatt running for one hour uses one kilowatt hour. We'll use that distinction again when discussing efficiency.

## Slide 7: Tiers Describe Infrastructure Capabilities

# pronunciation: Tier I -> tier one; Tier II -> tier two; Tier III -> tier three; Tier IV -> tier four
Uptime Institute's four Tiers describe site infrastructure capabilities. Tier one provides basic capacity. Tier two adds redundant capacity components. Tier three adds concurrent maintainability: planned work can remove a component or distribution path without interrupting operations. Tier four adds fault tolerance for an individual equipment failure or distribution interruption.

These categories don't promise a particular annual uptime percentage. They also don't replace resilient applications, network design or disciplined operations. Use the Tier description to ask what maintenance and failure the infrastructure can accommodate, then consider the service's wider requirements.

## Slide 8: Enterprise, Colocation, Hyperscale and Edge

Enterprise, colocation, hyperscale and edge describe different aspects of a data center. An enterprise facility supports an organization's needs. Colocation provides space and supporting infrastructure for customers' equipment. Hyperscale describes an approach built to operate and expand at very large scale. Edge places computing closer to the users, devices or activity it serves.

The labels can overlap. An organization might place an edge deployment in a colocation facility. Ask which characteristic a label describes: the operating arrangement, the scale, or the relationship to the workload.

## Slide 9: AI Factories Align the Whole System

# Approved Astra content update · Leo / Eleven v4
Training adjusts an artificial intelligence model using data. Inference uses a trained model to produce an output, such as identifying a defect in an image. These activities can place different demands on the infrastructure. An AI factory organizes computing and data movement around developing and running AI at scale. Accelerators work with memory, storage, networks and software. Electrical power and heat removal support the complete system. Useful output depends on those parts working together. AI factory describes a purpose and design approach. It can overlap enterprise, colocation or hyperscale arrangements. It does not prescribe one rack density, one cooling technology or one ownership model. Ask what the workload needs before choosing the infrastructure.

## Slide 10: Place AI Where the Service Can Work

# Approved Astra content update · Leo / Eleven v4
Consider an industrial inspection service. A camera sends an image to a trained model at the local site. The response must arrive before the item passes the inspection point. A remote connection cannot be assumed to meet that deadline. Now the wide-area connection becomes unavailable. Local inference can continue if its model, data, power and computing resources remain available. Separate, nonurgent analysis can wait. When connectivity returns, that work can use regional capacity if data rules and available resources permit. This is a placement decision, not an instant move of a running task. Edge describes proximity to the activity being served. OCP's AI Computing Continuum project develops open, modular infrastructure approaches for regional, enterprise, telecommunications and industrial environments beyond hyperscale facilities. Its dedicated Academy course explores the architecture. Choose placement through response needs, connectivity, data constraints and site capacity.

## Slide 11: Match the Facility to Its Role

Match each facility type to the characteristic emphasized in its definition. Treat these as useful associations, rather than categories that can never overlap. Submit a complete set of matches to continue. Correct answers aren't required, and you can use the explanations to review the relationships and try again.

## Slide 12: Location Balances Access, Energy and Risk

Location balances several needs. Being closer to users can reduce network delay, or latency. Strong connectivity gives services access to users and other facilities. Power availability, cooling conditions, water requirements and local hazards affect what a site can support.

Organizations also consider costs and requirements for where information is stored or processed. A city name alone doesn't establish compliance or resilience. The useful question is whether a location fits the workload and its constraints. The lowest-cost site can be a poor choice if it cannot meet those needs.

## Slide 13: Regional Hubs Serve Different Needs

The regional examples illustrate the same location questions in different settings. Ashburn connects services to a major North American network market. São Paulo serves a large South American market, while Frankfurt connects European users and networks.

Johannesburg, Singapore and Sydney illustrate regional connectivity in southern Africa, Southeast Asia and Australia. Their usefulness depends on the customers, networks and facility options a particular deployment needs. These are examples of regional roles, rather than a ranking of cities or a guarantee that any site in one city will meet a project's requirements.

## Slide 14: Remote Sites Have a Different Tradeoff

# pronunciation: McMurdo -> Mack Murdo
Remote research creates a different location problem. At a station such as Mack Murdo in Antarctica, instruments and researchers need local computing and data handling far from the usual network hubs.

Processing some information locally can reduce dependence on a distant connection. Information may still need to be stored, transferred or backed up elsewhere. The lesson is to place the needed capability where the activity occurs, while planning for limited connectivity, maintenance access and logistics. A remote installation doesn't need to resemble a large commercial campus to perform an important role.

## Slide 15: Fiber Connects Facilities and Users

Data centers connect through physical networks. Terrestrial fiber links buildings and regions; submarine fiber links land networks across oceans. Local access networks complete the connection to businesses, devices and users.

Satellite systems can provide connectivity or an alternate path where geography and infrastructure make other options difficult. Their performance depends on the system and location, so avoid assuming one fixed delay or bandwidth for every satellite connection. The map illustrates how many networks depend on shared physical routes. It isn't a current inventory of every cable or connection.

## Slide 16: Redundancy Must Survive the Same Failure

Two connections can still share one point of failure. Imagine separate network services that pass through the same trench. A single excavation could damage both. Extra equipment is useful only when it addresses the failure you're trying to withstand.

Resilience combines appropriate separation with ways to continue or recover service. That may include alternate routes, replicated systems and tested recovery procedures. Backups support recovery, but they don't automatically provide uninterrupted service. Ask what event could affect the paths or systems together, and what the service would do next.

## Slide 17: Cloud Is a Service Model Built on Facilities

Cloud computing is a way to provide resources as an on-demand service. Users can obtain shared computing capabilities that can be provisioned and released with little manual intervention. The service still relies on physical equipment and facilities.

A cloud can be private to one organization, public, or connected with other cloud environments. It doesn't have to span many data centers, and a private cloud doesn't have to be reached through the public internet. When comparing options, separate the service model from the facility and check which availability features the particular service provides.

## Slide 18: What Connects the Digital World

# Approved Astra content update · Leo / Eleven v4
Digital services depend on connected physical systems. Facility labels describe different dimensions, including ownership, scale and proximity. An AI factory adds a workload and design lens. Training and inference have requirements that must be matched to the whole system. Placement across the computing continuum depends on response needs, connectivity, data and site capacity. Resilience depends on how systems behave during maintenance, failure and recovery. Cloud services still depend on real facilities. Keep these relationships in mind as we follow power and heat through the next module.

## Slide 19: Apply the Digital World Model

Use these three questions to connect the terms to their purpose. Consider what a data center physically does, what makes cloud a service model, and why computing might be placed near its users.

Submit an answer to each question before continuing. You don't need every answer correct to advance. Read the explanation for your selected choice, and retry if you want to check your reasoning again.

## Slide 20: up_next

Thank you for completing The Digital World. You can now connect digital services to their physical foundations and distinguish facility characteristics from cloud services.

Module two examines how power delivery, cooling and physical layout support the equipment. You'll follow those systems together, because a working service depends on the whole chain.

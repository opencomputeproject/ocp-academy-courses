# Module 1: The Digital World — scripts and teaching text

Status: draft for Module 1 script approval. The outline is approved; the total course target has been tightened to approximately 90 minutes.

Edit the paired files under `audio/module1/` to change spoken wording, or describe the changes in chat. This review document is generated from those scripts and `course.json`; it is not a second authoring source.

Voice: ElevenLabs Leo v2; stable Multilingual v2 model; maintained speed 1.18. No synthesis has been performed. Pronunciation comments are excluded from spoken audio.

All original videos retain their original audio. New introductions play before learner-initiated video playback, without competing audio.

## Timing plan

The eighteen new scripts contain approximately 1,303 spoken words. At an illustrative 150–165 words per minute this is about 7.9–8.7 minutes of new narration, plus 6:02 of original video. Reading, reflection and the four original questions bring the module target to about 19 minutes. Actual generated audio determines the final playback time; narration speed remains 1.18.

The learner-time plan for the complete four-module course is 19 + 24 + 16 + 31 = approximately 90 minutes. Optional reference reading is outside that estimate.

## Scripts

### 01 — The Digital World

Script: `audio/module1/slide_01_the_digital_world.txt` · approximately 45 words

From a familiar service to its physical foundations.

**Narration**

Module one: The Digital World. Every digital service depends on physical infrastructure. You'll follow that connection from a familiar application to the facility, equipment, electricity and networks behind it. You'll also distinguish facility types, resilience capabilities and cloud services, so the terms describe something concrete.

### 02 — Follow the Service, Facility, Rack and Operations

Script: `audio/module1/slide_02_course_overview.txt` · approximately 82 words

Four connected questions about the systems behind digital services.

1. The Digital World
2. Data Center Physical Infrastructure
3. Inside the Rack
4. Management and Trends

**Narration**

This course follows four connected questions. What does a data center do? What keeps its equipment running? How does that equipment fit into a rack? And how do people operate and improve the whole system?

You'll work through those questions in four modules. Short narrated explanations connect the concepts, while the videos provide longer examples. Knowledge checks give you feedback and a chance to retry. Together, the modules prepare you to explore how the Open Compute Project develops shared approaches to infrastructure.

### 03 — Welcome to Data Center 101

Script: `audio/module1/slide_03_course_introduction_video.txt` · approximately 20 words

Section label: Introduction

Media: `resources/videos/module1/1-1-welcome-course-overview-1080p.mp4`

Caption: A short introduction to the course and the physical systems behind digital services.

**Narration**

Watch the course introduction for the wider context. Start the video when you're ready, then continue to the service journey.

### 04 — One Request Depends on Many Systems

Script: `audio/module1/slide_04_service_journey.txt` · approximately 77 words

Section label: Service Dependencies

Media: `figures/module1/service-journey.mp4`

Caption: A simple service action depends on connected physical systems.

**Narration**

Think about opening a shared document. Your device sends a request through networks to the systems providing that service. Computing equipment handles the request, storage holds the information, and a response travels back.

The animation follows that sequence. The physical systems underneath stay necessary throughout: electricity powers the equipment, and cooling removes the heat it produces. A simple action on your device can depend on many connected systems, even though the service hides most of that complexity.

### 05 — What Is a Data Center?

Script: `audio/module1/slide_05_what_is_a_data_center_video.txt` · approximately 24 words

Section label: Facility Purpose

Media: `resources/videos/module1/1-2-what-is-a-data-center-1080p.mp4`

Caption: Computing equipment depends on the facility and systems that support it.

**Narration**

Watch how a data center brings computing equipment and its supporting systems together. Listen for what the facility enables and what keeps it operating.

### 06 — Capacity Is More Than Floor Space

Script: `audio/module1/slide_06_capacity_and_units.txt` · approximately 89 words

Section label: Physical Capacity

- **IT capacity** Compute, storage and network capability.
- **Facility capacity** Power delivery, heat removal and physical space.
- **Power** kW and MW describe a rate or available electrical capacity.
- **Energy** kWh measures electrical use over time.

Media: `figures/module1/capacity-and-units.svg`

Caption: Physical capacity and energy use answer different planning questions.

Reference pill: [Power and energy units](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php)

**Narration**

A data center needs several kinds of capacity. Servers process information, storage retains it, and networks move it. The facility must supply enough electrical power and remove the resulting heat. Available floor space alone doesn't tell you what equipment a site can support.

Keep power and energy separate. Kilowatts and megawatts describe the rate of electrical use or available capacity. Kilowatt hours measure energy used over time. A constant load of one kilowatt running for one hour uses one kilowatt hour. We'll use that distinction again when discussing efficiency.

### 07 — Tiers Describe Infrastructure Capabilities

Script: `audio/module1/slide_07_tier_capabilities.txt` · approximately 89 words

Section label: Infrastructure Resilience

A capability classification does not guarantee an annual uptime percentage.

Tier | Distinguishing capability
--- | ---
I — Basic capacity | Capacity to support the critical environment.
II — Redundant capacity | Additional capacity components; distribution remains a limitation.
III — Concurrently maintainable | Planned component or distribution-path maintenance without interrupting operations.
IV — Fault tolerant | An individual equipment failure or distribution interruption does not interrupt operations.

Reference pill: [Uptime Tier capabilities](https://uptimeinstitute.com/tiers)

Editorial correction: Replace embedded uptime percentages and annual downtime predictions with current capability definitions.

**Narration**

Uptime Institute's four Tiers describe site infrastructure capabilities. Tier one provides basic capacity. Tier two adds redundant capacity components. Tier three adds concurrent maintainability: planned work can remove a component or distribution path without interrupting operations. Tier four adds fault tolerance for an individual equipment failure or distribution interruption.

These categories don't promise a particular annual uptime percentage. They also don't replace resilient applications, network design or disciplined operations. Use the Tier description to ask what maintenance and failure the infrastructure can accommodate, then consider the service's wider requirements.

### 08 — Enterprise, Colocation, Hyperscale and Edge

Script: `audio/module1/slide_08_facility_types.txt` · approximately 85 words

Section label: Facility Characteristics

The labels describe different dimensions and can overlap.

- **Enterprise:** A facility serving an organization's own computing needs.
- **Colocation:** Space, power and supporting infrastructure for customers' equipment.
- **Hyperscale:** Infrastructure designed for very large, repeatable operations and growth.
- **Edge:** Computing placed close to the users, devices or activity it serves.

**Narration**

Enterprise, colocation, hyperscale and edge describe different aspects of a data center. An enterprise facility supports an organization's needs. Colocation provides space and supporting infrastructure for customers' equipment. Hyperscale describes an approach built to operate and expand at very large scale. Edge places computing closer to the users, devices or activity it serves.

The labels can overlap. An organization might place an edge deployment in a colocation facility. Ask which characteristic a label describes: the operating arrangement, the scale, or the relationship to the workload.

### 09 — Match the Facility to Its Role

Script: `audio/module1/slide_09_facility_matching.txt` · approximately 48 words

Match all four definitions, then submit. An attempt is required; correctness is not.

**M1-KC1 — Match each data center type to the characteristic emphasized in its definition.**

- Edge Data Centers → Located near end-users to reduce latency
  Explanation: Edge emphasizes proximity to a workload or its users. It can be deployed within several ownership or operating models.
- Hyperscale Data Center → Support global-scale cloud infrastructure
  Explanation: Hyperscale emphasizes scale and repeatable operations. Large cloud infrastructure is the example tested here.
- Enterprise Data Center → Built and used by a single organization
  Explanation: Enterprise emphasizes serving an organization's own needs; it does not specify one fixed facility size.
- Colocation Data Center → Shared facility where tenants bring their own equipment
  Explanation: Colocation separates the facility service from the customer's equipment. The provider supplies contracted space and supporting infrastructure.

Correct feedback: Each association identifies the characteristic emphasized by that label. The labels can overlap in real deployments.

Fallback feedback: Compare the definition with the label's purpose: edge is proximity, hyperscale is scale, enterprise is organizational use, and colocation is a facility service.

**Narration**

Match each facility type to the characteristic emphasized in its definition. Treat these as useful associations, rather than categories that can never overlap. Submit a complete set of matches to continue. Correct answers aren't required, and you can use the explanations to review the relationships and try again.

### 10 — Location Balances Access, Energy and Risk

Script: `audio/module1/slide_10_location_tradeoffs.txt` · approximately 88 words

Section label: Site Selection

Media: `figures/module1/location-tradeoffs.svg`

Caption: Choose a location by the workload's requirements and the site's constraints.

**Narration**

Location balances several needs. Being closer to users can reduce network delay, or latency. Strong connectivity gives services access to users and other facilities. Power availability, cooling conditions, water requirements and local hazards affect what a site can support.

Organizations also consider costs and requirements for where information is stored or processed. A city name alone doesn't establish compliance or resilience. The useful question is whether a location fits the workload and its constraints. The lowest-cost site can be a poor choice if it cannot meet those needs.

### 11 — Regional Hubs Serve Different Needs

Script: `audio/module1/slide_11_regional_examples.txt` · approximately 90 words

Section label: Regional Examples

Illustrative roles, not a city ranking or a site guarantee.

- **Ashburn:** North American network connectivity.
- **São Paulo:** Access to a large South American market.
- **Frankfurt:** European users and interconnected networks.
- **Johannesburg:** A regional example in southern Africa.
- **Singapore:** A regional example in Southeast Asia.
- **Sydney:** A regional example in Australia.

**Narration**

The regional examples illustrate the same location questions in different settings. Ashburn connects services to a major North American network market. São Paulo serves a large South American market, while Frankfurt connects European users and networks.

Johannesburg, Singapore and Sydney illustrate regional connectivity in southern Africa, Southeast Asia and Australia. Their usefulness depends on the customers, networks and facility options a particular deployment needs. These are examples of regional roles, rather than a ranking of cities or a guarantee that any site in one city will meet a project's requirements.

### 12 — Remote Sites Have a Different Tradeoff

Script: `audio/module1/slide_12_remote_research.txt` · approximately 91 words

Section label: Remote Computing

Media: `figures/module1/remote-research.svg`

Caption: Local capability supports the research activity while remote links and logistics impose constraints.

Reference pill: [McMurdo research computing example](https://www.unavco.org/polar-services/forward-fielded-instruments/mcmurdo-station/)

**Narration**

Remote research creates a different location problem. At a station such as Mack Murdo in Antarctica, instruments and researchers need local computing and data handling far from the usual network hubs.

Processing some information locally can reduce dependence on a distant connection. Information may still need to be stored, transferred or backed up elsewhere. The lesson is to place the needed capability where the activity occurs, while planning for limited connectivity, maintenance access and logistics. A remote installation doesn't need to resemble a large commercial campus to perform an important role.

### 13 — Fiber Connects Facilities and Users

Script: `audio/module1/slide_13_network_connections.txt` · approximately 88 words

Section label: Physical Connectivity

Media: `resources/images/module1/world-cable-map.jpg`

Caption: Illustrative source map; not a current cable inventory. Embedded map and cable-data credits are retained.

Reference pill: [Submarine cable resilience](https://www.itu.int/digital-resilience/submarine-cables/)

**Narration**

Data centers connect through physical networks. Terrestrial fiber links buildings and regions; submarine fiber links land networks across oceans. Local access networks complete the connection to businesses, devices and users.

Satellite systems can provide connectivity or an alternate path where geography and infrastructure make other options difficult. Their performance depends on the system and location, so avoid assuming one fixed delay or bandwidth for every satellite connection. The map illustrates how many networks depend on shared physical routes. It isn't a current inventory of every cable or connection.

### 14 — Redundancy Must Survive the Same Failure

Script: `audio/module1/slide_14_failure_domains.txt` · approximately 88 words

Section label: Shared Failures

Media: `figures/module1/shared-failure-routes.svg`

Caption: Separate services may still share a physical risk. Route diversity must address the event being considered.

Reference pill: [Physical network resilience](https://www.itu.int/digital-resilience/submarine-cables/)

**Narration**

Two connections can still share one point of failure. Imagine separate network services that pass through the same trench. A single excavation could damage both. Extra equipment is useful only when it addresses the failure you're trying to withstand.

Resilience combines appropriate separation with ways to continue or recover service. That may include alternate routes, replicated systems and tested recovery procedures. Backups support recovery, but they don't automatically provide uninterrupted service. Ask what event could affect the paths or systems together, and what the service would do next.

### 15 — Cloud Is a Service Model Built on Facilities

Script: `audio/module1/slide_15_cloud_service_model.txt` · approximately 92 words

Section label: Facility and Service

- **Facility** Houses and supports physical equipment.
- **Cloud** Provides on-demand access to pooled configurable resources.
- **Deployment** Can be private, public or connected with other cloud environments.
- **Availability** Depends on the selected service and its architecture.

Media: `figures/module1/cloud-service-layers.svg`

Caption: The service model changes how resources are provided; the physical dependencies remain.

Reference pill: [NIST cloud definition](https://www.nist.gov/publications/nist-definition-cloud-computing?pub_id=909616)

**Narration**

Cloud computing is a way to provide resources as an on-demand service. Users can obtain shared computing capabilities that can be provisioned and released with little manual intervention. The service still relies on physical equipment and facilities.

A cloud can be private to one organization, public, or connected with other cloud environments. It doesn't have to span many data centers, and a private cloud doesn't have to be reached through the public internet. When comparing options, separate the service model from the facility and check which availability features the particular service provides.

### 16 — What Connects the Digital World

Script: `audio/module1/slide_16_digital_world_takeaways.txt` · approximately 90 words

- Digital services depend on connected physical systems.
- Facility labels describe operating arrangement, scale or proximity.
- Resilience depends on maintenance, failure and recovery behavior.
- Cloud describes a service model that still depends on facilities.

**Narration**

Keep four connections in mind. Digital services depend on physical systems. Facility labels describe characteristics such as operating arrangement, scale and proximity. Infrastructure resilience depends on how systems handle maintenance and failures, rather than a label alone. And cloud describes how resources are delivered as a service.

Together, these ideas help you ask clearer questions. What work must the service perform? Where should it run? What physical capacity does it need? And which interruptions must it withstand? The next module follows those questions into the facility's power and cooling systems.

### 17 — Apply the Digital World Model

Script: `audio/module1/slide_17_digital_world_check.txt` · approximately 66 words

Submit all three questions to continue. Use the feedback to review and retry.

**M1-KC2 — What is the primary role of a data center in digital infrastructure?**

- [Distractor] To replace the cloud
  Feedback: Cloud services rely on data-center equipment. A facility supports those services rather than replacing the service model.
- [Distractor] To create mobile apps
  Feedback: Developers create apps. The physical facility provides the equipment and supporting systems on which applications and their services can run.
- [Correct] To store and process data through physical hardware
- [Distractor] To provide customer support services
  Feedback: Customer support is an organizational function that may use digital services. The data center's underlying role is to house and support the hardware that stores, processes and moves information.

Correct feedback: The data center brings physical computing, storage and networking equipment together with the systems that support its operation.

Fallback feedback: Separate the facility's physical role from the applications or organizational activities it supports.

**M1-KC3 — Which statement best describes cloud computing?**

- [Distractor] A single company-owned data center, regardless of how resources are provided
  Feedback: A single facility can host a private cloud, but ownership and location don't establish the service model. Look for on-demand access to pooled resources.
- [Correct] On-demand network access to pooled, configurable computing resources
- [Distractor] Any off-site equipment, even when each change requires manual provisioning
  Feedback: Off-site hosting describes location. Cloud also concerns how resources are provisioned, shared and made available on demand.
- [Distractor] A service that can exist only on the public internet
  Feedback: Private cloud resources can be accessed through private networks. Public internet access is not a requirement for every cloud deployment.

Correct feedback: Cloud describes how computing resources are provided. The physical deployment may vary, and a private cloud need not span many data centers.

Fallback feedback: Look for the resource-delivery characteristics rather than ownership, off-site location or public internet access alone.

**M1-KC4 — Which data center type is specifically placed near its users or activity to reduce latency?**

- [Distractor] Public Library
  Feedback: A library may use local computing, but this label describes an institution. Edge is the infrastructure label that emphasizes proximity to the activity or users.
- [Distractor] Underground Bunker Facility
  Feedback: A bunker can house a data center, but the building form does not tell you how close the computing is to its users. Edge specifically describes that placement goal.
- [Distractor] Tier 1 Cloud Hub
  Feedback: A Tier label concerns site infrastructure capability. It does not specify proximity to users, and 'Tier 1 Cloud Hub' is not the facility type being tested.
- [Correct] Edge Data Center

Correct feedback: Edge placement brings computing closer to the users, devices or activity it serves, which can reduce network delay.

Fallback feedback: Choose the label that describes computing placement relative to a workload or its users.

**Narration**

Use these three questions to connect the terms to their purpose. Consider what a data center physically does, what makes cloud a service model, and why computing might be placed near its users.

Submit an answer to each question before continuing. You don't need every answer correct to advance. Read the explanation for your selected choice, and retry if you want to check your reasoning again.

### 18 — Next: Data Center Physical Infrastructure

Script: `audio/module1/slide_18_physical_infrastructure_next.txt` · approximately 51 words

**Narration**

Thank you for completing The Digital World. You can now connect digital services to their physical foundations and distinguish facility characteristics from cloud services.

Module two examines how power delivery, cooling and physical layout support the equipment. You'll follow those systems together, because a working service depends on the whole chain.

## Approval scope

Approval locks the eighteen Module 1 spoken scripts and their aligned teaching/quiz wording. Figure/media production has its own plan in `_figure_plan_module1.md`. All source knowledge checks remain, including the matching interaction and the three single-answer questions. The cloud definition and location prompt are corrected as described in `_knowledge_check_audit.md`.

Glossary definitions are drafted separately. First-use positions remain provisional until the exact original and generated media have been fully reviewed. No unsupported glossary placement is being treated as approved evidence.

Source preservation, facts and spelling are checked before this handoff. Audio quality, pronunciation, media fit, interaction behavior and LMS tracking require the production build and subsequent QA.

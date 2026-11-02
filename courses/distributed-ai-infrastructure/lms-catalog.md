**Title**\
Distributed AI Infrastructure

**Short Description**\
Explore coordination, state, timing, placement and controlled recovery in distributed AI infrastructure.

**Long Description**

This five-module course connects workload dependencies to the infrastructure and operating decisions that support useful AI capacity. Learners examine distributed state, timing evidence, cross-region placement and controlled recovery through narrated examples, videos and knowledge checks.

**Overall duration: 80 minutes**

**Module 1: Introduction to Distributed AI Infrastructure — 14 minutes.**\
Classify the coordination boundary for a workload. Explain why a straggler can delay a participating group. Name the evidence needed before adding accelerators.

**Module 2: Architectural Assumptions and Distributed State — 19 minutes.**\
Separate model, optimizer, input and execution state. Distinguish data parallelism from model sharding. Review retries, scaling and recovery at a declared group boundary.

**Module 3: Event Ordering, Timing, and Causality — 16 minutes.**\
Separate arrival order, causal dependency and physical timestamps. Explain why averages can hide coordination stalls. Use identifiers and clock uncertainty to investigate a trace.

**Module 4: Cross-Domain Architectures and Geographic Boundaries — 15 minutes.**\
Separate multi-region serving from cross-site synchronous execution. Estimate a simple communication budget with explicit assumptions. Identify provider, identity, data and recovery boundaries.

**Module 5: Orchestration, Scaling, and Infrastructure Guardrails — 16 minutes.**\
Connect workload admission to power, cooling and fabric capacity. Separate detection, decision and safe recovery authority. Apply explicit guardrails to a final deployment decision.

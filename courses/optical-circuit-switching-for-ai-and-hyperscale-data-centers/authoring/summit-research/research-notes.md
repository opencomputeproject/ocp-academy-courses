# OCP 2026 Summit references for the Intro OCS course

Verified 4 November 2026. These are optional extensions of the five-module course, not required full-length viewing. The official index, all 47 PDF pages, and YouTube player metadata were inspected. All source-slide pages were rendered and visually reviewed. No video or audio was downloaded.

## Recommended integration

Use the first talk chiefly in Module 4, the second chiefly in Module 5, and the third chiefly in Module 3 with a Module 5 cross-reference. Preserve the original distinctions between demonstrated deployments, emerging architectures, and ecosystem work.

## Transcript and timing limitation

The official YouTube pages identify the Open Compute Project channel and advertise both authored English and automatic English captions. Caption requests returned HTTP 200 but empty bodies. No transcript content was recovered; no topic timecodes are verified. Use the full video URLs without start-time parameters. PDF page references are verified and are the preferred precise learning anchors.

## Optically-Accelerated AI Clusters Enabled by Interoperable Multi-Vendor OCSs: Use Cases

Presenters: Iwan Kartawira (iPronics), Kazuaki Ueda (KDDI Corporation).
The slide title page also credits Kazuya Anazawa (NTT Inc.).

[Official video](https://www.youtube.com/watch?v=LQJmCZUTHic) | [Official slide link](https://drive.google.com/file/d/1ahYwnygxq6vzFGNZWNrXO7r9fLLhCvg7/view?usp=drivesdk) | [PDF mirror](https://www.dropbox.com/scl/fi/wcmqwcikp940exc7moyqi/Optically-Accelerated-AI-Clusters-Enabled-by-Interoperable-Multi-Vendor-OCSs-Use-Cases.pdf?rlkey=95iivshifs7g4rb30h3lj7e5n&dl=0)

Proposed optical AI-cluster architecture combines packet switching, OCS, CPO and software control. The principal emerging applications are shared spare pools for recovery and topology adaptation to collective communication. Open models and coordinated software are prerequisites; the deck presents planned interoperability work rather than a production deployment report.

Evidence from the actual PDF:

- Pages 4, 5, 6, 7: CPO and OCS perform different functions. EPS retains packet routing while OCS changes physical connectivity at multiple possible network layers.
- Pages 8: Shared spare resources can replace dedicated one-for-one protection; the SDN controller redirects optical paths around a failed leaf or accelerator.
- Pages 9, 10: Direct optical connections may bypass leaf or spine EPS to suit All-Reduce or All-to-All. Coordination with job orchestration and communication libraries is required.
- Pages 10: Temporary disconnection during optical reconfiguration can disrupt RoCEv2. Traffic visibility and hardware/software co-design remain identified gaps.
- Pages 11, 12, 13, 14: A common OCP OCS YANG model is intended to remove vendor-specific controller translators. An OCP/IOWN-GF multi-vendor recovery demonstration is planned for OFC2027.

Suggested course use:

- Module 4 — After emerging topology adaptation or dynamic resource pooling. Suggested PDF pages: 6, 8, 9, 10.
  Prompt: Compare two motives for reconfiguration: replacing a failed resource and matching an AI job’s communication pattern. What software must coordinate each?
- Module 5 — After interoperability and community collaboration. Suggested PDF pages: 11, 12, 13, 14.
  Prompt: Explain how a common model can simplify a controller without eliminating device-specific capability limits.
- Module 2 — Optional technology context only. Suggested PDF pages: 4, 6.

Claim boundaries:

- Do not describe the OFC2027 demonstration as completed in 2026.
- Do not claim measured job speedups or recovery-time guarantees; the selected use-case slides are architectural proposals.
- The deck claims YANG R1.0 released, while the Interfaces deck labels its specification v0.8; do not infer a single current revision from these presentations.

## Standardizing OCS Interfaces for Seamless Integration

Presenters: Richard Yu (Google).
The slide title page also credits Brian O’Connor (Google).

[Official video](https://www.youtube.com/watch?v=_TBtUSijLAM) | [Official slide link](https://drive.google.com/file/d/1lY488pmxQUKovdQz3ZgfUDUj6u5GLH1S/view?usp=drivesdk) | [PDF mirror](https://www.dropbox.com/scl/fi/zynyd5yhs6c5awek4c8pi/Standardizing-OCS-Interfaces-for-Seamless-Integration.pdf?rlkey=bsl6uho36aphs0tgepmjvli0d&dl=0)

Explains a common OCS management approach based on OpenConfig/YANG and gNMI, including capability discovery, connection intent and observed port state. It shows how a shared API can accommodate different OCS technologies and restoration behaviors while reusing existing network-management tools.

Evidence from the actual PDF:

- Pages 4, 5, 6: Existing management facilities can be reused, with OCS-specific changes concentrated in forwarding control, configuration and monitoring. OpenConfig supports familiar tooling and streaming telemetry.
- Pages 7: gNMI provides Get, Set and Subscribe operations over modeled configuration and state.
- Pages 8, 9: Common operations cover connection establishment, restoration behavior, capability discovery, connection status and port health. Devices differ in connectivity constraints, switching behavior and cold-boot recovery.
- Pages 10, 11, 12, 13: The model separates device capabilities and port state from controller-selected connection intent. This permits inspection of requested and actual connections together.
- Pages 14, 15: The presentation identifies the interface specification as v0.8, points to the public OCP repository, and requests YANG/OpenConfig contributors.

Suggested course use:

- Module 5 — After standards and multi-vendor interoperability. Suggested PDF pages: 6, 7, 8, 9, 13.
  Prompt: Distinguish the intended cross-connect from its observed status. Why must an operator check both?
- Module 2 — After comparing OCS technologies. Suggested PDF pages: 8, 9.
  Prompt: Name one capability or recovery behavior that a common API must describe rather than assume.
- Module 3 — Optional bridge from deployment to operations. Suggested PDF pages: 7, 8.

Claim boundaries:

- Do not call all described interfaces finalized or universally deployed; the deck explicitly labels its specification a draft version.
- Do not teach slide-2 power percentages as universal OCS system savings.
- Do not imply every OCS supports arbitrary any-to-any, multicast, unidirectional operation, or the same reboot behavior.

## Zero-Touch OCS Fabrics for AI Scale-Out Infrastructure at Hyperscale

Presenters: Michael DeMerchant (Lumentum Operations LLC), Kannan Raj (Oracle).

[Official video](https://www.youtube.com/watch?v=XjJ8sXzr-Oc) | [Official slide link](https://drive.google.com/file/d/1c2YvZLrfVKRWOfFyc-rVGNZ9kGx56EaH/view?usp=drivesdk) | [PDF mirror](https://www.dropbox.com/scl/fi/tzncpbjmbpyk4m9vn0hli/Zero-Touch-OCS-Fabrics-for-AI-Scale-Out-Infrastructure-at-Hyperscale.pdf?rlkey=kp7bf1cxs1w8nppwnekl939wu&dl=0)

Presents the operating requirements for scalable OCS fabrics: automated device lifecycle, verified end-to-end topology, predictable optical performance and qualified manufacturing supply. Its strongest introductory lesson is that successful optical programming does not by itself prove the intended packet path.

Evidence from the actual PDF:

- Pages 3, 4, 7: Operational state requires endpoint evidence because the OCS cross-connect does not inspect packets. Optical presence or cross-connect status alone cannot prove the intended peer.
- Pages 5, 6: Automation spans initial identity and credentials, topology qualification, continuing health, upgrades and recovery. gNMI, gNOI and gNSI require common behavior and service semantics as well as transport compatibility.
- Pages 8: Distinct expected peer patterns expose cabling mistakes and permit parallel path qualification, improving on simple serial loopback checks.
- Pages 9: A safe change sequence uses intent, prechecks, programming, validation and commit, with rollback and retained evidence on failure.
- Pages 10, 11, 12, 13: Mass-production processes, alternate supply and consistent insertion loss complement software conformance. The presenters call for an operator-ready lifecycle profile and shared conformance tests.

Suggested course use:

- Module 3 — After production deployment considerations or operational lessons. Suggested PDF pages: 4, 5, 7, 8, 9.
  Prompt: An optical path reports connected, but the endpoint sees the wrong peer. Has deployment validation passed? What evidence is still required?
- Module 5 — After ecosystem readiness and standardization. Suggested PDF pages: 3, 6, 10, 11, 13.
  Prompt: Explain why manufacturing consistency and a shared conformance suite both matter to multi-vendor adoption.
- Module 4 — Optional scale-across context only. Suggested PDF pages: 2, 12.

Claim boundaries:

- This talk supports operational requirements, not a documented count, size or measured performance of Oracle production OCS deployments.
- Slide 12 presents vendor optical-loss data and link-budget compatibility examples; do not generalize them into universal product specifications or a complete end-to-end loss budget.
- The operator-ready profile is a call to action; do not present it as an already mandatory OCP standard.

## Cross-talk synthesis

The three talks form a useful teaching sequence: a programmable optical fabric needs both a useful application and a reliable operating model. Shared management models make multi-vendor integration possible, but they do not automatically prove correct cabling, successful endpoint communication, compatible optical loss, coordinated AI-job behavior, or repeatable manufacturing. Keep those responsibilities distinct.

The two interface-version statements are inconsistent as a single revision claim: the Use Cases deck reports YANG R1.0 released, while the Interfaces deck describes specification v0.8. They may concern different artifacts or update timing; the research does not resolve this. Course language should say that open interface work is progressing, or link to the repository for current status, without assigning an unverified universal version.

## Asset inventory

- `reference-map.json`: structured course integration map and source provenance.
- `official-index-rows.json` and `recorded-content-index.html`: archived official source listings.
- Three PDFs, per-page JSON text, readable text files, and rendered contact sheets.
- Three YouTube metadata records and archived public watch-page HTML.
- `youtube-access-check.json`: successful public page access and caption availability detection.

Public watch-page metadata is evidence of video identity and duration, not evidence that the video was watched or its spoken content transcribed.

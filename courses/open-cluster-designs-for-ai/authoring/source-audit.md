# Source audit — 29 October 2026

The course uses the five contributions returned by the [official filtered contribution collection](https://www.opencompute.org/contributions/?project=Strategic+Initiatives%2FOpen+Cluster+Designs+for+Artificial+Intelligence), plus the 2026 Summit current-activities presentation for work in progress. All five documents were extracted page by page; critical table, endpoint and maturity statements were checked in rendered PDF pages. Learner links use live OCP and Academy pages, not GitHub research locations.

| Contribution | Revision | Viewer pages | Main teaching use |
|---|---|---:|---|
| Open Cluster Designs for AI white paper | 14 January 2026, 1.0 | 22 | Hierarchy, functional networks, design scope |
| OPG-M System Architecture | 14 January 2026, 1.0 | 57 | Building-block equipment, layout and endpoint records |
| XOC-N System Architecture | 14 January 2026, 1.0 | 62 | Shared cluster layer and verified leaf–spine identities |
| Open Cluster Designs Aligned AI Training Fabric Reference Architecture | April 2026, 1.2 | 77 | Wiring, planes, fabric functions and operating implementation |
| Open Cluster Designs Aligned AI Inference Fabric Reference Architecture | April 2026, 1.2 | 67 | Workload dependencies, gateways, tenancy and validation |
| Current Activities in the Open Cluster Designs for AI Strategic Initiative | 2026 Summit | 29 slides | Illustrative liquid-cooled OPG-576, 800G/1.6T direction |

Canonical URLs, hashes and page counts are in `source-manifest.json`; the local research PDFs are retained outside Git. Teaching PDF pills cite verified PDF viewer pages. The final resource slide links to whole documents/collections without page fragments. Source revision, form factor and selected configuration remain explicit.

## Reconciliations and limits

- January hardware examples use air-cooled eight-xPU servers and 400G attachments. April fabric references retain the eight-xPU-server form factor while separating logical architecture from rack density/cooling. Neither establishes full qualification of an arbitrary rack-scale compute domain.
- OPG-M p.46 Table 27 lists four 51T leaves, while its detailed Clos layout and utilization on pp.28/47 use two 51T leaves; the rail example uses four 26T leaves. M2S6 teaches the reconciled detailed configurations and requires the records to agree before ordering.
- In-band uplink summary quantities differ between OPG-M p.26 and XOC-N p.21; XOC-N's actual p.50 connection record uses six. The course avoids a universal summary count.
- Training p.29 and its earlier tier example differ on spine quantities; training p.33 dual-plane leaf counts also conflict with the stated port budget. The course does not reproduce those disputed quantities.
- Training p.39's dual-plane comparison suggests twice the bandwidth for two 200G links versus one 400G link. M3S5 uses actual nominal arithmetic: 400G, 400G and 800G respectively for 1×400, 2×200 and 2×400. Continuity still requires end-to-end validation.
- OPG-M power-table units include a W label for kW-scale entries. No disputed power number is taught as a site requirement.
- Verified trace: OPG-M p.29 Table 10 connects SOL1 port 1's two 400G breakout legs to N1 NIC1 and NIC5. The separate uplink is OPG1 SOL1 port2 optical-module port1 to SO1 port1 optical-module port1; XOC-N p.25 Table9 uses alias O1S1 (2,1). The video keeps these identities and avoids asserting an unchecked breakout-leg order.
- Training Minimal retains a scale-out back-end while converging SO-C/storage; Full separates those functions. Minimal Inference can omit the scale-out back-end for independent single-host execution; Distributed Inference adds the path for cross-host dependencies without removing the front-end/gateway.
- Gateway NAT does not supply every required firewall/ACL policy (inference pp.33–34). A virtual lab checks intent and workflows, not physical reach or production-scale performance. An SLI is a measurement; an SLO is a target.
- Hedgehog and SONiC are contributed implementation examples, not requirements imposed on all OCP clusters. Independent out-of-band recovery remains distinct.
- Summit slide7 labels OPG-576 illustrative and work in progress. M4S8 preserves that status. The recording is a reference, not part of the duration estimate. No claim of a complete listening/transcription of the Summit recording is made.

## Cross references

Course 92 provides broad system context; course 69 supplies the facility learning path. AICC course 58 and its project are introduced in M4S8 for broader deployment context. The deprecated learning-plan version of Open Systems for AI is excluded. Course 93 is an authorized future LMS destination even before publication.

## Source notices

January contributions carry CC BY-SA 4.0 notices. The inference document's footer and license body differ (BY-SA versus BY); retain the source notices and use the more conservative share-alike treatment for its adapted teaching material. Authors and source-specific attribution are in `NOTICE.md`. This is an authoring record of the notices, not a change to the repository's software license.

## Module 2 figure revision — 30 October 2026

The original XOC-N Figures 6 and 7 now replace simplified diagrams on M2S6/M2S7. Figure6 (p.24) shows eight spine switches and sixteen leaves across eight OPG-128s; Figure7 (p.33) shows eight spines and thirty-two leaves. Narration relates these to January's two 51T-class versus four 26T-class leaves per pod group and keeps April's same-platform comparison separate. Source drawings are cropped only, attributed in visible captions, and linked at the exact PDF viewer pages. See `reused-figure-inventory.json`.

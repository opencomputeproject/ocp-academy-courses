# AI Native Edge-MHS source analysis and scope controls

Planning baseline: 13 November 2026. These notes support the proposed single-course, three-module outline in `../_outline.md`. They identify technical facts, source conflicts, CAD limitations and overlap boundaries before course authoring.

## Reviewed sources and provenance

| Source | Review and role |
|---|---|
| [Base Specification v1.0.0](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-Base-Specification_V1.0.0.pdf) | All 98 pages extracted/read; selected tables, dimensioned drawings and conflicting passages rendered and inspected. Governing technical source. Printed pages match PDF viewer pages. Header retains “Rev 0.9” alongside “Version 1.0.0”; preserve the exact supplied release identity instead of silently editing it. |
| [v1.0.0 3D design archive](https://www.opencompute.org/wp-content/uploads/2026/11/AI-Native-Edge-MHS-V1.0.0-3D-Files.zip) | Official archive downloaded through its contributions-page browser link. Four members inventoried; both STEP assemblies imported for topology validity and bounds. Archive contents and SHA-256 are in `_cad_inventory.json`; geometric observations in `_cad_geometry.json`. |
| [OCP contributions entry](https://www.opencompute.org/contributions/?project=AI+Computing+Continuum%2FAI+Native+Edge+MHS) | Confirms the design archive is a supporting contribution to the base specification. |
| [AICC project](https://www.opencompute.org/projects/aicc/) and [AI Native Edge-MHS subproject](https://www.opencompute.org/projects/aicc/ai-native-edge-mhs/) | Establish current project relationship and context. Project-level scope does not expand the detailed v1.0.0 base-spec contract. |
| [DC-MHS specifications index](https://www.opencompute.org/projects/server/mhs/dc-mhs-specs-and-designs/) | Confirms v0.7 M-PNP package listing and separately versioned specification documents. The page distinguishes current workstream material from signed contribution releases. No assumption that package version equals final approval or deployed LMS edition. |
| Adjacent local AICC and M-PNP course sources | Actual module/slide content inspected; paths and boundaries below. No existing course modified. |
| 2026 Global Summit recordings/decks | Astra reviewed listing links, recording metadata and associated decks. `_video_plan.md` records the exact reviewed evidence and limitations. Conference content is explanatory/contextual, not replacement normative text. |

The figure-caption manifest `_source_figures.json` inventories actual body captions, not stale contents entries. Repeated figure numbers must be identified by page. No source figure has yet been chosen as a final extracted course asset.

## Requirements and numerical anchors

The following is an authoring fact register, not an exhaustive compliance checklist. Preserve each condition and exact numeric value. A course interaction must distinguish the requirement, the observation and the engineering conclusion.

| Topic | Verified rule or fact | Actual source page |
|---|---|---:|
| Requirement strength | “Shall” indicates a requirement; “Should” a recommendation; “May” permission. Section 6 explicitly says its table is not a checklist because a row can contain multiple requirements. | 14–16, 20 |
| Classes | Class N width 168mm; Class L width 295mm; allowed HPM depth 250mm–365mm in both outline sections. | 21–22, 37–38 |
| CCI | Five listed planning intervals: 260mm, 280mm, 305mm, 350mm, 365mm. Outline tables give N305/L305 depth 305.59mm; designators round down to the nearest mm. These do not set complete chassis dimensions. | 22–24, 37–38 |
| Near/far and scaling | Near/far are relative to datum. Fixed features reference the datum; floating features reference the edge. A fixed feature can drop outside a shorter outline. | 23, 27–31 |
| Standard tolerances | Datum-to-fiducial ±0.076mm; datum-to-profiled edge ±0.254mm; datum-to-drilled-hole center ±0.127mm; profiled edge-to-edge ±0.127mm; feature size ±0.100mm; PCB thickness ±10% nominal. Use the exact dimension category, not a single universal tolerance. | 36, Table 4 |
| Negative PCB features | Allowed locally, provided required features are not compromised and they do not remove a full left/right edge to create a nonstandard width. System dependence on a notch can reduce interchangeability. | 39–40 |
| Datum/holes | Required hole size, pad, component KOZ and route KOZ must be followed; additional holes follow Detail A. Vias shown are reference only. Class N has 5 required near-side mounting/riser holes when risers are implemented, 2 without. Class L count is disputed; see conflicts. | 40–46 |
| Secondary Zone 1 | Universal component height restriction 1.6mm; local tall-component exceptions ≤400mm2 per instance and separation ≥10mm. Combined board/component 5.2mm is recommended guidance, not an extra universal “shall.” | 47–48 |
| Secondary Zone 2 | Required zero-height chassis-hook KOZs, including floating far-edge KOZs at all depths; partial KOZ applies where the edge intersects the area. Alignment-post/grounded-retention-barb maximum 3.20mm; power/signal through-hole leads not permitted in hook keepouts. | 49–54 |
| Secondary Zones 3–4 | Support approaches are illustrated; backplate allowance is calculated as 6.2mm − HPM thickness − 0.08mm standoff tolerance − other allowances. | 55–56 |
| Board thickness and stack-up | Maximum nominal HPM thickness 3.18mm with ±10% tolerance. The 6.2mm mounting-height assumption supports the example stack-up, but the actual chassis mounting height is a system choice. Connector offset is a BOM choice outside base-spec scope. | 57–58 |
| Retention/handling | Chassis retention hole and handle-hole interface are required; the handle hole is near the far edge. Installing a handle in it is not mandatory. | 59–61 |
| DC-SCM/NIC | Recommended DC-SCM R2.2 CFF placement; mandatory battery-backed voltage interface. OCP NIC is optional; if implemented, the specified placement condition applies. Keep-in-volume conflicts need review. | 26, 62–63 |
| M-PIC non-power | Electrical implementation follows M-PIC. Intrusion, control panel and PDB-management connectors are required but may be depopulated. Recommended exact placements sit within mandatory allowable zones. Internal USB/boot storage are recommended. | 63–67 |
| HSIO | Table 6 lists SFF-TA-1033 with 21A power for near fixed risers; SFF-TA-1016, -1026, -1033 for other HSIO. All implemented HSIO must be M-XIO-defined and in the table. | 69–73 |
| Riser applicability | Class N supports 2 fixed positions; Class L 3. Full population is not required. Implemented near fixed risers have mandatory connector/position and 21A-power-block conditions. “Recommended connector” in a figure caption does not erase body requirements. | 70–73 |
| Primary heights | 12mm strongly recommended; 11.3mm required with PCIe CEM cards directly above HPM/peripherals, with stated exceptions; 6mm required when PCIe risers are implemented. Apply source exemptions and distinguish soldered/mated assemblies from later-added heatsinks/shrouds. | 74–77 |
| Custom/storage/NIC limits | No formal Platform Custom Zone; E1.S placement/implementation outside scope. Direct OCP NIC DSFF support is outside scope; cabled implementation details are not defined. | 78–79 |
| Far power | Cabled ingress/egress uses 2x6+12SB or 2x3+6SB PICPWR. The far zone must include the body of at least one 2x6+12SB connector and enough connectors for full HPM ingress budget. That second clause is in the body even though table item numbering skips 38. | 81–85, especially 83 |
| Power ratings versus delivery | Listed connector ratings 864W (2x6), 486W (2x3), riser connector 252W do not establish actual delivered system power. Each implemented fixed riser must receive at least 87W, supporting a 75W CEM card plus conversions/miscellaneous load. | 81, 86 |
| Electrical dependencies | Read M-PIC, M-XIO, M-CRPS and M-PESTI for the electrical interface contract. Base-spec form factor does not establish firmware/discovery interoperability. | 17–18, 88 |

## Examples, exclusions and future material

The 181mm Class N pitch is the shown common-chassis arrangement in §11.2.1, p. 34, and the chassis/tray example on p. 30. It is not a promise that arbitrary N/L boards fit every rack enclosure. The chassis determines maximum supported depth; cables, trays, standoffs, connector variants and I/O must also be reviewed. Chassis/board-pan geometry is not fully specified (pp. 29–30, 49, 97).

The 6.2mm Z-height stack-up on p. 58 is explicitly an example. Distinguish it from mandatory board thickness/zone constraints and the calculated backing-plate allowance (pp. 56–57). The conceptual renderings on pp. 90–94 and power-flow examples on pp. 95–96 are application examples; p. 97 warns its illustrative hole placements may not match the HPM specification. Page 92 also describes a configuration with riser placements outside the specified locations; that illustration cannot waive §12.9 fixed-riser conditions.

Section 5.1–5.2, p. 13 excludes compute-core design (CPU, memory, VRs, SMP routing), compute-core debug, thermal solutions, reliability/design-in details, BOM population, fan connections, complete risers/chassis, environmental requirements/materials, software, firmware, detailed hardware management and security. Their interface requirements can still apply at the HPM boundary. Do not convert “outside this base specification” into “unimportant to the finished system.”

Section 16.4, p. 98 lists timing support, blind-mate HPM support and a 162mm HPM as potential future material. Section 10.1, p. 23 permits discussion of adapted/interposer approaches without defining a native blind-mate interface. Section 13, p. 80 places alternate-source conversion in system power infrastructure and treats native 48V as future consideration. Conference OAC/intermediate-width proposals cannot be added to the released requirements.

## Source conflicts requiring editorial controls

| Issue | Evidence | Authoring disposition |
|---|---|---|
| Class L hole count | Table 1 item 10 p. 14 says **6** required near-side mounting/riser holes; §12.2.2 p. 44 says **7**; actual hole drawing is p. 46. | Show as a source-conflict review case. Obtain workstream clarification before definitive hole-count quizzes or compliance conclusions. A CAD observation does not resolve the normative conflict. |
| DC-SCM power version | Table 1 item 41 p. 16 and §13.4 p. 86 say **R3.2**; §§10.6/12.7 and reference §15 point to **R2.2**, pp. 26/62/89. | Do not silently replace either version or teach a pinout/power rule inferred from the typo. Flag the interface baseline for clarification. |
| Contents and figure references | Body framework is Fig. 3 p. 21; N/L overview is Figs. 11/12 pp. 32/33; outlines Figs. 15/16 pp. 37/38; secondary zones start p. 47; references p. 89; future material p. 98. Contents/figure lists retain earlier numbering. Fig. 42 appears at p. 44 and p. 77; Fig. 58 labels two different drawings pp. 97–98. | Cite actual page + section + caption; never auto-map from figure number alone. |
| Four versus five CCIs | Class N outline prose p. 37 says four distinct CCIs; its table and §10.1 p. 22 list five. | Display the five enumerated values with source pointer; preserve the inconsistency in maintainer notes. |
| M-PNP description copy | §8 p. 17 repeats the M-PESTI expansion in the M-PNP entry. | Use the actual M-PNP title and adjacent course/spec sources; retain distinction between framework and sideband interface. |
| Section 6 numbering/completeness | Item 38 absent; far-power mandatory text remains §13.2.2 p. 83. “Table 66” and several figure/section references are stale. | Do not build a compliance checklist by copying the table rows alone. |
| Summit dimension prose | Edge-MHS deck p. 9 says 18mm × 22mm for the recommended CFF zone; its drawing shows 18mm width, 117.1mm height and 22mm offset. | Exclude this prose value from requirements/answers. Astra flags the mismatch in the video plan. |

## CAD content and limits

The archive contains only four files: two `.stp` assemblies and two `.asm.1` assemblies. There are no separate 2D drawings, README, chassis, tray or complete compute-system files. Both STEP headers identify PTC Creo Parametric 2024401 exports on **2025-12-09**, earlier than the specification's publication date. This is provenance to retain, not proof that the package is invalid or compliant.

The STEP files declare millimetre length units and import as valid solid topology. The Class N board solid has local XYZ extents **168 × 1.57 × 365mm**, with two connector occurrences; Class L has **295 × 1.57 × 365mm**, three connector occurrences and a thin `SCM_CFF_KIZ_2` marker. These are observed examples. **1.57mm is a modeled choice, not a required board thickness.** Bounding boxes include the modeling kernel's numerical margins; they are not toleranced measurements. Local CAD axes are not automatically the specification's XY/datum reference.

The native `.asm.1` headers identify Creo assemblies and contain references to subordinate assembly/part names not separately included in the ZIP. Their self-contained native reconstruction has not been verified in Creo. Use the imported STEP geometry for accessible teaching views; do not promise editable native assemblies will open with all dependencies.

The supplied models are 365mm deep. N350/L260 exercises must use published drawings and/or clearly labeled teaching derivatives. Preserve the original files and cite the applied changes. STEP import/topology validity does not verify every hole, connector, clearance, electrical connection or engineering requirement. These models do not support complete thermal, service-path, powered-system or collision-free claims. A thin marker shape is not a functional DC-SCM assembly.

## Adjacent course overlap evidence

Reviewed AICC source:
`../ai-computing-continuum/course.json`

The 45-minute intermediate Slides course is titled *AI Computing Continuum: Extending AI Beyond the Hyperscale Data Center*. Module 1 covers inference and hyperscale-adjacent motivation. Module 2 slides 3–6 cover five domains, site constraints, disaggregated inference and modular toolkit. Module 3 covers scale/sync/reach-across. Module 4 covers ecosystem roles and use cases. The new course needs only a short context bridge; board dimensions, datum-referenced geometry and mechanical review are new depth.

Reviewed current M-PNP source:
`../ocp-mhs-modular-plug-and-play-m-pnp/course.json`

Also cross-checked the v0.7 preview in `MPNP/MPNP_Academy_v0.7_Preview/course.json` and identified the older v0.5 source at `MPNP/MPNP_Academy_SCORM/course.json`. The v0.7 four-module course covers: MHS/M-PNP vision; FRU/discovery/boot; HPM/peripheral programmable devices; interoperability/schemas/tools/adoption. Module 1 slides 3–5 give the physical/electrical versus logical distinction; Module 4 slides 3/6/7 cover evidence and reproducible baselines. Keep those ideas as brief links/handoff cards. Do not reteach schemas, discovery algorithms, PD registers/states or firmware tooling.

M-PNP's v0.7 package includes FRU/Discovery/Boot v0.7.0 RC1, HPM/Peripheral PD v0.7.0 RC1 and Interop v0.3.0. Package and per-file versions remain separate. These inspected local sources do not verify the deployed LMS edition. No update to either neighboring course is authorized or needed for this scope.

## Terminology planned for first use

| Term | Learner-facing meaning | Source |
|---|---|---|
| HPM | Host Processor Module; the PCB/PCBA form factor defined by this base specification. | §9 p. 19 |
| CCI | Common Chassis Interval; an HPM length planning point associated with common infrastructure. | pp. 18, 22 |
| Datum | Reference point/axis/plane from which dimensions and tolerances are measured. | p. 19; §12.2 p. 40 |
| Near / far | Relative location closer to or further from the common datum. | p. 31 |
| Fixed / floating feature | Datum-referenced feature / edge-referenced feature as outline changes. | p. 27 |
| KOZ | Keep Out Zone; the specific component/routing/height restrictions depend on the cited zone. | p. 19; pp. 40–58 |
| CFF / DC-SCM | Compact Form Factor / Data Center Secure Control Module. | p. 19; p. 62 |
| B2B / B2C / hybrid | Board-to-board / board-to-cable / a combined mated interface. | p. 68 |
| HSIO | High-speed I/O; use the actual connector/companion-spec conditions for a design. | p. 19; pp. 67–73 |
| PDB / PICPWR | Power Distribution Board / platform infrastructure power connector family. | pp. 80–86, companion M-PIC |

During authoring, add glossary aids at verified first substantive use and attach page-specific source links where learners need them. This inventory is not permission to add unsupported glossary pills or duplicate course-boundary content.

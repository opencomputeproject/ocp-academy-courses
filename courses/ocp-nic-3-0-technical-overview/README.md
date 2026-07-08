# OCP NIC 3.0 Technical Overview

A comprehensive OCP Academy course on the OCP NIC 3.0 Design Specification, version 1.6.0.

This folder contains the editable course source for the SCORM package. It includes the course definition, narration scripts, and lightweight figure assets, but not generated audio, rendered HTML, or LMS package outputs.

## Modules

| Module | Title | Focus |
|---|---|---|
| 1 | Introduction to OCP NIC 3.0 | The specification purpose, form factors, capabilities, non-NIC scope, and contributing ecosystem. |
| 2 | Mechanical Architecture | SFF, TSFF, DSFF, and TDSFF dimensions, faceplates, connectors, guide-rail conversion, and retention. |
| 3 | Electrical Interface & Power | 4C+ signal groups, SFF/DSFF connector usage, signal ownership, bifurcation, power states, and hot-swap scope. |
| 4 | Management & Sideband Interfaces | RBT, MCTP, NC-SI, FRU EEPROM identity, DSFF OEM records, and telemetry responsibilities. |
| 5 | Signal Integrity, Thermal & Environmental | PCIe compliance fixtures, airflow direction, cooling tiers, thermal design, shock/vibration, and durability. |
| 6 | Compliance, Ecosystem & Future | Regulatory compliance, version 1.6.0 changes, OCP resources, and active SFF/DSFF design direction. |

Each module includes a knowledge check before its final transition or completion slide.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-nic-3-0-technical-overview
```

For local QA using previously generated audio:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh ocp-nic-3-0-technical-overview
```

The finished SCORM folder and LMS zip are created under `build/`.

## Public References

- OCP NIC 3.0 Design Specification, Version 1.6.0: https://www.opencompute.org/documents/ocp-nic-3-0-r1v60-20250410a-tn-no-cb-pdf
- OCP NIC Subproject: https://www.opencompute.org/community/mezz-nic

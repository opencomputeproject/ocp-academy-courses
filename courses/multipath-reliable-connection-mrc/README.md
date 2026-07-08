# OCP Academy - MRC Technical Overview

Multipath Reliable Connection (MRC), an open RDMA transport for AI training fabrics.

This folder contains the editable course source for the SCORM package. It includes the course definition, narration scripts, and lightweight SVG assets, but not generated audio, rendered HTML, or LMS package outputs.

## Modules

| Module | Title | Focus |
|---|---|---|
| 1 | Why MRC | AI training tail latency, RoCE limits, and the role MRC plays in multipath RDMA fabrics. |
| 2 | Inside MRC | Packet spraying, SRv6/uSID source routing, out-of-order receive, SACK/NACK recovery, and congestion response. |
| 3 | Deploying MRC | Multi-plane topologies, production evidence, performance results, API modes, and deployment tradeoffs. |

Each module includes a knowledge check before its final transition or completion slide.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh multipath-reliable-connection-mrc
```

For local QA using previously generated audio:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh multipath-reliable-connection-mrc
```

## Public References

- OCP Multipath Reliable Connection (MRC) Specification Revision 1.0: https://www.opencompute.org/documents/ocp-mrc-1-0-pdf
- Resilient AI Supercomputer Networking using MRC and SRv6: https://cdn.openai.com/pdf/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf
- Supercomputer networking to accelerate large scale AI training: https://openai.com/index/mrc-supercomputer-networking/

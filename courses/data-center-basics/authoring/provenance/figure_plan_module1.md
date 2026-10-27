# Module 1 figure and media plan

Status: ready for editorial approval alongside Module 1 scripts. No new figures, animation encodes or narration audio have been generated.

Use the maintained OCP Academy slide frame, typography and green/neutral palette. Keep headings, course name, branding, reference pills and glossary controls outside teaching media. New figures use simple editable SVG; the animation uses editable HTML/CSS and a separate encoded media file. No AI-generated bitmap images are proposed.

## Slide-by-slide treatment

| Slide | Treatment | Instructional purpose / production note |
|---:|---|---|
| 1 | Maintained title layout | New simple rack-shaped course mark, without text inside the SVG. Use the separate `DC` badge. |
| 2 | Maintained four-module overview | Compact module list and honest approximate duration. No decorative animation. |
| 3 | Original introduction video | Reuse the exact MP4 and its poster. Full playback controls, original sound, no loop, learner-initiated playback. A brief new audio introduction ends before video audio plays. |
| 4 | New silent service-journey animation | Show a request moving from user → network → compute/storage, followed by a response returning. A static support band identifies electricity and heat removal. Motion teaches the transaction sequence; it replaces a static flow figure. |
| 5 | Original data-center explanation video | Reuse the exact MP4 and poster. Same sound/playback policy as slide 3. Full source text/audio review is required before final glossary placements. |
| 6 | New capacity-and-units SVG | Show compute, storage and network capability supported by electrical and cooling capacity. Include the compact worked relationship `1 kW × 1 h = 1 kWh`. Avoid showing kW as energy or floor space as sufficient capacity. |
| 7 | Accessible HTML comparison table | Four Tier capability rows. Replace the original uptime/downtime infographic; do not reproduce its numerical guarantees. |
| 8 | Four related cards | Distinguish enterprise use, colocation service, hyperscale operation and edge placement. A short subtitle explains overlap. Keep card tones unified. |
| 9 | Source matching interaction | Retain all four source pairs, shuffle the selectable side, support keyboard operation and explain each pair after submission. No glossary controls. |
| 10 | New location-tradeoffs SVG | Put workload requirements at the center of a small decision matrix: connectivity/proximity, power/cooling resources, risk/recovery, and cost/data requirements. Use grouping rather than ambiguous directional arrows. |
| 11 | Six regional-example cards | Retain all six source metro examples in two rows. Short labels avoid unsupported rankings and tiny map annotations. This is the outline's readable alternative to the source clickable map. |
| 12 | New remote-research SVG | Instruments → local processing/storage; a separate remote link reaches other facilities. Clearly distinguish local capability from external connectivity. Include no map-based sovereignty claim. |
| 13 | Reused source cable map | Preserve the original image and its embedded map/data credit. Caption it as illustrative rather than a current route inventory. Provide zoom; avoid implying precise current cable topology. |
| 14 | New shared-failure-routes SVG | Compare two links in a shared trench with physically separated routes. The comparison should show the failure boundary without implying that physical separation solves every resilience problem. |
| 15 | New cloud-service-layers SVG | Separate resource delivery from the physical compute/storage/network layer and supporting facility. Do not imply cloud requires virtualization, public internet access or multiple data centers in every implementation. |
| 16 | Maintained takeaways layout | Four concise summary statements. No extra diagram needed. |
| 17 | Three source single-answer questions | Preserve the three original concepts and keys, with documented cloud/location repairs. Each wrong answer gets its own explanation. Use a readable question-by-question or scrollable maintained quiz presentation rather than squeezing all answers onto one fixed-height canvas. |
| 18 | Maintained module-completion layout | Thank the learner and introduce Module 2. Keep the LMS-tracked handoff distinct from isolated local review navigation. No glossary controls. |

## Animation specification: service journey

- Asset: `figures/module1/service-journey.mp4`; source under `animations/module1/`.
- Master pass: 14 seconds, finite one-shot timeline. Poster around 7 seconds, chosen after reviewing the actual rendered state.
- 0–2 seconds: stable system diagram; request appears at the user endpoint.
- 2–5 seconds: request traverses the network and reaches computing equipment.
- 5–8 seconds: compute/storage relationship highlights as the request is handled.
- 8–12 seconds: response returns through the network to the user endpoint.
- 12–14 seconds: hold the final completed exchange. No subordinate animation restarts.
- The supporting power/cooling band remains visible throughout. Do not animate a capacity gauge or energy counter that the narration does not explain.
- Player: short silent loop, `autoplay: true`, `loop: true`, `muted: true`. Narration playback/scrubbing uses the maintained loop-time behavior. No narration-master video mode is proposed.
- Capture lossless PNG frames at 1920 × 1080 or greater; encode exactly one master pass with high-quality H.264 or VP9. The encoded final frame must be the final source state.
- Inspect the first, quarter, midpoint, three-quarter and final states plus each transition; inspect one full pass and the final second for resets, overlap and flicker.

## Diagram and slide QA

Run the shared SVG arrow checker before rendering or encoding. Every arrow shaft ends at the center of the arrowhead's flat back, and the tip stops at the target boundary. Give labels at least 0.75 em of interior clearance; measure rather than assume text fit. Inspect every final figure/poster at full size and within desktop/mobile slides in light and dark themes.

Retain a clean white rounded media frame with an even 15–20 px inset. Keep learner reference/glossary controls in the normal content flow beneath the media or last teaching element.

Original media receives complete playback, visible-text and audio review. Record reviewed text with a hash of the exact retained media, then determine true first substantive glossary use. Do not mark a candidate glossary placement verified before that review.

## Source re-use and corrections

The original MP4 files and map are retained as binaries with their recovery hashes. The Tier graphic is replaced for accuracy. The source location markers become readable cards and a separate remote-use diagram. Other source facts and interaction concepts are preserved in the slide text, scripts and source references rather than by reproducing the Rise click mechanics.

Original contribution acknowledgment remains in course metadata and learner credits. The new narration and code-authored diagrams are identified as part of this adaptation, not attributed to the original contributor.

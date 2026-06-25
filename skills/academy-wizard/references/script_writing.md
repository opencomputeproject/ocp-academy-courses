# Writing narration scripts

The narration is the spine of every slide. Visuals support it, not the other way around.

## Voice

Warm, authoritative, and curious. The narrator is the kind of senior engineer who has seen three generations of the technology and can explain why each one came to be without condescension. Confident, never hyped. The OCP community values rigor.

## Tone targets

- **Active voice over passive.** "The NIC negotiates link speed at boot" beats "Link speed is negotiated by the NIC at boot."
- **Natural contractions.** "It's" and "you'll" are how people talk. Reading "it is" out loud sounds stilted.
- **Define acronyms on first use.** "NC-SI — the Network Controller Sideband Interface — provides…". After first use, acronym alone is fine.
- **One idea per sentence.** Listeners can't re-read. Short sentences land.
- **No filler.** Strike "basically," "essentially," "in order to," "at the end of the day."
- **Numbers in words for small values, digits for large.** "Two PCIe lanes" but "64 GT/s."

## What not to say

- **No "as you can see on the slide."** The audio plays automatically as the listener is also reading. Don't direct their attention to the screen explicitly.
- **No "in this slide" or "let's move on to the next slide."** The transition is visual.
- **No filler intros.** Don't open with "So, welcome to slide 4." Get into the content.
- **No marketing-speak.** "Industry-leading," "best-in-class," "cutting-edge" — strike them all. State facts.
- **No internal source labels unless approved.** Do not say "the webinar," "the transcript," "the article," "the slide deck," "our source material," or vendor names in narration unless the user explicitly wants that source named. Prefer the underlying technical point. OCP guidelines, OCP contribution documents, and user-approved panel references may be named when they help credibility.

## Slide-type templates

These are starting points, not rigid forms.

### Title slide (~70 words, ~30s)

> Module two. Form factors and mechanical design. In this module, we'll cover the four active OCP NIC 3.0 form factors, how they share a common connector, the dimensions and tolerances that matter for system integration, and the retention features that keep cards seated through shock and vibration. By the end you'll be able to read a NIC spec sheet and know which form factor fits your chassis. Let's get started.

### Objectives slide (~140 words, ~60s)

Begin with "By the end of this module, you'll be able to…" then narrate each objective in a sentence. Don't read the objectives verbatim — paraphrase so the audio and the slide complement each other.

### Content slide (~210–280 words, ~90–120s)

Open with the *why* of this slide in one sentence — what gap in understanding does it fill. Walk through the bullets in order, but expand each into a sentence or two of context. Close with the *implication* — why this matters for the learner's work.

### Takeaways slide (~140 words, ~60s)

Recap the module in plain language. The bullets on screen are the headline; the narration is the elaboration. Don't just read the bullets — that's redundant and boring.

### Up Next slide (~60–80 words, ~30s)

This is the moment to acknowledge the learner finished a module and to set up the next one. Don't rush past it. Two beats: thanks for finishing this module, then a teaser for what's next.

> Nice work — you've finished module two, form factors and mechanical design. You now know the four active form factors, the common connector, and how cards are retained in the chassis. Next up: module three, the electrical interface and PCIe. We'll dig into the pinout, link bifurcation, power states, and hot-swap. See you there.

### Course Complete slide (~70–90 words, ~35s)

Final module's final slide. Thanks for the module AND wraps the course. Be warm — the learner just spent real time with you.

> That's a wrap on module six and on the course. Thank you for sticking with us through the full OCP NIC 3.0 Academy. You've worked through the form factors, the electrical interface, management and firmware, signal integrity and thermals, and now compliance and the roadmap. You're ready to read a NIC spec sheet and contribute meaningfully to the conversation. Visit opencompute.org to go deeper. Until next time.

## Pacing markers

If you want a brief pause, use a period or a comma. TTS engines respect punctuation. Don't write `(pause)` — most engines say it out loud.

Avoid commas inside numbers ("64,000" reads correctly, but lists like "1,2,3" read as "one comma two comma three" in some engines — use "1, 2, and 3").

## Pronunciation hints

Some technical terms confuse TTS. Spell them phonetically in the narration script *only when necessary*, and document the substitution in a comment at the top of the script file:

```
# pronunciation: NC-SI -> "N C S I"; PCIe -> "P C I E"
```

Cloud TTS engines (ElevenLabs, OpenAI) generally handle technical acronyms well. `say` does not — review and adjust if falling back.

### TTS pronunciation cheat sheet

These are field-tested substitutions for ElevenLabs Turbo v2.5 and similar voices. Bake them into your scripts the first time you write the term, not after you hear the TTS botch it.

| Term | Write in script as | Why |
|---|---|---|
| GPU (singular) | `G P U` | Reads as letters, correct |
| GPUs (plural) | `G P Yous` | Plain "G P Us" reads as "G‑P‑us" (the pronoun) |
| NIC / NICs | `Nick` / `Nicks` | Letter-by-letter sounds clinical; the word "Nick" reads naturally |
| FRU / FRUs | `Fru` / `Frus` | Industry pronunciation is "froo" — the all-caps form reads letter-by-letter |
| BIOS | `Bios` | Mixed case reads as the word "BYE-oss"; all-caps risks letter spelling |
| RoCE | `rocky` | The accepted industry pronunciation |
| RoCEv2 | `rocky v two` | Same logic |
| SACK / NACK | `sack` / `knack` | The spec uses them as words |
| SACKs / NACKs | `sacks` / `knacks` | Plural reads cleanly |
| ACK | `ack` | Reads as a word |
| SRv6 | `S R V six` | "S Rv six" gets read as "rev" |
| uSID / uSIDs | `micro S I D` / `micro S I Ds` | The `u` prefix is the Greek µ |
| NVIDIA | `Nvidia` | Brand pronounced as a word |
| OpenAI | `Open A I` | "OpenAI" run together is mispronounced by most voices |
| SONiC | `sonic` | Reads as the word |
| Spectrum-X, ConnectX-8 | `Spectrum-X`, `ConnectX-Eight` | Brand names with hyphens read OK; spell out trailing digits |
| GB200 | `G B two-hundred` | Brand model |
| T0 / T1 / T2 | `tier zero` / `tier one` / `tier two` | "T zero" also works |
| Big years (2026) | `twenty twenty-six` | Avoid digit-by-digit |
| Version numbers (0.5, 1.0, 0.5.0, 2.1, 3.0) | `version zero point five`, `version one point zero`, `version zero point five point zero`, `two point one`, `three point zero` | The decimal point reliably trips ElevenLabs and other TTS engines. **Always spell out every version number phonetically — including multi-segment versions like 0.5.0 (`zero point five point zero`).** |
| ESS / BESS / HESS | `ESS` / `BESS` / `HESS`, or `E S S` if ElevenLabs slurs it | Try normal all-caps first; spell letters with spaces if the voice rushes or blends them. |
| UL 9540 / UL 9540A | `U L ninety-five forty` / `U L ninety-five forty A` | Avoid digit-by-digit or "nine thousand five hundred forty" readings. |
| CSA C800 | `C S A C eight hundred` | Avoid "C eight zero zero" or "see-eight-hundred" ambiguity. |
| NFPA 855 | `N F P A eight fifty-five` | Reads naturally and avoids digit-by-digit drift. |
| AHJ / HMA | `A H J` / `H M A` | Spell out authority and analysis acronyms for clarity. |

When body text mixes singular and plural forms (e.g., one GPU and many GPUs), call it out in the pronunciation hint at the top:

```
# pronunciation: GPUs -> "G P Yous" (singular GPU -> "G P U"); NIC -> "Nick"
```

### Adjacent acronyms run together

When two letter-acronyms appear back-to-back (e.g., `HPM FPGA`, `SCM BMC`), TTS often slurs them — `HPM FPGA` becomes "H-P-M-F-P-G-A" all in one breath, or worse, drops a letter so it sounds like "F P G S". On the *first* occurrence in a script, spell the leading acronym phonetically with explicit spaces so the engine pauses between them:

```
the H P M FPGA specification — the standardized API surface every HPM FPGA exposes…
```

The second and subsequent occurrences read fine as the canonical form because the engine has by then established the pace.

## Examples from the reference course

The OCP NIC 3.0 Academy package has narration .wav files at `audio/module1/` through `audio/module6/`. There are no .txt scripts shipped — but the audio length and slide content give you the model. Open a few in a quick listen if you want a sense of pace.

## TTS-aware writing rules (added 2026)

These rules came out of real ElevenLabs output on the OCP Project Deschutes course. Following them up-front saves a regeneration pass.

### Keep paragraphs under ~80 words

ElevenLabs (and most modern TTS engines) lose vocal energy mid-paragraph on long technical content with dense terminology. Symptom: volume drops ~70–80 seconds into a clip; final sentences fade. Fix: split long paragraphs into two or three shorter ones at natural break points. Each new paragraph gives the model a fresh breath cue and restores projection.

After regenerating a clip that had fade or pronunciation issues, do a quick listen or waveform check of the tail. If the last 15–20 seconds visibly or audibly drop in level, tighten the script further and regenerate only that slide. Dense standards lists, slash-heavy names, long comma chains, and quoted phrases near the end are common fade triggers.

Also check for post-speech artifacts: buzz, chirps, or a short non-silent burst after a quiet gap. If the artifact occurs after narration has clearly finished, trim only that post-speech tail and leave the spoken ending intact. If the artifact overlaps speech, rewrite the final sentence into shorter plain-language phrasing and regenerate.

### Use em-dashes sparingly

Em-dashes (`—`) usually render as a clean pause, but in specific positions they can cause an audible blip or odd syllable. The pattern most at risk: em-dash introducing a clarifying phrase at the end of a script where the model is already low on energy. When in doubt, replace with a colon, period, or comma. Reserve em-dashes for short parenthetical inserts mid-sentence, which TTS handles well.

### Spell acronyms-spoken-as-words phonetically

ElevenLabs defaults to letter-by-letter pronunciation for all-caps acronyms. If the acronym is conventionally pronounced as a word, spell it phonetically in the .txt script (the slide HTML keeps the all-caps form for the reader).

OCP cheat sheet:
- `HAC` → write `Hack` in narration
- `NIC` → write `Nick`
- `DLC` → leave as letters (no common single-word pronunciation)
- `TCS / FWS / PLC / VFD / CDU` → leave as letters (these are read letter-by-letter)

When in doubt, listen to a draft generation and adjust on the next pass.

### Hex-style numbers like IEC 60068 / 60309

Read them as digit-by-digit (`six-zero-zero-six-eight`), not as "sixty thousand sixty-eight". ElevenLabs handles "six-zero-zero-six-eight" unambiguously; the natural-language form is hit-or-miss.

### Version numbers like 1.0

Write as `version one dot zero` in narration. Bare `1.0` is sometimes read "one point zero" and sometimes "one zero" — too variable for a tech course.

# Full-v4 multilingual rebuild - 10 November 2026

## Scope

English and all seven existing translations were rebuilt from repository main
`66b3be167767bcd7e14786c22cf7ef198688e2b9`. English technical teaching and scripts
are unchanged. The translated editions now include the current PG25 lifecycle
guidance, water/PG25 product-specification distinction, community-feedback
safeguards, updated figures, 18-second commissioning animation, PDF page links,
whole-document closing resources, glossary placements, home and player controls,
and formal localized LMS catalog exports.

The separate two-phase course is untouched. Its link on M1S7 remains in place.
SCORM 1.2 and all five existing Home/module identifiers are preserved for every
edition. No SCORM-version or reporting-architecture migration was made. Local
builds are prepared for review. This source PR publishes the editable materials
and validation records; LMS replacement remains a separate later action.

## Narration and translation

All 368 slide recordings, including 32 knowledge-check recordings, were freshly
generated with full ElevenLabs `eleven_v4`, using each edition's existing
approved voice. The English voice profile's name contains “v2”; that is its
profile name, not the model used for synthesis. No fallback model or provider
was used. Provider output was `mp3_44100_96`. Decoded native WAV masters and
synthesis receipts are retained outside the runtime, with script and media
hashes. Pacing uses pitch-preserving `atempo` at the maintained 1.18 factor,
without reference-model synthesis, padding, or trimming. Runtime narration is
96 kbps CBR, mono, 44.1 kHz MP3. The learner dial starts at 1.0 and preserves a
learner's saved preference separately from the authored pacing.

Translations reconcile the current English source with prior approved locale
memory and on-device translation. Protected identifiers, numbers, placeholders,
quiz IDs/correctness, URLs, and supporting PDF page ranges were retained.
Technical editorial checks corrected glycol nomenclature, the initial 1.5-year
lab schedule, cleaning/passivation qualifications, and flushing/bypass animation
labels. A final pass also corrected literal translations of operating envelope,
site action limits and measurement, plus the Traditional Chinese explanation of
nominal versus absolute filter efficiency. Native-language human acceptance and listening approval remain pending;
automated signal checks do not establish either.

## Measured Narration

| Language | M1 Audio | M2 Audio | M3 Audio | M4 Audio | Total Audio | ZIP MiB |
|---|---:|---:|---:|---:|---:|---:|
| English | 6:27 | 8:37 | 7:11 | 8:54 | 31:08 | 23.7 |
| Korean | 6:28 | 8:43 | 7:38 | 9:12 | 32:00 | 24.4 |
| Japanese | 7:41 | 9:56 | 8:48 | 10:34 | 36:59 | 28.1 |
| Simplified Chinese | 5:50 | 7:58 | 6:41 | 8:15 | 28:44 | 22.2 |
| Traditional Chinese | 6:06 | 8:19 | 7:00 | 8:35 | 29:59 | 23.2 |
| Vietnamese | 6:44 | 8:39 | 7:23 | 9:00 | 31:46 | 24.5 |
| Brazilian Portuguese | 7:53 | 10:30 | 8:47 | 10:53 | 38:03 | 28.7 |
| Latin American Spanish | 7:41 | 10:08 | 8:28 | 10:25 | 36:42 | 27.9 |

These are audio runtimes, not learner-time estimates. Existing catalog metadata
is retained at 35 minutes, with module estimates of 7, 10, 9 and 9 minutes.
Japanese, Portuguese and Spanish narration alone now exceeds that total; review
the localized learner-time estimates before LMS publication. Reference study,
interactions, replays and retries add time. No pacing or teaching material was
silently changed to make a language fit the original estimate.

## Validation

- Eight independent ZIPs passed CRC, strict manifest membership, current-byte
  comparison, deflate-compression and SCORM 1.2 checks. Each contains 68 runtime
  files, including 46 MP3 clips, and no WAVs, narration-script TXT files or
  authoring metadata.
- All 368 current clips have matching full-v4 receipts, voice IDs, script hashes,
  master hashes and final MP3 hashes. Provider/native-master hashes were checked.
  Pacing matched its target within 50 ms. MP3 frames confirm 96 kbps CBR, mono,
  44.1 kHz; full decoding retained the paced master duration within tolerance.
- Audio signal/tail reports passed without flags. These are not listening tests.
- Every slide was checked in the generated course pages at 1440, 390 and 320 px.
  All eight editions passed 692 layout, media, glossary and localized-control
  assertions each. Videos were silent, nonblank, 1080p and 18 seconds long;
  enlargement/dismissal and final content reachability were checked.
- After the final terminology corrections, each translated edition's diagrams
  and affected temperature slide were checked again at all three widths against
  the current source hash. Affected narration was regenerated, not relabeled.
- Each edition passed 50 quiz-persistence/retry/review-navigation checks and
  11 additional immediate-MP3-start, learner-speed, narration-preference and
  review-isolation checks. All browser reviews were headless and muted.
- Source, glossary, arrow, catalog and package checks passed for each edition.
  The full tracked translation catalog was reconciled despite sparse checkout;
  this course's seven existing entries required no change. Two unrelated
  pre-existing course-title drifts were deliberately not changed.
- Installed-tool tests: 149 passed. Repository-tool tests: 177 passed. Shared
  slide-control browser regression: 50 passed. No two-phase course files changed.

Shared fixes included in the local source changes localize previously hardcoded
transcript/narration controls and recognize acronyms next to CJK/Hangul text
without matching inside longer Latin identifiers. A regression test protects
learner aids on eligible summary slides; the installed renderer was brought
into line with the repository's existing summary behavior.

## PR Integration Checks

The source branch was rebased onto main `d5cf6d9` before publication. Newer
shared-player localization from the OCP Orientation work is retained. Narration
controls accept both its current label keys and this rebuild's earlier keys;
the off-tooltip and off-body-message meanings are kept separate. Glossary
matching preserves the merged CJK and Korean-particle support while adding
adjacent Hangul acronyms and pronunciation-spelled acronyms without accepting
substrings inside longer Latin identifiers.

Post-integration validation passed: 186 repository unit tests, 60 shared
slide-control browser assertions, 28 browser assertions covering both label
schemas, and source QA for all eight editions. Browser checks remained headless
and muted. These source compatibility changes do not regenerate narration or
alter the already-validated delivery ZIPs and their recorded checksums.

## Remaining Review and Publication

Review narration and language quality before publication. The formal catalog
exports are adjacent to each ZIP and tracked with each language source. The
shared English 800 x 400 course poster is unchanged. This PR publishes the source
changes and this report. A later Docebo localization task should update the LMS;
no LMS edit has been performed.

Issue #83 tracks the seven-language refresh. Issue #84 remains open: M3S8's
approved 1000 CFU/ml water action threshold still comes only from the supplied
unpublished DOCX. Its draft-only source metadata is preserved in every language;
the published PDF is not represented as support for that trigger.

See `v4-rebuild-audit.json` for ZIP checksums, measured durations and validation
counts. Authoring masters and detailed silent QA evidence are retained locally
outside the Git source and LMS ZIPs.

# Validation

The local reviewed course passed 93 slide/viewport cases at widths 1440, 390 and 320, including checks that authored body text and figures actually appear. Final targeted checks cover M2S3 content restoration, M2S7 Marketplace/logo resources and light/dark phone access, and narration pronunciation corrections. All browser/media QA ran muted.

The single-activity browser fixture passed 50 assertions for session lifecycle, navigation, saved bookmarks and quiz attempts, delayed completion, save-error visibility and review isolation. Resume/control suites passed 26 and 81 assertions; synchronized-video controls passed 21 assertions; native/teaching-media checks passed 87 assertions. Worst measured saved state was 588 characters, below the SCORM 1.2 limit.

All 30 approved WAVs passed signal/tail checks and local recognition comparison. Recognition is machine QA rather than perceptual listening approval. The four generated videos were decoded completely and completed muted playthroughs with their narration clocks aligned. Encodes are 1920×1080, contain no audio stream, and match final narration within one frame. Representative encode fidelity exceeded SSIM 0.995 and PSNR 45 dB. Media hashes, exact original-recording hash and logo provenance are retained in `authoring/media-provenance.json`.

The source contribution is rebuilt with current main's shared AcademyWizard and the existing approved narration. The source normalizes the original recording with `playback_mode: recorded` while retaining its `original_video` role, own audio, captions and disabled slide narration. It adopts current shared typography/spacing fixes rather than copying a historical toolchain. A source-rebuild verification record is added after validation.

The refreshed delivery ZIP is strict: one activity, `launch.html` at its entry, all declared runtime members, and no narration scripts or authoring metadata. LMS catalog JSON/Markdown/HTML remain outside it. The original recording remains unchanged. Browser/API simulations and archive verification do not establish acceptance in the actual target LMS; that test remains pending before learner release.

# Validation record

Repository preparation and rebuild: October 14, 2026. Shared renderer and runtime
files are unchanged. The retained figures, teaching videos, and narration scripts
are byte-identical to the delivered course. `course.json` differs only in portable
research-source paths and the worksheet's repository-compatible resource path.

## Checks repeated from the repository source

| Check | Result |
|---|---|
| Slides source QA with `--repo-root` and `--fail-on-flags` | Zero flags; six modules have teaching video, 32 PDF links checked, nine glossary placements checked |
| SVG arrow/geometry check | Pass for four SVG/HTML source files |
| Complete shared course build with retained approved narration | Six module pages, home, manifest, resources, and strict LMS ZIP generated successfully |
| Audio signal QA during build | All 60 tracks pass; zero tail/fade flags |
| Package validation and ZIP integrity | Pass; 112 packaged files, about 139.3 MiB; every declared runtime asset is present |
| Portable teaching-media builder | All six five-position previews render using retained poses and measured timing fallback |
| Portable promotion extraction/composer | All four excerpt sequences and preview frames regenerate from retained course MP4s and actual home screenshot |
| Promotion encode verification | Both complete 900-frame MP4s decode; seven representative comparisons pass SSIM ≥ 0.995 and PSNR ≥ 45 dB |
| Source preservation | Approved course content, scripts, fonts, and teaching media match the delivered files after path normalization |
| Commit hygiene | No generated narration, runtime course HTML, SCORM ZIP, original research download, API key, or machine-specific home path |

From the repository root, reproduce source checks with:

```bash
python skills/academy-wizard/scripts/slides_course_qa.py \
  courses/nvidia-mgx-1-2-rack-and-tray-interfaces/course.json \
  --repo-root . --fail-on-flags
python skills/academy-wizard/scripts/check_svg_arrows.py \
  courses/nvidia-mgx-1-2-rack-and-tray-interfaces
```

See the course README for full build instructions and `promotion/README.md` for
the promotion extraction, preview, and fidelity checks. Generated check outputs
remain ignored. Retained verification JSON files identify the delivered media.

## Prior delivered-course review

Before repository preparation, the delivery review covered all 60 slide positions
at desktop 1440 × 960 and mobile 390 × 844 with no JavaScript errors or horizontal
overflow. Maintained browser tests passed 50 quiz-persistence/navigation assertions,
21 synchronized-video assertions, and 16 loop-video assertions. Mobile lower
content and the second quiz's Submit control remained accessible by scrolling.
Representative native video frames, transition-adjacent frames, source figures,
and posters were visually inspected. All six teaching videos exceeded SSIM 0.995
and PSNR 45 dB in the retained encoded comparisons; all four synchronized clips
match their measured narration within one 30 fps frame.

The promotional videos were played through their full 30 seconds in Chromium
from local files; both reached the end with 900 frames. These results describe
the retained delivery, not an assertion about an external video platform.

## Remaining human and LMS review

Automated waveform checks do not establish pronunciation, pacing, projection, or
teaching tone. Human narration listening remains pending. Technical reviewers
should check the cited specification pages and the documented source ambiguities.
The HPM separation, expanded alignment display, and simultaneous-maxima force
budget are illustrative rather than validated mechanical simulations.

Live target-LMS upload, syllabus navigation, resume, and independent SCO tracking
have not been confirmed by the authoring workflow. Preserve the existing SCORM
1.2 multi-SCO deployment and test those behaviors in the target LMS before
changing its version or organization.

# OCP Academy brand style

The reference course uses a specific palette, type system, and CSS custom-property approach. The template inherits all of this. Don't change it unless the user requests a brand variant.

## Palette

| Token | Hex | Use |
|---|---|---|
| `--ocp-green` | `#8DC63F` | Primary accent. Buttons, highlights, link states. |
| `--ocp-green-dark` | `#6FA030` | Hover state for primary. |
| `--ocp-green-light` | `#A8D86A` | Subtle accents, ambient glows. |
| `--ocp-green-subtle` | `rgba(141,198,63,0.08)` | Tinted backgrounds (cards, chips). |
| `--ocp-gray` | `#5F6062` | Body text on light mode. |
| `--dark` | `#19194D` | Dark-mode background base. |
| `--dark-surface` | `#1e1e5a` | Dark-mode surface. |
| `--dark-card` | `#262673` | Dark-mode card backgrounds. |
| `--gray-200` | `#e5e7eb` | Card borders. |
| `--gray-500` | `#8a8a8c` | Muted text. |

## Motion intro

- The default course/module intro uses an animated diagonal sweep between OCP blue `#343895` and OCP green `#8DC63F`.
- Use the white horizontal OCP Academy SVG lockup (`ocp_academy_white.svg`) on this gradient. The full-color and black logo variants lose contrast against one end of the sweep.
- Intro type is uppercase, white, and wide-tracked for the eyebrow/subtitle. The title may be generated from arbitrary module names, so keep it in a responsive flex column rather than absolute-positioning the title, rule, and subtitle independently.
- The intro is HTML/CSS-native in the SCORM pages. Do not pre-render it as MP4 unless the user explicitly asks for exportable video assets.

## Type

- **Family**: Open Sans (Google Fonts), weights 300–800.
- **Headline**: weight 800, slight letter-spacing (`0.1em`), uppercase in some slide types.
- **Body**: weight 400 at 16px base.
- **Small caps section labels** above slide titles use weight 700, `0.2em` letter-spacing.

## Layout

- Slides are full-viewport `position: absolute` panels with `display: flex; flex-direction: column; justify-content: center;`.
- One slide is active at a time; transitions are managed by a `.active` class plus `.exit-left` for outgoing slides.
- The control bar is fixed at the bottom with three regions (theme toggle, slide nav, audio + fullscreen).
- The progress bar is a 4px bar pinned to the top of the viewport, filled left-to-right by `width: %`.

## Dark mode

Toggled via `[data-theme="dark"]` on `<html>`. Persisted in `localStorage` (key `ocp-deck-theme`). All colors are CSS variables, so switching theme swaps the variable values and every component recolors automatically.

## Animations

- `.animate-in` elements fade in 200ms staggered after `.slide.active` is applied.
- Slide transitions are 600ms ease.
- Don't add bouncy or playful easing — this is a professional reference course.

## Accessibility notes

- Color contrast in dark mode is acceptable but borderline for `--dark-muted` against `--dark-card`. Avoid putting critical info in muted text in dark mode.
- All buttons have `aria-label`.
- Keyboard navigation is wired (arrows, space, Home, End, F, D, P).
- Auto-playing audio respects browser autoplay policies (first slide audio loads after first user interaction).

## OCP green: two hexes

The CSS uses `--ocp-green: #8DC63F` for chrome (buttons, accents, links, hover states). The official iconography (CDU icon, OCP Academy hex emblem) uses `#80bc00` — a slightly more saturated green. They look similar but aren't identical. Do *not* try to normalize them — each is intentional in its context. When generating new figures in the OCP visual style, use `#8DC63F` for accents and let any embedded vector logos keep their native `#80bc00`.

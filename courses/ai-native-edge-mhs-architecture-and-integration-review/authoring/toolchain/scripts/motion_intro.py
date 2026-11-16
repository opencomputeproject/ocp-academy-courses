"""Shared OCP Academy motion-intro helpers for render_index.py and render_module.py."""

from __future__ import annotations
import html
from pathlib import Path
from typing import Any

DEFAULT_LOGO = "ocp_academy_white.svg"
DEFAULT_DURATION_MS = 8000


def esc(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def _cfg(course: dict) -> dict:
    cfg = course.get("motion_intro", {})
    return cfg if isinstance(cfg, dict) else {}


def _scope_cfg(course: dict, scope: str) -> dict:
    cfg = _cfg(course)
    scoped = cfg.get(scope, {})
    return scoped if isinstance(scoped, dict) else {}


def motion_intro_enabled(course: dict, scope: str) -> bool:
    """Default-on overlay. Disable with:
       motion_intro: {enabled:false}, or motion_intro.index.enabled:false,
       or motion_intro.modules.enabled:false.
    """
    raw = course.get("motion_intro", {})
    if raw is False:
        return False
    if isinstance(raw, dict) and raw.get("enabled") is False:
        return False
    scoped_raw = raw.get(scope) if isinstance(raw, dict) else None
    if scoped_raw is False:
        return False
    if isinstance(scoped_raw, dict) and scoped_raw.get("enabled") is False:
        return False
    return True


def motion_intro_logo(course: dict, scope: str | None = None) -> str:
    cfg = _cfg(course)
    scoped = _scope_cfg(course, scope) if scope else {}
    brand = course.get("brand", {}) if isinstance(course.get("brand", {}), dict) else {}
    logo = scoped.get("logo") or cfg.get("logo") or brand.get("motion_intro_logo") or DEFAULT_LOGO
    return str(logo)


def motion_intro_duration(course: dict, scope: str) -> int:
    cfg = _cfg(course)
    scoped = _scope_cfg(course, scope)
    raw = scoped.get("duration_ms", cfg.get("duration_ms", DEFAULT_DURATION_MS))
    try:
        duration = int(raw)
    except (TypeError, ValueError):
        duration = DEFAULT_DURATION_MS
    return max(1200, duration)


def load_motion_intro_css(template_dir: Path) -> str:
    return (template_dir / "motion_intro.css").read_text()


def motion_intro_body_class(course: dict, scope: str) -> str:
    return ' class="has-motion-intro"' if motion_intro_enabled(course, scope) else ""


def render_motion_intro(course: dict, scope: str, module: dict | None = None) -> str:
    if not motion_intro_enabled(course, scope):
        return ""

    scoped = _scope_cfg(course, scope)
    logo = motion_intro_logo(course, scope)
    duration = motion_intro_duration(course, scope)
    ui_labels = course.get("ui_labels") or {}
    intro_label = ui_labels.get("course_intro", "OCP Academy course intro")
    skip_intro = ui_labels.get("skip_intro", "Skip intro")

    if scope == "index":
        eyebrow = scoped.get("eyebrow") or "OCP Academy"
        title = scoped.get("title") or course.get("course_title") or "OCP Academy Course"
        subtitle = scoped.get("subtitle") or course.get("course_subtitle") or course.get("tagline") or "Community-driven Hyperscale Innovation for All"
    else:
        if module is None:
            raise ValueError("module is required for module motion intro")
        module_intro = module.get("motion_intro", {}) if isinstance(module.get("motion_intro", {}), dict) else {}
        eyebrow = module_intro.get("eyebrow") or scoped.get("eyebrow") or module.get("module_badge_text") or f"Module {module.get('id', '')}"
        title = module_intro.get("title") or module.get("title") or f"Module {module.get('id', '')}"
        subtitle = module_intro.get("subtitle") or module.get("subtitle") or course.get("course_subtitle") or ""
        duration = int(module_intro.get("duration_ms") or duration)
        logo = module_intro.get("logo") or logo

    return f'''
<div class="ocp-motion-intro" id="ocpMotionIntro" data-duration-ms="{duration}" role="presentation" aria-label="{esc(intro_label)}">
  <div class="ocp-motion-intro__bg"></div>
  <div class="ocp-motion-intro__grid"></div>
  <div class="ocp-motion-intro__vignette"></div>
  <div class="ocp-motion-intro__lockup">
    <img src="{esc(logo)}" alt="OCP Academy">
  </div>
  <div class="ocp-motion-intro__title-block">
    <div class="ocp-motion-intro__eyebrow">{esc(eyebrow)}</div>
    <div class="ocp-motion-intro__title">{esc(title)}</div>
    <div class="ocp-motion-intro__rule"></div>
    {f'<div class="ocp-motion-intro__subtitle">{esc(subtitle)}</div>' if subtitle else ''}
  </div>
  <div class="ocp-motion-intro__outro"></div>
  <button class="ocp-motion-intro__skip" type="button" id="ocpMotionIntroSkip" aria-label="{esc(skip_intro)}">{esc(skip_intro)}</button>
</div>'''


def motion_intro_script() -> str:
    return r'''
<script>
(function() {
  'use strict';
  var intro = document.getElementById('ocpMotionIntro');
  if (!intro) return;
  var skip = document.getElementById('ocpMotionIntroSkip');
  var done = false;
  var reduceMotion = false;
  try { reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (_) {}
  var duration = parseInt(intro.getAttribute('data-duration-ms') || '8000', 10);
  if (!isFinite(duration) || duration < 1200) duration = 8000;
  if (reduceMotion) duration = 900;

  function finishIntro(event) {
    if (event && event.stopPropagation) event.stopPropagation();
    if (done) return;
    done = true;
    intro.classList.add('is-done');
    intro.setAttribute('aria-hidden', 'true');
    document.body.classList.add('motion-intro-done');
    window.setTimeout(function() {
      if (intro && intro.parentNode) intro.parentNode.removeChild(intro);
    }, 750);
  }

  if (skip) {
    skip.addEventListener('click', finishIntro);
  }
  window.setTimeout(finishIntro, duration);
})();
</script>'''


def motion_intro_noscript_style() -> str:
    return '''<noscript><style>
.ocp-motion-intro{display:none!important;}
body.has-motion-intro .index-shell,
body.has-motion-intro .module-badge,
body.has-motion-intro .deck,
body.has-motion-intro .controls,
body.has-motion-intro .progress-bar{opacity:1!important;transform:none!important;}
</style></noscript>'''

#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <course-folder-or-nested-path>" >&2
  exit 2
fi

COURSE_NAME="$1"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/courses/$COURSE_NAME"
BUILD_ROOT="${BUILD_ROOT:-$ROOT_DIR/build}"
BUILD_DIR="${BUILD_DIR:-$BUILD_ROOT/$COURSE_NAME}"
DEFAULT_SKILL_DIR="$ROOT_DIR/skills/academy-wizard"
if [[ ! -d "$DEFAULT_SKILL_DIR" && -d "$HOME/.codex/skills/academy-wizard" ]]; then
  DEFAULT_SKILL_DIR="$HOME/.codex/skills/academy-wizard"
fi
SKILL_DIR="${ACADEMY_WIZARD_SKILL_DIR:-$DEFAULT_SKILL_DIR}"
PYTHON_BIN="${PYTHON:-python3}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Course source folder not found: $SOURCE_DIR" >&2
  exit 1
fi

if [[ ! -f "$SOURCE_DIR/course.json" ]]; then
  echo "Course definition not found: $SOURCE_DIR/course.json" >&2
  exit 1
fi

COURSE_STYLE="$($PYTHON_BIN - "$SOURCE_DIR/course.json" <<'PY'
import json
import sys
from pathlib import Path

course = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
style = str(course.get("style") or "Slides").strip().casefold()
if style not in {"slides", "scrolling"}:
    raise SystemExit(f"Unsupported course style: {course.get('style')!r}")
print(style)
PY
)"

# A course may pin its validated toolchain to preserve its published runtime.
# An explicit caller override still takes precedence.
if [[ -z "${ACADEMY_WIZARD_SKILL_DIR:-}" ]]; then
  COURSE_TOOLCHAIN="$("$PYTHON_BIN" - "$SOURCE_DIR/course.json" <<'PY'
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
value = json.loads(source.read_text(encoding="utf-8")).get("authoring_toolchain")
if value is not None:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise SystemExit("authoring_toolchain must be a course-relative directory")
    target = (source.parent / value).resolve()
    try:
        target.relative_to(source.parent)
    except ValueError:
        raise SystemExit("authoring_toolchain must stay within the course source folder")
    if not target.is_dir():
        raise SystemExit(f"Course toolchain not found: {target}")
    print(target)
PY
)"
  if [[ -n "$COURSE_TOOLCHAIN" ]]; then
    SKILL_DIR="$COURSE_TOOLCHAIN"
  fi
fi

COMMON_SCRIPTS=(new_course.py render_scrolling.py render_index.py validate_package.py course_delivery_summary.py zip_for_lms.py)
SLIDES_SCRIPTS=(gen_audio.py audio_tail_report.py render_module.py)
REQUIRED_SCRIPTS=("${COMMON_SCRIPTS[@]}")
if [[ "$COURSE_STYLE" == "slides" ]]; then
  REQUIRED_SCRIPTS+=("${SLIDES_SCRIPTS[@]}")
fi

for script in "${REQUIRED_SCRIPTS[@]}"; do
  if [[ ! -f "$SKILL_DIR/scripts/$script" ]]; then
    echo "AcademyWizard script missing: $SKILL_DIR/scripts/$script" >&2
    echo "Set ACADEMY_WIZARD_SKILL_DIR to your academy-wizard skill folder." >&2
    exit 1
  fi
done

# Formal LMS copy belongs to editable source, separately from the course README.
# Validate before staging media or making paid narration requests.
"$PYTHON_BIN" "$SKILL_DIR/scripts/course_delivery_summary.py" "$SOURCE_DIR/course.json" --write
"$PYTHON_BIN" "$SKILL_DIR/scripts/course_delivery_summary.py" "$SOURCE_DIR/course.json" --check

mkdir -p "$BUILD_DIR"

"$PYTHON_BIN" "$SKILL_DIR/scripts/new_course.py" "$BUILD_DIR" "$SOURCE_DIR/course.json"
if [[ "$COURSE_STYLE" == "scrolling" ]]; then
  # A Scrolling locale is a lightweight overlay: retain canonical binary
  # resources, then replace only localized assets such as translated videos,
  # captions, or images. This avoids checking the same large media into Git
  # once per language while still producing a self-contained SCORM package.
  if [[ "$SOURCE_DIR" == */locales/* ]]; then
    CANONICAL_SOURCE_DIR="${SOURCE_DIR%%/locales/*}"
    if [[ -d "$CANONICAL_SOURCE_DIR/resources" ]]; then
      rsync -a "$CANONICAL_SOURCE_DIR/resources/" "$BUILD_DIR/resources/"
    fi
  fi
  if [[ -d "$SOURCE_DIR/resources" ]]; then
    rsync -a "$SOURCE_DIR/resources/" "$BUILD_DIR/resources/"
  fi
  "$PYTHON_BIN" "$SKILL_DIR/scripts/render_index.py" "$BUILD_DIR/course.json"
  "$PYTHON_BIN" "$SKILL_DIR/scripts/validate_package.py" "$BUILD_DIR"
else
  if [[ -d "$SOURCE_DIR/audio" ]]; then
    rsync -a --include='*/' --include='*.txt' --exclude='*' "$SOURCE_DIR/audio/" "$BUILD_DIR/audio/"
  fi
  if [[ -d "$SOURCE_DIR/figures" ]]; then
    rsync -a "$SOURCE_DIR/figures/" "$BUILD_DIR/figures/"
  fi
  if [[ -d "$SOURCE_DIR/resources" ]]; then
    rsync -a "$SOURCE_DIR/resources/" "$BUILD_DIR/resources/"
  fi

  for asset_folder in fonts captions; do
    if [[ -d "$SOURCE_DIR/$asset_folder" ]]; then
      rsync -a "$SOURCE_DIR/$asset_folder/" "$BUILD_DIR/$asset_folder/"
    fi
  done

  if [[ -n "${EXISTING_AUDIO_DIR:-}" ]]; then
    rsync -a "$EXISTING_AUDIO_DIR/" "$BUILD_DIR/audio/"
  elif [[ "${SKIP_AUDIO:-0}" != "1" ]]; then
    if [[ "${FORCE_AUDIO:-0}" == "1" ]]; then
      "$PYTHON_BIN" "$SKILL_DIR/scripts/gen_audio.py" "$BUILD_DIR/course.json" --force
    else
      "$PYTHON_BIN" "$SKILL_DIR/scripts/gen_audio.py" "$BUILD_DIR/course.json"
    fi
  fi

  # Optional trusted course source generates offline learner resources directly
  # into the staged package; rendered resource HTML is not kept in source control.
  if [[ -f "$SOURCE_DIR/scripts/build_resources.py" ]]; then
    "$PYTHON_BIN" "$SOURCE_DIR/scripts/build_resources.py" "$BUILD_DIR/course.json"
  fi

  COURSE_RENDERER="$($PYTHON_BIN - "$SOURCE_DIR/course.json" <<'PY'
import json
import sys
print(json.load(open(sys.argv[1])).get("authoring_renderer") or "")
PY
)"
  if [[ -n "$COURSE_RENDERER" ]]; then
    # Course-owned renderers are trusted editable source, like build_resources.py.
    # Keep the renderer with the staged source so later review edits reproduce it.
    if [[ "$COURSE_RENDERER" != "$(basename "$COURSE_RENDERER")" || "$COURSE_RENDERER" != *.py || ! -f "$SOURCE_DIR/$COURSE_RENDERER" ]]; then
      echo "authoring_renderer must name an existing Python file in the course folder." >&2
      exit 1
    fi
    cp "$SOURCE_DIR/$COURSE_RENDERER" "$BUILD_DIR/$COURSE_RENDERER"
    ACADEMY_WIZARD_SKILL_DIR="$SKILL_DIR" "$PYTHON_BIN" "$BUILD_DIR/$COURSE_RENDERER" "$BUILD_DIR/course.json" --all
  else
    "$PYTHON_BIN" "$SKILL_DIR/scripts/render_module.py" "$BUILD_DIR/course.json" --all
  fi
  "$PYTHON_BIN" "$SKILL_DIR/scripts/render_index.py" "$BUILD_DIR/course.json"

  if [[ "${SKIP_AUDIO:-0}" == "1" && -z "${EXISTING_AUDIO_DIR:-}" ]]; then
    echo "Rendered without audio validation because SKIP_AUDIO=1 and EXISTING_AUDIO_DIR is unset."
    echo "Build folder: $BUILD_DIR"
    exit 0
  fi

  "$PYTHON_BIN" "$SKILL_DIR/scripts/audio_tail_report.py" "$BUILD_DIR/course.json" --fail-on-flags
  "$PYTHON_BIN" "$SKILL_DIR/scripts/validate_package.py" "$BUILD_DIR"
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/zip_for_lms.py" "$BUILD_DIR" --course-json "$SOURCE_DIR/course.json"

echo
echo "Build complete:"
echo "  Folder: $BUILD_DIR"
echo "  Zip:    $BUILD_DIR.zip"
echo "  LMS:    $BUILD_DIR.lms-catalog.{json,md,html}"

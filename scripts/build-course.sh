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

COMMON_SCRIPTS=(new_course.py render_scrolling.py render_index.py validate_package.py zip_for_lms.py)
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

mkdir -p "$BUILD_DIR"

"$PYTHON_BIN" "$SKILL_DIR/scripts/new_course.py" "$BUILD_DIR" "$SOURCE_DIR/course.json"
if [[ "$COURSE_STYLE" == "scrolling" ]]; then
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

  if [[ -n "${EXISTING_AUDIO_DIR:-}" ]]; then
    rsync -a "$EXISTING_AUDIO_DIR/" "$BUILD_DIR/audio/"
  elif [[ "${SKIP_AUDIO:-0}" != "1" ]]; then
    if [[ "${FORCE_AUDIO:-0}" == "1" ]]; then
      "$PYTHON_BIN" "$SKILL_DIR/scripts/gen_audio.py" "$BUILD_DIR/course.json" --force
    else
      "$PYTHON_BIN" "$SKILL_DIR/scripts/gen_audio.py" "$BUILD_DIR/course.json"
    fi
  fi

  "$PYTHON_BIN" "$SKILL_DIR/scripts/render_module.py" "$BUILD_DIR/course.json" --all
  "$PYTHON_BIN" "$SKILL_DIR/scripts/render_index.py" "$BUILD_DIR/course.json"

  if [[ "${SKIP_AUDIO:-0}" == "1" && -z "${EXISTING_AUDIO_DIR:-}" ]]; then
    echo "Rendered without audio validation because SKIP_AUDIO=1 and EXISTING_AUDIO_DIR is unset."
    echo "Build folder: $BUILD_DIR"
    exit 0
  fi

  "$PYTHON_BIN" "$SKILL_DIR/scripts/audio_tail_report.py" "$BUILD_DIR/course.json" --fail-on-flags
  "$PYTHON_BIN" "$SKILL_DIR/scripts/validate_package.py" "$BUILD_DIR"
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/zip_for_lms.py" "$BUILD_DIR"

echo
echo "Build complete:"
echo "  Folder: $BUILD_DIR"
echo "  Zip:    $BUILD_ROOT/$COURSE_NAME.zip"

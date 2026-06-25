#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <course-folder-name>" >&2
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

for script in new_course.py gen_audio.py audio_tail_report.py render_module.py render_index.py validate_package.py zip_for_lms.py; do
  if [[ ! -f "$SKILL_DIR/scripts/$script" ]]; then
    echo "AcademyWizard script missing: $SKILL_DIR/scripts/$script" >&2
    echo "Set ACADEMY_WIZARD_SKILL_DIR to your academy-wizard skill folder." >&2
    exit 1
  fi
done

mkdir -p "$BUILD_DIR"

"$PYTHON_BIN" "$SKILL_DIR/scripts/new_course.py" "$BUILD_DIR" "$SOURCE_DIR/course.json"
rsync -a --include='*/' --include='*.txt' --exclude='*' "$SOURCE_DIR/audio/" "$BUILD_DIR/audio/"
if [[ -d "$SOURCE_DIR/figures" ]]; then
  rsync -a "$SOURCE_DIR/figures/" "$BUILD_DIR/figures/"
fi

if [[ -n "${EXISTING_AUDIO_DIR:-}" ]]; then
  rsync -a "$EXISTING_AUDIO_DIR/" "$BUILD_DIR/audio/"
elif [[ "${SKIP_AUDIO:-0}" != "1" ]]; then
  AUDIO_ARGS=()
  if [[ "${FORCE_AUDIO:-0}" == "1" ]]; then
    AUDIO_ARGS+=(--force)
  fi
  "$PYTHON_BIN" "$SKILL_DIR/scripts/gen_audio.py" "$BUILD_DIR/course.json" "${AUDIO_ARGS[@]}"
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/render_module.py" "$BUILD_DIR/course.json" --all
"$PYTHON_BIN" "$SKILL_DIR/scripts/render_index.py" "$BUILD_DIR/course.json"

if [[ "${SKIP_AUDIO:-0}" == "1" && -z "${EXISTING_AUDIO_DIR:-}" ]]; then
  echo "Rendered without audio validation because SKIP_AUDIO=1 and EXISTING_AUDIO_DIR is unset."
  echo "Build folder: $BUILD_DIR"
  exit 0
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/audio_tail_report.py" "$BUILD_DIR/course.json"
"$PYTHON_BIN" "$SKILL_DIR/scripts/validate_package.py" "$BUILD_DIR"
"$PYTHON_BIN" "$SKILL_DIR/scripts/zip_for_lms.py" "$BUILD_DIR"

echo
echo "Build complete:"
echo "  Folder: $BUILD_DIR"
echo "  Zip:    $BUILD_ROOT/$COURSE_NAME.zip"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/skills/academy-wizard"
CODEX_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET_DIR="$CODEX_DIR/skills/academy-wizard"
FORCE=0

if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--force]" >&2
  exit 2
fi

if [[ ! -f "$SOURCE_DIR/SKILL.md" ]]; then
  echo "Bundled AcademyWizard skill not found at $SOURCE_DIR" >&2
  exit 1
fi

if [[ -e "$TARGET_DIR" && "$FORCE" != "1" ]]; then
  echo "Target already exists: $TARGET_DIR" >&2
  echo "Run with --force to replace it." >&2
  exit 1
fi

mkdir -p "$CODEX_DIR/skills"
if [[ "$FORCE" == "1" ]]; then
  rm -rf "$TARGET_DIR"
fi

rsync -a --delete \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  "$SOURCE_DIR/" \
  "$TARGET_DIR/"

echo "Installed AcademyWizard skill to:"
echo "  $TARGET_DIR"
echo
echo "Restart Codex or start a new Codex session so the skill list refreshes."

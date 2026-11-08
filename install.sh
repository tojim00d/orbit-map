#!/usr/bin/env bash
# Orbit Map installer.
#
#   ./install.sh                    install as a Claude Code plugin from this folder
#   ./install.sh --skills-dir DIR   copy the two skills into any agent's skills directory
#   ./install.sh --help
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$DIR/plugins/orbit-map/skills"
SKILLS_DIR=""

usage() {
  cat <<'EOF'
Orbit Map — project map & diagram skills for Claude Code.

Usage:
  ./install.sh                    Install as a Claude Code plugin from this folder.
  ./install.sh --skills-dir DIR   Copy the two skills into any agent's skills directory.
  ./install.sh --help             Show this help.

Skills: project-map (interactive one-file HTML map), project-diagram (static SVG/PNG).
Part of the Orbit pack: https://github.com/tojim00d/Orbit-skills
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --skills-dir)
      [ $# -ge 2 ] || { echo "error: --skills-dir needs a value" >&2; exit 1; }
      SKILLS_DIR="$2"; shift 2 ;;
    --skills-dir=*)
      SKILLS_DIR="${1#*=}"; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "error: unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

[ -d "$SKILLS_SRC" ] || { echo "error: skills not found: $SKILLS_SRC" >&2; exit 1; }

if [ -n "$SKILLS_DIR" ]; then
  mkdir -p "$SKILLS_DIR"
  copied=0; skipped=0
  for skill in "$SKILLS_SRC"/*/; do
    name="$(basename "$skill")"
    if [ -e "$SKILLS_DIR/$name" ]; then skipped=$((skipped + 1)); continue; fi
    cp -R "$skill" "$SKILLS_DIR/$name"; copied=$((copied + 1))
  done
  echo "Orbit Map: copied $copied skills to $SKILLS_DIR (skipped $skipped existing)."
  echo "Next: read AGENTS.md and describe the task in words."
  exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "error: the 'claude' CLI is not on PATH." >&2
  echo "Install Claude Code, or use: ./install.sh --skills-dir <dir> for another agent." >&2
  exit 1
fi

claude plugin marketplace add "$DIR"
claude plugin install orbit-map@orbit-map
echo "Done. Restart Claude Code and ask for a project map or diagram."
echo "Готово. Перезапусти Claude Code и попроси карту проекта или диаграмму."

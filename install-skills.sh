#!/usr/bin/env bash
# Install skills from this repo into ~/.hermes/skills/
# Usage: ./install-skills.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${HERMES_HOME:-$HOME/.hermes}/skills"

echo "Installing skills from $REPO_DIR/skills to $TARGET_DIR ..."

mkdir -p "$TARGET_DIR"

# If a RESOLVER.md already exists, back it up before rsync can overwrite it.
if [[ -f "$TARGET_DIR/RESOLVER.md" ]]; then
  BACKUP="$TARGET_DIR/RESOLVER.md.bak.$(date +%Y%m%d%H%M%S)"
  echo "Backing up existing $TARGET_DIR/RESOLVER.md to $BACKUP ..."
  cp "$TARGET_DIR/RESOLVER.md" "$BACKUP"
fi

# Copy category folders, preserving structure (do NOT delete existing user skills)
rsync -av "$REPO_DIR/skills/" "$TARGET_DIR/"

if [[ -f "$TARGET_DIR/RESOLVER.md" && -f "$TARGET_DIR/RESOLVER.md.bak."* ]]; then
  echo ""
  echo "NOTE: RESOLVER.md was replaced. If you had custom routing, merge the backup into the new file."
fi

echo "Done. Installed skills:"
find "$TARGET_DIR" -name 'SKILL.md' | sed "s|$TARGET_DIR/||" | sed 's|/SKILL.md||' | sort

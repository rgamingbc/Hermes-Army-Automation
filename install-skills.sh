#!/usr/bin/env bash
# Install skills from this repo into ~/.hermes/skills/
# Usage: ./install-skills.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${HERMES_HOME:-$HOME/.hermes}/skills"

echo "Installing skills from $REPO_DIR/skills to $TARGET_DIR ..."

mkdir -p "$TARGET_DIR"

# Copy category folders, preserving structure (do NOT delete existing user skills)
rsync -av "$REPO_DIR/skills/" "$TARGET_DIR/"

echo "Done. Installed skills:"
find "$TARGET_DIR" -name 'SKILL.md' | sed "s|$TARGET_DIR/||" | sed 's|/SKILL.md||' | sort

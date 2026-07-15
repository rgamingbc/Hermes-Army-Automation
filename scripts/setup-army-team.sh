#!/usr/bin/env bash
set -euo pipefail

# Army team one-shot setup script.
# Run this after cloning Hermes-Army-Automation.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR_DIR="$REPO_DIR/vendor/hermes-agent-setup"
HOME_DIR="${HOME_DIR:-$HOME}"
HERMES_HOME="${HERMES_HOME:-$HOME_DIR/.hermes}"
PROFILES_DIR="$HERMES_HOME/profiles"
SKILLS_DIR="$HERMES_HOME/skills"
CUSTOM_SKILLS_DIR="$SKILLS_DIR/custom"
HERMES_BIN="${HERMES_BIN:-$HOME_DIR/.local/bin/hermes}"

# Preflight checks
echo "== Preflight checks =="
missing=()

if ! command -v git >/dev/null 2>&1; then
  missing+=("git")
fi

if ! command -v rsync >/dev/null 2>&1; then
  missing+=("rsync")
fi

if [[ ! -x "$HERMES_BIN" ]]; then
  if command -v hermes >/dev/null 2>&1; then
    HERMES_BIN="$(command -v hermes)"
    echo "  Found hermes on PATH: $HERMES_BIN"
  else
    missing+=("hermes (expected at $HERMES_BIN or on PATH)")
  fi
fi

if [[ ${#missing[@]} -gt 0 ]]; then
  echo "Error: missing required tools:"
  for item in "${missing[@]}"; do
    echo "  - $item"
  done
  exit 1
fi

if [[ ! -d "$VENDOR_DIR" ]]; then
  echo "Error: vendor/hermes-agent-setup not found."
  echo "Run: git subtree add --prefix=vendor/hermes-agent-setup https://github.com/rgamingbc/Hermes-Agent-Setup.git main --squash"
  exit 1
fi

echo "  All checks passed."
echo ""

# Main setup
echo "== Hermes Army Team Setup =="
echo "Repo: $REPO_DIR"
echo "Hermes home: $HERMES_HOME"
echo "Hermes binary: $HERMES_BIN"
echo ""

# 1. Install generic skills from vendor
echo "[1/5] Installing generic Hermes skills..."
bash "$VENDOR_DIR/install-skills.sh"

# 2. Copy army-specific skill
echo "[2/5] Installing army-ceo-delegate skill..."
mkdir -p "$CUSTOM_SKILLS_DIR"
rsync -av "$REPO_DIR/skills/custom/army-ceo-delegate/" "$CUSTOM_SKILLS_DIR/army-ceo-delegate/"

# 3. Create profiles and copy templates
echo "[3/5] Creating army profiles..."
for profile in army-hq army-marketing-head army-dev-head army-research-head; do
  profile_dir="$PROFILES_DIR/$profile"
  mkdir -p "$profile_dir"

  if [[ ! -f "$profile_dir/config.yaml" ]]; then
    cp "$REPO_DIR/templates/army-profiles/$profile/config.yaml" "$profile_dir/config.yaml"
  else
    echo "  $profile/config.yaml already exists, skipping copy."
  fi

  if [[ ! -f "$profile_dir/.env" ]]; then
    cp "$REPO_DIR/templates/army-profiles/$profile/.env" "$profile_dir/.env"
  else
    echo "  $profile/.env already exists, skipping copy."
  fi

  # Replace hard-coded /Users/chloe paths with current user's home
  sed -i.bak "s|/Users/chloe/.hermes/skills/custom|$HOME_DIR/.hermes/skills/custom|g" "$profile_dir/config.yaml"
  rm -f "$profile_dir/config.yaml.bak"
done

# 4. Create shared kanban board
echo "[4/5] Creating army kanban board..."
if ! "$HERMES_BIN" kanban boards create army \
  --name "Army Team" \
  --description "Cross-department army team board" \
  --icon 🎖️ \
  --switch \
  --default-workdir "$HOME_DIR/hermes-army/launch-2026" 2>/tmp/hermes-kanban-stderr.log; then
  # Board may already exist; show warning but do not fail
  if grep -q "already exists\|duplicate" /tmp/hermes-kanban-stderr.log 2>/dev/null; then
    echo "  Board 'army' already exists, continuing."
  else
    echo "  Warning: failed to create kanban board. See /tmp/hermes-kanban-stderr.log"
  fi
fi

# 5. Optional placeholder replacement from env vars
echo "[5/5] Replacing placeholders from environment (if set)..."
replace_count=0
for profile in army-hq army-marketing-head army-dev-head army-research-head; do
  profile_dir="$PROFILES_DIR/$profile"

  # Per-profile tokens take precedence; fall back to generic env vars
  profile_upper="$(echo "$profile" | tr '[:lower:]-' '[:upper:]_')"
  token_var="${profile_upper}_TELEGRAM_BOT_TOKEN"
  token_value="${!token_var:-${TELEGRAM_BOT_TOKEN:-}}"

  if [[ -n "${KIMI_API_KEY:-}" ]]; then
    sed -i.bak "s|__KIMI_API_KEY__|$KIMI_API_KEY|g" "$profile_dir/config.yaml" "$profile_dir/.env" 2>/dev/null || true
    rm -f "$profile_dir/config.yaml.bak" "$profile_dir/.env.bak"
    replace_count=$((replace_count + 1))
  fi

  if [[ -n "$token_value" ]]; then
    sed -i.bak "s|__TELEGRAM_BOT_TOKEN__|$token_value|g" "$profile_dir/.env" 2>/dev/null || true
    rm -f "$profile_dir/.env.bak"
  fi

  if [[ -n "${TELEGRAM_ALLOWED_USERS:-}" ]]; then
    sed -i.bak "s|__YOUR_TELEGRAM_USER_ID__|$TELEGRAM_ALLOWED_USERS|g" "$profile_dir/.env" 2>/dev/null || true
    rm -f "$profile_dir/.env.bak"
  fi
done

if [[ "$replace_count" -gt 0 ]]; then
  echo "  Replaced placeholders using environment variables."
else
  echo "  No env vars set; placeholders left for manual editing."
fi

echo ""
echo "== Setup complete =="
echo ""
echo "Next steps:"
echo "  1. Review each profile's .env and fill in API keys / tokens:"
echo "       $PROFILES_DIR/{army-hq,army-marketing-head,army-dev-head,army-research-head}/.env"
echo "  2. Review each profile's config.yaml, especially auxiliary.vision.api_key."
echo "  3. Verify with:"
echo "       $HERMES_BIN --profile army-hq skills list | grep army-ceo-delegate"
echo "       $HERMES_BIN --profile army-hq kanban show"
echo ""
echo "Optional choices (see README.md for details and risks):"
echo "  - Enable HERMES_YOLO_MODE=1 for non-interactive automation"
echo "  - Enable HERMES_EXEC_ASK=false for messaging gateway automation"
echo ""
echo "To update generic setup later:"
echo "  git subtree pull --prefix=vendor/hermes-agent-setup https://github.com/rgamingbc/Hermes-Agent-Setup.git main --squash"

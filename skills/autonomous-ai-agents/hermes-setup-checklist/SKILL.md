---
name: hermes-setup-checklist
description: |
  Generic onboarding checklist for a new Hermes Agent profile or team. Ensures
  model, vision, delegation, kanban, shared skills, Obsidian vault, and Telegram
  gateway are configured before real work begins.
version: 1.0.0
platforms: [linux, macos, windows]
triggers:
  - setup checklist
  - hermes setup
  - onboard profile
  - new profile
  - team setup
metadata:
  hermes:
    tags: [setup, onboarding, checklist, profile, team]
---

# Hermes Setup Checklist

Use this skill whenever you create a new Hermes profile or onboard a new team member. Work through the checklist in order and report anything that is missing.

## 1. Model and provider

In `~/.hermes/profiles/<profile>/config.yaml`:

```yaml
model:
  default: kimi-k2.7-code          # or your preferred model
  provider: kimi-coding
  base_url: https://api.kimi.com/coding/v1
  supports_vision: true
```

Also update `auxiliary.vision.model` if you use a separate vision model.

## 2. API key

In `~/.hermes/profiles/<profile>/.env`:

```bash
KIMI_API_KEY=sk-...
# or the provider-specific variable required by your config
```

## 3. Approvals and guardrails (for trusted local work)

```yaml
approvals:
  destructive_slash_confirm: false
  command: auto
  write: auto
```

Adjust stricter values if the profile runs untrusted code.

## 4. Delegation (for team leads / CEOs)

```yaml
delegation:
  max_concurrent_children: 3
  max_spawn_depth: 2
  orchestrator_enabled: true
  max_iterations: 30
```

## 5. Kanban board

Enable the kanban toolset:

```yaml
toolsets:
  - kanban
```

Pin the profile to the shared board in `.env`:

```bash
HERMES_KANBAN_BOARD=army
```

## 6. Shared custom skills

Add an external skills directory so the profile can load team skills without copying files:

```yaml
skills:
  external_dirs:
    - /Users/chloe/.hermes/skills/custom
```

## 7. Optional global skills to install

Install useful optional skills into every profile:

```bash
hermes skills repair-official duckduckgo-search --restore --yes
hermes skills repair-official scrapling --restore --yes
hermes skills repair-official watchers --restore --yes
hermes skills repair-official subagent-driven-development --restore --yes
```

## 8. Obsidian vault

Set the vault path in `.env`:

```bash
OBSIDIAN_VAULT_PATH="/Users/$USER/Documents/Hermes Vault"
```

Create the standard vault layout:

```
Hermes Vault/
├── Daily/
├── System/Assistant/logs/
├── Work/Projects/
├── Personal/Projects/
├── People/
└── Inbox/
```

## 9. Telegram gateway (optional)

If this profile needs a Telegram bot:

```bash
TELEGRAM_BOT_TOKEN=...
TELEGRAM_ALLOWED_USERS=...
```

Then restart the gateway. Remember: one bot token = one live consumer.

## 10. Verify

```bash
hermes --version
hermes --profile <profile> config show
hermes --profile <profile> skills list
hermes --profile <profile> kanban show
```

Fix any errors before handing real work to the profile.

## Pitfalls

- Forgetting `supports_vision: true` when using a vision-capable Kimi model.
- Reusing the same Telegram bot token for two gateways.
- Copying skills manually instead of using `external_dirs` — harder to keep in sync.
- Letting the built-in memory fill up before setting up the Obsidian vault.

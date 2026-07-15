---
name: hermes-startup-handover
description: |-
  Global startup routine — automatically run at the beginning of every working session.
  Reads project handover, project index, repo onboarding, and ecosystem tools tracker
  to prevent overnight session memory loss.
triggers:
  - session_start
  - startup
  - handover
  - daily standup
  - resume project
  - continue work
  - morning
  - 開始
  - 開工
  - 繼續
---

# Hermes Startup Handover

This is a **global** skill. **Run automatically at the start of every working session** before doing anything else. Do not wait for the user to say "start", "開工", or "繼續". The user expects this to happen proactively after an overnight session reset.

## When to run

- Every new conversation/session that is not explicitly a fresh start.
- At the start of the day if the previous session has been cleared.
- If the user says "start", "continue", "開工", "繼續", or similar.

If the user explicitly says "start fresh", "new project", or "ignore previous work", skip this skill.

## User expectation (learned from correction)

The user expects Hermes to resume context automatically after the session resets. They should not have to ask for the handover; it is the first thing Hermes does. When the user says something like "比多次皇冠 ACC PW 我" after a reset, it means a required secret was not durably preserved. The startup routine must surface the credential gap immediately so the user can re-supply it before any work is wasted.

## 1. Identify the active project

Look for any of these signals:
- Project name mentioned by the user in the current or previous session.
- File paths mentioned by the user (e.g., vault project folders, repo paths).
- Repo names mentioned by the user.
- Previous session memory mentions a known project.

If no project is identified, ask the user: "老公，你想我繼續邊個 project？"

## 2. Read the Ecosystem Tools Tracker (with PATH fix)

Read the canonical tracker from the Obsidian vault:
- `~/Documents/Hermes Vault/Work/Projects/Hermes Agent Setup/Ecosystem Tools Tracker.md`

If it does not exist, create it using the `hermes-setup-checklist` skill template.

Before running the health checks, source `~/.hermes/.env` so that tools installed outside the system PATH (e.g., `gbrain`, `bun`) are discoverable:

```bash
set -a && source ~/.hermes/.env && set -a
```

If `~/.hermes/.env` does not include `~/.bun/bin`, append it during the setup phase and warn the user to run the setup checklist.

Verify the critical tools are still healthy:
- Hermes WebUI: `curl -s http://127.0.0.1:8789/health`
- agentic-stack: `python3 ~/.hermes/.agent/tools/show.py`
- gbrain PATH: `grep -n "^PATH=" ~/.hermes/.env` — must include `$HOME/.bun/bin`
- gbrain: `gbrain doctor --json` (if command not found, fall back to `export PATH="$HOME/.bun/bin:$PATH" && gbrain doctor --json`)
- repomix: `~/.hermes/bin/repomix --version`
- Vision: `grep -n "auxiliary.vision" ~/.hermes/config.yaml`

If any tool status has changed, note it for the shutdown update.

## 3. Read the project handover and the secrets index

Use `read_file` to read the project's handover file. Common locations:
- `~/Documents/Hermes Vault/Work/Projects/<Project Name> Hermes Handover.md`
- `~/Documents/Hermes Vault/Work/Projects/<project-folder>/README.md`

Also read the secrets index:
- `~/Documents/Hermes Vault/System/Assistant/secrets-index.md`

If the handover references a stored credential (e.g., `CROWN_M473_*`), verify that the variable exists in `~/.hermes/.env`. If it is missing, tell the user immediately: "老公，舊站 creds 搵唔到，要你再俾一次。"

If the handover file does not exist, create it using the `hermes-shutdown-handover` skill template and inform the user.

## 4. Read the project index (if it exists)

Look for an `index.md` or `README.md` in the project vault folder:
- `~/Documents/Hermes Vault/Work/Projects/<Project Name> Index.md`
- `~/Documents/Hermes Vault/Work/Projects/<project-folder>/index.md`

This gives the full map of where the latest report, skill, handover, and archive live.

## 5. Read the latest repo report

If the project uses a git repo, read the latest report mentioned in the handover or index. Reports are usually under `docs/` or `reports/` in the project repo.

## 6. Summarize back to the user

In 2–3 sentences, tell the user:
- Which project you are resuming
- What was last completed
- What is currently pending
- Any known blockers (e.g., missing credentials, waiting for third party)
- Any ecosystem tool status changes detected

Use the user's preferred language (Cantonese for this user). Do not dump the full handover; summarize it.

## 7. Propose next action

Based on the pending items, propose a sensible next step. For example:

> 老公，我哋上次完成咗 X，報告已放喺 vault。下一步可以繼續 Y，你話事。

## Pitfalls

- Do NOT wait for the user to trigger this skill explicitly.
- Do NOT assume the user wants to start a new project unless they say so.
- Do NOT skip reading the handover because the user greeted you casually.
- If the handover says "每日開始時先讀呢份 handover", it is mandatory — do not ignore.
- Do NOT skip the Ecosystem Tools Tracker check; it is how we remember what is installed.

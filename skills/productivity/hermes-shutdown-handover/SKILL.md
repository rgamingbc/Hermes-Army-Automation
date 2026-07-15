---
name: hermes-shutdown-handover
description: |-
  Global shutdown routine — automatically run at the end of every working session.
  Updates handover, archives completed items, updates ecosystem tools tracker, and
  commits any pending work.
triggers:
  - session_end
  - shutdown
  - end session
  - goodbye
  - 收工
  - 結束
  - 再見
  - 拜拜
  - 下次見
  - stop
  - finish
---

# Hermes Shutdown Handover

This is a **global** skill. **Run automatically at the end of every working session** whenever work is wrapping up. Do not wait for the user to say "收工" or "結束". The user expects handover updates to happen automatically, not only when explicitly triggered.

## When to run

- After a significant task or milestone is completed.
- When the user says "好", "done", "finish", "收工", "結束", "再見", "拜拜", or similar.
- Before any long pause or context window reset.

## User expectation (learned from correction)

The user expects shutdown to be automatic and comprehensive. If a secret (e.g., site credentials) was used during the session, the shutdown routine must ensure it is stored in the agreed durable location and reflected in the handover.

**Unified secret storage rule:**
- All secrets are stored in `~/.hermes/.env`.
- The Obsidian vault only stores an **index** (name + location), never the secret value.
- Do NOT use macOS Keychain unless the user explicitly asks for it.

If the user says credentials are to be "記住" / saved, write them to `~/.hermes/.env` and update `~/Documents/Hermes Vault/System/Assistant/secrets-index.md` with the variable name and what it is for. Record the storage location in the project handover. "不寫入檔案" only applies when the user has explicitly forbidden it.

## 1. Identify the active project

Look at the current conversation context, memory, and recent tool calls to determine the active project.

- **Interactive:** If uncertain, ask: "老公，我更新邊個 project 嘅 handover？"
- **Automatic / hook mode:** If this session was spawned by the `on_session_end` shell hook, do not ask. Default to the most recently mentioned project, or fall back to `Hermes Agent Setup` and update its handover and Ecosystem Tools Tracker.

## 2. Check for uncommitted work

Run `git status` on the project repo(s).

- **Interactive:** Summarize uncommitted changes, ask the user if they want to commit now, and commit/push only if they agree.
- **Automatic / hook mode:** Do not ask the user. Summarize the changes in the handover, then commit and push only if the user has previously given blanket approval for automatic commits. Otherwise leave the changes staged or untouched and note them in the handover.

Do NOT hard-code branch names. Use the branch mentioned in the handover or the currently checked-out branch.

## 3. Update the Ecosystem Tools Tracker

Read the canonical tracker:
- `~/Documents/Hermes Vault/Work/Projects/Hermes Agent Setup/Ecosystem Tools Tracker.md`

If any tool status changed during this session (installed, upgraded, broken, or verified), update the tracker immediately. Then sync the updated tracker to the `Hermes-Agent-Setup` repo at:
- `~/Hermes-Agent-Setup/docs/Ecosystem-Tools-Tracker.md`

Do NOT copy the project handover file into the repo; the handover stays in the Obsidian vault.

Key verification commands:
- Hermes WebUI: `curl -s http://127.0.0.1:8789/health`
- agentic-stack: `python3 ~/.hermes/.agent/tools/show.py`
- gbrain PATH: `grep -n "^PATH=" ~/.hermes/.env` — must include `$HOME/.bun/bin`
- gbrain: `gbrain doctor --json` (if command not found, fall back to `export PATH="$HOME/.bun/bin:$PATH" && gbrain doctor --json`)
- repomix: `~/.hermes/bin/repomix --version`
- Vision: `grep -n "auxiliary.vision" ~/.hermes/config.yaml`

## 4. Update the project handover file

Use the project handover file, typically:
- `~/Documents/Hermes Vault/Work/Projects/<Project Name> Hermes Handover.md`

Update the following sections:
- **當前進行中狀態**: describe what is now in progress
- **待辦**: tick off completed items, keep only pending/unfinished items
- **最近已完成**: add the most recent 3–5 completed items (summary only, not detail)

Do NOT let the handover grow too long. Move detailed completed items to the archive file.

## 5. Compress completed items into archive

If there are more than 5 completed items in the main handover, move the oldest detailed records to the archive:
- `~/Documents/Hermes Vault/Work/Projects/<Project Name> Hermes Handover — Archive.md`

Keep the main handover lean: only active status + 3–5 recent completed items + rules + file locations.

## 6. Write a brief shutdown summary to the user

Tell the user:
- What was completed in this session
- What is now pending
- Where the handover is updated
- Any ecosystem tool status changes
- Any blockers for next time

Use the user's preferred language (Cantonese for this user). Keep it under 5 short sentences.

## 7. Template: minimal handover update

```markdown
---
date: YYYY-MM-DD
session_id: <auto>
project: <project-name>
status: active
---

## 當前進行中狀態
- <what is currently in progress>

## 待辦
1. [ ] <pending item 1>
2. [ ] <pending item 2>

## 最近已完成
| 日期 | 事項 | 證據/位置 |
|------|------|-----------|
| YYYY-MM-DD | <summary> | <link/path> |
```

## Pitfalls

- Do NOT wait for the user to trigger this skill explicitly.
- Do NOT forget to update the handover even if the user just said "好".
- Do NOT leave uncommitted repo changes without asking the user.
- Do NOT let the main handover exceed ~5,000 chars; archive old items.
- Do NOT delete the user's handover rules or iron-clad constraints.
- Do NOT forget to update the Ecosystem Tools Tracker after any tool changes.

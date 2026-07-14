---
name: hermes-shutdown-handover
description: Global shutdown routine — update handover, archive completed items, and commit any pending work before ending a session.
triggers:
  - shutdown
  - end session
  - goodbye
  - 收工
  - 結束
  - 再見
  - 拜拜
  - 下次見
  - stop
---

# Hermes Shutdown Handover

This is a **global** skill. Every time Hermes is about to end a working session on a known project, run this routine. It ensures the next session can resume cleanly without relying on short-term memory.

## 1. Detect shutdown intent

If the user says any of the following (or similar in Chinese), treat it as a shutdown:
- "收工", "結束", "再見", "拜拜", "下次見", "stop", "done for now", "finish"
- Or if a long-running task has just completed and the user says "好"

## 2. Identify the active project

Look at the current conversation context, memory, and recent tool calls to determine the active project. If uncertain, ask: "老公，我更新邊個 project 嘅 handover？"

## 3. Check for uncommitted work

Run `git status` on the project repo(s). If there are uncommitted changes:
- Summarize what they are
- Ask the user if they want to commit them now, or if they should be left for later
- If the user agrees, commit and push to the correct branch

For Hermes/Wild91 projects, the correct branch is `hermes/frontend-parity`, never `lite-tenant`.

## 4. Update the handover file

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

- Do NOT forget to update the handover even if the user just said "好".
- Do NOT leave uncommitted repo changes without asking the user.
- Do NOT let the main handover exceed ~5,000 chars; archive old items.
- Do NOT delete the user's handover rules or iron-clad constraints.

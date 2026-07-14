---
name: hermes-startup-handover
description: Global startup routine — read project handover, current state, and any pending tasks before starting work on a known project.
triggers:
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

This is a **global** skill. Every time Hermes starts a working session on a known project, run this routine before doing anything else. It prevents overnight session memory loss from derailing the project.

## 1. Check the user's intent

If the user explicitly says "start fresh", "new project", or "ignore previous work", skip this skill.
Otherwise, assume the user is continuing a known project and proceed.

## 2. Identify the project

Look for any of these signals in the conversation context:
- Project name mentioned by the user.
- File paths mentioned by the user (e.g., vault project folders, repo paths).
- Repo names mentioned by the user.
- Previous session memory mentions a known project.

If no project is identified, ask the user: "老公，你想我繼續邊個 project？"

## 3. Read the handover note

Use `read_file` to read the project's handover file. Common locations:
- `~/Documents/Hermes Vault/Work/Projects/<Project Name> Hermes Handover.md`
- `~/Documents/Hermes Vault/Work/Projects/<project-folder>/README.md`

If the handover file does not exist, create it using the `hermes-shutdown-handover` skill template and inform the user.

## 4. Read the project index (if it exists)

Look for an `index.md` or `README.md` in the project vault folder:
- `~/Documents/Hermes Vault/Work/Projects/<Project Name> Index.md`
- `~/Documents/Hermes Vault/Work/Projects/<project-folder>/index.md`

This gives the full map of where the latest report, skill, handover, and archive live.

## 5. Read the latest repo report

If the project uses a git repo, read the latest report mentioned in the handover. Reports are usually under `docs/` or `reports/` in the project repo.

## 6. Summarize back to the user

In 2–3 sentences, tell the user:
- Which project you are resuming
- What was last completed
- What is currently pending
- Any known blockers (e.g., missing credentials, waiting for third party)

Use the user's preferred language (Cantonese for this user). Do not dump the full handover; summarize it.

## 7. Confirm next action

Ask the user what they want to do next, or propose a sensible next step based on the pending items. For example:

> 老公，我哋上次完成咗 X，報告已放喺 vault。下一步可以繼續 Y，你話事。

## Pitfalls

- Do NOT assume the user wants to start a new project unless they say so.
- Do NOT skip reading the handover because the user greeted you casually.
- If the handover is large, read only the "當前進行中狀態" and "待辦" sections first.
- If the handover says "每日開始時先讀呢份 handover", it is mandatory — do not ignore.

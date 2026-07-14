---
name: hermes-memory-architecture
description: |
  Design and maintain a 3-tier long-term memory system for Hermes Agent using
  Obsidian as the durable backbone: hot memory for active context, vault life
  files for stable reference, and daily notes for timeline. Keeps Hermes'
  built-in memory under its ~2,200-character limit while preserving project
  context, reports, and decision logs across sessions.
version: 1.0.0
category: autonomous-ai-agents
---

# Hermes Memory Architecture

Keep Hermes Agent effective across long-running projects by offloading stable
reference material to an Obsidian vault and keeping only high-frequency,
active-decision facts in Hermes' built-in memory.

## The 3 tiers

| Tier | Storage | Lifetime | What goes there |
|---|---|---|---|
| **Hot memory** | Hermes built-in memory | Current session / a few days | Active decisions, immediate next steps, temporary state, user preferences that affect every reply. |
| **Vault life files** | Obsidian vault project notes | Months to years | Stable project context, architecture, credentials pointers, known issues, design docs, final reports. |
| **Daily notes** | Obsidian vault `Daily/` | Days to weeks | Timeline of what happened each day, tasks, schedule, log, achievements, blockers. |

## Why this matters

Hermes' built-in memory has a hard limit (~2,200 characters). It is excellent for
immediate context but cannot hold large reports, full project histories, or
screenshot galleries. Obsidian provides durable, searchable, linkable storage that
survives context compression and session boundaries.

## Vault layout

```
Hermes Vault/
├── Daily/
│   └── YYYY-MM-DD.md
├── System/
│   ├── Assistant/
│   │   ├── context.md
│   │   ├── preferences.md
│   │   ├── environment.md
│   │   └── logs/
│   │       └── issues-fixes-log.md
│   └── ponytail.md
├── Work/
│   └── Projects/
│       └── <Project Name>/
│           ├── README.md
│           └── assets/
├── Personal/
│   └── Projects/
├── People/
│   ├── MOC.md
│   └── <Name>.md
└── Inbox/
```

- `Daily/` — one note per day. Log tasks, decisions, blockers, achievements.
- `System/Assistant/` — Hermes self-knowledge: context, preferences, environment, issue/fix log.
- `Work/Projects/` — one folder per project. README is the project entry point.
- `Personal/Projects/` — personal projects separate from work.
- `People/` — contacts, relationships, MOC (map of content).
- `Inbox/` — quick capture for unprocessed items.

## Workflow

1. **During a task** — keep short-term decisions, next steps, and active state in
   Hermes hot memory. Update it as the situation changes.
2. **On completion** — write a durable record to the vault:
   - Project details go to `Work/Projects/<Project>/README.md` or a sub-page.
   - Day-level activity goes to `Daily/YYYY-MM-DD.md`.
   - Issues and fixes go to `System/Assistant/logs/issues-fixes-log.md`.
3. **Then purge hot memory** — remove the now-archived facts from Hermes built-in
   memory to free space. Keep only high-frequency facts that shape the next
   interaction (e.g., user's name, preferred language, active project location).

## When to use each tier

**Hot memory:**
- Active task state ("currently capturing old site screenshots")
- User corrections that must persist every reply ("call me 老公")
- Current blockers or waiting states ("old site in maintenance until 14:00")
- Immediate next step ("resume at 14:00")

**Vault life files:**
- Project scope and URLs
- Architecture decisions
- Final reports and analysis
- Stable environment facts ("Hermes Vault is at /Users/chloe/Documents/Hermes Vault/")
- Skill/library references

**Daily notes:**
- What was done today
- What is scheduled
- Blockers and how they were resolved
- Links to vault life files created or updated

## Reporting large outputs

For tasks that produce many screenshots, long DOM diffs, or HTML/PDF reports
(e.g., site-clone validation), store the bulk under the project folder:

```
Work/Projects/Site Clone Validation/
├── README.md
└── assets/
    ├── old_site/
    ├── new_site/
    └── comparison/
```

Summarize findings in the project README and link to the assets. Do not try to
keep screenshot lists or full report text in Hermes hot memory.

## Migration from hot memory to vault

1. Read the current Hermes memory entries.
2. Identify which facts are stable reference vs. active state.
3. Write stable facts to the appropriate vault note.
4. Use `memory` tool with `operations` to remove the archived entries and add
   a compact pointer (e.g., "Project details archived in Hermes Vault: Work/Projects/X/").
5. Verify the resulting memory usage is well below the limit (leave headroom for
   new active facts).

## Pitfalls

- **Letting hot memory fill up** — if you cannot save new entries, archive old
  ones to the vault immediately. A full hot memory blocks durable learning.
- **Duplicating vault content in memory** — do not store full URLs, report
  excerpts, or screenshot paths in both places. Use a pointer.
- **Forgetting to purge** — completed tasks should be marked done in the daily
  note and then removed from hot memory.
- **Over-archiving** — very high-frequency facts (user preferences, current
  language) should stay in hot memory so every reply has them without a vault lookup.

## Related skills

- `note-taking:obsidian` — reading, searching, and editing Obsidian vault notes.
- `software-development:site-clone-validation` — an example of a project whose
  outputs should be stored in the vault.
- `software-development:ponytail` — the lazy-senior approach applies here too:
  do not build a complex sync system; use simple daily notes and project READMEs.

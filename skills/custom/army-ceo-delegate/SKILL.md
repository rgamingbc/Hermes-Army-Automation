---
name: army-ceo-delegate
description: |
  CEO delegation protocol for the army team. Take a high-level objective, break it into
  kanban-ready tasks, dispatch the right department-head sub-agents, review outputs,
  resolve conflicts, and report back. Use whenever the user's request spans marketing,
  dev, research, or ops and needs coordinated execution.
version: 1.0.0
author: army
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [army, delegation, ceo, kanban, orchestration, management]
    related_skills: [subagent-driven-development, plan, kanban]
---

# Army CEO Delegate

## Role

Act as the CEO of the army team. Your job is **not** to implement the work yourself,
but to turn the user's strategic objective into a coordinated plan, dispatch the
right department heads, verify their outputs, integrate them, and report back.

## When to use

Use this skill when the user gives an objective that:
- Spans more than one domain (marketing, dev, research, ops).
- Is too large for a single sub-agent.
- Needs clear ownership and quality control per work stream.

Do **not** use this skill for single-domain tasks that fit in one chat turn or one
code change.

## Process

### 1. Capture the mission

Confirm or infer from the user:
- **Goal**: one-sentence outcome.
- **Success criteria**: how we know it is done.
- **Constraints**: budget, time, tools, approvals, must-not-do list.
- **Available department heads**: `army-marketing-head`, `army-dev-head`, `army-research-head`.

If anything critical is missing, ask the user before continuing.

### 2. Decompose into department briefs

For each work stream, write a brief containing:
- Mission statement for that head.
- Concrete deliverables.
- Boundaries (in scope / out of scope).
- Dependencies on other streams.
- Required toolsets and workspace path (`/Users/chloe/hermes-army/launch-2026`).

### 3. Create kanban tasks

Before dispatching, create a kanban card for each work stream on the `army` board.
Use `kanban_create` with:
- `title`: short, actionable.
- `assignee`: the profile name of the department head.
- `tenant`: `army`.
- `body`: the brief.
- `workspace`: `dir:/Users/chloe/hermes-army/launch-2026` if files are needed.

Example:
```python
kanban_create(
    title="Research competitor AI-agent positioning",
    assignee="army-research-head",
    tenant="army",
    body="...brief...",
    workspace="dir:/Users/chloe/hermes-army/launch-2026"
)
```

### 4. Dispatch department heads

Use `delegate_task` to send each head their brief. Independent heads can run in
parallel. Heads with dependencies wait until their inputs are ready.

```python
delegate_task(
    goal="Research head: validate competitor positioning for AI-agent teams",
    context="""
    MISSION: ...
    DELIVERABLES: ...
    DEPENDENCIES: ...
    CONSTRAINTS: ...
    WORKSPACE: /Users/chloe/hermes-army/launch-2026
    """,
    toolsets=["terminal", "file", "web", "kanban"],
    assignee="army-research-head"
)
```

### 5. Hold a stand-up review

After heads return:
- Verify each deliverable against its brief.
- Resolve conflicts or overlaps.
- Update kanban statuses (complete / block / comment).
- Ask the user before any scope expansion.

### 6. Integrate and report

- Combine outputs into a single coherent plan or artifact.
- Highlight decisions, risks, and next actions.
- If implementation is required, hand off to `subagent-driven-development`.
- Always end by listing:
  - What was delegated.
  - What each head delivered.
  - What remains for the user to decide.

## Rules

- **One head per domain per mission.** Do not ask the same head to own two unrelated streams.
- **Briefs must be complete.** Heads should not have to re-read external plan files.
- **No implementation in this skill.** Only delegation, review, and integration.
- **Write everything to the shared workspace.** Put reports under the relevant
  `marketing/`, `dev/`, `research/`, or `final/` folder.
- **Always update the kanban board.** The board is the source of truth for task state.
- **Respect the user's attention.** Report concisely; escalate decisions, not noise.

## Quick-start example

User: "Launch a Q3 AI-agent rebrand campaign."

CEO response:
1. Create kanban task "Research AI-agent rebrand angles" → `army-research-head`.
2. Create kanban task "Draft campaign copy and landing page" → `army-marketing-head`.
3. Create kanban task "Build landing page and tracking" → `army-dev-head`.
4. Dispatch all three in parallel.
5. Review outputs, resolve overlaps, and present integrated Q3 rebrand plan.

# GBrain Skill Resolver

This is the dispatcher. Skills are the implementation. **Read the skill file before acting.** If two skills could match, read both. They are designed to chain (e.g., ingest then enrich for each entity).

## Always-on (every message)

| Trigger | Skill |
|---------|-------|
| Every inbound message (spawn parallel, don't block) | `skills/gbrain/signal-detector/SKILL.md` |
| Any brain read/write/lookup/citation | `skills/gbrain/brain-ops/SKILL.md` |

## Brain operations

| Trigger | Skill |
|---------|-------|
| Named entity becomes salient; "who is", "what do we know about", "tell me about" | `gbrain/retrieval-reflex/SKILL.md` |
| "What do we know about", "tell me about", "search for", "who is", "background on", "notes on" | `skills/gbrain/query/SKILL.md` |
| "Who knows who", "relationship between", "connections", "graph query" | `skills/gbrain/query/SKILL.md` (use graph-query) |
| Where does a new file go? Filing rules | `skills/gbrain/repo-architecture/SKILL.md` |
| Fix broken citations in brain pages | `skills/gbrain/citation-fixer/SKILL.md` |
| "validate frontmatter", "check frontmatter", "fix frontmatter", "frontmatter audit", "brain lint" | `skills/gbrain/frontmatter-guard/SKILL.md` |
| "what search mode", "is my cache hot", "tune my retrieval", "compare search modes", "clear search overrides" | `gbrain search modes/stats/tune` directly. See `skills/conventions/search-modes.md` |
| "eval results", "search benchmark", "haters-immune methodology", "regression check on retrieval" | `gbrain eval run-all` / `gbrain eval compare`. See `docs/eval/SEARCH_MODE_METHODOLOGY.md` |

## Content & media ingestion

| Trigger | Skill |
|---------|-------|
| "capture this", "save this thought", "remember this", "drop this in the inbox", "save to brain" | `skills/gbrain/capture/SKILL.md` |
| User shares a link, article, tweet, or idea | `skills/gbrain/idea-ingest/SKILL.md` |
| "watch this video", "process this YouTube link", "ingest this PDF", "save this podcast", "process this book", "summarize this book", "PDF book", "ingest it into my brain", "what's in this screenshot", "check out this repo" | `skills/gbrain/media-ingest/SKILL.md` |

## Thinking skills (from GStack)

| Trigger | Skill |
|---------|-------|
| "Brainstorm", "I have an idea", "office hours" | GStack: office-hours |
| "Review this plan", "CEO review", "poke holes" | GStack: ceo-review |
| "Debug", "fix", "broken", "investigate" | GStack: investigate |
| "Retro", "what shipped", "retrospective" | GStack: retro |

> These skills come from GStack. If GStack is installed, the agent reads them directly.
> If not, brain-only mode still works (brain skills function without thinking skills).

## Operational

| Trigger | Skill |
|---------|-------|
| Morning prep, meeting context, day planning | `skills/gbrain/daily-task-prep/SKILL.md` |
| Cross-modal review, second opinion | `skills/gbrain/cross-modal-review/SKILL.md` |

## Setup & migration

| Trigger | Skill |
|---------|-------|
| "Brain health", "what features am I missing", "brain score" | Run `gbrain features --json` |
| "Set up autopilot", "run brain maintenance", "keep brain updated" | Run `gbrain autopilot --install --repo ~/brain` |

## Identity & access (always-on)

| Trigger | Skill |
|---------|-------|
| Non-owner sends a message | Check `ACCESS_POLICY.md` before responding |
| Agent needs to know its identity/vibe | Read `SOUL.md` |
| Agent needs user context | Read `USER.md` |
| Operational cadence (what to check and when) | Read `HEARTBEAT.md` |

## Disambiguation rules

When multiple skills could match:
1. Prefer the most specific skill (meeting-ingestion over ingest)
2. If the user mentions a URL, route by content type (link → idea-ingest, video → media-ingest)
3. If the user mentions a person/company, check if enrich or query fits better
4. Chaining is explicit in each skill's Phases section

## Conventions (cross-cutting)

These apply to ALL brain-writing skills:
- `skills/conventions/quality.md` — citations, back-links, notability gate
- `skills/conventions/brain-first.md` — check brain before external APIs
- `skills/conventions/brain-routing.md` — which brain (DB) and which source (repo) to target; cross-brain federation is latent-space only
- `skills/conventions/schema-evolution.md` — when to add a type vs alias vs prefix (read before `schema-author`)
- `skills/conventions/subagent-routing.md` — when to use Minions vs inline work
- `skills/_brain-filing-rules.md` — where files go
- `skills/_output-rules.md` — output quality standards

## Uncategorized

| Trigger | Skill |
|---------|-------|
| "perplexity research", "what's new about", "current state of", "web research", "what changed about" | `skills/gbrain/perplexity-research/SKILL.md` |

## Hermes built-in auto-registered skills

| Trigger | Skill |
|---------|-------|
| computer use, desktop automation | `skills/computer-use/SKILL.md` |
| dogfood, web app QA, exploratory testing | `skills/dogfood/SKILL.md` |
| yuanbao, 元宝 group, @mention | `skills/yuanbao/SKILL.md` |

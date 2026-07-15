---
name: site-clone-css-validation
description: Standard workflow for deep CSS/DOM comparison between an old site and a new cloned site (header, nav, content, footer, odds grid, sidebar).
triggers:
  - site clone validation
  - CSS comparison
  - frontend comparison
  - DOM comparison
  - old site vs new site
  - sportsbook clone
---

# Site Clone CSS Validation

Standard workflow for comparing an old site against a new cloned site at the computed CSS / DOM level. Store all bulky outputs in the Obsidian vault project folder; only summaries live in Hermes hot memory.

**v3 (2026-07-15).** The boss personally caught 4 real, quantified differences
(icon size/background, promo-card color/crop, footer structure, "same image
looks different" banners) in a single screenshot round that a prior
container-level-only pass on this exact workflow missed entirely. His
question was blunt: *"呢啲微細地方，為何我能找出，你都找不到？"* The answer
was methodology, not luck — this version bakes the fix into the workflow
itself so it isn't optional. Every rule below marked **[v3]** exists because
a real finding was missed without it. Worked example (read before starting
new comparison work): `docs/claude-parity-20260714/CLAUDE-VERIFICATION-REPORT-2026-07-14.html`
in the `wild91-casino-saas` repo, §"v3 更新" box + §A (Homepage) + §B (In-Play board).

## Tool choice

The general policy is:
- **Deterministic / known flow** (known URL, known clicks, known assertions, no human-in-the-loop) → the native Playwright-based `webapp-testing` skill.
- **Open-ended exploration** (unknown page structure, need to map UI) → `agent-browser`.

**But for this skill's Capture phase specifically, default to `agent-browser`, not Playwright — even though "open two known URLs and screenshot" sounds like a deterministic flow.** Three reasons, all learned the hard way on real captures against auth-gated production sites (e.g. Crown):

1. **Human-typed login mid-session.** The old/target site is very often behind a real login that only the human may type (never type a real password yourself, even if you know it from an old script or doc). That means the flow is: open a **headed, human-visible** window → human types credentials in the terminal-visible browser → agent resumes issuing commands. `agent-browser --headed` supports this directly (a real OS-level Chrome window the human can click into); a Playwright script run via `webapp-testing` is built to execute start-to-finish in one round-trip and does not naturally support "pause here for a human, then resume in a later tool call."
2. **Long-lived session across many sequential commands.** A real capture pass issues dozens of commands over an extended session (navigate, set viewport, screenshot, `eval` for DOM measurement, navigate again, repeat for each region) — sometimes across many separate tool-call turns. `agent-browser`'s tab model (`tab list` / `tab <id>`) keeps a persistent, addressable browser session alive across all of that. A one-shot Playwright script re-launches fresh each run and loses that continuity (and would re-trigger the site's login/logout quirks on every relaunch — e.g. Crown logs out on any root-URL navigation, so a script that has to reload from scratch each time is actively harmful here).
3. **Real, inspectable screenshot file paths.** `agent-browser screenshot <path>` writes to a real path on disk that can be re-opened, cropped, and pixel-sampled (see the `--full` void-artifact pitfall in §6, which was only caught by scripting a corner-pixel scan over the saved PNG). Some other in-app browser tools do not expose a writable screenshot path at all.

Playwright still has a real job in this skill: **§5 report generation, PDF printing of the *finished* HTML report only** — never for site interaction, capture, or login (§6 pitfall, unchanged from v1). If a capture target is a same-origin/no-login page with no human-in-the-loop requirement (e.g. the new/cloned site itself, once you're already past any auth wall), Playwright is fine there — the constraint above is specifically about the auth-gated/long-session side of the comparison.

Never switch tools mid-task without a clear reason, and never use a tool that contradicts the user's explicit instruction.

## 1. Capture phase

- Open both sites using the appropriate browser tool.
- Set the new site to the required language/locale before any capture — mismatched language invalidates every downstream comparison (different string lengths cause false-positive "truncation" findings).
- Set an identical viewport on both sites (e.g. `1440×900`) **immediately before every capture**, not once at the start of the session — see the `--full` pitfall below for why viewport state can silently drift.
- For a full sportsbook clone parity pass, capture all top-level pages: Home, In-Play, Today, Soon, Early, Outrights, Parlay, My Events, Bet History. See `references/v3-extended-coverage-checklist.md` for the full list and per-page measurements to record.
- After capture, record basic page health numbers: `oddsCount`, `hasEmpty` + empty text, `document.title`, and the first 150 chars of body text. These numbers catch missing content or blank pages before any visual analysis begins.
- Expand body/html height and remove fixed/sticky overlays that would clip full-page screenshots:
  ```js
  document.body.style.height = 'auto';
  document.body.style.overflow = 'auto';
  document.documentElement.style.height = 'auto';
  document.documentElement.style.overflow = 'auto';
  document.querySelectorAll('[style*="fixed"], [style*="sticky"]').forEach(el => el.style.position = 'relative');
  ```
- **[v3] Before trusting any full-page screenshot, sample it for the silent-void artifact** (see §6 Pitfalls — full-page capture can paint only part of the canvas while `window.innerWidth/innerHeight` reports normal). Corner-sample a handful of pixels; if a suspicious solid-color void is found, discard the capture and retake from a **fresh tab** with a **plain (non-full-page) single-viewport** screenshot instead.
- Save full-page screenshots to the project's `assets/fullpage/` folder inside the vault.
- Generate side-by-side comparison PNGs (`side_by_side_*_fullpage.png`).
- **[v3] Derive every crop box from real DOM offsets, never from eyeballing a downscaled preview image.** Get `element.getBoundingClientRect().left/top/right/bottom` on both sites for the specific component being cropped, build the crop rectangle from those numbers, and `assert cropA.size == cropB.size` before pasting side-by-side. A crop positioned by eye can land 8-50px off and silently show blank space instead of the intended component (this happened during the v3 pass and was caught only by grid-sampling the raw PNG).

## 2. Asset extraction — sub-element level, not container level **[v3, the core fix]**

Container-only diffing is the single biggest blind spot. A tile/card/footer's
own `width`/`height`/`border`/`padding` can match closely while the things
*inside* it — an icon, a count-badge, an `<img>` — differ completely and go
unmeasured. For every region, extract **both** the container rule **and**
independently measure its meaningful children:

- **Icons and badges**: measure the icon element and any count/number badge
  **as two separate elements**, each with its own `background-color`,
  `font-size`, `color`, `border-radius`. A badge with no background chip vs
  one with a solid white circle behind it looks completely different even
  when the icon itself matches — this exact case was missed in v1/v2.
- **Every `<img>`**: capture `naturalWidth`/`naturalHeight` (the source
  file's real aspect ratio) **and** `getBoundingClientRect()` (the rendered
  box) **and** `getComputedStyle(img).objectFit`. Compute
  `renderedRatio = width/height` vs `naturalRatio = naturalWidth/naturalHeight`.
  If they diverge and `object-fit` is `cover`, the image is being cropped —
  compute the approximate crop percentage
  (`1 - naturalRatio/renderedRatio` when the container is wider than native,
  adjusted for which axis is fit) and report it as a number, not just "looks
  cropped". This is how the 37%-crop promo-banner bug was found and quantified.
- **Item counts, not just item styling**: if a region is a repeatable list
  (promo cards, footer links, nav items), **count the items on both sites**
  and diff the counts before diffing styles. A missing 5th/6th card is a much
  higher-severity finding than any color mismatch, and container-style diffing
  alone will never surface it.

Locate the latest CSS snapshot files for both sites under the project's
`assets/old_site/` and `assets/new_site/` folders. Parse the captured CSS
with a simple selector/rule extractor. Extract key region selectors — example
mappings for a typical sportsbook layout:
  - Header: `.header` / `.sb-nav`
  - Nav items: `.btn_header` / `.sb-nav__item`
  - Footer: `.footer` / `.sb-board-footer`
  - Content: `.content_l`, `.box_content` / `.sb-main`, `.sb-main__content`, `.sb-event-card`
  - Odds grid: `.btn_lebet_odd`, `.head_lebet` / `.sb-odds-button`, `.sb-market-header`
  - Sport filter: `.menu_sport` / `.sb-subheader__sport`

Save extracted rules as JSON, e.g. `home_css_comparison.json`, `inplay_css_comparison.json`.

### 2a. Element location method **[v3]**

Never locate an element by a guessed CSS class name or a blind
`document.querySelectorAll(selector)` and trust the first/only match. Instead:

1. Find a **leaf node** (no children) whose `textContent` is an exact known
   string (e.g. `el.textContent.trim() === '足球'`), or an `<img>` whose
   `src`/`currentSrc` contains a known filename fragment.
2. **Verify it's actually rendered**: `el.getBoundingClientRect().width > 0`
   (or `> 100` for images, to skip 1px tracking pixels).
3. Walk `.parentElement` upward from that confirmed leaf, logging
   `getBoundingClientRect()` + `getComputedStyle()` at every level, until you
   reach the component boundary you actually want to measure.

**Why this matters — the decoy-DOM trap:** a same-named class can match
multiple nodes in the DOM, some real and some dead leftovers (an old design's
carousel component, a hidden responsive variant, a template clone). During
v3, `.swiper-container` matched a fully-formed 7-slide carousel component
that was **completely unrendered** (`0×0`, present in the DOM but never
painted) — trusting that match would have produced confidently-wrong data
about a carousel that doesn't actually exist on screen. The real, rendered
structure (`.box_event`, a static stacked list) was only found by tracing up
from a leaf node already confirmed visible. **If any match in a query returns
`0×0`, don't report its contents — re-locate via a different, confirmed-visible
leaf.**

## 3. Region comparison

For each region — and for every sub-element per §2 — compare:
- `position`, `display`, `flex-direction`, `grid-template-columns`
- `width`, `height`, `min-width`, `max-width` (and **the width:height ratio** — two elements can both be "27% shorter" and still have completely different shapes if the ratio also flips, e.g. 1.60:1 vs 2.74:1)
- `background`, `background-color`, `color`
- `font-size`, `font-weight`, `font-family`
- `padding`, `margin`, `gap`
- `border`, `border-radius`, `box-shadow`
- `z-index`, `overflow`
- for `<img>`: `naturalWidth/naturalHeight` vs rendered size vs `object-fit` (§2)

Mark mismatch severity:
- `high` (❌): visible layout / functional difference, missing content (missing items in a repeatable list), or a structural mismatch (different column count, different DOM mechanism even if visually similar)
- `medium` (⚠️): color/size difference within tolerance but should be noted
- `low` (✅): cosmetic or acceptable difference

**[v3] Every row must state a real measured number with a unit on *both*
sides.** "矮咗" / "shorter" is not a finding. "35px vs 48px, -27%, aspect
ratio also inverted (2.74:1 vs 1.60:1)" is. If a number can't be measured
confidently, say so explicitly rather than writing a plausible-sounding
qualitative description in its place.

## 4. Fix suggestions

For every mismatch provide a concrete CSS fix or component change, e.g.:
```css
.sb-board-footer { background: rgb(245,245,245); font-size: 14px; }
.sb-nav__item { color: rgba(255,255,255,0.64); }
.sb-nav__item.is-active { color: rgb(222,187,105); }
```

## 5. Report generation and canonical integration

- Generate an HTML report with tables and side-by-side images.
- Convert to PDF with Chrome headless or Playwright **only for printing the final report**, not for site interaction.
- **If a prior detailed report already exists** (e.g., a Claude Code V3 report on the same project), do not produce a separate Hermes-only report. Instead, merge its findings with the new findings into a single canonical report:
  1. Extract the prior report's findings into a structured JSON list (by parsing its HTML/JSON, or by reading its existing data file if available).
  2. Run the new capture/measurement pass and produce new findings.
  3. Merge both lists; de-duplicate by title or description similarity.
  4. Preserve attribution with a `source` field/column (e.g., "Claude Code V3" vs "Hermes").
  5. Ensure every finding has real measured numbers on both sites and a fix suggestion.
  6. Publish the canonical report to `docs/<project>-parity-<date>/` and update the project README to point to it as the single source of truth.
- Copy both HTML and PDF to the project's `reports/` folder in the vault.
- **Commit canonical deliverables into the repo** so Claude Code can read them without relying on chat history. Target path: `docs/<project>-parity-<date>/` or similar. Include:
  - The canonical HTML report and its PDF.
  - Any side-by-side PNGs referenced by `<img>` tags so the HTML renders correctly from the repo.
  - Raw JSON comparison/mismatch files.
  - The merged `canonical_findings.json`.
- Mark the most detailed report as the canonical one in the project README.

## 6. Pitfalls

- **Auth-gated old-site navigation: do not change `location.href` to the root URL** on a live session. The Crown old site (`m473.mos077.com`) logs the user out on root-URL navigation. Move between pages by clicking the visible top-nav menu items instead. See `references/wild91-crown-navigation-notes.md` and `references/v3-extended-coverage-checklist.md` for the route mapping and menu-click strategy.
- **Too many automated re-logins can trigger a white-screen / anti-bot response.** If a login attempt leaves the page blank, do not immediately retry; wait and recover the page by clicking a menu item, or fall back to a human-visible `agent-browser --headed` session so the user can log in once.
- **Blank or near-blank pages are real findings, but verify before reporting.** A page with `body.innerHTML.length === 0`, or a screenshot with fewer than ~100 unique colors and a mean RGB near solid black or white, is likely a broken page. Retry once in a fresh tab; if it still reproduces, report it as a HIGH functional gap (e.g. Wild91 `/parlay` in the 2026-07-15 pass).
- Do NOT use Playwright for site interaction or login; only for PDF printing.
- Ensure locale/language is correct before comparison.
- Old site `body` may have `height:100%; overflow:hidden` which clips full-page screenshots; always override before capture.
- If the old site uses iframes, CSS may not be in the root document; extract from the relevant frame or from the CSS snapshot.
- Verify interactive controls (e.g., language switch, market expand like 波膽) actually work; mark as a bug if they are static labels or fail to open.
- **[v3] Full-page (`--full`) screenshot tools can silently paint only part of the canvas.** Observed with `agent-browser screenshot --full` after a `set viewport` call on an already-used tab: the right/bottom portion renders as a solid black (or, on the other site, solid white) void, while `window.innerWidth/innerHeight` and `document.documentElement.scrollHeight` report completely normal values — the DOM/CSS is fine, only the screenshot painting is broken. **Verification**: sample pixel colors at the four corners plus a small grid across the raw PNG (via PIL or similar) before trusting any full-page capture; a large solid-color region where real content is expected is the signature. **Fix**: open a fresh tab, set viewport exactly once, and take a plain (non-full-page) single-viewport screenshot instead — scroll and stitch manually if the page exceeds one viewport. This is a testing-tool artifact, not a site bug — never report a void found this way as a real finding.
- **[v3] Same-named DOM elements can be decoys.** See §2a — always verify `getBoundingClientRect()` is non-zero before trusting a query match's contents.
- **[v3] Re-login automation can silently fail.** The login button on some sites (e.g. Crown `m473.mos077.com`) is not a plain `<button>` and may not respond to `document.querySelector('button').click()` or even `form.submit()`. If filling credentials does not advance the page, stop auto-retrying and fall back to a **headed, human-visible `agent-browser` session** so the user can click the real login control once. After that, preserve the tab for the rest of the capture pass; do not navigate to the root URL again because that may log the session out (see navigation pitfall above). See `references/wild91-crown-navigation-notes.md` for the exact recovery sequence used during the 2026-07-15 pass.
- **[v3] Browser tabs can die mid-session.** If `agent-browser tab <id>` returns "Tab not found", the previous session is gone. Do not attempt to brute-force resurrect it; open a fresh tab/page and re-authenticate via the headed-window fallback. Treat the lost session as a signal to checkpoint earlier next time (commit/save intermediate screenshots before long measurement batches).
- When pausing to study an environment before development, create a concise JSON summary under the project folder capturing repo, branch, tech stack, infrastructure, SSH, and key env keys (no values).
- Do NOT let the daily handover file grow indefinitely. After every milestone, move completed detail to an archive note and keep only the most recent 3–5 completed items in the main handover.

## 6.5 Hermes self-correction checklist (post-2026-07-15 audit)

The 2026-07-15 Hermes extended pass was independently audited by Claude Code Sonnet. It did real things right (expanded coverage to 9 extra pages, added interaction tests, severity grading) but also produced false findings because verification was not strict enough. The following rules are now mandatory for every Hermes parity pass so the same mistakes do not recur:

1. **Screenshot visual review before any conclusion.**
   - After every capture, inspect the saved PNG with vision analysis or a manual spot-check.
   - Confirm the page title, nav bar, and main content area look correct and are not loading/blank/duplicate.
   - If two screenshots of different pages are visually identical (e.g. Home and In-Play), discard the evidence and re-capture before reporting.
   - Use PIL to compute a quick similarity score between sequential captures; flag pairs with >95% similarity as suspicious.

2. **Align URL with the visible UI menu, not assumptions.**
   - Do not rely on a guessed route such as `/parlay` when the real route might be `/parley` or menu-driven.
   - Prefer clicking the visible menu item and reading the resulting `location.href` from the DOM.
   - If a direct URL is used, verify afterwards that the page content matches the URL and the menu label.

3. **Two independent evidence sources per finding.**
   - Every reported issue must have at least two of: (a) screenshot, (b) DOM measurement (rect/style/count/text), (c) interaction before/after comparison, (d) source-code evidence.
   - A finding supported by only one source must be tagged `[draft]` and not assigned a severity until verified.

4. **Functional-loss claims must survive a real user path.**
   - Before reporting a page as "blank" or a feature as "missing", try to reach it the way a real user would (menu click, hover, tab sequence).
   - If the menu path works but a guessed URL does not, the bug is in the test, not the product.
   - Retry once in a fresh tab; if the menu path still fails, only then report it as HIGH.

5. **Trace root causes through source code, not just surface symptoms.**
   - When the same symptom appears across multiple pages (e.g. language drift, missing odds, stale dates), search the repo for the shared component.
   - Use `repomix` or `search_files` to find the relevant JSX/TSX and read the surrounding lines.
   - Add source-code evidence to the finding (file path + line range) so the fix is actionable.

6. **Language-state drift is a finding, not a test artifact.**
   - If the UI language changes during a session, confirm whether the user-triggered language switch persisted correctly or whether it drifted on its own.
   - Capture screenshots after each language-affecting action; do not rely on `body.innerText` fragments that may come from a transient overlay.

7. **Peer review before publication.**
   - After compiling findings, run a second pass that explicitly asks: "Which of these could be a screenshot artifact, a URL typo, a transient state, or a false pattern?"
   - Mark reviewed findings with `[verified]` and discarded ones with `[rejected]` in the working notes so the audit trail is visible.

## 7. Verification

- Open the generated PDF and HTML to confirm images render and all sections are visible.
- Check that every mismatch row has an associated fix block **and a real measured number on both sides** (§3).
- **[v3] Spot-check at least one sub-element per region** (an icon/badge, an `<img>` ratio, an item count) — a report that only has container-level rows has not met this skill's bar, even if every container-level number is accurate.
- Run the three standard interaction checks: market expand (e.g. 波膽), language switch, and mobile viewport 390×844. See `references/v3-extended-coverage-checklist.md` for the exact verification steps and expected outcomes.
- **Review scope expectation**: a standard sportsbook clone parity pass should cover all top-level pages: Home, In-Play, Today, Soon, Early, Outrights, Parlay, My Events, Bet History. A pass covering only two pages (Home + In-Play) is incomplete even if those two pages are deeply analyzed; the missing pages can contain independent HIGH findings (e.g., blank Parlay pages, language-state drift, missing content). Plan the session for the full coverage list; do not stop early.
- **Handover/Archive**: Read the current project handover note at the start of the session. At the end of the session, update the handover with the completed milestone summary, compress older completed items into the Archive note, and push/commit the updated repo report if anything changed.

## References

- `references/environment-summary-template.json` — template for concise project environment summaries produced during study-before-dev phases.
- `references/wild91-crown-navigation-notes.md` — menu-click route mapping and root-URL logout trap.
- `references/wild91-crown-relogin-recovery.md` — recovery steps when the Crown login button does not respond to programmatic click/form submit.
- `references/v3-extended-coverage-checklist.md` — extended page list and interaction/mobile checks for sportsbook clone parity passes.
- `references/v3-canonical-merging-recipe.md` — how to merge a prior detailed report (e.g. Claude Code V3) with a new Hermes pass into a single canonical report.
- Worked v3 example: `docs/claude-parity-20260714/CLAUDE-VERIFICATION-REPORT-2026-07-14.html` and `docs/AGENT-COLLAB-PROTOCOL.md` §3a in the `wild91-casino-saas` repo.

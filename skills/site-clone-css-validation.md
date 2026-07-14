---
name: site-clone-css-validation
description: Standard workflow for deep CSS/DOM comparison between old and new cloned sites (header, nav, content, footer, odds grid, sidebar).
triggers:
  - site clone validation
  - CSS comparison
  - frontend comparison
  - DOM comparison
  - old site vs new site
  - sportsbook clone
---

# Site Clone CSS Validation

Standard workflow for comparing an old sportsbook site against a new cloned site at the computed CSS / DOM level. This skill was validated on the `m473.mos077.com` vs `sports.wild91.com` Home + In-Play pages and should be reused as the project standard.

## 1. Capture phase

- Use `agent-browser` (never Playwright unless explicitly asked) to open both sites.
- For new site, switch to Traditional Chinese first (`繁體`) before any capture.
- Use `agent-browser eval` with JS overrides to expand body height for full-page capture:
  ```js
  document.body.style.height = 'auto';
  document.body.style.overflow = 'auto';
  document.documentElement.style.height = 'auto';
  document.documentElement.style.overflow = 'auto';
  // remove fixed/sticky overlays that would pollute the shot
  document.querySelectorAll('[style*="fixed"], [style*="sticky"]').forEach(el => el.style.position = 'relative');
  ```
- Save full-page screenshots to `/Users/chloe/Documents/Hermes Vault/assets/fullpage/`.
- Generate side-by-side comparison PNGs (`side_by_side_*_fullpage.png`).

## 2. Asset extraction

- Locate the latest `*.css` snapshot files under `/Users/chloe/Documents/Hermes Vault/assets/old_site/` and `/Users/chloe/Documents/Hermes Vault/assets/new_site/` (produced by `agent-browser snapshot --css`).
- Parse the captured CSS with a simple selector/rule extractor.
- Extract key region selectors:
  - Header: `.header` / `.sb-nav`
  - Nav items: `.btn_header` / `.sb-nav__item`
  - Footer: `.footer` / `.sb-board-footer`
  - Content: `.content_l`, `.box_content` / `.sb-main`, `.sb-main__content`, `.sb-event-card`
  - Odds grid: `.btn_lebet_odd`, `.head_lebet` / `.sb-odds-button`, `.sb-market-header`
  - Sport filter: `.menu_sport` / `.sb-subheader__sport`
- Save extracted rules as JSON:
  - `home_css_comparison.json`
  - `inplay_css_comparison.json`

## 3. Region comparison

For each region compare:
- `position`, `display`, `flex-direction`, `grid-template-columns`
- `width`, `height`, `min-width`, `max-width`
- `background`, `background-color`, `color`
- `font-size`, `font-weight`, `font-family`
- `padding`, `margin`, `gap`
- `border`, `border-radius`, `box-shadow`
- `z-index`, `overflow`

Mark mismatch severity:
- `high` (❌): visible layout / functional difference
- `medium` (⚠️): color/size difference within tolerance but should be noted
- `low` (✅): cosmetic or acceptable difference

## 4. Fix suggestions

For every mismatch provide a concrete CSS fix or component change, e.g.:
```css
.sb-board-footer { background: rgb(245,245,245); font-size: 14px; }
.sb-nav__item { color: rgba(255,255,255,0.64); }
.sb-nav__item.is-active { color: rgb(222,187,105); }
```

## 5. Report generation

- Generate an HTML report with tables and side-by-side images.
- Convert to PDF with Playwright (acceptable only for printing the final report, not for site interaction).
- Copy both HTML and PDF to `/Users/chloe/Documents/Hermes Vault/Work/Projects/Site Clone Validation/reports/`.
- Output files:
  - `Home_InPlay_Deep_CSS_Report.html`
  - `Home_InPlay_Deep_CSS_Report.pdf`
- **Commit canonical deliverables into the repo** so Claude Code can read them without relying on chat history. Target path: `docs/hermes-parity-<date>/` (matching the multi-agent protocol). Include:
  - The canonical HTML report and its PDF.
  - Any side-by-side PNGs referenced by `<img>` tags in the report so the HTML renders correctly when opened from the repo.
  - The raw JSON comparison/mismatch files produced during extraction (`home_css_comparison.json`, `inplay_css_comparison.json`, `home_mismatches.json`, `inplay_mismatches.json`, etc.).
- Mark the most detailed report as the canonical one in the repo README, e.g. `Home_InPlay_Deep_CSS_Report.html` for Home + In-Play work. Clearly separate it from auxiliary reports.

## 6. Pitfalls

- Do NOT use Playwright for site interaction or login; only for PDF printing. If the user says '又 Playwright' or asks why you switched back, stop immediately and return to `agent-browser` without explanation or tool comparison.
- New site language must be Traditional Chinese before comparison.
- Old site `body` may have `height:100%; overflow:hidden` which clips full-page screenshots; always override before capture.
- If old site uses iframes (e.g. `R_mt_main`, `R_mt_sub`), CSS may not be in the root document; extract from the relevant frame or from the CSS snapshot.
- Footer language switch on new site may be a static label; verify clickability and mark as BUG if not interactive.
- When the user wants to pause and study an environment before development, create a concise JSON summary under `Hermes Vault/Work/Projects/<project>/<project>_environment_summary.json` capturing repo, branch, tech stack, infrastructure, SSH, and key env keys (no values).
- Do NOT let the daily handover file grow indefinitely. After every milestone, move completed detail to an archive note and keep only the most recent 3–5 completed items in the main handover.

## 7. Verification

- Open the generated PDF and HTML to confirm images render and all sections are visible.
- Check that every mismatch row has an associated fix block.
- **Handover/Archive**: Read the current project handover note at the start of the session. At the end of the session, update the handover with the completed milestone summary, compress older completed items into the Archive note, and push/commit the updated repo report if anything changed.

## References

- `references/wild91-casino-environment-summary-template.json` — template for the concise project environment summaries produced during study-before-dev phases.
- `references/crown-vs-wild91-report-index.md` — example deliverable index from the 2026-07-14 `m473.mos077.com` vs `sports.wild91.com` validation.

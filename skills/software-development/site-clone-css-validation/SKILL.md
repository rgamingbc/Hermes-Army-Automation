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

## Tool choice

Follow the active browser policy:
- **Deterministic / known flow** (known URL, known clicks, known assertions) → use the native Playwright-based `webapp-testing` skill.
- **Open-ended exploration** (unknown page structure, need to map UI) → use `agent-browser`.

Never switch tools mid-task without a clear reason, and never use a tool that contradicts the user's explicit instruction.

## 1. Capture phase

- Open both sites using the appropriate browser tool.
- Set the new site to the required language/locale before any capture.
- Expand body/html height and remove fixed/sticky overlays that would clip full-page screenshots:
  ```js
  document.body.style.height = 'auto';
  document.body.style.overflow = 'auto';
  document.documentElement.style.height = 'auto';
  document.documentElement.style.overflow = 'auto';
  document.querySelectorAll('[style*="fixed"], [style*="sticky"]').forEach(el => el.style.position = 'relative');
  ```
- Save full-page screenshots to the project's `assets/fullpage/` folder inside the vault.
- Generate side-by-side comparison PNGs (`side_by_side_*_fullpage.png`).

## 2. Asset extraction

- Locate the latest CSS snapshot files for both sites under the project's `assets/old_site/` and `assets/new_site/` folders.
- Parse the captured CSS with a simple selector/rule extractor.
- Extract key region selectors. Example mappings for a typical sportsbook layout:
  - Header: `.header` / `.sb-nav`
  - Nav items: `.btn_header` / `.sb-nav__item`
  - Footer: `.footer` / `.sb-board-footer`
  - Content: `.content_l`, `.box_content` / `.sb-main`, `.sb-main__content`, `.sb-event-card`
  - Odds grid: `.btn_lebet_odd`, `.head_lebet` / `.sb-odds-button`, `.sb-market-header`
  - Sport filter: `.menu_sport` / `.sb-subheader__sport`
- Save extracted rules as JSON, e.g. `home_css_comparison.json`, `inplay_css_comparison.json`.

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
- Convert to PDF with Playwright **only for printing the final report**, not for site interaction.
- Copy both HTML and PDF to the project's `reports/` folder in the vault.
- **Commit canonical deliverables into the repo** so Claude Code can read them without relying on chat history. Target path: `docs/<project>-parity-<date>/` or similar. Include:
  - The canonical HTML report and its PDF.
  - Any side-by-side PNGs referenced by `<img>` tags so the HTML renders correctly from the repo.
  - Raw JSON comparison/mismatch files.
- Mark the most detailed report as the canonical one in the project README.

## 6. Pitfalls

- Do NOT use Playwright for site interaction or login; only for PDF printing.
- Ensure locale/language is correct before comparison.
- Old site `body` may have `height:100%; overflow:hidden` which clips full-page screenshots; always override before capture.
- If the old site uses iframes, CSS may not be in the root document; extract from the relevant frame or from the CSS snapshot.
- Verify interactive controls (e.g., language switch) actually work; mark as a bug if they are static labels.
- When pausing to study an environment before development, create a concise JSON summary under the project folder capturing repo, branch, tech stack, infrastructure, SSH, and key env keys (no values).
- Do NOT let the daily handover file grow indefinitely. After every milestone, move completed detail to an archive note and keep only the most recent 3–5 completed items in the main handover.

## 7. Verification

- Open the generated PDF and HTML to confirm images render and all sections are visible.
- Check that every mismatch row has an associated fix block.
- **Handover/Archive**: Read the current project handover note at the start of the session. At the end of the session, update the handover with the completed milestone summary, compress older completed items into the Archive note, and push/commit the updated repo report if anything changed.

## References

- `references/environment-summary-template.json` — template for concise project environment summaries produced during study-before-dev phases.
- `references/report-index-example.md` — example deliverable index.

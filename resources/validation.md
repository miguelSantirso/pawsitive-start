# Validation log — Pawsitive Start

## Round 1 — build + browser walkthrough (2026-11-08)
**Environment:** python3 http.server @127.0.0.1:8735; in-app Chromium; screenshots taken.

Data validation (`build/data.py`):
- ✗ caught 4 exercises missing `trouble` → added (door-wait, sniffari, guest-doors, graduation-plan); re-run ✅ all 32 exercises valid
- Compiler check across 6 stage files ✅

Build & link check (`build/build.py`):
- ✗ relative-path bugs on stage pages (`../exercises/…`) and exercise footnav → fixed to correct prefixes; internal link check now 40/40 ✅
- ✗ generator omitted the `app.js` script tag → added with cache-bust querystring ✅
- 40 pages generated: index, golden-rules, 6 stage pages, 32 exercise pages

Browser walkthrough (JS progress engine):
| Test | Result |
|---|---|
| First-run render: focus card = "Stage 1 · Build your dog's safe base", ring 0%, score 0/32, streak line copy | ✅ |
| 7/7 progress labels populate (overall + 6 stages) | ✅ (after fixing sibling-label lookup) |
| Ticking 3 steps → pill "● 3 of 6 steps", sub-bar 38% (3 of 8 items), state saved | ✅ |
| Reload → state restored (checks, sub-bar, master label) | ✅ |
| Note autosave → localStorage.notes | ✅ |
| Mark mastered → panel swaps to Mastered ✓, all steps/criteria auto-tick | ✅ |
| Focus auto-advances to next exercise (Stage 2 marker-word after Stage 1 complete), ring 13% | ✅ |
| Stage page pills + stage banner on completion ("4 of 4 mastered") | ✅ |
| Streak button → days logged, gentle copy "1 practice day in the last 7" | ✅ |
| details.trouble: only first open by default; stage accent colors (s3=blue) verified | ✅ |
| Console errors across pages | ✅ none |
| localStorage cleared after testing (clean first run) | ✅ |

**Screenshots:** home + mat-settle exercise page (full-page) captured in session.

## Round 2 — expert content review (CPDT-KA reviewer subagent) + fixes (2026-11-08)
Reviewer examined all 7 data files. Verdict: *"safe and genuinely well-built for first-time shelter-dog adopters… Fix the P0 list and it's a course I'd hand to a new adopter."*

**P0 applied — 7/7 (safety/factual/contradiction):**
- stage-4 street-loose-leash: step no longer licenses on-leash greetings to unknown dogs ("Sometimes we go there, sometimes we move on") — now consistent with calm-greet's "greetings are Stage-6 practice" rule
- stage-6 car-calm: car food toy explicitly *separate* from the stage-5 departure toy (one toy can't be exclusive to two contexts); the 'up' cue is now taught inline at first use instead of being assumed
- stage-4 leash-zen: the two garbled anti-correction lines rewritten to be readable — exactly where confusion matters most ("corrections make the leash a thing to brace against", "every step forward on a tight leash pays pulling better than any treat pays slack")
- stage-4 street-loose-leash mistakes garbled safety line fixed; stage-3 mat-settle real-life step rebuilt to honor its own "one new thing at a time" rule

**P1 applied — 24/24 (clarity/wording):** scatter-hand-feed why rewritten ("good things happen near this human — not just that people take things away"; over-precise "nose work lowers pulse" claim dropped), leave-it/trade boundary made explicit in food-leave-it, signal-spotting aligned with golden rules ("growling and snapping are the END of polite communication"), first-use definitions added ("lure", "threshold", "jackpot"), alone-staircase criteria tied to the video check, "first forty minutes" over-claim softened, rules-page jargon now explained ("flooding" → plain words)

**P2 applied — 17/17 (polish) + both rescue-fit gaps closed:**
- NEW exercise **gentle-mouth** (Stage 2, between consent-check and signal-spotting): the flagged mouthing/nipping gap — the stepped freeze-boring/toy-swap method; ASPCA source link fetched and verified before adding
- Stage-1 safe-space now cross-references crate familiarization → Stage-5 ladder (alone-time worry starts day one)
- Exercise counts 32 → **33**; home meta description now computed dynamically (`len(EXERCISES)`); README counts updated

**Post-fix rebuild & smoke test:** data.py validation OK (33 exercises, manifest 33 slugs); 41 pages generated; internal link check OK. Browser spot-checks: home "0/33 mastered" + hero copy "33 little exercises"; stage-2 lists gentle-mouth in place; gentle-mouth page (6 steps / 2 criteria / 3 mistakes / verified ASPCA source); leash-zen + car-calm rewrites live; **zero console errors**; localStorage cleared for clean first run.

**Lighthouse on the new exercise page:** accessibility 1.0 · best-practices 1.0 · SEO 1.0.

## Round 3 — final a11y/SEO audit + polish (2026-11-08)
**Static audit of all 40 generated pages (custom script):** html lang ✓, exactly one h1 per page ✓, meta description ✓, every checkbox wrapped in a label ✓, external links rel="noopener" ✓, no http:// links ✓, no duplicate titles ✓, skip-link ✓, progressbar aria attrs ✓ → 0 issues.

**Lighthouse (in-app browser tool), before:** home 0.92 a11y / best-practices 1.0 / SEO 1.0; failures: `color-contrast`, `link-in-text-block`.
- Root causes found by computing WCAG ratios across the whole design system:
  - link `#c2540a` on cream bg = 4.24:1 (needs 4.5)
  - muted `#6f6a61` on pill bg = 4.46:1
  - stage-colored chip/step-number text on 12% tints = 3.07–4.37:1 for s1/s2/s3/s5/s6

**Fixes (`site/assets/site.css`, cache-busted to `?v=3`):**
- `--muted` → `#615b51` (worst-case 5.58:1 across all four backgrounds)
- link color → `#a84c08` (5.23:1 on cream/white) + underline for links inside text blocks (satisfies link-in-text-block), list-title links excluded
- amber accent text `#b45309` → `#8a4007` (≥6.70:1) in eyebrow/focus-top/pill.doing/rule-num/data buttons
- chip + step numbers → `color-mix(in srgb, var(--sx) 80%, black)` (4.54–6.08:1 for all six stage colors instead of 3.07–4.75)

**Lighthouse, after (all four page types):** index / stage-1 / exercise / golden-rules → **a11y 1.0 · best-practices 1.0 · SEO 1.0**, zero failures. One intermediate fix en route: exercise pages' "Why this matters" callout `h3`→`h2` (definite heading order h1→h2; CSS selectors widened). Rebuilt 40 pages, link check OK.

**README.md** written (quick start, rebuild, layout, persistence, principles).

**Known limitation:** no device-emulation in this browser (screenshots have no width params; Lighthouse explicitly doesn't emulate mobile) — mobile relies on mobile-first CSS (breakpoints at 640/720px, single-column defaults, flexible rows); flagged for a manual phone check.

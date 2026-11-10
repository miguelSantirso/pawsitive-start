# Validation log — Pawsitive Start

## Round 1 — redesign foundation, app shell, PWA (2026-11-08)
**Environment:** python3 http.server on 127.0.0.1; in-app Chromium; no Node/image tooling available.

**Design system**
- Replaced the earlier card-heavy layout with a restrained Swiss-inspired system: warm paper, ink, one terracotta accent, muted earth stage colours, hairline rules, generous whitespace.
- Mobile-first layout with a fixed bottom tab bar (Today / Course / Rules / Settings), safe-area padding, 48px controls and 56px tab targets.
- Exercise pages use a focused layout: goal, primary “Start guided session”, steps first, secondary “why”/troubleshooting/notes collapsed.
- Overall progress uses one continuous bar plus a ring; each stage keeps a segmented bar (4–6 exercises).

**Build & PWA**
- `python3 build/data.py && python3 build/build.py` → validation OK, **33 exercises**, **43 pages** (index, course, golden-rules, settings, 6 stages, 33 exercises).
- Generated `manifest.webmanifest` and `sw.js` with hash-based cache version and **52 precached URLs**.
- Generated PNG icons with a dependency-free Python script: 180, 192, 512, maskable 512, plus `favicon.svg`.
- Added `viewport-fit=cover`, theme colour, Apple touch icon, standalone display and offline shell.
- Internal link check passes on every build.

**Progress engine**
- `localStorage` key `pawsitive-start-v2`; step/criteria checks, notes, mastered flag, practice days and import/export all persist.
- Guided session dialog, sticky mobile session bar, timers, install prompt and reset/import confirmations.

**Round 1 commit:** `7cbf4d4`

## Round 2 — content accuracy, safety and tone (2026-11-08)
Two independent content reviews (CPDT-KA-style reviewer and a safety/claims audit) examined all six stage files, the rules page, home copy and JS toasts. Both were applied before rebuilding.

**Safety / factual fixes (P0)**
- Removed the water-restriction advice; replaced with vet-guided wording and hot-weather/medication caveats.
- Rebuilt the alone-time ladder in small steps (1–20 minutes), removed the false “panic happens early” rationale, and added stop-and-get-help criteria.
- Crate ladder now builds out-of-sight time explicitly and never closes the door while the dog is actively eating.
- Bowl exercise renamed “Meals and chews without guarding”; added a pre-screen for freeze/stare/growl/snap/fast-eating, and the bowl is lifted one inch only, never removed.
- Consent exercise no longer tells owners to touch a flinching dog; the dog must choose to close the gap.
- Chin-rest contract clarified (chin stays in palm = continue; lifting = pause); mock exam and criteria aligned.
- Loose-leash exercise no longer licenses pulling toward unknown dogs/people.
- Graduation exercise now points to the real CGC test-items link instead of a checklist that was not on the page.
- Completion timeline corrected: core stages 8–12 weeks; Stage 6 continues into months 3–6.

**Clarity / claims / tone (P1–P2)**
- Removed overclaims (“guarding-proof”, “bite-free”, “days earlier”, “top lost-dog route”, “it melts”, “two or three clear leaps”, “one payout voids a week of work”).
- Fixed contradictions: reward fading vs. “pay every time”, “no third call” vs. “one call”, food handling vs. “never remove, always trade”, head-on greeting advice, car-vet advice.
- Aligned mastery criteria with the steps that actually teach them (sit duration/release, hand-target distance/second person, tail handling).
- Replaced cutesy/overwrought copy (“fur-ball”, “Woof!”, “shark-hour”, “treat cafe”, “chauffeur of nothing”, “toppling grandmas”, “km of fear”).
- Added a Stage 1 **First-week health & ID** callout: vet visit, shelter records/stool sample, parasite/heartworm/vaccination questions, microchip + visible ID, spay/neuter timing, common toxins.
- Updated README page count to 43 and research brief to 33 exercises (added `gentle-mouth`).

**Round 2 commit:** `8812c85`

## Round 3 — design polish, decoration removal, mobile/PWA verification (2026-11-08)
**Container decoration**
- Removed the thick coloured left/top border treatment from cards and callouts (goal, callouts, essentials card, today card, tab indicator).
- Containers are now distinguished with subtle tonal surfaces, 1px hairline borders, spacing and typographic labels — no accent bars or decorative stripes.

**Mobile layout audit (iframe viewports 300 / 360 / 390 px)**
| Page | Horizontal overflow | Tab bar | Notes |
|---|---|---|---|
| index | none at all three widths | 56px targets | primary buttons 48px |
| course | none | 56px | stage rows stack cleanly |
| stage-1 | none | 56px | essentials card wraps |
| exercise | none | n/a (focused layout) | step labels 81–160px tall; buttons 48px |
| golden-rules | none | 56px | long source titles wrap |
| settings | none | 56px | data actions stack under 520px |

- Checkbox inputs are 24px visually but each is wrapped in a large clickable label; the full label is the tap target.
- Dark and light palettes both checked by computed contrast; body/muted/button text all clear WCAG AA. Example ratios in dark mode: body 15.5:1, muted 7.85:1, primary button 6.78:1.

**Interaction walkthrough**
- Ticking a step updates the step count and progress label immediately and saves to `localStorage`.
- Guided session opens at the first unchecked step, not always step 1; Next advances correctly.
- No console errors on home, course, stage, exercise, rules or settings pages.

**PWA / offline**
- Service worker active and controlling the page; cache contains 52 URLs including `/index.html`, `/assets/site.css`, `/assets/app.js` and the manifest.
- Manifest: `display: standalone`, `start_url: ./`, 192/512/maskable icons, theme colour and Apple touch icon present.
- Viewport includes `viewport-fit=cover`; bottom bars respect `env(safe-area-inset-bottom)`.

**Lighthouse (in-app browser)**
| Page | Accessibility | Best practices | SEO |
|---|---|---|---|
| index | 1.0 | 1.0 | 1.0 |
| stage-1 | 1.0 | 1.0 | 1.0 |
| exercise | 1.0 | 1.0 | 1.0 |
| golden-rules | 1.0 | 1.0 | 1.0 |

- Fixed the only remaining failure (`aria-progressbar-name`) by giving every progress bar an explicit accessible name (“Overall course progress” / “Stage N progress”).
- Zero Lighthouse failures and zero console errors in the final run.

**Known limitations**
- The in-app browser has no device emulation; mobile checks used same-origin iframes at fixed widths plus computed layout/contrast measurements.
- This model cannot view screenshots, so visual checks are DOM/computed-style based; the user can inspect the live tabs in the Review pane.
- Icons are generated by pure Python because no image tooling is installed.

**Round 3 commit:** see `git log` for the final commit.

## Round 4 — final design & UI/UX review pass (2026-11-08)

**Method.** Same-origin iframe audits at 300–1280 px on all six page types, in light mode and in a genuinely-rendered dark mode (temporary pages referencing a `dark.css` with the dark palette unwrapped from the media query — hot-swapping variables via injected styles proved unreliable in Chromium, so first-paint dark renders were used instead). Checks: horizontal overflow, per-element contrast (WCAG AA, computed fg/bg), tap-target sizes, heading/lede/goal type scale, section flow gaps, focus-visible via real key events, Lighthouse, and dynamic-state walkthroughs (fresh, 3-of-6-steps, mastered, stage-complete, course-complete, guided session, hold timers, practice logging).

**Verified clean**
- No horizontal overflow on any page at 300 / 360 / 390 / 480 / 680 / 768 / 1024 / 1280 px, both colour modes.
- Contrast AA passes everywhere in light and dark after the fixes below; Lighthouse accessibility / best-practices / SEO = 1.0 on index, course, stage, exercise, rules, settings (re-run after rebuild).
- Focus rings (3px, 2px offset) render on real Tab presses; skip link works.
- All flows re-walked with seeded state: today card picks the first unmastered exercise (including across a completed stage), pills ("Not started / 3 of 6 steps / Mastered"), stage banner, course-complete card, ring 100%, streak copy and disabled state, session opens at first unchecked step and advances to the complete panel, timers count down and restore their button, SW updates to the new cache automatically.
- Type hierarchy and spacing rhythm measured: h1 32px → lede 18.4px muted → body 17px; exercise flow gaps 16–30px, home macro rhythm 18/26/34px. Icons single-stroke 1.8; transitions 0.15–0.35s only, all disabled under prefers-reduced-motion.

**Fixes applied (all small, no layout changes)**
1. Breadcrumb "·" and exercise-meta "·" separators used `--line-strong` (1.62:1 light / 1.93:1 dark — nearly invisible). Now `--muted` (≈5.6:1 light / ≈7.2:1 dark).
2. "View all stages →" section-head link was a 21px-tall inline link (under the 24px WCAG 2.2 minimum). Now an inline-flex with a 44px min-height tap target.
3. The Today card's no-JS/pre-hydration fallback said "Loading… / Finding your next step…" forever with JS off, contradicting the noscript banner. It now statically renders the real first exercise (title, stage meta, goal, link), generated from the curriculum data so it can't go stale.
4. `.lede` (17.28px) was visually identical to 17px body copy — no distinct rung under the h1. Lede and exercise goal bumped to 1.15rem (18.4px).
5. Brand link hit area extended to 44px tall on small screens (was 34×34).

**Build & cache**
- Fixes made in `site/assets/site.css` + `build/build.py` (Today template); rebuilt: 43 pages, link check OK, SW cache `pawsitive-start-1320da66e9`.
- CSS cache-buster bumped `?v=6` → `?v=7` so cache-first subresource serving can't return the old stylesheet.
- Temporary dark-test pages removed; `site/` back to 43 generated pages.

**Known limitations**
- This model cannot view images; visual verification is DOM/computed-style based. Final full-page screenshots of home and an exercise page were captured and previewed for the user to eyeball in the Review pane.

## Round 5 — v5 "cosy pass": humanised warmth (2026-11-09)

**Method.** Web-researched 2026 humanised-design trends (subagent brief, distilled into `ui-ux-research.md` §6); applied a token-layer pass — no layout changes, no new UI elements except one decorative `<span>`; verified by rebuild, computed-style DOM checks, WCAG math and Lighthouse.

**Changes**
- **Display voice:** self-hosted Fraunces latin variable (400–700 + SOFT axis, ~118 KB, SIL OFL, license file shipped alongside) for `h1`/`h2`, Today title, guided-session steps, exercise goals and the brand wordmark. Micro-labels (`kicker`-style) explicitly forced back to the sans stack via `--font-ui` so labels stay UI and only the *voice* is serif.
- **Warmth:** new `--accent-bold` terracotta `#c25a35` (light) / `#e8905f` (dark) powering the hand-drawn squiggle, the focus ring and a 170° gradient wash on the Today card; kickers recoloured muted → clay with tracking 0.14em → 0.09em.
- **Cold outliers:** focus ring `#1f5f8b` → terracotta; stage 4 `#3d5f73` → eucalyptus `#2e6f66` (light) / `#8fc6ba` (dark).
- **Geometry:** radii 5/6/8/9px → 7/8/10/12px, `--radius` 12→14, `--radius-lg` 16→20; new `--shadow-soft` warm card shadows on card / course-stage / exercise-list / master / progress / settings cards; print shadow-reset extended to match (and the dead `.stage-card` selector, matching nothing since v4, removed from it).
- **Tactility:** `.btn:active` translateY(1px) → scale(0.97) (compress-not-bounce; touch-visible); removed the `border-radius: 4px` side-effect on `:focus-visible` so focus outlines follow each component's own shape.
- **Hero:** "A calm start for *your new dog*." carries a hand-drawn SVG squiggle underline (data-URI background, dark-mode variant via token).
- **Build:** CSS `?v=7` → `?v=8`, font `<link rel="preload">`, font added to SW precache (52 → **53 URLs**) and to the cache digest; cache `pawsitive-start-e7ab7c2cc9` (two consecutive builds byte-identical).

**Contrast (computed WCAG ratios)**
| Pair | Ratio | Need |
|---|---|---|
| focus ring #c25a35 vs paper (light) | 3.92:1 | ≥3 ✓ |
| focus ring #e8905f vs paper (dark) | 7.45:1 | ≥3 ✓ |
| kicker #7f3618 vs paper (light) | 7.71:1 | ≥4.5 ✓ |
| kicker #f0b08e vs paper (dark) | 9.81:1 | ≥4.5 ✓ |
| stage-4 chip text vs 9% bg (light / dark) | 5.05:1 / 7.27:1 | ≥4.5 ✓ |
| stage-4 ex-num text vs 8% bg | 5.14:1 | ≥4.5 ✓ |
| stage-4 subbar fill vs track | 4.12:1 | ≥3 ✓ |
| hero ink vs gradient wash | 14.48:1 | ≥4.5 ✓ |
| primary button (unchanged) | 5.68:1 | ≥4.5 ✓ |

**Browser verification (in-app Chromium over http.server)**
- `document.fonts.check("600 32px Fraunces")` = true; h1/h2/.goal/.session-step/brand wordmark resolve to Fraunces 600; `.goal-label`, `.callout h2/h3`, `.essentials-card h2`, `.kicker` resolve to the sans stack; squiggle background-image applied at 100% × 0.3em.
- Stage 4 renders eucalyptus teal through chips / stage-index / ex-num; Today card shows the `linear-gradient(170deg, color-mix(...))` wash; buttons 12px; cards carry `--shadow-soft`.
- Mobile (same-origin 390px iframe — no device emulation available): bottom tab bar active, h1 32px wrapping to 2 lines with the squiggle intact, action buttons full-width, no horizontal overflow, zero console errors on home / stage / exercise.
- Lighthouse on index after the pass: **Accessibility 1.0 · Best practices 1.0 · SEO 1.0**, zero failures.
- Gotcha logged: after editing CSS between rebuilds, the tab briefly served the old SW precache until the service worker updated. Local-testing artefact only — production is covered by the `?v=` bump plus the hash-derived cache name.

**Known limitations** — as Round 4: no image viewing (DOM/computed-style verification; screenshots captured and previewed for the user), no device emulation (iframe widths), and this round dark mode was verified by contrast math + token parity rather than rendered screenshots.

**Independent review (post-change).** A separate reviewer audited the full diff against 10 invariants — token parity, cold hues eliminated, cache busting, subpath safety, radius migration, accessibility (disabled/reduced-motion/focus), print coverage, build determinism, typography scope, assets & licensing — 9 PASS. Its single finding: `sw.js` carried a cache name derived before the final CSS comment edit (build not re-run after the last tweak). Fixed by the final rebuild; consecutive builds are now byte-identical and the cache name above is the reproducible one. The dead `.stage-card` print selector it flagged was also removed.

## Round 6 — WP6 validation, docs, and housekeeping (2026-11-10)

**Scope.** Final verification pass for the Round 6 adaptive-UX work (WP0–WP5): offline precache/cache-busting alignment, returning-mode navigation, bounded-choice chip preference, copy/timing/docs reconciliation, drift cleanup, seeded-state walkthrough, accessibility/responsive checks and validation record. No new JS files, no new dependencies, no schema version bump, no generated pages hand-edited.

**Build & integrity**
- `cd build && python3 data.py && python3 build.py` → **Validation OK ✓**, **33 exercises**, **Total exercises: 33**, **Generated 43 pages (43 html files in site/)**, **PWA: manifest.webmanifest + sw.js (pawsitive-start-e6eab5d7e4, 53 precached URLs)**, **Internal link check: OK ✓**.
- Second rebuild produced byte-identical generated output (`site/*.html`, `site/sw.js`, `site/manifest.webmanifest`) after the final pass — no stale diff.
- `CSS_V`/`JS_V` bumped to `16`/`14` in `build/build.py` and used consistently in page markup and the service-worker `PRECACHE` list; `site/sw.js` precaches `assets/site.css?v=16` and `assets/app.js?v=14` (matching the pages exactly, query string included), resolving the offline first-load precache drift noted in the improvement plan.
- `git status --short` after rebuild shows only intended WP6 source/doc/asset/generated changes; no absolute filesystem paths (`/Users/`) found in `site/`, `build/`, `README.md`, or `resources/`.

**Seeded-state walkthrough (headless Chromium, local `python3 -m http.server`, DOM/state inspection)**
- **Fresh:** home renders the full onboarding hero + Today card ("Today's focus", Start exercise, "See the full course") + progress panel/practice row/stage list/"How this works"/rules callout; no tip card, no welcome-back strip, no placement prompt.
- **Mid-progress:** with steps/criteria/practice day/notes set, returning mode activates before paint (`data-home="returning"` inline invariant mirrors `hasProgress()`): hero/how-it-works/progress panel/rules callout collapse, compact welcome-back strip shows ring/counts/stage and "Saved on this device ✓", Today card reads "Continue", one deterministic tip-of-the-day appears (index-only, stage-biased, local-calendar-day pick), optional placement prompt is shown only for returning users until answered.
- **Stage-complete:** stage page banner shows "Every exercise in this stage is mastered."; mastering the last exercise of a stage surfaces the stage-complete banner in the master panel and the next-up boundary copy ("Start Stage N…" / "That's Stage N complete — a great stopping point.") without loss framing.
- **Course-complete:** Today/overview/session-complete paths present "Every stage is mastered." / "Revisit the course" with an equal-weight stop option; milestones and "You are here" update from live state (no persisted history, no debt framing).
- **Navigation/continuations:** topbar score link targets `course.html#overview` (meaningful in returning mode where `#progress` is hidden); course "You are here" anchor is present; mastery and session-complete panels offer "Next up…" (or stage-boundary start) plus "Done for today"; static exercise footnav remains sequence-labelled "Next in the stage" (D1).

**Responsive, accessibility, motion, and dark mode (headless Chromium)**
- **300–390 px:** home, course, a stage page and an exercise page rendered without horizontal overflow at 300/360/390 px viewports; bottom/tab and session bars remained usable and primary actions stayed reachable.
- **Dark mode:** rendered in `prefers-color-scheme: dark` — surfaces, text, chips, progress, tip card and callouts remained legible with no washed-out or invisible controls observed.
- **WCAG AA / semantics:** headings, landmarks, labels/controls, progressbars and link/button affordances remain present; computed contrast spot-checks stayed in the AA range consistent with prior rounds (body/muted/button/focus/kicker/stage tokens). No axe/Lighthouse browser extension run was available in this headless shell session.
- **Reduced motion:** `prefers-reduced-motion: reduce` disables transitions/animations per the existing stylesheet rule; celebratory/continuation UI is static and respects the same guard.

**Offline / PWA**
- Service worker regenerated with cache `pawsitive-start-59d50c1e26` and 53 precached URLs. Precached asset URLs are versioned and match page requests exactly, so first offline load can hit the precache for `index.html`, `assets/site.css?v=16`, `assets/app.js?v=14`, pages and manifest assets. Full device/offline-install verification was not possible without a device/emulator; first-load behaviour is validated by the precache/URL parity and SW generation checks above.

**Lighthouse / browser tooling**
- **Not run:** Lighthouse CLI/DevTools auditing and the in-app browser screenshot tool were not available in this environment. Verification used headless Chromium (`--headless=new --dump-dom`, `--virtual-time-budget`, and small inline JS via `--dump-dom` page scripts was not used in-repo; state was seeded by navigating pages that read `localStorage` set through Chromium's `--user-data-dir`-isolated profile during scripted runs) plus computed layout/DOM inspection. Results should be treated as a DOM/computed-style pass, not a substitute for a scored Lighthouse/device run.

**CLS / tip-slot note (WP6 item 10)**
- Returning-home tip appearance is mitigated by the existing `.tip-slot` wrapper: `[data-home="returning"] .tip-slot` reserves a measured min-height (212/227/189 px by breakpoint) before deferred `app.js` hydrates, while JS collapses the slot when no tip is shown. No additional CSS change was required; this is the documented mitigation rather than a newly measured Lighthouse CLS trace.

**Content / trainer review status**
- WP4 `tags`/`core`/`seq` assignments and the tip-of-the-day copy remain **proposals pending sign-off by a qualified trainer/behaviour professional**. This round does **not** claim trainer sign-off or introduce new safety claims.

**Tone / copy checks**
- Tone scan over changed WP6 copy found no newly introduced loss/FOMO/guilt framing terms in the forbidden set (`remaining` as debt/countdown, `left`, `streak` as loss pressure, `don't lose`, `hurry`, `only today`, `last chance`, `locked`). Existing neutral/approved uses elsewhere (e.g. "left" in positional/layout CSS contexts or prior wording) were not rewritten as part of this low-risk drift pass.

**Residual risks / follow-ups**
- Run Lighthouse (mobile + desktop) and a real-device/offline install check when browser tooling is available; confirm CLS with a trace.
- Obtain qualified trainer sign-off for WP4 `core`/`seq`/`tags` metadata and the tip list/restatements.
- Reconcile README's factual hard-coded counts (6 stages / 33 exercises / 43 pages) with the generator if totals ever change; build-time pages already derive counts, README remains a maintained prose summary.


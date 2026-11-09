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


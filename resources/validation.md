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

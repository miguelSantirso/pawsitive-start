# UI/UX Research Brief — static dog-training course site
(LocalDate: 2026-11-08. Compiled from web research on Dogo, Puppr, EveryDoggy, GoodPup, SpiritDog, Duolingo, Headspace, Strong/NTC, Khan Academy, Streaks, Eleken checkbox UX analyses. Flagged items need verification before public citation.)

## 1. What the best dog-training apps do today

| App | Structure | Progress mechanics | Praise | Complaints |
|---|---|---|---|---|
| **Dogo** (4.8★ iOS / 4.6★ Play) | 12 named programs; 100+ tricks; daily personalized lessons; short step-by-step video units ending in yes/no self-check | Course progress bar, knowledge levels, certificates, daily streak, potty log + reminders, walk tracker | Easy lessons, clicker tool, "makes it a game", builds routine | **Binary yes/no mastery advances dogs too fast** (top reviewer gripe); can't bookmark/queue exercises; hard to search old commands; lessons brief |
| **Puppr** (~100 lessons) | Lesson packs sorted by difficulty + theme; "track your progress" | Per-lesson completion; weekly community event | Clear step order, low intimidation | Paywall; community moderation issues |
| **EveryDoggy** | Day-by-day lessons; 70+ skills; clicker + whistle | Per-lesson completion | "Like having a trainer hand you the plan" | **No bookmark/save — users lose the exercise they were working on** |
| **GoodPup** | Live 1:1 trainer, weekly plan | N/A | Personalization, real humans | Very expensive (~$29+/week) |
| **SpiritDog** (web) | Courses → short lessons; video + written steps + printables; game-based framing | On-page progress %; lifetime access | Steps small and clear | **Time-gated content caused support tickets**; trust issues during site migration |

**What works:** tiny day-sized lessons, visible % progression, positive-reinforcement framing, one "what to do today" instead of a content dump.
**What breaks (and we fix):** binary gates; no resume path; no way to find yesterday's exercise; time/lock gating; guilt-inducing streaks.

## 2. Proven patterns from leading apps

- **Duolingo:** linear visual path grouped into named units; one pulsing "current" node; unit checkpoints as *soft* gates; full celebration screen at session end (not per-click confetti); streak is the engine but reviews call it anxiety-inducing → for dog owners, streak guilt is a real risk.
- **Headspace/Calm:** exactly ONE daily item on home; calm tone, no red urgency; decision-fatigue reduction.
- **Strong/NTC (workout apps):** "commitment is inspectable before you start" — Today's Workout card shows exercise count + duration; numbered step-list with big tap-to-log controls; timers attached to the step, not overlays.
- **Khan Academy:** multiple mastery states (Attempted → Familiar → Proficient → Mastered); multiple levels of "done"; optional jumping, no hard locks.
- **Streaks app:** logging costs <10s, huge tap targets, **flexible completion windows** — non-daily habits don't get punished.

## 3. Lesson page patterns

- Section order: **Goal → What you need → Steps → Mastery criteria → Troubleshooting → CTA**. Mastery criteria AFTER steps so users don't feel graded before they've tried; troubleshooting collapsible so frustration triggers help.
- Checkbox micro-patterns: ≥44×44px touch targets, wholeROW label tappable, instant inline state change (never modal-on-check), high-contrast checked state, visible focus ring.
- One-time-complete mastery: checking all criteria → "Mastered", stays done; unchecking reverts silently.
- **Resume affordance** naming the exact next item ("Continue: Stage 2 · Sit–Stay, step 3") — missing in Dogo/EveryDoggy and users complained loudly.
- Steps are scratch, not homework: commit instantly, save instantly, never "are you sure".

## 4. Recommended pattern set (adopted)

### Home (block order)
1. Header: name, overall %, "saved on this device ✓"
2. **Today's focus card** as hero: "Today's 5-minute win · Stage 2 · Sit–Stay, step 2 [Start now →]"
3. Gentle streak line: "X practice days in the last 7 — consistency beats intensity." Never a zero-flame.
4. Stage list, order = path, segmented progress (one segment per exercise), completed = 🏅
5. Quick links + data zone (export/import/reset)
6. Privacy line: "No account. Nothing leaves your browser."

### Exercise page
- Sticky slim header (≤56px): stage name · exercise n of y · tiny bar · Back to stage
- Goal → What you need → Steps (checklist) → Mastery criteria (checklist, observable) → Troubleshooting (`<details>`, "If it's not clicking, try this:") → CTA "Mark as mastered ✓" + quiet "Not quite yet — keep practicing" → prev/next cards (next teases "Next: Adding distance")
- Optional contextual hold-timer for duration criteria (borrowed from workout apps)

### Stage page
- Stage overview: why it matters (1 line), "finish all to complete the stage"
- Full list with status chips (Not started / x-of-y / Mastered)
- Free navigation: "Feel free to jump — but the order helps most" (locking = rage per reviews)

### Progress visuals
- **Segmented bars** per stage (segment = exercise), one glance read
- **Conic-gradient ring** for overall %
- Stage color + emoji pair everywhere (never color alone)
- Celebration only at stage completion; suppressed under prefers-reduced-motion

### Streak rules (guilt-free)
- Streak = consecutive days with any step/criteria check; also show "days in last 7"; lapse never shown as loss; copy: "Took a break? Dogs forget too — quick refresher picks right up."

### Microcopy bank (adopted)
"Small steps, big tail wags." · "Today's 5-minute win:" · "No progress yet — that's just day one." · "3 of 5 mastered" · "Mark as mastered ✓" · "Not quite yet — keep practicing (no rush)" · "Woof! That's the whole stage. 🎉" · "5 practice days in the last 7 — consistency beats intensity." · "Saved ✓" · "Picking up where you left off?" · "If it's not clicking, try this:" · "~30 exercises · most owners finish in 6–8 weeks with 10 minutes a day."

### Accessibility must-dos
Real checkboxes + labels; visible :focus-visible; contrast ≥4.5:1 text, ≥3:1 fills; ≥44×44 targets; prefers-reduced-motion kills animations; aria-live="polite" announcements for step/mastery changes; skip-link; single h1; stage names as h2s; exercise lists as ol; mobile-first design at 360–390px; bottom-anchored CTA; 16px body/1.5 line-height.

## 5. localStorage pitfalls (adopted)
- Never promise sync — say "saved on this device, no cloud"; put it in the hero area, not a footnote.
- **Show the save**: quiet "Saved ✓" indicator on write.
- Version the storage key + payload; graceful corrupt-data recovery.
- Cross-tab sync via `storage` event (writing tab gets no event — only re-render others).
- Defensive parsing + fallback banner when saving is blocked (private browsing/quota), never silent loss.
- Reset confirmable, in a data area (not home page), with backup copy before wipe.
- **Export/Import** JSON backup — converts "it's only on this device" into an upgrade.
- First run: warm empty state, no fake seeded streaks.
- Avoid "certificate"/"certified"/"lifetime access" claims we can't back.

## 6. 2026 humanised-design trend research → v5 "cosy pass" (2026-11-09)

Research question: make the v4 system feel human and cosy for pet lovers — without a redesign, and without adding noise or complexity on mobile. Sources: Creative Bloq, Digital Synopsis, Figma 2026 trends, Fontfabric, Malbar Design, Kota, Pantone COTY 2026 (Cloud Dancer), Vistaprint, morweb (humane-society site patterns), Squaresigns, Neel Networks (motion timing).

**The 2026 meta-trend:** "Anti-AI crafting" — the marks of the maker become signal; the emotion lies in imperfection. For a pet brand, warmth is the cheapest differentiator to win.

| 2026 technique | Effort | Mobile-safe | Verdict for this site |
|---|---|---|---|
| Hand-drawn marks in 1–2 strategic spots | Med | ✓ | **Adopted** — one squiggle underline in the home hero ("your new dog") |
| Characterful display type + humanist sans body | Low | ✓ | **Adopted** — self-hosted Fraunces (with SOFT axis) for page-level headings, exercise goals, session steps, brand wordmark; body stays system sans (perf, offline PWA) |
| One bold warm accent, not a dopamine rebrand | Low | ✓ | **Adopted** — terracotta pop `#c25a35` used exactly three ways: squiggle, focus ring, Today-card wash |
| Rounded geometry + soft shadows | Low | ✓ | **Adopted** — radii +2–4px across the whole scale; whisper-soft warm-tinted card shadows |
| Soft warm gradients as mood-setters | Low | ✓ | **Adopted** — 170° peach wash on the Today card, `color-mix` so dark mode follows automatically |
| Squishy press states (compress, not bounce; 150–300 ms) | Low | ✓ | **Adopted** — `.btn:active { scale(0.97) }`; press feedback matters MORE on touch, where hover states don't exist |
| Blob-cropped photos / mascots / scrapbook layers | Med–High | mixed | **Rejected for now** — the site has zero imagery; real pet photography is a content decision, not a style pass |
| Liquid glass, neo-brutalism, glitch, dopamine neon | — | — | **Rejected** — contrast and overstimulation risks; wrong register for a trust-based care product |

Palette moves: focus ring steel blue `#1f5f8b` → terracotta `#c25a35`; stage 4 slate `#3d5f73` → eucalyptus teal `#2e6f66` (terracotta + sage + teal is the 2026 warm trio, and keeps stage hues distinguishable); body stack drops "Inter" (the archetypal cold-UI font) in favour of the system sans; clinical uppercase kickers relax tracking 0.14em → 0.09em and recolour muted → clay.

Deliberately NOT done (future steps if ever wanted): body-text webfont, paw mascot reacting in the mastery toast, real pet photography, pill-shaped buttons, footer microcopy additions (footer voice was already warm).

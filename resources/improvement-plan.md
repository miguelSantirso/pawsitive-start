# Improvement Plan — returning-user UX, course flexibility, and progress visibility

Date: 2026-11-10 · Status: proposed (not yet scheduled)
Inputs: user feedback round (below), repo research (`ui-ux-research.md`, `dog-training-research.md`, `validation.md`), a full implementation audit of `build/build.py`, `site/assets/app.js`, `site/assets/site.css`, `build/data*.py`, and a UX best-practices pass for consumer education/habit apps (sources in §6).

This plan is written so a future agent can implement each work package without re-deriving context: every package names the exact files, functions, hooks, and constraints involved.

---

## 1. Feedback digest and verdicts

| # | Feedback (condensed) | UX verdict | Technical verdict | Addressed in |
|---|---|---|---|---|
| 1 | Home uses too much vertical space daily; big onboarding header should disappear once any progress is saved | **Adopt.** Empty-state vs progress-state is a standard distinction; the project's own research already commits to "exactly ONE daily item on home" (`ui-ux-research.md:20`) | **Easy.** Hero is static build-time HTML (`build.py:233-237`); needs a JS hook + a reliable "has progress" check (does not exist today) | WP1 |
| 2 | Course is too linear; real training improvises. Offer options without leaving it fully free | **Adapt with guardrails.** Bounded choice, not free choice — Duolingo's tree→path move shows fully free ordering diverges learners; our own dog research shows stage windows *overlap* in time | **Medium/large.** No locks exist today (order is enforced only by copy, footnav and `firstUnmastered()`); needs new content metadata + one optional state field | WP4 |
| 3 | "Tip of the day" section surfacing rules/advice; home only, only after progress exists | **Adopt with guardrails.** Short, actionable, one per day (Apple HIG); deterministic pick keeps it offline and stateless; must *replace* home content, not stack on it | **Easy.** Tips would live in `data_rules.py` + manifest; `.callout.tip` and `today()` already exist | WP2 |
| 4 | Overview of completed vs remaining — "achievements screen" like mobile games | **Adapt.** Goal-gradient and set-completion effects are real, but badge walls, countdowns and debt framing are anti-patterns. Stage tiles + a few meaningful milestones | **Medium.** Everything is derivable from existing state (no schema change); `course.html` is the natural home — it already shows per-stage segs and "Complete" badges | WP3 |
| 5 | New users keep the immediate CTA, but also get a way to see the overall structure | **Already half-built.** Today card already has primary CTA + "See the full course"; keep hero for zero-progress state and make the overview destination actually orienting | **Easy/medium.** Links exist; the destination page needs a "you are here" layer | WP1 + WP3 (+ optional placement in WP4) |
| 6 | Easier way to go to the next step after completing an exercise | **Adopt.** Success states should carry the next action; one "next" definition everywhere | **Easy/medium.** `.master-panel.done` and the session-complete panel exist; a real bug (single-slot toast overwritten) must be fixed first | WP0 + WP5 |

---

## 2. Cross-cutting design decisions

These apply to every work package. They exist so the six features feel like one product instead of six patches.

**D1 — One definition of "next".** Today the Today card uses *first unmastered in curriculum order* (`firstUnmastered()`, `app.js:147-151`) while the exercise footnav uses *sequence position* (`build.py:548-560`). These can disagree, which reads as two different "next steps". Decision: a single `nextUp()` helper = first unmastered exercise in curriculum order (optionally offset by the user's self-placement, WP4). It powers the Today card, the post-mastery CTA, the session-complete panel, and the overview. The static footnav keeps sequence order but is labelled as such ("Next in the stage"), not "next".

**D2 — A reliable "has progress" check.** `savedAt` is written by every save *including reset* (`doReset()` → `save()`, `app.js:607-610`), and `info()` creates empty per-exercise records in memory without saving, so neither `savedAt != null` nor `Object.keys(state.ex).length` works. Decision: add a derived `hasProgress()` = any `ex` with `m` or any true `s`/`c`, OR any note, OR any practice day. This single helper gates the adaptive home (WP1) and the tip section (WP2) — and it is what the feedback calls "once any progress is saved".

**D3 — Build stays static, adaptation is runtime.** Pages are generated Python templates; progress lives in localStorage. Any dynamic behaviour needs a `js-*` hook in the template first (edit `build.py`, rebuild, then extend `app.js`). The existing `render()` pipeline (`app.js:168-178`) is the single place to add new render functions. No new JS files, no dependencies.

**D4 — State changes are additive only.** The localStorage schema (`pawsitive-start-v2`, `app.js:13`) stays at `v: 1`. New optional fields (self-placement, tip dismissal) are filled by `normalize()` (`app.js:43-53`) which already back-fills missing `days`/`notes` — same pattern, no migration, old backups still import.

**D5 — Tone guardrails (from `ui-ux-research.md` and validation history).** No loss framing ("still remaining" → "next up"), no FOMO or time-limited awards, no auto-advance, "stop here" is always a first-class choice with equal visual weight, streaks stay guilt-free. Everything celebratory respects `prefers-reduced-motion`.

**D6 — Every WP ships the same way.** Bump `?v=` on changed assets (`build.py:174-175`, hand-edited), run `data.py` + `build.py` (SW cache name regenerates from the digest, `build.py:806-810`), then a seeded-state walkthrough (fresh / mid-progress / stage-complete / course-complete), 300–390 px mobile pass, rendered dark mode, WCAG AA, reduced motion, Lighthouse, and the internal link check. This is the documented validation process (`validation.md`) — new work lands as "Round 6".

**D7 — Manifest budget.** `window.PS` is inlined into all 43 pages (`data.py:100-110`, injected at `build.py:105-107`). Additions use the existing single-letter style and only fields actually consumed. Anything larger (e.g. full tip texts) should be reconsidered — see WP2.

---

## 3. Work packages

### WP0 — Foundations: state helpers, shared "next", toast fix

**Goal.** The small shared pieces three other packages depend on, plus one real bug.

**Scope.**
1. `hasProgress()` in `app.js` (per D2). Use it nowhere yet, or only internally; WP1/WP2 consume it.
2. `nextUp(fromSlug?)` in `app.js`: next unmastered slug in `PS.slugs` order (from `fromSlug` when given, else from the top); `null` when the course is complete (per D1).
3. Fix the toast overwrite bug: `setMastered()` triggers `celebrateStage()` (`app.js:136-144`, toast "Stage complete: …"), but the click handler immediately calls `showToast("Mastered. Small wins add up.")` (`app.js:686`), overwriting it in the same tick — the stage-complete toast is effectively never seen. Either give `showToast` a minimal queue/priority, or (simpler, and better UX) render stage completion as a banner on the master panel / stage hero instead of a toast, keeping the toast for the mastery acknowledgement.
4. While touching `renderToday()`: remove the dead `m.tm` reference (`app.js:282` — `tm` is not in the manifest; either add `tm` (minutes) to manifest `ex` entries, which WP5's "Next up" card can reuse, or delete the branch and fix the stale header comment at `app.js:7`).

**Acceptance.** `hasProgress()` true exactly when progress exists (unit-test by inspection across seeded states, incl. after a reset); mastering the last exercise of a stage visibly announces the stage completion; no dead code left.
**Effort.** S (half a day incl. validation). **Dependencies.** none. **Risks.** none significant.

---

### WP1 — Adaptive home: hero collapses once progress exists

**Goal.** One screen tall is enough for daily use; the onboarding hero is an empty-state treatment, not permanent chrome. (Feedback 1; preserves feedback 5's first-run CTA.)

**UX design.**
- **Zero progress (first open, or reset):** today's layout, unchanged: hero → Today card ("Start exercise" + "See the full course") → ring panel → practice row → stage list → "How this works" → rules callout. The new-user experience the feedback explicitly wants to keep.
- **Any progress (per D2):**
  - Hero section (`home-head`, `build.py:233-237`) and the "How this works" principles block (`build.py:270-271`) are hidden; the static rules callout moves behind a `<details>` or into the collapsed strip.
  - A compact **"welcome back" strip** (one line, ~56–64 px) replaces them: small overall ring (reuse `.ring`, it scales) + "Stage N · X/33 mastered · Y practice days this week" + **"Saved on this device ✓"**. Keeping the storage-honesty promise in the strip is non-negotiable: `ui-ux-research.md:69` requires it "in the hero area, not a footnote" — the strip *is* the hero once collapsed.
  - Returning order: strip → Today card (now reading "Continue: <exercise>") → tip of the day (WP2 slot) → practice row → stage list. One tall block (Today card), everything else secondary — the "one daily item" principle the research already commits to (`ui-ux-research.md:20`, Headspace/Calm pattern; the Headspace stacked-home redesign is the documented anti-pattern).
  - The strip links to the overview (WP3) for feedback 5's "place myself" need.

**Technical approach.**
- Add a `js-home-hero` hook (or `data-mode` attribute on `<body>`/`<html>` of `index.html` only) in `home_body()` (`build.py:224-278`); new `renderHomeMode()` called from `render()`; toggling uses the existing `[hidden] { display:none !important }` rule (`site.css:115`).
- **Flash/CLS problem:** `app.js` is `defer`, so a visible hero collapses after parse on every returning visit — one layout shift per home load. Recommended fix: a tiny generated inline script in `index.html`'s `<head>` (precedent: the `window.PS` manifest is already an inline script, `build.py:105-107`) that reads `localStorage["pawsitive-start-v2"]` directly, computes the same derived check, and sets `data-home="returning"` on `<html>` before first paint. `app.js` remains the source of truth; the inline check is ~10 duplicated lines and gets listed as a Round-6 validation invariant (must match `hasProgress()` exactly). Wrap in try/catch (private-mode localStorage throws; on failure fall back to intro mode — correct, since no-JS/no-storage users cannot have saved progress). CSS keys off `[data-home="returning"]`. Simpler fallback if the duplication is rejected: accept the collapse shift and measure it in validation (Lighthouse CLS budget).
- New compact-strip markup generated in `home_body()` with `hidden` default + `js-strip-*` hooks filled by render functions that already exist (`renderScore`, `renderStreak` data is one function call away).
- No state or schema changes.

**Acceptance criteria.** Fresh profile: identical to today. Profile with one checked step: hero gone, strip present with correct counts, storage line visible, Today card still the first interactive block. No-JS: full intro layout (correct — hero is the right treatment for a user who cannot have progress). 300 px no horizontal overflow; dark mode; CLS measured and documented.
**Effort.** M (1–2 days incl. validation). **Dependencies.** WP0 (`hasProgress`). **Risks.** The inline-script duplication (D3 exception) must be documented or dropped; hiding the hero changes the no-JS story slightly (acceptable, argued above).

---

### WP2 — Tip of the day

**Goal.** Surface the golden rules as a rotating one-liner on the home page, only for returning users. (Feedback 3.)

**UX design.**
- A `.callout.tip`-styled card (existing component, `site.css:836-856`) directly under the Today card — in the slot vacated by "How this works" (it must *replace* home content, not add height; WP1 interplay).
- One tip per day, one or two sentences max, always phrased as "try / good to know", never "you missed / you should have" (D5, guilt-free tone).
- Each tip links to its source anchor on `golden-rules.html` ("Why this helps →").
- Contextual bias: prefer tips relevant to the user's current stage (the stage containing `nextUp()`), falling back to general golden rules. This keeps tips feeling curated rather than random.
- Shown **only** when `hasProgress()` — on first open, nothing renders, not even an empty card (gate, don't placeholder).

**Technical approach.**
- Content: new `TIPS` list in `build/data_rules.py` (same shape family as `HOW_IT_WORKS`: `{t, ref, st}` — text, golden-rules anchor, optional stage). ~25–40 tips written from existing rules content (10 golden rules, 10 stress signals, 7 happy signals, don'ts, house rule, gear…). No new claims: tips are restatements of reviewed content, so no new safety surface — anything touching food/guarding/water must still be flagged for a Round-2-style content check.
- Selection is **deterministic by local date** (`day-of-epoch % pool.length` within the stage-relevant subset): same tip all day, works offline, reshuffle-free, and needs **zero state**. A seen-list + dismissal would add state for little benefit; if wanted later, add `tips` to the schema via `normalize()` back-fill (D4) — not in v1.
- Rendering: `js-tip` hook in `home_body()`, `hidden` by default; new `renderTip()` in the `render()` pipeline; date math reuses `today()` (`app.js:81-84`).
- Manifest: do **not** inline tip texts into `window.PS` (D7 — it would bloat all 43 pages). Instead build a tiny `tips.js`-style JSON script only in `index.html` (one page, one inline `<script type="application/json">`, same pattern as the session data on exercise pages, `build.py:660`), or extend the manifest with a compact index only if the tips list stays small. Prefer the single-page injection.

**Acceptance criteria.** First open: no tip card. With progress: one tip, stable across reloads, links to the right anchor, respects reduced-motion (it's static text — trivially yes). Content review sign-off for the tip list. No measurable Lighthouse regression on other pages (they must not carry tip data).
**Effort.** S for code, M overall (tip writing + content review dominates). **Dependencies.** WP0 (`hasProgress`), WP1 (slot on home). **Risks.** Content drift from the rules page (mitigated: tips reference rules by anchor, generated from the same data).

---

### WP3 — Course page becomes the overview / achievements screen

**Goal.** "What I've completed and what's left," game-like but guilt-free, and a map new users can place themselves in. (Feedback 4 and the overview half of 5.)

**UX design.** Enhance `course.html` rather than adding a fifth tab (the tab bar has 4 tabs today; a 5th changes every page — see audit gotchas; the Course tab already navigates here and the Today card already links it).
- **"You are here" header:** overall ring + "Stage N · X of 33 · next up: <exercise>" (from `nextUp()`), with the current stage tile visually marked.
- **Overlapping timeline, not a strict ladder:** stage tiles show their time windows from `STAGE.when` (already in data, already in the manifest as `w` — currently unused by `app.js`). Stage 1 "days 1–3", Stage 2 "days 3–14", Stage 3 "weeks 2–5"… rendered so the overlap is visible. This single change addresses feedback 2's *mental model* cheaply and doubles as the new-user placement view.
- **Per-stage tiles** (extend the existing `.course-stage` cards, `build.py:282-311`): "3 of 6 done · next up: <title>" link, binary "Complete" stamp when all exercises are mastered (the existing `badge-done`), nothing that counts down or frames the rest as debt. Language: "done", "next up", "not started yet" — never "remaining".
- **Milestones section** (the achievements flavour): a short, meaningful list, computed live from existing state — e.g. *First exercise mastered*, *Stage 1 complete — decompression done*, *Seven practice days logged*, *Halfway there (17 of 33)*, *Stage complete ×N*, *Course complete*. Anti-patterns deliberately avoided (from the research in §6): no badge wall (no per-exercise awards), no points, no time-limited or comparative awards, no counts that visibly go down on undo. Milestones are computed live (like today's course-complete card) rather than persisted history — simpler, honest, and undo already silently removes stage-complete states today.
- Stage-complete celebration stays where `ui-ux-research.md:57` put it: stage completion only, reduced-motion aware — now actually visible thanks to WP0's toast fix, plus the existing `.stage-banner` on stage pages.

**Technical approach.**
- `course_body()` rebuild in `build.py` (static shells + `js-*` hooks); new `renderCourse()` (or extend `renderStageCards()`, `app.js:231-236`) in the `render()` pipeline. Reuse `data-progress` hooks — `renderProgressBars()` (`app.js:195-208`) already fills any `[data-progress="all"]` / `"N"` element, so rings, bars and segs come for free.
- Milestones: pure functions over existing state (`isMastered`, `stageSlugs`, `state.days`, `Object.keys(state.notes)`) — no schema change. Titles/copy static in the template, `.is-earned` toggles at runtime.
- "You are here": current stage = stage of `nextUp()` (or the user's self-placement once WP4 lands).
- No new page → no `PRECACHE` change and no link-checker regex extension needed (`build.py:796-816`). Home strip (WP1) and stage pages link to `course.html`.
- Optional: keep the milestone markup componentized so a future dedicated "achievements" screen, if ever wanted, is a re-skin.

**Acceptance criteria.** A mid-progress user can answer "what have I done / what's next" in one glance; a fresh user sees the whole map with time windows and the CTA still reachable; WCAG AA on all new contrast/text; works from `file://` and offline (all data already client-side).
**Effort.** M. **Dependencies.** WP0 (`nextUp`); coordinate with WP1 (strip link). **Risks.** Copy drift toward debt-framing — keep language list above as the review checklist.

---

### WP4 — Guided flexibility: options within structure

**Goal.** Take the course one step toward improvisation without making it a free-for-all. (Feedback 2.) This is the largest and most design-sensitive package — it changes *content model*, not just UI.

**UX design — "recommended path + bounded choice":**
1. **Bounded choice in the Today card.** Primary action stays the recommended next (`nextUp()`). Under it, up to **two** alternative chips from the *current stage only* — "Also good today: [Leash basics] [Settle on a mat]" — each with a one-line "good when your dog…" hint. Cap at two (Hick's law / choice overload; Duolingo's own path research shows unbounded choice diverges learners). None are hidden; none are locked.
2. **Core vs supporting exercises.** Mark each exercise `core` or supporting. Stage pages group or tag rows so users see what's essential vs what can wait. Jumping supporting exercises is explicitly fine in copy.
3. **Self-placement ("Where is your dog right now?").** An optional, editable, one-question setting (three answers: "Just home" → Stage 1, "Settling in" → Stage 2–3, "Out and about" → Stage 4+) that offsets `nextUp()`'s starting point. Shown once, softly, when progress starts — never at first open (don't tax the stressed first-time user), also available in Settings. It must **never** hide or skip Stage 1 safety content; the stage list always shows everything.
4. **Safety rails stay ordered.** Exercises that are genuinely sequential in real training (the alone-time ladder with its stop criteria, the bowl pre-screen — the items validation Rounds 2–4 kept ordered) get a `seq` flag: the UI shows "do X first" with the reason, as advice, never as a lock (`ui-ux-research.md:51`: "locking = rage per reviews").
5. **Copy changes.** "Work through the stages in order" (`build.py:265`) and "Do these in order when you can" (`build.py:512`) become overlap-aware: "Stages build on each other — the order helps most, and starting the next stage while finishing the last is normal."

**Technical approach.**
- Content metadata in `data_stage1..6.py`, validated in `data.py:35-83`: optional `tags` (small controlled vocabulary, e.g. calm / leash / alone-time / home-life / bonding / handling), `core` (bool, default true), `seq` (bool). Schema validation keeps the vocabulary closed (a typo fails the build, matching the repo's `data.py` style).
- Manifest: extend `PS.ex[slug]` with only what's consumed — e.g. `f` (first tag) and `core` — keeping D7's budget. The chips need title + tag + href, all derivable.
- State: optional `focus: { stage: n }` back-filled by `normalize()` (D4 — no `v` bump, old backups still import). `nextUp()` consumes it. Settings gets the placement control (mirrors the existing settings-card pattern, `build.py:386-460`).
- Today card: `js-focus-alt` hook rendered by `renderToday()`'s extension; chips reuse `.chip` / `.btn btn-quiet` styles.
- Stage pages: `core`/`seq` presentation is build-time (grouping or badges in `stage_body()`, `build.py:464-520`) — no runtime cost.
- The overlapping timeline in WP3 is the mental-model half of this package and lands first.

**Acceptance criteria.** A user whose dog is advancing faster in leash work than alone-time can follow that thread in ≤2 taps from home without ever seeing a lock or a warning; a novice user who touches nothing still gets exactly today's linear experience; safety-flagged items always show their "do X first" reason; content review (trainer) signs off the core/seq/tags assignment for all 33 exercises.
**Effort.** L (the trainer review of tag/seq assignments is the long pole). **Dependencies.** WP0 (`nextUp`), benefits from WP3 (timeline). **Risks.** Scope creep into a full "custom plan builder" — explicitly out of scope (§5); tag vocabulary growing — keep closed and small.

---

### WP5 — Next-step flow after completing an exercise

**Goal.** Never dead-end a mastery moment. (Feedback 6.)

**UX design.**
- When the master panel flips to done (`.master-panel.done`, `site.css:903`), it gains the continuation UI inline — no modal, no redirect:
  - Primary: **"Next up: <title> →"** (the `nextUp()` exercise — skips already-mastered items).
  - Secondary: "Back to Stage N".
  - Equal-weight quiet option: **"Done for today"** (D5 — stopping is a first-class choice, not a failure).
- If the next exercise crosses a stage boundary, the panel says so: "That's Stage N complete — a great stopping point." with "Start Stage N+1" / "Done for today". (Celebration restraint per `ui-ux-research.md:57`: stage completion is the only celebration moment.)
- The session-complete panel inside the guided-session dialog (`build.py:651-656`) gets the same next CTA, so both completion paths lead somewhere.
- The static footnav stays as-is (sequence navigation, relabelled "Next in the stage" per D1).

**Technical approach.**
- Extend `renderExercisePage()` (`app.js:309-361`): fill a `js-next-up` link + title in the master panel and session-complete panel when `isMastered(slug())`. Template hooks added in `exercise_body()` (`build.py:625-630` area).
- Href building on exercise pages must respect subpath safety: exercise pages sit one level deeper (`P = "../"`); resolve via the `data-root` already read by `app.js` for the service worker (`app.js:14-16`) instead of hardcoding `../`. This becomes a Round-6 invariant (no absolute paths — `README.md:49-52`).
- Reuses WP0's `nextUp()` and the toast/banner fix. If `nextUp()` is `null` (course complete), the panel shows the existing course-complete treatment ("Revisit the course").
- Optionally surface the next exercise's `time` ("Next up: Sit-stay · ~5 min") — which is the good reason to add `tm` to the manifest in WP0 instead of deleting the dead reference.

**Acceptance criteria.** Completing an exercise offers exactly one obvious next action plus an honest stop; the offered next never points at an already-mastered exercise; both completion paths (master button, session dialog) work; announcement via `.js-announcer` for screen readers; reduced motion respected.
**Effort.** S–M. **Dependencies.** WP0 (`nextUp`, toast fix). **Risks.** Pressure-to-continue feel — mitigated by the equal-weight stop option and no auto-advance (§5).

---

### WP6 — Validation, docs, and housekeeping (continuous)

**Goal.** Keep the repo's own bar (`validation.md`) and fix the small drifts the audit surfaced.

- **Every WP:** rebuild (`python3 data.py && python3 build.py`), bump `?v=` in `build.py:174-175` when `app.js`/`site.css` change (hand-edited — the SW cache name does regenerate, `build.py:806-810`, but HTTP-cached stale bytes are a real failure mode), seeded-state walkthrough, 300–390 px + dark + WCAG AA + reduced motion, Lighthouse, link check. Record as **validation Round 6**.
- **Known drifts to fix along the way:** stale microcopy in `ui-ux-research.md:63` ("6–8 weeks" — corrected to 8–12 in `validation.md:37` but never backported); README "about 10 minutes a day" vs `build.py:255` "not a strict ten-minute clock" (reconcile the claim); home meta description hard-codes "33 short exercises" (`build.py:761`) vs `{TOTAL}` in the lede.
- **Offline check:** the audit found PRECACHE lists CSS/JS without `?v=` while pages request versioned URLs (`build.py:796-804` + `caches.match` semantics), so the precache entries miss — verify offline first-load after any asset bump and consider precaching the versioned URLs instead.
- **Docs:** update `ui-ux-research.md` with the new patterns (it is the design source of truth) and `README.md`'s project layout / progress notes for any new behavior.
- **Link checker:** if any WP adds a top-level page (current design: none do), extend the regex at `build.py:814-816` so the build actually checks the new links.

**Effort.** Continuous; ~half a day per WP plus one final consolidated round.

---

## 4. Sequencing

| Phase | Packages | Feedback covered | Rationale |
|---|---|---|---|
| 1 — quick wins | WP0 → WP5, then WP1 | 6, then 1 (+5's first-run preserved) | WP0 is tiny and unblocks everything; WP5 is small, self-contained, and the most daily-felt friction after the home page; WP1 is the biggest daily-use win |
| 2 — visibility | WP2, WP3 | 3, 4, 5 | WP2 slots into the space WP1 frees; WP3 makes the overview a real destination and sets up WP4's mental model |
| 3 — flexibility | WP4 | 2 | Largest scope, content decisions + trainer review needed; ship the visible value first, design this one carefully |

WP6 runs with every phase. Nothing here blocks a deploy in between — each WP is independently shippable through the existing GitHub Pages flow.

---

## 5. Explicitly out of scope / rejected

- **Full free ordering or a "build your own plan" mode.** Duolingo's tree→path evidence (learners diverge, take longer to converge) plus our novice, safety-sensitive audience. Bounded choice (WP4) is the deliberate middle.
- **Badge walls, points, leaderboards, comparative stats.** Vanity awards and social comparison contradict the guilt-free positioning; research on gamification shows motivation gains without learning gains, and loss-framed counters are the classic dark pattern.
- **Activity-ring clones per stage.** Apple's rings are (a) Apple's, (b) already used once on this site for the overall ring — reuse the existing ring and the "Complete" stamps instead.
- **Auto-advance / "one more rep" nudges after completion.** Engagement-maximizing patterns this product explicitly avoids; the next CTA is a tap, never a timer.
- **Calendar-based auto-placement** ("you adopted 3 weeks ago, so…"). The 3-3-3 clock varies per dog (`dog-training-research.md:25`); placement is self-declared and editable.
- **Accounts, sync, or a server.** Product premise: no account, nothing leaves the device.
- **A fifth bottom tab.** Layout cost on every page for a destination `course.html` already serves.
- **Hard locks anywhere.** `ui-ux-research.md:51` — "locking = rage per reviews". Safety ordering is advice with reasons, never a gate.

---

## 6. Sources worth citing (load-bearing subset)

**From the repo:** `ui-ux-research.md` (one daily item, soft gates, guilt-free streaks, celebration restraint, storage honesty), `dog-training-research.md` (overlapping stage windows :58-63, 3-3-3 variance :25, difficulty adaptation :9), `validation.md` (round process, seeded states, Round 2 safety review).

**External:**
- Duolingo — "The science behind the new home screen design" (path vs tree): https://blog.duolingo.com/new-duolingo-home-screen-design
- Duolingo whitepaper (tree vs path outcomes): https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_language_read_listen_write_speak_2024.pdf
- Khan Academy — skill progress & unit views: https://support.khanacademy.org/hc/en-us/articles/47078681852045
- Apple HIG — Offering help / tips: https://developer.apple.com/design/human-interface-guidelines/offering-help
- Apple HIG — Activity rings (why not to clone them): https://developer.apple.com/design/human-interface-guidelines/activity-rings
- Carbon Design System — Empty states: https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states
- NN/g — Instructional overlays / coach marks: https://www.nngroup.com/articles/mobile-instructional-overlay
- Goal-gradient & badge effects (ScienceDirect): https://www.sciencedirect.com/science/article/abs/pii/S0148296318303060 · Cornell badges paper: https://www.cs.cornell.edu/home/kleinber/www13-badges.pdf
- SDT app-feature taxonomy: https://www.sciencedirect.com/science/article/pii/S1071581920300513
- Gamified feedback study (points/bars ≠ learning): https://www.sciencedirect.com/science/article/pii/S0747563225003097
- Streak loss-aversion anti-pattern: https://www.codexical.com/posts/2026-06-21-streak-mechanics-loss-aversion-design
- Success-state pattern (next action attached to success): https://ui-patterns.com/patterns/SuccessState · Set completion: https://ui-patterns.com/patterns/set-completion
- Headspace "after the basics" (single-item home): https://www.headspace.com/articles/after-headspace-basics

*(Web sources were gathered by a research pass and cited from search-result level; treat URLs as leads to verify when writing user-facing copy claims, not as copy-paste material.)*

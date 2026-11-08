# 🐾 Pawsitive Start

A free, no-account website that guides **new dog owners who just adopted from a shelter or rescue** through educating and training their dog — as a course of **6 stages and 33 short exercises**, about 10 minutes a day.

## Quick start

Option A — just look around:
- Open `site/index.html` in any browser. Progress saving (localStorage) works from `file://` too.

Option B — recommended (proper URLs, faster loads):
```bash
cd site
python3 -m http.server 8000
# → http://localhost:8000
```
No Node, no dependencies, no build tooling to install — Python 3.9+ is the only runtime.

## Rebuilding the site

The 43 HTML pages are generated from Python data modules:

```bash
cd build
python3 data.py      # validates the whole course schema; exits non-zero with a fix list
python3 build.py     # writes index, golden-rules, 6 stage pages, 33 exercise pages
                     # + runs an internal link check
```

- Course content lives in `build/data_stage1.py` … `build/data_stage6.py` (33 exercises) and `build/data_rules.py` (golden rules, don'ts, stress signals, gear, pro-help, learn links).
- `build/data.py` aggregates + schema-validates and exports the `MANIFEST` injected into every page as `window.PS`.
- Page templates live in `build/build.py` (shells, topbar/footer, home/rules/stage/exercise bodies).

## Project layout

```
pawsitive-start/
├── build/            # generator + content data (edit these, then rebuild)
├── site/             # generated static site — deploy anything inside as-is
│   ├── assets/       # site.css design system, app.js progress engine
│   ├── exercises/    # 33 exercise pages
│   ├── stage-*.html  # 6 stage pages
│   ├── index.html    # home / plan
│   └── golden-rules.html
└── resources/        # research briefs + validation log (not part of the site)
```

## How progress tracking works

- All state is stored in the browser's `localStorage` (key `pawsitive-start-v2`) — no account, no server, nothing leaves the device.
- Per exercise: step checkboxes, mastery-criteria checkboxes, "mastered" flag, notes, timers.
- Global: overall % ring, per-stage segmented bars, guilt-free practice-day streak, and **Export / Import backup** buttons in the footer for moving between devices.
- Clearing your browser data resets the course. There's also a "Reset progress…" button in the footer.

## Content principles

- **Reward-based only.** No prongs, chokes, shocks or dominance games — aligned with AVSAB's humane-training position statement.
- **Rescue-first sequencing.** Stage 1 is pure decompression (the ASPCA "3-3-3" pattern); keeper-skills like alone-time training and consent handling get their own stage.
- **Plain language.** Every exercise: goal → why → 5–8 steps → mastery criteria → common mistakes → troubleshooting.
- Selected source links appear on the Golden Rules page and on individual exercises (ASPCA, AVSAB, VCA, AKC, Karen Overall, and more).

## Validation

`resources/validation.md` logs the validation rounds (build/link checks, browser walkthrough, expert trainer review of content, Lighthouse a11y/SEO audits). Research briefs behind the course: `resources/dog-training-research.md` and `resources/ui-ux-research.md`.

---

Made with kindness for new dog parents. Not a substitute for a vet or a certified behavior professional — the site tells you when to call one.

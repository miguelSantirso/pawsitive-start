# 🐾 Pawsitive Start

A free, no-account website that guides **new dog owners who just adopted from a shelter or rescue** through educating and training their dog — as a course of **6 stages and 33 short exercises**, a few calm minutes a day (not a strict clock).

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

## Deploying (GitHub Pages)

The site is live at **https://miguelsantirso.github.io/pawsitive-start/**
source repo: `github.com/miguelSantirso/pawsitive-start`.

- Deploys are automatic: every push to `main` runs `.github/workflows/deploy.yml`,
  which publishes the contents of `site/` as a GitHub Pages artifact (~30s, no
  npm/pip build step runs on CI — build locally first, commit the output).
- Manual deploy: repo → Actions tab → "Deploy to GitHub Pages" → Run workflow.

### Routine

```bash
cd build
python3 data.py     # validate content; exits non-zero with a fix list
python3 build.py    # regenerate site/ (+ link check)
git add -A && git commit -m "..." && git push origin main   # auto-deploys
```

### Deploy troubleshooting (for future agents)

- If a run fails in `actions/deploy-pages@v4` with
  `Failed to create deployment (status: 404)`, Pages is not enabled on the repo
  yet (e.g. brand-new repo). Enable it once with:
  `gh api -X POST /repos/miguelSantirso/pawsitive-start/pages -f build_type=workflow`
  then `gh run rerun <run-id>`. This is the GitHub Pages "Source: GitHub Actions"
  mode; do not switch the repo to "Deploy from a branch" in settings.
- After pushing, verify liveness: `curl -s -o /dev/null -w "%{http_code}\n"
  https://miguelsantirso.github.io/pawsitive-start/` (expect 200).
- Runbook notes: the site must stay subpath-safe. All asset/script paths are
  relative (`../assets/site.css`, `data-root="../"` on the script tag);
  `manifest.webmanifest` uses `start_url`/`scope: "./"`; the service worker URL
  and scope are derived from `data-root` + `location.href` in
  `site/assets/app.js`. A new absolute (`/...`) path or a repo rename breaks
  this. Do not add absolute links.
- Changing `app.js` or `site.css` requires bumping the `CSS_V` / `JS_V` constants
  in `build/build.py` (they feed both the `?v=` query strings in the generated
  pages and the service-worker precache list, which must match exactly);
  the SW cache name constant also changes per build.

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
├── .github/workflows/  # deploy.yml — auto-publishes site/ to GitHub Pages
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

- All state is stored in the browser's `localStorage` (key `pawsitive-start-v2`, schema `v: 1`) — no account, no server, nothing leaves the device.
- Per exercise: step checkboxes, mastery-criteria checkboxes, "mastered" flag, notes, timers.
- Global: overall % ring, per-stage segmented bars, and **Export / Import backup** buttons in the footer for moving between devices.
- Clearing your browser data resets the course. There's also a "Reset progress…" button in the footer.

### Round 6 — adaptive returning-user behaviour

The home page and completion flows adapt at runtime to saved progress; every page stays fully static and no-JS still works.

- **Adaptive home.** With no progress, home shows the full onboarding hero. Once any progress exists (a checked step or criterion, a mastered exercise, or a note), the home adapts to a simpler returning view. The check runs in a tiny inline script in `index.html` before first paint to avoid a flash, and mirrors `hasProgress()` in `app.js` (a documented validation invariant).
- **Tip of the day.** Also returning-only: one short tip per local calendar day, picked deterministically from `build/data_rules.py` (`TIPS`), biased toward the user's current stage and linking to its source anchor on the golden-rules page. Tip data is injected into `index.html` only (not the shared `window.PS` manifest).
- **Course overview.** `course.html` doubles as the "you are here" map: overall ring, current stage, per-stage "next up" links, an overlapping-stage timeline, and live milestones (no badge wall, no counts that frame undone work as debt). The topbar score link points here.
- **Next up after mastery.** Marking an exercise mastered offers "Next up: …" (or "Start Stage N" at a stage boundary) plus an equal-weight "Done for today". The static exercise footnav stays sequence order and is labelled "Next in the stage".
- **Optional self-placement.** A skippable "Where is your dog right now?" prompt (home, once, only after progress exists) and the same control in Settings offsets the suggested starting point. It is stored locally (`focus`), never hides Stage 1 content, and never locks anything.

## Content principles

- **Reward-based only.** No prongs, chokes, shocks or dominance games — aligned with AVSAB's humane-training position statement.
- **Rescue-first sequencing.** Stage 1 is pure decompression (the ASPCA "3-3-3" pattern); keeper-skills like alone-time training and consent handling get their own stage.
- **Plain language.** Every exercise: goal → why → 5–8 steps → mastery criteria → common mistakes → troubleshooting.
- Selected source links appear on the Golden Rules page and on individual exercises (ASPCA, AVSAB, VCA, AKC, Karen Overall, and more).

## Validation

`resources/validation.md` logs the validation rounds (build/link checks, browser walkthrough, expert trainer review of content, Lighthouse a11y/SEO audits). Research briefs behind the course: `resources/dog-training-research.md` and `resources/ui-ux-research.md`.

---

Made with kindness for new dog parents. Not a substitute for a vet or a certified behavior professional — the site tells you when to call one.

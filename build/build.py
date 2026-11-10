#!/usr/bin/env python3
"""Pawsitive Start — static site generator.

Usage:  python3 build/build.py

Generates the app shell, Today / Course / Rules / Settings pages, one page
per stage and exercise, the web app manifest and a service worker.
"""
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, BUILD)

import data_rules  # noqa: E402
import make_icons  # noqa: E402
from data import STAGES, EXERCISES, MANIFEST  # noqa: E402

BRAND = "Pawsitive Start"
TOTAL = len(EXERCISES)
# Cache-busting versions for the two hand-edited assets. Pages request these
# exact versioned URLs, and the service-worker precache must list the same
# ones (caches.match is exact-match, query string included) or the offline
# precache misses. Bump both whenever site.css / app.js change.
CSS_V = 19
JS_V = 17
EX_BY_SLUG = {row["ex"]["slug"]: row for row in EXERCISES}
TAG_LABELS = {
    "calm": "Calm",
    "leash": "Leash",
    "alone-time": "Alone time",
    "home-life": "Home life",
    "bonding": "Bonding",
    "handling": "Handling",
}


def tag_label(tag):
    return TAG_LABELS.get(tag, tag.replace("-", " ").capitalize())


def seq_advice(e):
    """Calm, advice-only 'do this first' line for sequential exercises (WP4)."""
    if not e.get("seq"):
        return ""
    reason = e.get("seq_reason", "")
    after = e.get("seq_after")
    if after and after in EX_BY_SLUG:
        return f'After {EX_BY_SLUG[after]["ex"]["title"]}: {reason}'
    if reason:
        return reason[0].upper() + reason[1:]
    return ""



def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- icons
ICONS = {
    "paw": (
        '<path d="M12 21c-3.3 0-5.8-1.9-5.8-4.6 0-2.1 1.7-3.4 3.3-4.1'
        '.9-.4 1.7-.8 2.5-.8s1.6.4 2.5.8c1.6.7 3.3 2 3.3 4.1'
        ' 0 2.7-2.5 4.6-5.8 4.6Z"/>'
        '<circle cx="6.2" cy="9.4" r="2.1"/><circle cx="10" cy="6.4" r="2.2"/>'
        '<circle cx="14" cy="6.4" r="2.2"/><circle cx="17.8" cy="9.4" r="2.1"/>'
    ),
    "today": (
        '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4'
        'M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'
    ),
    "book": (
        '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15.5H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>'
        '<path d="M4 18.5A2.5 2.5 0 0 1 6.5 16H20"/>'
    ),
    "shield": (
        '<path d="M12 3 5 6v5c0 4.5 3 8.2 7 10 4-1.8 7-5.5 7-10V6l-7-3Z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "sliders": (
        '<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/>'
        '<circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>'
    ),
    "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "chevron-right": '<path d="m9 5 7 7-7 7"/>',
    "check": '<path d="m5 12 5 5L20 7"/>',
    "play": '<path d="M8 5v14l11-7-11-7Z"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
    "upload": '<path d="M12 16V4M7 9l5-5 5 5M5 21h14"/>',
    "trash": '<path d="M4 7h16M9 7V4h6v3M6 7l1 14h10l1-14M10 11v6M14 11v6"/>',
    "install": (
        '<rect x="7" y="2" width="10" height="20" rx="2"/>'
        '<path d="M12 6v7M9.5 10.5 12 13l2.5-2.5"/>'
    ),
    "timer": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9 2h6"/>',
    "note": '<path d="M5 3h10l4 4v14H5V3Z"/><path d="M15 3v4h4M8 12h8M8 16h6"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/>',
}


def svg(name, cls=""):
    body = ICONS[name]
    klass = f' class="{cls}"' if cls else ""
    if name == "paw":
        return (f'<svg{klass} viewBox="0 0 24 24" aria-hidden="true" '
                f'fill="currentColor">{body}</svg>')
    return (f'<svg{klass} viewBox="0 0 24 24" aria-hidden="true" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round">{body}</svg>')


# ---------------------------------------------------------------- shell
SUBBAR = (
    '<div class="subbar-track" role="progressbar" '
    'aria-label="This exercise\'s progress" aria-valuemin="0" '
    'aria-valuemax="100" aria-valuenow="0">'
    '<div class="subbar-fill js-subfill" style="width:0%"></div></div>'
)

TABS = [
    ("index.html", "Today", "today", "home"),
    ("course.html", "Course", "book", "course"),
    ("golden-rules.html", "Rules", "shield", "rules"),
    ("settings.html", "Settings", "sliders", "settings"),
]


def manifest_script():
    payload = json.dumps(MANIFEST, ensure_ascii=False).replace("</", "<\\/")
    return "<script>window.PS=" + payload + ";</script>"


def tip_script():
    """Tip-of-the-day data, injected into index.html only (WP2 / D7).

    Tip texts deliberately stay out of window.PS so the other 42 pages do not
    carry them. Same inline JSON pattern as the session data on exercise pages.
    """
    payload = json.dumps(data_rules.TIPS, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/json" class="js-tip-data">{payload}</script>'


def home_mode_script():
    """Set data-home="returning" before first paint on the home page only.

    Round-6 validation invariant: this derived check MUST mirror hasProgress()
    in site/assets/app.js exactly (it is duplicated here to avoid a flash of
    the onboarding hero on returning visits). Ignore savedAt, ignore empty
    per-exercise records; any mastered exercise, any true step/criteria flag,
    any non-blank note, or any practice day means progress exists.
    """
    return '''<script>
(function () {
  try {
    var raw = localStorage.getItem("pawsitive-start-v2");
    if (!raw) return;
    var st = JSON.parse(raw);
    if (!st || typeof st !== "object" || st.v !== 1) return;
    if (!st.ex || typeof st.ex !== "object" || Array.isArray(st.ex)) return;
    function anyTrue(a) {
      if (!a) return false;
      for (var i = 0; i < a.length; i++) if (a[i]) return true;
      return false;
    }
    var key, inf;
    var notes = st.notes && typeof st.notes === "object" && !Array.isArray(st.notes) ? st.notes : {};
    var days = Array.isArray(st.days) ? st.days : [];
    for (key in st.ex) {
      if (!Object.prototype.hasOwnProperty.call(st.ex, key)) continue;
      inf = st.ex[key] || {};
      if (inf.m || anyTrue(inf.s) || anyTrue(inf.c)) {
        document.documentElement.setAttribute("data-home", "returning");
        return;
      }
    }
    for (key in notes) {
      if (Object.prototype.hasOwnProperty.call(notes, key) &&
          notes[key] && String(notes[key]).trim()) {
        document.documentElement.setAttribute("data-home", "returning");
        return;
      }
    }
    if (days.length) {
      document.documentElement.setAttribute("data-home", "returning");
    }
  } catch (e) {}
})();
</script>'''


def topbar(P, page, subbar=False, stage=None):
    # Returning mode hides the home #progress panel (WP1), so the score link
    # points at the course overview instead — meaningful for every mode.
    score = f'<a class="score js-score" href="{P}course.html#overview">0/{TOTAL} mastered</a>'
    if page == "exercise":
        return f'''<header class="topbar topbar-focus"><div class="topbar-inner">
<a class="backlink" href="{P}stage-{stage}.html">{svg("arrow-left")}<span>Stage {stage}</span></a>
{score}
</div>{SUBBAR if subbar else ""}</header>'''
    return f'''<header class="topbar"><div class="topbar-inner">
<a class="brand" href="{P}index.html"><span class="logo">{svg("paw")}</span><span class="brand-text">{BRAND}</span></a>
<div class="topbar-actions">
<a class="topbar-link" href="{P}course.html">Course</a>
<a class="topbar-link" href="{P}golden-rules.html">Rules</a>
{score}
</div></div></header>'''


def tabbar(P, page):
    current = "course" if page == "stage" else page
    items = []
    for href, label, icon, key in TABS:
        cur = ' aria-current="page"' if key == current else ""
        items.append(
            f'<a class="tab" href="{P}{href}"{cur}>{svg(icon)}<span>{label}</span></a>'
        )
    return f'<nav class="tabbar" aria-label="Main">{"".join(items)}</nav>'


def footer(P):
    return f'''<footer class="site-footer"><div class="inner">
<p class="brand-line">{BRAND}</p>
<p class="save-line js-save-note">Progress is saved in this browser, on this device. No account, nothing leaves your device.</p>
<p><span class="save-ind js-saved"></span></p>
<p class="small">A free course for people who just adopted a shelter or rescue dog. <a href="{P}golden-rules.html">Golden rules</a> · <a href="{P}settings.html">Settings &amp; backup</a></p>
<p class="small">Not a substitute for a vet or a certified behaviour professional. The course tells you when to call one.</p>
</div></footer>'''


def shell(title, desc, P, body, page, colorclass="", subbar=False,
          body_attrs="", stage=None, bare_title=False, extra_head=""):
    full_title = title if bare_title else f"{title} · {BRAND}"
    classes = " ".join(x for x in [colorclass, "" if page == "exercise" else "has-tabbar"] if x)
    tab = "" if page == "exercise" else tabbar(P, page)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f7f2e9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#171512" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{P}assets/icon-512.png">
<meta name="twitter:card" content="summary">
<link rel="manifest" href="{P}manifest.webmanifest">
<link rel="icon" href="{P}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{P}assets/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="{BRAND}">
<link rel="preload" as="font" type="font/woff2" href="{P}assets/fonts/fraunces.woff2" crossorigin>
<link rel="stylesheet" href="{P}assets/site.css?v={CSS_V}">
<script src="{P}assets/app.js?v={JS_V}" data-root="{P}" defer></script>
{manifest_script()}
{extra_head}
</head>
<body class="{classes}"{body_attrs}>
<a class="skip-link" href="#main">Skip to content</a>
<noscript><p class="noscript">This course works without JavaScript, but saving progress needs it switched on.</p></noscript>
{topbar(P, page, subbar, stage)}
<main class="shell" id="main">
{body}
</main>
{footer(P)}
{tab}
<div class="toast" role="status"></div>
<div class="visually-hidden js-announcer" aria-live="polite"></div>
</body>
</html>'''


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- shared bits
def stage_rows(P):
    rows = []
    for s in STAGES:
        n = s["num"]
        rows.append(f'''<li class="stage-row s{n} js-stage-card" data-stage="{n}">
<a class="stage-row-link" href="{P}stage-{n}.html">
<span class="stage-index">{n:02d}</span>
<span class="stage-body"><span class="stage-name">{esc(s["name"])}</span><span class="stage-meta">{esc(s["when"])} · {len(s["exercises"])} exercises</span><span class="stage-purpose">{esc(s["purpose"])}</span></span>
<span class="stage-progress"><span class="progress-row"><span class="segs" data-progress="{n}"></span><span class="progress-label js-prog-label"></span></span></span>
<span class="stage-chevron">{svg("chevron-right")}</span>
</a>
</li>''')
    return "\n".join(rows)


def principles():
    out = []
    for i, h in enumerate(data_rules.HOW_IT_WORKS, 1):
        out.append(f'''<div class="principle"><span class="n">{i:02d}</span><h3>{esc(h["t"])}</h3><p>{esc(h["d"])}</p></div>''')
    return f'<div class="principles">{"".join(out)}</div>'


# ---------------------------------------------------------------- Today
def home_body():
    # No-JS / pre-hydration fallback for the Today card: the first exercise.
    # With JS on, renderToday() replaces this instantly; with JS off it stays
    # true and useful instead of showing a spinner that never resolves.
    first_row = EXERCISES[0]
    first_ex, first_stage = first_row["ex"], first_row["stage"]
    first_href = f'exercises/{first_ex["slug"]}.html'
    first_meta = f'Stage {first_stage["num"]} · {esc(first_stage["name"])}'
    body = f'''
<section class="home-head">
<span class="kicker">For shelter &amp; rescue dog parents</span>
<h1>A calm start for <span class="squiggle">your new dog</span>.</h1>
<p class="lede">A step-by-step course for the first weeks after adoption: six stages, {TOTAL} short exercises, a few calm minutes at a time. No account and no experience needed.</p>
</section>

<section class="welcome-strip js-welcome-strip" aria-label="Welcome back" hidden>
<div class="ring" data-progress="all"><span class="hole"></span><span class="ring-num js-ring-num">0%</span></div>
<div class="strip-copy">
<p class="strip-line"><span class="js-strip-stage">Stage 1</span> · <span class="js-strip-mastered js-score">0/{TOTAL} mastered</span> · <span class="js-strip-days">0 practice days this week</span></p>
<p class="strip-sub"><span class="js-strip-save strip-save">Saved on this device ✓</span> · <a href="golden-rules.html">Rules</a></p>
</div>
<a class="strip-link" href="course.html" aria-label="Course overview"><span>Course overview</span>{svg("chevron-right")}</a>
</section>

<section class="today-card js-focus" data-href="exercises/" aria-labelledby="today-title">
<div class="today-top"><span class="kicker js-focus-kicker">Today's focus</span><span class="today-meta js-focus-meta">{first_meta}</span></div>
<h2 class="today-title js-focus-title" id="today-title">{esc(first_ex["title"])}</h2>
<p class="today-text js-focus-text">{esc(first_ex["goal"])}</p>
<div class="today-actions">
<a class="btn btn-primary js-focus-link" href="{first_href}">{svg("play")} <span class="js-focus-link-text">Start exercise</span></a>
<a class="btn btn-quiet" href="course.html">See the full course</a>
</div>
<div class="focus-alt js-focus-alt" hidden>
<p class="focus-alt-lead">Also good today</p>
<div class="focus-alt-chips js-focus-alt-chips" role="list"></div>
</div>
</section>

<!-- WP4: soft, inline self-placement prompt. Shown only for returning users
     until answered, and never at first open. -->
<section class="placement-prompt js-placement-prompt" aria-labelledby="placement-h" hidden>
<h2 id="placement-h">Where is your dog right now?</h2>
<p class="placement-text">This only changes where we suggest you start. Every stage stays open, and Stage 1 is always worth a read — especially the first-week safety notes.</p>
<div class="placement-options">
<button type="button" class="btn btn-quiet js-placement" data-stage="1" aria-pressed="false">Just home</button>
<button type="button" class="btn btn-quiet js-placement" data-stage="2" aria-pressed="false">Settling in</button>
<button type="button" class="btn btn-quiet js-placement" data-stage="4" aria-pressed="false">Out and about</button>
</div>
<button type="button" class="btn btn-ghost js-placement-skip">Not sure — start at the beginning</button>
</section>

<!-- WP2: tip of the day (insert directly after the Today card). WP6: the
     js-tip-slot wrapper reserves the card's space before the deferred app.js
     hydrates, so the card appearing doesn't shift the page (see .tip-slot in
     site/assets/site.css). -->
<div class="tip-slot js-tip-slot">
<section class="callout tip tip-card js-tip" aria-labelledby="tip-h" hidden>
<h3 id="tip-h">Try this today</h3>
<p class="tip-text js-tip-text"></p>
<a class="tip-link js-tip-link" href="golden-rules.html"><span>Why this helps</span> {svg("arrow-right")}</a>
</section>
</div>
{tip_script()}

<section class="progress-panel home-progress" id="progress" aria-labelledby="progress-h">
<div class="ring" data-progress="all"><span class="hole"></span><span class="ring-num js-ring-num">0%</span></div>
<div class="progress-copy">
<h2 id="progress-h" class="kicker">Your progress</h2>
<p class="score-line js-score">0/{TOTAL} mastered</p>
<div class="progress-row"><div class="progress" data-progress="all"><div class="progress-fill js-fill"></div></div><span class="progress-label js-prog-label"></span></div>
<p class="small">The core stages take most owners 8–12 weeks; Stage 6 continues into months 3–6. Plan for a few short sessions a day plus walks — not a strict ten-minute clock.</p>
</div>
</section>

<div class="practice-row">
<button type="button" class="btn btn-quiet js-streak">I practised today</button>
<span class="streakline js-streakline"></span>
</div>

<div class="section-head"><h2>Your course</h2><a href="course.html">View all stages →</a></div>
<ol class="stage-list">
{stage_rows("")}
</ol>

<div class="home-principles">
<div class="section-head"><h2>How this works</h2></div>
{principles()}
</div>

<div class="callout tip home-rules-callout">
<h3>Read this once</h3>
<p>The <a href="golden-rules.html">golden rules</a> explain rewards, timing, body language and the 3-3-3 adjustment clock. Five quiet minutes there saves weeks of guesswork later.</p>
</div>
'''
    return body


# ---------------------------------------------------------------- Course
# Stage windows such as "Weeks 2–5" are normalised to a shared days scale for
# the static overlap timeline. A course "month" is four weeks, which keeps
# "Months 3–6" aligned with the end of "Weeks 6–12".
_WHEN_UNIT_DAYS = {"day": 1, "week": 7, "month": 28}


def when_span(when):
    """Return (start_day, end_day) for a stage window such as "Weeks 2–5"."""
    m = re.search(r"(day|week|month)s?\s+(\d+)\s*[–—−-]\s*(\d+)", when.lower())
    if not m:
        raise ValueError(f"Unrecognised stage window: {when!r}")
    unit, start, end = m.group(1), int(m.group(2)), int(m.group(3))
    factor = _WHEN_UNIT_DAYS[unit]
    return start * factor, end * factor


def course_body():
    spans = [when_span(s["when"]) for s in STAGES]
    max_day = max(end for _, end in spans)

    timeline = []
    for s, (start, end) in zip(STAGES, spans):
        n = s["num"]
        left = start / max_day * 100
        width = (end - start) / max_day * 100
        timeline.append(f'''<li class="timeline-row s{n}">
<span class="timeline-key"><span class="timeline-num" aria-hidden="true">{n:02d}</span><span class="visually-hidden">Stage {n} · {esc(s["name"])}</span></span>
<span class="timeline-track"><span class="timeline-bar" style="--start:{left:.2f}%;--len:{width:.2f}%"><span class="timeline-when">{esc(s["when"])}</span></span></span>
</li>''')

    cards = []
    for s in STAGES:
        n = s["num"]
        first = s["exercises"][0]
        cards.append(f'''<article class="course-stage s{n} js-stage-card" data-stage="{n}">
<div class="course-stage-head">
<span class="stage-index">{n:02d}</span>
<div><h2><a href="stage-{n}.html">{esc(s["name"])}</a></h2><span class="stage-meta">{esc(s["when"])} · {len(s["exercises"])} exercises</span><span class="stage-now">You are here</span></div>
<span class="badge-done">Complete</span>
</div>
<p class="stage-purpose">{esc(s["purpose"])}</p>
<div class="progress-row"><div class="segs" data-progress="{n}"></div><span class="progress-label js-prog-label"></span></div>
<div class="stage-foot">
<span class="stage-done-line js-stage-done">Not started yet</span>
<span class="stage-next-wrap js-stage-next-wrap"><span aria-hidden="true"> · </span><span class="stage-next-label">next up:</span> <a class="stage-next js-stage-next" href="exercises/{esc(first["slug"])}.html"><span class="js-stage-next-title">{esc(first["title"])}</span></a></span>
</div>
<a class="stage-open" href="stage-{n}.html">Open stage {svg("arrow-right")}</a>
</article>''')

    first_row = EXERCISES[0]
    first_href = f'exercises/{first_row["ex"]["slug"]}.html'
    halfway = (TOTAL + 1) // 2
    body = f'''
<section class="page-head course-head">
<span class="kicker">The full course</span>
<h1>Six stages, one calm dog.</h1>
<p class="lede">Start with decompression, then build the everyday skills that keep a rescue dog safe, confident and at home.</p>
<div class="course-here" id="overview">
<div class="ring" data-progress="all"><span class="hole"></span><span class="ring-num js-ring-num">0%</span></div>
<div class="here-copy">
<p class="here-line"><span class="js-course-stage">Stage 1</span><span aria-hidden="true"> · </span><span class="js-course-count">0 of {TOTAL} done</span><span class="js-course-next-wrap"><span aria-hidden="true"> · </span>next up: <a class="js-course-next" href="{first_href}">{esc(first_row["ex"]["title"])}</a></span></p>
</div>
</div>
</section>

<section class="course-timeline" aria-labelledby="timeline-h">
<div class="section-head"><h2 id="timeline-h">How the stages overlap</h2></div>
<p class="section-note">Typical windows, not deadlines. Stages often overlap.</p>
<ol class="timeline-list">{"".join(timeline)}</ol>
<div class="timeline-axis" aria-hidden="true"><span></span><span class="timeline-axis-track"><span>Day 1</span><span>~3 months</span><span>~6 months</span></span></div>
</section>

<div class="section-head"><h2>Your stages</h2></div>
{''.join(cards)}

<section class="milestones" aria-labelledby="milestones-h">
<div class="section-head"><h2 id="milestones-h">Milestones</h2></div>
<ul class="milestone-list">
<li class="milestone" data-milestone="first"><span class="milestone-icon" aria-hidden="true"></span><span class="milestone-copy"><span class="milestone-title">First exercise mastered</span><span class="milestone-sub">The first small win — and the hardest part is starting.</span></span><span class="milestone-state">Not yet</span></li>
<li class="milestone" data-milestone="stage1"><span class="milestone-icon" aria-hidden="true"></span><span class="milestone-copy"><span class="milestone-title">Stage 1 complete — decompression done</span><span class="milestone-sub">Safety, sleep and routine are in place.</span></span><span class="milestone-state">Not yet</span></li>
<li class="milestone" data-milestone="seven-days"><span class="milestone-icon" aria-hidden="true"></span><span class="milestone-copy"><span class="milestone-title">Seven practice days logged</span><span class="milestone-sub">Any practice counts — there is no streak to lose.</span></span><span class="milestone-state">Not yet</span></li>
<li class="milestone" data-milestone="halfway"><span class="milestone-icon" aria-hidden="true"></span><span class="milestone-copy"><span class="milestone-title">Halfway there</span><span class="milestone-sub">{halfway} of {TOTAL} exercises done.</span></span><span class="milestone-state">Not yet</span></li>
<li class="milestone" data-milestone="stage-complete"><span class="milestone-icon" aria-hidden="true"></span><span class="milestone-copy"><span class="milestone-title">A full stage complete</span><span class="milestone-sub js-ms-stages">0 of {len(STAGES)} stages complete</span></span><span class="milestone-state">Not yet</span></li>
<li class="milestone" data-milestone="course"><span class="milestone-icon" aria-hidden="true"></span><span class="milestone-copy"><span class="milestone-title">Course complete</span><span class="milestone-sub">All six stages done. Revisit anything you like.</span></span><span class="milestone-state">Not yet</span></li>
</ul>
</section>

<div class="callout tip">
<h3>Before you start</h3>
<p>Read the <a href="golden-rules.html">golden rules</a> once — especially body language and the 3-3-3 clock. They make every exercise here easier.</p>
</div>
'''
    return body


# ---------------------------------------------------------------- Rules
def rules_body():
    rule_cards = "".join(
        f'''<div class="rule-card" id="rule-{i}"><span class="n">{i:02d}</span><h3>{esc(r["t"])}</h3><p>{esc(r["d"])}</p></div>'''
        for i, r in enumerate(data_rules.GOLDEN_RULES, 1)
    )
    dont_items = "".join(f"<li>{esc(d)}</li>" for d in data_rules.DONT_LIST)
    stress_items = "".join(f"<li>{esc(s)}</li>" for s in data_rules.STRESS_SIGNALS)
    happy_items = "".join(f"<li>{esc(s)}</li>" for s in data_rules.HAPPY_SIGNALS)
    gear_items = "".join(f"<li>{esc(g)}</li>" for g in data_rules.GEAR)
    help_items = "".join(f"<li>{esc(h)}</li>" for h in data_rules.HELP_SIGNALS)
    learn_items = "".join(
        f'''<li><a href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])} {svg("external")}</a><span class="blurb">{esc(l["blurb"])}</span></li>'''
        for l in data_rules.LEARN
    )
    body = f'''
<section class="page-head">
<span class="kicker">Read once, benefit constantly</span>
<h1>The golden rules.</h1>
<p class="lede">Every exercise in the course uses these principles. New to dogs? Read this page first and you will already be ahead of most owners.</p>
<ul class="quick-nav">
<li><a href="#how-dogs-learn">How dogs learn</a></li>
<li><a href="#signals">Body language</a></li>
<li><a href="#donts">What to skip</a></li>
<li><a href="#gear">Gear</a></li>
<li><a href="#help">When to get help</a></li>
<li><a href="#sources">Sources</a></li>
</ul>
</section>

<h2 id="how-dogs-learn">How dogs learn</h2>
<div class="rule-grid">{rule_cards}</div>

<h2 id="signals">Body language first</h2>
<div class="rule-grid">
<div class="rule-card"><h3>Stress signals</h3><ul>{stress_items}</ul></div>
<div class="rule-card"><h3>Relaxed signals</h3><ul>{happy_items}</ul></div>
</div>

<div class="callout tip">
<h3>The household signal rule</h3>
<p>{esc(data_rules.HOUSE_RULE)}</p>
</div>

<div class="callout warn" id="donts">
<h3>Ten things to skip entirely</h3>
<ul class="dont-list">{dont_items}</ul>
</div>

<div class="callout info" id="gear">
<h3>Your gear checklist</h3>
<p>Everything you need to run the whole course fits in one shopping trip:</p>
<ul class="needrow">{gear_items}</ul>
</div>

<div class="callout warn" id="help">
<h3>When to bring in a professional</h3>
<ul>{help_items}</ul>
<p>{esc(data_rules.HELP_WHO)}</p>
</div>

<h2 id="sources">Sources &amp; further reading</h2>
<p class="section-note">Stable links to the organizations and vets the course draws on.</p>
<details class="sources">
<summary>Open the full reading list</summary>
<ul class="learn-list">{learn_items}</ul>
</details>
'''
    return body


# ---------------------------------------------------------------- Settings
def settings_body():
    body = f'''
<section class="page-head">
<span class="kicker">Settings</span>
<h1>Your app, your data.</h1>
<p class="lede">Install the course for full-screen, offline use, and keep a backup of your progress. Everything stays on this device.</p>
</section>

<section class="settings-card">
<h2>Install on your phone</h2>
<p>Installed, the course opens like an app: full screen, its own icon, and it keeps working without a signal.</p>
<ol>
<li><strong>iPhone:</strong> open this page in Safari, tap Share, then <em>Add to Home Screen</em>.</li>
<li><strong>Android:</strong> open it in Chrome, tap the menu, then <em>Install app</em>.</li>
</ol>
<div class="install-actions"><button type="button" class="btn btn-primary js-install" hidden>{svg("install")} Install app</button></div>
<p class="small js-install-note">Use your browser menu if the install button is not shown.</p>
</section>

<section class="settings-card">
<h2>Where is your dog right now?</h2>
<p>This only changes where the Today card suggests you start. Every stage stays open, and Stage 1 is always worth a read — especially the first-week safety notes. Changes save automatically.</p>
<div class="placement-options settings-placement" role="group" aria-label="Where is your dog right now?">
<button type="button" class="btn btn-quiet placement-btn js-placement-set" data-stage="1" aria-pressed="false">Just home<span class="placement-sub">Stage 1</span></button>
<button type="button" class="btn btn-quiet placement-btn js-placement-set" data-stage="2" aria-pressed="false">Settling in<span class="placement-sub">Stages 2–3</span></button>
<button type="button" class="btn btn-quiet placement-btn js-placement-set" data-stage="4" aria-pressed="false">Out and about<span class="placement-sub">Stage 4 onwards</span></button>
<button type="button" class="btn btn-quiet placement-btn js-placement-set" data-stage="" aria-pressed="false">Start at the beginning<span class="placement-sub">Stage 1 onwards</span></button>
</div>
<p class="small">“Start at the beginning” clears the placement and puts the suggested next exercise back at the top of the course.</p>
</section>

<section class="settings-card">
<h2>Back up your progress</h2>
<p>Progress lives in this browser. Export a backup before changing phones, clearing browser data, or reinstalling the app.</p>
<div class="data-actions">
<button type="button" class="btn btn-quiet js-export">{svg("download")} Export backup</button>
<button type="button" class="btn btn-quiet js-import">{svg("upload")} Import backup</button>
</div>
<details>
<summary>How backups work</summary>
<p>The export downloads a small JSON file with your checkmarks, mastered exercises, practice days and notes. Import it on another device to pick up where you left off. Importing replaces whatever is currently saved in this browser.</p>
</details>
</section>

<section class="settings-card">
<h2>Start over</h2>
<p>This clears every checkmark, mastered exercise, practice day and note on this device. Export a backup first if you might want it back.</p>
<button type="button" class="btn btn-danger js-reset">{svg("trash")} Reset all progress…</button>
</section>

<section class="settings-card">
<h2>About this course</h2>
<p>{BRAND} is a free, no-account course for people who just adopted a shelter or rescue dog. It is reward-based throughout and follows the advice of the ASPCA, AVSAB, VCA and AKC. Read the <a href="golden-rules.html">golden rules</a> for the principles and the <a href="golden-rules.html#sources">reading list</a> for the research behind them.</p>
<details>
<summary>Privacy and storage</summary>
<p>There is no server, account, analytics or tracking. Your progress is stored only in this browser's local storage. Clearing site data or using a different browser starts a fresh course unless you import a backup.</p>
</details>
</section>

<dialog class="modal" id="import-dialog" aria-labelledby="import-title">
<div class="modal-inner">
<h2 id="import-title">Import a backup</h2>
<p>Choose the backup file you exported, or paste its contents.</p>
<label for="import-file">Backup file</label>
<input type="file" id="import-file" accept="application/json,.json">
<label for="import-text">Or paste the backup text</label>
<textarea id="import-text" spellcheck="false" placeholder='{{"v":1,…}}'></textarea>
<p class="small">Importing replaces the progress currently saved in this browser.</p>
<div class="modal-actions">
<button type="button" class="btn btn-ghost js-modal-close">Cancel</button>
<button type="button" class="btn btn-primary js-import-confirm">Import</button>
</div>
</div>
</dialog>

<dialog class="modal" id="reset-dialog" aria-labelledby="reset-title">
<div class="modal-inner">
<h2 id="reset-title">Reset all progress?</h2>
<p>Every checkmark, mastered exercise, practice day and note on this device will be cleared. This cannot be undone.</p>
<div class="modal-actions">
<button type="button" class="btn btn-ghost js-modal-close">Cancel</button>
<button type="button" class="btn btn-danger js-reset-confirm">Reset everything</button>
</div>
</div>
</dialog>
'''
    return body


# ---------------------------------------------------------------- Stage
def stage_body(s):
    n = s["num"]
    rows = []
    for k, e in enumerate(s["exercises"], 1):
        tags_html = "".join(f'<span class="ex-tag">{esc(tag_label(t))}</span>' for t in e["tags"])
        supporting_html = "" if e.get("core", True) else '<span class="ex-flag">Supporting</span>'
        advice = seq_advice(e)
        seq_html = f'<span class="ex-seq">{esc(advice)}</span>' if advice else ""
        rows.append(f'''<li class="ex-row" data-ex="{esc(e["slug"])}">
<a class="ex-row-link" href="exercises/{esc(e["slug"])}.html">
<span class="ex-num">{k:02d}</span>
<span class="grow"><span class="ex-title">{esc(e["title"])}</span><span class="ex-sub">{esc(e["time"])}</span><span class="ex-tags">{tags_html}{supporting_html}</span>{seq_html}</span>
<span class="status-slot"></span>
<span class="chevron">{svg("chevron-right")}</span>
</a>
</li>''')
    prev_stage = STAGES[n - 2] if n > 1 else None
    next_stage = STAGES[n] if n < len(STAGES) else None
    essentials_html = ""
    if s.get("essentials"):
        items = "".join(f"<li>{esc(x)}</li>" for x in s["essentials"])
        essentials_html = f'''
<section class="essentials-card">
<div class="section-head"><h2>First-week health &amp; ID</h2></div>
<ul class="essentials-list">{items}</ul>
</section>
'''
    prev_html = (
        f'<a class="footlink" href="stage-{prev_stage["num"]}.html"><span class="dir">← Previous stage</span><span class="t">{prev_stage["num"]:02d} · {esc(prev_stage["name"])}</span></a>'
        if prev_stage else
        '<a class="footlink" href="index.html"><span class="dir">← Back</span><span class="t">Today &amp; your course</span></a>'
    )
    next_html = (
        f'<a class="footlink" href="stage-{next_stage["num"]}.html"><span class="dir">Next stage →</span><span class="t">{next_stage["num"]:02d} · {esc(next_stage["name"])}</span></a>'
        if next_stage else
        '<a class="footlink" href="golden-rules.html"><span class="dir">Reference</span><span class="t">The golden rules</span></a>'
    )

    body = f'''
<div class="crumbs"><a href="index.html">Today</a><span>·</span><a href="course.html">Course</a><span>·</span>Stage {n}</div>
<section class="stage-hero s{n}">
<div class="stage-hero-top"><span class="stage-index">{n:02d}</span><span class="chip">Stage {n} · {esc(s["when"])}</span></div>
<h1>{esc(s["name"])}</h1>
<p class="lede">{esc(s["purpose"])}</p>
<p class="stage-intro">{esc(s["intro"])}</p>
<div class="progress-row"><div class="segs" data-progress="{n}"></div><span class="progress-label js-prog-label"></span></div>
<div class="stage-banner js-stage-banner" role="status">Every exercise in this stage is mastered.</div>
</section>
{essentials_html}

<section class="exercise-list-card">
<div class="section-head"><h2>Exercises</h2><span class="small">{len(s["exercises"])} in this stage</span></div>
<ol class="ex-list">{''.join(rows)}</ol>
</section>

<div class="footnav">{prev_html}
{next_html}
</div>
'''
    return body


# ---------------------------------------------------------------- Exercise
def exercise_body(row):
    s, e = row["stage"], row["ex"]
    n, slug = s["num"], e["slug"]
    steps = "\n".join(
        f'<li data-i="{i}"><label><input type="checkbox" class="js-step"><span class="step-num">{i + 1:02d}</span><span class="step-label">{esc(t)}</span></label></li>'
        for i, t in enumerate(e["steps"])
    )
    crits = "\n".join(
        f'<li data-c="{i}"><label><input type="checkbox" class="js-crit"><span class="step-num">✓</span><span class="step-label">{esc(t)}</span></label></li>'
        for i, t in enumerate(e["criteria"])
    )
    mistakes = "".join(f"<li>{esc(m)}</li>" for m in e["mistakes"])
    tr_list = "".join(
        f'<details class="trouble"><summary>{esc(t["q"])}</summary><p>{esc(t["a"])}</p></details>'
        for t in e["trouble"]
    )
    timer = ""
    if e.get("timer"):
        timer = f'''<div class="timer-row"><button type="button" class="btn btn-quiet js-timer-btn" data-sec="{e["timer"]}">{svg("timer")} Start {e["timer"]}-second timer</button><span class="timer-readout js-timer-readout" role="timer"></span></div>'''
    src = ""
    if e.get("source"):
        src = f'<p class="learn-more">Source: <a href="{esc(e["source"]["url"])}" target="_blank" rel="noopener">{esc(e["source"]["label"])}</a></p>'
    need_items = "".join(f"<li>{esc(x)}</li>" for x in e["need"])

    advice = seq_advice(e)
    seq_callout = (
        f'<div class="callout info seq-callout"><h3>Good to know before you start</h3><p>{esc(advice)}</p></div>\n\n'
        if advice else ""
    )

    gi = row["i"]
    prev_row = EXERCISES[gi - 2] if gi > 1 else None
    next_row = EXERCISES[gi] if gi < len(EXERCISES) else None
    prev_link = (
        (f'{prev_row["ex"]["slug"]}.html', prev_row["ex"]["title"], "← Previous in the stage")
        if prev_row else
        (f'../stage-{n}.html', f'Stage {n} · {s["name"]}', "Back to stage")
    )
    next_link = (
        (f'{next_row["ex"]["slug"]}.html', next_row["ex"]["title"], "Next in the stage →")
        if next_row else
        ("../golden-rules.html", "The golden rules", "Reference")
    )

    session_data = json.dumps(
        {"title": e["title"], "slug": slug, "steps": e["steps"]},
        ensure_ascii=False,
    ).replace("</", "<\\/")

    body = f'''
<div class="crumbs"><a href="../index.html">Today</a><span>·</span><a href="../stage-{n}.html">Stage {n} · {esc(s["name"])}</a></div>
<section class="exercise-head s{n}">
<span class="kicker">Stage {n} · {esc(s["name"])}</span>
<h1>{esc(e["title"])}</h1>
<div class="exercise-meta"><span>{esc(e["time"])}</span><span>{len(e["steps"])} steps</span><span class="js-stepcount">0 of {len(e["steps"])} steps done</span></div>
</section>

<div class="goal"><span class="goal-label">The goal</span>{esc(e["goal"])}</div>

{seq_callout}<div class="exercise-actions">
<button type="button" class="btn btn-primary js-session-start">{svg("play")} Start guided session</button>
<a class="btn btn-quiet" href="#steps">See all steps</a>
</div>

<details class="why-block">
<summary>{svg("info")} Why this matters</summary>
<p>{esc(e["why"])}</p>
</details>

<section class="exercise-section">
<h2>What you need</h2>
<ul class="needrow">{need_items}</ul>
</section>

<section class="exercise-section" id="steps">
<h2>Steps</h2>
<p class="section-note">Tick each step as you go. The bar at the top fills in.</p>
<ol class="steps">{steps}</ol>
</section>

<section class="exercise-section">
<h2>Mastery check</h2>
<p class="section-note">You have got this when all of these are true in a normal session, on a normal day.</p>
<ol class="steps crit">{crits}</ol>
{timer}
</section>

<div class="callout warn">
<h3>Common mistakes</h3>
<ul>{mistakes}</ul>
</div>

<section class="exercise-section">
<h2>If your dog is struggling</h2>
<div class="trouble-list">{tr_list}</div>
</section>
{src}

<details class="notes-block">
<summary>{svg("note")} Notes for you two</summary>
<div class="notes-inner">
<label class="visually-hidden" for="ex-notes">Notes</label>
<textarea class="js-notes" id="ex-notes" placeholder="What worked today? Where did your dog get stuck? What helped?"></textarea>
<div class="notes-saved js-notes-saved"></div>
</div>
</details>

<div class="master-panel">
<h2>Practised this one?</h2>
<p>Mastered means the checks above passed in a normal session, on a normal day. You can undo it at any time.</p>
<div class="stage-complete js-stage-complete" role="status" hidden>Stage {n} complete — a great stopping point.</div>
<button type="button" class="btn btn-primary js-master">Mark as mastered</button>
<button type="button" class="btn btn-ghost js-keepgoing">Not quite yet</button>
<div class="master-next js-master-next" hidden>
<div class="master-next-actions">
<a class="btn btn-primary js-master-next-link" href="../index.html" hidden><span class="js-master-next-label">Next up</span>{svg("arrow-right")}</a>
<a class="btn btn-quiet js-master-next-back" href="../stage-{n}.html">Back to Stage {n}</a>
<a class="btn btn-quiet js-master-next-done" href="../index.html">Done for today</a>
</div>
</div>
</div>

<div class="footnav">
<a class="footlink" href="{prev_link[0]}"><span class="dir">{prev_link[2]}</span><span class="t">{esc(prev_link[1])}</span></a>
<a class="footlink" href="{next_link[0]}"><span class="dir">{next_link[2]}</span><span class="t">{esc(next_link[1])}</span></a>
</div>

<div class="session-bar" aria-label="Session controls">
<div class="session-bar-copy"><span class="session-bar-label js-session-label">0 of {len(e["steps"])} steps</span><div class="progress"><div class="progress-fill js-session-fill"></div></div></div>
<button type="button" class="btn btn-primary js-session-start">Start</button>
</div>

<dialog class="session-dialog js-session-dialog" aria-labelledby="session-title">
<div class="session-inner">
<div class="session-head"><div><span class="kicker">Guided session</span><h2 id="session-title">{esc(e["title"])}</h2></div><button type="button" class="icon-btn js-session-close" aria-label="Close session">{svg("x")}</button></div>
<div class="session-progress"><div class="progress"><div class="progress-fill js-session-progress"></div></div><span class="js-session-count">Step 1 of {len(e["steps"])}</span></div>
<div class="session-body">
<p class="session-step js-session-step"></p>
<p class="session-hint">Say the step out loud, then tap Next when you have done it.</p>
</div>
<div class="session-actions"><button type="button" class="btn btn-quiet js-session-prev">Back</button><button type="button" class="btn btn-primary js-session-next">Next</button></div>
<div class="session-complete js-session-complete" hidden>
<h2>Session complete</h2>
<p class="js-session-complete-text">Nice work. If it went well, mark the exercise as mastered — or come back tomorrow and repeat it.</p>
<div class="session-next js-session-nextup" hidden>
<p class="session-next-lead js-session-next-lead" hidden></p>
<a class="btn btn-primary js-session-next-link" href="../index.html" hidden><span class="js-session-next-label">Next up</span>{svg("arrow-right")}</a>
</div>
<button type="button" class="btn btn-primary js-session-master">Mark as mastered</button>
<button type="button" class="btn btn-quiet js-session-done">Close</button>
</div>
</div>
</dialog>

<script type="application/json" class="js-session-data">{session_data}</script>
'''
    return body


# ---------------------------------------------------------------- PWA files
MANIFEST_FILE = {
    "name": "Pawsitive Start — calm dog training",
    "short_name": "Pawsitive",
    "description": "A calm, step-by-step training course for newly adopted shelter and rescue dogs.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#f7f2e9",
    "theme_color": "#f7f2e9",
    "categories": ["education", "lifestyle"],
    "icons": [
        {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "assets/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
    "shortcuts": [
        {"name": "Today", "short_name": "Today", "url": "./index.html"},
        {"name": "Course", "short_name": "Course", "url": "./course.html"},
        {"name": "Golden rules", "short_name": "Rules", "url": "./golden-rules.html"},
    ],
}


def write_pwa(precache, cache_name):
    write(os.path.join(SITE, "manifest.webmanifest"),
          json.dumps(MANIFEST_FILE, ensure_ascii=False, indent=2) + "\n")
    listed = ",\n".join(f'  "{u}"' for u in precache)
    sw = f'''/* Pawsitive Start service worker — generated by build/build.py */
const CACHE = "{cache_name}";
const PRECACHE = [
{listed}
];

self.addEventListener("install", (event) => {{
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
}});

self.addEventListener("activate", (event) => {{
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
    ).then(() => self.clients.claim())
  );
}});

self.addEventListener("fetch", (event) => {{
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate") {{
    event.respondWith(
      fetch(request).then((response) => {{
        const copy = response.clone();
        caches.open(CACHE).then((cache) => cache.put(request, copy));
        return response;
      }}).catch(() =>
        caches.match(request).then((hit) => hit || caches.match("index.html"))
      )
    );
    return;
  }}

  event.respondWith(
    caches.match(request).then((hit) => {{
      if (hit) return hit;
      return fetch(request).then((response) => {{
        if (response && response.status === 200 && response.type === "basic") {{
          const copy = response.clone();
          caches.open(CACHE).then((cache) => cache.put(request, copy));
        }}
        return response;
      }});
    }})
  );
}});
'''
    write(os.path.join(SITE, "sw.js"), sw)


# ---------------------------------------------------------------- main
def main():
    make_icons.ensure(os.path.join(SITE, "assets"))

    pages = []
    pages.append(("index.html", shell(
        f"{BRAND} — dog training in small, calm steps",
        f"A step-by-step course for newly adopted shelter dogs: six stages, {TOTAL} short exercises, a few calm minutes at a time.",
        "", home_body(), "home", bare_title=True,
        body_attrs=' data-page="home"', extra_head=home_mode_script())))
    pages.append(("course.html", shell(
        "The course",
        f"{len(STAGES)} stages and {TOTAL} short exercises that take a new rescue dog from decompression to everyday confidence.",
        "", course_body(), "course",
        body_attrs=' data-page="course"')))
    pages.append(("golden-rules.html", shell(
        "The golden rules",
        "How dogs learn: rewards, timing, sessions, proofing, body language and consent — the principles behind every exercise.",
        "", rules_body(), "rules",
        body_attrs=' data-page="rules"')))
    pages.append(("settings.html", shell(
        "Settings and backup",
        "Install Pawsitive Start as an app and export or import your progress. Everything stays on your device.",
        "", settings_body(), "settings",
        body_attrs=' data-page="settings"')))

    for s in STAGES:
        n = s["num"]
        pages.append((f"stage-{n}.html", shell(
            f"Stage {n} · {s['name']}",
            f"{s['purpose']} ({s['when']})",
            "", stage_body(s), "stage", colorclass=f"s{n}",
            body_attrs=f' data-page="stage" data-stage="{n}"')))

    for row in EXERCISES:
        s, e = row["stage"], row["ex"]
        pages.append((f"exercises/{e['slug']}.html", shell(
            e["title"],
            f"{s['when']} · {len(e['steps'])}-step exercise for new dog owners: {e['goal']}",
            "../", exercise_body(row), "exercise", colorclass=f"s{s['num']}",
            subbar=True, stage=s["num"],
            body_attrs=f' data-page="exercise" data-slug="{esc(e["slug"])}"')))

    for path, content in pages:
        write(os.path.join(SITE, path), content)

    # ---- precache + cache version from generated bytes ----
    # CSS/JS entries carry the same ?v= the pages request; unversioned URLs
    # would never match in caches.match and the offline precache would miss.
    precache = [
        "./", "index.html", "course.html", "golden-rules.html", "settings.html",
        "manifest.webmanifest", f"assets/site.css?v={CSS_V}", f"assets/app.js?v={JS_V}",
        "assets/fonts/fraunces.woff2",
        "assets/favicon.svg", "assets/icon-180.png", "assets/icon-192.png",
        "assets/icon-512.png", "assets/icon-maskable-512.png",
    ]
    precache += [f"stage-{s['num']}.html" for s in STAGES]
    precache += [f"exercises/{row['ex']['slug']}.html" for row in EXERCISES]

    digest = hashlib.sha1()
    for rel in ["assets/site.css", "assets/app.js", "assets/fonts/fraunces.woff2"] + [p for p, _ in pages]:
        with open(os.path.join(SITE, rel), "rb") as f:
            digest.update(f.read())
    cache_name = "pawsitive-start-" + digest.hexdigest()[:10]
    write_pwa(precache, cache_name)

    # ---- internal link check ----
    href_re = re.compile(
        r'href="((?:\.\./|)(?:index|course|settings|golden-rules|stage-\d|exercises/[a-z0-9-]+)\.html(?:#[a-z0-9-]+)?)"'
    )
    page_files = []
    for base, _dirs, files in os.walk(SITE):
        for f in files:
            if f.endswith(".html"):
                page_files.append(os.path.join(base, f))
    broken = []
    for pf in page_files:
        base_dir = os.path.dirname(pf)
        with open(pf, encoding="utf-8") as fh:
            content = fh.read()
        for m in href_re.finditer(content):
            target = os.path.normpath(os.path.join(base_dir, m.group(1).split("#")[0]))
            if not os.path.exists(target):
                broken.append(f"{os.path.relpath(pf, SITE)} → {m.group(1)}")

    print(f"Generated {len(pages)} pages ({len(page_files)} html files in site/)")
    print(f"PWA: manifest.webmanifest + sw.js ({cache_name}, {len(precache)} precached URLs)")
    if broken:
        print(f"⚠️ BROKEN INTERNAL LINKS ({len(broken)}):")
        for b in broken[:20]:
            print("  ✗", b)
        sys.exit(1)
    print("Internal link check: OK ✓")


if __name__ == "__main__":
    main()

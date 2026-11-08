# Aggregates all stage files, validates the course schema, and exports MANIFEST.
import importlib, re, sys


def _load(n):
    try:
        return importlib.import_module(f"data_stage{n}").STAGE
    except ImportError:
        return None


STAGES = []
_missing = []
for n in (1, 2, 3, 4, 5, 6):
    s = _load(n)
    if s is None:
        _missing.append(n)
    else:
        STAGES.append(s)

ERRORS = []


def err(msg):
    ERRORS.append(msg)


# ---- validation ----
if _missing:
    err(f"Missing stage data files: {_missing}")

slugs_seen = set()
SLUG_RE = re.compile(r"^[a-z0-9-]+$")

for s in STAGES:
    n = s.get("num")
    for k in ("num", "slug", "name", "emoji", "color", "when", "purpose", "intro", "exercises"):
        if k not in s:
            err(f"stage {n}: missing key '{k}'")
    if n and not (1 <= n <= 6):
        err(f"stage {n}: num out of range")
    if s.get("color") != n:
        err(f"stage {n}: color should equal num")
    if not s.get("purpose") or len(s["purpose"]) > 140:
        err(f"stage {n}: purpose missing or >140 chars")
    for e in s["exercises"]:
        slug = e.get("slug", "?")
        if not SLUG_RE.match(slug or ""):
            err(f"stage {n} · {slug}: bad slug")
        if slug in slugs_seen:
            err(f"stage {n} · {slug}: duplicate slug")
        slugs_seen.add(slug)
        for k in ("slug", "title", "emoji", "time", "goal", "why", "need", "steps", "criteria", "mistakes", "trouble"):
            if k not in e:
                err(f"stage {n} · {slug}: missing key '{k}'")
        if not 5 <= len(e.get("steps", [])) <= 9:
            err(f"stage {n} · {slug}: steps count {len(e.get('steps', []))} out of range 5–9")
        if not 2 <= len(e.get("criteria", [])) <= 3:
            err(f"stage {n} · {slug}: criteria count {len(e.get('criteria', []))} out of range 2–3")
        if not 2 <= len(e.get("mistakes", [])) <= 4:
            err(f"stage {n} · {slug}: mistakes count out of range 2–4")
        if not 2 <= len(e.get("need", [])) <= 6:
            err(f"stage {n} · {slug}: need count out of range 2–6")
        tr = e.get("trouble", [])
        if not 1 <= len(tr) <= 3:
            err(f"stage {n} · {slug}: trouble count out of range 1–3")
        for t in tr:
            if "q" not in t or "a" not in t:
                err(f"stage {n} · {slug}: trouble item missing q/a")
        if len(e.get("goal", "")) > 160:
            err(f"stage {n} · {slug}: goal >160 chars")
        if len(e.get("title", "")) > 60:
            err(f"stage {n} · {slug}: title >60 chars")
        if len(e.get("why", "")) < 40:
            err(f"stage {n} · {slug}: why too short")
        if "timer" in e and not isinstance(e["timer"], int):
            err(f"stage {n} · {slug}: timer must be int")
        if "source" in e:
            src = e["source"]
            if "label" not in src or "url" not in src:
                err(f"stage {n} · {slug}: source missing label/url")
            if not str(src.get("url", "")).startswith("https://"):
                err(f"stage {n} · {slug}: source url not https")

if ERRORS:
    print("OH NO — course validation errors:")
    for e in ERRORS:
        print(" ✗", e)
    sys.exit(1)

# ---- flat exercise list, curriculum order ----
EXERCISES = []
_gi = 0
for s in STAGES:
    for k, e in enumerate(s["exercises"]):
        _gi += 1
        EXERCISES.append({"stage": s, "ex": e, "i": _gi, "k": k})

# ---- manifest for the client ----
MANIFEST = {
    "slugs": [row["ex"]["slug"] for row in EXERCISES],
    "stages": {str(s["num"]): {"n": s["name"], "e": s["emoji"], "w": s["when"]} for s in STAGES},
    "ex": {
        row["ex"]["slug"]: {
            "t": row["ex"]["title"], "g": row["ex"]["goal"],
            "st": row["stage"]["num"], "s": len(row["ex"]["steps"]), "cr": len(row["ex"]["criteria"]),
        }
        for row in EXERCISES
    },
}

if __name__ == "__main__":
    print("Validation OK ✓")
    for s in STAGES:
        print(f"  Stage {s['num']} {s['emoji']} {s['name']} ({s['when']}) → {len(s['exercises'])} exercises")
    print(f"Total exercises: {len(EXERCISES)}")
    print(f"Manifest slugs: {len(MANIFEST['slugs'])}")

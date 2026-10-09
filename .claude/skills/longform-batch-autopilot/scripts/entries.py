#!/usr/bin/env python3
"""Turn a client's topics (+ post-call statuses) into the LONGFORMS entry lines.

Usage: python3 -I entries.py TOPICS.json            -> prints {"entries": [...], "left_out": [...], "notes": [...]}

TOPICS.json:
{
  "platforms": "X, LinkedIn",            # the topic sheet's PLATFORMS row (decides the default tag)
  "call": true,                          # false when there is no transcript: every topic goes in
  "topics": [
    {"n": 1, "type": "A", "posts": 1,    # posts = 2 when the TOPIC header says "2 POSTS"
     "vehicle": "Longform (X/LI)",       # VEHICLE field, verbatim
     "perspective": "Operator in his 30s ... personally.",   # PERSPECTIVE field, verbatim
     "status": "KEPT",                   # from the brief: KEPT / PIVOT (...) / NOT DISCUSSED / KILLED / PARKED / NEW
     "vehicle_override": null,           # only when the CALL explicitly set a different vehicle
     "posts_override": null}             # only when the CALL explicitly changed the post count
  ]
}

Rules (taken from Jeremiah's Week 1 and Week 2 longform docs, see references/longform-doc.md):
- Line format: "<n> - (<platform>) - (<perspective>) - (<vehicle>)".
- Numbers run 1, 2, 3 over the lines that are written, not the topic-sheet numbers.
- A "2 POSTS" topic is two consecutive numbers with identical lines.
- A vehicle that names a different format per platform ("Thread (X) / Long form (LI)") is one number
  split into n.1 (X) and n.2 (LI). A bare "Thread" for an X + LinkedIn client splits the same way
  (Thread on X, Long-form on LinkedIn).
- A platform tag inside VEHICLE ("(X/LI)", "(LI)", "(X)") moves into the platform slot. With no tag,
  the platform comes from PLATFORMS: X + LinkedIn -> X/LI, X only -> X, LinkedIn only -> LI.
- "Longform" / "Long form" -> "Long-form"; "Medium form" -> "Medium-form"; everything else as written.
- Perspective is copied verbatim minus its final period. Curly and straight apostrophes are kept.
- Who gets a line: with a call, KEPT and PIVOT topics, NEW topics that have a vehicle, and NOT DISCUSSED
  topics that are Type B (no answers needed). NOT DISCUSSED Type A topics and KILLED topics are left out.
  Without a call (no transcript), every topic gets a line.
"""
import json, re, sys

TAG = re.compile(r"\s*\((X\s*/\s*LI|LI\s*/\s*X|X|LI|LinkedIn)\)\s*", re.I)
# a platform written as a leading word: "LI Longform", "X: Narrative thread", "LinkedIn - case study"
PREFIX = re.compile(r"^\s*[•\-*]?\s*\**\s*(X|Twitter|LI|LinkedIn)\s*\**\s*[:\-–]?\s*\**\s+", re.I)


def norm_vehicle(v):
    v = re.sub(r"\s+", " ", v).strip().strip("*").strip()
    v = v.rstrip(".").strip()
    v = re.sub(r"\blong[\s-]?form\b", "long-form", v, flags=re.I)
    v = re.sub(r"\bmedium[\s-]?form\b", "medium-form", v, flags=re.I)
    v = re.sub(r"\bshort[\s-]?form\b", "short-form", v, flags=re.I)
    return v[:1].upper() + v[1:] if v else v


def plat_word(w):
    w = w.upper()
    return "X" if w in ("X", "TWITTER") else "LI"


def tag_of(s):
    m = TAG.search(s)
    if not m:
        return None
    t = re.sub(r"\s", "", m.group(1)).upper()
    return {"LINKEDIN": "LI", "LI/X": "X/LI"}.get(t, t)


def default_platform(platforms):
    p = platforms.lower()
    x = bool(re.search(r"\bx\b|twitter", p))
    li = "linkedin" in p or re.search(r"\bli\b", p) is not None
    return "X/LI" if (x and li) or not (x or li) else ("X" if x else "LI")


def split_vehicle(vehicle, platforms):
    """Return [(platform, vehicle_text), ...]; more than one item means an n.1/n.2 split."""
    parts = [p for p in re.split(r"\s+/\s+|\n+", vehicle) if p.strip() and p.strip() not in ("•", "-", "*")]
    tagged = [(tag_of(p), TAG.sub(" ", p).strip()) for p in parts]
    if len(parts) > 1 and all(t in ("X", "LI") for t, _ in tagged):
        return [(t, norm_vehicle(v)) for t, v in tagged]
    prefixed = [PREFIX.match(p) for p in parts]
    if len(parts) > 1 and all(prefixed):
        # "X article + Doc SS QT / LI Longform", or one bullet per platform: keep the format words
        # (up to the first full stop), drop the platform word
        return [(plat_word(m.group(1)), norm_vehicle(p[m.end():].split(". ")[0]))
                for m, p in zip(prefixed, parts)]
    t = tag_of(vehicle)
    base = TAG.sub(" ", vehicle).strip()
    plat = t or default_platform(platforms)
    if plat == "X/LI" and re.fullmatch(r"(an?\s+)?thread", base.strip(), re.I):
        return [("X", "Thread"), ("LI", "Long-form")]
    return [(plat, norm_vehicle(base))]


def perspective_text(p):
    p = re.sub(r"\s+", " ", p.strip())
    return p[:-1] if p.endswith(".") else p


def included(t, call):
    if not call:
        return True, "no transcript: every topic goes in"
    s = (t.get("status") or "").upper()
    typ = (t.get("type") or "").upper()
    if s.startswith("KILLED"):
        return False, "killed on the call"
    if s.startswith(("PARKED", "ON HOLD")):
        return False, "parked for a later batch on the call"
    if s.startswith("NOT DISCUSSED"):
        if typ.startswith("B"):
            return True, "not discussed, but Type B needs no answers"
        return False, "Type A, not discussed on the call (no answers to write from)"
    if s.startswith("NEW") and not (t.get("vehicle_override") or t.get("vehicle")):
        return False, "new on the call but no vehicle was set"
    if s.startswith(("KEPT", "PIVOT", "NEW")):
        return True, s.split()[0].lower()
    return False, "unknown status %r: check by hand" % t.get("status")


def build(data):
    platforms = data.get("platforms", "X, LinkedIn")
    call = data.get("call", True)
    entries, left_out, notes, n = [], [], [], 0
    for t in data["topics"]:
        ok, why = included(t, call)
        if not ok:
            left_out.append({"topic": t["n"], "why": why})
            continue
        vehicle = t.get("vehicle_override") or t["vehicle"]
        if t.get("vehicle_override"):
            notes.append("T%s: vehicle changed on the call to %r" % (t["n"], vehicle))
        posts = int(t.get("posts_override") or t.get("posts") or 1)
        persp = perspective_text(t["perspective"])
        if t.get("split"):   # explicit per-platform vehicles, e.g. [{"platform":"X","vehicle":"Thread"}, ...]
            pieces = [(s["platform"].upper().replace("LINKEDIN", "LI"), norm_vehicle(s["vehicle"])) for s in t["split"]]
        else:
            pieces = split_vehicle(vehicle, platforms)
        for _ in range(posts):
            n += 1
            if len(pieces) == 1:
                plat, veh = pieces[0]
                entries.append({"topic": t["n"], "line": "%d - (%s) - (%s) - (%s)" % (n, plat, persp, veh)})
            else:
                for i, (plat, veh) in enumerate(pieces, 1):
                    entries.append({"topic": t["n"], "line": "%d.%d - (%s) - (%s) - (%s)" % (n, i, plat, persp, veh)})
    return {"entries": entries, "left_out": left_out, "notes": notes}


if __name__ == "__main__":
    print(json.dumps(build(json.load(open(sys.argv[1]))), ensure_ascii=False, indent=1))

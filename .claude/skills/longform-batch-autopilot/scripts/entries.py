#!/usr/bin/env python3
"""Turn a client's topics (+ post-call statuses) into the LONGFORMS entry lines.

Usage: python3 -I entries.py TOPICS.json
Prints {"entries": [{"topic", "line"}], "left_out": [{"topic", "why"}], "notes": [...], "problems": [...]}.
Write the doc with the lines; put every note and problem in the run summary.

The rules come from Jeremiah's real docs (Mason Oct Wk1 + Wk2, Keval, Josh C, Ben K, Teddy, Abdul, Lior,
Jason; see references/longform-doc.md). TOPICS.json:

{
  "client": "Mason L.",                  # longform doc name; loads the per-client settings in CLIENTS
  "platforms": "X, LinkedIn",            # the topic sheet's PLATFORMS row
  "call": true,                          # false when there is no transcript: every topic goes in
  "expected_posts": null,                # the brief's total post count, if it states one (checked)
  "topics": [                            # sheet order; a freeform "Topic 0" first if the sheet has one
    {"n": 1, "type": "A",                # "A" / "B"; null for a freeform topic (treated as B)
     "label": null,                      # 3rd header segment or TYPE suffix: "Snipe", "Quick Response", ...
     "title": "Being Stupid In Your 60s",
     "posts": 1,                         # 2 when the header says "2 POSTS" (counts inside VEHICLE are read too)
     "vehicle": "Longform (X/LI)",       # VEHICLE field, verbatim (all lines, bullets included)
     "perspective": "Operator ... personally.",   # PERSPECTIVE field, verbatim
     "status": "KEPT",                   # the brief's status, as written; normalised here
     "struck": false, "check": null,     # whole topic struck through on the sheet / "✅" or "❌" on its header
     "vehicle_override": null,           # only when the CALL settled a new vehicle
     "posts_override": null,             # only when the CALL changed the post count
     "perspective_override": null,       # a label, when the sheet has no PERSPECTIVE (freeform / new post)
     "merged_into": null,                # topic number this one was folded into (human call; flagged)
     "no_cta": null, "li_vehicle": null, # Ben: value tweet with no DM CTA / LinkedIn format from a FOR LINKEDIN note
     "extra_posts": []}                  # posts the strategist asked for in a sheet comment or on the call:
                                         #   {"perspective": "Chad mentality", "vehicle": null, "same_material": false,
                                         #    "source": "Kyle comment: Make a 2nd post on Boxing and chad mentality"}
  ]
}
"""
import json, re, sys

# Per-client line habits, learned from their real docs. Keyed by longform doc name.
CLIENTS = {
    "Jason G.": {"perspective_mode": "drop_last_sentence", "doc_ss_as": "Apple Notes"},
    "Abdul F.": {"drop_photo_suffix": True, "thread_li": "Long-form listicle", "doc_ss_as": "Apple Notes"},
    "Ben K.": {"split_cta_posts": True},
    "Joshua C.": {"promo_split": True},
    "Lior P.": {"platforms": "X"},
    "Zarak A.": {"platforms": "X"},
}

TAG = re.compile(r"\s*\(\s*(X\s*(?:/|&|\+|and)\s*(?:LI|LinkedIn)|(?:LI|LinkedIn)\s*(?:/|&|\+|and)\s*X"
                 r"|X|LI|LinkedIn|Twitter)\s*\)\s*", re.I)
SEP = re.compile(r"\s+/\s+|(?<=\))\s*[/,;·]\s*|\s+·\s+|\n+")
PREFIX = re.compile(r"^\s*[•\-*]?\s*\**\s*(X|Twitter|LI|LinkedIn)\s*\**\s*[:\-–]?\s*\**\s+", re.I)
ASSET_TAG = re.compile(r"[\s.,-]*\bwith\s+(?:an?\s+)?images?\s*\(\s*(?:X|LI|LinkedIn)\s*\)", re.I)
PLAT_PHRASE = re.compile(r"\s*\bfor\s+(X|LI|LinkedIn)\s+and\s+(X|LI|LinkedIn)\b", re.I)
WITH_IMAGE = re.compile(r"[\s.,-]*\bwith\s+(?:an?\s+)?images?\b(?!\s*\()", re.I)
CAPS_TAIL = re.compile(r"\s+[A-Z][A-Z ]{6,}$")
COUNT = re.compile(r"[,\s]*\(?\s*(?:[x×]\s*(\d+)|\b(two|three|four|2|3|4)\s+posts?)\s*\)?\s*$", re.I)
NOISE_PAREN = re.compile(r"\s*\((?:organic|paid|dash|dashes|bullets?|[A-Z]{2,5})\)")
FMT = {"thread", "threads", "listicle", "listicles", "infographic", "image", "images", "photo", "photos",
       "screenshot", "post", "posts", "tweet", "carousel", "video", "checklist", "hook", "article", "graphic",
       "diagram", "reply", "list", "lists", "lines", "promo"}
WORDN = {"two": 2, "three": 3, "four": 4}


def tag_norm(s):
    t = re.sub(r"\s", "", s).upper().replace("LINKEDIN", "LI").replace("TWITTER", "X")
    return "X/LI" if re.fullmatch(r"X(/|&|\+|AND)LI|LI(/|&|\+|AND)X", t) else t


def default_platform(platforms):
    p = (platforms or "").lower()
    x = bool(re.search(r"\bx\b|twitter", p))
    li = "linkedin" in p or re.search(r"\bli\b", p) is not None
    return "X/LI" if (x and li) or not (x or li) else ("X" if x else "LI")


def curl_double(s):
    out = []
    for i, ch in enumerate(s):
        out.append(("“" if i == 0 or s[i - 1] in " ([—-" else "”") if ch == '"' else ch)
    return "".join(out)


def lower_fmt(v):
    w = v.split(" ")
    for i in range(1, len(w)):
        word = w[i]
        if word[:1].isupper() and word[1:].islower() and word.lower() in FMT:
            prev = w[i - 1]
            if i - 1 > 0 and prev[:1].isupper() and prev.lower() not in FMT:
                continue                         # "Google Doc Screenshot", "Apple Notes Screenshot"
            w[i] = word.lower()
    return " ".join(w)


def norm_vehicle(v, cfg, notes):
    v = re.sub(r"\s+", " ", v).strip().strip("*").strip().rstrip(".").strip()
    v = CAPS_TAIL.sub("", v)                     # "... WITH LIFESTYLE IMAGE REQUEST"
    v = WITH_IMAGE.sub("", v)                    # bare image requests
    v = NOISE_PAREN.sub("", v)                   # (organic) (dash) (GDS) ...
    v = re.sub(r"\blisticle\s+(long|medium)[\s-]?form\b", r"\1-form listicle", v, flags=re.I)
    v = re.sub(r"\blong[\s-]?form\b", "long-form", v, flags=re.I)
    v = re.sub(r"\bmedium[\s-]?form\b", "medium-form", v, flags=re.I)
    v = re.sub(r"\bshort[\s-]?form\b", "short-form", v, flags=re.I)
    if cfg.get("drop_photo_suffix"):
        v = re.sub(r"\s*\+\s*(?:\d+(?:-\d+)?\s+)?photos?\b", "", v, flags=re.I)
    if cfg.get("doc_ss_as"):
        new = re.sub(r"\b(?:Google\s+)?Doc\s+(SS|Screenshot)\b", lambda m: cfg["doc_ss_as"] + " " + m.group(1), v)
        new = re.sub(r"^GDS$", cfg["doc_ss_as"] + " SS", new)
        if new != v:
            notes.append("screenshot relabelled %r -> %r (this client's habit): confirm" % (v, new))
        v = new
    if re.search(r"\([^()]*\)", v):
        notes.append("vehicle qualifier in brackets turned into a comma: %r" % v)
    v = re.sub(r"\s*\(([^()]*)\)", r", \1", v).strip(" ,")
    v = v[:1].upper() + v[1:] if v else v
    return curl_double(lower_fmt(v))


QT_AFTER = re.compile(r"(?:\bthen\b|\+|\band\b),?\s+(?:a\s+)?(?:[\w-]+\s+){0,4}?(quote[\s-]?tweet|QT)\b", re.I)


def article_pieces(plat, text, notes):
    """An X article plus a quote tweet of it is two numbers in his doc: (Article) and (Article wrapper),
    as in Keval Oct Wk2. Returns None when `text` is not an X article."""
    t = text.strip()
    if plat in ("X", "X/LI") and re.match(r"^(X\s+)?article\b", t, re.I) and (plat == "X" or t[:1] in "Xx"):
        if QT_AFTER.search(t):
            notes.append("X article + QT %r: wrapper given its own number, as in Keval's doc: confirm" % t)
            return [("X", "Article"), "WRAPPER"]
        return [("X", "Article")]
    return None


def split_pieces(vehicle, plat_default, cfg, notes):
    """-> (pieces, count). pieces = [(platform, vehicle)]; a "WRAPPER" item adds an X article wrapper number."""
    parts = [p for p in SEP.split(vehicle) if p.strip() and p.strip() not in ("•", "-", "*")]

    def piece(plat, text):
        return article_pieces(plat, text, notes) or [(plat, norm_vehicle(text, cfg, notes))]
    tagged = [(TAG.search(p), p) for p in parts]
    if len(parts) > 1 and all(m for m, _ in tagged):
        return [x for m, p in tagged for x in piece(tag_norm(m.group(1)), TAG.sub(" ", p))], None
    prefixed = [PREFIX.match(p) for p in parts]
    if len(parts) > 1 and all(prefixed):
        return [x for m, p in zip(prefixed, parts)
                for x in piece(tag_norm(m.group(1)), p[m.end():].split(". ")[0])], None
    v, plat, count = vehicle, None, None
    v = ASSET_TAG.sub("", v)                     # "(LI)" glued to an image request is not the platform
    if PLAT_PHRASE.search(v):
        plat, v = "X/LI", PLAT_PHRASE.sub("", v)
    m = TAG.search(v)
    if m:
        plat, v = tag_norm(m.group(1)), TAG.sub(" ", v).strip()
    c = COUNT.search(v)
    if c:
        count = int(c.group(1)) if c.group(1) else WORDN.get(c.group(2).lower()) or int(c.group(2))
        v = v[:c.start()]
    plat = plat or plat_default
    base = v.strip()
    if re.match(r"^X\s+article\b", base, re.I):
        return article_pieces("X", base, notes), count
    if plat == "X/LI":
        if re.fullmatch(r"(an?\s+)?thread", base, re.I) or re.search(r"\([^()]*\bthread\b[^()]*\)", base, re.I):
            return [("X", "Thread"), ("LI", cfg.get("thread_li", "Long-form"))], count
        if cfg.get("promo_split") and re.search(r"\bpromo\b", base, re.I):
            nv = norm_vehicle(base, cfg, notes)
            notes.append("promo split into X and LI (this client's habit)")
            return [("X", nv), ("LI", nv)], count
    return [(plat, norm_vehicle(base, cfg, notes))], count


def perspective_text(p, cfg, notes):
    p = re.sub(r"\s+", " ", (p or "").strip())
    if cfg.get("perspective_mode") == "drop_last_sentence":
        s = re.split(r"(?<=\.)\s+(?=[A-Z])", p)
        if len(s) > 1:
            p = " ".join(s[:-1])

    def flat(m):                                 # "sellers (brands and distributors) and buyers (a, b, and c)"
        mem = []
        for g in re.findall(r"\w+ \(([^()]+)\)", m.group(0)):
            mem += [x.strip() for x in re.split(r",\s*(?:and\s+)?|\s+and\s+", g) if x.strip()]
        return ", ".join(mem[:-1]) + ", and " + mem[-1]
    p2 = re.sub(r"\w+ \([^()]+\)(?:(?:,\s*|\s+)and\s+\w+ \([^()]+\))+", flat, p)
    if p2 != p:
        notes.append("perspective brackets flattened: %r" % p2)
    p = p2
    return p[:-1] if p.endswith(".") else p


def status_norm(s):
    s = re.sub(r"\*", "", (s or "")).strip()
    s = re.sub(r"^(NOTE|STATUS)\s*:\s*", "", s, flags=re.I).upper()
    table = [
        (r"^KILLED\b.*\bREPLAC", "PIVOT"),
        (r"\bALREADY (TOUCHED|COVERED)\b|\bCOVERED (ABOVE|EARLIER|ELSEWHERE|IN)\b|^COVERED\b", "COVERED"),
        (r"^(KILLED|SKIPPED|NOT PICKED|DROPPED)\b", "KILLED"),
        (r"^(PARKED|REVISIT)", "PARKED"),
        (r"^ON HOLD", "ON HOLD"),
        (r"^PIVOT|^KEPT\b.*\bPIVOT|^GO\b.*\bPIVOT", "PIVOT"),
        (r"^RESOLVED", "RESOLVED"),
        (r"^BLOCKED", "BLOCKED"),
        (r"^(KEPT|ANSWERED|NO PIVOT|GO\b|DRAFTABLE|READY)", "KEPT"),
        (r"^(NOT DISCUSSED|NOT ASKED)|TYPE B,? UNCHANGED", "NOT DISCUSSED"),
        (r"^NEW", "NEW"),
    ]
    for rx, canon in table:
        if re.search(rx, s):
            return canon
    return "UNKNOWN"


def included(t, call, notes, problems):
    label, veh = t.get("label") or "", t.get("vehicle") or ""
    tn = t.get("n")
    if re.search(r"\b(snipe|quick\s*response)\b", label, re.I) or re.match(r"\s*snipe", veh, re.I) \
            or t.get("quick_response"):
        return False, "snipe/quick response: goes in its own (Snipes) / (Quick response posts) doc"
    if t.get("struck") or t.get("check") == "❌":
        return False, "struck through / ❌ on the sheet"
    if t.get("merged_into") is not None:
        notes.append("T%s folded into T%s: confirm" % (tn, t["merged_into"]))
        return False, "merged into T%s" % t["merged_into"]
    if not call:
        return True, "no transcript: every topic goes in"
    s = status_norm(t.get("status"))
    typ = (t.get("type") or "B").strip().upper()
    if s == "KILLED":
        return False, "killed on the call"
    if s == "PARKED":
        if re.search(r"screenshot", veh, re.I) and (t.get("parked_include") or re.search(
                r"send|provide|as he has", t.get("status") or "", re.I)):
            notes.append("T%s parked but the client sends the screenshots: kept, source them" % tn)
            return True, "parked, client supplies the asset"
        notes.append("T%s parked on the call: left out, include?" % tn)
        return False, "parked for a later batch"
    if s == "ON HOLD":
        notes.append("T%s on hold: left out, include?" % tn)
        return False, "on hold"
    if s == "NOT DISCUSSED":
        if typ.startswith("B"):
            return True, "not discussed, but Type B needs no answers"
        return False, "Type A, not discussed on the call (no answers to write from)"
    if s == "NEW":
        if t.get("vehicle_override") or veh:
            return True, "new on the call, vehicle set"
        notes.append("NEW %r has no vehicle: decide" % (t.get("title") or tn))
        return False, "new on the call but no vehicle was set"
    if s == "BLOCKED":
        notes.append("T%s blocked: %s" % (tn, t.get("status")))
    if s == "RESOLVED" and not t.get("vehicle_override"):
        notes.append("T%s resolved on the call but no vehicle given: check" % tn)
    if s == "UNKNOWN":
        problems.append("T%s status %r not recognised: included, check" % (tn, t.get("status")))
    return True, s.lower()


def build(data):
    cfg = dict(CLIENTS.get(data.get("client", ""), {}))
    plat_default = default_platform(cfg.get("platforms") or data.get("platforms", "X, LinkedIn"))
    call = data.get("call", True)
    entries, left_out, notes, problems = [], [], [], []
    n = 0

    def emit(tn, persp, vehicle, posts, t):
        nonlocal n
        pieces, count = split_pieces(vehicle, plat_default, cfg, notes)
        posts = int(t.get("posts_override") or max(posts or 1, count or 1))
        if t.get("li_vehicle") and len(pieces) == 1:
            pieces = [("X", pieces[0][1]), ("LI", norm_vehicle(t["li_vehicle"], cfg, notes))]
            notes.append("T%s LinkedIn format from its FOR LINKEDIN note" % tn)
        elif cfg.get("split_cta_posts") and len(pieces) == 1 and pieces[0][0] == "X/LI":
            no_cta = t.get("no_cta")
            if no_cta is None:
                no_cta = bool(re.search(r"value tweet|\bVT\b", (t.get("label") or "") + " " + vehicle, re.I)
                              and re.search(r"hot take|opinion", persp, re.I))
            if not no_cta:
                pieces = [("X", pieces[0][1]), ("LI", pieces[0][1])]
            notes.append("T%s %s (this client splits posts with a DM CTA): confirm" % (tn, "kept X/LI" if no_cta else "split X / LI"))
        for _ in range(posts):
            wrapper = "WRAPPER" in pieces
            real = [p for p in pieces if p != "WRAPPER"]
            n += 1
            if len(real) == 1:
                entries.append({"topic": tn, "line": "%d - (%s) - (%s) - (%s)" % (n, real[0][0], persp, real[0][1])})
            else:
                for i, (plat, veh) in enumerate(real, 1):
                    entries.append({"topic": tn, "line": "%d.%d - (%s) - (%s) - (%s)" % (n, i, plat, persp, veh)})
            if wrapper:
                n += 1
                entries.append({"topic": tn, "line": "%d - (X) - (%s) - (Article wrapper)" % (n, persp)})

    def persp_or_label(t, raw, tn):
        p = perspective_text(raw, cfg, notes) if raw else ""
        if not p:
            p = (t.get("title") or "").strip().rstrip(".")
            if p:
                notes.append("T%s has no PERSPECTIVE: used its title %r as the label, confirm" % (tn, p))
        if not p:
            p = "TBD"
            problems.append("T%s has no perspective or title: line says (TBD)" % tn)
        return p

    for t in data["topics"]:
        tn = t.get("n")
        ok, why = included(t, call, notes, problems)
        if ok:
            raw_p = t.get("perspective_override") or t.get("perspective")
            persp = persp_or_label(t, raw_p, tn)
            vehicle = t.get("vehicle_override") or t.get("vehicle") or ""
            if t.get("vehicle_override"):
                notes.append("T%s vehicle set on the call: %r" % (tn, vehicle))
            if not vehicle.strip():
                vehicle = "Long-form promo" if re.search(r"promo", t.get("title") or "", re.I) else "Long-form"
                notes.append("T%s has no VEHICLE: used %r, confirm" % (tn, vehicle))
            emit(tn, persp, vehicle, t.get("posts"), t)
        else:
            left_out.append({"topic": tn, "why": why})
        for x in t.get("extra_posts") or []:      # strategist-requested extra posts follow their parent
            raw_p = x.get("perspective") or (t.get("perspective") if x.get("same_material") else None)
            if not raw_p:
                problems.append("T%s extra post has no perspective label: line says (TBD)" % tn)
            persp = perspective_text(raw_p, cfg, notes) if raw_p else "TBD"
            vehicle = x.get("vehicle") or t.get("vehicle_override") or t.get("vehicle") or "Long-form"
            notes.append("T%s extra post added (%s): confirm" % (tn, x.get("source") or "strategist request"))
            emit("%s+" % tn, persp, vehicle, 1, {})

    numbers = {re.match(r"(\d+)", e["line"]).group(1) for e in entries}
    if data.get("expected_posts") and len(numbers) != int(data["expected_posts"]):
        problems.append("%d posts made, the brief counts %s: check the lines" % (len(numbers), data["expected_posts"]))
    for e in entries:
        if "()" in e["line"]:
            problems.append("empty slot in line: %r" % e["line"])
    return {"entries": entries, "left_out": left_out, "notes": notes, "problems": problems}


if __name__ == "__main__":
    print(json.dumps(build(json.load(open(sys.argv[1]))), ensure_ascii=False, indent=1))

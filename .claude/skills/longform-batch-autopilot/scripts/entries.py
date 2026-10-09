#!/usr/bin/env python3
"""Turn a client's topics (+ post-call statuses) into the LONGFORMS entry lines.

Usage: python3 -I entries.py TOPICS.json
Prints {"entries": [{"topic", "line"}], "left_out": [{"topic", "why"}],
        "would_be": [{"topic", "lines", "why"}], "notes": [...], "problems": [...]}.
Write the doc with the lines; put every note, problem and would-be line in the run summary.

would_be: each Type A topic left out for want of answers (no transcript, NOT ANSWERED, NOT DISCUSSED;
never a killed, struck, ❌, snipe, merged, parked or on-hold one) with the line(s) it would get if Jeremiah
adds it, worked out as if the call happened and it was KEPT. They are numbered "?" ("?.1" / "?.2" for an
X/LI split) and never use up a real number: {"topic": 3, "lines": ["? - (X/LI) - (...) - (...)"], "why": "..."}.
Its extra_posts' lines come after its own; a left-out topic's extra posts are left out with it ("3+").

The rules come from Jeremiah's real docs (Mason Oct Wk1 + Wk2, Keval, Josh C, Ben K, Teddy, Abdul, Lior,
Jason; see references/longform-doc.md). TOPICS.json:

{
  "client": "Mason L.",                  # longform doc name; loads the per-client settings in CLIENTS
  "strategist": "Kyle",                  # named in the type-clash gate; "the strategist" if missing
  "platforms": "X, LinkedIn",            # the topic sheet's PLATFORMS row
  "call": true,                          # false with no transcript and no brief: Type B in, Type A out
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
     "posts_override": null,             # only when the call or a strategist comment changed the post count
     "posts_override_source": null,      # where posts_override came from: "Kyle's sheet comment \"2 posts\"" (Josh C
                                         #   Oct Wk2 T4); named in its note, else the note says "set on the call"
     "perspective_override": null,       # a label, when the sheet has no PERSPECTIVE (freeform / new post)
     "inferred": null,                   # what was inferred rather than read: "vehicle and post count from the
                                         #   heading" (Ben K Oct Wk2 T7, no VEHICLE field); flagged
     "merged_into": null,                # topic number this one was folded into (human call; flagged)
     "objective": null,                  # OBJECTIVE field; "snipe" / "quick response" in it is flagged
     "other_tab_label": null,            # the same topic's header label on the other tab (e.g. Strategy says "Snipe")
     "other_tab_type": null,             # "A" / "B": the Strategy tab's raw list type, when it differs (Lior Oct Wk2)
     "client_question": null,            # true: a Type B box that carries a FOR <CLIENT> question
                                         #   (either one is a strategist gate in problems, call or no call,
                                         #   unless the topic is out for another reason: killed, struck, snipe...)
     "written_answer": null,             # the client's own written answer on the sheet, in short: "RECENT WINS JOSH
                                         #   SENT + image" (Josh D Oct Wk2 T3); flagged when a Type A topic is left out
     "freeform": false,                  # a "Topic 0" or EXTRA post outside the sheet tables: n stays an integer (an
                                         #   EXTRA takes the next number after the sheet topics), type null, and
                                         #   perspective_override a 1-3 word subject ("Trybe", Josh D Oct Wk1); flagged
     "no_cta": null, "li_vehicle": null, # Ben: no DM CTA, so an X/LI post stays one line / LinkedIn format from a
                                         #   FOR LINKEDIN note (the only thing that splits a Ben value tweet)
     "extra_posts": []}                  # posts the strategist asked for in a sheet comment or on the call:
                                         #   {"perspective": "Chad mentality", "vehicle": null, "same_material": false,
                                         #    "source": "Kyle comment: Make a 2nd post on Boxing and chad mentality"}
                                         #   they follow their parent in or out
  ]
}
"""
import itertools, json, re, sys

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
    # abbreviations he never writes in a line
    new = re.sub(r"\bLF\b", "long-form", v)
    new = re.sub(r"\bMF\b", "medium-form", new)
    new = re.sub(r"^(an?)\s+(?=\S)", "", new, flags=re.I)              # "A short-form post..." -> "short-form post..."
    new = re.sub(r"(?<=\w)\s+plus\s+(?=\w)", " + ", new, flags=re.I)   # Teddy Oct Wk1: "hook plus a ..." -> "hook + a ..."
    if new != v:
        notes.append("vehicle wording tidied %r -> %r: confirm" % (v, new))
        v = new
    # brackets (Caulen Oct Wk2, his real doc): a single format noun merges ("Short form (listicle)" ->
    # "Short-form listicle"); a bracket describing a "+ asset" is dropped ("Short form + image
    # (notes-style doc)" -> "Short-form + image"); any other bracket becomes a comma qualifier, flagged
    def bracket(m):
        inner, before = m.group(1).strip(), v[:m.start()]
        if inner.lower() in FMT:
            notes.append("format noun in brackets merged into the vehicle: (%s): confirm" % inner)
            return " " + inner.lower()
        if re.search(r"\+\s*[^+()]+$", before):
            notes.append("bracket after a '+ asset' dropped: (%s): confirm" % inner)
            return ""
        notes.append("vehicle qualifier in brackets turned into a comma: (%s): confirm" % inner)
        return ", " + inner
    v = re.sub(r"\s*\(([^()]*)\)", bracket, v).strip(" ,")
    v = re.sub(r"\s{2,}", " ", v)
    v = v[:1].upper() + v[1:] if v else v
    return curl_double(lower_fmt(v))


QT_AFTER = re.compile(r"(?:\bthen\b|\+|\band\b|\bwith\b),?\s+(?:a\s+)?(?:[\w-]+\s+){0,4}?(quote[\s-]?tweet|QT)\b", re.I)


def article_pieces(plat, text, notes):
    """An X article plus a quote tweet of it is two numbers in his doc: (Article) and (Article wrapper),
    as in Keval Oct Wk2. Returns None when `text` is not an X article."""
    t = text.strip()
    if plat in ("X", "X/LI") and re.match(r"^(X\s+)?article\b", t, re.I) and (plat == "X" or t[:1] in "Xx"):
        rest = QT_AFTER.split(re.sub(r"^(X\s+)?article\b", "", t, flags=re.I))[0].strip(" ,.:;-–—")
        if rest:
            notes.append("X article vehicle %r written as (Article), qualifier dropped: '%s': confirm" % (t, rest))
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
    p = (p or "").strip()
    cut = re.split(r"\x0b\s*\x0b|\n\s*\n|\x0b\n|\n\x0b", p, maxsplit=1)
    if len(cut) > 1 and cut[1].strip():
        notes.append("PERSPECTIVE ran on into other text after a blank line; cut there: %r..." % cut[1].strip()[:60])
        p = cut[0]
    p = re.sub(r"\s+", " ", p.replace("\x0b", " ").strip())
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
    if re.search(r"\.[\"”']$", p):             # ...as "tools like." -> ...as "tools like"
        return p[:-2] + p[-1]
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
        (r"^(NOT ANSWERED|UNANSWERED|NO ANSWER|DEFERRED)\b|^BLOCKED\b.*\b(ANSWER|DEFER|ASYNC)", "NOT ANSWERED"),
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


# Type A topics left out only for want of answers: these get would-be lines (Josh D Oct Wk2, no transcript)
NO_CALL_A = "Type A, no transcript to show the call answered it"
NOT_ANSWERED_A = "Type A, not answered on the call"
NOT_DISCUSSED_A = "Type A, not discussed on the call (no answers to write from)"


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
    typ = (t.get("type") or "B").strip().upper()
    if not call:
        # Jeremiah, Oct 9: Type B stays regardless of the call; a Type A topic needs the call's answers
        if typ.startswith("B"):
            return True, "no transcript: Type B needs no answers"
        notes.append("T%s is Type A and there is no transcript: left out; add its line if the call answered it" % tn)
        return False, NO_CALL_A
    s = status_norm(t.get("status"))
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
    if s == "NOT ANSWERED":
        # Jeremiah, Oct 9: a Type A topic the call didn't answer was skipped on the call, so no line
        if typ.startswith("B"):
            return True, "came up unanswered, but Type B needs no answers"
        return False, NOT_ANSWERED_A
    if s == "NOT DISCUSSED":
        if typ.startswith("B"):
            return True, "not discussed, but Type B needs no answers"
        return False, NOT_DISCUSSED_A
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


def type_clash(t, who, strategist):
    """A strategist gate: the type decides in or out, so a doubt over it is a problem (Lior Oct Wk2 T1: Type B
    in Client strategy, Type A with a question for Reut in the Strategy tab's raw list)."""
    typ = re.sub(r"^TYPE\s*", "", (t.get("type") or "B").strip().upper())
    why = []
    other = re.sub(r"^TYPE\s*", "", (t.get("other_tab_type") or "").strip().upper())
    if other and other != typ:
        why.append("Strategy tab says Type %s" % other)
    if t.get("client_question") and typ.startswith("B"):
        why.append("the box asks %s a question" % who)
    if why:
        return "T%s type clash: Client strategy says Type %s, %s: line follows Client strategy, confirm with %s" % (
            t.get("n"), typ, " and ".join(why), strategist)


def build(data):
    cfg = dict(CLIENTS.get(data.get("client", ""), {}))
    plat_default = default_platform(cfg.get("platforms") or data.get("platforms", "X, LinkedIn"))
    call = data.get("call", True)
    who = (data.get("client") or "").split(" ")[0] or "the client"
    strategist = data.get("strategist") or "the strategist"
    entries, left_out, would_be, notes, problems = [], [], [], [], []
    numbers_from = itertools.count(1)

    def shape(tn, persp, vehicle, posts, t, notes):
        """-> (pieces, posts): one post's (platform, vehicle) pieces and how many posts get them."""
        pieces, count = split_pieces(vehicle, plat_default, cfg, notes)
        posts = int(t.get("posts_override") or max(posts or 1, count or 1))
        if t.get("li_vehicle") and len(pieces) == 1:
            pieces = [("X", pieces[0][1]), ("LI", norm_vehicle(t["li_vehicle"], cfg, notes))]
            notes.append("T%s LinkedIn format from its FOR LINKEDIN note" % tn)
        elif cfg.get("split_cta_posts") and len(pieces) == 1 and pieces[0][0] == "X/LI":
            if re.search(r"value tweet|\bVTs?\b", (t.get("label") or "") + " " + vehicle, re.I):
                # Ben K Oct Wk1: 'Value tweet ">" Listicle' stayed one X/LI line; only a FOR LINKEDIN note split one
                notes.append("T%s kept X/LI (value tweet; split only with a FOR LINKEDIN note): confirm" % tn)
            else:
                if not t.get("no_cta"):
                    pieces = [("X", pieces[0][1]), ("LI", pieces[0][1])]
                notes.append("T%s %s (this client splits posts with a DM CTA): confirm"
                             % (tn, "kept X/LI" if t.get("no_cta") else "split X / LI"))
        return pieces, posts

    def write(nums, persp, pieces, posts):
        """The lines for `posts` posts, numbered from `nums` (real numbers, or "?" for would-be lines)."""
        out = []
        real = [p for p in pieces if p != "WRAPPER"]
        for _ in range(posts):
            num = next(nums)
            if len(real) == 1:
                out.append("%s - (%s) - (%s) - (%s)" % (num, real[0][0], persp, real[0][1]))
            else:
                out += ["%s.%d - (%s) - (%s) - (%s)" % (num, i, plat, persp, veh) for i, (plat, veh) in enumerate(real, 1)]
            if "WRAPPER" in pieces:
                out.append("%s - (X) - (%s) - (Article wrapper)" % (next(nums), persp))
        return out

    def persp_or_label(t, raw, tn, notes, problems):
        if t.get("perspective_override") and not t.get("freeform"):
            notes.append("T%s perspective is a label, not the sheet's PERSPECTIVE: %r, confirm" % (tn, t["perspective_override"]))
        p = perspective_text(raw, cfg, notes) if raw else ""
        if not p:
            p = (t.get("title") or "").strip().rstrip(".")
            if p:
                notes.append("T%s has no PERSPECTIVE: used its title %r as the label, confirm" % (tn, p))
        if not p:
            p = "TBD"
            problems.append("T%s has no perspective or title: line says (TBD)" % tn)
        return p

    def topic_lines(t, tn, nums, notes, problems):
        raw_p = t.get("perspective_override") or t.get("perspective")
        persp = persp_or_label(t, raw_p, tn, notes, problems)
        vehicle = t.get("vehicle_override") or t.get("vehicle") or ""
        if t.get("vehicle_override"):
            notes.append("T%s vehicle set on the call: %r" % (tn, vehicle))
        if t.get("posts_override"):
            src = t.get("posts_override_source")
            notes.append("T%s post count %s from %s: confirm" % (tn, t["posts_override"], src) if src
                         else "T%s post count set on the call: %s" % (tn, t["posts_override"]))
        if int(t.get("posts") or 1) > 1 and t.get("extra_posts"):
            problems.append("T%s has a header count (%s posts) and extra posts too: a comment naming each post's "
                            "subject is not extra posts, check for double counting" % (tn, t.get("posts")))
        snipe_hint = " ".join(str(t.get(k) or "") for k in ("objective", "other_tab_label"))
        if re.search(r"\b(snipe|quick\s*response)\b", snipe_hint, re.I):
            problems.append("T%s may be a snipe/quick response (%s): kept in LONGFORMS, confirm or move it to "
                            "its own doc" % (tn, snipe_hint.strip()[:80]))
        if not vehicle.strip():
            vehicle = "Long-form promo" if re.search(r"promo", t.get("title") or "", re.I) else "Long-form"
            notes.append("T%s has no VEHICLE: used %r, confirm" % (tn, vehicle))
        if t.get("freeform"):
            notes.append("freeform extra post T%s (%s): confirm" % (tn, persp))
            if not isinstance(tn, int):
                problems.append("T%s freeform topic number should be an integer, the next after the sheet topics" % tn)
            label = t.get("perspective_override") or ("" if t.get("perspective") else persp)
            if len(label.split()) > 3:
                # Josh D Oct Wk1: Jeremiah labelled Devin's EXTRA newsletter article just "Trybe"
                problems.append("T%s freeform label %r: label should be a 1-3 word subject, as in Jeremiah's 'Trybe'"
                                % (tn, label))
        pieces, posts = shape(tn, persp, vehicle, t.get("posts"), t, notes)
        if cfg.get("promo_split") and re.search(r"\bpromo\b", t.get("title") or "", re.I) \
                and not re.search(r"\bpromo\b", vehicle, re.I) and [p[0] for p in pieces] == ["X/LI"]:
            # Josh C Oct Wk2 T7 "A Day in My Life on the Road (Ecom North Toronto Promo)", VEHICLE "Longform, ..."
            notes.append("T%s title says promo, vehicle doesn't: split X/LI?" % tn)
        return write(nums, persp, pieces, posts)

    def extra_lines(t, x, nums, notes, problems):
        tn = t.get("n")
        raw_p = x.get("perspective") or (t.get("perspective") if x.get("same_material") else None)
        if not raw_p:
            problems.append("T%s extra post has no perspective label: line says (TBD)" % tn)
        persp = perspective_text(raw_p, cfg, notes) if raw_p else "TBD"
        vehicle = x.get("vehicle") or t.get("vehicle_override") or t.get("vehicle") or "Long-form"
        notes.append("T%s extra post added (%s): confirm" % (tn, x.get("source") or "strategist request"))
        return write(nums, persp, *shape("%s+" % tn, persp, vehicle, 1, {}, notes))

    for t in data["topics"]:
        tn = t.get("n")
        ok, why = included(t, call, notes, problems)
        would = not ok and why in (NO_CALL_A, NOT_ANSWERED_A, NOT_DISCUSSED_A)
        clash = (ok or would) and type_clash(t, who, strategist)
        if clash:
            problems.append(clash)
        if t.get("inferred") and (ok or would):
            notes.append("T%s %s: inferred, not on the sheet: confirm" % (tn, t["inferred"]))
        if ok:
            entries += [{"topic": tn, "line": l} for l in topic_lines(t, tn, numbers_from, notes, problems)]
        else:
            left_out.append({"topic": tn, "why": why})
        if would:
            # as if the call happened and kept it; its own notes would only repeat what the line shows
            would_be.append({"topic": tn, "lines": topic_lines(t, tn, itertools.repeat("?"), [], []), "why": why})
            if t.get("written_answer"):
                # Josh D Oct Wk2 T3: "RECENT WINS JOSH SENT" pasted under PERSPECTIVE, no transcript
                notes.append("T%s left out, but the sheet holds %s's written answer (%s): answered in writing? add its line?"
                             % (tn, who, t["written_answer"]))
        for x in t.get("extra_posts") or []:      # strategist-requested extra posts follow their parent, in or out
            if ok:
                entries += [{"topic": "%s+" % tn, "line": l} for l in extra_lines(t, x, numbers_from, notes, problems)]
                continue
            # a left-out Type A topic's extra post needs the call's answers too: no real number
            left_out.append({"topic": "%s+" % tn, "why": "extra post on T%s, left out with it (%s)" % (tn, why)})
            if would:
                would_be[-1]["lines"] += extra_lines(t, x, itertools.repeat("?"), [], [])

    numbers = {re.match(r"(\d+)", e["line"]).group(1) for e in entries}
    if data.get("expected_posts") and len(numbers) != int(data["expected_posts"]):
        problems.append("%d posts made, the brief counts %s: check the lines" % (len(numbers), data["expected_posts"]))
    for e in entries:
        if "()" in e["line"]:
            problems.append("empty slot in line: %r" % e["line"])
    return {"entries": entries, "left_out": left_out, "would_be": would_be, "notes": notes, "problems": problems}

if __name__ == "__main__":
    print(json.dumps(build(json.load(open(sys.argv[1]))), ensure_ascii=False, indent=1))

#!/usr/bin/env python3
"""Check every call quote in a post-call brief against the transcript (SKILL.md Step 4.4, brief.md).

Usage: check_quotes.py TRANSCRIPT BRIEF.md [--sheet SHEET.txt ...] [--json]
  TRANSCRIPT  auto-detected; a saved tool result (JSON) is unwrapped to its text:
              - Fireflies (fireflies_fetch / fireflies_get_transcript): "[MM:SS - MM:SS] Speaker: text" lines,
                the first one may start "Sentences: "; H:MM:SS past the hour.
              - Kyle's pasted form (the task's "Google Drive / Google Docs" field): a "<Speaker> - MM:SS" line,
                then that turn's text, ending "Transcribed by https://fireflies.ai/"; page headers are dropped.
              - untimed (Granola, the Topics doc's third tab): "Me: ...", "Them: ...", "Kyle Meng: ..." lines,
                or a "Speaker:" line followed by its text. Lines above "Transcript:" are the header.
  BRIEF.md    the brief, markdown or plain text.
  --sheet     the topic sheet's text (read_file_content, or a saved read_doc). Repeat it for any other text the
              brief quotes (the Strategy tab, the Client Brain, the feedback ledger, sheet comments).
              Quotes in the Batch header and Original brief sections are checked only when it is given.
Each quote ("..." or curly) gets one status:
  ok          found in the transcript within its window (10 s slack), or anywhere when the transcript is
              untimed or the quote has no window
  WRONG TIME  found, but outside its window (prints where it is)
  SHEET       not in the transcript, found in --sheet (an Original brief quote: fine)
  NOT FOUND   in neither
Window: a time right after the quote, or right before it ('Kyle [30:53]: "..."'): [MM:SS–MM:SS] (en dash or
hyphen) as given, a lone [MM:SS] from there to a minute on. Otherwise the line's label time, which also covers
the bullets under it: the one in the bold label opening the line ("**The stupid (Q1) [09:16–10:51]:**"), or in
plain text a time in the line's first clause followed by ":" ("The setup [00:20–00:39]:"). Other times in a
line point elsewhere and set nothing. A quote of one or two words is a term: only a time next to it applies.
Matching ignores case, curly vs straight quotes and apostrophes, punctuation and spacing. Annotations
([likely "TAM", reading], [word missing], [garbled ...]) are removed first; a quote is split into fragments
on "..." / "…" and on any other bracket ("[former ecom brand, named on the call]"), and each fragment must
be found, in call order. Fragments under 3 words are ignored unless they are the whole quote. A quote that
matches only once repeated words are collapsed ("major, major" quoted as "major") is NOT FOUND, with a hint.
Not call quotes, skipped: headings, table rows, code blocks, the Longform doc and Sources sections, a reading
("cat goes up" reads as "CAC goes up"), a cited file ("Keval Shah — Client Feedback Ledger", Writer notes),
and quotes in bold labels unless a time follows them (a flag "**"100 million bucks" [01:42–01:44].**").
Also printed: "starts mid-sentence" warnings (not for a quote opening lowercase or with "..."), "no timestamp"
on an untimed quote under From the call, and the unfinished sentences inside quoted text (cut off with "-",
"—", "...", no end mark, or trailing off on "the", "my", "of" ...) for the brief's Flags.
Plain text by default, --json for machine output. Exits 1 when any quote is NOT FOUND or WRONG TIME.
"""
import bisect, json, re, sys

TS = r"\d{1,2}:\d{2}(?::\d{2})?"
TAG = re.compile(r"\[\s*(%s)(?:\s*[–—-]\s*(%s))?\s*\]" % (TS, TS))
SLACK = 10
FOLD = str.maketrans({"’": "'", "‘": "'", "ʼ": "'", "“": '"', "”": '"'})
FILLERS = set("yeah yes yep yup no nope so and but then like um uh okay ok well oh right cool sure perfect alright"
              .split())
FILLER_PAIRS = ("i mean", "you know", "for example")
OPEN_END = set("a an the my your our their his its and but or because cause if than whether".split())
PREP_END = set("of with to for from into like so".split())
WH = set("what where who whom which how why whatever".split())
COMPLETE_BEFORE = {"to": set("need needs want wants have has had got ought used able supposed".split()),
                   "like": set("look looks looked would you'd i'd we'd they'd".split()),
                   # "the last, like, week or so." (Keval Oct Wk3)
                   "so": set("think hope guess believe say said do did not or".split())}
ANNOT = re.compile(r"\s*\[(?:likely|probably|possibly|maybe|reading|word missing|words missing|word\(s\) missing"
                   r"|garbled|sic|inaudible|unclear|crosstalk)\b[^\]]*\]", re.I)
META = re.compile(r"(Meeting Title|Date|Meeting participants|Participants|Attendees|Title|Time|Duration|Id|DateString"
                  r"|Privacy|Speakers|Calendar Type|Meeting Link|Is Live|Organizer|Summary|Notes)\s*:", re.I)
SHEET_SECTIONS = ("batch header", "original brief")
OWN_SECTIONS = ("longform doc", "sources")
PLAIN_HEAD = re.compile(r"(original brief( \(topic sheet\))?|from the call|flags|other items from the call.*|open items.*"
                        r"|longform doc|how to read this brief|batch header.*|sources)\s*:?$|topic \d+\s*[—–-]\s", re.I)
BULLET = re.compile(r"\s*(?:[-*+•]|\d+[.)])\s+")
LABEL = re.compile(r"\s*(?:(?:[-*+•]|\d+[.)])\s+)?\*\*(.+?)\*\*")
READING = re.compile(r"(?:\breads? as|\blikely|\bprobably|\bshould read|\bi\.e\.,?"
                     r"|[\"”]\s*(?:\[[^\]]*\]\s*)?as)\s*$", re.I)
ORDER = "each fragment is there, but not in call order"
QUOTE = re.compile(r"[\"“]([^\"“”]*)[\"”]")


def tsec(t):
    s = 0
    for p in t.split(":"):
        s = s * 60 + int(p)
    return s


def window(m):
    """[MM:SS–MM:SS] as given; a lone [MM:SS] marks where the quoted passage starts, so it covers the next minute
    (Keval Oct Wk3: "Pretenders" and "fluff content" [20:47], the second said at 21:07)."""
    a = tsec(m.group(1))
    return (a, tsec(m.group(2)), m.group(0)) if m.group(2) else (a, a + 60, m.group(0))


def fmt(s):
    return "%d:%02d:%02d" % (s // 3600, s // 60 % 60, s % 60) if s >= 3600 else "%02d:%02d" % (s // 60, s % 60)


def words(s):
    return [w for w in (x.strip("'") for x in re.findall(r"[\w$%']+", s.translate(FOLD).lower())) if w]


def read_text(path):
    s = open(path, encoding="utf-8").read()
    try:
        d = json.loads(s)
    except ValueError:
        return s
    strs, runs = [], []
    def walk(x):
        if isinstance(x, str):
            strs.append(x)
        elif isinstance(x, dict) and "textRun" in x:
            runs.append(x["textRun"].get("content", ""))
        elif isinstance(x, (list, dict)):
            for v in (x.values() if isinstance(x, dict) else x):
                walk(v)
    walk(d)
    return "".join(runs) if runs else "\n".join(strs)     # a read_doc: only its text, runs glued


def collapse(ws):
    out = []
    for w in ws:
        out.append(w)
        for n in range(1, 13):
            if len(out) >= 2 * n and out[-n:] == out[-2 * n:-n]:
                del out[-n:]
                break
    return out


class Corpus:
    def __init__(self, ws):
        self.text, self.starts, pos = " " + " ".join(ws) + " ", [], 1
        for w in ws:
            self.starts.append(pos); pos += len(w) + 1

    def find(self, frag):
        pat, out = " " + " ".join(frag) + " ", []
        k = self.text.find(pat)
        while k >= 0:
            i = bisect.bisect_left(self.starts, k + 1)
            out.append((i, i + len(frag) - 1))
            k = self.text.find(pat, k + 1)
        return out


# ---------- transcript ----------

def parse_transcript(text):
    """-> (format, segments [{start, end, speaker, text}]); start/end in seconds, None when untimed."""
    ff = re.compile(r"(?:Sentences:\s*)?\[(%s)\s*-\s*(%s)\]\s*([^:\]]{1,80}?):\s?(.*)$" % (TS, TS))
    segs = [{"start": tsec(m.group(1)), "end": tsec(m.group(2)), "speaker": m.group(3).strip(), "text": m.group(4)}
            for m in (ff.match(l.strip()) for l in text.splitlines()) if m]
    if len(segs) >= 2:
        return "Fireflies", segs
    # Kyle's paste: page headers, footers and page numbers sit inside the text
    t = re.sub(r"Transcribed by https?://fireflies\.ai/?(\s*\d+\s*/\s*\d+)?", "\n", text)
    t = re.sub(r"Meeting Title:[^\n]*?(?:\n\s*)?Meeting created at:[^\n]*?\d{1,2}:\d{2}\s*[AP]M(\s*\d+\s*/\s*\d+)?",
               "\n", t)
    head = re.compile(r"\**\s*([^\s:*][^:*\n]{0,60}?)\s+-\s+(%s)\s*\**$" % TS)
    if sum(1 for l in t.splitlines() if head.match(l.strip())) < 2:
        # pasted with its line breaks lost: "Mason Littlejohn - 00:00 Sample. Kyle Meng - 07:19 Yeah. ..."
        name = r"(?:[A-Z][\w'’-]*|[A-Z]\.)"
        hits = list(re.finditer(r"(%s(?: %s){0,3}) - (%s)\b" % (name, name, TS), t))
        if len(hits) >= 2:
            cands = [h.group(1).split() for h in hits]
            count = {}
            for c in cands:
                for k in range(1, len(c) + 1):
                    count[" ".join(c[-k:])] = count.get(" ".join(c[-k:]), 0) + 1
            parts, last = [], 0
            for h, c in zip(hits, cands):
                nm = next((" ".join(c[-k:]) for k in range(len(c), 0, -1) if count[" ".join(c[-k:])] >= 2), " ".join(c))
                at = h.start(1) + len(h.group(1)) - len(nm)
                parts += [t[last:at], "\n%s - %s\n" % (nm, h.group(2))]
                last = h.end()
            t = "".join(parts) + t[last:]
    turns, cur = [], None
    for l in t.splitlines():
        m = head.match(l.strip())
        if m:
            cur = {"start": tsec(m.group(2)), "speaker": m.group(1).strip(), "text": ""}
            turns.append(cur)
        elif cur is not None and l.strip() and not re.fullmatch(r"\d+\s*/\s*\d+", l.strip()):
            cur["text"] += " " + l.strip()
    if len(turns) >= 2:
        for a, b in zip(turns, turns[1:] + [None]):
            a["end"] = max(a["start"], b["start"]) if b else a["start"] + 120
        return "Fireflies (pasted)", turns
    lines = text.splitlines()
    start = next((i + 1 for i, l in enumerate(lines) if re.fullmatch(r"\s*Transcript:\s*", l)), 0)
    spk = re.compile(r"((?:[A-Z][\w.'’-]*)(?: [A-Z][\w.'’-]*){0,3}):(?:\s+(.*))?$")
    segs, who = [], "?"
    for l in lines[start:]:
        l = l.strip()
        if not l or (not start and META.match(l)):
            continue
        m = spk.match(l)
        if m:
            who = m.group(1)
            if m.group(2):
                segs.append({"start": None, "end": None, "speaker": who, "text": m.group(2)})
        else:
            segs.append({"start": None, "end": None, "speaker": who, "text": l})
    return "untimed", segs


class Transcript:
    def __init__(self, text):
        self.format, self.segs = parse_transcript(text)
        self.timed = bool(self.segs) and self.segs[0]["start"] is not None
        self.sents, ws, self.wseg, self.wsent = [], [], [], []
        for si, sg in enumerate(self.segs):
            for st in re.split(r"(?<=[.?!…])\s+", sg["text"].strip()):
                sw = words(st)
                if sw:
                    self.sents.append({"seg": si, "text": st, "first": len(ws)})
                    for w in sw:
                        ws.append(w); self.wseg.append(si); self.wsent.append(len(self.sents) - 1)
        self.words, self.corpus = ws, Corpus(ws)
        ends = [sg["text"].rstrip().rstrip("\"'”’)") for sg in self.segs if sg["text"].strip()]
        # Fireflies ends every line with punctuation, so a bare ending there is a cut-off
        # ("Me: Oh man. I, I", Josh C Oct Wk2)
        self.punctuated = bool(ends) and sum(1 for e in ends if re.search(r"[.?!…-]$", e)) >= 0.9 * len(ends)

    def span(self, i, j):
        a, b = self.segs[self.wseg[i]], self.segs[self.wseg[j]]
        return a["start"], b["end"]

    def where(self, i):
        sg = self.segs[self.wseg[i]]
        return ((fmt(sg["start"]) + " ") if self.timed else "") + sg["speaker"]

    def unfinished(self, k):
        t = self.sents[k]["text"].strip().rstrip("\"'”’)")
        if re.search(r"(--|[-–—…]|\.\.\.)$", t):
            return True
        if self.punctuated and not re.search(r"[.?!]$", t):
            return True
        sw = words(t)
        if not sw or t.endswith("?"):
            return False
        last, prev = sw[-1], sw[-2] if len(sw) > 1 else ""
        if last in OPEN_END:
            return True
        # a stranded preposition ends a question or a relative clause
        # ("the company that you bought from", Josh C Oct Wk2)
        rel = re.search(r"\b(that|which|who) (i|you|we|they|he|she|people)\b", t.lower())
        return last in PREP_END and not WH & set(sw) and not rel and prev not in COMPLETE_BEFORE.get(last, ())

    def mid_sentence(self, i, j):
        """True when words other than fillers, or a stutter of the quote's opening ("I, I can"), precede it."""
        before = " %s " % " ".join(self.words[self.sents[self.wsent[i]]["first"]:i])
        for pair in FILLER_PAIRS:
            before = before.replace(" %s " % pair, " ")
        return any(w not in FILLERS and w not in self.words[i:min(j, i + 3) + 1] for w in before.split())


# ---------- brief ----------

def quotes_in(brief):
    """Yield (line no, section, quote, its own window, the label window over it, in a sheet section)."""
    section, cur, code = "", None, False
    for n, raw in enumerate(brief.splitlines(), 1):
        line = raw.rstrip()
        if line.lstrip().startswith("```"):
            code = not code
            continue
        bare = re.sub(r"\*\*", "", line).strip()
        if code or not bare:
            continue
        if line.lstrip().startswith("#") or (len(bare) <= 160 and PLAIN_HEAD.match(bare)):
            section, cur = bare.lstrip("#").strip().lower(), None
            continue
        if bare.startswith("|") or section.startswith(OWN_SECTIONS):
            continue
        lab = LABEL.match(line)
        found, label_ts = [], []
        for which, txt in (("label", lab.group(1) if lab else ""), ("rest", line[lab.end():] if lab else line)):
            txt = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", txt)          # markdown link -> its text
            txt = ANNOT.sub("", txt)
            txt = re.sub(r"\[(?!\s*%s\s*(?:[–—-]\s*%s\s*)?\])[^\[\]]*\]" % (TS, TS), "\x00", txt)
            # a label's time covers the line and the bullets under it: "**The stupid (Q1) [09:16–10:51]:**", or
            # in plain text a time in the line's first clause followed by ":",
            # '... and "so much closer" [08:07–09:41]:' (Caulen Oct Wk2); a later "Kyle [30:53]:" only
            # introduces its quote (Keval Oct Wk3)
            is_label = lambda t: which == "label" or not lab and bool(
                re.match(r"[^\"“”\[\],;.\n]{0,40}?\**\s*:", txt[t.end():])
                and not re.search(r"[.;!?]\s", txt[:t.start()]))
            used = set()
            for m in QUOTE.finditer(txt):
                if READING.search(txt[:m.start()]):
                    continue                                          # "cat goes up" reads as "CAC goes up"
                if txt[:m.start()].endswith("(") and txt[m.end():m.end() + 1] == ",":
                    continue                      # a cited file: ("Keval Shah — Client Feedback Ledger", Writer notes)
                tag = TAG.match(txt, m.end() + re.match(r"[\s.,;:!?)]*", txt[m.end():]).end())
                if which == "label":
                    # a flag's quote with its time, which stays the line's label time:
                    # **"100 million bucks" [01:42–01:44].** (Caulen Oct Wk2); an untimed one is a title
                    if tag:
                        found.append((m.group(1), window(tag)))
                    continue
                if not tag or tag.start() in used or is_label(tag):
                    # "Kyle [30:53]: "..."; a label time right before it times it too, without being used up:
                    # Kyle [12:41]: "That's perfect." (Mason Oct Wk2)
                    tag = re.search(TAG.pattern + r"[\s:*]*$", txt[:m.start()])
                    tag = tag and TAG.match(txt, tag.start())
                    tag = tag if tag and tag.start() not in used else None
                if tag and not is_label(tag):
                    used.add(tag.start())
                found.append((m.group(1), window(tag) if tag else None))
            label_ts += [t for t in TAG.finditer(txt) if t.start() not in used and is_label(t)]
        # other loose times in a line point elsewhere (Mason Oct Wk2: The "bloodline" line [23:29] repeats
        # Topic 3's close ("eliminate that out of my bloodline"), said at 20:14)
        own = window(label_ts[0]) if len(label_ts) == 1 else None
        if len(label_ts) > 1:
            lo, hi = min(window(t)[0] for t in label_ts), max(window(t)[1] for t in label_ts)
            own = (lo, hi, "[%s–%s]" % (fmt(lo), fmt(hi)))
        if lab or (own and not BULLET.match(line)):
            cur = own
        for q, win in found:
            yield n, section, q, win, own or cur, section.startswith(SHEET_SECTIONS)


def fragments(q):
    fr = [words(f) for f in re.split(r"\.\.\.|…|\x00", q)]
    fr = [f for f in fr if f]
    return [f for f in fr if len(f) >= 3] or fr          # all short: check them all, never skip the quote


def place(tr, frs, win):
    """First in-order placement of all fragments, preferring one inside the window. -> (placement, missing)"""
    occ = [tr.corpus.find(f) for f in frs]
    missing = [" ".join(f) for f, o in zip(frs, occ) if not o]
    if missing:
        return None, missing
    inwin = lambda o: win is None or not tr.timed or (
        tr.span(*o)[0] <= win[1] + SLACK and tr.span(*o)[1] >= win[0] - SLACK)
    best, dead = [None], set()
    def go(k, after, acc, all_in):
        if k == len(occ):
            if all_in:
                return acc
            best[0] = best[0] or acc
            return None
        if (k, after, all_in) in dead:
            return None
        for o in sorted((o for o in occ[k] if o[0] > after), key=lambda o: not inwin(o)):
            r = go(k + 1, o[1], acc + [o], all_in and inwin(o))
            if r:
                return r
        dead.add((k, after, all_in))
        return None
    got = go(0, -1, [], True)
    return (got, []) if got else (best[0], [] if best[0] else [ORDER])


def check(tr, brief, sheet):
    sheet_c = Corpus(words(sheet)) if sheet is not None else None
    collapsed = None
    out, skipped = [], 0
    for n, section, q, win, over, in_sheet in quotes_in(brief):
        frs = fragments(q)
        if not frs:
            continue
        if win is None and len(words(q)) >= 3:
            win = over                                                # a word or two is a term, not a timed quote
        if in_sheet and sheet_c is None:
            skipped += 1
            continue
        r = {"line": n, "section": section, "quote": q.strip(), "status": "", "found_at": [], "detail": "",
             "window": win and win[2], "warnings": [], "sents": []}
        pl, missing = place(tr, frs, win)
        if pl:
            r["found_at"] = [tr.where(o[0]) for o in pl]
            timed_win = win is not None and tr.timed
            ok = not timed_win or all(tr.span(*o)[0] <= win[1] + SLACK and tr.span(*o)[1] >= win[0] - SLACK for o in pl)
            r["status"] = "ok" if ok else "WRONG TIME"
            if not ok:
                r["found_at"] = sorted({tr.where(o[0]) for o in tr.corpus.find(frs[0])})
            # a quote opening lowercase or with an ellipsis says it is partial; a capital that isn't the
            # sentence's start can hide a dropped clause ("like I posted previously", Caulen Oct Wk2)
            if len(words(q)) >= 4 and tr.mid_sentence(*pl[0]) and not re.match(r"\s*(\.\.\.|…|[a-z])", q):
                s = tr.sents[tr.wsent[pl[0][0]]]
                r["warnings"].append("starts mid-sentence: %s: \"%s\"" % (tr.where(pl[0][0]), s["text"]))
            if tr.timed and win is None and section == "from the call":
                r["warnings"].append("no timestamp")
            r["sents"] = sorted({tr.wsent[i] for o in pl for i in range(o[0], o[1] + 1)})
        elif sheet_c is not None and all(sheet_c.find(f) for f in frs):
            r["status"] = "SHEET"
        else:
            r["status"] = "NOT FOUND"
            r["detail"] = ORDER if missing == [ORDER] else "no match for \"%s\"" % "\", \"".join(missing)
            if missing != [ORDER]:
                # Caulen Oct Wk2: "major, major initiatives" quoted as "major initiatives"
                collapsed = collapsed or Corpus(collapse(tr.words))
                if all(collapsed.find(collapse(f)) for f in frs):
                    r["detail"] = ("matches only with repeated words collapsed: quote the words as transcribed,"
                                   " cut a stutter only with \"…\"")
        out.append(r)
    unf = {}
    for r in out:
        for k in r.pop("sents"):
            if tr.unfinished(k):
                i = tr.sents[k]["first"]
                u = unf.setdefault(k, {"at": tr.where(i), "sentence": tr.sents[k]["text"], "lines": []})
                u["lines"].append(r["line"])
    return out, [unf[k] for k in sorted(unf)], skipped


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    if as_json:
        a.remove("--json")
    sheet = None
    while "--sheet" in a:
        i = a.index("--sheet"); sheet = (sheet or "") + "\n" + read_text(a[i + 1]); del a[i:i + 2]
    if len(a) != 2:
        sys.exit(__doc__)
    tr = Transcript(read_text(a[0]))
    if not tr.segs:
        sys.exit("no transcript lines found in %s" % a[0])
    res, unf, skipped = check(tr, read_text(a[1]), sheet)
    counts = {s: sum(1 for r in res if r["status"] == s) for s in ("ok", "WRONG TIME", "SHEET", "NOT FOUND")}
    ok = not counts["WRONG TIME"] and not counts["NOT FOUND"]
    if as_json:
        print(json.dumps({"transcript": {"format": tr.format, "segments": len(tr.segs), "timed": tr.timed},
                          "quotes": res, "unfinished": unf, "skipped": skipped, "counts": counts, "pass": ok},
                         ensure_ascii=False, indent=1))
    else:
        print("transcript: %s, %d %s" % (tr.format, len(tr.segs), "lines" if tr.timed else "lines, no timestamps"))
        for r in res:
            q = r["quote"] if len(r["quote"]) <= 80 else r["quote"][:77] + "..."
            extra = {"ok": "at " + ", ".join(r["found_at"][:2]),
                     "WRONG TIME": "found at " + ", ".join(r["found_at"][:4]),
                     "SHEET": "on the sheet", "NOT FOUND": r["detail"]}[r["status"]]
            win = (r["window"] + " ") if r["window"] else ""
            print("L%-4d %-10s  %s\"%s\"  (%s)" % (r["line"], r["status"], win, q, extra))
        warns = [(r["line"], w) for r in res for w in r["warnings"]]
        if warns:
            print("warnings:")
            for n, w in warns:
                print("  L%d %s" % (n, w))
        if unf:
            print("unfinished sentences (flag them in the brief):")
            for u in unf:
                print("  %s: \"%s\"  (quoted at L%s)" % (u["at"], u["sentence"], ", L".join(map(str, u["lines"]))))
        if skipped:
            print("%d sheet quotes skipped (Batch header, Original brief): pass --sheet to check them" % skipped)
        print("%d quotes: %s" % (len(res), ", ".join("%d %s" % (v, k) for k, v in counts.items())))
        print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

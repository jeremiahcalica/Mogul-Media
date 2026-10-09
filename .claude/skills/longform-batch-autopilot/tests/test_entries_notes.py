#!/usr/bin/env python3
"""entries.py's notes, problems and would_be on small synthetic sheets: Ben's value tweets, inferred fields,
type clashes, post-count sources, freeform EXTRA posts, would-be lines for left-out Type A topics, written
answers, Josh C's promo titles, the X article qualifier, merged format-noun brackets, extra posts that
follow a left-out parent, and the Oct 10 audit fixes (type and status reading, snipes, extra-post counts).
Run: python3 -I tests/test_entries_notes.py"""
import json, os, shutil, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
script = os.path.join(here, "..", "scripts", "entries.py")
tmp = tempfile.mkdtemp()
fails = []


def run(topics, **top):
    data = dict({"client": "Test", "platforms": "X, LinkedIn", "call": True}, **top)
    if data["call"] is None:                     # call=None: no "call" key at all
        del data["call"]
    data["topics"] = [dict({"title": "t%s" % t["n"], "vehicle": "Long-form", "perspective": "P%s." % t["n"],
                            "status": "KEPT", "type": "A"}, **t) for t in topics]
    p = os.path.join(tmp, "topics.json")
    json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return json.loads(subprocess.run([sys.executable, "-I", script, p], capture_output=True, text=True, check=True).stdout)


def check(name, cond, out=None):
    if not cond:
        fails.append(name)
        print("   FAIL", name, json.dumps(out, ensure_ascii=False)[:600] if out is not None else "")


lines = lambda o: [e["line"] for e in o["entries"]]

# 1. Ben value tweets stay one X/LI line unless a FOR LINKEDIN note sets the LI format
o = run([{"n": 1, "vehicle": "Value tweet", "posts": 2},
         {"n": 2, "label": "VT", "vehicle": "Listicle"},
         {"n": 3, "vehicle": "Value tweet", "li_vehicle": "Listicle"},
         {"n": 4, "vehicle": "Medium form"},
         {"n": 5, "vehicle": "Medium form", "no_cta": True}], client="Ben K.")
check("ben value tweet unsplit", lines(o) == [
    "1 - (X/LI) - (P1) - (Value tweet)", "2 - (X/LI) - (P1) - (Value tweet)", "3 - (X/LI) - (P2) - (Listicle)",
    "4.1 - (X) - (P3) - (Value tweet)", "4.2 - (LI) - (P3) - (Listicle)",
    "5.1 - (X) - (P4) - (Medium-form)", "5.2 - (LI) - (P4) - (Medium-form)", "6 - (X/LI) - (P5) - (Medium-form)"], o)
check("ben value tweet note", o["notes"].count("T1 kept X/LI (value tweet; split only with a FOR LINKEDIN note): confirm") == 1
      and "T2 kept X/LI (value tweet; split only with a FOR LINKEDIN note): confirm" in o["notes"]
      and "T4 split X / LI (this client splits posts with a DM CTA): confirm" in o["notes"], o)

# 2. inferred
o = run([{"n": 1, "inferred": "vehicle and post count from the heading"}])
check("inferred note", "T1 vehicle and post count from the heading: inferred, not on the sheet: confirm" in o["notes"], o)

# 3. type clash, call or no call; a Type A box asking a question is no clash
for call in (True, False):
    o = run([{"n": 1, "type": "A", "other_tab_type": "B"}, {"n": 2, "type": "B", "client_question": True},
             {"n": 3, "type": "B", "other_tab_type": "A", "client_question": True},
             {"n": 4, "type": "A", "client_question": True}, {"n": 5, "type": "B", "other_tab_type": "B"}],
            client="Lior P.", strategist="Kyle", call=call)
    check("type clash call=%s" % call, o["problems"] == [
        "T1 type clash: Client strategy says Type A, Strategy tab says Type B: line follows Client strategy, confirm with Kyle",
        "T2 type clash: Client strategy says Type B, the box asks Lior a question: line follows Client strategy, confirm with Kyle",
        "T3 type clash: Client strategy says Type B, Strategy tab says Type A and the box asks Lior a question: line follows "
        "Client strategy, confirm with Kyle"], o)
o = run([{"n": 1, "type": "B", "client_question": True}])
check("type clash default names", o["problems"] == ["T1 type clash: Client strategy says Type B, the box asks Test a question: "
                                                    "line follows Client strategy, confirm with the strategist"], o)

# 4. post count source
o = run([{"n": 4, "posts_override": 2, "posts_override_source": "Kyle's sheet comment \"2 posts\""}, {"n": 5, "posts_override": 3}])
check("posts override source", 'T4 post count 2 from Kyle\'s sheet comment "2 posts": confirm' in o["notes"]
      and "T5 post count set on the call: 3" in o["notes"] and len(lines(o)) == 5, o)

# 5. freeform EXTRA: flagged, integer number after the sheet topics, label of 1-3 words
o = run([{"n": 1, "type": "B"},
         {"n": 2, "type": None, "freeform": True, "perspective": None, "perspective_override": "Trybe", "vehicle": "Long-form"},
         {"n": 3, "type": None, "freeform": True, "perspective": None,
          "perspective_override": "15 creators in 7 days: what I learned using Trybe", "vehicle": "Long-form"}], call=False)
check("freeform lines", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)", "2 - (X/LI) - (Trybe) - (Long-form)",
                                     "3 - (X/LI) - (15 creators in 7 days: what I learned using Trybe) - (Long-form)"], o)
check("freeform notes", "freeform extra post T2 (Trybe): confirm" in o["notes"]
      and not [n for n in o["notes"] if "perspective is a label" in n], o)
check("freeform label problem", o["problems"] == ["T3 freeform label '15 creators in 7 days: what I learned using Trybe': "
                                                  "label should be a 1-3 word subject, as in Jeremiah's 'Trybe'"], o)

# 6. would_be: Type A left out for want of answers only; "?" numbers never move the real ones
o = run([{"n": 1, "status": "KEPT"},
         {"n": 2, "status": "NOT ANSWERED (no take given)", "vehicle": "Thread"},
         {"n": 3, "status": "NOT DISCUSSED", "posts": 2},
         {"n": 4, "status": "KILLED"}, {"n": 5, "struck": True}, {"n": 6, "check": "❌"}, {"n": 7, "label": "Snipe"},
         {"n": 8, "merged_into": 1}, {"n": 9, "status": "PARKED"}, {"n": 10, "status": "ON HOLD"},
         {"n": 11, "type": "B", "status": "NOT DISCUSSED"},
         {"n": 12, "status": "NOT DISCUSSED", "vehicle": "X article, then quote tweet"}])
check("would_be real lines", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)", "2 - (X/LI) - (P11) - (Long-form)"], o)
check("would_be", o["would_be"] == [
    {"topic": 2, "lines": ["?.1 - (X) - (P2) - (Thread)", "?.2 - (LI) - (P2) - (Long-form)"], "why": "Type A, not answered on the call"},
    {"topic": 3, "lines": ["? - (X/LI) - (P3) - (Long-form)", "? - (X/LI) - (P3) - (Long-form)"],
     "why": "Type A, not discussed on the call (no answers to write from)"},
    {"topic": 12, "lines": ["? - (X) - (P12) - (Article)", "? - (X) - (P12) - (Article wrapper)"],
     "why": "Type A, not discussed on the call (no answers to write from)"}], o)
o = run([{"n": 1, "type": "A"}, {"n": 2, "type": "B"}, {"n": 3, "type": "A", "label": "Quick Response"}], call=False)
check("would_be no transcript", lines(o) == ["1 - (X/LI) - (P2) - (Long-form)"] and o["would_be"] == [
    {"topic": 1, "lines": ["? - (X/LI) - (P1) - (Long-form)"], "why": "Type A, no transcript to show the call answered it"}], o)

# 7. written answer on a left-out Type A topic
o = run([{"n": 3, "written_answer": "RECENT WINS JOSH SENT + image"}, {"n": 4, "type": "B", "written_answer": "x"},
         {"n": 5, "struck": True, "written_answer": "y"}], client="Josh D.", call=False)
check("written answer", [n for n in o["notes"] if "written answer" in n] == [
    "T3 left out, but the sheet holds Josh's written answer (RECENT WINS JOSH SENT + image): answered in writing? add its line?"], o)

# 8. Josh C: promo in the title but not the vehicle
o = run([{"n": 7, "title": "A Day in My Life on the Road (Ecom North Toronto Promo)", "vehicle": "Longform, day-in-the-life"},
         {"n": 8, "title": "Ecom North (Promo)", "vehicle": "Longform promo"}], client="Joshua C.")
check("promo title", [n for n in o["notes"] if "promo" in n.lower() and "title" in n] == [
    "T7 title says promo, vehicle doesn't: split X/LI?"], o)
o = run([{"n": 7, "title": "Toronto (Promo)", "vehicle": "Longform"}])
check("promo title other client", not [n for n in o["notes"] if "title says promo" in n], o)

# 9. X article: the dropped qualifier is quoted
o = run([{"n": 1, "type": "B", "vehicle": "X Article (long form, sectioned, 10–15K characters)"}], platforms="X")
check("article qualifier", lines(o) == ["1 - (X) - (P1) - (Article)"] and any(
    "qualifier dropped: '(long form, sectioned, 10–15K characters)'" in n for n in o["notes"]), o)

# 10. a single format noun in brackets merges, flagged
o = run([{"n": 2, "vehicle": "Short form (listicle)"}])
check("bracket merge", lines(o) == ["1 - (X/LI) - (P2) - (Short-form listicle)"]
      and "format noun in brackets merged into the vehicle: (listicle): confirm" in o["notes"], o)

# review fixes: plural VTs, "Type A" spelled out, no clash on a topic out for another reason, extra posts follow
# their parent out (and into would_be), a non-integer freeform number, promo note only on an unsplit line
o = run([{"n": 1, "vehicle": "2 VTs"}], client="Ben K.")
check("ben VTs unsplit", lines(o) == ["1 - (X/LI) - (P1) - (2 VTs)"], o)
o = run([{"n": 1, "type": "B", "other_tab_type": "Type A"}, {"n": 2, "status": "KILLED", "other_tab_type": "B"},
         {"n": 3, "struck": True, "other_tab_type": "B"}, {"n": 4, "label": "Snipe", "other_tab_type": "B"}])
check("type clash only where the type decides", o["problems"] == [
    "T1 type clash: Client strategy says Type B, Strategy tab says Type A: line follows Client strategy, confirm with "
    "the strategist"], o)
for call, status in ((False, "KEPT"), (True, "NOT ANSWERED")):
    o = run([{"n": 1, "status": status, "extra_posts": [{"perspective": "Chad mentality", "source": "Kyle comment"}]},
             {"n": 2, "type": "B"}], call=call)
    check("extra post follows a left-out parent call=%s" % call, lines(o) == ["1 - (X/LI) - (P2) - (Long-form)"]
          and o["would_be"][0]["lines"] == ["? - (X/LI) - (P1) - (Long-form)", "? - (X/LI) - (Chad mentality) - (Long-form)"]
          and {"topic": "1+", "why": "extra post on T1, left out with it (%s)" % o["left_out"][0]["why"]} in o["left_out"], o)
o = run([{"n": 1, "status": "KILLED", "extra_posts": [{"perspective": "Chad"}]}])
check("extra post follows a killed parent", lines(o) == [] and o["would_be"] == [] and len(o["left_out"]) == 2, o)
o = run([{"n": "EXRA", "type": None, "freeform": True, "perspective": None, "perspective_override": "Trybe"}], call=False)
check("freeform number", "TEXRA freeform topic number should be an integer, the next after the sheet topics" in o["problems"], o)
o = run([{"n": 1, "title": "Toronto (Promo)", "vehicle": "Medium form (X) / Long form (LI)"}], client="Joshua C.")
check("promo title, already split", not [n for n in o["notes"] if "title says promo" in n], o)
o = run([{"n": 1, "type": "B", "vehicle": "X Article: sectioned"}], platforms="X")
check("article qualifier punctuation", any("qualifier dropped: 'sectioned'" in n for n in o["notes"]), o)

# audit, Oct 10
# 1. the type as the sheet header writes it ("TOPIC N | TYPE B"); a missing or unreadable type on a sheet topic
o = run([{"n": 1, "type": "TYPE B", "status": "NOT DISCUSSED"}, {"n": 2, "type": "Type B", "status": "NOT ANSWERED"},
         {"n": 3, "type": "TYPE A  2 POSTS", "status": "NOT DISCUSSED"}, {"n": 4, "type": "B, 2 posts", "status": "NOT DISCUSSED"},
         {"n": 5, "type": None, "status": "NOT DISCUSSED"}, {"n": 6, "type": "C", "status": "NOT DISCUSSED"},
         {"n": 7, "type": None, "freeform": True, "perspective": None, "perspective_override": "Trybe"},
         {"n": 8, "type": None, "status": "NEW: agreed on the call"}])
check("type read", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)", "2 - (X/LI) - (P2) - (Long-form)",
                                "3 - (X/LI) - (P4) - (Long-form)", "4 - (X/LI) - (P5) - (Long-form)",
                                "5 - (X/LI) - (Trybe) - (Long-form)", "6 - (X/LI) - (P8) - (Long-form)"]
      and [w["topic"] for w in o["would_be"]] == [3, 6], o)
check("type problems", o["problems"] == ["T5 type missing/unreadable (None, treated as Type B): check",
                                         "T6 type missing/unreadable ('C', treated as Type A): check"], o)
o = run([{"n": 1, "type": "TYPE B"}, {"n": 2, "type": "Type A"}], call=False)
check("type read, no transcript", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)"]
      and [w["topic"] for w in o["would_be"]] == [2] and o["problems"] == [], o)
o = run([{"n": 1, "type": "Type B", "other_tab_type": "TYPE A"}, {"n": 2, "type": "TYPE B", "other_tab_type": "Type B"}])
check("type clash, spelled out", o["problems"] == [
    "T1 type clash: Client strategy says Type B, Strategy tab says Type A: line follows Client strategy, confirm with "
    "the strategist"], o)

# 2. COVERED only when the status starts with it
o = run([{"n": 1, "status": "KILLED (already covered in last week's post)"},
         {"n": 2, "status": "NOT DISCUSSED (material covered in T2's section)"},
         {"n": 3, "status": "NOT ANSWERED, covered above"},
         {"n": 4, "status": "COVERED (already touched on at 12:40)"},
         {"n": 5, "status": "Already touched on earlier in the call"}])
check("covered anchored", lines(o) == ["1 - (X/LI) - (P4) - (Long-form)", "2 - (X/LI) - (P5) - (Long-form)"]
      and [w["topic"] for w in o["would_be"]] == [2, 3]
      and {"topic": 1, "why": "killed on the call"} in o["left_out"], o)

# 3. a status it can't read: Type A out with a would-be line, Type B in, both problems; no "call" key
o = run([{"n": 1, "status": "Partially answered"}, {"n": 2, "status": ""}, {"n": 3, "status": None},
         {"n": 4, "type": "B", "status": "Partially answered"}])
check("unknown status", lines(o) == ["1 - (X/LI) - (P4) - (Long-form)"]
      and [(w["topic"], w["lines"]) for w in o["would_be"]] == [(n, ["? - (X/LI) - (P%s) - (Long-form)" % n]) for n in (1, 2, 3)]
      and o["problems"] == ["T1 status 'Partially answered' not recognised: left out, check",
                            "T2 status '' not recognised: left out, check",
                            "T3 status None not recognised: left out, check",
                            "T4 status 'Partially answered' not recognised: included, check"], o)
o = run([{"n": 1}, {"n": 2, "status": "NOT DISCUSSED"}], call=None)
check("no call key", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)"]
      and o["problems"] == ['no "call" key: assumed the call happened; set it'], o)

# 4. "skipped" means not reached (Jeremiah, Oct 9, 22:51): NOT DISCUSSED, unless it also says killed or dropped
o = run([{"n": 1, "type": "B", "status": "Skipped on call"}, {"n": 2, "status": "Skipped on call"},
         {"n": 3, "type": "B", "status": "Skipped on call, killed"}, {"n": 4, "type": "B", "status": "SKIPPED (dropped by Kyle)"}])
check("skipped", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)"]
      and o["would_be"] == [{"topic": 2, "lines": ["? - (X/LI) - (P2) - (Long-form)"],
                             "why": "Type A, not discussed on the call (no answers to write from)"}]
      and [x["why"] for x in o["left_out"] if x["topic"] in (3, 4)] == ["killed on the call"] * 2, o)

# 5. BLOCKED: answered and waiting on an asset is in; waiting on the answer is NOT ANSWERED
o = run([{"n": 1, "status": "BLOCKED (answered; waiting on the video)"},
         {"n": 2, "status": "BLOCKED (answers given, sign-off pending)"},
         {"n": 3, "status": "BLOCKED (answer given, photo pending)"},
         {"n": 4, "status": "BLOCKED (not answered, infographics from Sean)"}, {"n": 5, "status": "BLOCKED (Keval's answer)"},
         {"n": 6, "status": "BLOCKED (deferred to next call)"}, {"n": 7, "status": "BLOCKED (async)"},
         {"n": 8, "status": "BLOCKED (defer)"}])
check("blocked", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)", "2 - (X/LI) - (P2) - (Long-form)",
                              "3 - (X/LI) - (P3) - (Long-form)"]
      and [w["topic"] for w in o["would_be"]] == [4, 5, 6, 7, 8]
      and {w["why"] for w in o["would_be"]} == {"Type A, not answered on the call"}, o)

# 6. snipes in the call's vehicle, the sheet's vehicle or the status
o = run([{"n": 1, "vehicle_override": "Snipe (QT)"}, {"n": 2, "vehicle": "Quick Response post"},
         {"n": 3, "vehicle": "Quote tweet snipe"}, {"n": 4, "status": "KEPT (snipe)"},
         {"n": 5, "status": "KEPT (quick response)"},
         {"n": 6, "vehicle": "Snipe (quote tweet)", "vehicle_override": "Long-form"}, {"n": 7, "vehicle": "Quote tweet"}])
check("snipes", lines(o) == ["1 - (X/LI) - (P6) - (Long-form)", "2 - (X/LI) - (P7) - (Quote tweet)"]
      and [x["topic"] for x in o["left_out"] if x["why"].startswith("snipe")] == [1, 2, 3, 4, 5]
      and o["would_be"] == [], o)

# 7. an extra post is one post, whatever the parent's VEHICLE count; a VEHICLE count is a double-count check too
o = run([{"n": 1, "vehicle": "Thread, x2", "extra_posts": [{"perspective": "Chad mentality", "source": "Kyle comment"}]},
         {"n": 2, "extra_posts": [{"perspective": "Second", "vehicle": "Value tweet, x2"}]},
         {"n": 3, "posts": 2, "vehicle": "Long-form, x2", "extra_posts": [{"perspective": "Third"}]}])
check("extra post count", lines(o) == [
    "1.1 - (X) - (P1) - (Thread)", "1.2 - (LI) - (P1) - (Long-form)", "2.1 - (X) - (P1) - (Thread)",
    "2.2 - (LI) - (P1) - (Long-form)", "3.1 - (X) - (Chad mentality) - (Thread)", "3.2 - (LI) - (Chad mentality) - (Long-form)",
    "4 - (X/LI) - (P2) - (Long-form)", "5 - (X/LI) - (Second) - (Value tweet)", "6 - (X/LI) - (Second) - (Value tweet)",
    "7 - (X/LI) - (P3) - (Long-form)", "8 - (X/LI) - (P3) - (Long-form)", "9 - (X/LI) - (Third) - (Long-form)"], o)
check("extra post double count", o["problems"] == [
    "T1 has a VEHICLE count (2 posts) and extra posts too: a comment naming each post's subject is not extra posts, "
    "check for double counting",
    "T3 has a header and VEHICLE count (2 posts) and extra posts too: a comment naming each post's subject is not "
    "extra posts, check for double counting"], o)
o = run([{"n": 1, "status": "NOT DISCUSSED", "vehicle": "Long-form, x2", "extra_posts": [{"perspective": "Chad"}]}])
check("extra post count, would-be", o["would_be"][0]["lines"] == [
    "? - (X/LI) - (P1) - (Long-form)", "? - (X/LI) - (P1) - (Long-form)", "? - (X/LI) - (Chad) - (Long-form)"], o)

# review of the audit fixes, Oct 10
# "not killed" in a skipped status doesn't kill it (brief.md's Note: "Status is open, not killed."); "kill it" does
o = run([{"n": 1, "type": "B", "status": "Skipped on call. Status is open, not killed."},
         {"n": 2, "type": "B", "status": "Skipped (not dropped, not reached)"},
         {"n": 3, "type": "B", "status": "Skipped, Kyle said kill it"}, {"n": 4, "type": "B", "status": "Skipped (Dropbox link)"}])
check("skipped, not killed", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)", "2 - (X/LI) - (P2) - (Long-form)",
                                          "3 - (X/LI) - (P4) - (Long-form)"]
      and [x["why"] for x in o["left_out"]] == ["killed on the call"], o)
# BLOCKED waiting on the answers, in any wording, is NOT ANSWERED
o = run([{"n": 1, "status": "BLOCKED (waiting on answers)"}, {"n": 2, "status": "BLOCKED (answers pending)"},
         {"n": 3, "status": "BLOCKED (to be answered by email)"}, {"n": 4, "status": "BLOCKED (needs answering)"},
         {"n": 5, "status": "BLOCKED (not yet answered)"}, {"n": 6, "status": "BLOCKED (waiting on Josh's take)"},
         {"n": 7, "status": "BLOCKED (answers in, photo pending)"}, {"n": 8, "status": "BLOCKED (Kyle to take a look)"},
         {"n": 9, "status": "BLOCKED (take given, video pending)"}])
check("blocked on answers", lines(o) == ["1 - (X/LI) - (P7) - (Long-form)", "2 - (X/LI) - (P8) - (Long-form)",
                                         "3 - (X/LI) - (P9) - (Long-form)"]
      and [w["topic"] for w in o["would_be"]] == [1, 2, 3, 4, 5, 6], o)
# a Type A status that reads KEPT but says the call never reached it (Ben K Oct Wk2 T1's wording, a Type B)
o = run([{"n": 1, "status": "KEPT as written. Not discussed on the call."}, {"n": 2, "status": "PIVOT — unanswered"},
         {"n": 3, "type": "B", "status": "KEPT as written. Not discussed on the call."},
         {"n": 4, "status": "KEPT angle and vehicle. Ben answered Question 1 on the call. Question 2 was not asked."},
         {"n": 5, "status": "KEPT. Q2 not discussed."}])
check("kept but not discussed", lines(o) == ["1 - (X/LI) - (P3) - (Long-form)", "2 - (X/LI) - (P4) - (Long-form)",
                                             "3 - (X/LI) - (P5) - (Long-form)"]
      and [w["topic"] for w in o["would_be"]] == [1, 2]
      and o["problems"] == ["T1 status 'KEPT as written. Not discussed on the call.' reads KEPT but also says not "
                            "discussed/answered: left out, check",
                            "T2 status 'PIVOT — unanswered' reads PIVOT but also says not discussed/answered: left out, check"], o)
# an extra post asked for as a snipe goes in the Snipes doc, like a snipe topic
o = run([{"n": 1, "extra_posts": [{"perspective": "S", "vehicle": "Quote tweet snipe"}, {"perspective": "E"}]},
         {"n": 2, "status": "NOT DISCUSSED", "extra_posts": [{"perspective": "S2", "vehicle": "Snipe"}]}])
check("extra post snipe", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)", "2 - (X/LI) - (E) - (Long-form)"]
      and [x["topic"] for x in o["left_out"] if x["why"].startswith("snipe")] == ["1+", "2+"]
      and o["would_be"] == [{"topic": 2, "lines": ["? - (X/LI) - (P2) - (Long-form)"],
                             "why": "Type A, not discussed on the call (no answers to write from)"}], o)

# final pass, Oct 10: "TypeB", snipe spellings, answers written after the call, mixed statuses
o = run([{"n": 1, "type": "TypeB", "status": "NOT DISCUSSED"}, {"n": 2, "label": "Snipes"}, {"n": 3, "label": "QR"},
         {"n": 4, "vehicle": "Quick-response post"}, {"n": 5, "status": "KEPT - snipe"}, {"n": 6, "status": "SNIPE"},
         {"n": 7, "status": "Answered in writing after the call"}, {"n": 8, "status": "BLOCKED (awaiting his reply)"},
         {"n": 9, "status": "BLOCKED (awaiting video asset)"}, {"n": 10, "status": "KEPT, but Q2 unanswered"}])
check("final pass", lines(o) == ["1 - (X/LI) - (P1) - (Long-form)", "2 - (X/LI) - (P9) - (Long-form)",
                                 "3 - (X/LI) - (P10) - (Long-form)"]
      and [w["topic"] for w in o["would_be"]] == [7, 8]
      and any("T10 status" in p and "line kept" in p for p in o["problems"]), o)

shutil.rmtree(tmp)
print("ok     entries_notes" if not fails else "FAIL   entries_notes (%d)" % len(fails))
sys.exit(1 if fails else 0)

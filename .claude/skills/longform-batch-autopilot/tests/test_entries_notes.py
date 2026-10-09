#!/usr/bin/env python3
"""entries.py's notes, problems and would_be on small synthetic sheets: Ben's value tweets, inferred fields,
type clashes, post-count sources, freeform EXTRA posts, would-be lines for left-out Type A topics, written
answers, Josh C's promo titles, the X article qualifier, merged format-noun brackets, and extra posts that
follow a left-out parent.
Run: python3 -I tests/test_entries_notes.py"""
import json, os, shutil, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
script = os.path.join(here, "..", "scripts", "entries.py")
tmp = tempfile.mkdtemp()
fails = []


def run(topics, **top):
    data = dict({"client": "Test", "platforms": "X, LinkedIn", "call": True}, **top)
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

shutil.rmtree(tmp)
print("ok     entries_notes" if not fails else "FAIL   entries_notes (%d)" % len(fails))
sys.exit(1 if fails else 0)

"""Check one model output against the schema and the rules the schema can't express.

A failing output is rejected and the run repeated (DESIGN.md §5.3). Checks:
  1. JSON schema (schema/eval-output-v1.schema.json)
  2. measure_id, clause IDs, question/flag IDs exist; every value on the list
     appears exactly once, and no unknown value appears
  3. every quote is verbatim in its clause (tools/quotes.py: whitespace-insensitive;
     "..." may join verbatim fragments in order)
  4. the result matches the evidence: none <-> no evidence; supports/conflicts
     only if every piece has that effect; both only if both effects appear
  5. mirror evidence is present on both values: same clause and quote, opposite effect
  6. no blocked terms in model-written fields (quotes exempt, and terms the measure itself uses)
  7. no outside names: every capitalized word a model writes (a person, place, agency, program,
     nickname such as "Gann limit") must appear in the measure text or current law. A sentence's
     first word is checked only if it isn't an ordinary dictionary word.

Usage: python3 tools/validate_output.py <measure.json> <output.json> [--concerns concerns/v1-draft.yaml]
Exit code 0 = valid, 1 = rejected.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quotes import matches  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema/eval-output-v1.schema.json"
OPPOSITE = {"supports": "conflicts", "conflicts": "supports"}


def blocked_terms():
    terms = [l.strip() for l in (ROOT / "prompts/blocked-terms.txt").read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    return [(t, re.compile(rf"(?<![\w-]){re.escape(t)}(?![\w-])", re.I)) for t in terms]


WORDS = set(w.strip().lower() for w in open("/usr/share/dict/words")) if Path("/usr/share/dict/words").exists() else set()
WORDS |= {l.strip().lower() for l in (ROOT / "prompts/allowed-words.txt").read_text().splitlines()
          if l.strip() and not l.startswith("#")}


def variants(w):
    """w plus its forms without a common English ending ("Requires" -> require, requir, ...)."""
    w = w.lower()
    out = {w}
    for suf, rep in (("ies", "y"), ("es", ""), ("s", ""), ("ed", ""), ("ed", "e"), ("d", ""), ("ing", ""),
                     ("ing", "e"), ("ers", ""), ("er", ""), ("ly", "")):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            out.add(w[: len(w) - len(suf)] + rep)
    return out


def ordinary_word(w):
    """True if w (any case, any common English ending) is a dictionary word."""
    return bool(variants(w) & WORDS)


def outside_names(text, source):
    """Capitalized words in `text` that never appear in `source`. A word that the measure uses in
    lower case ("Taxpayers", "Overrides") or an ordinary word at the start of a sentence is fine;
    a name the measure never uses ("Gann", a politician, an agency) is not."""
    low = source.lower()
    found = []
    for sent in re.split(r"(?<=[.!?:;])\s+|\n", text):
        toks = re.split(r"[\s/—–]+", sent.strip())
        for i, raw in enumerate(toks):
            w = re.sub(r"^[\"“‘'(\[]+|[\"”’')\],.;:!?]+$", "", raw)
            w = re.sub(r"[’']s$", "", w)
            if not re.match(r"^[A-Z][a-z]", w) or w in source or any(v in low for v in variants(w) if len(v) >= 4):
                continue
            initial = i == 0 or re.match(r"^\(?\w{1,4}\)$|^[-–—•*]$", toks[i - 1])
            if initial and ordinary_word(w):
                continue
            found.append(w)
    return found


def result_of(effects):
    """The result that a set of evidence effects implies."""
    effects = set(effects)
    if not effects:
        return "none"
    return "both" if len(effects) > 1 else effects.pop()


def validate(measure, out, clist, part=None):
    """part: None, or a list of clause IDs this run was limited to (a part of a long measure).
    Then restatements are required, and quotes allowed, only for those clauses."""
    errs = []
    schema = json.loads(SCHEMA.read_text())
    for e in jsonschema.Draft202012Validator(schema).iter_errors(out):
        errs.append(f"schema: {'/'.join(map(str, e.path))}: {e.message}")
    if errs:
        return errs  # later checks assume the shape is right

    all_clauses = {c["id"]: c["text"] for c in measure["clauses"]}
    clauses = {k: v for k, v in all_clauses.items() if part is None or k in part}
    concerns = {c["id"]: c for c in clist["concerns"]}
    qids = {q["id"] for q in clist["questions"]}
    fids = {f["id"] for f in clist["flags"]}

    if out["measure_id"] != measure["measure_id"]:
        errs.append(f"measure_id {out['measure_id']!r} != {measure['measure_id']!r}")

    def clause_ok(where, cid, quote=None):
        if cid not in clauses:
            errs.append(f"{where}: {'clause outside this part' if cid in all_clauses else 'unknown clause'} {cid}")
        elif quote is not None and not matches(quote, clauses[cid]):
            errs.append(f"{where}: quote not found verbatim in {cid}: {quote[:60]!r}")

    for r in out["restatements"]:
        clause_ok("restatement", r["clause_id"])
    missing = set(clauses) - {r["clause_id"] for r in out["restatements"]}
    if missing:
        errs.append(f"restatements missing for clauses: {', '.join(sorted(missing))}")

    seen, evid = {}, {}
    for e in out["values"]:
        cid = e["value_id"]
        if cid not in concerns:
            errs.append(f"unknown value {cid}")
            continue
        if cid in seen:
            errs.append(f"{cid}: appears more than once")
            continue
        seen[cid] = e
        for ev in e["evidence"]:
            clause_ok(f"{cid} evidence", ev["clause_id"], ev["quote"])
        implied = result_of(ev["effect"] for ev in e["evidence"])
        if implied != e["result"]:
            errs.append(f"{cid}: result {e['result']!r} but evidence implies {implied!r}")
        evid[cid] = e["evidence"]
    absent = sorted(set(concerns) - set(seen), key=lambda c: int(c[1:]))
    if absent:
        errs.append(f"values missing ({len(absent)}): {', '.join(absent)}")

    for cid, evs in evid.items():
        m = concerns[cid]["mirror"]
        if not m or m not in evid:
            continue
        for ev in evs:
            pair = [g for g in evid[m] if g["clause_id"] == ev["clause_id"] and g["quote"] == ev["quote"]]
            if not pair:
                errs.append(f"{cid} evidence in {ev['clause_id']}: mirror {m} has no evidence with the same clause and quote")
            elif all(g["effect"] != OPPOSITE[ev["effect"]] for g in pair):
                errs.append(f"{cid} evidence in {ev['clause_id']}: mirror {m} effect is not the opposite of {ev['effect']}")

    for a in out["analysis"]:
        clause_ok("analysis", a["clause_id"])
        if a["question_id"] not in qids:
            errs.append(f"analysis: unknown question {a['question_id']}")
    for fl in out["flags"]:
        clause_ok(f"flag {fl['flag_id']}", fl["clause_id"], fl["quote"])
        if fl["flag_id"] not in fids:
            errs.append(f"flag: unknown flag {fl['flag_id']}")

    texts = [("restatement", r["text"]) for r in out["restatements"]]
    texts += [(f"{e['value_id']} why", ev["why"]) for e in out["values"] for ev in e["evidence"]]
    texts += [("analysis", a["answer"]) for a in out["analysis"]]
    texts += [("flag", fl["note"]) for fl in out["flags"]]
    source = " ".join(all_clauses.values()) + " " + (measure.get("current_law") or "")
    for term, rx in blocked_terms():
        if rx.search(source):
            continue   # the measure itself uses the word ("Liberal Construction" is a section title)
        for where, t in texts:
            if rx.search(t):
                errs.append(f"{where}: blocked term {term!r}")
    for where, t in texts:
        names = outside_names(t, source)
        if names:
            errs.append(f"{where}: names not in the measure text {sorted(set(names))}")
    return errs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("measure")
    ap.add_argument("output")
    ap.add_argument("--concerns", default=str(ROOT / "concerns/v1-draft.yaml"))
    a = ap.parse_args()
    errs = validate(json.loads(Path(a.measure).read_text()), json.loads(Path(a.output).read_text()),
                    yaml.safe_load(Path(a.concerns).read_text()))
    for e in errs:
        print("REJECT", e)
    print("VALID" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)

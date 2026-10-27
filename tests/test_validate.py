"""Planted-defect test for tools/validate_output.py.

The good fixture must pass. Each mutation plants one defect, and the validator
must reject it with a matching message. Run: python3 tests/test_validate.py
"""
import copy
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from validate_output import validate  # noqa: E402

F = ROOT / "tests/fixtures"
measure = json.loads((F / "synthetic-storage.measure.json").read_text())
good = json.loads((F / "synthetic-storage.output-good.json").read_text())
clist = yaml.safe_load((ROOT / "concerns/v1-draft.yaml").read_text())


def entry(o, cid):
    return next(e for e in o["values"] if e["value_id"] == cid)


def m_quote(o):
    entry(o, "C01")["evidence"][0]["quote"] = "a fee of thirty dollars"


def m_result(o):
    entry(o, "C01")["result"] = "supports"


def m_none_with_evidence(o):
    entry(o, "C02")["evidence"] = copy.deepcopy(entry(o, "C01")["evidence"])


def m_both_wrong(o):
    entry(o, "C01")["result"] = "both"


def m_missing(o):
    o["values"] = [e for e in o["values"] if e["value_id"] != "C40"]


def m_duplicate(o):
    o["values"].append(copy.deepcopy(entry(o, "C40")))


def m_unknown(o):
    o["values"].append({"value_id": "C999", "result": "none", "evidence": []})


def m_mirror_missing(o):
    e = entry(o, "C33")
    e["result"], e["evidence"] = "none", []


def m_mirror_same(o):
    e = entry(o, "C33")
    e["result"] = "supports"
    e["evidence"][0]["effect"] = "supports"


def m_blocked(o):
    entry(o, "C01")["evidence"][0]["why"] = "A reckless new fee on applicants."


def m_outside_name(o):
    entry(o, "C01")["evidence"][0]["why"] = "Adds a fee like the one Governor Smith proposed."


def m_clause(o):
    entry(o, "C01")["evidence"][0]["clause_id"] = "§2"


def m_schema(o):
    o["vote_summary"] = {}


def m_measure_id(o):
    o["measure_id"] = "SYN-9999"


CASES = [(m_quote, "not found verbatim"), (m_result, "evidence implies"), (m_none_with_evidence, "evidence implies"),
         (m_both_wrong, "evidence implies"), (m_missing, "values missing"), (m_duplicate, "more than once"),
         (m_unknown, "unknown value"), (m_mirror_missing, "mirror C33 has no evidence"),
         (m_mirror_same, "not the opposite"), (m_blocked, "blocked term"), (m_outside_name, "names not in the measure text"), (m_clause, "unknown clause"),
         (m_schema, "schema"), (m_measure_id, "measure_id")]

from quotes import matches  # noqa: E402

T = "The Department shall issue a storage certificate\nto each applicant upon payment of a fee."
QUOTE_CASES = [("storage certificate to each applicant", True),            # line break in text = space
               ("The Department shall issue ... upon payment of a fee", True),  # verbatim fragments in order
               ("upon payment of a fee ... The Department shall issue", False),  # out of order
               ("the Department shall issue", False),                      # case changed
               ("The Department ... payment", False),                      # fragment under 3 words
               ("The Department shall issue a storage permit", False)]     # word changed

fails = 0
for q, want in QUOTE_CASES:
    ok = matches(q, T) == want
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} quote {'matches' if want else 'rejected'}: {q!r}")
errs = validate(measure, good, clist)
print(("ok  " if not errs else "FAIL") + " good fixture passes" + ("" if not errs else f": {errs}"))
fails += bool(errs)
for mutate, expect in CASES:
    o = copy.deepcopy(good)
    mutate(o)
    errs = validate(measure, o, clist)
    hit = any(expect in e for e in errs)
    fails += not hit
    print(f"{'ok  ' if hit else 'FAIL'} {mutate.__name__}: {errs[0] if errs else 'accepted'}")
print(f"{len(CASES) + len(QUOTE_CASES) + 1 - fails}/{len(CASES) + len(QUOTE_CASES) + 1} passed")
sys.exit(1 if fails else 0)

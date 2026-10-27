"""Campaign data: who funds, supports, and opposes each measure, and each entity's record.

Inputs (never sent to a model; the text analysis must not depend on them):
  data/entities.yaml               people and organizations, with stable IDs across elections
  elections/<id>/campaign.yaml     per measure: committees, contributions, endorsements

  check(election, campaign, entities)   -> (errors, warnings)
  measure_view(code, campaign, ents)    -> what the measure page shows
  entity_records(elections, ents)       -> {entity_id: [rows across elections]}

Usage: python3 tools/campaign.py check <election-id>
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SIDES = ("support", "oppose")
KINDS = ("organization", "person", "committee")


def load_entities():
    d = yaml.safe_load((ROOT / "data/entities.yaml").read_text())
    return {e["id"]: e for e in d["entities"]}, d.get("policy", {})


def load_campaign(eid):
    f = ROOT / "elections" / eid / "campaign.yaml"
    return yaml.safe_load(f.read_text()) if f.exists() else None


def blocked_terms():
    terms = [l.strip() for l in (ROOT / "prompts/blocked-terms.txt").read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    return [(t, re.compile(rf"(?<![\w-]){re.escape(t)}(?![\w-])", re.I)) for t in terms]


def check(election, camp, ents):
    errs, warn = [], []
    for eid, e in ents.items():
        if e.get("kind") not in KINDS:
            errs.append(f"entity {eid}: kind must be one of {KINDS}")
        for term, rx in blocked_terms():
            if rx.search(e["name"]):
                # Site rule: no party or ideology labels anywhere. An entity whose official name
                # contains one (e.g. a party committee) needs an owner decision before it can be shown.
                errs.append(f"entity {eid}: name contains blocked term {term!r} (no rule yet for showing it)")
    if camp is None:
        return errs, warn
    codes = {m["code"] for m in election["measures"]}
    srcs = camp.get("sources", {})
    synthetic = election.get("synthetic") or camp.get("synthetic")
    for sid, s in srcs.items():
        if not synthetic and not (s.get("url") and s.get("fetched_at")):
            errs.append(f"source {sid}: real data needs url and fetched_at")
    for code, m in (camp.get("measures") or {}).items():
        if code not in codes:
            errs.append(f"campaign: {code} is not a measure in this election")
            continue
        committees = {}
        for c in m.get("committees", []):
            committees[c["entity"]] = c["side"]
        rows = [("committee", c, c["entity"]) for c in m.get("committees", [])]
        rows += [("contribution", c, c["from"]) for c in m.get("contributions", [])]
        rows += [("endorsement", c, c["entity"]) for c in m.get("endorsements", [])]
        for kind, r, who in rows:
            w = f"{code} {kind} {who}"
            if who not in ents:
                errs.append(f"{w}: unknown entity (add it to data/entities.yaml)")
            if r.get("source") not in srcs:
                errs.append(f"{w}: unknown source {r.get('source')!r}")
            if kind != "contribution" and r.get("side") not in SIDES:
                errs.append(f"{w}: side must be support or oppose")
            if kind == "contribution":
                if r.get("to") not in committees:
                    errs.append(f"{w}: 'to' must be one of this measure's committees")
                if not isinstance(r.get("amount_usd"), (int, float)) or r["amount_usd"] <= 0:
                    errs.append(f"{w}: amount_usd must be a positive number")
            if kind == "committee" and ents.get(who, {}).get("kind") != "committee":
                warn.append(f"{w}: entity kind is not 'committee'")
    return errs, warn


def shown(ent, amount, policy):
    """Whether an individual gets named (and a page) for this amount. Organizations always do."""
    if ent["kind"] != "person":
        return True
    return amount is None or amount >= policy.get("individual_min_usd", 0)


def measure_view(code, camp, ents, policy):
    """{"as_of", "sources", "sides": {support|oppose: {committees, funders, other_individuals_usd, endorsers}}}"""
    if not camp or code not in (camp.get("measures") or {}):
        return None
    m = camp["measures"][code]
    side_of = {c["entity"]: c["side"] for c in m.get("committees", [])}
    sides = {s: {"committees": [], "funders": [], "other_individuals_usd": 0, "other_individuals_n": 0,
                 "endorsers": []} for s in SIDES}
    for c in m.get("committees", []):
        sides[c["side"]]["committees"].append({**ents[c["entity"]], "raised_usd": c.get("raised_usd"), "source": c["source"]})
    for c in m.get("contributions", []):
        s, ent = side_of[c["to"]], ents[c["from"]]
        if shown(ent, c["amount_usd"], policy):
            sides[s]["funders"].append({**ent, "amount_usd": c["amount_usd"], "to": ents[c["to"]]["name"], "source": c["source"]})
        else:
            sides[s]["other_individuals_usd"] += c["amount_usd"]
            sides[s]["other_individuals_n"] += 1
    for c in m.get("endorsements", []):
        sides[c["side"]]["endorsers"].append({**ents[c["entity"]], "source": c["source"]})
    for s in sides.values():
        s["funders"].sort(key=lambda f: -f["amount_usd"])
        s["raised_usd"] = sum(c["raised_usd"] or 0 for c in s["committees"])
    return {"as_of": camp.get("as_of"), "sources": camp.get("sources", {}), "sides": sides,
            "synthetic": camp.get("synthetic", False)}


def entity_records(elections, ents, policy):
    """{entity_id: [{"election", "measure", "role", "side", "amount_usd", "source"}]}, newest election first.
    elections: [(election dict, campaign dict, {code: measure page info})]."""
    rec = defaultdict(list)
    for e, camp, pages in elections:
        if not camp:
            continue
        for code, m in (camp.get("measures") or {}).items():
            side_of = {c["entity"]: c["side"] for c in m.get("committees", [])}
            base = {"election": e, "measure": pages.get(code, {"code": code}), "sources": camp.get("sources", {})}
            for c in m.get("committees", []):
                rec[c["entity"]].append({**base, "role": "committee", "side": c["side"], "amount_usd": c.get("raised_usd"), "source": c["source"]})
            for c in m.get("contributions", []):
                if shown(ents[c["from"]], c["amount_usd"], policy):
                    rec[c["from"]].append({**base, "role": "contributor", "side": side_of[c["to"]], "amount_usd": c["amount_usd"],
                                           "to": ents[c["to"]], "source": c["source"]})
            for c in m.get("endorsements", []):
                rec[c["entity"]].append({**base, "role": "endorser", "side": c["side"], "amount_usd": None, "source": c["source"]})
    for rows in rec.values():
        rows.sort(key=lambda r: (r["election"]["date"], r["measure"].get("code", "")), reverse=True)
    return rec


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "check":
        sys.exit(__doc__)
    e = yaml.safe_load((ROOT / "elections" / sys.argv[2] / "election.yaml").read_text())
    ents, _ = load_entities()
    errs, warn = check(e, load_campaign(sys.argv[2]), ents)
    for w in warn:
        print("warn ", w)
    for x in errs:
        print("ERROR", x)
    print(f"campaign {sys.argv[2]}: {len(errs)} errors, {len(warn)} warnings")
    sys.exit(1 if errs else 0)

"""Reconcile all accepted runs for one measure into one record (DESIGN.md §5.4).

No judge model. The rules are mechanical and published.

Every run returns one result per concern: supports, conflicts, both, or none.

Within one model (K seeds), per concern:
  the model's result is its most common result across seeds. A result other
  than none counts only if it appears in at least half of the seeds; otherwise
  the model's result is none.
  A piece of evidence (clause x concern x effect) counts for the model if it
  appears in at least half of the seeds.

Across models, per concern:
  consensus        more than half of the models hold the same result (not none)
  split            at least two models found an effect, but no result has a majority
                   (including when a majority found nothing)
  outlier          exactly one model found an effect
  below-threshold  found only in a minority of one model's seeds

Consensus concerns are shown on the measure page. Splits are shown as "models
disagree". Outliers and below-threshold appear only in "How we got this".

Only accepted runs whose manifest matches the election's pins, whose prompt files
(system prompt, user template, schema) are byte-identical to the current ones for
that version, and whose measure hash matches the current measure file, are used.
"""
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def same_prompt(manifest, hashes):
    """True if the run used exactly the current prompt files for its version (not just the label)."""
    return all(manifest["sha256"].get(k) == v for k, v in hashes.items())


def load_runs(runs_dir, measure_id, pins, measure_sha=None):
    """{model_slug: {"seeds": {seed: parsed}, "meta": {...}}}"""
    from build_prompt import prompt_hashes
    hashes = prompt_hashes(pins["prompt_version"])
    out = {}
    for d in sorted((runs_dir / measure_id).glob("*/")):
        seeds, attempts, rejected, versions, model, parts = {}, 0, 0, set(), None, 0
        for f in sorted(d.glob("run*.attempt*.json")):
            e = json.loads(f.read_text())
            m = e["manifest"]
            if m["prompt_version"] != pins["prompt_version"] or m["concern_list_version"] != pins["concern_list_version"]:
                continue
            if measure_sha and m["sha256"]["measure"] != measure_sha:
                continue   # run was made on an earlier version of the measure text
            if not same_prompt(m, hashes):
                continue   # run was made with an earlier draft of the prompt files
            attempts += 1
            model = e["model"]
            if not e.get("accepted"):
                rejected += 1
                continue
            seeds.setdefault(m["seed"], e["parsed"])
            parts = max(parts, len(e.get("parts") or []))
            if (e.get("meta") or {}).get("model_version"):
                versions.add(e["meta"]["model_version"])
        if seeds:
            out[d.name] = {"seeds": seeds, "meta": {
                "slug": d.name, "provider": d.name.split("__")[0], "model": model,
                "model_versions": sorted(versions), "seeds": sorted(seeds),
                "attempts": attempts, "rejected": rejected, "parts": parts}}
    return out


def model_positions(seeds):
    """One model's results: ({concern: {"result", "found_in", "of"}}, {(clause, concern, effect): evidence+count})."""
    k = len(seeds)
    results, cells = defaultdict(Counter), defaultdict(list)
    for seed, o in sorted(seeds.items()):
        for e in o["values"]:
            results[e["value_id"]][e["result"]] += 1
            seen = set()
            for ev in e["evidence"]:
                key = (ev["clause_id"], e["value_id"], ev["effect"])
                if key not in seen:      # one vote per seed per cell
                    seen.add(key)
                    cells[key].append(ev)
    pos = {}
    for cid, ctr in results.items():
        found = sum(n for r, n in ctr.items() if r != "none")
        r, n = next(((r, n) for r, n in ctr.most_common() if r != "none"), ("none", 0))
        pos[cid] = {"result": r if r != "none" and n * 2 >= k and n >= ctr["none"] else "none",
                    "found_in": found, "of": k}
    ev = {key: {**evs[0], "found_in": len(evs), "of": k} for key, evs in cells.items() if len(evs) * 2 >= k}
    return pos, ev


def reconcile(measure, runs_dir, pins, concerns, measure_sha=None):
    runs = load_runs(runs_dir, measure["measure_id"], pins, measure_sha)
    models = sorted(runs)
    positions, evidence = {}, {}
    for m in models:
        positions[m], evidence[m] = model_positions(runs[m]["seeds"])
    order = {c["id"]: i for i, c in enumerate(measure["clauses"])}
    out = []
    for c in concerns["concerns"]:
        cid = c["id"]
        by_model = {m: positions[m].get(cid, {"result": "none", "found_in": 0, "of": len(runs[m]["seeds"])}) for m in models}
        held = Counter(p["result"] for p in by_model.values() if p["result"] != "none")
        finders = sum(held.values())
        top, top_n = held.most_common(1)[0] if held else ("none", 0)
        if top_n * 2 > len(models):
            status = "consensus"
        elif finders >= 2:
            status = "split"
        elif finders == 1:
            status = "outlier"
        elif any(p["found_in"] for p in by_model.values()):
            status = "below-threshold"
        else:
            continue
        # Evidence: every clause x effect that some model holds; count the models holding it.
        merged = {}
        for m in models:
            for (clause, ccid, effect), ev in evidence[m].items():
                if ccid != cid:
                    continue
                e = merged.setdefault((clause, effect), {"clause_id": clause, "effect": effect, "quote": ev["quote"],
                                                         "why": ev["why"], "certainty": ev["certainty"], "models": []})
                e["models"].append(m)
        evs = sorted(merged.values(), key=lambda e: (order.get(e["clause_id"], 99), e["effect"]))
        for e in evs:
            e["agree"] = len(e["models"])
        out.append({
            "value_id": cid, "name": c["name"], "domain": c["domain"], "axis": c["axis"],
            "advances_when": c["advances_when"], "mirror": c["mirror"],
            "status": status, "result": top if status == "consensus" else None,
            "agree": top_n, "models": len(models),
            "by_model": by_model, "evidence": evs,
        })

    first = lambda m: runs[m]["seeds"][min(runs[m]["seeds"])]
    restatements = defaultdict(list)
    analysis = defaultdict(list)
    flags = {}
    for m in models:
        for r in first(m)["restatements"]:
            restatements[r["clause_id"]].append({"model": m, "text": r["text"]})
        for a in first(m)["analysis"]:
            analysis[(a["clause_id"], a["question_id"])].append({"model": m, "answer": a["answer"], "disputed": a["disputed"]})
        for seed_out in runs[m]["seeds"].values():
            for fl in seed_out["flags"]:
                k = (fl["clause_id"], fl["flag_id"])
                e = flags.setdefault(k, {"clause_id": k[0], "flag_id": k[1], "quote": fl["quote"], "notes": {}})
                e["notes"].setdefault(m, fl["note"])
    qtext = {q["id"]: q["text"] for q in concerns["questions"]}
    ftext = {f["id"]: f["text"] for f in concerns["flags"]}
    return {
        "measure_id": measure["measure_id"],
        "clauses": measure["clauses"],
        "current_law": measure.get("current_law"),
        "pins": pins,
        "models": [runs[m]["meta"] for m in models],
        "results": out,
        "restatements": dict(restatements),
        "analysis": [{"clause_id": c, "question_id": q, "question": qtext.get(q, q), "answers": v}
                     for (c, q), v in sorted(analysis.items(), key=lambda kv: (order.get(kv[0][0], 99), int(kv[0][1][1:])))],
        "flags": [{**f, "flag": ftext.get(f["flag_id"], f["flag_id"]), "models": sorted(f["notes"])}
                  for f in sorted(flags.values(), key=lambda f: (order.get(f["clause_id"], 99), f["flag_id"]))],
        "reconciled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

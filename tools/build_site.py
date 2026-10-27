"""Build the static website from elections/, runs/, and the method files.

For each election folder (elections/<id>/election.yaml) and each measure in it:
  1. reconcile the accepted runs that match the election's pins
  2. write the public data: site/e/<election>/<code>/data.json
  3. write the "Verify this" bundle: .../bundle.zip (everything needed to rerun)
  4. write the copy-paste prompt: .../prompt.txt
  5. render the measure page, with campaign data (elections/<id>/campaign.yaml) if present
Then the home, election, values, method, and verify pages, one page per person or
organization in the campaign data (their record across all elections), and the
do-it-yourself packs (dist/portable as a zip).

The output folder is plain static files. Any static host can serve it.

Usage: python3 tools/build_site.py [--elections demo-synthetic,...] [--out build/site]
"""
import argparse
import hashlib
import io
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompt import build as build_prompt  # noqa: E402
from reconcile import reconcile  # noqa: E402
import campaign  # noqa: E402
from quotes import spans as quote_spans, ws  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "site/templates"
STATIC = ROOT / "site/static"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def highlight(text, quotes):
    """Wrap each quoted span in <mark>, merging overlaps. Returns safe HTML.
    Matching follows tools/quotes.py, so highlighting works on whitespace-collapsed text."""
    text = ws(text)
    spans = []
    for q, ref in quotes:
        for a, b in (quote_spans(q, text) or []):
            spans.append([a, b, [ref]])
    spans.sort()
    merged = []
    for s in spans:
        if merged and s[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], s[1])
            merged[-1][2] += s[2]
        else:
            merged.append(s)
    out, pos = [], 0
    for a, b, refs in merged:
        out.append(escape(text[pos:a]))
        out.append(Markup(f'<mark data-refs="{escape(" ".join(refs))}">') + escape(text[a:b]) + Markup("</mark>"))
        pos = b
    out.append(escape(text[pos:]))
    return Markup("").join(out)


RESULT_ORDER = {"both": 0, "supports": 1, "conflicts": 2}


def views(rec):
    """Page views over the shown (consensus) concerns: grouped by domain, and by clause.
    Nothing is ranked; within a domain, concerns keep the list's order."""
    shown = [c for c in rec["results"] if c["status"] == "consensus"]
    by_domain = {}
    for c in shown:
        by_domain.setdefault(c["domain"], []).append(c)
    n = max(len(rec["models"]), 1)
    by_clause = {cl["id"]: {"supports": [], "conflicts": []} for cl in rec["clauses"]}
    for c in shown:
        for e in c["evidence"]:
            if e["agree"] * 2 > n and e["clause_id"] in by_clause and c not in by_clause[e["clause_id"]][e["effect"]]:
                by_clause[e["clause_id"]][e["effect"]].append(c)
    counts = {r: sum(c["result"] == r for c in shown) for r in RESULT_ORDER}
    return shown, by_domain, by_clause, counts


def zip_bundle(path, files):
    """files: {archive name: bytes}. Fixed timestamps so identical inputs give identical zips."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(files):
            zi = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, files[name])
    path.write_bytes(buf.getvalue())
    return hashlib.sha256(buf.getvalue()).hexdigest()


BUNDLE_README = """Only Tradeoffs: verification bundle for {code} ({ballot_label}), {election}

Everything here is what the models received and returned. To rerun:

  pip install pyyaml jsonschema boto3 google-genai openai
  python3 tools/run_eval.py measure.json --concerns values.yaml --provider <vertex|bedrock|openai> --model <id> --runs 3 --out myruns
  # compare your results (value x result, and clause x value x effect) with reconciled.json

Or paste prompt.txt into any chat and compare the JSON it returns.

Contents
  measure.json          the clauses and current law the models were given
  values.yaml           value list {concern_version}
  prompts/              system prompt, user template, blocked terms ({prompt_version})
  schema.json           output schema
  runs/                 every attempt by every model: manifest, exact prompt file name, raw reply,
                        parsed output, validation errors (rejected attempts included)
  reconciled.json       the published result
  tools/                the scripts that built the prompts, validated, and reconciled

Models are not fully deterministic and vendors update them, so compare findings, not wording.
"""


def build_measure(election, m_entry, concerns, concerns_path, out_root, env, runs_dir, camp, ents, policy):
    mpath = ROOT / m_entry["file"]
    measure = json.loads(mpath.read_text())
    rec = reconcile(measure, runs_dir, election["pins"], concerns, hashlib.sha256(mpath.read_bytes()).hexdigest())
    code_slug = slug(m_entry["code"])
    out = out_root / "e" / election["id"] / code_slug
    out.mkdir(parents=True, exist_ok=True)
    meta = {k: m_entry.get(k) for k in ("code", "ballot_label", "jurisdiction", "kind", "source", "source_name")}
    src = measure.get("source") or meta.get("source") or {}
    meta["source"] = src
    if src.get("archived"):
        # Publish our archived copy of the official source next to the page, and the import log.
        arch = ROOT / src["archived"]
        out.mkdir(parents=True, exist_ok=True)
        meta["source_copy"] = "source" + arch.suffix
        shutil.copyfile(arch, out / meta["source_copy"])
        log = arch.with_suffix(".import-log.txt")
        if log.exists():
            meta["source_log"] = "import-log.txt"
            shutil.copyfile(log, out / "import-log.txt")
    rec.update(meta=meta, election_id=election["id"], synthetic=election.get("synthetic", False))

    # copy-paste prompt (seed 1); the prompt depends only on the measure and seed
    tmp = out / ".tmp"
    _, p = build_prompt(mpath, 1, concerns_path, tmp)
    shutil.rmtree(tmp)
    paste = f"{p['messages'][0]['content']}\n\n---\n\n{p['messages'][1]['content']}"
    (out / "prompt.txt").write_text(paste)

    files = {
        "README.txt": BUNDLE_README.format(code=meta["code"], ballot_label=meta["ballot_label"], election=election["name"],
                                           concern_version=election["pins"]["concern_list_version"],
                                           prompt_version=election["pins"]["prompt_version"]).encode(),
        "measure.json": mpath.read_bytes(),
        **({f"source/{Path(meta['source']['archived']).name}": (ROOT / meta["source"]["archived"]).read_bytes()}
           if meta["source"].get("archived") else {}),
        "values.yaml": Path(concerns_path).read_bytes(),
        "schema.json": (ROOT / f"schema/eval-output-{election['pins']['prompt_version']}.schema.json").read_bytes(),
        "prompt.txt": paste.encode(),
        "reconciled.json": json.dumps(rec, indent=2, ensure_ascii=False).encode(),
    }
    pv = election["pins"]["prompt_version"]
    for f in (f"system-{pv}.md", f"user-{pv}.md", "blocked-terms.txt"):
        files[f"prompts/{f}"] = (ROOT / "prompts" / f).read_bytes()
    for f in ("build_prompt.py", "validate_output.py", "run_eval.py", "reconcile.py"):
        files[f"tools/{f}"] = (ROOT / "tools" / f).read_bytes()
    for f in sorted((runs_dir / measure["measure_id"]).rglob("*.json")):
        files[f"runs/{f.relative_to(runs_dir / measure['measure_id'])}"] = f.read_bytes()
    rec["bundle_sha256"] = zip_bundle(out / "bundle.zip", files)
    (out / "data.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))

    # quotes to highlight: evidence of every shown or disputed concern
    quotes = {}
    for c in rec["results"]:
        if c["status"] in ("consensus", "split"):
            for e in c["evidence"]:
                quotes.setdefault(e["clause_id"], []).append((e["quote"], c["value_id"]))
    clauses = [{"id": c["id"], "anchor": "clause-" + slug(c["id"]),
                "html": highlight(c["text"], quotes.get(c["id"], []))} for c in rec["clauses"]]
    anchors = {c["id"]: c["anchor"] for c in clauses}
    shown, by_domain, by_clause, counts = views(rec)
    page = env.get_template("measure.html").render(
        election=election, m=rec, meta=meta, clauses=clauses, anchors=anchors,
        shown=shown, by_domain=by_domain, by_clause=by_clause, counts=counts,
        n_values=len(concerns["concerns"]),
        restate={k: v[0]["text"] for k, v in rec["restatements"].items() if v},
        analysis_groups=[(cid, [x for x in rec["analysis"] if x["clause_id"] == cid])
                         for cid in dict.fromkeys(x["clause_id"] for x in rec["analysis"])],
        splits=[c for c in rec["results"] if c["status"] == "split"],
        camp=campaign.measure_view(m_entry["code"], camp, ents, policy),
        policy_min=policy.get("individual_min_usd", 0), depth=3)
    (out / "index.html").write_text(page)
    return {**meta, "slug": code_slug, "n_models": len(rec["models"]),
            "n_shown": len(shown), "counts": counts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--elections", default="all")
    ap.add_argument("--out", default=str(ROOT / "build/site"))
    ap.add_argument("--runs", default=str(ROOT / "runs"))
    ap.add_argument("--concerns", default=str(ROOT / "concerns/v1-draft.yaml"))
    a = ap.parse_args()

    out_root = Path(a.out)
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)
    shutil.copytree(STATIC, out_root / "static")
    concerns = yaml.safe_load(Path(a.concerns).read_text())
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    env.globals.update(built=built, concerns_version=concerns["version"], concerns_frozen=concerns["frozen"],
                       value_by_id={c["id"]: c for c in concerns["concerns"]})
    # depth: how many folders down the page sits, or "/" for a page served at any path (404)
    env.filters["rel"] = lambda depth: depth if isinstance(depth, str) else "../" * depth
    env.filters["host"] = lambda url: re.sub(r"^https?://([^/]+).*", r"\1", url or "")
    env.filters["mname"] = lambda slug: slug.split("__", 1)[-1]          # vertex__gemini-x -> gemini-x
    env.filters["shortq"] = lambda q: q.split("?")[0] + "?" if "?" in q else q  # first sentence only

    ents, policy = campaign.load_entities()
    folders = sorted((ROOT / "elections").glob("*/election.yaml"))
    wanted = None if a.elections == "all" else set(a.elections.split(","))
    elections, camp_list = [], []
    for f in folders:
        e = yaml.safe_load(f.read_text())
        if wanted and e["id"] not in wanted:
            continue
        jur = {j["id"]: j for j in e["jurisdictions"]}
        camp = campaign.load_campaign(e["id"])
        errs, _ = campaign.check(e, camp, ents)
        if errs:
            sys.exit(f"{e['id']}: campaign data has errors; run `python3 tools/campaign.py check {e['id']}`")
        measures = [build_measure(e, m, concerns, a.concerns, out_root, env, Path(a.runs), camp, ents, policy)
                    for m in e["measures"]]
        camp_list.append((e, camp, {m["code"]: m for m in measures}))
        groups = [{"j": j, "measures": [m for m in measures if m["jurisdiction"] == j["id"]]} for j in e["jurisdictions"]]
        (out_root / "e" / e["id"] / "index.html").write_text(
            env.get_template("election.html").render(election=e, groups=groups, jur=jur, depth=2))
        elections.append({**e, "n_measures": len(measures)})
        print(f"{e['id']}: {len(measures)} measures")

    elections.sort(key=lambda e: e["date"], reverse=True)
    domains = {}
    for c in concerns["concerns"]:
        domains.setdefault(c["domain"], []).append(c)
    pages = {
        "index.html": ("index.html", {"elections": elections, "depth": 0}),
        "values/index.html": ("values.html", {"domains": domains, "questions": concerns["questions"], "flags": concerns["flags"], "depth": 1}),
        "method/index.html": ("method.html", {"depth": 1}),
        "verify/index.html": ("verify.html", {"depth": 1}),
        "404.html": ("404.html", {"depth": "/"}),
    }
    records = campaign.entity_records(camp_list, ents, policy)
    people = []
    for eid, rows in records.items():
        totals = {s: sum(r["amount_usd"] or 0 for r in rows if r["role"] == "contributor" and r["side"] == s) for s in campaign.SIDES}
        people.append({**ents[eid], "rows": rows, "totals": totals,
                       "n_measures": len({(r["election"]["id"], r["measure"]["code"]) for r in rows})})
        pages[f"p/{eid}/index.html"] = ("entity.html", {"ent": ents[eid], "rows": rows, "totals": totals, "depth": 2})
    people.sort(key=lambda p: (p["kind"] == "committee", p["name"].lower()))
    pages["p/index.html"] = ("people.html", {"people": people, "policy": policy, "depth": 1})
    for path, (tpl, ctx) in pages.items():
        (out_root / path).parent.mkdir(parents=True, exist_ok=True)
        (out_root / path).write_text(env.get_template(tpl).render(**ctx))

    portable = ROOT / "dist/portable"
    if portable.exists():
        files = {str(p.relative_to(portable)): p.read_bytes() for p in portable.rglob("*") if p.is_file()}
        zip_bundle(out_root / "verify/only-tradeoffs-packs.zip", files)
    print(f"site → {out_root} ({sum(1 for _ in out_root.rglob('*.html'))} pages)")


if __name__ == "__main__":
    main()

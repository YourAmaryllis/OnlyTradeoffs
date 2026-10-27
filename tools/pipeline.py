"""One entry point for an election, from official texts to a deployable site.

  new     <id> --name ... --date YYYY-MM-DD   scaffold elections/<id>/election.yaml
  check   <id>       validate the election folder (measures and campaign data) before spending money on model runs
  run     <id> -- <run_eval args>               run every measure through one model (offline, resumable)
  status  <id>       accepted runs per measure x model, for the election's pinned versions
  gate    <id>       bias suite must have been run and compared for every model used
  build   [<id>,...] reconcile + bundles + static site → build/site
  all     <id> -- <run_eval args>               check, run, status, build

Typical cycle for a new election:
  python3 tools/pipeline.py new ca-2028-11 --name "California, November 2028" --date 2028-11-07
  # put each official text in elections/ca-2028-11/measures/<file>.json and list it in election.yaml
  # put funders / committees / endorsements in elections/ca-2028-11/campaign.yaml (entities in data/entities.yaml)
  python3 tools/pipeline.py check ca-2028-11
  python3 tools/pipeline.py run ca-2028-11 -- --provider vertex --model <id> --runs 3
  python3 tools/pipeline.py run ca-2028-11 -- --provider bedrock --model <id> --runs 3
  python3 tools/pipeline.py status ca-2028-11
  python3 tools/pipeline.py build
  # then publish build/site to the static host

`run` is resumable: a measure x model x seed that already has an accepted run
for the pinned versions is skipped, so an interrupted batch can simply be rerun.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
ELECTIONS = ROOT / "elections"
RUNS = ROOT / "runs"


def load(eid):
    f = ELECTIONS / eid / "election.yaml"
    if not f.exists():
        sys.exit(f"no election {eid} ({f})")
    return yaml.safe_load(f.read_text())


def mid_of(m):
    return json.loads((ROOT / m["file"]).read_text())["measure_id"]


def sha_of(m):
    import hashlib
    return hashlib.sha256((ROOT / m["file"]).read_bytes()).hexdigest()


def cmd_new(a):
    d = ELECTIONS / a.id
    if d.exists():
        sys.exit(f"{d} already exists")
    (d / "measures").mkdir(parents=True)
    pins = yaml.safe_load((ROOT / "concerns/v1-draft.yaml").read_text())["version"]
    (d / "election.yaml").write_text(f"""id: {a.id}
name: {a.name}
date: {a.date}
status: draft
synthetic: false
pins:
  prompt_version: v1
  concern_list_version: {pins}
jurisdictions:
- id: state
  name: (state name)
  type: state
measures: []
# - file: elections/{a.id}/measures/<measure-id>.json   # {{"measure_id", "clauses": [{{"id", "text"}}], "current_law"}}
#   code: Proposition 1
#   ballot_label: (as printed on the ballot; shown to voters, never sent to a model)
#   jurisdiction: state
#   kind: initiative | referendum | amendment | bond | charter | advisory
#   source_name: (what the official source is, e.g. "Initiative 25-0024A1, as filed with the Attorney General")
#   (the source URL, archived copy and sha256 are written into the measure file by tools/import_measure.py)
""")
    (d / "campaign.yaml").write_text("""# Who funds, supports, and opposes each measure. Never sent to a model.
# Every row cites a source; every person or organization is listed in data/entities.yaml.
as_of: null
sources: {}
#  sos: {title: (filing database name), url: (URL), fetched_at: YYYY-MM-DD}
measures: {}
#  Proposition 1:
#    committees:    [{entity: <id>, side: support|oppose, raised_usd: 0, source: sos}]
#    contributions: [{from: <id>, to: <committee id>, amount_usd: 0, source: sos}]
#    endorsements:  [{entity: <id>, side: support|oppose, source: <id>}]
""")
    print(f"created {d}/election.yaml and campaign.yaml")


def cmd_check(a):
    e = load(a.id)
    errs, warn = [], []
    for k in ("id", "name", "date", "status", "pins", "jurisdictions", "measures"):
        if k not in e:
            errs.append(f"missing key {k}")
    jids = {j["id"] for j in e.get("jurisdictions", [])}
    clist = yaml.safe_load((ROOT / "concerns/v1-draft.yaml").read_text())
    if e["pins"]["concern_list_version"] != clist["version"]:
        warn.append(f"pinned concern list {e['pins']['concern_list_version']} != current {clist['version']}")
    if e.get("status") == "published" and not clist["frozen"]:
        errs.append("status is published but the concern list is not frozen")
    seen_ids, seen_codes = set(), set()
    for m in e.get("measures", []):
        tag = m.get("code", m.get("file"))
        f = ROOT / m["file"]
        if not f.exists():
            errs.append(f"{tag}: file not found {m['file']}")
            continue
        mj = json.loads(f.read_text())
        if mj["measure_id"] in seen_ids:
            errs.append(f"{tag}: duplicate measure_id {mj['measure_id']}")
        seen_ids.add(mj["measure_id"])
        if m["code"] in seen_codes:
            errs.append(f"{tag}: duplicate code")
        seen_codes.add(m["code"])
        if m.get("jurisdiction") not in jids:
            errs.append(f"{tag}: unknown jurisdiction {m.get('jurisdiction')}")
        cids = [c["id"] for c in mj["clauses"]]
        if len(cids) != len(set(cids)) or not all(c["text"].strip() for c in mj["clauses"]):
            errs.append(f"{tag}: clause ids must be unique and texts non-empty")
        if not e.get("synthetic"):
            src = mj.get("source") or m.get("source") or {}
            if not (src.get("url") and src.get("sha256") and src.get("fetched_at")):
                errs.append(f"{tag}: real measures need source url, sha256 and fetched_at")
            arch = ROOT / src.get("archived", "") if src.get("archived") else None
            if not arch or not arch.is_file():
                errs.append(f"{tag}: no archived copy of the official source (run tools/import_measure.py)")
            elif hashlib.sha256(arch.read_bytes()).hexdigest() != src.get("sha256"):
                errs.append(f"{tag}: archived source does not match its recorded sha256")
            if mj.get("current_law") is None:
                warn.append(f"{tag}: no current law (fine for new law; needed for amendments)")
    import campaign
    ents, _ = campaign.load_entities()
    cerrs, cwarn = campaign.check(e, campaign.load_campaign(a.id), ents)
    errs += [f"campaign: {x}" for x in cerrs]
    warn += [f"campaign: {x}" for x in cwarn]
    for w in warn:
        print("warn ", w)
    for x in errs:
        print("ERROR", x)
    print(f"{a.id}: {len(e.get('measures', []))} measures, {len(errs)} errors, {len(warn)} warnings")
    return 1 if errs else 0


def accepted(measure_id, pins, measure_sha=None):
    """{model_slug: set(seeds)} with accepted runs for these pins (and this measure text, if given)."""
    from build_prompt import prompt_hashes
    from reconcile import same_prompt
    hashes = prompt_hashes(pins["prompt_version"])
    out = defaultdict(set)
    for f in (RUNS / measure_id).glob("*/run*.attempt*.json"):
        e = json.loads(f.read_text())
        m = e["manifest"]
        if e.get("accepted") and m["prompt_version"] == pins["prompt_version"] \
                and m["concern_list_version"] == pins["concern_list_version"] \
                and (measure_sha is None or m["sha256"]["measure"] == measure_sha) and same_prompt(m, hashes):
            out[f.parent.name].add(m["seed"])
    return out


def cmd_run(a, rest):
    e = load(a.id)
    if cmd_check(a):
        sys.exit("fix errors first")
    opt = lambda k, d=None: rest[rest.index(k) + 1] if k in rest else d
    import re
    slug = f"{opt('--provider')}__{re.sub(r'[^A-Za-z0-9._-]', '_', opt('--model'))}"
    runs, first = int(opt("--runs", 3)), int(opt("--first-seed", 1))
    base = [x for i, x in enumerate(rest) if x not in ("--runs", "--first-seed")
            and (i == 0 or rest[i - 1] not in ("--runs", "--first-seed"))]
    todo = []
    for m in e["measures"]:
        mid = mid_of(m)
        have = accepted(mid, e["pins"], sha_of(m)).get(slug, set())
        for seed in range(first, first + runs):
            if seed not in have:
                todo.append((m["file"], seed))
    print(f"{len(todo)} measure x seed runs to do for {slug} ({len(e['measures']) * runs - len(todo)} already accepted)")
    by_seed = defaultdict(list)
    for f, s in todo:
        by_seed[s].append(f)
    rc = 0
    for seed, files in sorted(by_seed.items()):
        rc |= subprocess.run([sys.executable, str(ROOT / "tools/run_batch.py"), *files, "--jobs", str(a.jobs), "--",
                              *base, "--runs", "1", "--first-seed", str(seed)]).returncode
    return rc


def cmd_status(a):
    e = load(a.id)
    rows, models = [], set()
    for m in e["measures"]:
        mid = mid_of(m)
        acc = accepted(mid, e["pins"], sha_of(m))
        models |= set(acc)
        rows.append((m["code"], acc))
    models = sorted(models)
    print(f"{a.id} (pins: prompt {e['pins']['prompt_version']}, concerns {e['pins']['concern_list_version']})")
    print("measure".ljust(17) + "".join(s.split("__")[-1][:26].ljust(28) for s in models))
    for code, acc in rows:
        print(code[:16].ljust(17) + "".join(str(len(acc.get(s, ()))).ljust(28) for s in models))
    return 0


def cmd_gate(a):
    """Every model used in the election must have a full bias-suite run with the same pins."""
    e = load(a.id)
    pairs = yaml.safe_load((ROOT / "tests/bias/pairs.yaml").read_text())["pairs"]
    import hashlib
    bias_ids = [(json.loads(f.read_text())["measure_id"], hashlib.sha256(f.read_bytes()).hexdigest())
                for f in sorted((ROOT / "tests/bias/measures").glob("*.json"))]
    used = set()
    for m in e["measures"]:
        used |= set(accepted(mid_of(m), e["pins"], sha_of(m)))
    rc = 0
    for slug in sorted(used):
        covered = sum(1 for b, s in bias_ids if accepted(b, e["pins"], s).get(slug))
        ok = covered == len(bias_ids)
        rc |= not ok
        print(f"{'pass' if ok else 'FAIL'} {slug}: bias suite {covered}/{len(bias_ids)} measures ({len(pairs)} pairs)")
    if not rc:
        print("Run `python3 tools/bias_check.py compare` and review tests/bias/report.md before publishing.")
    return rc


def cmd_build(a):
    args = [sys.executable, str(ROOT / "tools/build_site.py")]
    if a.ids:
        args += ["--elections", a.ids]
    return subprocess.run(args).returncode


def main():
    argv = sys.argv[1:]
    rest = argv[argv.index("--") + 1:] if "--" in argv else []
    argv = argv[:argv.index("--")] if "--" in argv else argv
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new"); p.add_argument("id"); p.add_argument("--name", required=True); p.add_argument("--date", required=True)
    for c in ("check", "status", "gate"):
        sub.add_parser(c).add_argument("id")
    for c in ("run", "all"):
        p = sub.add_parser(c); p.add_argument("id"); p.add_argument("--jobs", type=int, default=5)
    p = sub.add_parser("build"); p.add_argument("ids", nargs="?", default="")
    a = ap.parse_args(argv)
    if a.cmd == "new":
        return cmd_new(a)
    if a.cmd == "check":
        return cmd_check(a)
    if a.cmd == "run":
        return cmd_run(a, rest)
    if a.cmd == "status":
        return cmd_status(a)
    if a.cmd == "gate":
        return cmd_gate(a)
    if a.cmd == "build":
        return cmd_build(a)
    if a.cmd == "all":
        rc = cmd_run(a, rest)
        cmd_status(a)
        a.ids = a.id
        return rc | cmd_build(a)


if __name__ == "__main__":
    sys.exit(main() or 0)

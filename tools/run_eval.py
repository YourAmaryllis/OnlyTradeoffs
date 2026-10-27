"""Run one measure through one model, K times, and keep everything.

Every model receives the byte-identical system and user messages produced by
build_prompt.py. No vendor-specific structured-output mode is used, so the
instruction really is the same everywhere; the JSON is parsed from the text reply
and checked by validate_output.py. A rejected attempt is retried (up to
--retries) and every attempt, accepted or not, is saved (DESIGN.md §5.7).

Providers (model IDs are pinned by the caller and recorded with each run):
  bedrock   AWS Bedrock Converse API. Uses --aws-profile / AWS_PROFILE and --region.
  vertex    Google Vertex AI (google-genai). Uses application-default credentials,
            --gcp-project, --gcp-location.
  openai    Any OpenAI-compatible endpoint: --base-url and an API key from the
            env var named by --key-env (xAI: https://api.x.ai/v1, XAI_API_KEY).

Long measures (more than --part-words words) are evaluated in parts: runs of consecutive
clauses, each its own call with the full text as context and prompts/part-v1.md saying which
clauses to cover. Each part is validated on its own clauses and retried on its own; a part that
already passed is reused. When every part has passed, the parts are merged (evidence unioned per
value, result recomputed from the evidence) and the merge is validated like a normal run.

Usage:
  python3 tools/run_eval.py <measure.json> --provider vertex --model gemini-2.5-pro --runs 3
Output: runs/<measure_id>/<provider>__<model>/run<seed>.attempt<n>.json
        (parts: part-run<seed>-p<k>.attempt<n>.json, referenced from the merged run file)
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompt import ROOT, build, parts_of  # noqa: E402
from validate_output import result_of  # noqa: E402
from validate_output import validate  # noqa: E402


def call_bedrock(a, system, user):
    import boto3
    sess = boto3.Session(profile_name=a.aws_profile, region_name=a.region)
    r = sess.client("bedrock-runtime").converse(
        modelId=a.model,
        system=[{"text": system}],
        messages=[{"role": "user", "content": [{"text": user}]}],
        inferenceConfig={"maxTokens": a.max_tokens, **({"temperature": a.temperature} if a.temperature is not None else {})},
    )
    text = "".join(b.get("text", "") for b in r["output"]["message"]["content"])
    return text, {"usage": r.get("usage"), "stop_reason": r.get("stopReason")}


def call_vertex(a, system, user):
    from google import genai
    from google.genai import types
    client = genai.Client(vertexai=True, project=a.gcp_project, location=a.gcp_location)
    cfg = types.GenerateContentConfig(system_instruction=system, max_output_tokens=a.max_tokens,
                                      **({"temperature": a.temperature} if a.temperature is not None else {}))
    r = client.models.generate_content(model=a.model, contents=user, config=cfg)
    u = r.usage_metadata
    return r.text or "", {"usage": u.model_dump() if u else None,
                          "stop_reason": str(r.candidates[0].finish_reason) if r.candidates else None,
                          "model_version": getattr(r, "model_version", None)}


def call_openai(a, system, user):
    from openai import OpenAI
    client = OpenAI(base_url=a.base_url, api_key=os.environ[a.key_env])
    r = client.chat.completions.create(
        model=a.model, max_tokens=a.max_tokens,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        **({"temperature": a.temperature} if a.temperature is not None else {}))
    return r.choices[0].message.content or "", {"usage": r.usage.model_dump() if r.usage else None,
                                                "stop_reason": r.choices[0].finish_reason,
                                                "model_version": r.model}


CALL = {"bedrock": call_bedrock, "vertex": call_vertex, "openai": call_openai}
TRANSIENT = re.compile(r"429|RESOURCE_EXHAUSTED|Throttling|TooManyRequests|503|UNAVAILABLE|overloaded|timed? ?out", re.I)


def parse_json(text):
    """Strip one pair of markdown fences if present; record that we did."""
    t = text.strip()
    m = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", t, re.S)
    return json.loads(m.group(1) if m else t), bool(m)


def normalize(parsed):
    """Strip square brackets a model copies from the prompt's clause layout ("[Prop 41 Sec. 1]").
    Only clause IDs are touched, never quotes or text; every change is recorded in the attempt file."""
    changes = []

    def fix(d):
        cid = d.get("clause_id")
        if isinstance(cid, str) and cid.startswith("[") and cid.endswith("]"):
            d["clause_id"] = cid[1:-1]
            changes.append(cid)
    if isinstance(parsed, dict):
        for key in ("restatements", "analysis", "flags"):
            for d in parsed.get(key) or []:
                if isinstance(d, dict):
                    fix(d)
        for v in parsed.get("values") or []:
            for d in (v.get("evidence") or []) if isinstance(v, dict) else []:
                if isinstance(d, dict):
                    fix(d)
    return sorted(set(changes))


def next_attempt(out_dir, stem):
    done = [int(re.search(r"attempt(\d+)", f.name).group(1)) for f in out_dir.glob(f"{stem}.attempt*.json")]
    return max(done, default=0) + 1


def attempt_loop(a, measure, clist, out_dir, seed, part, stem):
    """Call the model until one attempt passes validation (or retries run out). Every attempt is
    saved as <stem>.attempt<n>.json, numbered after any already saved. Returns (accepted, path)."""
    prompt_path, rec = build(a.measure, seed, a.concerns, out_dir, part)
    system, user = rec["messages"][0]["content"], rec["messages"][1]["content"]
    first = next_attempt(out_dir, stem)
    attempt, bad_answers, waits = first - 1, 0, 0
    while bad_answers <= a.retries:
        attempt += 1
        t0 = time.time()
        entry = {"manifest": rec["manifest"], "prompt_file": prompt_path.name,
                 "provider": a.provider, "model": a.model, "attempt": attempt,
                 "params": {"max_tokens": a.max_tokens, "temperature": a.temperature},
                 "started_at": datetime.now(timezone.utc).isoformat()}
        try:
            text, meta = CALL[a.provider](a, system, user)
            entry.update(meta=meta, raw_text=text)
            try:
                parsed, fenced = parse_json(text)
                changes = normalize(parsed)
                entry.update(parsed=parsed, stripped_fences=fenced, normalized=changes)
                errs = validate(measure, parsed, clist, part[2] if part else None)
            except json.JSONDecodeError as e:
                errs = [f"not valid JSON: {e}"]
        except Exception as e:  # network/auth/quota: record, and back off if it's transient
            entry.update(error=f"{type(e).__name__}: {e}")
            errs = ["call failed"]
        entry.update(seconds=round(time.time() - t0, 1), errors=errs, accepted=not errs)
        path = out_dir / f"{stem}.attempt{attempt}.json"
        path.write_text(json.dumps(entry, indent=2, ensure_ascii=False))
        print(f"{stem} attempt {attempt}: {'ACCEPTED' if not errs else 'REJECTED'} "
              f"({entry['seconds']}s) {'; '.join(errs[:3])}")
        if not errs:
            return 1, path
        if "error" in entry:
            if not TRANSIENT.search(entry["error"]) or waits >= a.max_waits:
                break
            # Rate limit or overload: saved, but not counted against --retries (those are for bad answers).
            waits += 1
            time.sleep(min(30 * 2 ** (waits - 1), 300))
            continue
        bad_answers += 1
    return 0, None


def merge(measure, outputs):
    """Merge part outputs into one output for the whole measure."""
    vals = {}
    for o in outputs:
        for v in o["values"]:
            e = vals.setdefault(v["value_id"], {"value_id": v["value_id"], "result": "none", "evidence": []})
            seen = {(x["clause_id"], x["quote"], x["effect"]) for x in e["evidence"]}
            e["evidence"] += [x for x in v["evidence"] if (x["clause_id"], x["quote"], x["effect"]) not in seen]
    for e in vals.values():
        e["result"] = result_of(x["effect"] for x in e["evidence"])
    return {"measure_id": measure["measure_id"],
            "restatements": [r for o in outputs for r in o["restatements"]],
            "values": list(vals.values()),
            "analysis": [x for o in outputs for x in o["analysis"]],
            "flags": [x for o in outputs for x in o["flags"]]}


def run_parts(a, measure, clist, out_dir, seed, parts):
    n = len(parts)
    files = []
    for k, ids in enumerate(parts, 1):
        stem = f"part-run{seed}-p{k}"
        _, rec = build(a.measure, seed, a.concerns, out_dir, (k, n, ids))
        reuse = None
        for f in sorted(out_dir.glob(f"{stem}.attempt*.json")):
            e = json.loads(f.read_text())
            if e.get("accepted") and e["manifest"]["sha256"] == rec["manifest"]["sha256"]:
                reuse = f
        if reuse:
            print(f"{stem}: reusing {reuse.name}")
            files.append(reuse)
            continue
        ok, path = attempt_loop(a, measure, clist, out_dir, seed, (k, n, ids), stem)
        if not ok:
            print(f"seed {seed}: part {k}/{n} did not pass; not merging")
            return 0
        files.append(path)
    outputs = [json.loads(f.read_text())["parsed"] for f in files]
    merged = merge(measure, outputs)
    errs = validate(measure, merged, clist)
    prompt_path, rec = build(a.measure, seed, a.concerns, out_dir)
    attempt = next_attempt(out_dir, f"run{seed}")
    entry = {"manifest": {**rec["manifest"], "parts": n}, "prompt_file": None,
             "provider": a.provider, "model": a.model, "attempt": attempt,
             "params": {"max_tokens": a.max_tokens, "temperature": a.temperature, "part_words": a.part_words},
             "parts": [f.name for f in files],
             "meta": {"model_version": next((json.loads(f.read_text()).get("meta") or {}).get("model_version")
                                            for f in files)},
             "parsed": merged, "errors": errs, "accepted": not errs,
             "started_at": datetime.now(timezone.utc).isoformat()}
    (out_dir / f"run{seed}.attempt{attempt}.json").write_text(json.dumps(entry, indent=2, ensure_ascii=False))
    print(f"run{seed}: merged {n} parts -> {'ACCEPTED' if not errs else 'REJECTED ' + '; '.join(errs[:3])}")
    return int(not errs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("measure")
    ap.add_argument("--provider", choices=CALL, required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--first-seed", type=int, default=1)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--temperature", type=float, default=None, help="default: vendor default (recorded as null)")
    ap.add_argument("--max-waits", type=int, default=6, help="rate-limit backoffs per run (30s, 60s, ... up to 5 min each)")
    ap.add_argument("--part-words", type=int, default=5000, help="evaluate in parts above this many words")
    ap.add_argument("--concerns", default=str(ROOT / "concerns/v1-draft.yaml"))
    ap.add_argument("--out", default=str(ROOT / "runs"))
    ap.add_argument("--aws-profile", default=os.environ.get("AWS_PROFILE"))
    ap.add_argument("--region", default="us-west-2")
    ap.add_argument("--gcp-project", default=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    ap.add_argument("--gcp-location", default="global")
    ap.add_argument("--base-url", default="https://api.x.ai/v1")
    ap.add_argument("--key-env", default="XAI_API_KEY")
    a = ap.parse_args()

    measure = json.loads(Path(a.measure).read_text())
    clist = yaml.safe_load(Path(a.concerns).read_text())
    slug = f"{a.provider}__{re.sub(r'[^A-Za-z0-9._-]', '_', a.model)}"
    out_dir = Path(a.out) / measure["measure_id"] / slug
    ok = 0
    out_dir.mkdir(parents=True, exist_ok=True)
    words = sum(len(c["text"].split()) for c in measure["clauses"])
    parts = parts_of(measure, a.part_words) if words > a.part_words else None
    if parts:
        print(f"{measure['measure_id']}: {words} words -> {len(parts)} parts")
    for seed in range(a.first_seed, a.first_seed + a.runs):
        if parts:
            ok += run_parts(a, measure, clist, out_dir, seed, parts)
        else:
            ok += attempt_loop(a, measure, clist, out_dir, seed, None, f"run{seed}")[0]
    print(f"{ok}/{a.runs} runs accepted → {out_dir}")
    sys.exit(0 if ok == a.runs else 1)


if __name__ == "__main__":
    main()

"""Render the exact messages sent to every model for one measure and one run.

Input: a measure file (JSON): {"measure_id", "clauses": [{"id", "text"}], "current_law": str|null}
Output: <out_dir>/<measure_id>.run<seed>.prompt.json, holding the system and user
messages as sent, plus a manifest (prompt, concern-list and schema versions,
SHA-256 of every input, the seed, and the concern order the seed produced).

Concern order is shuffled per run (DESIGN.md §5.3), but with a recorded seed, so
anyone can rebuild the identical prompt (§5.7).

With --paste, also writes <...>.paste.txt: the system and user messages as one
block, for the copy-paste option of the "Verify this" panel (§5.7).

Usage: python3 tools/build_prompt.py <measure.json> --seed N [--out runs/] [--paste]
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPT_VERSION = "v1"
SCHEMA = ROOT / "schema/eval-output-v1.schema.json"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def render_concern(c):
    lines = [f"{c['id']}: {c['name']}", f"  axis: {c['axis']}"]
    lines.append(f"  advances when: {c['advances_when']}")
    if c["mirror"]:
        lines.append(f"  mirror: {c['mirror']}")
    if c["check_against"]:
        lines.append(f"  check against: {', '.join(c['check_against'])}")
    return "\n".join(lines)


def prompt_hashes(version=None):
    """SHA-256 of the prompt files a run must have used to count for `version` (current files)."""
    v = version or PROMPT_VERSION
    files = {"system_prompt": ROOT / f"prompts/system-{v}.md", "user_template": ROOT / f"prompts/user-{v}.md",
             "schema": ROOT / f"schema/eval-output-{v}.schema.json"}
    return {k: sha(f.read_text()) for k, f in files.items() if f.exists()}


def parts_of(measure, max_words):
    """Split clauses into runs of consecutive clauses of at most max_words (one clause may exceed it)."""
    parts, cur, n = [], [], 0
    for c in measure["clauses"]:
        w = len(c["text"].split())
        if cur and n + w > max_words:
            parts.append(cur)
            cur, n = [], 0
        cur.append(c["id"])
        n += w
    if cur:
        parts.append(cur)
    return parts


def build(measure_path, seed, concerns_path, out_dir, part=None):
    """part: None, or (k, n, [clause ids]) to build the prompt for part k of n."""
    measure_raw = Path(measure_path).read_bytes()
    measure = json.loads(measure_raw)
    concerns_raw = Path(concerns_path).read_bytes()
    clist = yaml.safe_load(concerns_raw)
    system = (ROOT / f"prompts/system-{PROMPT_VERSION}.md").read_text()
    template = (ROOT / f"prompts/user-{PROMPT_VERSION}.md").read_text()
    schema_raw = SCHEMA.read_text()
    # The model gets only the structural top-level keys of the schema (no $schema, $id, title, description):
    # in the first Gemini batches, 38 attempts copied metadata keys into the answer.
    schema_for_model = json.dumps({k: v for k, v in json.loads(schema_raw).items()
                                   if k in ("type", "additionalProperties", "required", "properties")}, indent=2, ensure_ascii=False)

    order = [c["id"] for c in clist["concerns"]]
    random.Random(seed).shuffle(order)
    by_id = {c["id"]: c for c in clist["concerns"]}

    user = (template
            .replace("{{measure_id}}", measure["measure_id"])
            .replace("{{clauses}}", "\n\n".join(f"[{c['id']}]\n{c['text']}" for c in measure["clauses"]))
            .replace("{{current_law}}", measure.get("current_law") or "Not provided. Answer Q1 from the measure text alone and say that current law was not provided.")
            .replace("{{values}}", "\n\n".join(render_concern(by_id[i]) for i in order))
            .replace("{{questions}}", "\n".join(f"{q['id']}: {q['text']}" for q in clist["questions"]))
            .replace("{{flags}}", "\n".join(f"{f['id']}: {f['text']}" for f in clist["flags"]))
            .replace("{{schema}}", schema_for_model))
    part_raw = None
    if part:
        k, n, ids = part
        part_raw = (ROOT / f"prompts/part-{PROMPT_VERSION}.md").read_text()
        block = part_raw.replace("{{k}}", str(k)).replace("{{n}}", str(n)).replace("{{ids}}", ", ".join(ids))
        user = user.replace("## Current law this measure changes", block + "\n## Current law this measure changes", 1)
    assert "{{" not in user, "unfilled placeholder in user template"

    record = {
        "manifest": {
            "measure_id": measure["measure_id"],
            "prompt_version": PROMPT_VERSION,
            "concern_list_version": clist["version"],
            "concern_list_frozen": clist["frozen"],
            "seed": seed,
            "concern_order": order,
            "sha256": {
                "measure": sha(measure_raw),
                "concern_list": sha(concerns_raw),
                "system_prompt": sha(system),
                "user_template": sha(template),
                "schema": sha(schema_raw),
                "user_message": sha(user),
                **({"part_template": sha(part_raw)} if part_raw else {}),
            },
        },
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }
    if part:
        record["manifest"]["part"] = {"index": part[0], "of": part[1], "clauses": part[2]}
    out = Path(out_dir) / (f"{measure['measure_id']}.run{seed}.prompt.json" if not part
                           else f"{measure['measure_id']}.run{seed}.part{part[0]}.prompt.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    return out, record


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("measure")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--concerns", default=str(ROOT / "concerns/v1-draft.yaml"))
    ap.add_argument("--out", default=str(ROOT / "runs"))
    ap.add_argument("--paste", action="store_true")
    a = ap.parse_args()
    out, rec = build(a.measure, a.seed, a.concerns, a.out)
    if a.paste:
        sys_msg, user_msg = (m["content"] for m in rec["messages"])
        paste = out.with_name(out.name.replace(".prompt.json", ".paste.txt"))
        paste.write_text(f"{sys_msg}\n\n---\n\n{user_msg}")
        print(paste)
    print(f"{out}  ({len(rec['messages'][1]['content']):,} chars in user message; concern list {rec['manifest']['concern_list_version']})")

"""Build the do-it-yourself packs so anyone can run the method on their own model.

All packs are generated from the same files the official pipeline uses
(prompts/system-v1.md, concerns/v1-draft.yaml, schema/eval-output-v1.schema.json)
plus prompts/portable-v1.md (the chat workflow), so they can't drift apart.

  dist/portable/claude-skill/only-tradeoffs/   Claude skill (SKILL.md + files)
  dist/portable/gemini-gem/                    Gem instructions + knowledge files
  dist/portable/chatgpt-gpt/                   Custom GPT instructions + knowledge files
  dist/portable/any-chat/paste-prompt.md       one self-contained message for any chat
                                               (Grok, open-weights chat UIs, etc.)
  dist/portable/MANIFEST.json                  versions and SHA-256 of every file

Usage: python3 tools/build_portable.py
"""
import hashlib
import json
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist/portable"
GPT_LIMIT = 8000  # custom GPT instruction field limit, characters

system = (ROOT / "prompts/system-v1.md").read_text()
workflow = (ROOT / "prompts/portable-v1.md").read_text().replace("{{system}}", system)
concerns_raw = (ROOT / "concerns/v1-draft.yaml").read_text()
# Same schema the official runs send: document metadata removed (see build_prompt.py).
schema_raw = json.dumps({k: v for k, v in json.loads((ROOT / "schema/eval-output-v1.schema.json").read_text()).items()
                         if k in ("type", "additionalProperties", "required", "properties")}, indent=2, ensure_ascii=False)
clist = yaml.safe_load(concerns_raw)
version = f"prompt v1, values {clist['version']}{'' if clist['frozen'] else ' (draft, not frozen)'}"

skill_md = f"""---
name: only-tradeoffs
description: Evaluate the official text of a US ballot measure or law against a fixed, label-free list of values people hold, showing for each value whether the text supports it, conflicts with it, or both, with the exact words. Use when someone asks what a ballot measure, proposition, initiative, or bill actually does, or wants to verify an Only Tradeoffs evaluation.
---

# Only Tradeoffs ({version})

Files in this skill:
- `values.yaml`: the value list, analysis questions, and text-quality flags
- `schema.json`: the JSON the evaluation must match

Read both files before evaluating.

{workflow}
"""

gem_md = f"""# Only Tradeoffs ({version})

Paste everything below the line into the Gem's **Instructions** field, and upload `values.yaml` and `schema.json` as the Gem's **Knowledge** files.

---

{workflow}
"""

paste_md = f"""# Only Tradeoffs: paste prompt ({version})

Copy everything below the line into a new chat with any model, then paste the official text of the measure after it.

---

{workflow}

---

## values.yaml

```yaml
{concerns_raw}```

## schema.json

```json
{schema_raw}
```

---

Measure text follows. If none is given yet, ask for it (Step 1).
"""


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


if OUT.exists():
    shutil.rmtree(OUT)
for d in ("claude-skill/only-tradeoffs", "gemini-gem", "chatgpt-gpt"):
    write(f"{d}/values.yaml", concerns_raw)
    write(f"{d}/schema.json", schema_raw)
write("claude-skill/only-tradeoffs/SKILL.md", skill_md)
write("gemini-gem/instructions.md", gem_md)
write("chatgpt-gpt/instructions.md", gem_md.replace("Gem's **Instructions** field", "GPT's **Instructions** field")
      .replace("Gem's **Knowledge** files", "GPT's **Knowledge** files"))
write("any-chat/paste-prompt.md", paste_md)

gpt_body = workflow
if len(gpt_body) > GPT_LIMIT:
    raise SystemExit(f"GPT instructions are {len(gpt_body)} chars, over the {GPT_LIMIT} limit")

manifest = {"version": version, "files": {
    str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(OUT.rglob("*")) if p.is_file()}}
write("MANIFEST.json", json.dumps(manifest, indent=2))
print(f"{OUT.relative_to(ROOT)}: {len(manifest['files'])} files; {version}; GPT instructions {len(gpt_body)}/{GPT_LIMIT} chars")

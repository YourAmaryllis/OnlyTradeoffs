# Only Tradeoffs

Evaluates the official text of US ballot measures clause by clause against a fixed, label-free list of concerns, and shows for every concern whether the text supports it, conflicts with it, or both, with the exact words. It also shows who funds, supports, and opposes each measure, kept apart from the text analysis. No verdicts, no scores, no recommendations. The same instructions run on several models, and everything needed to rerun them is published.

Start with `DESIGN.md`.

## Layout

| Path | What it is |
|---|---|
| `DESIGN.md` | Mission, rules, method, pipeline, website, next steps |
| `research/` | Phase 0: sources, per-perspective concerns (labeled, audit only), the label-free concern list, bias review and response, coverage audit |
| `concerns/v1-draft.yaml` | **Generated** from `research/concerns-v1.md`. What the models receive. No perspective labels |
| `prompts/` | System prompt, user template, blocked terms, chat workflow for the do-it-yourself packs |
| `schema/` | JSON schema every model output must match |
| `tests/fixtures/` | Synthetic measure with a valid output and a defective one |
| `tests/bias/` | Mirror and swap pairs (`pairs.yaml`), expanded measures, generated report |
| `runs/` | Every model attempt, with its prompt, manifest, raw reply, and validation result |
| `dist/portable/` | **Generated.** Claude skill, Gemini Gem, custom GPT, and a paste prompt for any chat |
| `tools/` | Scripts below |

## Commands

```
python3 tools/coverage_audit.py research           # research/coverage-audit.md
python3 tools/build_concerns.py                     # concerns/v1-draft.yaml
python3 tools/build_prompt.py <measure.json> --seed 1 [--paste]
python3 tools/validate_output.py <measure.json> <output.json>
python3 tools/run_eval.py <measure.json> --provider vertex|bedrock|openai --model <id> --runs 3
python3 tools/run_batch.py <measures...> --jobs 6 -- <run_eval args>
python3 tools/bias_check.py expand | compare
python3 tools/build_portable.py                     # dist/portable/
```

Python 3 with `pyyaml`, `jsonschema`, and, per provider, `boto3`, `google-genai`, or `openai`.

## Requirements for importing scanned filings

- `brew install tesseract poppler` (Tesseract 5, `pdftoppm`)
- `pip install pdfplumber rapidocr_onnxruntime`
- `python3 tools/import_measure.py --pdf ... --ocr vote` (default) reads each page three ways and votes; see `tools/ocr_vote.py`.

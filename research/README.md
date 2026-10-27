# Phase 0 Research — Concern List

Status: **v1 draft, revision 3** (after `bias-review.md` and its re-review), 2026-10-26. Not frozen. See "Before freezing" below.

## Files, in the order to read them

| File | What it is |
|---|---|
| `sources.md` | Registry of every source used (S01–S39), with date, URL, and **how much of it we actually read** (F / A / S / K) |
| `perspectives.md` | Step 1: concerns collected per perspective, in each perspective's own terms, each citing sources. **Labeled; audit only.** |
| `bias-review.md` | External bias review of revision 1 |
| `bias-review-response.md` | Point-by-point response: what was accepted, changed, or rebutted. Round 2 covers the reviewer's re-review |
| `concerns-v1.md` | Steps 2–4: the merged, label-free list. 83 concerns (revision 4) + 9 analysis questions + 9 text-quality flags, each concern with its trail back to `perspectives.md`. Includes merge, exclusion, and gap logs. |
| `coverage-audit.md` | Step 5: **generated** by `tools/coverage_audit.py`. Reverse index showing every perspective entry reached a concern, plus which concerns rest on a single perspective, and which perspectives are backed by a source read in full. |
| `raw/` | Archived copies of fetched sources (Pew 2026 typology; 2024 Republican and Democratic platforms, full text) |

## Tracing a concern back to its sources

`concerns-v1.md` C41 → trail `CON-07, CL-09` → `perspectives.md` CON-07 cites S05, S14 → `sources.md` S05 = 2024 Republican platform (read in full), S14 = Institute for Justice (search summary only).

## What came out of this pass

1. **Mirror concerns and "check against".** Where values directly oppose on the same axis (firearm ownership / firearm regulation, abortion access / prenatal protection, and 4 more), both sides are separate concerns; neither is the default. Where values are only *often* in tension (ease of voting / verification, school options / public-school funding), they're linked as "check against", and a cost is recorded only when a quoted clause supports it. *(Revised after the bias review; the first draft auto-scored every pair.)*
2. **Directional concerns (⇄).** Some axes have no built-in good direction (who decides, local vs. state control, tax distribution, sentencing). The finding states which way the text moves; the voter judges.
3. **Economists became questions, not concerns.** The market-oriented and interventionist lists turned out to be largely the *same questions asked with different expectations*: compared to what, at what cost, who pays, what incentives, who gains power, is the evidence settled. They're merged into 9 analysis questions applied to every clause.
4. **Shared ground is larger than expected.** Cost of living, energy cost, transparency, government favoritism toward specific firms, due process, and preemption (each side objects when it's used against them) all came from more than one perspective.

## Before freezing v1

- [ ] Upgrade **S** (search summary) and **K** (from knowledge) sources to **F** (read in full). 5 of the 38 sources are read in full (S01, S02, S05, S06, S39); the other 33 are S or K. (ID S18 is unused.)
- [ ] Add the sources listed in `sources.md` "Gaps", and close `gap` and `wording-test` concerns (see Log 3 in `concerns-v1.md`).
- [ ] Decide on the three remaining candidate additions: animal welfare, tribal sovereignty/gaming, rural interests. (Redistricting became C70.)
- [ ] Wording review: for every concern, would each perspective call the name and axis fair? Run this with multiple models *and* human reviewers from each perspective.
- [ ] Review the single-perspective concerns listed in `coverage-audit.md`.
- [ ] Raise "Concerns with two or more perspectives backed by a full read" (last line of `coverage-audit.md`; re-run after revision 4). Read S08 manually (blocks automated fetches).
- [ ] Decide on list size: 83 is readable only with grouping (the site shows only concerns a measure touches; no personal filter, by decision). Cut duplicates, never single-perspective or `gap` rows (bias review §9).

Regenerate the audit after any edit:

```
python3 tools/coverage_audit.py research
```

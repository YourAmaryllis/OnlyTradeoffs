# Only Tradeoffs — Design

> *What's in the text, and which concerns it supports or conflicts with.*

Status: draft v0.2 · 2026-10-27 · Domain: onlytradeoffs.org (watch onlytradeoffs.com, expires 2026-12-07)

---

## 1. What this is

A website that reads the **original legal text** of every measure on American ballots (state, county, city, district) and shows, for every concern on a fixed list of concerns people hold, whether the text **supports** it, **conflicts with** it, both, or neither, with the exact words that do it.

It is built for a voter who wants to know what a measure actually does, to the things they care about **and** to the things other people care about, without anyone telling them how to vote or which side they're "supposed" to be on. The site shows every concern a measure touches, the same way for every reader; it doesn't filter to "your" concerns, because seeing the measure from other people's concerns is the point.

Later phases extend the same engine to any enacted law or pending bill.

> **Terminology (2026-10-27):** what this document calls a **concern** is shown to readers, and named in the prompt and output schema, as a **value**: something some people want more of, with a direction ("supported when…"). Economists' nearest words are *values* (as in trading off competing values) or *objectives/criteria* (decision analysis). Internal file names (`concerns/`, `research/concerns-v1.md`, `build_concerns.py`) and IDs (C01…) keep the old name, because IDs are stable.

## 2. Non-negotiables

These are product rules, not guidelines. Anything that breaks one is a bug.

1. **Text only.** The input to the evaluation is the official measure text, plus the current law it changes. No voter guides, no pro/con arguments, no fiscal-analyst summaries, no ballot titles written by officials, no news, no party positions.
2. **No tribes anywhere.** The published site, the evaluation prompts and the concern list never mention political parties, ideologies, movements, or public figures. Concerns are named by *what they are* ("household tax burden"), never by *who holds them*.
3. **Every concern, both directions.** Every model reports a result for every concern on the list. The page shows every concern the text supports and every concern it conflicts with. No personal filter hides any of them. If a measure shows only supports or only conflicts, that triggers a review, not a publish.
4. **Every claim cites a clause.** A finding without a quoted clause doesn't ship.
5. **Fact vs. inference is labeled.** "The text says X" is kept separate from "X likely leads to Y". Effects that depend on future regulations or court rulings are marked as such.
6. **Same instruction, many models.** Every evaluation runs identically on several AI models from different vendors. Disagreement is shown, not hidden or averaged away.
7. **No gain/loss framing.** The site never says what a vote "gains" or "gives up", and never frames results as "if Yes wins / if No wins": calling something a gain already decides what is desirable. Results are relative to each concern ("supports C33"), never to the reader. (Decided 2026-10-27; this replaced the earlier Yes/No ledgers.)
8. **No recommendations.** No scores, grades, "verdicts" or vote suggestions. The site never adds up the tradeoffs for you; you decide what you weigh.
9. **Fully open and reproducible.** Everything sent to the models is published: the exact prompts, the concern list, the output schema, the source text (with its hash), the model versions and settings, and every raw output. Anyone can rerun an evaluation themselves and compare. See §5.7.

## 3. Phases

| Phase | Scope | Notes |
|---|---|---|
| **0. Foundation** | Concern research → neutral concern list; eval prompt; multi-model harness; bias test suite | Nothing is published until the bias suite passes |
| **1. Ballot measures** | Statewide measures first, then the largest cities/counties | Text-only evaluation. No cross-referencing |
| **2. Cross-reference** | *After* the text evaluation is frozen: compare against major party platforms, independent and legacy news reports | Shown on a separate tab, clearly marked as "what others say". It never alters the text evaluation |
| **3. Laws & bills** | Enacted statutes, pending legislation | Same engine; bills are longer and amend more existing law, so the "current law" diff matters more |

**Timing:** the 2026 general election is 2026-11-03, eight days away. That's too soon for a credible launch. Treat 2026 measures as the **pilot corpus** (the texts are final and public, which makes them ideal for tuning), and aim for a public launch ahead of the 2027 off-year elections and the 2028 primaries.

## 4. Building the concern list

This is the most important part of the project. If the concerns are lopsided, a neutral evaluator will still produce lopsided results.

### 4.1 Why the prior checklist is being reworked

`reference/prior-checklist-v0.md` has a sound per-clause method and a useful list of legal mechanisms. But:

- It's organized by political camp, which breaks rule 2.
- It's asymmetric: the progressive section is written from its critics' viewpoint (its "red-flag phrases" are things opponents watch for, not things progressives value).
- Classical liberals are missing.
- It has no economist lens.
- It only flags risks, with no gain column.

**What we keep:** quote → what it does → which concern; the mechanism list (continuous appropriation, "notwithstanding", private right of action, rule-making delegation, preemption, sunset); the cross-cutting text-quality checks.

### 4.2 Process

**Step 1: Research by perspective (labeled, kept out of prompts and measure pages).** For each perspective, build a sourced list of what its voters and thinkers actually care about, *in their own words, from their own sources*:

| Perspective | Primary sources to mine |
|---|---|
| Conservative | Party and movement platforms, think-tank issue pages (e.g. Heritage, AEI, Claremont), conservative survey research |
| Classical liberal / libertarian | Cato, Reason, FIRE, IJ, Mercatus; Hayek and Friedman |
| Progressive | Party platforms, think tanks (e.g. CAP, EPI, Roosevelt Institute), advocacy groups' issue pages |
| Market-oriented economists | Thomas Sowell, Milton Friedman, F.A. Hayek, James Buchanan (public choice), Gary Becker |
| Interventionist / institutional economists | Joseph Stiglitz, Paul Krugman, George Akerlof, Emmanuel Saez / Gabriel Zucman, Thomas Piketty, Elinor Ostrom |
| Voters at large | Pew, Gallup, AP-NORC, and similar issue-priority polling, broken out by group, so the list reflects what voters rank highly and not just elites |

Rule for this step: **steelman each side.** Every concern must be phrased the way its holders would phrase it, and checked against that side's own sources. It must not come from the other side's description of them.

**Step 2: Flatten and strip labels.** Merge all lists into one, remove every perspective label, and dedupe. Many concerns turn out to be shared and differ only in which direction people want them to move.

**Step 3: Make each concern an axis, not a red flag.** A concern is a *thing a measure can move*, in either direction. "Household tax burden" can go up or down; "funding for public services" can go up or down. One clause often moves two concerns in opposite directions, and that **is** the tradeoff.

**Step 4: Neutrality check.** For each concern's name and description: would someone from *every* perspective agree the wording is fair? Concerns that one side would call loaded get renamed. Test with human reviewers from each perspective and with multiple models.

**Step 5: Coverage check.** Using the labeled research from step 1, confirm every perspective's top concerns are represented. This mapping is used only to audit balance. It never enters prompts or measure pages, but it is published in the methodology repo (§5.7) so anyone can check our coverage.

### 4.3 The economist lens isn't a list of concerns. It's a set of questions.

The economists contribute *how to analyze*, which applies to every clause regardless of topic:

- **Compared to what?** What's the current law this replaces? (baseline)
- **Who pays, and who benefits?** Who bears the cost in practice versus on paper? (incidence and distribution)
- **What incentives does it create?** How will people, firms and agencies respond?
- **And then what?** Second-order effects and unintended consequences.
- **What problem is it fixing?** Is there a market failure, externality, information gap or imbalance of bargaining power that the text addresses?
- **Who decides later?** How much is left to agencies, courts, or future appropriations (public choice)?
- **What does enforcement cost**, and who carries it out?
- **Can it be undone?** Constitutional vs. statutory change, sunset, amendment threshold.

Answers to these are always labeled **inference**, not fact.

**Axes are mechanical; every concern defines its sign.** An axis describes what the text changes, never the outcome supporters expect (outcomes are inference, under the analysis questions). Each concern states what counts as `advances`. Directional concerns (⇄) have no preferred direction; the finding reports which way the text moves.

**Mirror concerns and "check against".** Where values directly oppose on *the same axis* (e.g. firearm ownership vs. firearm regulation), both sides are listed as separate mirror concerns, so neither is the default; one quoted clause moves both. Concerns that are merely *often* in tension (e.g. ease of voting vs. voter verification) are linked as "check against": a reminder to look, and a cost is recorded on the related concern **only when a quoted clause supports it**. Restoring voting rights after a conviction advances ease of voting and does nothing to verification.

### 4.4 Concern list

**Superseded by `research/concerns-v1.md`** (83 concerns as of revision 4, 9 analysis questions, 9 text-quality flags, with full source trail). The v0 draft below is kept only for history.

<details><summary>v0 draft (unsourced, superseded)</summary>


**Money**
- Household tax and fee burden
- Funding for public services
- Public debt and long-term obligations (bonds, pensions)
- Voter/legislative control over future spending (continuous appropriation, automatic escalators, sunsets)
- Who pays vs. who benefits (distribution across income, region, generation)
- Cost of living (housing, energy, everyday prices)

**Work and business**
- Business costs and compliance burden
- Competition and ease of starting a business (licensing, entry barriers)
- Worker pay, benefits and safety
- Job availability
- Flexibility in how people work (contractor vs. employee)
- Collective bargaining

**Property and housing**
- Owners' freedom to use their property
- Housing supply and affordability
- Renter stability and protections

**Government power**
- Size and reach of government authority (new agencies, new mandates)
- Decisions made by elected officials vs. appointed or expert bodies
- Transparency and oversight
- Local vs. state control
- Enforcement method and litigation exposure (penalties, private lawsuits)
- Reversibility (how hard it is to change later)

**Rights and liberties**
- Speech, association and religious exercise
- Due process and fairness in the justice system
- Personal privacy and data collection
- Equal treatment under the law
- Firearms ownership and use
- Personal medical and reproductive decisions
- Parents' role in children's education and health decisions

**Safety**
- Crime prevention and public safety
- Rights and protections for victims
- Incarceration, sentencing and rehabilitation

**Public services**
- Healthcare access and cost
- Education quality and choice
- Assistance for people in need
- Infrastructure and transportation

**Environment and resources**
- Environmental quality and climate
- Energy reliability and cost
- Water and land use

**Elections and democracy**
- Ease of voting
- Election security and verifiability
- Money and influence in politics
- Citizens' ability to propose and repeal laws directly

</details>

### 4.5 Text-quality flags (structural, not concerns)

Shown separately. They describe *how the law is written*, not what it does to a concern:

- Vague or expansive definitions
- "Notwithstanding any other provision of law" and other override language
- Effect depends on future regulations
- Unfunded mandate (requires action without funding it)
- Severability clause, or the lack of one
- Effective date and phase-in
- Amendment threshold (e.g. supermajority to change; "furthers the purposes" restrictions)
- Possible single-subject issues (unrelated provisions bundled together)

## 5. Evaluation pipeline

```
discover → fetch official text → archive → segment → evaluate (N models × K runs)
        → reconcile → bias checks → human review → publish
```

### 5.1 Discovery and sources

- **Discovery** (finding which measures exist): any list is fine, including state Secretary of State calendars, county election offices, and Ballotpedia's measure lists. Lists are used only to *find* measures.
- **Text**: only from the official source (SoS, county or city clerk, legislature). Store the original PDF/HTML, its SHA-256, the source URL, and the fetch date. If the official text can't be found, the measure is marked "text unavailable"; we never fall back to a summary.
- **Current law**: for measures that amend existing law, fetch the affected sections of current statute/charter/constitution so we can build a redline (old → new). "Compared to what" depends on it.
- **Excluded from the evaluation input**: official ballot title and summary, fiscal-impact statement, arguments for/against, sponsor names. (The ballot label is shown to users for identification, but the models never see it.)

### 5.2 Segmentation

Split the text into clauses using its own structure (section/subsection numbering), and give each clause a stable ID (`CA-2026-P50 §3(b)(2)`). Every finding points to a clause ID and a quoted span.

### 5.3 Evaluation passes (identical prompt for every model)

1. **Plain-language restatement.** What each clause does, in neutral words, with no evaluation.
2. **Concern results.** For **every** concern on the list, one result: `supports` / `conflicts` / `both` / `none`, signed by the concern's "advances when" definition, with the evidence: each piece is a clause ID, an exact quote, its effect (`supports` or `conflicts`), a `why`, and `certainty: stated | likely | depends-on-implementation`. The result must match the evidence. (Through prompt v0, cells were clause × concern with `advances/costs/mixed/moves`; revision 4 of the concern list gave every concern one direction so the four results apply.)
3. **Economist questions** (§4.3) for each significant clause, all labeled inference.
4. **Text-quality flags** (§4.5).

Output is strict JSON against a schema (`schema/eval-output-v1.schema.json`), which makes model outputs comparable concern by concern.

**Long measures (2026-10-27):** above 5,000 words a measure is evaluated in parts of consecutive clauses (`run_eval.py --part-words`). Each part is its own call with the **full text as context** and `prompts/part-v1.md` naming the clauses to cover; it is validated on those clauses only and retried on its own. When all parts pass, they are merged (evidence unioned per value, result recomputed from the evidence) and the merge is validated like a single run. A single 12,500-word call (CA 2026 Prop 40) failed 13 times on skipped restatements and loose quotes.

**No outside names (2026-10-27):** every capitalized name a model writes must appear in the measure text (or be an ordinary word; legal words missing from the dictionary are listed in `prompts/allowed-words.txt`). This catches names from training memory, e.g. the first Prop 41 run called Article XIII B by its sponsor's nickname. Names that are in the official text (a findings section naming officials) are shown, because the text is the source.

**Exact prompts:** a run counts only if its system prompt, user template, and schema are byte-identical to the current files for its version, so drafts never mix on a page.

**Prompt hygiene:**
- Concern list order is randomized per run.
- Blocked vocabulary in outputs: party names, ideology labels, and loaded adjectives ("radical", "extreme", "common-sense", "dangerous", "progress", "freedom" used as a slogan). An output containing them is rejected and rerun.
- The model is told to describe mechanisms, not motives ("this clause does X", never "this is intended to").

### 5.4 Multi-model

- **Models:** at least 4 vendors with different training pipelines, e.g. Anthropic (Claude), OpenAI (GPT), Google (Gemini), xAI (Grok), plus at least one open-weights model (e.g. Llama, Mistral, Qwen or DeepSeek). Exact model versions are pinned and recorded with each run.
- **Runs:** K runs per model (e.g. 3) to measure each model's own consistency.
- **Reconciliation:** compare concern by concern (result), and evidence by evidence (clause × concern × effect).
  - **Consensus:** a majority of models agree → shown as the finding.
  - **Split:** shown as "models disagree", with each position and its quoted reasoning. Splits are content, not noise.
  - **Outlier:** one model alone → kept in the run log and visible on the "how we got this" view.
- **Agreement is not neutrality.** The major models share much of their training data and post-training methods, so they can agree and all lean the same way. Consensus is a display fact, not evidence of fairness. The bias test suite (§5.5) is the gate.
- **No judge model** picks winners. A model may help *merge wording* of agreeing findings, and that output is checked against the source findings.

### 5.5 Bias test suite (gate before publish)

- **Mirror tests:** pairs of synthetic measures that are policy mirror images (raise/lower a tax, expand/restrict a right, add/remove a mandate). Evaluations must be symmetric. A model that's harsher on one direction gets flagged per concern.
- **Swap tests:** the same text with the topic swapped (e.g. a mandatory-disclosure rule applied to unions vs. corporations). The structural findings should match.
- **Language audit:** blocked vocabulary; tone balance between supports and conflicts explanations.
- **Corpus balance:** over all published measures, per concern, track the supports/conflicts ratio and each model's lean. Report this publicly.
- **Human panel:** reviewers from different perspectives rate a sample of evaluations for fairness. Disagreements feed back into the concern wording or the prompt.

### 5.6 Versioning and transparency

Every published evaluation records: source text hash, concern-list version, prompt version, model versions, run IDs, and reconciliation result. Changing the concern list or prompt triggers a full re-evaluation, and the old version stays viewable. A public methodology page explains all of this.

### 5.7 Run it yourself

We don't ask anyone to trust us. Each measure page has a **"Verify this"** panel that gives:

- **Download bundle** (one zip): source text + hash, current-law text, clause segmentation, concern list version, every prompt exactly as sent (system + user messages), JSON schema, model IDs and parameters, every raw model response, and the reconciliation output.
- **Copy-paste prompt:** the complete prompt for one model run, ready to paste into any AI chat, for people without technical setup.
- **CLI / script:** an open-source runner (`npx onlytradeoffs verify <measure-id>` or a Python equivalent) that rebuilds the prompts from the bundle, runs them against the user's own API keys, and diffs the results against ours.
- **Public repository** holding the methodology, prompts, concern lists (all versions), bias test suite, and the Phase 0 research archive, with full history.

Caveat we state up front: models aren't perfectly deterministic and vendors update them, so a rerun won't match word for word. That's why we publish K runs per model and compare *results* (concern × result, clause × concern × effect), not wording. A rerun that consistently disagrees with ours is a bug report we want.

The Phase 0 research archive does carry perspective labels, because it records where each concern came from. It lives in the methodology repository as an audit trail. It's never shown on measure pages and never sent to the evaluating models.

## 6. Website

- **Find my ballot:** enter an address → list of measures (state → county → city → district).
- **Measure page:**
  - **What the text touches:** a one-screen map, domain by domain, of every concern the text supports, conflicts with, or both (color + label; never ranked)
  - **By concern** (default view): one collapsed card per touched concern; open it for the axis, the mirror concern, and each piece of evidence (quote → clause, why, certainty, model agreement)
  - **By section of the text:** for each clause, its restatement and two columns, "Supports" and "Conflicts with", so the tradeoff inside one clause is visible at once
  - Models disagree (collapsed), text-quality flags, analysis (inference), full text with highlighted quotes, "How we got this", "Verify this"
  - **Who is for and against it:** committees, money raised, top funders, endorsers per side, with sources; visibly separate from the text analysis, never sent to a model (§6.2)
- **People and organizations:** one page per funder, committee, or endorser, with their record across every election on the site (side, role, amount, source). No labels, no inferred leanings.
- **Phase 2 tab:** "What others say" (party platforms, news), visibly separate from the text evaluation.
- No ads, no endorsements, no donation-driven placement. Funding sources disclosed.

### 6.1 Build pipeline (implemented 2026-10-26)

The site is **static and generated**, so every election is a rebuild and nothing runs on a server:

```
elections/<id>/election.yaml      measures, jurisdictions, pinned prompt + concern versions
   │  pipeline.py check           validate before spending on model runs
   │  pipeline.py run -- …        offline, resumable; one call per model; every attempt saved in runs/
   │  pipeline.py gate            every model used must have run the full bias suite
   │  pipeline.py build           reconcile → data.json, bundle.zip, prompt.txt, HTML → build/site/
   ▼
build/site/                        plain files; any static host (S3+CloudFront, GCS, Cloudflare Pages)
```

- **Pins:** an election names the prompt and concern-list versions it uses. Only runs with those versions are reconciled, so a later prompt change never mixes into an old election, and old elections stay rebuildable.
- **Pages:** home, election (grouped by jurisdiction), measure (see above), concerns (the full list, read-only), people and organizations (index + one page each), method, verify (do-it-yourself packs).
- **Palette:** teal for supports, amber for conflicts with, a split teal/amber dot for both. Every color is paired with a text label. Never red/blue (party colors) or red/green (good/bad).
- **Not built yet:** address lookup ("find my ballot"; needs a geocoder and district data), the Phase 2 "What others say" tab, and deployment.

### 6.1a Official sources (2026-10-27)

- The models read the measure's own text from the most primary source available, never the voter guide: for initiatives, the text as filed with the Attorney General (`oag.ca.gov/initiatives`); for legislative measures, the chaptered text on `leginfo.legislature.ca.gov`.
- The fetched file is archived unchanged in `elections/<id>/sources/`, fingerprinted (SHA-256), and published on the measure page next to the official link.
- `tools/import_measure.py` turns it into clauses by the measure's own numbering, and writes an import log of every change it made (layout, plus a small set of logged OCR fixes for scanned filings). `pipeline.py check` refuses a real measure without an archived source whose hash matches.
- AG filings are scans. `tools/ocr_vote.py` reads each page three ways (Tesseract 5, RapidOCR running the PaddleOCR models, and the PDF's own OCR layer) and keeps, word by word, what two agree on; when all three differ, the reading closest to the other two wins only if it clearly does. Subdivision labels misread as (1)/(I)/(0)/"G)" are corrected from the measure's own lettering. Raw readings are kept in `sources/ocr/`, and every override is in the import log. On the 2026 CA filings this fixed every error found in the layer-only text ("Defmitions", "talces", "G)" for "(j)", a missed "SEC. 5"), with about a dozen logged unresolved spots, mostly on cover pages.
- The page still says the scan is the authority.

### 6.2 Campaign data (implemented 2026-10-27)

- `data/entities.yaml`: every person, organization, and committee, with a stable ID so a record follows them across elections.
- `elections/<id>/campaign.yaml`: per measure, committees (side, amount raised), contributions (from → committee, amount), endorsements (side). Every row cites a source with URL and fetch date (official filing databases first).
- `tools/campaign.py check` (also run by `pipeline.py check` and before every build): unknown entities, unknown sources, contributions to a committee not on that measure, missing URLs for real data.
- **Never sent to a model.** The prompt builder reads only the measure file. The page says so next to the data.
- **Privacy:** an individual who isn't a public official is named only at or above `individual_min_usd` (default $5,000) per measure, or if they endorsed publicly. Smaller gifts are shown as a count and a total.
- **No labels:** names come from filings, and nobody is described by what they fund. An entity whose official name contains a blocked term (e.g. a party committee) fails the check until there's a rule for it (open question).
- **Not built yet:** importers for state filing data (e.g. Cal-Access, other states' bulk CSVs), entity matching across filings (same donor, different spellings).

## 7. Data model (sketch)

```
Jurisdiction(id, type: state|county|city|district, parent_id, name, fips)
Election(id, jurisdiction_id, date)
Measure(id, election_id, code, ballot_label, kind: initiative|referendum|amendment|bond|charter|advisory)
SourceDoc(id, measure_id, role: measure_text|current_law, url, sha256, fetched_at, blob_ref)
Clause(id, measure_id, path, text, span_start, span_end)
Concern(id, version, name, description, domain)
EvalRun(id, measure_id, model, model_version, prompt_version, concern_version, run_index, raw_output, created_at)
ConcernResult(id, eval_run_id, concern_id, result: supports|conflicts|both|none)
Evidence(id, concern_result_id, clause_id, effect: supports|conflicts, quote, why, certainty)
ReconciledConcern(id, measure_id, concern_id, status: consensus|split|outlier|below-threshold, result, positions_json, evidence_json)
Entity(id, kind: organization|person|committee, name)
Committee(measure_id, entity_id, side: support|oppose, raised_usd, source)
Contribution(measure_id, from_entity_id, to_committee_id, amount_usd, source)
Endorsement(measure_id, entity_id, side, source)
Flag(id, measure_id, clause_id, kind, note)
```

## 8. Open questions

1. **Stack:** Next.js on Vercel + Supabase (matches existing projects) vs. a static site generated from the eval DB (cheaper, harder to tamper with, easy to archive). Leaning static for the public site with a private pipeline.
2. **Local measure coverage:** thousands of local jurisdictions publish text inconsistently (scanned PDFs, clerk sites). This needs OCR, per-county scrapers, or crowdsourced uploads with hash verification.
3. **Human panel:** who, how many, how paid, how chosen so the panel itself is balanced.
4. **Concern-list size:** too few and real tradeoffs are hidden; too many and the page becomes unreadable. Now 83 (revision 4). The page shows only touched concerns, grouped by domain and collapsed, so list size mostly costs model tokens, not reader attention.
8. **Party and ideology names in campaign data:** party committees and some advocacy groups have a party or ideology word in their legal name. Showing the name breaks "no tribes anywhere"; hiding or renaming it misreports a filing. Undecided; `campaign.py check` blocks such entities until decided.
5. **Bond measures and tax renewals:** mostly money concerns; may need a lighter template.
6. **Legal review:** election-law and defamation exposure for statements about measures (low, given text-only and no recommendations, but check).
7. **Cost:** N models × K runs × passes × measures. Estimate after the pilot.

## 9. Next steps

1. ~~Phase 0 research (§4.2 step 1): sourced concern lists per perspective → `research/`.~~ v1 draft done 2026-10-26; see `research/README.md` for what remains before freezing.
2. Freeze the list and convert it to `concerns/v1.yaml` (the machine-readable input the models receive). **Conversion done; freeze pending.** `tools/build_concerns.py` generates `concerns/v1-draft.yaml` from `research/concerns-v1.md` (which stays the source of truth), drops trails, statuses and logs, checks that mirrors are reciprocal, and refuses to build if any perspective ID would reach a model. The freeze still waits on the checklist in `research/README.md`.
3. ~~Write the eval prompt and JSON schema → `prompts/`, `schema/`.~~ Draft v0 done 2026-10-26:
   - `prompts/system-v0.md`, `prompts/user-v0.md`, `prompts/blocked-terms.txt`
   - `schema/eval-output-v0.schema.json` (every property required, nulls for optional values, so it works with each vendor's strict structured-output mode)
   - `tools/build_prompt.py`: renders the exact messages per run, shuffles concern order with a **recorded seed**, and writes a manifest of versions and SHA-256 hashes (§5.7)
   - `tools/validate_output.py`: schema, verbatim quotes, `moves` only on ⇄ concerns, mirror pairs present and opposite, summary items cite findings, blocked terms outside quotes
   - `tests/fixtures/synthetic-storage.*`: a synthetic measure with a valid output and one with 8 planted defects (all rejected)
   - Not yet run against any real model.
   - **v1 (2026-10-27):** `prompts/system-v1.md`, `schema/eval-output-v1.schema.json`: one entry per concern with supports / conflicts / both / none and its evidence; no Yes/No summary. Validator checks every concern is answered once and that each result matches its evidence. `tests/test_validate.py` plants 13 defects (all caught). v0 runs are archived in `runs/_superseded/prompt-v0/`.
4. ~~Build the mirror/swap test set → `tests/bias/`.~~ v0 done 2026-10-26:
   - `tests/bias/pairs.yaml`: 10 mirror pairs and 5 swap pairs, all synthetic, each with current law. Mirror pairs expect opposite effects on every concern unless listed under `same` (e.g. both directions of a detainer rule are state overrides of county choice); swap pairs expect identical effects unless listed under `may_differ`.
   - `tools/bias_check.py expand` writes 30 measure files. Their measure IDs are opaque hashes, so a model can't tell it's being tested or which side of a pair it's reading.
   - `tools/bias_check.py compare` reports asymmetries per seed and stable (majority of runs), recall misses on `required` concerns, and a per-concern supports/conflicts tilt table per model.
   - `tools/run_eval.py` (one measure × one model × K seeds) and `tools/run_batch.py` (parallel). Every attempt is saved, rejected ones included.
4a. Do-it-yourself packs (§5.7): `tools/build_portable.py` → `dist/portable/` with a Claude skill, Gemini Gem and custom GPT instructions plus knowledge files, and one self-contained paste prompt for any other chat (Grok, open-weights UIs). All are generated from the same prompt, concern list, and schema files as the official runs. `build_prompt.py --paste` gives the per-run prompt for the "Verify this" panel.
4b. Model access: Gemini via Vertex AI (working). Claude and open-weights models via Bedrock. Grok via the xAI API (OpenAI-compatible; `run_eval.py --provider openai --base-url https://api.x.ai/v1`). GPT via the OpenAI API. Consumer chat apps (Gems, GPTs, Grok's app) are for public self-verification only, never for official runs, because they add hidden instructions and don't pin model versions.
5. Pilot on ~10 statewide 2026 measures across several states and both directions of policy.

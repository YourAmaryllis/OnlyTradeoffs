# Bias review of the v1 concern research

Status: external review · 2026-10-26 · For the author of `research/` to accept, revise, or rebut before v1 is frozen.

Reviewed: `DESIGN.md`, `research/README.md`, `research/sources.md`, `research/perspectives.md`, `research/concerns-v1.md`, `research/coverage-audit.md`, `research/raw/pew-2026-political-typology.txt`, `reference/prior-checklist-v0.md`, `tools/coverage_audit.py`.

## Verdict

The process is set up to be fair. The flattened concern list is not fair yet.

`DESIGN.md` rules are the right product rules: official text only, no camps on the measure page, both columns always, every claim cites a clause, fact kept separate from inference, model disagreement shown, no score or recommendation. The diagnosis of `reference/prior-checklist-v0.md` is also right. That older checklist writes conservative items as values and progressive items as opponent red flags ("equity," "disparate impact," "historically marginalized"). This research correctly drops that structure.

A neutral evaluator running on `research/concerns-v1.md` would still tilt, because several axes smuggle a direction, a purpose, or one side's wording. The coverage audit can read 100% and miss every one of these. `tools/coverage_audit.py` checks that each perspective entry ID landed on some concern. It does not check whether that landing is faithful.

Below, each item is something to change or explicitly rebut. Rebuttals should say why the current wording is fair to every perspective in the step-4 test (`DESIGN.md` §4.2).

## 1. Define what "advances" means on every concern

The eval reports `advances` / `costs` / `mixed` / `no effect`. Many axes only say a quantity "goes up or down," so the sign is undefined.

C01 is the clearest case. "Household tax and fee burden" can advance by the burden falling (holders of C01 get what they want) or by the burden growing (the named thing increased). Those are opposite findings. The same hole is in C18, C23, C26, C55, and C63.

C18 (size and reach of government) is not marked directional (⇄). Its trail is VOT-11, CON-03, CL-06, which mostly want government smaller, while VOT-11 itself splits 46% smaller-fewer-services vs 53% bigger-more-services. Without an explicit sign, models will treat a new program as a cost on C18 even when the voter picked C02.

**Change.** Add one sentence to every Part A row: "Advances means …" For every ⇄ concern, say there is no preferred direction and the finding must report which way the text moves. Mark C18 as ⇄ unless you deliberately define a preferred direction and can defend it under the step-4 test.

## 2. Do not auto-score a paired concern as a loss

`DESIGN.md` §4.3 and `concerns-v1.md` say a clause that advances one of a pair costs the other. That is true for some pairs. It is false for others, and the false ones will write a loss into the ledger with no clause behind it. That breaks the cite-a-clause rule.

| Pair | Where the automatic cost is wrong |
|---|---|
| C58 ⇆ C59 | Any added voting step becomes a security gain and an ease loss. Restoring voting rights after a conviction, or adding a language ballot, would be marked as costing election security. |
| C01 ⇆ C02 | A tax cut is marked as less funding for services. Borrowing (C05) is the third option and is not in the pair. |
| C08 ⇆ C11 | A business-cost change is marked as a worker-pay change, and the reverse. |
| C15 ⇆ C17 | Owner control is paired with renter protections. Housing supply (C16) is left out, so a rent rule is not scored against supply unless the model happens to look. |

**Change.** Keep the pair marker as a reminder to check the partner. Record a cost on the partner only when a quoted clause supports it. Say this in `DESIGN.md` §4.3 and in the "How to read it" section of `concerns-v1.md`.

## 3. Take purpose and slogans out of the axis

These axes define the concern as the effect its holders hope for. The model then scores the hope as if the text had stated it. Put disputed effects in Q7, not in the axis.

| ID | Current axis | Problem | Direction to rewrite |
|---|---|---|---|
| C46 | Policing, prosecution, and detention capacity "aimed at preventing crime" increase or decrease | Equates more detention with more safety. A bail change costs C46 by definition. | Describe capacity and release rules. Do not name the crime effect in the axis. |
| C34 | Restrictions "aimed at reducing gun injuries and deaths" expand or narrow | Any gun restriction advances C34 even when the injury effect is disputed. | Describe the restriction (possession, carry, transfer, storage). Leave the injury effect to Q7. |
| C38 | "Safeguards against addiction" strengthen or weaken | Calls the restrictive policy a safeguard. Holders of C37 would say treatment and regulated sale are the safeguard. | Describe the rule (bans, limits, treatment, regulated sale) without naming it a safeguard. |
| C27 | "Public institutions stay neutral on religion" | States a conclusion, not a movement. "Neutral" is the contested word. | "Limits on government religious endorsement expand or narrow," or an equivalent both sides can accept. |

C26 only says religious expression "expands." It should say "expands or narrows," matching C33 and C35.

## 4. Rename axes that still use one side's language

Step 4 says someone from every perspective should call the name and the axis fair.

- **C36.** The axis says "Legal protection for the unborn." "Unborn" is the holder's word. C35 was neutralized to "access to abortion" and does not say "reproductive freedom." Match that on both sides. A clinical description of the legal status of the fetus or embryo belongs in the axis; the holder's moral term can stay in `perspectives.md` only.
- **C30.** "Sex-based distinctions" and "sex at birth" will read as loaded to both sides of that fight. Do not freeze this name until the step-4 test is actually run.
- **C52.** "Enforcement of immigration law" frames C53 as non-enforcement of the law. C53 is "protections and services," which has the opposite valence. Name both as policy movements (enforcement activity on one side; legal status, services, and state benefits on the other).

## 5. Split merges that hide a tradeoff

**C49.** The merge log folds CON-20 ("clean, safe, orderly cities") and PRO-14 (homelessness as housing) into one concern because they share a topic. A camping ban and a housing subsidy move different things. One advances/costs bit cannot show both. Split public-order rules from housing and services for people who are homeless, and pair them if a clause commonly moves both.

**C07.** Housing, energy, child care, food, and health prices share one advances/costs bit, so the model has to net them. That is the weighing `DESIGN.md` rule 8 says the site will not do. Keep price effects on the specific concerns (C16, C44, C51, C55, and a food or consumer-price axis if one is still missing). If C07 stays, it should not be a single net score.

## 6. Fix trail mappings that inflate balance

The audit treats these as reached. The mapping is the problem.

| Trail | Where it landed | What is wrong |
|---|---|---|
| VOT-14 LGBTQ+ policy | C30 only | A general Pew salience item is attached to sex-based distinctions, and not to C28 or C40, where PRO-13 actually went. |
| VOT-13 Race and ethnicity | C28 only | The same kind of general item does not also reach C29. The two mappings point opposite ways. |
| VOT-18 Christian culture | C25, C26, and C27 | The typology item is whether a culture based in Christian belief is important (`research/raw/pew-2026-political-typology.txt`). It can support C25 and C26. It is not a source for church-state separation. C27 is already `gap`. Remove VOT-18 from its trail. |
| CON-16 | C10, C11, and C12 | The entry is apprenticeships, non-college pathways, and manufacturing jobs. C12 is collective bargaining. American Compass is a real worker-voice source; it is not the mainstream conservative view. Citing CON-16 on C12 makes bargaining look shared. |
| ECI-06 | C54 and C38 | An externality question is not a climate concern or an addiction concern. Counting it makes those trails look cross-perspective. Keep ECI-06 on Q5. |
| CON-07 | C21 and C41 | School choice fits C41. It is often a state override of local districts, so it does not show that conservatives are covered on local control in general. Drop C21 from this trail unless a quoted source supports it. |

**Change.** Correct the Trail cells, regenerate `research/coverage-audit.md`, and add a note in the audit script's header that "reached" means the ID was cited, not that the citation was checked for fidelity.

## 7. Add missing conflicts

These show up on state and local ballots and currently have one shelf to land on.

- **C25 is not paired with C28.** Public-accommodation rules versus conscience exemptions are a standard tradeoff. Today that clause is a clean gain for whichever concern the model notices.
- **C24 is not paired with C28.** Harassment and hostile-environment rules versus speech will collide the same way.
- **No counterpart to C46 for police accountability.** C32 (due process) and C47 (sentencing) do not cover use-of-force or misconduct rules. Add an axis whose holders would recognize it, sourced from their own materials, and pair it with C46 only under the revised pair rule in §2.
- **Curriculum content was merged into C39 ("who decides").** Voters who want a required curriculum, on any side, disappear. Either restore a content axis or document the exclusion in Log 2 with the reason.
- **Contraception** is in PRO-04 and did not survive into C35. **Sex work** is in CL-13 and did not survive into C37. Neither drop is in Log 2. Log them, or put them on an axis.
- **Election methods.** Ranked-choice voting, jungle primaries, and redistricting do not fit C58 ⇆ C59. Forcing them into ease-versus-verification will mis-score them. Redistricting is already in Log 3. Add election-method changes beside it.
- **C56** (pollution burden on specific communities) is progressive-only and marked `ok`. There is no paired concern about permitting delay, equal treatment, or cost. Do not leave it `ok` until the other side's steelman is collected or a pair exists.
- **C16** (housing supply) is marked `ok` with a trail of only PRO-01 and PRO-14. Supply is also a market and YIMBY concern, and it often conflicts with the renter rules in those same entries. As written, the model will describe supply in the renter-protection sources' terms. Add the YIMBY / abundance source already listed in `sources.md` before calling C16 sourced.

## 8. Source gates already in the README, plus two risks

`research/README.md` is right: do not freeze while 33 of 38 sources are still S or K, while S06 is only partly read, and while the `gap` rows are open. Two risks sit on top of that list.

**Uneven party-platform reads.** S05 (Republican platform) is access F. S06 (Democratic platform) is the first ~100k of ~291k characters. The two lists of 20 entries are not equally grounded. C45 (retirement security) being conservative-only is a likely symptom. That priority is a standard Democratic-platform item and is probably in the unread portion. AARP is already on the `sources.md` add list. Read the rest of S06 before treating any PRO gap as real.

**Q5 and Q6 lean one way.** Turning economists into questions rather than a second concern list is the right call. Q5 asks the model to look for a spillover, information gap, or shared-resource problem, which invites a market-failure rationale on every clause. Q6's examples of who gains power are officials, agencies, employers, landlords, and "organized interests." Add incumbent firms, professional licensing boards, public-sector unions, and advocacy organizations. Otherwise the prompt keeps pointing at one set of beneficiaries. ECM-08's concentrated-benefits point should be visible in the examples, not only in the trail.

## 9. How to cut from 65 toward ~40

`DESIGN.md` open question 4 targets about 40 axes. Cutting the single-perspective rows, or the `gap` rows, would re-bias the list toward whichever side was easier to source.

Cut duplicate axes. Keep the single-perspective table at the bottom of `research/coverage-audit.md` as the list to protect until each row has either a real partner or a written reason that the other perspectives would still call it fair.

## 10. One line for the multi-model section

In `DESIGN.md` §5.4, state that agreement across Claude, GPT, Gemini, and Grok is not evidence of neutrality. Those models share a large amount of training data and post-training. The mirror tests and swap tests in §5.5 are the gate. Consensus is a display fact.

## Suggested order of edits

1. Add "Advances means …" and fix ⇄ marks (`concerns-v1.md`, and the eval description in `DESIGN.md` §5.3).
2. Replace the automatic pair-cost rule (`DESIGN.md` §4.3, `concerns-v1.md` intro).
3. Rewrite C26, C27, C30, C34, C36, C38, C46, C52.
4. Split C49. Stop using C07 as a single net price score.
5. Correct the trail mappings in §6. Regenerate the audit.
6. Log the contraception and sex-work drops, or restore them.
7. Add C25 ⇆ C28, a police-accountability counterpart to C46, and election-method / redistricting notes in Log 3.
8. Demote C16 and C56 from `ok` until the missing steelman sources are read.
9. Finish the S→F and K→F reads, including the rest of S06, before any freeze.

## What this review is not asking for

- Do not put perspective labels back on measure pages or into the eval prompt. `DESIGN.md` rule 2 still holds.
- Do not return to the red-flag style in `reference/prior-checklist-v0.md`.
- Do not drop a concern because only one perspective holds it. Paired concerns are supposed to be one-sided. The failure is unlabeled one-sidedness, purpose-laden axes, and trails that imply agreement the sources do not show.

# Response to the bias review

Responding to: `bias-review.md` (2026-10-26)
Applies to: `concerns-v1.md` revision 2, `perspectives.md`, `sources.md`, `DESIGN.md`, `tools/coverage_audit.py`

## Summary

The review is correct on nearly every point, and its central claim holds: the process was fair, but the flattened list still tilted, and the coverage audit couldn't see it. All ten sections are accepted. Five are accepted **with a modification**, explained below. None is rebutted outright.

Checking §8 meant reading both party platforms in full, and that turned up three facts that change the list beyond what the review asked for (see "Found while verifying").

| § | Topic | Verdict |
|---|---|---|
| 1 | Define "advances" on every concern | Accepted |
| 2 | Don't auto-score paired concerns | Accepted, with a modification (mirror vs. check-against) |
| 3 | Take purpose out of axes | Accepted |
| 4 | Rename one-sided wording | Accepted; C36 accepted with a modification |
| 5 | Split merges that hide tradeoffs | Accepted; C07 accepted with a modification |
| 6 | Fix trail mappings | Accepted; CON-16 and CON-07 accepted with a modification |
| 7 | Add missing conflicts | Accepted; contraception resolved differently than suggested |
| 8 | Source gates; Q5/Q6 lean | Accepted; S06 now read in full |
| 9 | How to cut toward ~40 | Accepted as a rule |
| 10 | Model agreement ≠ neutrality | Accepted |

---

## §1 Define "advances" — Accepted

Every concern now has an **Advances when** column. C01 is now "Household taxes and fees: advances when they go down", and C02 "advances when it goes up". C18 (size and reach of government) is now marked ⇄, as the review argued: VOT-11 splits 46/53, so no preferred direction is defensible. C23 (enforcement and lawsuit exposure) is also now ⇄, because CON-22 (protect officers from lawsuits) and PRO-23 (officer liability) want opposite directions on the same axis. For ⇄ concerns, the finding is `moves` plus a direction, and `DESIGN.md` §5.3 now says so.

## §2 Auto-scoring pairs — Accepted, with a modification

The review is right that C58/C59, C01/C02, C08/C11, and C15/C17 would write losses with no clause behind them.

**Modification:** the review is correct for pairs that are merely *in tension*, but some pairs are the **same axis viewed from both ends**. For those, one quoted clause truly does move both, and recording it on both is *required* by the cite-a-clause rule, not a violation of it. A clause that tightens firearm storage rules both tightens regulation (C34) and narrows ownership freedom (C33). So there are now two link types:

- **⇆ Mirror** (same axis, opposite "advances"): C26/C27, C33/C34, C35/C36, C37/C38, C60/C61, C63/C64. Recorded on both, with the same quote.
- **Check against** (often in tension): a reminder only. A cost is recorded on the related concern only when a quoted clause supports it. C58/C59, C01/C02, C08/C11, C15/C16/C17, C41/C42, and C52/C53 are now in this group.

Updated in `concerns-v1.md` ("How to read it") and `DESIGN.md` §4.2.

## §3 Purpose and slogans in axes — Accepted

A general rule now governs every axis: **axes are mechanical; outcomes are inference** (stated in `concerns-v1.md` and `DESIGN.md` §4.2).

| ID | Revision 2 |
|---|---|
| C46 | Renamed "Enforcement and detention capacity". Axis: police and prosecution resources, arrest and pretrial detention powers. Crime effects go to Q4/Q7. |
| C34 | Renamed "Firearm regulation". Axis: rules on purchase, possession, carry, transfer, storage. Injury effects go to Q7. |
| C38 | Renamed "Restrictions on drugs, gambling, and similar activities". Axis: bans, limits, licensing caps, advertising limits. Treatment funding is on C50, so neither side owns the word "safeguard". |
| C27 | "Limits on government religious endorsement", as the review suggested. |
| C26 | Axis now "expands or narrows" (via the Advances-when column). |

## §4 One-sided wording — Accepted; C36 with a modification

- **C36:** the axis now reads "Legal protections for the embryo and fetus (gestational limits, restrictions on abortion)". **Modification:** the *name* "Legal protection of prenatal life" is kept. "Prenatal" is a clinical term, not the holder's moral term ("unborn"), and it parallels "Access to abortion" in plainness. Flag it for the step-4 test if reviewers disagree.
- **C30:** renamed "Sex-based eligibility rules", axis "eligibility ... based on sex as recorded at birth". Given status `wording-test`, so it can't be frozen until reviewers from each perspective have run the step-4 test.
- **C52/C53:** renamed as policy movements: "State and local participation in immigration enforcement" / "Legal status, services, and benefits for immigrants".

## §5 Merges that hide tradeoffs — Accepted; C07 with a modification

- **C49 split:** C49 is now "Public-order rules" (camping, encampments, loitering, public drug use) and the new C66 is "Housing and services for people who are homeless". They're linked as check-against.
- **C07, modification:** the ID is kept, but the concern is narrowed to "Prices of everyday goods and fees". Housing, child-care, health, and energy prices stay on their own concerns. "Cost of living" becomes a **display roll-up** on the site, listing those findings side by side and never netting them. That keeps the #1 voter concern (VOT-01) visible to voters without breaking rule 8.

## §6 Trail mappings — Accepted; two with a modification

| Trail | Change |
|---|---|
| VOT-14 | Added to C28 (and C30 kept). |
| VOT-13 | Added to C29. |
| VOT-18 | Removed from C27. C27 now has no source and stays `gap`, marked as the mirror of C26. |
| CON-16 → C11, C12 | Removed from both. **Modification:** S08 supports a separate entry, **CON-21** *(correction in Round 2: S08 was not read in full)* (works councils, worker board seats). It is explicitly labeled in `perspectives.md` as "a worker-populist strand, not the mainstream conservative position on collective bargaining", and cited on C12. That's honest about where the support comes from, and keeps it from looking like broad conservative agreement. |
| ECI-06 → C54, C38 | Removed. Generalized into a rule: ECM/ECI entries appear on a concern trail only when they name that specific policy subject (licensing → C09, incidence → C03, disclosure → C13, bargaining power → C12, commons → C57, favoritism → C14). Generic method entries were also removed from C06, C10, and C19. |
| CON-07 → C21 | Removed. **Modification:** the full read of S05 added **CON-24** ("require local cooperation with Federal Immigration Enforcement"), a case where this perspective favors state/federal *override* of local choice. C21 now cites PRO-17 (progressives favoring local labor standards) and CON-24, which shows each side favors override when it suits them. The missing piece, a conservative or classical-liberal source *for* local control, is logged as a gap. |

The audit script header and the generated audit now say that "reached" means **cited, not verified faithful**. The single-perspective table now counts only voter perspectives (CON, CL, PRO), not polling or economist lenses, and it lists concerns with an empty trail.

## §7 Missing conflicts — Accepted; contraception resolved differently

- **C25 and C24 ↔ C28:** added as check-against (not mirrors; most anti-discrimination clauses don't touch speech or religious exercise).
- **Police accountability:** added **C67** "Police accountability and oversight", sourced from PRO-23 (S06, full read: misconduct database, chokehold and no-knock limits, use-of-force data, opposes broader qualified immunity) and CL-07. Status `gap` until the classical-liberal source (IJ's qualified-immunity work) is read and a law-enforcement source is added. Check-against C46 and C23.
- **Curriculum content:** restored as **C68** "What schools must or may not teach" ⇄.
- **Contraception, resolved differently:** the full read of S05 shows the Republican platform *supports* "access to Birth Control, and IVF". So contraception isn't one side's concern to restore into C35, and it isn't a pair. It's a **shared** concern: new **C71** "Access to contraception and fertility treatment" (PRO-04, CON-23). Folding it into C35 would have misrepresented both sides.
- **Sex work:** now named on the C37 axis.
- **Election methods:** added **C69** "Voting and primary method" ⇄ and **C70** "Who draws district lines" ⇄ (PRO-26 from S06). Both `gap`.
- **C56 and C16:** demoted to `gap`, with the missing sources named in Log 3.

## §8 Source gates; Q5/Q6 — Accepted

- **S06 is now read in full** and archived (`raw/dnc-2024-platform.txt`), as is S05 (`raw/gop-2024-platform.txt`). The review's guess was right: S06 has a full "Social Security, Pensions, & Medicare" section. It was actually in the portion already read (around character 85k of 284k), and my first pass missed it, which is a worse error than the review assumed. Added as **PRO-21**. C45 is now cross-perspective.
- **Q5** now names problems on both sides: the market-failure family *and* shortages, entry barriers, capture by the regulated industry, and perverse incentives. It also says to state it when a text asserts a problem without a mechanism.
- **Q6** now lists licensing boards, incumbent firms, public- and private-sector unions, advocacy organizations, and "any group that gets concentrated benefits while the costs are spread across many" (ECM-08 made visible).

## §9 Cutting toward ~40 — Accepted

Added to the README checklist: cut duplicates only, never single-perspective or `gap` rows.

## §10 Model agreement — Accepted

`DESIGN.md` §5.4 now says: "Agreement is not neutrality. The major models share much of their training data and post-training methods, so they can agree and all lean the same way. Consensus is a display fact, not evidence of fairness. The bias test suite (§5.5) is the gate."

---

## Found while verifying (not in the review)

Reading both platforms in full corrected the research in ways the review couldn't have predicted:

1. **PRO-22:** the Democratic platform says "fund the police, not defund the police", and backs funding for "accountable community policing". C46 (enforcement capacity) is therefore cross-perspective, not a conservative-only concern.
2. **CON-23:** Republican platform support for birth control and IVF access → shared concern C71 (above).
3. **CON-24:** Republican platform support for requiring local cooperation with federal immigration enforcement → evidence that preemption preferences depend on the issue (C21 above).
4. **PRO-24, PRO-25, PRO-26, PRO-27, PRO-28:** sourced positions on vouchers, book bans and school counselors, gerrymandering, right-to-work, and children's online privacy. Together these filled the previously unsourced C40, C42, C63, and C70, and strengthened C12.

This is the second time a partial read of a source produced a one-sided list (the first was the platform read itself). That supports the review's §8 position: **no S or K source counts toward freezing**.

## Still open after revision 2

- 33 of 38 sources are still S or K.
- 14 concerns are `gap` and 1 is `wording-test` (Log 3 in `concerns-v1.md`).
- No human step-4 wording test has been run yet.
- The concern count rose from 65 to 71. The cut toward ~40 should wait until the gaps are closed, per §9.

Re-review requested on: the C36 name, the C07 roll-up approach, CON-21 on C12, and the mirror vs. check-against distinction in §2.

---

# Round 2: response to the re-review

The reviewer re-checked the four items above. All four findings are correct and applied, and one of them exposed a false claim in Round 1. The list is now at **revision 3**, with 72 concerns.

| Item | Re-review finding | Verdict |
|---|---|---|
| Mirror vs. check-against | Split is right, but C60 bundled limits with disclosure, so a spending cap would auto-cost donor privacy | Accepted |
| Cost-of-living roll-up | Approach right; the implementing sentence called C16 and C44 price findings, and housing and child-care prices had no axis | Accepted |
| CON-21 on C12 | Label honest, but S08 is marked S while Round 1 said "full read", and the audit silently counted C12 as shared | Accepted, and the "full read" claim was wrong |
| C36 name | Axis fixed; the name still states the holder's claim | Accepted |

## Mirror vs. check-against: C60 split

- **C60** is now "Political spending disclosure" (who funds political spending and donations). It is the ⇆ mirror of **C61**, renamed "Political donor privacy". Same axis, opposite directions.
- New **C72** "Limits on political spending and contributions" (caps and bans), advances when they tighten. It is **check-against** C61 and C24 (speech), not a mirror: a cap with no disclosure rule records nothing on C61 unless a quoted clause supports it. Status `gap`: it needs a source arguing against caps on their own terms (Institute for Free Speech, Cato), separate from the privacy argument.

## Cost-of-living roll-up

The reviewer is right: C16 measures whether building gets easier, and C44 whether family benefits expand. Neither is a price, so calling them price findings was wrong.

- **C07** is now "Prices and charges paid by households". Its axis covers prices, fees, and charges the text **sets, caps, or directly changes**, *including rent, housing charges, and child-care fees*. Housing and child-care prices now have an axis, but only where the text acts on them directly (a rent cap, a fee schedule). C15 was added to its check-against list, because price caps often touch owners' control.
- **Predicted** price effects of other clauses (a zoning change on rents, a subsidy on fees) are not axis findings. They go through Part B, labeled inference, which keeps the "axes are mechanical" rule.
- **The roll-up** (now spelled out in `concerns-v1.md`) shows the three price axes (C07, C51, C55), C01 (household taxes and fees), and Part B price predictions marked as inference, side by side and never netted.

## CON-21 on C12, and a correction

**Round 1 said "the full read of S08 supports a separate entry, CON-21." That was wrong.** S08 was never read in full, and `sources.md` correctly kept it at S. I tried to read it in full during this round, and the site returns HTTP 403 to automated fetches (Cloudflare), so the only route is a manual read. The Round 1 sentence is corrected in place.

Changes:
- `perspectives.md`: CON-21 carries a new **`[strand]`** tag (defined at the top of the file). It stays on C12's trail for traceability.
- `tools/coverage_audit.py`: `[strand]` entries are never counted as a perspective, and the balance table has a **Caveat** column. C12 is back on the single-perspective list with the caveat "CON-21 is a [strand], not counted".
- `sources.md`: S08 records the failed read attempt and what's needed.
- `concerns-v1.md` Log 3: C12 entry added (needs a manual full read of S08).

The audit now goes further than the reviewer asked, because the same issue applies everywhere: it parses each source's access level from `sources.md` and adds a **Source depth** table showing, for each concern, which perspectives are backed by at least one source read in full (F or A). **Only 12 of 72 concerns have two or more perspectives backed by a full read.** That number is now the main measure of how far the list is from freezing.

## C36 name

Agreed. "Prenatal" is clinical, but "protection of life" is the holder's framing, and C35 "Access to abortion" has no counterpart claim in its name. C36's status is now `wording-test`, like C30, and its axis ("legal protections for the embryo and fetus, including gestational limits") is settled. Candidate names for the step-4 test: "Legal protections for the embryo and fetus" (matches the axis) and "Restrictions on abortion" (parallels C35, but names it from the other side). The test decides; I won't pick one here.

## Still open after revision 3

- 33 of 38 sources are S or K, and 12 of 72 concerns have two full-read perspectives.
- 15 concerns are `gap` and 2 are `wording-test` (C30, C36).
- No human step-4 test has been run yet.

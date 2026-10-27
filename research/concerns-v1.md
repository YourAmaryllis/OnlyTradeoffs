# Concern List v1 (draft, revision 2): neutral, label-free

Built from `perspectives.md` using steps 2–4 of DESIGN.md §4.2: merge, strip labels, turn each concern into an axis, and phrase it so every perspective would call the wording fair.

**Revision 2 (2026-10-26)** applies `bias-review.md`. What changed and why, item by item, is in `bias-review-response.md`. Concern IDs are stable: nothing was renumbered, and new concerns take new IDs (C66–C71).

**Revision 3 (2026-10-26)** applies the reviewer's re-review (`bias-review-response.md`, Round 2): C60 split into disclosure (C60, mirror of C61) and limits (new C72, check-against); C07 axis and the cost-of-living roll-up corrected; C36 name moved to `wording-test`; CON-21 no longer counts as a second perspective on C12.

**Revision 4 (2026-10-26)** follows the owner's decision that every concern gets one of four results (supports, conflicts, both, none) and that the site never frames a vote as gains and losses. The twelve directional (⇄) concerns could not take that form, so each now has one "advances when" direction. Nine became mirror pairs with a new concern (C73, C75–C78, C81–C83); C06, C43 and C68 gained a related, non-mirror concern (C74, C79, C80); C57 now covers use of resources, with protection already on C54. C18 also gets the mechanical axis that the first bias run asked for (`tests/bias/FINDINGS.md` #1–2). All 23 touched concerns are `wording-test` until reviewed.

**This file is the input the evaluating models will receive** (Part A + Part B + Part C, minus the "Trail" and "Status" columns and the logs). Those columns and the logs exist for auditing only.

## How to read it

- **Axis:** what the text can change, described **mechanically**. An axis never names the outcome its supporters expect ("reduces crime", "prevents addiction"). Predicted outcomes go in the Part B answers, labeled inference, and contested ones are flagged under Q7.
- **Advances when:** the direction in which the text **supports** the concern. Text that moves the axis the other way **conflicts with** it. For each concern, a model reports one of four results: `supports`, `conflicts`, `both` (different clauses, or one clause, push each way), or `none`. Every concern has exactly one such direction. (Through revision 3, twelve concerns were "directional", with no preferred direction; revision 4 split them, see Log 1.)
- **⇆ Mirror:** two concerns on **the same axis** with opposite "advances when" directions (e.g. C33 firearm ownership / C34 firearm regulation). The same quoted clause necessarily moves both, so a clause that supports one conflicts with its mirror, with the same quote. They exist as two concerns so neither side is the default: a reader sees the same clause from both sides.
- **Check against:** related concerns that a clause *often* moves in the opposite direction. This is **only a reminder** to look. A conflict is recorded on a related concern **only if a quoted clause shows it**, never automatically. (Example: restoring voting rights after a conviction supports C58 and has no effect on C59.)
- **Trail:** the perspective entries (`perspectives.md`) that produced this concern. Economist entries (ECM/ECI) appear on a trail only when they name that specific policy subject (e.g. licensing → C09). Generic method entries (incentives, externalities, second-order effects) live in Part B only.
- **Status:** `ok` = sourced. `gap` = included for coverage, but a steelman source for at least one side is missing (see Log 3). `wording-test` = name and axis must pass the step-4 fairness test with reviewers from each perspective before freezing.

**Cost of living** is the #1 voter concern (VOT-01), but prices move on several separate axes. It is therefore a **display roll-up** on the site, not a scored concern. It lists side by side, and never nets into one score:

- findings on the three axes that are prices: C07 (prices and charges set or directly changed by the text, including housing and child-care charges), C51 (healthcare prices), and C55 (energy prices);
- C01 findings (taxes and fees paid by households);
- Part B answers that predict a price effect from a clause on another axis (e.g. a zoning change on C16 and rents, a child-care subsidy on C44 and fees), shown with the **inference** label.

C16 (whether building housing gets easier) and C44 (whether family benefits expand) are not price axes, so their findings are not price findings. A price effect from them is a prediction and goes through Part B.

---

## Part A: Concerns (83)

### Money and taxes

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C01 | Household taxes and fees | Taxes and fees paid by individuals and families | They go down | C02, C05 | CON-02, VOT-17, CL-10 | ok |
| C02 | Funding for public services | Money available for public services | It goes up | C01, C05 | PRO-06, VOT-11 | ok |
| C03 | Larger tax share from higher incomes | Share of taxes paid at each income level | Higher incomes pay a larger share | ⇆ C73 | PRO-05, ECI-04, VOT-16 | wording-test |
| C73 | Equal tax rates across incomes | Share of taxes paid at each income level | Rates move toward the same rate for every income | ⇆ C03 | PRO-05, ECI-04, VOT-16 *(inherited from C03, rev. 4)* | wording-test |
| C04 | Simplicity and evenness of taxes | Complexity of tax rules; whether activities and industries are taxed alike | Rules get simpler and more even | C14 | CON-02, CL-11 | ok |
| C05 | Public debt and long-term obligations | Borrowing, bonds, pension and benefit liabilities | They go down | C02 | CL-10, CON-03 | ok |
| C06 | Budget flexibility | Spending locked in (earmarks, automatic increases, continuous appropriation) or limits locked in (caps, supermajority rules) | Fewer lock-ins of either kind | C74, C02, C22 | CON-03, CL-10, PRO-06 | wording-test |
| C74 | Guaranteed funding for set purposes | Spending earmarked, automatically increased, or continuously appropriated for a stated purpose | More spending is guaranteed | C06, C05 | CON-03, CL-10, PRO-06 *(inherited from C06, rev. 4)* | wording-test |
| C07 | Prices and charges paid by households | Prices, fees, and charges the text sets, caps, or directly changes, including rent, housing charges, child-care fees, food, goods, and utility services (healthcare prices are on C51, energy prices on C55; predicted price effects of other clauses go to Part B) | They go down | C08, C13, C15 | VOT-01, VOT-20, CON-01, PRO-01 | ok |

### Work and business

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C08 | Business costs and compliance burden | Costs, paperwork, and liability for businesses and nonprofits | They go down | C11, C13, C23 | CON-03, CON-18, CL-05 | ok |
| C09 | Freedom to start a business or enter a trade | Licenses, permits, and other entry requirements | They loosen | C13 | CL-03, ECM-09 | ok |
| C10 | Jobs and investment | Hiring and investment. **Always inference**; answer Q7 | They likely rise | C08, C11 | VOT-01, CON-16 | ok |
| C11 | Worker pay, benefits, and protections | Minimum pay, leave, scheduling, safety rules, wage enforcement | They strengthen | C08, C10 | PRO-02 | ok |
| C12 | Worker bargaining and representation | Workers' ability to organize, bargain, or be represented collectively | It expands | C08 | PRO-02, PRO-27, CON-21, ECI-03 | ok |
| C13 | Consumer protection | Rules against deceptive, predatory, or hidden practices | They strengthen | C08, C09 | PRO-16, ECI-02 | ok |
| C14 | Government favoritism toward particular industries or firms | Subsidies, carve-outs, exemptions, or protections for specific businesses | They decrease | C04 | CL-11, ECM-08, CON-03 | ok |

### Property and housing

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C15 | Property owners' rights | Owners' control over use of their property; protection from takings and forfeiture | It expands | C16, C17 | CL-04 | ok |
| C16 | Housing supply | Rules on building housing (zoning, permitting, approval steps) | Building gets easier | C15, C17, C21 | PRO-14, PRO-01 | gap |
| C17 | Renter stability and protections | Renters' protection from rent increases and eviction | It strengthens | C15, C16 | PRO-14 | ok |

### Government power and accountability

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C18 | Limits on government reach | Government agencies, programs, mandates, staff, regulatory powers, and spending authority | Any of these is removed or reduced | ⇆ C75 | VOT-11, CON-03, CL-06, PRO-06 | wording-test |
| C75 | Government programs and powers | Government agencies, programs, mandates, staff, regulatory powers, and spending authority | Any of these is created or expanded | ⇆ C18 | VOT-11, CON-03, CL-06, PRO-06 *(inherited from C18, rev. 4)* | wording-test |
| C19 | Decisions by elected officials and voters | Who makes a decision: elected officials and voters, or appointed boards, agencies, and experts | Decisions move toward elected officials or voters | ⇆ C76 | VOT-19, CL-06 | wording-test |
| C76 | Decisions by appointed experts and boards | Who makes a decision: elected officials and voters, or appointed boards, agencies, and experts | Decisions move toward appointed boards, agencies, or experts | ⇆ C19 | VOT-19, CL-06 *(inherited from C19, rev. 4)* | wording-test |
| C20 | Transparency and oversight | Public reporting, audits, open meetings, oversight of public bodies and money | They strengthen | — | CON-03, CL-06, PRO-15 | ok |
| C21 | Local control | Authority split between local governments and the state (preemption) | Authority moves to local governments | ⇆ C77 | PRO-17, CON-24, ECM-07 | wording-test |
| C77 | Statewide uniform rules | Authority split between local governments and the state (preemption) | Authority moves to the state | ⇆ C21 | PRO-17, CON-24, ECM-07 *(inherited from C21, rev. 4)* | wording-test |
| C22 | Checks and balances | Separation of powers and limits between branches | They strengthen | C19 | VOT-02, CL-06 | ok |
| C23 | Ability to enforce rules in court | Who can sue or be sued, penalties, enforcement powers | The ability to sue, penalize, or enforce expands | ⇆ C78 | CON-18, CON-22, CL-06, PRO-02, PRO-23 | wording-test |
| C78 | Protection from lawsuits and penalties | Who can sue or be sued, penalties, enforcement powers | Exposure to lawsuits, penalties, or enforcement shrinks | ⇆ C23 | CON-18, CON-22, CL-06, PRO-02, PRO-23 *(inherited from C23, rev. 4)* | wording-test |

### Rights and liberties

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C24 | Freedom of speech and expression | Protection of speech; compelled or restricted speech | Protection expands | C28, C72 | CON-13, CL-02 | ok |
| C25 | Religious exercise and conscience | Ability of individuals and organizations to act on religious belief, including exemptions | It expands | C28 | CON-12, VOT-18 | ok |
| C26 | Religious expression in public institutions | Religious expression in public schools and government | It expands | ⇆ C27 | CON-12, VOT-18 | ok |
| C27 | Limits on government religious endorsement | Limits on public institutions endorsing or sponsoring religion | They expand | ⇆ C26 | *(mirror of C26; no source yet)* | gap |
| C28 | Protection from discrimination | Anti-discrimination protections, including which characteristics are covered | They expand | C24, C25, C29, C30 | PRO-12, PRO-13, VOT-13, VOT-14, VOT-15 | ok |
| C29 | Group-neutral treatment by government | Whether government programs and decisions consider race, sex, or other group status | Such consideration decreases | C28 | CL-14, CON-08, VOT-13, VOT-15 | ok |
| C30 | Sex-based eligibility rules | Eligibility for sports, facilities, and programs based on sex as recorded at birth | Such rules are added | C28 | CON-08, VOT-14 | wording-test |
| C31 | Personal privacy and data | Collection, sharing, and retention of personal data by government or companies | It decreases | C63 | CL-08, CON-06, PRO-28 | ok |
| C32 | Due process | Fair procedures, presumption of innocence, legal protections for the accused | They strengthen | C46 | CL-07, PRO-08 | ok |
| C33 | Firearm ownership and carry | Legal ability to own, carry, and use firearms | It expands | ⇆ C34 | CON-11, CL-12, VOT-09 | ok |
| C34 | Firearm regulation | Rules on purchase, possession, carry, transfer, and storage of firearms | They tighten | ⇆ C33 | PRO-09, VOT-09 | ok |
| C35 | Access to abortion | Legal access to abortion | It expands | ⇆ C36 | PRO-04, CL-01, VOT-08 | ok |
| C36 | Legal protection of prenatal life | Legal protections for the embryo and fetus (gestational limits, restrictions on abortion) | They expand | ⇆ C35 | CON-14, VOT-08 | wording-test |
| C37 | Personal choice on drugs, gambling, sex work, and similar activities | Adults' legal freedom to engage in these activities | It expands | ⇆ C38 | CL-13, CL-01 | ok |
| C38 | Restrictions on drugs, gambling, and similar activities | Bans, limits, licensing caps, advertising limits on these activities | They tighten | ⇆ C37 | *(mirror of C37; no source yet)* | gap |

### Families and education

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C39 | Parents' authority over children's education and health | Parents' rights to know, consent, opt out, and direct | They expand | C40, C68 | CON-06, VOT-04 | ok |
| C40 | Students' access to information and services at school | Library materials, counseling, and health services available to students without added restriction | It expands | C39, C68 | PRO-25, PRO-13 | ok |
| C41 | Education options beyond the assigned public school | Public funding and legal room for alternatives (charters, vouchers, education savings accounts, homeschool) | It expands | C42 | CON-07, CL-09 | ok |
| C42 | Funding and stability of public school systems | Resources for and enrollment stability of district schools | They increase | C41 | PRO-24, PRO-19, PRO-06, VOT-04 | ok |
| C43 | Teacher pay and job protections | Teacher pay levels, raises, tenure, and job protections | They increase or strengthen | C79 | CON-19, PRO-19 | wording-test |
| C79 | Teacher pay tied to performance | Whether teacher pay, retention, and evaluation depend on measured performance | The link to performance strengthens | C43 | CON-19, PRO-19 *(inherited from C43, rev. 4)* | wording-test |
| C44 | Support for families with children | Child care, pre-K, child benefits, family leave | They expand | C01, C02 | CON-15, PRO-01, PRO-19 | ok |
| C45 | Retirement security and seniors | Benefits, pensions, and protections for older residents | They strengthen | C05 | CON-17, PRO-21 | ok |
| C68 | Required curriculum content | Content that schools must teach, display, or include | Content is required or added | C80, C39, C40 | CON-08, PRO-25 | wording-test |
| C80 | Limits on curriculum content | Content that schools may not teach, display, or include | Content is prohibited or restricted | C68, C39, C40 | CON-08, PRO-25 *(inherited from C68, rev. 4)* | wording-test |

### Safety and justice

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C46 | Enforcement and detention capacity | Police and prosecution resources; arrest and pretrial detention powers. Crime effects are inference (Q4, Q7) | They increase | C32, C47, C67 | VOT-07, CON-05, CON-22, PRO-22 | ok |
| C47 | Shorter sentences and alternatives to incarceration | Sentence lengths, mandatory minimums, early release, diversion, rehabilitation | Sentences shorten, or release and alternatives expand | ⇆ C81 | PRO-08, CON-05 | wording-test |
| C81 | Longer sentences and limits on early release | Sentence lengths, mandatory minimums, early release, diversion, rehabilitation | Sentences lengthen, or release and alternatives narrow | ⇆ C47 | PRO-08, CON-05 *(inherited from C47, rev. 4)* | wording-test |
| C48 | Rights of crime victims | Victims' notification, participation, and restitution rights | They strengthen | C32 | CON-05 | gap |
| C67 | Police accountability and oversight | Misconduct oversight, use-of-force limits, officer liability, public data | It expands | C46, C23 | PRO-23, CL-07 | gap |
| C49 | Public-order rules | Rules on camping, encampments, loitering, public drug use | They tighten | C66 | CON-20 | ok |
| C66 | Housing and services for people who are homeless | Shelter, housing, and treatment capacity | It expands | C49, C02 | PRO-14, CON-20 | ok |

### Health

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C50 | Healthcare coverage and access | Number of people covered; access to care, including addiction and mental-health treatment | It expands | C02 | PRO-03, VOT-03 | ok |
| C51 | Healthcare prices and choice | Cost of care; patients' and providers' choice among plans and providers | Prices fall or choice expands | C50 | VOT-03, CL-03, PRO-01 | ok |
| C71 | Access to contraception and fertility treatment | Legal access to and coverage of contraception and IVF | It expands | — | PRO-04, CON-23 | ok |

### Immigration

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C52 | State and local participation in immigration enforcement | Cooperation, detention agreements, and information sharing with immigration enforcement | It expands | C53, C21 | CON-04, CON-24, VOT-05 | ok |
| C53 | Legal status, services, and benefits for immigrants | State-level legal protections, services, and benefits for immigrants | They expand | C52 | PRO-20, VOT-05 | ok |

### Environment, energy, and resources

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C54 | Environmental protection and climate | Limits on pollution and emissions; conservation | They strengthen | C55, C08 | PRO-10, VOT-12 | ok |
| C55 | Energy cost and reliability | Energy prices and supply reliability | Prices fall or reliability improves | C54 | CON-10, PRO-10, VOT-06 | ok |
| C56 | Pollution burden on specific communities | Concentrated or cumulative pollution burden in particular neighborhoods | It decreases | C08, C16 | PRO-11 | gap |
| C57 | Use and development of land, water, and resources | Access to shared land, water, and natural resources for use, extraction, or development | Access for use or development expands | C54, C15 | ECI-07 | wording-test |

### Elections and democracy

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C58 | Ease of registering and voting | Steps required to register and vote | Steps are removed or simplified | C59 | PRO-07, VOT-02 | ok |
| C59 | Verification of voter eligibility and ballots | Identity, eligibility, and ballot verification steps | Steps are added | C58 | CON-09, VOT-02 | ok |
| C60 | Political spending disclosure | Public disclosure of who funds political spending and donations | It expands | ⇆ C61 | PRO-15 | ok |
| C61 | Political donor privacy | Ability to fund political spending and donations without public disclosure | It expands | ⇆ C60 | CL-02 | ok |
| C72 | Limits on political spending and contributions | Caps and bans on political contributions and spending | They tighten | C24, C61 | PRO-15 | gap |
| C62 | Citizens' power to propose and repeal laws | Initiative, referendum, and recall requirements | They get easier | — | PRO-18 | gap |
| C69 | Established voting and primary methods | How votes are cast and counted, and how primaries work | Single-choice plurality voting or party primaries are adopted or kept | ⇆ C82 | *(none yet)* | wording-test |
| C82 | Alternative voting and primary methods | How votes are cast and counted, and how primaries work | Ranked-choice voting, top-two, or open primaries are adopted or kept | ⇆ C69 | *(none yet)* *(inherited from C69, rev. 4)* | wording-test |
| C70 | District lines drawn by elected legislators | Who draws legislative and congressional districts, and by what rules | Elected legislators gain the role | ⇆ C83, C22 | PRO-26 | wording-test |
| C83 | District lines drawn by independent commissions | Who draws legislative and congressional districts, and by what rules | Independent or citizen commissions gain the role | ⇆ C70, C22 | PRO-26 *(inherited from C70, rev. 4)* | wording-test |

### Technology

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C63 | Rules on AI and online platforms | Rules on AI systems, algorithms, and online platforms | They tighten | ⇆ C64 | VOT-10, PRO-28 | gap |
| C64 | Freedom to build and use new technology | Room to develop and deploy technology without new restrictions | It expands | ⇆ C63 | VOT-10, CL-03 | gap |

### Public infrastructure

| ID | Concern | Axis | Advances when | Check against | Trail | Status |
|---|---|---|---|---|---|---|
| C65 | Infrastructure and transportation | Investment in roads, transit, water systems, broadband | It increases | C01, C05 | CON-20, PRO-01 | gap |

---

## Part B: Analysis questions (applied to every significant clause)

These come from the economist entries (ECM, ECI). Both sets turn out to be largely the same questions, asked with different expectations about the answer. Answers are always labeled **inference**, never fact.

| ID | Question | Trail |
|---|---|---|
| Q1 | **Compared to what?** What does current law do today, and what exactly changes? | ECM-01 |
| Q2 | **What does it cost, including what doesn't show up in the budget?** Direct cost, compliance cost, opportunity cost | ECM-02, ECM-06, ECI-05 |
| Q3 | **Who pays and who benefits in practice?** Not just who the text names, but who ends up bearing the cost | ECI-04, ECM-08 |
| Q4 | **How will people, businesses, and agencies respond?** Incentives created; second-stage effects | ECM-04, ECM-05 |
| Q5 | **What problem does it address, and does the mechanism reach it?** Consider problems on both sides: spillover costs, information gaps, shared-resource overuse, or unequal bargaining power that the clause may fix; and shortages, entry barriers, capture by the regulated industry, or perverse incentives that the clause may create or remove. If the text asserts a problem without a mechanism, say so | ECI-01, ECI-02, ECI-06, ECI-07, ECM-03, ECM-07, ECM-09 |
| Q6 | **Who gains power or discretion?** Consider elected officials, agencies, licensing boards, incumbent firms, employers, landlords, public- and private-sector unions, advocacy organizations, and any group that gets concentrated benefits while the costs are spread across many | ECM-08, ECM-09, ECI-03, ECM-07 |
| Q7 | **Is the effect empirically settled or disputed?** If researchers disagree, say so and describe both findings; don't pick a side | ECM-03, ECI-08 |
| Q8 | **How much is lost in administration and enforcement?** | ECI-05, ECM-10 |
| Q9 | **Can it be undone?** Constitutional vs. statutory, amendment threshold, sunset | CL-06, S39 |

---

## Part C: Text-quality flags (structural; not concerns)

From the prior checklist (S39), kept unchanged in substance:

| ID | Flag |
|---|---|
| F1 | Vague or expansive definitions of key terms |
| F2 | Override language ("notwithstanding any other provision of law") |
| F3 | Real effect depends on future regulations, appointments, or appropriations |
| F4 | Unfunded mandate (requires action without funding it) |
| F5 | Severability clause, or its absence |
| F6 | Effective date and phase-in |
| F7 | Amendment restrictions (supermajority to change; "furthers the purposes" limits) |
| F8 | Possible single-subject issue (unrelated provisions bundled) |
| F9 | Private right of action created |

---

## Log 1: Merges and splits

| Change | Result | Why |
|---|---|---|
| CON-01 inflation, PRO-01 lowering costs, VOT-01 | C07 + "cost of living" roll-up | Shared concern. Rev. 3: the price axes are C07 (household prices and charges, including rent and child-care fees), C51, and C55; no single score nets them. The roll-up displays them with C01 and with Part B price predictions labeled inference |
| CON-03 spending waste, CL-06 limits, PRO-15 influence | C20 | All ask "can the public see and check what government does with power and money" |
| CON-07 school choice, CL-09 education choice | C41 | Same policy, described as parental vs. individual liberty |
| CL-07 due process, PRO-08 justice reform (procedure part) | C32 | Shared value; the sentencing part went to C47 |
| CON-10 energy production, PRO-10 lower energy costs | C55 (cost) + C54 (environment) | Both want low, reliable energy prices; they disagree on means. Splitting cost from environment makes that visible |
| CON-08 school content on race, sex, gender | C39 (who decides) + C30 (eligibility rules) + C68 (content) | Rev. 2: content restored as its own axis (C68); "who decides" alone hid voters who want specific content required |
| CON-20 public order, PRO-14 homelessness | **Split** (rev. 2) into C49 (public-order rules) and C66 (housing and services) | A camping ban and a housing program move different things |
| ECM and ECI lists | Part B | Methods, not concerns |
| PRO-07 voting rights restoration | C58 | Subset of ease of voting |
| PRO-04 contraception part, CON-23 | C71 (rev. 2) | Previously dropped silently. The full platform read showed both sides support access, so it's a shared concern, not a pair |
| CL-13 sex work | C37 (rev. 2) | Previously dropped silently; now named on the axis |
| C03, C18, C19, C21, C23, C47, C69, C70 (⇄) | Mirror pairs with C73, C75, C76, C77, C78, C81, C82, C83 (rev. 4) | A concern with no preferred direction can't be supported or conflicted with. Splitting the axis gives each side its own named concern, as the existing mirror pairs already did. New concerns inherit the parent's trail until it's re-sorted per side |
| C06 (⇄) | C06 budget flexibility + C74 guaranteed funding (rev. 4) | Not a mirror: a tax cap reduces flexibility without guaranteeing any funding |
| C43 (⇄) | C43 pay and job protections + C79 pay tied to performance (rev. 4) | Not a mirror: an across-the-board raise supports C43 and has no effect on C79 |
| C68 (⇄) | C68 required content + C80 limits on content (rev. 4) | Content itself can't have a neutral direction, so the concerns are about *requiring* vs *restricting*. Same rule for different content (e.g. different faiths' texts) must get the same result. Who decides stays on C39 and C21/C77 |
| C57 (⇄) | C57 use and development of resources (rev. 4) | The protection side is already C54 |

## Log 2: Excluded (and why)

| Item | Why excluded |
|---|---|
| Foreign policy (S01), military, reserve currency (S05) | Almost entirely federal; revisit in Phase 3 |
| "Investigations into Trump" (S01) | About a person, not a policy; breaks rule 2 |
| Political style and civility (S02) | Not something a law's text moves |
| "Christian culture" as such (VOT-18) | Reworded as C25/C26, which a law's text can move; the cultural question itself isn't a legal axis |
| Trust in parties (S02) | Not a policy concern |
| Feeling ignored by politics (VOT-20) | Not something a law's text moves; the financial-stress half of VOT-20 is covered by C07 |

## Log 3: Gaps (status `gap` or `wording-test`)

| Concern | Missing | Source to add |
|---|---|---|
| C16 | Market / abundance-side source; no classical-liberal or conservative source on zoning | YIMBY / abundance groups; Cato or Mercatus on zoning |
| C21 | Source for conservative or classical-liberal support of *local* control (CON-24 shows the opposite case) | Local-control arguments against state housing or energy mandates |
| C27 | Any steelman source for limits on government religious endorsement | Americans United for Separation of Church and State; Baptist Joint Committee |
| C30 | Step-4 wording test | Reviewers from each perspective |
| C36 | Step-4 wording test on the name: "protection of prenatal life" may state the holder's claim (re-review, Round 2). Axis is settled | Reviewers from each perspective |
| C72 | Source arguing *against* spending caps on their own terms (separate from donor privacy) | Institute for Free Speech; Cato on contribution limits |
| C12 | CON-21 rests on S08, which is still a search summary. Until S08 is read in full, C12 counts as single-perspective | Full read of S08 (site blocks automated fetches; needs a manual read) |
| C38 | Steelman source for restrictions | Public-health organizations on gambling and cannabis; Smart Approaches to Marijuana; state attorney-general reports |
| C48 | Victims'-rights source | Marsy's Law for All; National Organization for Victim Assistance |
| C56 | Other side: permitting speed, equal treatment, cost | Permitting-reform sources (cross-perspective; abundance groups) |
| C57 | Resource-specific sources | State water-bond analyses; conservation and agricultural groups |
| C62 | Source for *limiting* initiatives (higher thresholds, single-subject rules) | Legislative sponsors of I&R reform measures (8 on 2026 ballots per S38) |
| C63/C64 | AI-specific sources on both sides | State AI-bill sponsors; tech-industry groups; civil-society AI-safety groups |
| C65 | Infrastructure source | ASCE Infrastructure Report Card; state DOT / bond analyses |
| C67 | Classical-liberal source read in full; law-enforcement side | IJ qualified-immunity project; NAACP LDF; a police association |
| C68 | Curriculum-content sources on both sides | Curriculum-mandate bills (civics, financial literacy, ethnic studies, etc.) and their sponsors |
| C69 | Any source | FairVote; opponents of ranked-choice voting (states that banned it) |
| C70 | Other-side source | Arguments for legislature-drawn maps; commission critics |
| (candidate) | Animal welfare | Frequent ballot topic (farm-animal confinement, hunting); not yet in any perspective list |
| (candidate) | Tribal sovereignty and gaming | Recurring ballot topic; S06 has a Tribal Nations section |
| (candidate) | Rural interests (agriculture, rural services) | Rural voters under-represented in sources so far |

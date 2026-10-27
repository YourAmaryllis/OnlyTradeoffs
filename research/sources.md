# Source Registry — Phase 0 Concern Research

Every source used to build the concern list gets an ID here. Perspective notes (`perspectives.md`) cite these IDs, and every concern in `concerns-v1.md` cites perspective entries, so any concern can be traced back to the documents that put it there.

**Access level**, i.e. how much of the source we actually read:

- **F**: fetched and read directly (full text or the relevant part)
- **A**: fetched and archived in `research/raw/`
- **S**: read through a search-engine summary of the page. The URL is known, but the full text wasn't read. **Read in full before v1 is frozen.**
- **K**: a well-known primary work cited from general knowledge, not opened in this session. **Get a copy and verify before v1 is frozen.**

Research session: 2026-10-26.

## Voter-level data (what the public ranks, by group)

| ID | Source | Date | Access | Used for |
|---|---|---|---|---|
| S01 | Pew Research Center, "Economy ranks as top issue in midterms for all voters, but partisans differ over the importance of other issues" — https://www.pewresearch.org/politics/2026/10/08/economy-ranks-as-top-issue-in-midterms-for-all-voters-but-partisans-differ-over-the-importance-of-other-issues/ | 2026-10-08 (survey Sep 28–Oct 4, 2026) | F | 16 issues × % "very important", by party preference |
| S02 | Pew Research Center, "Beyond Red vs. Blue: The Political Typology" (2026) — https://www.pewresearch.org/wp-content/uploads/sites/20/2026/06/PP_2026.5.10_political-typology_report.pdf | 2026 (survey Nov 17–30, 2025, n=10,357) | A (`raw/pew-2026-political-typology.*`) | 9 value clusters; value questions (gov size, checks & balances, equal opportunity, secure borders, capitalism, Christian culture, economic fairness, experts) |
| S03 | AP-NORC, "2026: The public's priorities and expectations" — https://apnorc.org/projects/2026-the-publics-priorities-and-expectations/ | Dec 2025 | S | Open-ended priorities by party: personal finance, immigration, health care, environment, crime, taxes |
| S04 | Gallup, Most Important Problem / Economic Confidence, April 2026 — https://news.gallup.com/file/poll/708746/260423ECI.pdf | Apr 2026 | S | Cost of living, inequality, debt, taxes, jobs as named problems |
| S38 | Ballotpedia News, 2026 statewide measure topics; "2026 had the fewest ballot initiatives filed since 2014" — https://news.ballotpedia.org/2026/09/11/2026-had-the-fewest-ballot-initiatives-filed-since-2014-with-692/ ; initiative-process measures — https://news.ballotpedia.org/2026/08/26/at-least-eight-ballot-measures-in-2026-will-address-state-initiative-and-referendum-processes-the-highest-number-since-2000/ | Aug–Sep 2026 | S | **Coverage check only**: what topics actually show up on ballots (income tax, campaign finance, LGBTQ, abortion, drug policy, voter ID, I&R process, housing, firearms). Not a source of concerns. |

## Party platforms (used only to collect concerns, never shown in or sent to the evaluation)

| ID | Source | Date | Access | Used for |
|---|---|---|---|---|
| S05 | 2024 Republican Party Platform — https://www.presidency.ucsb.edu/documents/2024-republican-party-platform | Jul 2024 | A (`raw/gop-2024-platform.txt`) | 20 promises, 10 chapters; state/local-relevant items. Full text read 2026-10-26 (bias-review pass) |
| S06 | 2024 Democratic Party Platform — https://www.presidency.ucsb.edu/documents/2024-democratic-party-platform | Aug 2024 | A (`raw/dnc-2024-platform.txt`) | 9 chapters; state/local-relevant items. First pass read only ~100k of 291k chars; full text read 2026-10-26 (bias-review pass) |
| S07 | Libertarian Party platform (state affiliate copy of national text) — https://bookstack.aklp.org/books/foundational-documents/page/platform | current | S | Personal liberty & economic liberty sections and subsections |

## Conservative / right-of-center policy sources

| ID | Source | Date | Access | Used for |
|---|---|---|---|---|
| S08 | American Compass, "New Direction" agenda — https://americancompass.org/new-direction/ | 2023 | S | Worker/family/industry-focused conservatism: family benefits, non-college pathways, reshoring, worker representation. *Full read attempted 2026-10-26: the site returns 403 to automated fetches (Cloudflare). Needs a manual read and an archived copy in `raw/`. Until then CON-21 does not count as a perspective (`[strand]` tag).* |
| S09 | Heritage Foundation Election Integrity Scorecard (2026 update, via Daily Signal) — https://www.dailysignal.com/2026/09/15/election-integrity-scorecard/ | Sep 2026 | S | Voter ID, list accuracy, absentee rules, ballot harvesting, observers, citizenship verification, audits, private election funding |
| S10 | ALEC task-force areas (via Britannica) — https://britannica.com/topic/American-Legislative-Exchange-Council | current | S | Policy areas at state level: civil justice, commerce, tech, criminal justice, education, energy, health, tax |
| S11 | Manhattan Institute, "Reforming New York's Bail Reform" — https://manhattan.institute/article/reforming-new-yorks-bail-reform-a-public-safety-minded-proposal | 2020–22 | S | Pretrial release, judicial discretion over public-safety risk, repeat offenders |
| S12 | State parental-rights statutes: Kansas HB 2662 (2022) — https://www.kslegislature.gov/li_2022/b2021_22/measures/documents/hb2662_01_0000.pdf ; NY A7835 (2023) — https://www.nysenate.gov/legislation/bills/2023/A7835 | 2022–23 | S | Curriculum transparency, notification, opt-out, consent provisions as written in actual bill text |
| S13 | Tax Foundation, "Principles of Sound Tax Policy" — https://taxfoundation.org/taxedu/principles/ | current | S | Simplicity, transparency, neutrality, stability |

## Classical liberal / libertarian policy sources

| ID | Source | Date | Access | Used for |
|---|---|---|---|---|
| S14 | Institute for Justice, four pillars — https://ij.org/ll/l-l-12-14-the-institute-for-justice-is-the-national-law-firm-for-liberty/ | current | S | Economic liberty, property rights (eminent domain, civil forfeiture), school choice, free speech |
| S15 | Cato Handbook for Policymakers, 9th ed. — https://www.cato.org/cato-handbook-policymakers/cato-handbook-policymakers-9th-edition-2022 | 2022 | S | Liberty/free-market recommendations across ~77 federal and state chapters |
| S16 | Mercatus Center, state regulatory accumulation, certificate-of-need, occupational licensing — https://www.mercatus.org/scholars/matthew-d-mitchell | current | S | Regulatory budgets and sunsets; entry barriers |
| S17 | FIRE (Foundation for Individual Rights and Expression), mission & issue areas — https://www.thefire.org | current | K | Speech, campus expression, donor privacy, compelled speech |
| S07 | (Libertarian Party platform, above) | | | |

## Progressive / left-of-center policy sources

| ID | Source | Date | Access | Used for |
|---|---|---|---|---|
| S19 | The Fairness Project, campaigns & issues — https://thefairnessproject.org | current | S | Ballot-measure agenda: minimum wage, paid leave, Medicaid expansion, predatory debt, reproductive rights, direct democracy |
| S20 | ITEP, "Who Pays?" 7th ed. — https://itep.org/executive-summary/ | 2024 | S | Distribution of state/local taxes by income; regressivity |
| S21 | Center on Budget and Policy Priorities, state fiscal policy & TABOR — https://www.cbpp.org/info.html | current | S | Revenue adequacy, public services, tax/spending limits, EITC |
| S22 | Brennan Center, Voting Laws Roundup (Sep 2026) — https://www.brennancenter.org | Sep 2026 | S | Restrictive vs. expansive voting law categories |
| S23 | Economic Policy Institute, worker-rights preemption map & state pages — https://www.epi.org/state/ | current | S | Minimum wage, scheduling, prevailing wage, paid leave; state preemption of local labor standards |
| S24 | The Sentencing Project (priorities) — https://www.sentencingproject.org/about-us/ ; Vera Institute, new sentencing paradigm — https://vera.org/newsroom/the-vera-institute-of-justice-proposes-a-new-paradigm-for-sentencing-in-the-united-states | 2023–24 | S | Sentence caps, second-look, mandatory minimums, youth justice, voting rights for people with convictions |
| S25 | EPA environmental justice definition and cumulative impacts framework; Rhode Island H 8036 (2022) — https://webserver.rilegislature.gov/BillText22/HouseText22/H8036.htm | 2022–24 | S | "Fair treatment and meaningful involvement"; cumulative pollution burden |

## Economists, market-oriented

| ID | Source | Date | Access | Used for |
|---|---|---|---|---|
| S26 | Thomas Sowell: three questions ("Compared to what? At what cost? What hard evidence?") — https://www.goodreads.com/author_blog_posts/23377441 ; *Basic Economics* (5th ed., 2014); *Applied Economics: Thinking Beyond Stage One* (2004) | — | S (quote) / K (books) | Baseline comparison, cost, evidence, second-stage effects, incentives |
| S27 | Milton Friedman, *Capitalism and Freedom* (1962), ch. 9 on occupational licensure; *Free to Choose* (1980), "four ways to spend money" | — | K | Licensing as an entry barrier; spending other people's money on other people |
| S28 | F.A. Hayek, "The Use of Knowledge in Society," *American Economic Review* (1945) | — | K | Local knowledge; limits of central planning |
| S29 | James Buchanan & Gordon Tullock, *The Calculus of Consent* (1962); Econlib bio — https://www.econlib.org/library/Enc1/bios/Buchanan.html | — | S / K | Public choice: concentrated benefits/diffuse costs; incentives of officials; constitutional rules |
| S30 | Frédéric Bastiat, "That Which Is Seen and That Which Is Not Seen" (1850) | — | K | Unseen costs / opportunity cost |

## Economists, interventionist / institutional

| ID | Source | Date | Access | Used for |
|---|---|---|---|---|
| S31 | Arthur Okun, *Equality and Efficiency: The Big Tradeoff* (1975); summaries — https://www.econlib.org/library/Enc/bios/Okun.html , https://equitablegrowth.org/calculating-the-leak-in-okuns-bucket/ | — | S / K | Equity–efficiency tradeoff; the "leaky bucket" (admin cost + incentive effects of redistribution) |
| S32 | Joseph Stiglitz, Nobel lecture "Information and the Change in the Paradigm in Economics" (2001) — https://www.math.utoronto.ca/mccann/1855/papers/stiglitz-Nobel-lecture01.pdf | 2001 | S | Asymmetric information; markets not efficient when incomplete; room for corrective policy |
| S33 | George Akerlof, "The Market for 'Lemons'," *QJE* (1970) | — | K | Quality uncertainty; disclosure and standards |
| S34 | A.C. Pigou, *The Economics of Welfare* (1920) | — | K | Externalities; corrective taxes |
| S35 | Elinor Ostrom, *Governing the Commons* (1990) | — | K | Shared resources; local and community governance (fits neither camp neatly; included on purpose) |
| S36 | Emmanuel Saez & Gabriel Zucman, *The Triumph of Injustice* (2019) | — | K | Tax progressivity; effective rates at the top |
| S37 | David Card & Alan Krueger, "Minimum Wages and Employment" (NJ/PA), *AER* (1994) | — | K | Employment effect of minimum wage is an empirical question; monopsony |

## Prior work

| ID | Source | Access | Used for |
|---|---|---|---|
| S39 | Prior agent's checklist — `reference/prior-checklist-v0.md` | F | Mechanism list and text-quality flags (kept); tribe-based structure (dropped) |

## Gaps to close before freezing v1

1. Upgrade every **S** to **F**: open and read the actual page or report, especially S03, S04, S09, S20, S21, S22, S23.
2. Upgrade every **K** to **F**: get the texts (several are public domain or on Econlib).
3. **Add perspective sources this pass didn't reach:**
   - Conservative: Heritage issue pages, State Policy Network affiliates, Family Policy Alliance (or similar) on family/religious liberty, NRA-ILA on firearms.
   - Classical liberal: Goldwater Institute (state-level), Reason Foundation (pensions, privatization).
   - Progressive: Center for American Progress, ACLU state priorities, Everytown on firearms, SEIU / AFL-CIO, NAACP LDF, Movement Advancement Project (LGBTQ).
   - Cross-cutting: YIMBY / abundance housing groups, Pew's own state-policy work, AARP (seniors), NFIB (small business).
4. Add a non-partisan religious-voter source and a rural-voter source; both are under-covered.
5. ~~Full read of S06.~~ Done 2026-10-26.
6. Add steelman sources for the concerns added in the bias-review pass: police accountability (IJ qualified-immunity work, NAACP LDF, Campaign Zero; and a law-enforcement association for the other side), curriculum content (both sides), election methods (FairVote; opponents of ranked-choice voting), redistricting commissions (both sides), YIMBY / abundance housing sources for C16, a permitting-speed source to pair with C56, and a conservative/classical-liberal source on local control (e.g. local zoning vs. state housing mandates).

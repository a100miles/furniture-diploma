# Evidence of Relevance

**Task:** DIP-4 · **Owner:** Muzaffar Kapezov · **Status:** protocol ready, interviews to be conducted and recorded before 24 October 2026

The committee requires 3–5 discussions with user representatives (or a substantive agreement with a real client) and asks whether **verified findings are distinguished from assumptions**. This document holds the protocol, the record of each discussion, and the resulting findings. Only the "Findings" section may be used as evidence in the proposal and requirements; anything not confirmed there stays in the assumption register.

> ⚠️ The interview records in §4 are **empty templates**. Do not fill them with invented answers: write only what participants actually said, with their consent.

## 1. Hypotheses to test

| ID | Hypothesis (assumption) | Linked requirement |
|----|-------------------------|--------------------|
| H1 | People buying furniture online are often unsure whether an item will fit the room | FR-01, FR-02, FR-07 |
| H2 | Non-designers find it hard to arrange furniture and would accept an automatic suggestion as a starting point | FR-06 |
| H3 | Users want recommendations filtered by style **and** budget, and want to know why an item is recommended | FR-05, FR-09 |
| H4 | A browser tool without installation is preferred over a mobile app | NFR-04 |
| H5 | Users would trust an AI layout more if it visibly respects walkways and door clearance | FR-07 |
| H6 | Furniture sellers / interior designers would use such a tool with clients | Target users |

## 2. Participants (plan)

| # | Profile | Why | Recruited by | Status |
|---|---------|-----|--------------|--------|
| P1 | Student or young professional who recently furnished a rented flat | Core target user | Sultanbek | ☐ |
| P2 | Family that bought furniture in the last 12 months | Core target user, higher budget | Muzaffar | ☐ |
| P3 | Furniture store salesperson / showroom manager (Astana) | Seller perspective, real objections of buyers | Tamerlan | ☐ |
| P4 | Interior designer (freelance or studio) | Expert view on layout rules and tools they use | Muzaffar | ☐ |
| P5 | Online furniture shopper who returned an item because it did not fit (optional) | Direct evidence for H1 | Sultanbek | ☐ |

If a furniture retailer agrees to provide catalog data or to pilot the tool, record it as a **client agreement** in §5 — this is stronger evidence than interviews.

## 3. Interview guide (20–30 minutes, semi-structured)

**Consent.** Explain the project, that participation is voluntary, that notes will be anonymised (P1…P5), and ask permission to take notes/record. Do not store names, phone numbers or recordings in the repository.

**A. Context**
1. When did you last choose furniture for a room? What was it and for which room?
2. Where did you look (store, marketplace, Instagram, IKEA, Kaspi, …)?

**B. Problems (H1, H2)**
3. How did you decide whether it would fit? Did you measure? Did anything turn out the wrong size?
4. How did you decide where to put it? Who helped you?
5. What was the hardest part of the whole process?

**C. Existing tools (H4)**
6. Have you used any planner or AR app (IKEA, Planner 5D, …)? What did you like / dislike?
7. Phone app or website — which would you use for this, and why?

**D. Proposed concept (H3, H5)** — show the prototype or mockups (`docs/ux-prototype.md`).
8. If the system suggested 5 sofas that fit your room, style and budget, what would make you trust the suggestion?
9. Would an explanation like "fits a 4 m wall, Scandinavian, 20 % under budget" help?
10. If it arranged the furniture automatically, would you use it as is, adjust it, or ignore it?

**E. Seller / designer only (H6)**
11. What questions do customers ask most often before buying?
12. Would you show such a tool to a customer? What would it need to have?

**F. Close**
13. Anything we did not ask that matters to you?

## 4. Interview records

Copy this block for each participant.

```
### P#: <profile>
Date / place / format: 
Interviewer / note-taker: 
Consent obtained: yes / no

Key quotes (verbatim, anonymised):
- 

Observations:
- 

Hypotheses: H1 confirmed / refuted / no evidence — note
            H2 …
            H3 …
            H4 …
            H5 …
            H6 …

New requirements or changes suggested:
- 
```

## 5. Client agreement (if any)

| Organisation | Contact role | What was agreed (data, pilot, feedback) | Date | Evidence (email/letter stored outside repo) |
|--------------|--------------|------------------------------------------|------|----------------------------------------------|
| — | — | — | — | — |

## 6. Findings (fill after interviews)

| Hypothesis | Participants supporting | Participants contradicting | Verdict | Effect on requirements |
|------------|-------------------------|----------------------------|---------|------------------------|
| H1 | | | | |
| H2 | | | | |
| H3 | | | | |
| H4 | | | | |
| H5 | | | | |
| H6 | | | | |

## 7. Secondary evidence already available

These are published findings, not our own data, and are cited as such:

- Size and fit uncertainty is the main barrier that AR furniture tools address (Öztürkcan, 2021).
- Interactive visualisation increases enjoyment and purchase intention, but a plain website was rated more useful (Kowalczuk et al., 2021) — suggesting decision support matters, not just 3D.
- Major retailers (IKEA Kreativ) and planners (Planner 5D) invest in AI room tools, indicating market demand (see `existing-systems.md`).

## 8. Assumption register

Statements used in the proposal that are **not yet verified** by our own evidence. Move a row to §6 once an interview confirms or refutes it.

| Assumption | Used in | Planned check |
|------------|---------|---------------|
| H1–H6 above | proposal, requirements | Interviews P1–P5 |
| Target users have a laptop or desktop browser with WebGL | NFR-04 | Interview Q7 + browser stats |
| A curated catalog of ~50 items is enough to demonstrate value | scope | Supervisor feedback, usability test |

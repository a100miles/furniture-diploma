# Pre-defense 1 submission (24 October 2026)

| Item | Value |
|------|-------|
| Repository | https://github.com/a100miles/furniture-diploma |
| Tag | `pre-defense-1` (create on reviewed `main` after merging the pre-defense PRs — DIP-16) |
| YouTrack | https://furniture-diploma.youtrack.cloud/projects/DIP |

## Completed work
- Analysis: literature review (24 peer-reviewed papers + 2 technical sources, all open access), existing systems comparison, technology comparison, evidence-of-relevance protocol.
- Design: requirements with acceptance criteria, architecture description, system context / use case / component diagrams and database schema with editable sources.
- Planning: backlog DIP-1…DIP-31 with owners and acceptance criteria, milestones, risks, dependencies; verification and evaluation plan.
- Prototype (single Python service, before the split into Go core API + ML service): FastAPI backend (catalog, explained recommendations, auto-layout, validation, save/load) and React + three.js 3D editor; 35 backend tests and frontend geometry tests.

## Known limitations
- Demo catalog (25 items, illustrative prices), furniture shown as boxes.
- Projects stored in memory; 90° rotations only; walkway clearance is a soft rule.
- Existing-systems claims partly based on vendor/press sources until hands-on checks are done.

## Outstanding tasks
- Conduct and record 3–5 interviews (DIP-4); update requirements with findings.
- Supervisor review and feedback log (DIP-12).
- Populate YouTrack and link tasks to PRs (DIP-11).
- Second store parser and 5 000+ items (DIP-25, FR-31); mebel.kz parser done with 4 084 items, not yet loaded into the prototype API.
- Next milestone: PostgreSQL persistence (DIP-17), 3D models (DIP-18), clearance constraints (DIP-19), benchmark (DIP-20).

## Tamerlan's one-minute ML explanation

The current prototype uses explicit constraints and rule-based scoring; CLIP is planned, not yet implemented. CLIP represents product images and text in a shared embedding space, allowing a text request to retrieve visually relevant furniture. Numeric dimensions and budget must still be checked explicitly. Similarity alone does not guarantee compatibility with furniture already selected.

We compare the planned ranker with B1: filter by category and price, then sort cheapest first, and with the current rule-based scorer. For 50–100 realistic queries, two team members independently grade candidates 0, 1 or 2; an interior designer reviews disagreements, and we report agreement. nDCG@10 measures whether highly relevant items appear near the top, relative to an ideal ordering. We also report Precision@5/10 and hard-constraint satisfaction. Beating B1 is an evaluation target, not a result we have already obtained.

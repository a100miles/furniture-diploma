# Pre-defense 1 submission (24 October 2026)

| Item | Value |
|------|-------|
| Repository | https://github.com/a100miles/furniture-diploma |
| Tag | `pre-defense-1` (create on reviewed `main` after merging the pre-defense PRs — DIP-16) |
| YouTrack | _TODO: project URL_ |

## Completed work
- Analysis: literature review, existing systems comparison, technology comparison, evidence-of-relevance protocol.
- Design: requirements with acceptance criteria, architecture description, system context / use case / component diagrams and database schema with editable sources.
- Planning: backlog DIP-1…DIP-24 with owners and acceptance criteria, milestones, risks, dependencies; verification and evaluation plan.
- Prototype (single Python service, before the split into Go core API + ML service): FastAPI backend (catalog, explained recommendations, auto-layout, validation, save/load) and React + three.js 3D editor; 35 backend tests and frontend geometry tests.

## Known limitations
- Demo catalog (25 items, illustrative prices), furniture shown as boxes.
- Projects stored in memory; 90° rotations only; walkway clearance is a soft rule.
- Existing-systems claims partly based on vendor/press sources until hands-on checks are done.

## Outstanding tasks
- Conduct and record 3–5 interviews (DIP-4); update requirements with findings.
- Supervisor review and feedback log (DIP-12).
- Populate YouTrack and link tasks to PRs (DIP-11).
- First catalogue data from local store parsers (DIP-25).
- Next milestone: PostgreSQL persistence (DIP-17), 3D models (DIP-18), clearance constraints (DIP-19), benchmark (DIP-20).

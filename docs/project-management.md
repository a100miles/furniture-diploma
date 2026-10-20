# Project Management and Risks

**Task:** DIP-11 · **Status:** draft for pre-defense 1 (24 October 2026)

## 1. Tools and links

| Item | Link |
|------|------|
| Git repository | https://github.com/a100miles/furniture-diploma |
| YouTrack project (key `DIP`) | **TODO: paste the YouTrack project URL here** |
| Backlog import file | [`project-management/youtrack-backlog.csv`](../project-management/youtrack-backlog.csv) |

**YouTrack setup (one-time).** Create project with key `DIP`, add all three team members and the supervisor, then *Import → CSV* the backlog file (columns map to Summary, Assignee, Priority, Due Date, Description). Task numbers will then match the IDs used in this repository (DIP-1 … DIP-24). For each task add the acceptance criteria from the CSV and, when done, a link to the pull request.

## 2. Working process

- `main` is the reviewed baseline. Nobody pushes to `main` directly.
- One branch per task: `DIP-<n>-short-name` (e.g. `DIP-14-room-editor`).
- Commit messages start with the task ID: `DIP-14: Add drag-to-move for furniture`.
- Each change goes through a pull request that (1) explains the change, (2) references the YouTrack task, (3) says how it was checked. Another team member reviews before merge.
- Each student commits from their own GitHub account with their real name and university e-mail in `git config user.name / user.email`.
- Weekly sync (30 min) and a meeting with the supervisor every two weeks; notes in `supervisor-feedback.md`.
- Each pre-defense submission is tagged: `pre-defense-1`, `pre-defense-2`, `final-pre-defense`. Tags are never moved.

## 3. Allocation of responsibilities

*Proposed split — to be confirmed by the team at the next sync.*

| Member | Primary area | Secondary area |
|--------|--------------|----------------|
| **Tamerlan Yessimov** | Backend (FastAPI), data model, database, repository & CI | Technology comparison, project management |
| **Sultanbek Zhumagali** | Frontend 3D room editor (React + three.js), UX mockups | Existing systems comparison, usability study |
| **Muzaffar Kapezov** | AI layer: recommendation engine, auto-layout algorithm, benchmark | Literature review, evaluation plan |

All members: interviews (`relevance-evidence.md`), requirements review, testing.

## 4. Backlog (pre-defense 1 scope and next steps)

| ID | Task | Owner | Priority | Due | Acceptance criteria |
|----|------|-------|----------|-----|---------------------|
| DIP-1 | Repository structure, README, .gitignore, config example | Tamerlan | Critical | 21 Oct | README covers all items from the guidelines; structure has src/docs/diagrams/tests/config |
| DIP-2 | Project proposal and scope | Tamerlan | Critical | 22 Oct | Title, team, supervisor, problem, users, aim, objectives, outcomes, scope present |
| DIP-3 | Requirements specification (FR/NFR, priorities, acceptance criteria) | Muzaffar | Critical | 22 Oct | Every mandatory requirement has a verifiable acceptance criterion |
| DIP-4 | Evidence of relevance: 3–5 interviews | Sultanbek | Critical | 23 Oct | ≥ 3 interview records; findings table filled; assumptions separated |
| DIP-5 | Literature review | Muzaffar | Critical | 22 Oct | ≥ 12 sources, ≥ 8 scientific, analysis table, synthesis |
| DIP-6 | Existing system comparison | Sultanbek | Critical | 22 Oct | 3–5 systems × 6–10 criteria; hands-on evidence for each claim |
| DIP-7 | Technology comparison | Tamerlan | Critical | 22 Oct | ≥ 3 decisions × 2–3 alternatives, justified by requirements |
| DIP-8 | Architecture description and diagrams (context, use case, component) | Tamerlan | Critical | 23 Oct | Editable sources + exports in `docs/diagrams/`; consistent with requirements |
| DIP-9 | UX mockups and prototype | Sultanbek | Critical | 23 Oct | Key scenarios covered; prototype runs locally |
| DIP-10 | Verification and evaluation plan | Muzaffar | Critical | 22 Oct | Test plan, metrics, conditions, baseline defined |
| DIP-11 | Project management, YouTrack, risks | Tamerlan | Critical | 21 Oct | YouTrack populated; risks and milestones documented |
| DIP-12 | Supervisor review of pre-defense 1 package | All | Critical | 23 Oct | Feedback recorded with decisions in `supervisor-feedback.md` |
| DIP-13 | Backend skeleton: catalog and recommendation API | Tamerlan | High | 23 Oct | `/api/catalog`, `/api/recommendations` with tests passing |
| DIP-14 | 3D room editor prototype | Sultanbek | High | 23 Oct | Room setup, add/move/rotate/remove furniture in 3D |
| DIP-15 | Auto-layout algorithm v1 (rule-based) | Muzaffar | High | 23 Oct | No overlaps/out-of-bounds on test rooms; unit tests |
| DIP-16 | Tag `pre-defense-1` and submission summary | Tamerlan | Critical | 24 Oct | Tag on reviewed `main`; summary with limitations and open tasks |
| DIP-17 | PostgreSQL persistence and save/load projects (FR-08) | Tamerlan | High | Nov | Projects persist across restarts; migrations |
| DIP-18 | glTF furniture models and catalog of ≥ 50 items | Sultanbek | High | Nov | Models load < 1 s each; licences recorded |
| DIP-19 | Clearance and door-swing constraints in layout (FR-07) | Muzaffar | High | Nov | Clearance violation rate ≤ 5 % on benchmark |
| DIP-20 | Benchmark set and baselines B1/B2 | Muzaffar | High | Dec | 30 rooms; metrics script reproducible |
| DIP-21 | Style embedding recommendations (pgvector) | Muzaffar | Medium | Jan | Hybrid ranking beats B1 on precision@5 |
| DIP-22 | CI pipeline (lint, tests) on GitHub Actions | Tamerlan | Medium | Nov | Every PR runs tests |
| DIP-23 | Usability study | Sultanbek | High | per schedule | 8–12 participants, SUS and task metrics reported |
| DIP-24 | Optional natural-language requests (LLM → constraints) | Muzaffar | Low | per schedule | Text prompt produces valid constraint set |

## 5. Milestones

| Milestone | Target date | Content |
|-----------|-------------|---------|
| M1 · Pre-defense 1 | **24 Oct 2026** | Analysis, design, planning documents; runnable prototype; tag `pre-defense-1` |
| M2 · Core MVP | Dec 2026 | Persistence, ≥ 50-item catalog with models, layout v1 with clearance |
| M3 · Pre-defense 2 | per university schedule | AI features complete, algorithm evaluation, tag `pre-defense-2` |
| M4 · Final pre-defense | per university schedule | Usability study, final report, tag `final-pre-defense` |

## 6. Risks

| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|:-----------:|:------:|------------|-------|
| R1 | 3D models of real furniture are unavailable or have restrictive licences | High | High | Start with parametric box/low-poly models; use CC0 sources (e.g. Poly Haven, Kenney); record licence per model | Sultanbek |
| R2 | WebGL performance too low on weak laptops | Medium | Medium | Low-poly models, instancing, limit shadows; measure NFR-01 early | Sultanbek |
| R3 | AI scope creep (training ML models takes too long) | High | High | Rule-based v1 first; ML/LLM only as optional replaceable module | Muzaffar |
| R4 | Not enough interview participants before 24 Oct | Medium | High | Recruit from 3 channels (university, stores, designers); online calls allowed | All |
| R5 | Uneven contributions visible in Git history | Medium | High | Task ownership in YouTrack; each member commits own work from own account | Tamerlan |
| R6 | Dependency on external LLM API (cost, availability, keys) | Medium | Medium | LLM is optional; keys only in `.env`, never in repo; fallback to rules | Muzaffar |
| R7 | Catalog data (prices) becomes outdated | Medium | Low | Prices marked with date; import script; demo catalog clearly labelled | Tamerlan |
| R8 | Team member unavailable (illness, exams) | Medium | Medium | Documented code, PR reviews spread knowledge, secondary owner per area | All |

## 7. Dependencies

- DIP-3 (requirements) ← DIP-4 (interview findings), DIP-5, DIP-6.
- DIP-8 (architecture) ← DIP-3, DIP-7.
- DIP-13/14/15 (prototype) ← DIP-7 (stack decision), DIP-8.
- DIP-10 (evaluation) ← DIP-3.
- DIP-16 (tag) ← all pre-defense 1 tasks reviewed and merged.
- External: supervisor availability for DIP-12; YouTrack instance access; 3D model sources (R1).

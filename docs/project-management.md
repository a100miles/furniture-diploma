# Project Management and Risks

**Task:** DIP-11 · **Status:** draft for pre-defense 1 (24 October 2026)

## 1. Tools and links

| Item | Link |
|------|------|
| Git repository | https://github.com/a100miles/furniture-diploma |
| YouTrack project (key `DIP`) | https://furniture-diploma.youtrack.cloud/projects/DIP |
| Backlog import file | [`project-management/youtrack-backlog.csv`](../project-management/youtrack-backlog.csv) |

**YouTrack setup (one-time).** Create project with key `DIP`, add all three team members and the supervisor, then *Import → CSV* the backlog file (columns map to Summary, Assignee, Priority, Due Date, Description). Task numbers will then match the IDs used in this repository (DIP-1 … DIP-31). For each task add the acceptance criteria from the CSV and, when done, a link to the pull request.

## 2. Working process

- `main` is the reviewed baseline. Nobody pushes to `main` directly.
- One branch per task: `DIP-<n>-short-name` (e.g. `DIP-14-room-editor`).
- Commit messages start with the task ID: `DIP-14: Add drag-to-move for furniture`.
- Each change goes through a pull request that (1) explains the change, (2) references the YouTrack task, (3) says how it was checked. Another team member reviews before merge.
- Each student commits from their own GitHub account with their real name and university e-mail in `git config user.name / user.email`.
- Weekly team meeting with the supervisor (in person or MS Teams): review of completed tasks, demo, agreement on next steps; comments and decisions recorded in `supervisor-feedback.md`.
- Two-week iterations in YouTrack; every task has an owner, expected result, acceptance criteria and deadline.
- If the plan slips, tasks are redistributed at the next weekly meeting; the riskiest parts (data quality, 3D performance, recommendation accuracy) are prototyped early.
- The current committee snapshot is tagged `prob-period-1`. Give each future snapshot a new immutable tag, with its name agreed before that checkpoint.

## 3. Allocation of responsibilities

| Member | Role | Responsibilities |
|--------|------|------------------|
| **Tamerlan Yessimov** | Team lead; ML developer | Coordination (YouTrack, task breakdown, deadlines, code review on GitHub, pre-defense materials); ML recommendation service: CLIP embeddings of images and descriptions, style-similarity search, ranking by room size, budget and already chosen furniture, natural-language query parsing, experimental evaluation (Precision@K, nDCG@K vs. baseline) |
| **Sultanbek Zhumagali** | Backend developer | System architecture and API contracts (OpenAPI); Go core API; catalogue parsers for Kazakhstan stores (mebel.kz and others) and data normalisation; database schema; layout module (placement validation, automatic arrangement); Docker, CI, demo stand |
| **Muzaffar Kapezov** | Frontend and 3D developer | UX research, 3–5 user interviews, prototypes of key scenarios; web client (catalogue, product card, account with projects); 3D editor (room by dimensions, doors and windows, drag/rotate, wall snapping, top-down and free camera); glTF/GLB optimisation (Draco, LOD), parametric models; rendering performance and browser checks |

Integration is through shared API contracts and cross-review of pull requests.

### Individual deliverables per checkpoint

| Member | Pre-defense 1 (24 Oct 2026) | Pre-defense 2 | Final pre-defense |
|--------|-----------------------------|---------------|-------------------|
| Tamerlan | Literature review (recommender systems, multimodal search), README, YouTrack tasks, evaluation plan | Baseline and first ML ranker with measured metrics | Improved model, comparison with baseline, integration |
| Muzaffar | Prototypes of key scenarios, use case diagram, user interviews, comparison of 3D libraries | 3D editor with room building and furniture placement | Rendering optimisation, parametric models, UX testing |
| Sultanbek | Component diagram, database schema, backend and storage technology comparison, first catalogue data | Catalogue and projects API, placement validation module | Automatic layout, load tests, deployment |

## 4. Backlog (pre-defense 1 scope and next steps)

| ID | Task | Owner | Priority | Due | Acceptance criteria |
|----|------|-------|----------|-----|---------------------|
| DIP-1 | Repository structure, README, .gitignore, config example | Tamerlan | Critical | 21 Oct | README covers all items from the guidelines; structure has src/docs/diagrams/tests/config |
| DIP-2 | Project proposal and scope | Tamerlan | Critical | 22 Oct | Title, team, supervisor, problem, users, aim, objectives, outcomes, scope present |
| DIP-3 | Requirements specification (FR/NFR, priorities, acceptance criteria) | Tamerlan | Critical | 22 Oct | Every mandatory requirement has a verifiable acceptance criterion |
| DIP-4 | Evidence of relevance: 3–5 interviews | Muzaffar | Critical | 23 Oct | ≥ 3 interview records; findings table filled; assumptions separated |
| DIP-5 | Literature review (recommender systems, multimodal search, layout) | Tamerlan | Critical | 22 Oct | ≥ 12 sources, ≥ 8 scientific, analysis table, synthesis |
| DIP-6 | Existing system comparison | Muzaffar | Critical | 22 Oct | 3–5 systems × 6–10 criteria; hands-on evidence for each claim |
| DIP-7 | Technology comparison (3D libraries; server platform, storage, interaction) | Sultanbek | Critical | 22 Oct | ≥ 3 decisions × 2–3 alternatives, justified by requirements; 3D library section by Muzaffar |
| DIP-8 | Architecture description and diagrams (context, use case, component) | Sultanbek | Critical | 23 Oct | Editable sources + exports in `docs/diagrams/`; use case diagram by Muzaffar |
| DIP-9 | UX prototypes of key scenarios | Muzaffar | Critical | 23 Oct | Room setup, selection, placement, saving covered; prototype runs locally |
| DIP-10 | Verification and evaluation plan | Tamerlan | Critical | 22 Oct | Test plan, metrics (incl. nDCG@10), conditions, baseline defined |
| DIP-11 | Project management, YouTrack, risks | Tamerlan | Critical | 21 Oct | YouTrack populated; risks and milestones documented |
| DIP-12 | Supervisor review of pre-defense 1 package | Tamerlan | Critical | 23 Oct | Feedback recorded with decisions in `supervisor-feedback.md` |
| DIP-13 | Prototype API: catalogue and recommendation endpoints | Sultanbek | High | 23 Oct | `/api/catalog`, `/api/recommendations` with tests passing |
| DIP-14 | 3D room editor prototype | Muzaffar | High | 23 Oct | Room setup, add/move/rotate/remove furniture in 3D |
| DIP-15 | Layout module v1: validation and rule-based auto-layout | Sultanbek | High | 23 Oct | No overlaps/out-of-bounds on test rooms; unit tests |
| DIP-16 | Tag `prob-period-1` and matching submission summary | Tamerlan | Critical | 24 Oct | Tag points to the committee snapshot; summary matches the tagged tree and records open tasks |
| DIP-17 | PostgreSQL persistence for users, rooms, projects (FR-08) | Sultanbek | High | Nov | Projects persist across restarts; versioned migrations |
| DIP-18 | glTF/GLB models with Draco and LOD | Muzaffar | High | Nov | Models load < 1 s each; licences recorded |
| DIP-19 | Walkways, door and window constraints in layout (FR-39, FR-40) | Sultanbek | High | Nov | Clearance violation rate ≤ 5 % on benchmark |
| DIP-20 | Layout benchmark set and baselines | Sultanbek | High | Dec | 30 rooms; metrics script reproducible |
| DIP-21 | Recommendation evaluation set and baseline B1 | Tamerlan | High | Dec | ≥ 50 labelled queries; Precision@K and nDCG@10 for B1 reported |
| DIP-22 | CI pipeline (lint, tests) on GitHub Actions | Sultanbek | Medium | Nov | Every PR runs tests |
| DIP-23 | Usability study | Muzaffar | High | per schedule | 8–12 participants, SUS and task metrics reported |
| DIP-24 | Top-down camera, wall snapping, windows in 3D editor | Muzaffar | High | Nov | Plan view and snapping work; windows rendered as openings |
| DIP-25 | Catalogue parsers for Kazakhstan stores (mebel.kz and others) | Sultanbek | Critical | 23 Oct | First catalogue data loaded; robots.txt and rate limits respected; ≥ 5 000 items by pre-defense 2 |
| DIP-26 | Go core API skeleton (hexagonal architecture, OpenAPI contract) | Sultanbek | High | Nov | Catalogue search endpoint with p95 < 300 ms on 5 000 items |
| DIP-27 | Database schema | Sultanbek | Critical | 23 Oct | ER diagram with editable source; covers users, rooms, projects, catalogue, embeddings |
| DIP-28 | CLIP image/text embeddings in pgvector | Tamerlan | High | Dec | Embeddings for all items with images; similar-item search endpoint |
| DIP-29 | Natural-language query parsing into filters | Tamerlan | Medium | Jan | ≥ 80 % of a 30-query test set parsed into correct filters |
| DIP-30 | Docker Compose with Redis and MinIO; demo stand | Sultanbek | Medium | Dec | `docker compose up` starts all services |
| DIP-31 | Parametric 3D models from catalogue dimensions | Muzaffar | High | Dec | Bounding box matches catalogue dimensions within 1 cm |

## 5. Milestones

| Milestone | Target date | Content |
|-----------|-------------|---------|
| M1 · Pre-defense 1 | **24 Oct 2026** | Proposal and scope, literature review, existing systems and technology comparison, requirements with acceptance criteria, context / use case / component diagrams, database schema, UI prototypes, evaluation plan, first catalogue data; snapshot tag `prob-period-1` |
| M2 · Pre-defense 2 (MVP) | per university schedule | Catalogue (≥ 5 000 items), 3D editor, basic layout, first version of recommendations; tag name to be agreed before the checkpoint |
| M3 · Final pre-defense | per university schedule | Full system, test results and metrics, thesis text; tag name to be agreed before the checkpoint |

## 6. Risks

| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|:-----------:|:------:|------------|-------|
| R1 | 3D models of real furniture are unavailable or have restrictive licences | High | High | Parametric models from catalogue dimensions for every item; start with parametric box/low-poly models; use CC0 sources (e.g. Poly Haven, Kenney); record licence per model | Muzaffar |
| R2 | WebGL performance too low on weak laptops | Medium | Medium | Low-poly models, instancing, limit shadows; measure NFR-01 early | Muzaffar |
| R3 | AI scope creep (training ML models takes too long) | High | High | Use pretrained open-source CLIP models (integration, not training from scratch); rule-based baseline first; LLM optional | Tamerlan |
| R4 | Not enough interview participants before 24 Oct | Medium | High | Recruit from 3 channels (university, stores, designers); online calls allowed | All |
| R5 | Uneven contributions visible in Git history | Medium | High | Task ownership in YouTrack; each member commits own work from own account | Tamerlan |
| R6 | Dependency on external LLM API (cost, availability, keys) | Medium | Medium | LLM is optional; keys only in `.env`, never in repo; fallback to rules | Tamerlan |
| R7 | Catalogue data quality: missing or inconsistent dimensions, stores change their HTML or block parsers | High | High | Normalisation rules with rejected-row reports; several stores; dated prices; polite parsing (robots.txt, rate limits); early prototype | Sultanbek |
| R8 | Team member unavailable (illness, exams) | Medium | Medium | Documented code, PR reviews spread knowledge, secondary owner per area | All |
| R9 | Two-service architecture (Go + Python) slows integration | Medium | Medium | OpenAPI contract first; contract tests; prototype REST contract kept | Sultanbek |

## 7. Dependencies

- DIP-3 (requirements) ← DIP-4 (interview findings), DIP-5, DIP-6.
- DIP-8 (architecture) ← DIP-3, DIP-7.
- DIP-13/14/15 (prototype) ← DIP-7 (stack decision), DIP-8.
- DIP-21, DIP-28 (recommendation quality) ← DIP-25 (catalogue data), DIP-27 (schema).
- DIP-26 (Go core API) ← DIP-27, DIP-8.
- DIP-10 (evaluation) ← DIP-3.
- DIP-16 (tag) ← all pre-defense 1 tasks reviewed and merged.
- External: supervisor availability for DIP-12; YouTrack instance access; 3D model sources (R1).

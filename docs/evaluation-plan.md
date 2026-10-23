# Verification and Evaluation Plan

**Task:** DIP-10 · **Status:** draft for pre-defense 1 (24 October 2026)

The plan shows **how the project aim will be demonstrated**: the system helps a non-expert choose furniture that fits their room, style and budget, and arrange it validly in 3D, faster and with more confidence than without the system.

Requirement IDs (FR-xx, NFR-xx) refer to `requirements.md`.

## 1. Levels of verification

| Level | What | Tool | When | Pass criterion |
|-------|------|------|------|----------------|
| Unit tests | Recommendation scoring, constraint filters, layout solver, geometry (overlap, bounds) | `go test` (core API), `pytest` (ML service, prototype), `vitest` (web client) | Every commit (CI) | 100 % of tests pass; ≥ 60 % line coverage of recommendation and layout code (NFR-06) |
| API / integration tests | REST endpoints with real request/response schemas; OpenAPI contract tests between core API and ML service | `go test` + `httptest`, `pytest` + FastAPI `TestClient` | Every commit (CI) | All endpoints return documented schema; invalid input → HTTP 422 |
| End-to-end tests | Key user scenarios in a real browser | Playwright | Before each pre-defense | UC-01…UC-06 complete without errors |
| Performance tests | Rendering FPS, API latency | Browser performance panel, `pytest-benchmark` / `locust` | Milestones M2, M3 | NFR-01, NFR-02, NFR-08, NFR-09, NFR-35 targets met |
| Algorithm evaluation | Quality of recommendations and layouts vs. baseline | Offline benchmark script (`backend/tests/benchmark/`) | M2, M3 | See §3 |
| Usability study | Real users performing tasks | Moderated sessions, SUS questionnaire | M3 (before final pre-defense) | See §4 |

## 2. Requirement → verification mapping

| Requirement | Verification method | Metric / acceptance check |
|-------------|---------------------|---------------------------|
| FR-01 Room setup | Unit + E2E | Room with width/length/height 2–10 m accepted; out-of-range rejected |
| FR-02 3D view & navigation | E2E + manual | User can orbit, zoom, pan; room renders to scale |
| FR-03 Add / move / rotate / remove | E2E | Each operation reflected in scene and in project JSON |
| FR-04 Catalog browse/filter | API test | Filter by category, style, max price returns only matching items |
| FR-05 Recommendations | Unit + algorithm eval | 100 % of returned items satisfy hard constraints; ranking quality ≥ baseline (§3) |
| FR-06 Auto-layout | Unit + algorithm eval | 0 overlaps, 0 out-of-bounds, clearance satisfied in ≥ 95 % of benchmark rooms |
| FR-07 Validation | Unit | Overlap and out-of-bounds detected with 100 % accuracy on test cases |
| FR-08 Save / load | API + E2E | Saved project reloads identically (deep-equal JSON) |
| FR-09 Cost summary | Unit | Total equals sum of item prices; budget overrun flagged |
| NFR-01 Rendering performance | Performance test | ≥ 30 FPS with 30 items on reference laptop (integrated GPU, Chrome) |
| NFR-02 Recommendation latency | Performance test | p95 < 2 s over 100 requests on the MVP catalogue |
| NFR-08 Layout generation time | Performance test | First layout within 10 s for 15 items (p95 over the benchmark) |
| NFR-09 Editing feedback | Manual + browser profiler | Collision feedback within 100 ms while dragging, 30 items |
| NFR-03 Usability | Usability study | Mean SUS ≥ 68; task success ≥ 80 % |
| NFR-04 Compatibility | Manual matrix | Works in latest Chrome, Firefox, Edge, Safari |
| NFR-05 Security | Review + tests | No secrets in repo (secret scan); all inputs validated by schema |
| NFR-06 Maintainability | CI | Lint passes; tests run with one command |
| NFR-35 Catalogue search latency | Load test (k6) | p95 < 300 ms on ≥ 5 000 items, 20 virtual users |
| NFR-36 Recommendation quality | Offline evaluation (§3.4) | nDCG@10 of the ML ranker > baseline B1 |
| FR-31 Catalogue collection | Import report | ≥ 5 000 items from ≥ 2 stores; rejected rows logged |
| FR-57 Parametric models | Unit + visual check | Generated model matches catalogue dimensions within 1 cm for 20 sample items |

## 3. Algorithm evaluation against baselines

### 3.1 Benchmark set
- 30 synthetic rooms: 10 bedrooms, 10 living rooms, 10 home offices; sizes 2.5×3 m to 6×5 m; each with 1 door and 1–2 windows.
- Each room has a requested set of items (4–12) and a user profile (style, budget).
- Optional: 20 rooms sampled from 3D-FRONT (research licence) for realism.

### 3.2 Baselines

| Component | Baseline (what a user gets today without our AI) | Our method |
|-----------|---------------------------------------------------|-----------|
| Recommendation | **B1 – filter by category and price**: catalogue filtered by category and max price, cheapest first (typical e-shop) | Rule-based scorer (prototype), then CLIP-embedding ranker with room, budget and chosen-furniture constraints |
| Layout | **B2 – random valid placement**: items placed at random positions, retried until no overlap | Guideline-based solver (wall alignment, clearance, facing relations) |
| Layout | **B3 – manual placement** by participants in the usability study | Auto-layout then user edits |

### 3.3 Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Constraint satisfaction rate | % of recommended items that fit room and budget | 100 % (B1 is measured for comparison) |
| Precision@K (K = 5, 10) | Share of the top-K items judged relevant for the query | > B1 |
| nDCG@10 | Normalised discounted cumulative gain of the top-10 list against graded relevance labels (Järvelin & Kekäläinen, 2002) | > B1 (main recommendation metric) |
| Overlap rate | % of layouts with any pair of intersecting footprints | 0 % |
| Out-of-bounds rate | % of layouts with any item outside the room | 0 % |
| Clearance violation rate | % of layouts blocking door swing or with walkway < 0.6 m | ≤ 5 % and < B2 |
| Layout guideline score | Mean of normalised guideline terms (wall alignment, facing, spacing) | > B2 by ≥ 20 % |
| Expert rating | 2 interior design experts rate 10 layouts (ours vs. B2, blind, 1–5 Likert) | Ours > B2, Wilcoxon p < 0.05 |
| Latency | Server time per request | Recommendations p95 < 2 s; catalogue search p95 < 300 ms; first layout ≤ 10 s for 15 items |
| Rendering | Frame rate with 30+ objects | ≥ 30 FPS on a mid-range laptop |

### 3.4 Recommendation evaluation protocol

- **Evaluation set:** 50–100 queries built from realistic scenarios (room type, room size, style, budget, already chosen items, optional free-text request), each with a pool of candidate items from the real catalogue.
- **Relevance labels:** each candidate is graded 0–2 (not suitable / acceptable / good fit) by two team members independently, with an interior designer reviewing disagreements; agreement reported with Cohen's κ.
- **Systems compared:** B1 baseline (filter by category and price, cheapest first) → rule-based scorer (prototype) → CLIP-embedding ranker with constraints (final).
- **Metrics:** Precision@5, Precision@10, nDCG@10, constraint satisfaction rate; a paired test (Wilcoxon) over queries for nDCG@10.
- **Tooling:** Jupyter notebooks and scikit-learn metrics in the ML service repository folder; results committed as CSV with the notebook.

## 4. Usability study

- **Participants:** 10–12 target users (not the interviewees from `relevance-evidence.md` where possible).
- **Conditions:** within-subjects, counterbalanced: (A) catalog + manual 3D placement only, (B) full system with recommendations and auto-layout.
- **Tasks:** T1 set up a 4×3.5 m living room; T2 choose a sofa, coffee table and TV stand in a given style under a given budget; T3 arrange them so the room is usable; T4 save the project.
- **Measured:** task success, time on task, number of edits, SUS after each condition, decision confidence (1–7 "I am confident this furniture will fit and look good"), short interview.
- **Measurement conditions:** same mid-range laptop (integrated graphics, Chrome, 1920×1080, mouse), same catalogue snapshot, quiet room, think-aloud, sessions ≤ 40 min, consent form, anonymised data.
- **Success criteria for the aim:** in condition B vs. A — time on T2+T3 reduced by ≥ 25 %, decision confidence higher (paired test p < 0.05), SUS ≥ 68, zero invalid final layouts.

## 5. Threats to validity
- Small sample → report effect sizes and medians, not only p-values.
- Synthetic rooms may be easier than real ones → include 3D-FRONT rooms if licence allows.
- Catalog is curated by the team → style tags reviewed by an interior designer (P4).
- Learning effect between conditions → counterbalancing.

## 6. Schedule

| Milestone | Date | Evaluation activity |
|-----------|------|---------------------|
| M1 Pre-defense 1 | 24 Oct 2026 | Plan approved; unit tests for prototype running (35 backend tests in CI) |
| Checkpoint (between M1 and M2) | Dec 2026 | Benchmark set + baselines implemented; recommendation evaluation set labelled |
| M2 Pre-defense 2 (MVP) | per university schedule | Baseline and first ML ranker with measured nDCG@10; layout benchmark; performance tests |
| M3 Final pre-defense | per university schedule | Usability study results, full test report |

Milestones M1–M3 are the same as in `project-management.md`.

## References

- Järvelin, K., & Kekäläinen, J. (2002). Cumulated gain-based evaluation of IR techniques. *ACM Transactions on Information Systems, 20*(4), 422–446. https://doi.org/10.1145/582415.582418
- Brooke, J. (2013). SUS: A retrospective. *Journal of Usability Studies, 8*(2), 29–40. https://uxpajournal.org
- Bangor, A., Kortum, P., & Miller, J. (2009). Determining what individual SUS scores mean: Adding an adjective rating scale. *Journal of Usability Studies, 4*(3), 114–123. https://uxpajournal.org/wp-content/uploads/sites/7/pdf/JUS_Bangor_May2009.pdf

All references are open access; see `literature-review.md` [22], [23].

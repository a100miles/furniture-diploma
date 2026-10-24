# Arca: Web-Based System for AI-Assisted Furniture Selection and 3D Room Planning

**Diploma Project** · Astana IT University · Software Engineering, group SE-2420 · 2026–2027

*Thesis title: Development of a Web-Based System for AI-Assisted Furniture Selection and 3D Room Planning*

Arca is a web application that collects furniture from several Kazakhstan online stores into one catalogue, recommends furniture fitting a user's room, style and budget, explains each recommendation, arranges the furniture automatically without collisions, and lets the user refine the result in an interactive 3D view.

![Prototype: auto-arranged living room](docs/assets/prototype/03-auto-layout.png)

## Problem statement

People who buy furniture, especially online, often cannot tell whether an item will fit their room, how to arrange it, or whether the whole set stays within budget. Existing tools either show 3D/AR views without helping to *choose* (Planner 5D, HomeByMe), lock users into one retailer or brand catalogue (IKEA Kreativ, Roomle), or generate attractive images that ignore real dimensions (generative "AI interior" apps). None explains *why* an item is suggested, and none works with the assortment of local Kazakhstan furniture stores. See [existing systems comparison](docs/existing-systems.md) and [literature review](docs/literature-review.md).

## Target users

- **Primary:** people furnishing a flat or a room (students, young families, renters) without design experience.
- **Secondary:** furniture store consultants and interior designers working with clients; local furniture shops that gain 3D visualisation without modelling costs.

Evidence and open assumptions: [docs/relevance-evidence.md](docs/relevance-evidence.md).

## Expected outcomes

1. A working web system on a demo stand: unified catalogue of **≥ 5 000 items** from several local stores, room setup, explained AI recommendations, automatic valid layout, 3D editing, cost summary, saved projects.
2. Recommendation quality **nDCG@10 above the baseline** (filter by category and price); layouts with **no overlaps and clear walkways**.
3. A 3D scene of **30+ objects at ≥ 30 FPS** on a mid-range laptop; catalogue search API **p95 < 300 ms**.
4. A usability study showing reduced time and higher decision confidence compared with manual planning (SUS ≥ 68).

Details: [proposal](docs/proposal.md) · [evaluation plan](docs/evaluation-plan.md).

## Team and responsibilities

| Member | Responsibility (see [project management](docs/project-management.md#3-allocation-of-responsibilities)) |
|--------|--------------------------------------------------|
| Tamerlan Yessimov | Team lead; ML developer: AI furniture recommendation service (CLIP embeddings, ranking, natural-language queries, evaluation) |
| Sultanbek Zhumagali | Backend developer: system architecture and API contracts, Go core API, catalogue parsers and data, database, layout module, infrastructure |
| Muzaffar Kapezov | Frontend and 3D developer: web client and 3D room planner, UX research and prototypes, 3D assets |

**Supervisor:** Kashkimbayeva Nurzhamal

## Scope

**In scope:** rectangular and L-shaped rooms with doors and windows; unified catalogue (≥ 5 000 items) from several Kazakhstan stores with dimensions, materials, styles, prices and images; parametric 3D models for items without a seller model; recommendations with explanations (CLIP embeddings + constraints, natural-language requests); automatic layout with hard constraints (inside room, no overlap, door zone free); browser 3D editor; cost vs. budget; save/load.

**Out of scope:** photoreal rendering, AR on phones, room scanning, non-rectangular rooms (v1), checkout/payments, training large generative models.

## Current status (probation period 1 snapshot, 24 October 2026)

| Deliverable | Status |
|-------------|--------|
| Proposal, requirements, technology comparison | ✅ drafts — [proposal](docs/proposal.md), [requirements](docs/requirements.md), [technology comparison](docs/technology-comparison.md) |
| Literature review (24 scientific papers + 2 technical sources, all open access) | ✅ [docs/literature-review.md](docs/literature-review.md) |
| Existing systems (5 systems × 10 criteria) | ✅ draft; hands-on checks pending — [docs/existing-systems.md](docs/existing-systems.md) |
| Evidence of relevance | Five interviews transcribed and analysed; findings are preliminary, with participant profile, interview date, and consent-record gaps documented — [docs/relevance-evidence.md](docs/relevance-evidence.md) |
| Architecture and diagrams (context, use case, component) | ✅ [docs/architecture.md](docs/architecture.md), sources in [docs/diagrams/src](docs/diagrams/src) |
| Database schema | ✅ draft — [docs/database-schema.md](docs/database-schema.md) |
| First catalogue data (parsers) | ✅ mebel.kz parser: 4,084 items in 10 categories — [pipeline/](pipeline); second store and 5,000-item target remain for the MVP checkpoint; prototype still uses a 25-item demo catalogue |
| UX / prototype | ✅ runnable prototype — [docs/ux-prototype.md](docs/ux-prototype.md) |
| Verification and evaluation plan | ✅ [docs/evaluation-plan.md](docs/evaluation-plan.md) |
| Project management, risks, backlog | ✅ [docs/project-management.md](docs/project-management.md) |
| Supervisor feedback | Template ready — [docs/supervisor-feedback.md](docs/supervisor-feedback.md) |

**Prototype works today** (single Python service; the Go core API and Python ML service replace it, see [architecture](docs/architecture.md#prototype-vs-target-architecture)): room setup, 3D view, drag/rotate/remove, explained recommendations (25-item demo catalog), auto-layout, live validation, cost summary, save/load (in memory). **Known limitations:** demo catalog with illustrative prices; boxes instead of 3D models; 90° rotations only; projects lost on backend restart; walkway clearance is a soft rule.

## Technologies

| Layer | Choice |
|-------|--------|
| Web client | TypeScript, React, Vite, Three.js via React Three Fiber + drei, glTF/GLB with Draco |
| Core API | Go (net/http, hexagonal architecture), OpenAPI |
| ML service | Python, FastAPI, PyTorch, Hugging Face (CLIP), scikit-learn, Jupyter |
| Catalogue pipeline | Python parsers for Kazakhstan stores (e.g. mebel.kz) |
| Storage | PostgreSQL + pgvector, Redis, MinIO (S3-compatible) |
| Infrastructure | Docker Compose, GitHub Actions |
| Testing | Go tests, pytest, Vitest, Playwright, k6 |
| Diagrams | Mermaid (editable sources) |
| Prototype (probation period 1) | Python FastAPI single service + React/R3F client |

Justification: [docs/technology-comparison.md](docs/technology-comparison.md).

## Links

- **YouTrack:** https://furniture-diploma.youtrack.cloud/projects/DIP (backlog import file: [project-management/youtrack-backlog.csv](project-management/youtrack-backlog.csv))
- **Documentation:** [docs/](docs)
- **Architecture:** [docs/architecture.md](docs/architecture.md)

## Repository structure

```
backend/            prototype FastAPI service (to be split into Go core API + Python ML service)
  app/              API, recommender, layout solver, geometry, catalog
  data/             demo furniture catalog (JSON)
  tests/            pytest tests
pipeline/           catalogue parsers for Kazakhstan stores (Python)
  catalog_pipeline/ fetcher (robots.txt, rate limit), normalisation, store parsers
  data/             parsed catalogue (JSON) + import report
  tests/            pytest tests
frontend/           React + three.js 3D editor
  src/components/   UI and 3D scene
  src/lib/          API client, types, geometry (+ vitest tests)
docs/               proposal, requirements, reviews, comparisons, plans
  diagrams/src/     editable Mermaid sources
  diagrams/export/  SVG / PNG exports
  assets/           screenshots
project-management/ YouTrack backlog import
.env.example        configuration example (placeholders only)
```

## Setup and running

Requirements for the prototype: Python 3.11+, Node.js 20+.

```bash
# 1. Backend  (http://localhost:8000, API docs at /docs)
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload

# 2. Frontend (http://localhost:5173), in a second terminal
cd frontend
npm install
npm run dev
```

The frontend dev server proxies `/api` to the backend. Configuration options are listed in [.env.example](.env.example).

## Testing

```bash
cd backend && pytest          # 35 tests: geometry, recommender, layout, API
cd pipeline && pytest         # catalogue parser and robots.txt tests
cd frontend && npm test       # client geometry tests
cd frontend && npm run build  # type check + production build
```

## Contributing

- Branch per YouTrack task: `DIP-<n>-short-name`; use Conventional Commits with the ticket in a `Refs: DIP-<n>` footer (see [AGENTS.md](AGENTS.md)).
- Open a pull request explaining the change, the task, and how it was checked; another team member reviews before merging into `main`.
- Never commit secrets or personal data: use `.env` (ignored) based on `.env.example`.
- Current committee snapshot: [`prob-period-1`](docs/submissions/prob-period-1.md). Future snapshot tag names will be agreed for each checkpoint.

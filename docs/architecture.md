# Architecture Description

**Task:** DIP-8 · **Status:** draft for pre-defense 1 (24 October 2026)

Diagram sources (editable, [Mermaid](https://mermaid.js.org/)) are in [`diagrams/src/`](diagrams/src); readable exports (SVG + PNG) in [`diagrams/export/`](diagrams/export). To regenerate after editing: `npx -p @mermaid-js/mermaid-cli mmdc -i docs/diagrams/src/<name>.mmd -o docs/diagrams/export/<name>.svg`. They can also be edited in the browser at https://mermaid.live.

## 1. Architectural style

A **client–server web application** with a thin REST boundary:

- **Frontend (browser):** React single-page application; 3D rendering with three.js through React Three Fiber. Holds the editing state and gives instant feedback (client-side geometry checks while dragging).
- **Backend:** Python FastAPI service. Owns the catalog, the recommendation engine, the layout solver and the authoritative validation. Stateless per request except for project storage.
- **Storage:** PostgreSQL for catalog and projects (pgvector later for style embeddings); static/object storage for GLB models. *Prototype: JSON file catalog and in-memory projects; PostgreSQL arrives in DIP-17.*
- **Interaction:** REST/JSON over HTTPS, documented automatically with OpenAPI at `/docs`.

The "AI" components (recommendation engine, layout solver, optional natural-language adapter) sit behind narrow interfaces (`recommend(request)`, `auto_layout(request)`) so a learned or LLM-based model can replace the rule-based v1 without touching the API or the frontend (see `literature-review.md` §3.1).

## 2. System context

![System context](diagrams/export/01-system-context.svg)

| Actor / system | Interaction |
|----------------|-------------|
| Home user | Main user. Enters room and preferences, receives recommendations, arranges furniture in 3D. |
| Interior designer / seller | Uses the same functions with a client. |
| Catalog administrator | Maintains items, prices and 3D models (import in prototype; admin UI later). |
| Furniture retailer data (external) | Source of product data (dimensions, prices) via CSV/JSON import. |
| 3D model sources (external) | GLB models from retailers or CC0 libraries; licence recorded per model. |
| LLM API (external, optional) | Converts free-text wishes into layout constraints (DIP-24). The system works fully without it. |

## 3. Use cases

![Use case diagram](diagrams/export/02-use-case.svg)

| ID | Use case | Actor | Requirement | Prototype status |
|----|----------|-------|-------------|------------------|
| UC-01 | Set up room (dimensions, doors) | User | FR-01 | ✅ |
| UC-02 | View and navigate the room in 3D | User | FR-02 | ✅ |
| UC-03 | Browse and filter catalog | User | FR-04 | ✅ (category filter; API supports style and price) |
| UC-04 | Get AI furniture recommendations | User | FR-05 | ✅ rule-based v1 |
| UC-05 | Place / move / rotate / remove furniture | User | FR-03 | ✅ |
| UC-06 | Generate automatic layout | User | FR-06 | ✅ rule-based v1 |
| UC-07 | Validate layout (collisions, bounds, door) | System (included) | FR-07 | ✅ walkway clearance is soft in v1 |
| UC-08 | View cost summary vs. budget | User | FR-09 | ✅ |
| UC-09 | Save / load project | User | FR-08 | ✅ in-memory (DIP-17 adds DB) |
| UC-10 | Describe wishes in natural language | User, LLM API | (Could) | ⏳ DIP-24 |
| UC-11 | Manage catalog | Admin | — | ⏳ JSON file for now |

### Main scenario: UC-04 + UC-06 "Furnish my living room"

1. User enters room 4.0 × 3.5 m, door on the front wall, style *Scandinavian*, budget 600 000 ₸.
2. User presses **Recommend furniture** → `POST /api/recommendations`.
3. Backend filters the catalog by hard constraints (fits room, ≤ budget), scores the rest (style 50 %, size 30 %, price 20 %), returns top-3 per category with reasons, and a bundle that fits the budget.
4. User presses **Place set & auto-arrange** → `POST /api/layout` with the bundle.
5. Backend places items greedily (sofa → TV stand opposite → coffee table in front of sofa → armchair facing table → bookshelf in a corner), never violating hard constraints; returns placements and any items that did not fit.
6. Frontend renders the layout; user drags/rotates items; invalid positions turn red instantly; cost summary updates.
7. User saves the project → `POST /api/projects`.

**Alternative flows:** 3a — nothing in a category fits → category shown as empty with a message; 3b — budget cannot cover a full set → bundle marked "over budget"; 5a — no valid position for an item → listed as "not enough free space".

## 4. Components

![Component diagram](diagrams/export/03-component.svg)

| Component | Responsibility | Code |
|-----------|----------------|------|
| Room setup & panels UI | Forms for room and preferences; recommendation cards with reasons; catalog list; cost summary | `frontend/src/components/RoomForm.tsx`, `RecommendationPanel.tsx`, `CatalogPanel.tsx`, `CostSummary.tsx` |
| 3D Room Editor | Scene, walls, floor grid, door zones, furniture meshes, drag/rotate, invalid highlight | `frontend/src/components/Scene.tsx` |
| Project state store | Room, placed items, selection (React state in v1) | `frontend/src/App.tsx` |
| Client geometry | Instant validation and snapping while dragging (mirror of backend rules) | `frontend/src/lib/geometry.ts` |
| API client | Typed calls to the REST API | `frontend/src/lib/api.ts` |
| REST API layer | Routing, schema validation (Pydantic), OpenAPI | `backend/app/main.py`, `models.py` |
| Catalog service | Load and filter furniture | `backend/app/catalog.py` |
| Recommendation engine | Hard constraints, weighted scoring, explanations, budget bundle | `backend/app/recommender.py` |
| Layout solver | Candidate generation and guideline scoring, greedy placement | `backend/app/layout.py` |
| Geometry & validation | Footprints, overlap, bounds, door zone | `backend/app/geometry.py` |
| Project service | Save/load projects | `backend/app/main.py` (in-memory) |

## 5. Data model (initial)

```
FurnitureItem(id, name, category, styles[], width, depth, height, price, color, against_wall, [model_url])
Room(width, length, height, doors[Door(wall, offset, width)])
Placement(item_id, x, z, rotation ∈ {0, 90, 180, 270})
Project(id, name, room, placements[], style, budget)
```

Coordinates: floor rectangle [0, width] × [0, length] in metres; rotation 0° means the item's front faces +z (back against the z = 0 wall), matching three.js `rotation.y`.

## 6. API (prototype)

| Method & path | Purpose | Requirement |
|---------------|---------|-------------|
| `GET /api/health` | Liveness | — |
| `GET /api/catalog?category=&style=&max_price=` | Filtered catalog | FR-04 |
| `GET /api/catalog/categories` | Category list | FR-04 |
| `GET /api/catalog/{id}` | One item | FR-04 |
| `POST /api/recommendations` | Ranked, explained recommendations + budget bundle | FR-05, FR-09 |
| `POST /api/layout` | Automatic layout | FR-06, FR-07 |
| `POST /api/validate` | Validate a user's layout | FR-07 |
| `POST /api/projects`, `GET/PUT /api/projects/{id}` | Save / load | FR-08 |

Example request/response pairs are in [`ux-prototype.md`](ux-prototype.md#api-examples).

## 7. Consistency check (requirements ↔ use cases ↔ components)

| Requirement | Use case | Components |
|-------------|----------|------------|
| FR-01 | UC-01 | RoomForm, Room model |
| FR-02 | UC-02 | 3D Room Editor |
| FR-03 | UC-05 | 3D Room Editor, state store |
| FR-04 | UC-03 | CatalogPanel, Catalog service |
| FR-05 | UC-04 | RecommendationPanel, Recommendation engine |
| FR-06 | UC-06 | Layout solver |
| FR-07 | UC-07 | Geometry & validation (backend), client geometry |
| FR-08 | UC-09 | Project service |
| FR-09 | UC-08 | CostSummary, Recommendation engine (bundle) |

## 8. Architectural decisions (summary)

| ADR | Decision | Reason | Alternatives (see `technology-comparison.md`) |
|-----|----------|--------|-------------------------------------|
| ADR-1 | Rule-based recommender and layout first; ML/LLM later behind same interface | No training data or user history (cold start); validity and explainability required | Learned scene synthesis (ATISS, DiffuScene), LLM-only |
| ADR-2 | Hard constraints enforced by a deterministic solver, never by the AI proposal itself | Generative methods do not guarantee validity | Trust model output, post-filter |
| ADR-3 | Validation duplicated client-side for instant feedback; backend is authoritative | Dragging needs < 16 ms feedback | Server-only validation |
| ADR-4 | Axis-aligned footprints with 90° rotation in v1 | Simpler, exact geometry; covers most real layouts | Free rotation with oriented boxes (later) |

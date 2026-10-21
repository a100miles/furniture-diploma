# Project Proposal

**Title:** Development of a Web-Based System for AI-Assisted Furniture Selection and 3D Room Planning
**Product name:** Arca
**Programme / group:** Software Engineering, SE-2420

**Team:** Tamerlan Yessimov, Sultanbek Zhumagali, Muzaffar Kapezov
**Supervisor:** Kashkimbayeva Nurzhamal
**Task:** DIP-2

> Status: draft for review by the team and supervisor. The stack (React + React Three Fiber web client, Go core API, Python ML service, PostgreSQL + pgvector, Redis, MinIO, REST/JSON) is justified in [technology-comparison.md](technology-comparison.md).

---

## 1. Problem Statement

Buying furniture is a high-cost, low-confidence decision. People typically choose items from flat product photos and a list of dimensions, then discover after delivery that a sofa blocks a doorway, a wardrobe does not fit under a sloped ceiling, or the colours and styles clash with the rest of the room.

Existing tools fall into two groups:

- **Professional CAD and interior-design software** (e.g. SketchUp, Planner 5D, Roomstyler) is powerful but requires time to learn, and leaves all design decisions to the user.
- **Retailer configurators and AR apps** (e.g. IKEA Kreativ, Roomle, Wayfair "View in Room") are easy to use but are tied to one brand's catalogue or require manual modelling, and do little to suggest *what* to buy or *where* to put it.

None of these tools works with the assortment of **local furniture stores in Kazakhstan**. A buyer comparing sofas from several local shops has no way to try them in their own room.

Neither group answers the question most non-expert users actually have: *"Given my room and my taste, what should I buy and how should I arrange it?"*

## 2. Target Users

| User group | Need |
|---|---|
| People furnishing a new or rented flat (students, young families) | Choose affordable furniture that fits the space without design expertise |
| Homeowners renovating a single room | Try alternative arrangements and styles before buying |
| Small furniture shops and interior consultants | Show clients how items would look and fit in their room |

The primary target is non-expert home users on a desktop browser. Shops and consultants are a secondary audience that motivates the catalogue and admin features.

## 3. Proposed Solution

A web application, **Arca**, that combines an **AI recommendation engine** with an **interactive 3D room planner**, on top of a **unified catalogue** collected from several Kazakhstan online furniture stores (e.g. mebel.kz), with dimensions, materials, colour, price and images normalised into one schema:

1. The user describes the room: dimensions, doors, windows and fixed elements, either by entering measurements or by drawing the floor plan in the browser.
2. The user states preferences: room purpose (bedroom, living room, office...), aesthetic style (Scandinavian, minimalist, loft, classic...), budget and must-have items.
3. The system **recommends furniture** from the catalogue that fits the style, budget and physical space, using image and text embeddings (CLIP-family models) for style similarity with items already chosen, and explains why each item was chosen. Requests can also be written in natural language ("a light sofa under 300 000 tenge, up to 2 m wide").
4. The system **generates one or more layouts** that place the recommended furniture in the room while respecting clearances, walkways and ergonomic rules.
5. Items without a 3D model from the seller are shown as **parametric 3D models generated from their catalogue dimensions**, so any product can be placed in the room.
6. The user **explores and edits the result in 3D**: walks around the room, moves, rotates and swaps items, and immediately sees collisions and rule violations.
7. The user saves the design, compares alternatives and exports a shopping list.

## 4. Aim and Objectives

**Aim:** to design, implement and evaluate a web-based system that helps non-expert users choose furniture and plan room layouts by combining AI-generated suggestions with interactive 3D visualisation.

**Objectives:**

1. Review existing room-planning systems and research on automatic furniture layout and recommender systems ([literature-review.md](literature-review.md), [existing-systems.md](existing-systems.md)).
2. Specify functional and non-functional requirements ([requirements.md](requirements.md)).
3. Compare and select technologies for 3D rendering, backend, data storage and AI ([technology-comparison.md](technology-comparison.md)).
4. Build a unified furniture catalogue of at least 5 000 items from several Kazakhstan stores, with normalised dimensions, style tags, prices, images and 3D or parametric models.
5. Implement a recommendation module that selects items by style, budget, room type and available space.
6. Implement a layout-generation module that places items according to spatial and ergonomic constraints.
7. Implement a browser-based 3D editor for viewing and adjusting the room.
8. Evaluate the system through usability testing and layout-quality metrics ([evaluation-plan.md](evaluation-plan.md)).

## 5. Scope

### In scope

- Single rectangular and L-shaped rooms, with doors, windows and fixed obstacles (radiators, columns).
- A unified catalogue of at least 5 000 items collected by parsers from several Kazakhstan online furniture stores (respecting robots.txt and rate limits), across common categories (seating, tables, beds, storage, lighting, decor); a curated subset is tagged by style and has 3D models.
- Style-, budget- and space-aware recommendations with short natural-language explanations.
- Automatic layout generation with constraint checking (collisions, clearances, door swing, walkways).
- Interactive 3D view and editing in a desktop browser.
- User accounts, saved projects and shopping-list export.

### Out of scope (possible future work)

- Whole-apartment, multi-room planning.
- Real-time integration with retailers' stock and checkout.
- Room scanning from phone cameras or LiDAR.
- Photorealistic offline rendering.
- Native mobile and AR applications.

## 6. Proposed Approach

### 6.1 System architecture

| Layer | Responsibility | Technologies | Owner |
|---|---|---|---|
| Web client | Catalogue, product card, account with projects, room input, 3D scene and editing | TypeScript, React, Vite, Three.js / React Three Fiber, glTF + Draco | Muzaffar Kapezov |
| Core API | Catalogue search and filtering, users, rooms and projects, layout validation and automatic arrangement; REST/JSON with an OpenAPI contract | Go (net/http, hexagonal architecture) | Sultanbek Zhumagali |
| Catalogue data pipeline | Parsers for Kazakhstan furniture stores, cleaning and normalisation | Python | Sultanbek Zhumagali |
| ML service | CLIP image/text embeddings, style-similarity search, ranking under room, budget and chosen-furniture constraints, natural-language query parsing | Python, FastAPI, PyTorch, Hugging Face, scikit-learn | Tamerlan Yessimov |
| Storage | Users, rooms, projects, catalogue, item embeddings; cache; images and 3D models | PostgreSQL + pgvector, Redis, MinIO (S3-compatible) | Sultanbek Zhumagali |
| Infrastructure | Containers, CI with automated tests, demo stand | Docker Compose, GitHub Actions | Sultanbek Zhumagali |

### 6.2 AI components

- **Preference understanding.** Users may describe what they want in free text ("a cosy reading corner, light wood, under 300 000 KZT"). A language model converts this into structured preferences (style, colours, materials, budget, required items).
- **Furniture recommendation.** Each catalogue item is tagged with style, colour, material, category and dimensions. Items are scored by style similarity, budget fit and whether they physically fit the room, then combined into a coherent set (e.g. one sofa, one coffee table, matching chairs).
- **Layout generation.** Placement (in the core API) is treated as an optimisation problem. The cost function rewards wall alignment, functional groupings (sofa facing TV, bedside tables beside the bed), and penalises collisions, blocked doors and windows, and walkways narrower than a minimum width. This follows approaches described in the literature on automatic furniture arrangement (e.g. Merrell et al., 2011; Yu et al., 2011).
- **Explanations.** Every recommendation and layout comes with a short reason, so the user understands and can override the system's choices.

### 6.3 3D visualisation

The room is generated procedurally from the user's floor plan, and furniture is loaded as glTF models at real scale. The user can orbit, switch to a top-down plan view, drag and rotate items with snapping, and see constraint violations highlighted in real time.

## 7. Expected Outcomes

- A working web application (Arca) deployed on a demonstration stand and accessible from a browser.
- A unified catalogue of at least 5 000 items from several local stores, with parametric 3D models for items without a seller model.
- An ML recommendation service with nDCG@10 above the baseline (filter by category and price), and a layout module that produces arrangements with no overlaps and with walkways kept clear.
- A 3D planner that keeps a scene of 30+ objects at 30 FPS or more on a mid-range laptop, and a catalogue search API with p95 response time under 300 ms.
- An evaluation report comparing AI-generated layouts with manual ones and measuring usability.
- Diploma thesis and supporting documentation in this repository.

## 8. Novelty and Contribution

The project integrates things usually found separately: a **unified catalogue of local Kazakhstan stores**, catalogue-independent furniture **recommendation** by style compatibility with already chosen items and by the real room size, constraint-based automatic **layout generation**, and **interactive 3D editing** with live feedback, in a lightweight browser tool aimed at non-experts. Parametric models built from catalogue dimensions let users place any product, even when the seller provides no 3D model. Explanations for every suggestion make the AI's decisions transparent and easy to override.

## 9. Engineering Complexity

The project goes beyond a CRUD web application in five areas, each a substantial piece of engineering:

1. **Constrained layout optimisation.** Placing 10 to 15 items in a polygonal room is a combinatorial search over positions and rotations under hard constraints (no collisions, clear doors and walkways) and soft ones (functional groupings, wall alignment). It requires geometric collision detection, an occupancy-grid path check, a weighted cost function and a stochastic optimiser that returns a result within 10 seconds.
2. **Multi-criteria recommendation.** Selecting a *set* of items, not single items, means optimising style coherence, budget and physical fit together, closer to a constrained knapsack problem than to simple ranking.
3. **Real-time 3D editing in the browser.** Procedural room geometry, real-scale glTF assets, direct manipulation with snapping, and live constraint feedback within 100 ms, while keeping 30 FPS on integrated graphics.
4. **Data collection and normalisation** from several heterogeneous store websites into one schema (dimensions, materials, colours, prices), with deduplication and periodic updates.
5. **Distributed architecture:** web client, Go core API and Python ML service with a shared API contract, PostgreSQL + pgvector, Redis cache and S3-compatible storage.
6. **LLM integration with graceful degradation.** Turning free text into validated structured preferences and generating explanations, while keeping core features working when the LLM is unavailable.

Each area is backed by measurable acceptance criteria in [requirements.md](requirements.md).

## 10. Evaluation (summary)

Details are in [evaluation-plan.md](evaluation-plan.md). Planned measures:

- **Usability:** System Usability Scale (SUS) questionnaire (target 68 or higher, NFR-03) and task-completion time with 10 to 20 participants.
- **Layout quality:** share of generated layouts with no constraint violations; participant ratings of generated layouts versus layouts they arrange manually.
- **Recommendation relevance:** Precision@K and nDCG@10 against the baseline (filter by category and price), plus participant ratings of how well suggested items match the stated style and budget.
- **Performance:** layout-generation time, catalogue search latency (p95 < 300 ms) and 3D frame rate (30+ objects at 30 FPS or more) on typical hardware.

## 11. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Lack of free, consistent 3D furniture models | High | Use permissively licensed sources (e.g. Sketchfab CC models, Poly Haven), normalise scale, keep the catalogue small but complete |
| Layout optimisation is slow or produces poor layouts | High | Start with rule-based placement, add optimisation incrementally, cap iterations, generate in the background |
| LLM cost, latency or availability | Medium | LLM only for parsing and explanations; core recommendation works without it; cache responses |
| 3D performance on low-end laptops | Medium | Low-poly models, level of detail, compressed textures, frame-rate target in requirements |
| Scope creep within the diploma timeline | High | Fixed MVP scope (Section 4), features beyond it moved to future work |
| Uneven workload across the team | Medium | Clear module ownership and task tracking ([project-management.md](project-management.md)) |

## 12. Team Roles

| Member | Role | Primary area |
|---|---|---|
| Tamerlan Yessimov | Team lead; ML developer | Project coordination (YouTrack, code review, pre-defense materials); ML recommendation service: CLIP embeddings, ranking under room, budget and already-chosen-furniture constraints, natural-language query parsing, experimental evaluation |
| Sultanbek Zhumagali | Backend developer | System architecture and API contracts (OpenAPI); Go core API; catalogue parsers and data normalisation; database schema; layout module (placement validation and automatic arrangement); Docker, CI, demo stand |
| Muzaffar Kapezov | Frontend and 3D developer | UX research, interviews and prototypes; web client (catalogue, product card, account with projects); 3D editor (room, doors and windows, drag/rotate, wall snapping, top-down and free camera); glTF/Draco optimisation, LOD, parametric models; rendering performance |

## 13. Timeline (high level)

Detailed plan in [project-management.md](project-management.md).

| Phase | Deliverables |
|---|---|
| 1. Research and specification | Proposal, requirements, literature review, existing-systems analysis, technology comparison |
| 2. Design | Architecture, data model, UI wireframes, catalogue structure |
| 3. MVP implementation | Room input, catalogue, 3D view, basic rule-based recommendation and layout |
| 4. AI enhancement | Optimisation-based layout, style-aware ranking, natural-language preferences, explanations |
| 5. Evaluation | User study, metrics, fixes |
| 6. Thesis and defence | Final report, presentation, demo |

## 14. References (initial)

- Merrell, P., Schkufza, E., Li, Z., Agrawala, M., Koltun, V. (2011). *Interactive Furniture Layout Using Interior Design Guidelines.* ACM Transactions on Graphics (SIGGRAPH).
- Yu, L.-F., Yeung, S.-K., Tang, C.-K., Terzopoulos, D., Chan, T. F., Osher, S. (2011). *Make It Home: Automatic Optimization of Furniture Arrangement.* ACM Transactions on Graphics (SIGGRAPH).
- Brooke, J. (1996). *SUS: A "quick and dirty" usability scale.* Usability Evaluation in Industry.
- Ricci, F., Rokach, L., Shapira, B. (eds.) (2015). *Recommender Systems Handbook.* Springer.

The full list will be maintained in [literature-review.md](literature-review.md).

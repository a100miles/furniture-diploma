# Project Proposal

**Title:** Development of a Web-Based System for AI-Assisted Furniture Selection and 3D Room Planning

**Team:** Tamerlan Yessimov, Sultanbek Zhumagali, Muzaffar Kapezov
**Supervisor:** Kashkimbayeva Nurzhamal
**Task:** DIP-2

> Status: draft for review by the team and supervisor. The assumed stack (React + React Three Fiber, Python FastAPI, PostgreSQL, REST/JSON) will be justified in [technology-comparison.md](technology-comparison.md).

---

## 1. Problem Statement

Buying furniture is a high-cost, low-confidence decision. People typically choose items from flat product photos and a list of dimensions, then discover after delivery that a sofa blocks a doorway, a wardrobe does not fit under a sloped ceiling, or the colours and styles clash with the rest of the room.

Existing tools fall into two groups:

- **Professional CAD and interior-design software** (e.g. SketchUp, Planner 5D, Roomstyler) is powerful but requires time to learn, and leaves all design decisions to the user.
- **Retailer configurators and AR apps** (e.g. IKEA Kreativ, Wayfair "View in Room") are easy to use but are tied to one catalogue and do little to suggest *what* to buy or *where* to put it.

Neither group answers the question most non-expert users actually have: *"Given my room and my taste, what should I buy and how should I arrange it?"*

## 2. Target Users

| User group | Need |
|---|---|
| People furnishing a new or rented flat (students, young families) | Choose affordable furniture that fits the space without design expertise |
| Homeowners renovating a single room | Try alternative arrangements and styles before buying |
| Small furniture shops and interior consultants | Show clients how items would look and fit in their room |

The primary target is non-expert home users on a desktop browser. Shops and consultants are a secondary audience that motivates the catalogue and admin features.

## 3. Proposed Solution

A web application that combines an **AI recommendation engine** with an **interactive 3D room planner**:

1. The user describes the room: dimensions, doors, windows and fixed elements, either by entering measurements or by drawing the floor plan in the browser.
2. The user states preferences: room purpose (bedroom, living room, office...), aesthetic style (Scandinavian, minimalist, loft, classic...), budget and must-have items.
3. The system **recommends furniture** from a catalogue that fits the style, budget and physical space, and explains why each item was chosen.
4. The system **generates one or more layouts** that place the recommended furniture in the room while respecting clearances, walkways and ergonomic rules.
5. The user **explores and edits the result in 3D**: walks around the room, moves, rotates and swaps items, and immediately sees collisions and rule violations.
6. The user saves the design, compares alternatives and exports a shopping list.

## 4. Aim and Objectives

**Aim:** to design, implement and evaluate a web-based system that helps non-expert users choose furniture and plan room layouts by combining AI-generated suggestions with interactive 3D visualisation.

**Objectives:**

1. Review existing room-planning systems and research on automatic furniture layout and recommender systems ([literature-review.md](literature-review.md), [existing-systems.md](existing-systems.md)).
2. Specify functional and non-functional requirements ([requirements.md](requirements.md)).
3. Compare and select technologies for 3D rendering, backend, data storage and AI ([technology-comparison.md](technology-comparison.md)).
4. Build a furniture catalogue with real dimensions, style tags, prices and 3D models.
5. Implement a recommendation module that selects items by style, budget, room type and available space.
6. Implement a layout-generation module that places items according to spatial and ergonomic constraints.
7. Implement a browser-based 3D editor for viewing and adjusting the room.
8. Evaluate the system through usability testing and layout-quality metrics ([evaluation-plan.md](evaluation-plan.md)).

## 5. Scope

### In scope

- Single rectangular and L-shaped rooms, with doors, windows and fixed obstacles (radiators, columns).
- A curated catalogue of roughly 100 to 300 furniture items across common categories (seating, tables, beds, storage, lighting, decor).
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

### 6.1 System architecture (provisional)

| Layer | Responsibility | Technologies (assumed) |
|---|---|---|
| Frontend | Room input, 3D scene, editing UI | React, TypeScript, React Three Fiber (Three.js) |
| Backend API | Projects, catalogue, users, orchestration of AI modules; REST/JSON | Python, FastAPI |
| Recommendation module | Select items by style, budget, size; explain choices | Content-based filtering over style embeddings, optionally an LLM for preference parsing and explanations |
| Layout module | Place items in the room under constraints | Rule-based placement plus optimisation (simulated annealing or genetic algorithm) over a cost function |
| Storage | Users, projects, catalogue metadata | PostgreSQL; object storage for glTF models and textures |

### 6.2 AI components

- **Preference understanding.** Users may describe what they want in free text ("a cosy reading corner, light wood, under 300 000 KZT"). A language model converts this into structured preferences (style, colours, materials, budget, required items).
- **Furniture recommendation.** Each catalogue item is tagged with style, colour, material, category and dimensions. Items are scored by style similarity, budget fit and whether they physically fit the room, then combined into a coherent set (e.g. one sofa, one coffee table, matching chairs).
- **Layout generation.** Placement is treated as an optimisation problem. The cost function rewards wall alignment, functional groupings (sofa facing TV, bedside tables beside the bed), and penalises collisions, blocked doors and windows, and walkways narrower than a minimum width. This follows approaches described in the literature on automatic furniture arrangement (e.g. Merrell et al., 2011; Yu et al., 2011).
- **Explanations.** Every recommendation and layout comes with a short reason, so the user understands and can override the system's choices.

### 6.3 3D visualisation

The room is generated procedurally from the user's floor plan, and furniture is loaded as glTF models at real scale. The user can orbit, switch to a top-down plan view, drag and rotate items with snapping, and see constraint violations highlighted in real time.

## 7. Expected Outcomes

- A working web application deployed and accessible from a browser.
- A furniture catalogue with 3D models and metadata.
- Recommendation and layout-generation modules with documented algorithms.
- An evaluation report comparing AI-generated layouts with manual ones and measuring usability.
- Diploma thesis and supporting documentation in this repository.

## 8. Novelty and Contribution

The project integrates three things usually found separately: catalogue-independent furniture **recommendation**, constraint-based automatic **layout generation**, and **interactive 3D editing** with live feedback, in a lightweight browser tool aimed at non-experts. Explanations for every suggestion make the AI's decisions transparent and easy to override.

## 9. Engineering Complexity

The project goes beyond a CRUD web application in four areas, each a substantial piece of engineering:

1. **Constrained layout optimisation.** Placing 10 to 15 items in a polygonal room is a combinatorial search over positions and rotations under hard constraints (no collisions, clear doors and walkways) and soft ones (functional groupings, wall alignment). It requires geometric collision detection, an occupancy-grid path check, a weighted cost function and a stochastic optimiser that returns a result within 10 seconds.
2. **Multi-criteria recommendation.** Selecting a *set* of items, not single items, means optimising style coherence, budget and physical fit together, closer to a constrained knapsack problem than to simple ranking.
3. **Real-time 3D editing in the browser.** Procedural room geometry, real-scale glTF assets, direct manipulation with snapping, and live constraint feedback within 100 ms, while keeping 30 FPS on integrated graphics.
4. **LLM integration with graceful degradation.** Turning free text into validated structured preferences and generating explanations, while keeping core features working when the LLM is unavailable.

Each area is backed by measurable acceptance criteria in [requirements.md](requirements.md).

## 10. Evaluation (summary)

Details are in [evaluation-plan.md](evaluation-plan.md). Planned measures:

- **Usability:** System Usability Scale (SUS) questionnaire (target 68 or higher, NFR-03) and task-completion time with 10 to 20 participants.
- **Layout quality:** share of generated layouts with no constraint violations; participant ratings of generated layouts versus layouts they arrange manually.
- **Recommendation relevance:** participant ratings of how well suggested items match the stated style and budget.
- **Performance:** layout-generation time and 3D frame rate on typical hardware.

## 11. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Lack of free, consistent 3D furniture models | High | Use permissively licensed sources (e.g. Sketchfab CC models, Poly Haven), normalise scale, keep the catalogue small but complete |
| Layout optimisation is slow or produces poor layouts | High | Start with rule-based placement, add optimisation incrementally, cap iterations, generate in the background |
| LLM cost, latency or availability | Medium | LLM only for parsing and explanations; core recommendation works without it; cache responses |
| 3D performance on low-end laptops | Medium | Low-poly models, level of detail, compressed textures, frame-rate target in requirements |
| Scope creep within the diploma timeline | High | Fixed MVP scope (Section 4), features beyond it moved to future work |
| Uneven workload across the team | Medium | Clear module ownership and task tracking ([project-management.md](project-management.md)) |

## 12. Team Roles (proposed)

To be confirmed by the team.

| Member | Primary area |
|---|---|
| Tamerlan Yessimov | TBD |
| Sultanbek Zhumagali | TBD |
| Muzaffar Kapezov | TBD |

Suggested split: 3D frontend and editor; backend, catalogue and data; AI recommendation and layout modules.

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

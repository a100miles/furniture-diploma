# Technology Comparison

This document compares candidate technologies for five key technical decisions: the browser 3D rendering library, the server platform, data storage, the way the frontend and backend communicate, and the AI approach for furniture recommendation and automatic room layout. Each decision lists two or three realistic alternatives, compares them against the project's criteria, and ends with a justified choice. The last section summarises the recommended stack.

The criteria in section 1 are derived from the README goals and the requirements document (`docs/requirements.md`), and each criterion is linked to the functional (FR-xx) and non-functional (NFR-xx) requirements it serves. YouTrack task: DIP-7.

## 1. Selection criteria

The options are judged against the needs of this project, not in general:

| # | Criterion | Why it matters here | Requirements |
|---|-----------|---------------------|--------------|
| C1 | Runs in a normal browser, desktop and mobile, with no install | The README requires a web-based system | NFR-04 |
| C2 | Fast loading and smooth rendering | Users open the planner from a link; the scene must stay at 30 FPS or more with 30 items | NFR-01, FR-02 |
| C3 | Integration with a regular web UI and 3D editing tools | Most screens are 2D UI (catalogue, filters, cost summary) around a 3D view where items are added, moved and rotated | FR-01, FR-03, FR-04, FR-09, NFR-03 |
| C4 | Fit with the team's skills and the diploma timeline | Three developers, one academic year | NFR-06 |
| C5 | Python interoperability for ML work, and server performance | ML models (CLIP embeddings, ranking) need Python libraries; catalogue search must answer in under 300 ms (p95) and recommendations in under 2 s | FR-05, FR-06, FR-07, NFR-02 |
| C6 | Licence and cost | Must be free for academic use and deployable on a student budget | — |
| C7 | Community, documentation, maintenance, security | Reduces risk when the team gets stuck; mature frameworks ship security fixes and auth tooling | NFR-05, NFR-06 |
| C8 | Data integrity and persistence | Room designs must save and load reliably; catalogue filtering must be exact | FR-04, FR-08 |
| C9 | Academic defensibility | The choice must be explainable and its results measurable in the evaluation plan | NFR-02, NFR-03 |

## 2. 3D web rendering

### 2.1 Options

**Three.js** is the most widely used WebGL library. It is a rendering library rather than a full engine: it provides scenes, cameras, materials, lights, loaders (glTF, OBJ, FBX) and a WebGPU renderer, and leaves application structure to the developer. MIT licence.

**react-three-fiber (R3F)** is a React renderer for Three.js. The 3D scene is written as React components, so the scene and the 2D UI share state and the same component model. The `@react-three/drei` helper library adds ready components that a room planner needs directly: orbit controls, transform gizmos (move/rotate handles), environment lighting, contact shadows, glTF loading with caching and HTML labels in 3D space. MIT licence.

**Babylon.js** is a full 3D engine for the web maintained by Microsoft. It includes physics integration, a GUI system, an inspector and node-based material editor, and strong WebXR support out of the box. Apache 2.0 licence. It is more "batteries included" than Three.js, with a smaller ecosystem and fewer React-oriented tools (a community `react-babylonjs` binding exists but is far less used than R3F).

**Unity WebGL** builds a Unity (C#) project to WebAssembly and WebGL. Unity has the best editor tooling and asset pipeline of the three, but the web is an export target rather than its native environment: builds are large, start-up is slow, the canvas is isolated from the surrounding web page (communication with JavaScript goes through a bridge), and mobile browser support has historically been limited. The free Personal licence covers a student project, but the runtime is proprietary.

### 2.2 Comparison

| Criterion | Three.js + R3F | Babylon.js | Unity WebGL |
|-----------|----------------|------------|-------------|
| C1 Browser and mobile support | Excellent; plain WebGL/WebGPU | Excellent | Weaker; heavy on mobile |
| C2 Initial load | Small (library is a few hundred KB; models load on demand) | Medium (larger engine bundle, tree-shakable) | Poor (multi-MB WebAssembly runtime before anything shows) |
| C3 Web UI integration | Native: the scene is React components sharing state with the UI | Good, but scene and UI live in separate worlds unless a binding is used | Poor: separate canvas, JS bridge for every interaction |
| C4 Team fit / learning curve | Requires JS/TS and React, which are needed for the UI anyway | One more framework to learn next to the UI framework | Requires C# and the Unity editor in addition to the web stack |
| Built-in editor features (gizmos, snapping, picking) | Via drei (`TransformControls`, `PivotControls`, raycasting) | Built in (gizmo manager, picking) | Built in, but must be bridged to the web UI |
| Physics / collision | Optional (Rapier via `@react-three/rapier`) | Built in (Havok plugin) | Built in |
| AR / WebXR | Available (`@react-three/xr`) | Strongest built-in support | Limited on web |
| Asset format | glTF/GLB (open standard) | glTF/GLB | Unity asset pipeline; glTF via plugins |
| C6 Licence | MIT | Apache 2.0 | Proprietary, free Personal tier |
| C7 Ecosystem | Largest; most tutorials, examples, and Stack Overflow answers | Good official docs and forum, smaller community | Huge for games, small for web-embedded apps |

### 2.3 Decision

**Three.js with react-three-fiber and drei** (FR-02, FR-03, NFR-01, NFR-04). A room planner is mostly a web application with a 3D view in it, not a game. Keeping the catalogue, filters, recommendation panels and the 3D scene in one React state tree removes a whole class of synchronisation bugs and lets every team member work in one language (TypeScript). Load time is the best of the three, which matters for a link-shared web tool. Babylon.js is a credible alternative and would be preferred if AR or physics became central requirements; Unity WebGL is rejected because of load size, mobile limitations and the bridge between the game canvas and the web UI.

Supporting choices:

- **Asset format:** glTF 2.0 / GLB, compressed with Draco or Meshopt, with textures in KTX2 where possible. glTF is an open Khronos standard supported by every option above, so the asset pipeline does not lock the project in.
- **Measurements:** the scene uses metres as world units so furniture dimensions from the catalogue map directly to geometry.
- **Floor-plan view:** a top-down orthographic camera in the same R3F scene gives the 2D plan without a second renderer.

## 3. Server platform

The server side has two different jobs: (1) the **core API** — catalogue search and filtering, users and projects, layout validation and automatic arrangement, which must be fast and reliable under concurrent use; and (2) the **ML part** — image/text embeddings, ranking and natural-language query parsing, which depends on the Python ML ecosystem (PyTorch, Hugging Face, scikit-learn). The options are therefore compared as whole server architectures.

### 3.1 Options

**A. Go core API + Python ML service.** The core API is written in Go (standard `net/http`, hexagonal architecture: domain logic separated from HTTP and database adapters). A separate Python FastAPI service hosts the ML models and is called by the core API over an internal REST interface. Go compiles to a single static binary, has built-in concurrency (goroutines) and low, predictable latency; the team's backend developer already has production-style Go projects (REST APIs with PostgreSQL, Redis, S3 storage, gRPC microservices).

**B. Python FastAPI monolith.** One FastAPI application serves the API and runs the ML code in the same process. Fastest to start and one language, but CPU-heavy model inference and geometry search share the same worker pool as ordinary API requests, and the Python GIL limits CPU parallelism inside a process.

**C. Node.js (NestJS/Fastify) core API + Python ML service.** Same split as A, but the core API is TypeScript, sharing types with the frontend. Node's single-threaded event loop is weaker for CPU-bound geometry checks (collision tests for 30+ objects, layout search), and the team has less backend experience in Node than in Go.

### 3.2 Comparison

| Criterion | A: Go API + Python ML | B: FastAPI monolith | C: Node API + Python ML |
|-----------|-----------------------|---------------------|-------------------------|
| C5 Access to Python ML ecosystem | Yes, in the ML service | Yes, same process | Yes, in the ML service |
| Latency / throughput of catalogue search (NFR: search p95 < 300 ms) | High: compiled, goroutines, low GC pauses | Medium: async I/O fine, CPU work blocks workers | Medium: async I/O fine, CPU work blocks the event loop |
| CPU-bound layout search and collision checks | Strong: native speed, parallel candidates | Weak without NumPy/vectorisation | Weak without worker threads |
| Isolation of ML failures and load | Yes: ML service can be restarted or scaled separately; core API degrades to baseline ranking | No: one process | Yes |
| Deployment | Single static binary + one Python container | One container | Node runtime + Python container |
| API documentation | OpenAPI written contract-first, served with the API | Generated automatically | Generated (NestJS Swagger) |
| C4 Team fit | Backend developer's main language; ML lead works only in Python | Python only | Less backend experience in the team |
| Complexity | Two services and an internal contract | Lowest | Two services |

### 3.3 Decision

**Option A: Go core API (net/http, hexagonal architecture) plus a Python FastAPI ML service.** The deciding factors are the performance targets (catalogue search under 300 ms at p95, interactive layout validation for 30+ objects), the CPU-bound nature of the layout search, and the team's skills: the backend developer works in Go, the ML developer in Python. Splitting the ML service off also lets the core system keep working with the baseline ranking (filter by category and price) if the ML service is unavailable. The extra cost — two services and an internal API contract — is controlled by writing the contract first in OpenAPI and testing both sides against it.

Supporting choices:

- **Caching:** Redis for hot catalogue queries and computed recommendation results.
- **Data collection:** catalogue parsers in Python (requests/BeautifulSoup, respecting `robots.txt` and rate limits) that normalise dimensions, materials, colour and price from Kazakhstan furniture stores (e.g. mebel.kz) and load them into PostgreSQL.
- **Deployment:** Docker Compose (web client, Go API, ML service, PostgreSQL, Redis, MinIO) for development and the demo stand; GitHub Actions for CI.
- **Prototype note:** the pre-defense 1 prototype in `backend/` is a single Python FastAPI service written to validate the recommendation and layout ideas quickly. Its recommender becomes the starting point of the ML service; the catalogue, project and layout endpoints are re-implemented in the Go core API (DIP-26, DIP-15).

## 4. Data storage

### 4.1 Options

The system stores three kinds of data with different shapes: a furniture **catalogue** (structured items with dimensions, prices, categories, style tags and model file references), **user accounts and saved room designs** (a room's geometry plus a list of placed items with positions and rotations), and **item embeddings** (vectors used for style similarity in the recommender, section 6). Large binary assets (3D models, textures) are a fourth kind, kept outside the database in every option.

**PostgreSQL** is a relational database with strong typing, transactions and foreign keys, plus a `jsonb` column type for document-shaped data and the `pgvector` extension for vector similarity search.

**MongoDB** is a document database. Room designs map naturally onto documents, and the schema can change without migrations. Relations (user → designs → catalogue items) must be managed in application code, and vector search is available in the managed Atlas service rather than in the self-hosted community edition in the same way.

**SQLite** is an embedded single-file relational database with no server to run. It is ideal for prototypes and tests but supports only one writer at a time and has no mature built-in vector search.

### 4.2 Comparison

| Criterion | PostgreSQL (+ pgvector) | MongoDB | SQLite |
|-----------|-------------------------|---------|--------|
| Catalogue integrity (types, foreign keys, filtering by dimension and price ranges) | Strong | Weaker; enforced in code | Strong |
| Saved room designs (nested, evolving structure) | Good via `jsonb` | Excellent | Acceptable (JSON functions) |
| Vector similarity for style matching | `pgvector`, self-hosted | Atlas Vector Search (managed service) | Extensions only, immature |
| Concurrent users | Good | Good | Limited (single writer) |
| Tooling (Go API, Python ML service) | pgx / sqlc in Go, golang-migrate; SQLAlchemy in Python | Official Go and Python drivers | Go and Python drivers |
| Operations for a student team | One Docker container | One Docker container | None |
| C6 Licence | PostgreSQL licence (permissive) | SSPL (source-available) | Public domain |

### 4.3 Decision

**PostgreSQL with `pgvector`** (FR-04, FR-05, FR-08). The catalogue is the most queried data and is strongly relational (filter by category, dimensions, price, style; join to designs), which favours a relational database. The one document-shaped part, a saved room design, fits in a `jsonb` column, so MongoDB's main advantage is covered without giving up integrity. `pgvector` keeps item embeddings next to the catalogue rows, so a single SQL query can combine hard filters ("fits in 1.6 m, under budget") with style similarity, instead of synchronising a separate vector store. SQLite remains useful for fast unit tests but is not suitable as the deployed database.

Supporting choices:

- **Asset storage:** 3D models and textures are static files in object storage (S3-compatible, e.g. MinIO locally) or a CDN, referenced by URL from catalogue rows, never stored in the database or served through the API.
- **Schema management:** versioned SQL migrations (golang-migrate) in the repository; the ML service reads the catalogue and writes item embeddings through its own narrow repository layer.
- **Cache:** Redis in front of PostgreSQL for frequent catalogue queries (TTL-based invalidation on catalogue import).

## 5. Component interaction

### 5.1 Options

There are two interaction boundaries: the browser client ↔ core API, and the core API ↔ ML service.

**REST over HTTP with JSON** exposes resources (`/catalogue/items`, `/designs/{id}`, `/recommendations`, `/layouts`) with standard HTTP methods. An OpenAPI description (written contract-first) is used to generate a typed TypeScript client for the frontend and to test the Go API and the ML service against the same contract.

**GraphQL** exposes one endpoint where the client asks for exactly the fields it needs. It reduces over-fetching for complex, nested screens, but adds a schema layer, resolver code, harder HTTP caching and more tooling on both sides.

**WebSockets** keep a persistent two-way connection. They suit real-time collaboration (several users editing one room) and streaming progress from long-running jobs, but they are stateful, harder to scale and cache, and unnecessary for ordinary request/response operations.

### 5.2 Comparison

| Criterion | REST + JSON | GraphQL | WebSockets |
|-----------|-------------|---------|------------|
| Fit with operations (load catalogue, save design, request recommendations or a layout) | Direct mapping | Good, but more machinery than needed | Overkill for request/response |
| Typed client for the TS frontend | Generated from the OpenAPI contract | Generated from the GraphQL schema | Manual message types |
| HTTP caching of catalogue and assets | Native (CDN, ETag) | Difficult (single POST endpoint) | None |
| Long-running AI jobs (LLM call, layout optimisation) | Request with timeout, or a job resource polled by the client; Server-Sent Events for progress | Subscriptions (needs WebSockets anyway) | Native progress streaming |
| Real-time multi-user editing | Not supported | Via subscriptions | Native |
| Learning cost and testability | Lowest; testable with curl or the auto-generated docs page | Medium | Medium to high |

### 5.3 Decision

**REST with JSON, documented by OpenAPI, on both boundaries** (FR-05, FR-06, FR-08, NFR-06). Every operation in the planned system is a request followed by a response, and REST maps onto them directly with the least code and tooling. The generated OpenAPI client gives the frontend end-to-end types. Catalogue data and 3D assets benefit from ordinary HTTP caching, which GraphQL makes harder. If layout optimisation or LLM calls become slow enough that the user needs progress feedback, a single Server-Sent Events endpoint (or one WebSocket channel) can be added for that case without changing the rest of the API. Real-time collaborative editing is out of scope for the diploma and recorded as future work; it would be the main reason to adopt WebSockets.

**Core API ↔ ML service.** gRPC was considered for the internal call (smaller payloads, generated stubs in Go and Python; the backend developer has used it). REST/JSON was chosen because there is only one internal client, payloads are small (a candidate list and scores), and the same OpenAPI tooling, logging and curl-based debugging work on both boundaries. If the internal call becomes a measurable bottleneck, switching it to gRPC changes only the adapter in the Go API (hexagonal architecture).

Within the browser, the 2D UI and the 3D scene communicate through a shared client-side store (Zustand, section 7) rather than through events or a bridge, which is one of the reasons for choosing react-three-fiber in section 2.

## 6. AI approaches

The system needs two AI capabilities that should be evaluated separately:

1. **Recommendation:** choose suitable furniture items from the catalogue for a user's room, budget and style.
2. **Auto-layout:** place the chosen items in the room so the arrangement is valid (no overlaps, nothing blocking doors or windows, enough walking space) and looks reasonable.

### 6.1 Approach A: rules plus optimisation

**Recommendation:** content-based filtering. Each catalogue item has attributes (category, dimensions, style tags, colour, material, price). The user's preferences become a weighted scoring function; hard filters remove items that do not fit the room or budget. Item embeddings from product images and descriptions, computed with open-source CLIP-family models (Radford et al., 2021), allow "similar style" matching and matching to items the user has already chosen.

**Layout:** interior design guidelines are written as cost terms (clearance around furniture, circulation paths, alignment to walls, conversation distance between seats, facing the focal point, visual balance) and hard constraints (inside the room, no overlap, doors and windows clear). An optimiser searches for the arrangement with the lowest cost. This is the approach of Merrell et al. (2011), "Interactive Furniture Layout Using Interior Design Guidelines", and Yu et al. (2011), "Make It Home: Automatic Optimization of Furniture Arrangement", both of which used simulated annealing / Markov chain Monte Carlo search. Constraint solvers (Google OR-Tools CP-SAT) are an alternative for the hard constraints.

- **Strengths:** works with no training data; every result is explainable ("the sofa faces the TV because of the focal-point rule"); hard constraints are guaranteed; runs in well under a few seconds for a single room; each rule can be evaluated in isolation.
- **Weaknesses:** quality depends on how well the rules are written and weighted; adding a new room type means writing new rules; does not understand free-form requests.

### 6.2 Approach B: LLM-based

A large language model receives the room description (dimensions, doors, windows), the catalogue subset and the user's request in natural language, and returns either a list of items, a layout as coordinates, or a set of spatial relations ("bed against the north wall, nightstands on both sides"). Research examples include LayoutGPT (Feng et al., NeurIPS 2023), which prompts an LLM to output layouts in a CSS-like format, and Holodeck (Yang et al., CVPR 2024), which has an LLM produce spatial relations that a separate constraint solver then turns into coordinates.

- **Strengths:** understands free-form requests in any language ("a cosy Scandinavian bedroom for a student, under 300 000 tenge"); good at style reasoning and at writing explanations for users; no training needed.
- **Weaknesses:** direct numeric coordinates from LLMs often overlap or violate dimensions, so a validation and repair step is required; results are not deterministic, which complicates evaluation; per-request API cost and latency; depends on an external provider.

### 6.3 Approach C: learned models

Generative models trained on large datasets of designed rooms learn layout patterns directly. Examples are the deep convolutional scene priors of Wang et al. (2018), ATISS (Paschalidou et al., NeurIPS 2021), an autoregressive transformer over furniture objects, and later diffusion-based scene generators. They are typically trained on the 3D-FRONT dataset (Fu et al., 2021). For recommendation, collaborative filtering or learned ranking models fill the same role.

- **Strengths:** state-of-the-art realism on the room types in the training data; captures implicit patterns that are hard to write as rules.
- **Weaknesses:** needs a large dataset that matches our catalogue and room types (3D-FRONT uses its own furniture models and Chinese apartment layouts); training needs GPUs and time the diploma does not have; outputs still violate hard constraints and need post-processing; collaborative filtering needs user interaction history that a new system does not have (the cold-start problem); hard to explain.

### 6.4 Comparison

| Criterion | A: Rules + optimisation | B: LLM-based | C: Learned models |
|-----------|-------------------------|--------------|-------------------|
| Training data needed | None | None | Large (thousands of rooms; user history for CF) |
| Guarantees hard constraints | Yes | No; needs a solver or repair step | No; needs post-processing |
| Explainability | High | Medium (natural-language explanations, not always faithful) | Low |
| Handles free-form text requests | No | Yes | No (without extra models) |
| Determinism / reproducible evaluation | High (seeded) | Low | Medium |
| Running cost | CPU only, free | Per-request API cost | GPU for training, CPU/GPU for inference |
| Implementation risk in one year | Low | Low to medium | High |
| Novelty for a diploma | Medium on its own | High in combination | High, but risky |

### 6.5 Decision: hybrid pipeline

No single approach meets every requirement, so the system combines A and B, each where it is strongest:

1. **Preference understanding (LLM):** the user describes the room and taste in free text or through a short questionnaire. An LLM converts this into a structured preference object (style tags, colour palette, budget, required items, room function) validated against a JSON schema. A questionnaire-only path keeps the system working without the LLM.
2. **Recommendation (content-based scoring, FR-05; Python ML service):** hard filters (fits the room, within budget) followed by a weighted score combining attribute matches and CLIP embedding similarity to the stated style and to already selected furniture. Embeddings are stored in PostgreSQL with `pgvector`. Quality is measured with Precision@K and nDCG@10 against the baseline "filter by category and price". The output is a ranked shortlist per furniture category, with the score breakdown kept for explanations. Scoring runs in the database and in the ML service without any LLM call, so it stays well inside the 2 s budget of NFR-02.
3. **Layout (rules + optimisation, FR-06, FR-07; Go core API):** the selected items are placed by a cost-function optimiser (simulated annealing seeded by simple heuristics such as "large items against walls first"), with hard constraints for room bounds, overlaps, door swing areas and minimum walkways. The same constraint checks run in the editor whenever the user moves an item, which provides the collision and out-of-bounds validation of FR-07. Following the Holodeck idea, the LLM may optionally propose high-level relations ("desk under the window"), which enter the optimiser as soft cost terms rather than as raw coordinates.
4. **Explanation (LLM, optional):** the score breakdown and the satisfied rules are turned into a short user-facing explanation of why each item was chosen and placed where it is.

Learned models (approach C) are recorded as future work: once the system collects real user designs and feedback, they can serve as training data for a learned layout prior or a collaborative-filtering recommender.

This design keeps the core behaviour deterministic, explainable and measurable for the evaluation plan (constraint violations, walkway clearance, optimiser runtime, user ratings), while the LLM layer provides the natural-language interaction that makes the system feel novel. The LLM provider sits behind a small interface so it can be swapped, and the system degrades gracefully to questionnaire input and template explanations if the LLM is unavailable.

## 7. Recommended stack

| Layer | Choice | Main reason |
|-------|--------|-------------|
| Frontend framework | React + TypeScript, built with Vite | Largest ecosystem; required by R3F; type safety across a three-person team |
| 3D rendering | Three.js via react-three-fiber + drei | Scene and UI in one state tree; small bundle; editor helpers ready-made |
| UI state | Zustand | Lightweight store usable from both 2D UI and 3D components (the R3F team's own library) |
| 3D assets | glTF/GLB with Draco/Meshopt compression | Open standard, works with every engine considered |
| Core API | Go (net/http, hexagonal architecture) | Low latency for catalogue search, fast CPU-bound layout checks, team's backend language |
| ML service | Python, FastAPI, PyTorch, Hugging Face (CLIP), scikit-learn | ML ecosystem; isolated from the core API |
| Cache | Redis | Hot catalogue queries and recommendation results |
| Catalogue data | Python parsers for Kazakhstan stores (e.g. mebel.kz) | Local assortment that existing planners do not cover |
| Database | PostgreSQL + `pgvector` (SQLAlchemy/SQLModel, Alembic) | Relational catalogue, `jsonb` room designs, vector search for style similarity |
| Asset storage | S3-compatible object storage (MinIO) | Images and GLB models kept out of the database, cached by the browser |
| Frontend–backend interaction | REST + JSON with OpenAPI and a generated TypeScript client | Matches request/response operations; typed end to end; cacheable |
| Recommendation | Content-based scoring with CLIP embeddings + constraints | No user history needed; explainable; measurable with nDCG@10 |
| Auto-layout | Cost-function optimisation (simulated annealing) with hard constraints | Proven in the literature; guarantees valid layouts; no training |
| Natural-language layer | LLM API behind a provider interface | Parses free-text preferences and writes explanations; optional at runtime |
| Deployment / CI | Docker Compose, GitHub Actions | One command to run the full system; tests on every pull request |

### Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Few free, correctly scaled 3D furniture models | Start with a small curated catalogue (CC0 sources such as Poly Haven, or simple parametric models generated in code); keep real dimensions as data separate from the mesh |
| Layout optimiser gives unnatural results | Tune weights against a small set of hand-made reference rooms; let users lock items and re-run |
| LLM cost, latency or unavailability (an LLM call alone can exceed the NFR-02 budget) | LLM kept out of the recommendation path; used only for parsing free text and writing explanations, which load after the results; cache results; questionnaire and template fallbacks |
| Performance on weak laptops and phones (NFR-01) | Compressed assets, instancing, on-demand rendering (`frameloop="demand"` in R3F), simplified shadows |
| Team members new to React or 3D | R3F keeps 3D code in the same component model as the UI; pair on the first scene components |

## References

- Merrell, P., Schkufza, E., Li, Z., Agrawala, M., Koltun, V. (2011). Interactive Furniture Layout Using Interior Design Guidelines. *ACM Transactions on Graphics (SIGGRAPH)*, 30(4).
- Yu, L.-F., Yeung, S.-K., Tang, C.-K., Terzopoulos, D., Chan, T. F., Osher, S. J. (2011). Make It Home: Automatic Optimization of Furniture Arrangement. *ACM Transactions on Graphics (SIGGRAPH)*, 30(4).
- Wang, K., Savva, M., Chang, A. X., Ritchie, D. (2018). Deep Convolutional Priors for Indoor Scene Synthesis. *ACM Transactions on Graphics (SIGGRAPH)*, 37(4).
- Paschalidou, D., Kar, A., Shugrina, M., Kreis, K., Geiger, A., Fidler, S. (2021). ATISS: Autoregressive Transformers for Indoor Scene Synthesis. *NeurIPS 2021*.
- Fu, H., et al. (2021). 3D-FRONT: 3D Furnished Rooms with layOuts and semaNTics. *ICCV 2021*.
- Feng, W., et al. (2023). LayoutGPT: Compositional Visual Planning and Generation with Large Language Models. *NeurIPS 2023*.
- Yang, Y., et al. (2024). Holodeck: Language Guided Generation of 3D Embodied AI Environments. *CVPR 2024*.
- Three.js documentation: https://threejs.org/docs/
- react-three-fiber documentation: https://r3f.docs.pmnd.rs/
- Babylon.js documentation: https://doc.babylonjs.com/
- Unity Web platform documentation: https://docs.unity3d.com/Manual/webgl.html
- Radford, A., et al. (2021). Learning Transferable Visual Models From Natural Language Supervision (CLIP). *Proc. ICML 2021*, PMLR 139, 8748–8763.
- Go documentation: https://go.dev/doc/
- FastAPI documentation: https://fastapi.tiangolo.com/
- NestJS documentation: https://docs.nestjs.com/
- gRPC documentation: https://grpc.io/docs/
- Redis documentation: https://redis.io/docs/
- MinIO documentation: https://min.io/docs/
- PostgreSQL documentation: https://www.postgresql.org/docs/
- pgvector: https://github.com/pgvector/pgvector
- MongoDB documentation: https://www.mongodb.com/docs/
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- GraphQL specification: https://spec.graphql.org/
- Khronos glTF 2.0 specification: https://www.khronos.org/gltf/

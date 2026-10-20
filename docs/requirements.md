# Requirements Specification

**Project:** Web-Based System for AI-Assisted Furniture Selection and 3D Room Planning
**Task:** DIP-3

> Status: draft for team and supervisor review. See [proposal.md](proposal.md) for scope.
>
> **Priorities** use MoSCoW: **M** = Must have (MVP), **S** = Should have, **C** = Could have. "Won't have" items are listed in Section 2.11.
> **Acceptance criteria** describe how each requirement is verified; every Must requirement has a check that can be passed or failed. FR-01 to FR-09 and NFR-01 to NFR-06 are the core MVP requirements referenced by [evaluation-plan.md](evaluation-plan.md) and the design diagrams; higher IDs refine and extend them.
>
> **Stack:** React + React Three Fiber web client, Go core API, Python ML service, PostgreSQL + pgvector, Redis, MinIO, REST/JSON with OpenAPI (justified in [technology-comparison.md](technology-comparison.md)).

## 1. Users and Roles

| Role | Description |
|---|---|
| Guest | Unregistered visitor who can try the planner without saving |
| Registered user | Creates, saves and manages room projects |
| Administrator | Manages the furniture catalogue, styles and users |

## 2. Functional Requirements

### 2.1 Core MVP requirements

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-01 | **Room setup.** The system shall allow the user to create a room by entering length, width and ceiling height. | M | Entering 4.0 x 3.5 x 2.7 m produces a 3D room whose measured dimensions match within 1 cm. |
| FR-02 | **3D view and navigation.** The system shall render the room and furniture in 3D at real scale and allow the user to orbit, pan and zoom. | M | A 2.0 m catalogue sofa measures 2.0 m (within 2 cm) against the room walls; orbit, pan and zoom all work with the mouse; the camera cannot pass below the floor. |
| FR-03 | **Furniture editing.** The system shall allow the user to add, move, rotate and remove furniture by direct manipulation. | M | Each of the four actions is performed with the mouse and is reflected in the saved project (FR-08). |
| FR-04 | **Catalogue browsing.** The system shall allow the user to browse and filter the catalogue by category, style, price range and maximum size. | M | Each filter, alone and combined, returns only matching items (automated API tests). |
| FR-05 | **AI recommendations.** The system shall recommend a set of furniture based on room size, room purpose, chosen styles and budget. | M | For each room purpose the set contains that purpose's core items (e.g. bedroom: bed and storage; office: desk and chair); every item carries at least one chosen style tag; detailed fit and budget checks in FR-32 and FR-33. |
| FR-06 | **Auto-layout suggestion.** The system shall automatically place the selected furniture in the room. | M | For a room and up to 15 items, the system returns positions and rotations for all items, or reports which items did not fit; generated layouts pass FR-38 to FR-40. |
| FR-07 | **Collision and bounds validation.** The system shall detect furniture overlapping other furniture, walls or fixed obstacles, or extending outside the room, and highlight it in real time while editing. | M | Dragging an item into another item or through a wall turns it red during the drag and a warning names the violated rule; a scripted test with 20 overlapping and 20 valid placements classifies all 40 correctly. |
| FR-08 | **Save and load.** The system shall save project state (room, furniture, layout, preferences) and restore it on reopening. | M | A project with 10 items is saved, the browser is closed, and on reopening all item positions match within 1 mm and 1°. |
| FR-09 | **Cost summary.** The system shall show a list of all items in the design with prices and the total cost. | M | The list contains exactly the items in the scene and the total equals the sum of item prices, updating when items are added or removed. |

### 2.2 Accounts and projects

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-10 | The system shall allow a user to register and log in with email and password. | M | A new user registers, logs out and logs back in; a wrong password is rejected with an error message. |
| FR-11 | The system shall allow a guest to use the planner without an account. | S | A guest can define a room and generate a layout; on "Save" they are asked to register and the design is kept after registration. |
| FR-12 | The system shall allow a registered user to create, rename, duplicate and delete projects. | M | Each action is performed from the project list and the list reflects it after page reload. |
| FR-13 | The system shall autosave changes during editing. | S | After moving an item and waiting 30 s, reloading the page shows the item in its new position. |
| FR-14 | The system shall allow a user to share a read-only link to a project. | C | Opening the link in a private window shows the design with editing controls disabled. |

### 2.3 Room definition

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-15 | The system shall allow the user to draw a polygonal floor plan (e.g. L-shaped) in a 2D editor. | S | An L-shaped room with 6 corners is drawn and rendered in 3D with walls on all 6 edges. |
| FR-16 | The system shall allow the user to add doors and windows with position, width, height and (for doors) swing direction. | M | A door and a window appear as openings in the 3D walls at the entered positions; the door swing arc is shown in plan view. |
| FR-17 | The system shall allow the user to add fixed obstacles (radiators, columns, built-ins). | S | An added obstacle is rendered and treated as a collision by FR-06 and FR-07. |
| FR-18 | The system shall allow the user to choose wall and floor colours or materials. | C | Changing the floor material updates the 3D view immediately and persists after save. |
| FR-19 | The system shall validate room dimensions and openings. | M | Zero, negative or over 50 m dimensions, and a door wider than its wall, are rejected with a message naming the invalid field. |
| FR-20 | The system shall use metric units (metres, centimetres) for input and display. | M | All dimension fields and labels show metric units. |
| FR-21 | The system shall optionally display dimensions in imperial units. | C | Toggling units converts all displayed values; stored values are unchanged. |

### 2.4 Preferences

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-22 | The system shall allow the user to select the room purpose (bedroom, living room, office, kitchen-dining, kids' room). | M | Each purpose can be selected and is saved with the project. |
| FR-23 | The system shall allow the user to select one or more styles from a list of at least 5 (e.g. Scandinavian, minimalist, loft, classic, modern). | M | At least 5 styles are offered; selecting two styles is accepted and saved. |
| FR-24 | The system shall allow the user to set a total budget. | M | A budget is entered and saved; non-positive values are rejected. |
| FR-25 | The system shall allow the user to mark required and excluded item categories. | S | Marking "desk" required always yields a desk; marking "TV stand" excluded never yields one. |
| FR-26 | The system shall convert a free-text description of wishes into structured preferences using a language model, and show the result for confirmation. | S | For a test set of 20 descriptions, at least 16 are parsed into the correct style, room purpose and budget; the user can edit the parsed fields before applying them. |
| FR-27 | The system shall infer a style from an uploaded reference photo. | C | For 10 labelled test photos, the inferred style matches in at least 6. |

### 2.5 Furniture catalogue

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-28 | The system shall store furniture items with name, category, dimensions (W x D x H), price, style tags, colour, material, image and 3D model. | M | The schema contains all fields; the catalogue holds at least 5 000 items from at least two stores with all mandatory fields filled (3D model or parametric model, see FR-57). |
| FR-29 | The system shall allow an administrator to add, edit and remove catalogue items and upload 3D models. | M | An admin creates an item with a GLB model, edits its price and deletes it; a regular user receives HTTP 403 for the same operations. |
| FR-30 | The system shall store per-item placement metadata (front clearance, wall-mounted or free-standing, related items). | M | Every item has placement metadata and the layout module reads it (unit test). |
| FR-31 | The system shall collect catalogue items from several Kazakhstan online furniture stores (e.g. mebel.kz) and import CSV/JSON files, normalising dimensions, materials, colour and price into one schema. | M | Parsers for at least two stores load at least 5 000 items; parsers respect robots.txt and a configured request rate; rows with missing required fields are reported and skipped; dimensions are stored in centimetres. |
| FR-57 | The system shall generate a simplified parametric 3D model from catalogue dimensions for items without a seller 3D model. | M | For 20 sampled items without a model, the generated model's bounding box matches catalogue W x D x H within 1 cm and the item can be placed like any other. |

### 2.6 AI furniture recommendation

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-32 | Recommendations shall exclude items that cannot fit in the room or through its doors. | M | In a 2.5 x 2.5 m room with a 70 cm door, no recommended item has a footprint larger than the free floor area or a smallest cross-section wider than 70 cm. |
| FR-33 | The total price of the recommended set shall stay within the budget. | M | Across 50 automated cases with random budgets, the total never exceeds the budget; if no valid set exists, the user is told so. |
| FR-34 | Recommended items shall be stylistically consistent with each other. | S | In user testing, the mean rating for "items match each other" is at least 3.5 out of 5. |
| FR-35 | The system shall give a short natural-language explanation for each recommended item. | S | Every recommended item shows a 1 to 3 sentence explanation mentioning style, size or price. |
| FR-36 | The system shall offer alternatives for any recommended item ("similar", "cheaper", "smaller"). | S | Each option returns at least 3 items of the same category that are respectively similar in style, lower in price, or smaller in footprint. |
| FR-37 | The system shall adapt later suggestions to items the user replaced or removed. | C | After the user removes two items of a style, later alternatives rank that style lower (unit test). |

### 2.7 AI layout generation

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-38 | Generated layouts shall have no overlapping items and no items outside the room. | M | On a benchmark of 30 rooms, 100% of generated layouts pass the FR-07 collision and bounds check. |
| FR-39 | Generated layouts shall keep door swing areas and window fronts clear. | M | On the benchmark, no item intersects a door swing area, and no item taller than the sill intersects the 50 cm zone in front of a window. |
| FR-40 | Generated layouts shall keep walkways of at least a configurable minimum width (default 60 cm). | M | On the benchmark, every door connects to every item's front clearance zone by a path of at least the minimum width (occupancy-grid check). |
| FR-41 | Generated layouts shall respect functional relationships (bedside tables beside the bed, chairs at the table, sofa facing the TV). | S | On the benchmark, at least 90% of defined relationships are satisfied. |
| FR-42 | The system shall generate several alternative layouts. | S | At least 3 layouts are returned, each differing by more than 30 cm in at least one large item's position. |
| FR-43 | The system shall score each layout and explain its main strengths and violations. | S | Each layout shows a score from 0 to 100 and at least two explanation points. |
| FR-44 | The system shall re-arrange remaining furniture after the user locks some items in place. | C | Locked items keep their exact positions; the rest are re-placed and pass FR-38 to FR-40. |

### 2.8 3D visualisation and editing

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-45 | The system shall provide a top-down 2D plan view. | M | Plan view shows an orthographic top view with walls, openings and furniture outlines; FR-03 editing works in it. |
| FR-46 | The system shall snap furniture to walls and to a grid, with 90° rotation steps. | S | With snapping on, an item dragged within 10 cm of a wall aligns flush; rotation steps are 90° (15° with a modifier key). |
| FR-47 | The system shall display item dimensions and distances to the nearest walls on selection. | S | Selecting an item shows W x D x H and distance labels matching the scene within 1 cm. |
| FR-48 | The system shall support undo and redo of editing actions. | S | At least 20 consecutive actions can be undone and redone with Ctrl+Z / Ctrl+Shift+Z. |
| FR-49 | The system shall provide a first-person walkthrough mode. | C | The user walks through the room at 1.6 m eye height with WASD keys and cannot pass through walls. |
| FR-50 | The system shall allow switching an item's colour or material variant. | C | Selecting a variant updates the model's material and the FR-09 cost summary. |

### 2.9 Output

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-51 | The system shall export the cost summary as PDF or CSV. | S | The exported file opens in a standard viewer and matches the on-screen list. |
| FR-52 | The system shall export an image of the 3D view and of the plan view. | S | A PNG of at least 1920 x 1080 px is downloaded for each view. |
| FR-53 | The system shall allow side-by-side comparison of two saved designs. | C | Two designs are shown together with their total costs and layout scores. |

### 2.10 Administration

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-54 | The system shall provide an admin panel for the catalogue, styles and room-type rules. | M | An admin creates a new style and assigns it to items; it then appears in the user's style list (FR-23). Non-admins cannot open the panel. |
| FR-55 | The system shall allow an administrator to view and deactivate user accounts. | S | A deactivated user can no longer log in. |
| FR-56 | The system shall show basic usage statistics. | C | The panel shows the number of users and projects and the 10 most recommended items. |

### 2.11 Won't have (this project)

- Multi-room or whole-apartment planning.
- Live retailer integration, checkout and payments.
- Room scanning with camera or LiDAR, and AR placement.
- Native mobile applications.

## 3. Non-Functional Requirements

### 3.1 Core MVP requirements

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-01 | **Performance.** The 3D view shall run smoothly on typical student hardware. | M | A room with 30 items renders at 30 FPS or more on a laptop with integrated graphics (reference: Intel Iris Xe or equivalent), measured with browser performance tools. |
| NFR-02 | **Recommendation latency.** Recommendations shall be returned quickly. | M | 95th-percentile response time of the recommendation endpoint is under 2 s for the MVP catalogue, over 100 requests. |
| NFR-03 | **Usability.** The system shall be perceived as usable by first-time users. | M | The mean System Usability Scale (SUS) score across test participants is 68 or higher. |
| NFR-04 | **Browser compatibility.** The application shall work in current desktop browsers. | M | The core flow (FR-01 to FR-09) passes a manual smoke test in the latest versions of Chrome, Firefox, Edge and Safari. |
| NFR-05 | **Security.** Secrets shall never reach the client and all input shall be validated. | M | A search of the built frontend bundle and the repository finds no API keys or passwords; keys come from server environment variables; every API endpoint validates input with a Pydantic schema and rejects malformed requests with HTTP 422. |
| NFR-06 | **Maintainability.** Core logic shall be covered by automated tests. | M | Recommendation and layout modules have at least 60% line coverage, reported in CI; all tests pass on the main branch. |

### 3.2 Performance

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-07 | The application shall load quickly. | S | On a throttled 20 Mbit/s connection, the start page is interactive within 3 s (Lighthouse). |
| NFR-08 | Layout generation shall be fast and show progress. | M | The first layout returns within 10 s for 15 items (95th percentile over the benchmark); a progress indicator is visible meanwhile. |
| NFR-09 | Editing interactions shall feel immediate. | M | Collision feedback (FR-07) updates within 100 ms while dragging in a scene with 30 items. |
| NFR-10 | The backend shall handle concurrent users. | S | A load test with 50 virtual users (Locust or k6) keeps NFR-02 within its limit with an error rate below 1%. |
| NFR-35 | Catalogue search shall be fast on the full catalogue. | M | With at least 5 000 items, the 95th-percentile response time of the catalogue search endpoint is under 300 ms (k6 load test, 20 virtual users). |
| NFR-36 | Recommendation quality shall exceed the baseline. | M | On the labelled evaluation set, nDCG@10 of the ML ranking is higher than that of the baseline "filter by category and price" (see [evaluation-plan.md](evaluation-plan.md)). |

### 3.3 Usability

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-11 | First-time users shall complete the core flow without instructions. | M | In user testing, at least 80% of participants define a room and obtain a furnished layout within 5 minutes without help. |
| NFR-12 | The interface shall be available in English and Russian (Kazakh desirable). | S | All UI strings exist in both languages; switching language does not reload the project. |
| NFR-13 | Non-3D parts of the UI shall be accessible. | S | An axe or Lighthouse audit reports no WCAG 2.1 AA contrast errors; all forms are keyboard-operable. |
| NFR-14 | Error messages shall explain the problem and how to fix it. | M | Every validation error in FR-19 and FR-24 names the field and allowed range; no stack traces are shown to users. |

### 3.4 Reliability and availability

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-15 | Work in progress shall not be lost. | S | After a forced browser close, at most 30 s of edits are lost (FR-13). |
| NFR-16 | Core features shall work when the language-model service is unavailable. | M | With the LLM API key removed, FR-05, FR-06 and FR-32 to FR-40 still pass their acceptance checks; free-text input shows a "not available" message. |
| NFR-17 | The deployed system shall be available during evaluation and defence. | S | Uptime monitoring shows at least 99% availability over the evaluation period. |
| NFR-18 | Data shall be backed up. | S | A daily automated database backup exists and a restore has been tested once. |

### 3.5 Security and privacy

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-19 | Passwords shall be stored securely. | M | The database contains only bcrypt or Argon2 hashes (inspection). |
| NFR-20 | All traffic shall be encrypted. | M | The deployed site is served only over HTTPS; HTTP requests redirect to HTTPS. |
| NFR-21 | Access shall be restricted by ownership and role. | M | Automated tests confirm user A gets HTTP 403 or 404 for user B's projects, and non-admins get HTTP 403 on all admin endpoints. |
| NFR-22 | The application shall resist common web attacks, and users shall be able to delete their data. | S | Database access uses an ORM or parameterised queries; an OWASP ZAP baseline scan reports no high-risk alerts; deleting an account removes the user and all their projects. |

### 3.6 Compatibility

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-23 | The application shall handle missing WebGL support. | M | With WebGL 2 disabled, the app shows an explanatory message instead of a blank screen. |
| NFR-24 | The application shall be usable on tablets. | C | The core flow can be completed on a 10-inch tablet with touch input. |

### 3.7 Maintainability and extensibility

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-25 | Web client, core API, ML service and layout module shall be separated behind documented interfaces. | M | Recommendation runs in the ML service and is called only through its API; the layout module is a separate package of the core API; each is unit-tested without the web server; if the ML service is down the core API falls back to baseline ranking. |
| NFR-26 | New categories, styles and placement rules shall be addable without code changes. | S | A new style and a new relationship rule added via the admin panel or a config file take effect without redeploying code. |
| NFR-27 | Code style shall be enforced automatically. | S | CI runs linters and formatters (e.g. Ruff, ESLint, Prettier) and fails on violations. |
| NFR-28 | The REST API shall be documented. | S | The OpenAPI specifications of the core API and the ML service are kept in the repository and served at `/docs`; contract tests pass for both services. |

### 3.8 Deployment and operations

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-29 | The system shall run locally with one command. | M | On a clean machine with Docker, `docker compose up` starts the web client, core API, ML service, PostgreSQL, Redis and MinIO, and the app opens in the browser. |
| NFR-30 | The system shall be publicly deployed for evaluation and defence. | M | The application is reachable at a public HTTPS URL during the evaluation period. |
| NFR-31 | Server errors shall be logged. | S | Every HTTP 5xx response produces a log entry with timestamp, endpoint and stack trace. |

### 3.9 Data and content

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| NFR-32 | All catalogue assets shall be properly licensed. | M | Each item records the source and licence of its model and image; all licences permit academic use. |
| NFR-33 | 3D models shall be web-optimised. | M | All models are glTF/GLB, in metres, at most 50 000 triangles and 5 MB each (automated asset script). |
| NFR-34 | Catalogue dimensions shall match the 3D models. | S | For every item, model bounding-box dimensions differ from catalogue W x D x H by 2 cm or less (same script). |

## 4. Constraints and Assumptions

- The system runs in a desktop web browser; no installation is required.
- The catalogue is collected from public store websites and is not connected to real stock; prices are stored with the collection date.
- Room geometry is a single floor-level polygon with vertical walls and a flat ceiling.
- External AI services, if used, are accessed through an API whose cost stays within the team's budget.
- Development follows the diploma schedule in [project-management.md](project-management.md).

## 5. Traceability to Project Goals

| README goal | Requirements |
|---|---|
| Personalised AI recommendations by preferences, room dimensions and style | FR-05, FR-06, FR-22 to FR-27, FR-32 to FR-44, NFR-02 |
| Interactive 3D visualisation | FR-01 to FR-03, FR-07, FR-45 to FR-50, NFR-01, NFR-09 |
| Simplified decision-making (scale, placement, purchasing) | FR-07, FR-09, FR-47, FR-51 to FR-53, NFR-03, NFR-11 |

## 6. Summary

| Priority | Functional | Non-functional |
|---|---|---|
| Must | 29 | 22 |
| Should | 18 | 13 |
| Could | 10 | 1 |
| **Total** | **57** | **36** |

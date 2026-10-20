# Existing System Comparison

**Task:** DIP-6 · **Status:** draft for pre-defense 1 (24 October 2026)

## 1. Selection of systems

Five systems were selected because each represents a different way the market currently solves "help me choose and place furniture":

| ID | System | Category | Why selected |
|----|--------|----------|--------------|
| S1 | **IKEA Kreativ** (IKEA app / ikea.com) | Retailer tool, AI + mixed reality | Largest furniture retailer; AI room scan, erase existing furniture, place catalog items |
| S2 | **Planner 5D** (web, iOS, Android) | General-purpose 2D/3D home planner with AI features | Popular consumer planner; AI floor-plan recognition and a "design generator" |
| S3 | **HomeByMe** (Dassault Systèmes, web) | Browser 3D planner with branded catalogs | Closest to our "web-based 3D + real products" positioning |
| S4 | **Homestyler** (web, mobile) | 3D planner + rendering + AI styling | Large model library, photoreal rendering, AI decoration tools |
| S5 | **Generative "AI interior" image tools** (e.g. RoomGPT-style restyling apps) | Image generation | Represents pure generative-AI approach: restyle a room photo, no geometry |

## 2. Comparison criteria

Criteria follow directly from the project's problem statement (fit/scale uncertainty, decision support, accessibility):

| Code | Criterion | Why it matters |
|------|-----------|----------------|
| C1 | Runs in a web browser without installation | Accessibility for target users (NFR-04) |
| C2 | Interactive 3D room model with real dimensions | Core of fit/scale decision |
| C3 | Catalog of real, purchasable products with prices | Turns a picture into a purchasing decision |
| C4 | Personalised recommendations (style, room size, budget) | Main AI value proposition (FR-05) |
| C5 | Automatic layout / arrangement suggestion | Saves effort for non-designers (FR-06) |
| C6 | Physical validity checks (collisions, clearances, fits in room) | Trust in suggestions (FR-07) |
| C7 | Explanation of *why* an item/layout is suggested | Transparency of AI decisions |
| C8 | Budget / total-cost summary | Decision support (FR-09) |
| C9 | Multi-retailer / open catalog (not locked to one brand) | Freedom of choice |
| C10 | Free core functionality | Barrier to entry for students and young families |

## 3. Comparison matrix

Legend: **●** fully supported · **◐** partially / limited · **○** not supported · **?** not confirmed yet.

| Criterion | S1 IKEA Kreativ | S2 Planner 5D | S3 HomeByMe | S4 Homestyler | S5 AI image tools | **Our system (target)** |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| C1 Browser, no install | ◐ (desktop web + app; scan in app) | ● | ● | ● | ● | ● |
| C2 Interactive 3D with dimensions | ◐ (scanned photo-based scene) | ● | ● | ● | ○ (2D images) | ● |
| C3 Real products with prices | ● (IKEA only) | ◐ (generic models) | ◐ (selected brands) | ◐ | ○ | ◐ (curated demo catalog) |
| C4 Personalised recommendations | ◐ | ◐ | ○ | ◐ | ○ | ● |
| C5 Automatic layout | ○ | ◐ ("design generator") | ○ | ◐ | ○ | ● |
| C6 Validity checks | ? | ? | ? | ? | ○ | ● |
| C7 Explanations | ○ | ○ | ○ | ○ | ○ | ● |
| C8 Cost summary | ◐ (shopping list) | ○ | ◐ (shopping list) | ○ | ○ | ● |
| C9 Open / multi-brand catalog | ○ | ● | ◐ | ● | n/a | ● (data-driven catalog) |
| C10 Free core | ● | ◐ (freemium) | ◐ (freemium) | ◐ (freemium) | ◐ | ● |

## 4. Evidence for claims

The committee asks that capability claims be supported by evidence. Each row cites its source; the column **Verified how** separates what we confirmed from what we only read.

| Claim | Evidence | Verified how |
|-------|----------|--------------|
| S1 lets users scan a room, erase existing furniture and place IKEA products; scans are processed in the cloud; launched in the US first, then Canada (June 2023) and Australia | TechCrunch, VentureBeat and Inside Retail coverage of the IKEA Kreativ launch; IKEA product page | Press/vendor sources (read 2026-10-20); hands-on test pending (DIP-6) |
| S1 is limited to the IKEA catalog | IKEA Kreativ product page | Vendor source |
| S2 recognises uploaded floor plans (walls, doors, windows) and offers AI design generator / Smart Wizard; premium features need a subscription | Furniture Today (2021) launch article; planner5d.com AI pages and FAQ | Press/vendor sources; hands-on test pending |
| S2 recognition dimensions are approximate | Planner 5D FAQ | Vendor source |
| S3 runs in the browser with branded catalogs | homebyme.com | Vendor source; hands-on test pending |
| S4 offers AI decoration / rendering features | homestyler.com | Vendor source; hands-on test pending |
| S5 produces restyled 2D images with no geometry or real products | Behaviour of the method class (diffusion image generation) | Inferred from how the method works |
| No system in S1–S5 explains *why* an item is recommended | Absence in product pages and documentation | **Assumption** until hands-on test (C7 row) |
| C6 support in S1–S4 unknown | — | Marked "?" deliberately |

**Hands-on protocol (to complete before pre-defense 1, DIP-6).** Each team member tests the systems assigned to them using the same scenario: *"Furnish a 4.0 × 3.5 m living room in Scandinavian style with a budget of 500 000 KZT"*. For each criterion record: supported / partial / not supported, number of steps, screenshots stored in `docs/assets/existing-systems/`. Replace every "?" and every "Vendor source" with the observed result.

## 5. Conclusions: why the proposed system is needed

1. **AI is either opaque or absent.** Commercial tools add AI for capture (scan, plan recognition) or styling, not for explainable *selection* of items that fit the user's room, style and budget (C4, C7).
2. **Layout suggestions do not guarantee validity.** Generative image tools (S5) produce attractive but physically impossible results; planners leave arrangement to the user (C5, C6). The literature (see `literature-review.md`, §3.1) shows how to combine suggestions with guaranteed constraints.
3. **Catalog lock-in.** The strongest AI tool (S1) works only with one retailer's products (C9).
4. **Decision support is weak.** Few tools summarise total cost against a budget (C8).

The proposed system targets the combination C1 + C2 + C4 + C5 + C6 + C7 + C8. It does **not** try to beat S1 on photoreal room capture or S4 on rendering quality; these are explicitly out of scope.

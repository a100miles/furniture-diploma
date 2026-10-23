# Evidence of Relevance

**Task:** DIP-4 · **Owner:** Muzaffar Kapezov · **Status:** five interview transcripts analysed; findings are preliminary qualitative evidence, not statistical proof.

The committee requires 3–5 discussions with user representatives (or a substantive agreement with a real client) and asks whether **verified findings are distinguished from assumptions**. This document records the five available interviews and the implications that can reasonably be drawn from them.

**Source:** `interview-transcripts.md`, five anonymised English interviews received on 23 October 2026 and transcribed using Whisper (`large-v3-turbo`) with light cleanup. The source notes that wording is otherwise retained, and uncertain words are marked `[sic: likely …]`. Quotes below preserve the transcript wording apart from trimming irrelevant words.

**Important limitations:** the transcripts do not record participants' demographic/profile details, interview dates, interviewers, or a complete individual consent record for every participant. The common voluntary/anonymity introduction was read at the start of each session. P3 explicitly agreed to anonymous notes. Do not infer participant occupations from the original recruitment plan: the actual profiles are not supplied. The transcripts also do not establish that participants saw the prototype; questions asked about a proposed tool in general.

## 1. Hypotheses tested

| ID | Hypothesis | Linked requirement |
|----|------------|--------------------|
| H1 | People buying furniture online are often unsure whether an item will fit the room | FR-01, FR-02, FR-07 |
| H2 | Non-designers find it hard to arrange furniture and would accept an automatic suggestion as a starting point | FR-06 |
| H3 | Users want recommendations filtered by style **and** budget, and want to know why an item is recommended | FR-05, FR-09 |
| H4 | A browser tool without installation is preferred over a mobile app | NFR-04 |
| H5 | Users would trust an AI layout more if it visibly respects walkways and door clearance | FR-07 |
| H6 | Furniture sellers / interior designers would use such a tool with clients | Target users |

## 2. Participant and record audit

| ID | Actual profile | Interview date | Consent evidence in transcript | Evidence status |
|----|----------------|-----------------|-------------------------------|-----------------|
| P1 | Not recorded | Not recorded; recording received 23 Oct 2026 | Common voluntary/anonymity introduction documented; explicit individual yes/no consent not recorded | Responses available; profile/date/consent metadata incomplete |
| P2 | Not recorded | Not recorded; recording received 23 Oct 2026 | Common voluntary/anonymity introduction documented; explicit individual yes/no consent not recorded | Responses available; profile/date/consent metadata incomplete |
| P3 | Not recorded | Not recorded; recording received 23 Oct 2026 | Explicit “May I take anonymous notes?” — “Yes.” | Responses available; profile/date metadata incomplete |
| P4 | Not recorded | Not recorded; recording received 23 Oct 2026 | Common voluntary/anonymity introduction documented; explicit individual yes/no consent not recorded | Responses available; profile/date/consent metadata incomplete |
| P5 | Not recorded | Not recorded; recording received 23 Oct 2026 | Common voluntary/anonymity introduction documented; explicit individual yes/no consent not recorded | Responses available; profile/date/consent metadata incomplete |

**Action before final submission:** check the original consent/session records and add actual interview dates and non-identifying participant profiles if those records exist. If they do not exist, state that metadata was not collected. Do not reconstruct it from the old recruitment plan.

## 3. Participant-level summaries

### P1
- **Shopping and fit:** bought a desk after checking online stores and a local shop; considered price, size and design. Used a tape measure. A chair was “too wide to fit comfortably under my desk” (Q2, 0:31).
- **Planning difficulty:** places large items first and leaves walking space; has not used a room-planning app and sketches on paper or moves furniture (Q3–Q4, 0:51–1:04).
- **Main difficulty:** imagining how items will look together and whether the room will feel crowded (Q5, 1:21).
- **Concept and trust:** would try a tool; wants accurate measurements, simple 3D preview, budget-fitting options and ability to adjust the suggested layout (Q6, 1:34). Wants exact dimensions and an explanation of why the arrangement works; prefers a phone (Q7, 2:01).

### P2
- **Shopping and fit:** bought a desk online; considered price, size, design and reviews. A chair was bigger than expected and took up too much space (Q1–Q2, 0:11–0:28).
- **Planning difficulty:** imagines arrangements, sometimes moves furniture, and tries to preserve walking space. Uses Pinterest/Google Images rather than a dedicated planner (Q3–Q4, 0:50–1:08).
- **Main difficulty:** understanding how furniture will look in the actual room before buying (Q5, 1:27).
- **Concept and trust:** would use a tool to save time; wants 3D visualisation, automatic furniture placement and budget-based recommendations (Q6, 1:43). Trust depends on accurate measurements and realistic-looking furniture; prefers a mobile app (Q7, 2:05).

### P3
- **Shopping and fit:** compared online options by price, design, size and quality. Measures the room and checks product dimensions; reported no serious fit problem but said it can be difficult to imagine furniture scale (Q1–Q2, 0:19–0:44).
- **Planning difficulty:** considers space and convenience and leaves room to walk. Uses mental visualisation or online pictures rather than a dedicated planner (Q3–Q4, 1:11–1:31).
- **Main difficulty:** choosing furniture that matches the room, fits and stays within budget (Q5, 2:00).
- **Concept and trust:** would use the proposed tool to save time; wants measurements, recommendations, styles and budget options (Q6, part 2, 0:00). Wants realistic previews, accurate dimensions and real prices; prefers phone use (Q7, part 2, 0:38).

### P4
- **Shopping and fit:** bought a study desk about a year earlier, usually shops online (e.g. Kaspi), and filters by budget before comparing style, comfort and affordability. Checks listed dimensions and measures the room; reported never having a fit problem (Q1–Q2, 0:12–0:41).
- **Planning difficulty:** considers appearance, comfort and remaining free space. Uses imagination and online inspiration, not a dedicated planner (Q3–Q4, 1:07–1:25).
- **Main difficulty:** finding furniture that matches style, fits and stays within budget among many options (Q5, 1:47).
- **Concept and trust:** would use the tool to save time; wants measurements, budget-based recommendations and a way to see furniture in the room (Q6, 2:06). Trust depends on real dimensions, correct prices and reliable information; prefers phone because that is where they usually shop (Q7, 2:32).

### P5
- **Shopping and fit:** compares online stores and shops, prices, design, quality and reviews. Measures available space and checks listed dimensions but finds it difficult to imagine furniture scale (Q1–Q2, 0:11–0:46).
- **Planning difficulty:** considers room size, doors, windows and walking space; has not used many room-planning tools and relies on imagination and online pictures (Q3–Q4, 1:19–1:46).
- **Main difficulty:** matching fit, style and budget and comparing many options (Q5, 2:18).
- **Concept and trust:** would try a tool that accepts room dimensions, style and budget; wants multiple layouts, realistic 3D previews and products actually available locally (Q6, 2:47). Trust depends on accurate measurements, realistic imagery, current prices/details, reviews and links to real products. Prefers phone for convenience but says a computer could help detailed planning (Q7, 3:24).

## 4. Findings by hypothesis

Verdicts are qualitative and provisional. Counts below mean “participants whose transcript contains relevant supporting/contradicting evidence,” not prevalence estimates for a wider population. A participant may contribute to more than one side of a finding.

| Hypothesis | Supporting evidence | Contradicting / limiting evidence | Verdict | Effect on requirements |
|------------|--------------------|-----------------------------------|---------|------------------------|
| **H1** Fit uncertainty | P1 reports a chair too wide to fit comfortably under a desk; P2 reports a chair bigger than expected and taking too much space. P3 and P5 describe difficulty imagining scale; P1/P2/P3/P4/P5 all describe checking dimensions or wanting accurate measurements in the proposed tool. | P3 says no serious problem; P4 says they have never experienced a fit problem. No participant reported returning an item. | **Supported for uncertainty and prevention need; mixed for actual fit failures.** 2 concrete past fit issues, 2 further explicit scale-imagination concerns; do not claim frequent returns. | Keep room dimensions, furniture dimensions and visual preview. Make measurement units and item dimensions visible; validate clearances where implemented. |
| **H2** Layout difficulty and acceptance of automatic suggestion | All five describe mental imagining, sketches, online inspiration, or moving furniture rather than using a dedicated planner. All five said they would try/use the proposed tool. P1 explicitly wants to adjust the suggested layout; P2 requests automatic placement; P3–P5 want recommendations/layout options. | These are self-reported preferences for a proposed concept, not observed usability or proof of actual adoption. The participants’ design experience is not documented, so “non-designers” cannot be verified. | **Provisionally supported for perceived difficulty and stated interest; adoption unproven.** | Treat auto-arrangement as an editable starting point. Provide manual adjustment. Validate with task-based usability testing rather than interview intent alone. |
| **H3** Style + budget + explanation | All five explicitly mention budget and style/design as selection criteria and want recommendations tied to budget/style or room context. P1 explicitly asks for an explanation of why an arrangement works. Accurate dimensions/prices are recurring trust conditions; P5 asks for reviews and product links. | Only P1 directly asks for an explanation of why the arrangement works; others focus mainly on accuracy, realism, prices and product information. The full “why recommended” requirement is not independently supported by all five. | **Strong support for style/budget filters; partial support for explanations.** | Keep style and budget filters. Show dimensions, current prices and product source/details. Treat explanation/rationale as a promising feature to test, not a universal validated need. |
| **H4** Browser without installation preferred over mobile app | P5 says a computer could be useful for detailed planning. | P1–P5 all prefer a phone/mobile app for convenience. The interview question asked computer vs mobile, not browser vs installed app, so it does not directly test installation preference. | **Mobile preference contradicts a desktop-first interpretation; the exact browser-without-installation hypothesis remains untested.** | Do not cite these interviews as proof that browser-based access is preferred. Test mobile browser, desktop browser and installed-app expectations separately. A responsive browser may still serve phone users, but that is a design inference, not a finding. |
| **H5** Trust from visible walkway/door clearance | All five mention leaving enough space to move/walk or preserving free space. P5 explicitly considers doors and windows. P1 asks for exact dimensions and an explanation; multiple participants make trust contingent on accurate dimensions. | No participant was directly asked whether visibly enforced walkway/door clearance would increase trust in an AI layout. The evidence supports the importance of usable space, not the causal trust claim. | **Partial support for clearance as a layout requirement; trust effect untested.** | Include visible room boundaries and clearance checks if implemented. In usability tests, ask participants to judge a layout with and without visible clearance feedback and record the reason for trust/distrust. |
| **H6** Sellers/designers would use the tool with clients | None: the transcripts do not identify any participant as a seller or designer and contain no client-workflow evidence. | No explicit contradiction either; the target-user assumption was not tested with an identified professional. | **No evidence / not assessable.** | Keep sellers/designers as an unvalidated secondary target segment. Interview actual furniture sellers/designers or document a real client/pilot agreement before claiming professional demand. |

### Overall finding

The interviews most consistently support the problem of imagining furniture scale and the desire to compare items that fit a room, style and budget. They also show strong *stated* interest in a simple visual planning tool, but do not demonstrate actual adoption, prototype usability, professional demand, or preference for a browser over an installed app. Accurate dimensions and prices are important trust conditions. The value of explicit recommendation explanations and clearance feedback needs direct follow-up testing.

## 5. New requirements / changes suggested by the interviews

These are interview-derived candidates; they should be reconciled with the existing requirements before being treated as accepted scope.

1. **Room and product dimensions:** show room dimensions and each product’s real width/depth/height clearly.
2. **3D preview:** let users inspect how furniture scale and combinations look in the room.
3. **Budget and style filters:** support user-defined budget and style preference; show price and, where possible, total estimated cost.
4. **Editable automatic arrangement:** allow users to adjust the suggested layout rather than treating it as final.
5. **Walkway and opening awareness:** represent doors/windows and preserve practical walking space; test actual clearance rules.
6. **Trustworthy product data:** display current price, product details and links to real listings; reviews were specifically mentioned by P1/P2/P5.
7. **Local availability:** investigate whether recommendations can be purchased in the user’s city (explicitly raised by P5).
8. **Simple input flow and responsive phone use:** keep room-dimension entry easy; all five preferred phone use, while P5 noted a computer may help detailed planning.

## 6. Client agreement

No client agreement or retailer pilot is evidenced in the supplied interview transcripts. Do not treat an interview as a commitment to provide catalogue data or pilot the product.

| Organisation | Contact role | Agreement | Date | Evidence |
|--------------|--------------|-----------|------|----------|
| Not evidenced | Not evidenced | None recorded | — | None supplied |

## 7. Assumption register update

| Assumption | Status after interviews | Next check |
|------------|--------------------------|------------|
| H1 fit uncertainty | Partially supported; two concrete fit problems, broader scale uncertainty | Keep dimensions/preview; gather more incidents and measure returns only if relevant data are available |
| H2 automatic suggestion | Stated interest from five participants; actual adoption and “non-designer” profile not established | Usability tasks; verify participant profiles without identifying them |
| H3 style and budget | Supported in these interviews | Test filters in prototype; rationale feature needs more evidence |
| H4 browser without installation | Not directly tested; all five prefer phone over computer | Ask about installation, mobile browser and desktop browser separately |
| H5 visible clearance increases trust | Walking-space need supported; trust effect untested | Comparative usability test with clearance explanation/visualisation |
| H6 professional use | Not assessed | Interview verified sellers/designers or secure a real pilot/client agreement |
| Users have a laptop/desktop browser with WebGL | Not established; most preferred phone | Record devices and test mobile/desktop compatibility |
| Local store websites provide sufficient structured data for ≥5,000 items | Not tested by interviews | First parser run and catalogue import report (DIP-25) |

## 8. Research quality and follow-up

- The sample contains five short interviews. It is useful for exploratory requirements, not population-level estimates.
- Profiles and demographics are absent, so segment claims cannot be validated.
- The question about trust in H5 was indirect; a focused follow-up question is needed.
- H4 conflates device preference with software delivery preference. Split it into: (a) preferred device; (b) willingness to install an app; (c) willingness to use a browser on mobile/desktop.
- H6 needs a separate professional sample.
- Before final submission, verify consent metadata against the original session records. Do not place names, contact details, or audio recordings in the repository.

## 9. Secondary evidence

Published sources listed in `sources-open-access.md` and `existing-systems.md` are secondary evidence. They must remain distinguishable from the five interviews above. The interviews alone do not validate market size, demand at scale, retailer integration feasibility, or competitor feature coverage.
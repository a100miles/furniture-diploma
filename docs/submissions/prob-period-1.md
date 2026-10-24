# Probation period 1 committee package (24 October 2026)

| Item | Value |
|------|-------|
| Repository | https://github.com/a100miles/furniture-diploma |
| Tag | `prob-period-1` (reviewed `main` snapshot) |
| YouTrack | https://furniture-diploma.youtrack.cloud/projects/DIP |

## Completed work

- **Analysis:** literature review (24 peer-reviewed papers and 2 technical sources), existing-systems comparison, technology comparison, and five exploratory interviews about furniture choices and room planning, with transcripts and a qualitative findings analysis. Participant profiles are unavailable, so the records do not establish that all participants represent the target-user groups. See [relevance-evidence.md](../relevance-evidence.md).
- **Design:** requirements with acceptance criteria, architecture description, system context / use case / component diagrams, and database schema with editable sources.
- **Planning:** backlog DIP-1 through DIP-31, milestones, risks, dependencies, and a verification and evaluation plan.
- **Prototype:** a single Python service with FastAPI catalogue, explained recommendations, auto-layout, validation, and in-memory save/load; React and Three.js room editor. The backend has 35 tests; frontend geometry tests are included in the CI workflow.
- **Catalogue pipeline:** a polite mebel.kz parser and a snapshot of 4,084 items across 10 categories, with an import report. The prototype still uses its separate 25-item demo catalogue.

## Evidence and data limitations

- The five interviews support preliminary qualitative findings; they do not establish population-level demand, actual adoption, prototype usability, or professional demand.
- The supplied records do not contain participant profiles or actual interview dates. Explicit agreement to anonymous notes is recorded for P3; individual yes/no consent confirmations are not recorded for P1, P2, P4, or P5. See the audit in [relevance-evidence.md](../relevance-evidence.md). Do not infer missing information.
- The catalogue currently covers one store and 4,084 items. The 5,000-item, two-store goal is an MVP checkpoint target, not a completed result.
- Existing-systems claims still need hands-on checks for some products.

## Prototype limitations

- The prototype uses a 25-item demo catalogue with illustrative prices; the scraped catalogue is not loaded into its API.
- Furniture is shown as boxes; rotation is limited to 90-degree increments.
- Projects are stored in memory and are lost on backend restart.
- Walkway clearance is a soft rule rather than a hard constraint.
- CLIP ranking is planned, not implemented. Current recommendations use explicit constraints and rule-based scoring.

## Outstanding work

- Check original interview and consent records for missing metadata. If it was not collected or cannot be verified, keep that limitation explicit; do not reconstruct it.
- Complete the supervisor review and feedback log (DIP-12).
- Populate YouTrack and link tasks to pull requests (DIP-11).
- For the MVP checkpoint, add a second store and reach 5,000+ items (DIP-25, FR-31), then load catalogue data into the prototype API.
- Next implementation work includes PostgreSQL persistence (DIP-17), 3D models (DIP-18), hard clearance constraints (DIP-19), and layout benchmarking (DIP-20).

## One-minute ML explanation

The current prototype uses explicit constraints and rule-based scoring; CLIP is planned, not yet implemented. CLIP represents product images and text in a shared embedding space, allowing a text request to retrieve visually relevant furniture. Numeric dimensions and budget must still be checked explicitly. Similarity alone does not guarantee compatibility with furniture already selected.

The planned ranker will be compared with B1: filter by category and price, then sort cheapest first, and with the current rule-based scorer. For 50-100 realistic queries, two team members will independently grade candidates 0, 1, or 2; an interior designer will review disagreements, and agreement will be reported. nDCG@10 measures whether highly relevant items appear near the top, relative to an ideal ordering. Precision@5/10 and hard-constraint satisfaction will also be reported. Beating B1 is an evaluation target, not a result already obtained.

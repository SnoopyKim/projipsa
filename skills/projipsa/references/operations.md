# Operations

## Query

Use Query to answer a project question without changing files.

1. Read the memory index.
2. Read `wiki/project/current-state.md`.
3. Open only directly relevant maintained pages.
4. Follow linked decisions, questions, assumptions, risks, areas, procedures,
   external dependencies, or milestones when relevant.
5. Open raw sources only when a claim needs verification or provenance.
6. Check whether current state contradicts older logs or sources.
7. Answer with confirmed facts first, followed by assumptions, stale risks,
   disputed claims, and open questions.

Do not treat a log as current truth when a maintained page or newer decision
supersedes it.

## Ingest

Use Ingest for a new research artifact, meeting note, user feedback,
conversation output, external article, source document, or field observation.

1. Save the source under `raw/YYYY-MM/` or the established equivalent.
2. Preserve the original as closely as practical. Add provenance metadata only
   when it helps identify origin, date, or scope.
3. Identify affected maintained pages.
4. Update existing pages or create focused new pages.
5. Link new or changed claims to the source.
6. Update the index only when navigation changed.
7. Append the monthly log.

Summarize only project impact in maintained pages. Do not make future agents
read large raw sources by default.

## Update after work

Use Update after a work session, planning session, research pass, delivery,
meeting, review, or handoff.

1. Establish what actually changed and what explicitly did not.
2. Identify the evidence supporting every new confirmed claim.
3. Preserve an ephemeral, imported, or conversation-only artifact under
   `raw/YYYY-MM/`. When evidence already has a stable versioned project path,
   link that path instead of copying it.
4. Update `sources` frontmatter on affected maintained pages.
5. Update `wiki/project/current-state.md`.
6. Update only affected maintained pages.
7. Add or supersede decision pages for meaningful choices.
8. Update assumptions, risks, mitigations, and open questions.
9. Record validation evidence and residual gaps.
10. Append a compact factual monthly-log entry.

Example:

```md
## [2026-07-28] update | Project memory refreshed

- updated: wiki/project/current-state.md
- added: wiki/decisions/2026-07-28-example.md
- evidence: focused tests and reviewed diff
```

Do not turn an unverified implementation claim into confirmed current state.

## Lint

Check:

- missing or invalid frontmatter;
- duplicate page IDs;
- stale active pages;
- important claims without sources;
- orphan maintained pages;
- decisions not reflected in current state;
- assumptions without validation plans;
- risks without mitigation or rationale;
- resolved questions still presented as open;
- duplicate claims likely to drift;
- raw sources edited instead of appended;
- optional page families without a real project need;
- broken relative links.

Report findings first. Fix them only when repair is authorized. Use
`scripts/validate_memory.py` for deterministic structural checks, then apply
judgment for freshness, provenance quality, and semantic contradictions.

## Snapshot

Use Snapshot before a milestone, handoff, long pause, major transition, review,
launch, or restart.

Create or update a milestone page containing:

- scope;
- current state;
- completed work;
- explicitly incomplete or excluded work;
- validation and evidence reviewed;
- active assumptions and risks;
- open questions and important decisions;
- the exact next useful action.

Link it from the index when it should remain discoverable and append the
monthly log.

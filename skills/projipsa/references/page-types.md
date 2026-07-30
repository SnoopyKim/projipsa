# Page Types

## Principle

Every project needs operating memory. Not every project needs the same page
families. Use the universal core first and add optional families only when the
project's actual shape requires them.

## Frontmatter

Every maintained wiki page starts with YAML frontmatter:

```yaml
---
id: decision.example.2026-07-28
type: decision
status: active
confidence: confirmed
updated: 2026-07-28
sources:
  - raw/2026-07/source-example.md
related:
  - project.current-state
supersedes: []
superseded_by: []
---
```

Required fields:

- `id`: stable unique ID, lower-case and dot-delimited.
- `type`: a page type selected for this project.
- `status`: `active`, `draft`, `stale`, `superseded`, or `archived`.
- `confidence`: `confirmed`, `assumed`, `inferred`, or `disputed`.
- `updated`: ISO date of the last meaningful content update.
- `sources`: project-local regular-file paths, HTTP(S) sources, or maintained
  pages supporting the page. A confirmed page's source chain must eventually
  reach primary project evidence; self-reference or a maintained-page-only
  cycle is not evidence.
- `related`: related page IDs.

Templates ship `confidence: inferred` because a template cannot know the
project's evidence. Raise a page to `confirmed` only in the same edit that lists
its primary evidence in `sources`. A `confirmed` page with an empty `sources`
list is a validation error, not an acceptable interim state.

Optional fields include `owner`, `supersedes`, `superseded_by`, `depends_on`,
and `blocks`. Use `projipsa_adoption: true` only on the one decision that
records adoption of Projipsa; this marker lets migrated projects preserve an
equivalent decision's stable ID and path.

## Universal core

### Project

- `wiki/project/overview.md`: purpose, audience, scope, goals, and non-goals.
- `wiki/project/current-state.md`: current status, active defaults, latest
  validation, and next work.
- `wiki/project/glossary.md`: optional canonical local vocabulary.

### Decision

Preserve the decision, context, alternatives, reasoning, consequences, and
supersession links. Never delete a decision because it changed.

### Question

Track unresolved tradeoffs or unknowns. Small questions may share
`wiki/questions/open-questions.md`; promote questions that block or affect
multiple decisions.

### Log

Use `logs/YYYY-MM.md` for append-only chronology. Logs never replace current
state.

## Optional page families

- **Area**: a major workstream, domain, responsibility, initiative, audience,
  component, research theme, or project surface.
- **Assumption**: an unverified claim that current planning relies on.
- **Risk**: an active threat with impact, likelihood, mitigation, and signals.
- **Procedure**: repeatable operating steps with validation and recovery.
- **External**: a party, tool, contract, service, source, API, or dependency.
- **Milestone**: a launch, event, checkpoint, handoff, pause, or snapshot.
- **Delivery**: the current contract and resumable state for one substantial
  explicitly delegated engagement. Keep history in its change log and project
  chronology; keep draft or changed contracts distinct from confirmed ones;
  archive or supersede the page when the engagement closes.

## Page ID conventions

- Project overview: `project.overview`
- Current state: `project.current-state`
- Area: `area.<slug>`
- Decision: `decision.<slug>.<yyyy-mm-dd>`
- Projipsa adoption: `decision.projipsa-adoption.<yyyy-mm-dd>`
- Assumption: `assumption.<slug>`
- Risk: `risk.<slug>`
- Procedure: `procedure.<slug>`
- External dependency: `external.<slug>`
- Question: `question.<slug>`
- Milestone: `milestone.<slug>`
- Delivery: `delivery.<slug>`

Prefer stable IDs over path-derived IDs when pages may move.

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

Required, because a page without them cannot be linked, judged stale, or
believed:

- `id`: stable unique ID, lower-case and dot-delimited.
- `updated`: ISO date of the last meaningful content update.
- `sources`: project-local regular-file paths, HTTP(S) sources, or maintained
  pages supporting the page. A confirmed page's source chain should eventually
  reach primary project evidence; self-reference is a validation error, and a
  maintained-page-only cycle draws a warning. On a page that is rewritten over
  time, this lists the evidence for the claims the page makes now, so an entry
  leaves with the claim it supported; it is not an append-only ledger of
  everything the page once said.

Stated when it departs from the default, and checked whenever present:

- `type`: a page type selected for this project. Read from the page's directory
  when the page does not state it, so a page under `wiki/decisions/` is a
  decision unless it names itself something else.
- `status`: `active`, `draft`, `stale`, `superseded`, or `archived`. Defaults to
  `active`.
- `confidence`: `confirmed`, `assumed`, `inferred`, or `disputed`. Defaults to
  `inferred`, so a page claims more than that only by saying so.
- `related`: related page IDs. Write it when a link helps a reader; an empty
  list says nothing and is better left out.

Most templates ship `confidence: inferred` because a template cannot know the
project's evidence. Templates for assumptions, questions, risks, and deliveries
ship `confidence: assumed`, because those page types usually track planning
claims, unresolved unknowns, threats, or delegated state before they are
confirmed. Raise a page to `confirmed` only in the same edit that lists its
primary evidence in `sources`. A `confirmed` page with an empty `sources` list
is a validation error, not an acceptable interim state.

Optional fields include `owner`, `supersedes`, `superseded_by`, `depends_on`,
and `blocks`. Use `projipsa_adoption: true` only on the one decision that
records adoption of Projipsa; this marker lets migrated projects preserve an
equivalent decision's stable ID and path.

## Universal core

### Project

- `wiki/project/overview.md`: purpose, audience, scope, goals, and non-goals.
- `wiki/project/current-state.md`: current status, active defaults, latest
  validation, and next work. A replaced page, not an appended one; [the Update
  operation](operations.md) states when a line leaves and where it goes. Keep it
  short enough to stay worth reading at the start of every session.
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

Monthly is the default, not the only unit. Choose a finer one when a month's
file grows past a comfortable read, or when several branches, worktrees, or
sessions append at the same time: a shared append target is a conflict target,
and day granularity does not help when two writers finish on the same day. The
unit that removes the collision is one file per writer.

| Unit | Path | Use when |
|---|---|---|
| month | `logs/2026-08.md` | one writer at a time; the default |
| day | `logs/2026-08-12.md` | a month's chronology outgrows one read |
| session | `logs/2026-08/2026-08-12-<slug>.md` | parallel writers append concurrently |

Keep one unit per project rather than mixing them, and link the chronology from
`index.md` — the current file, or the directory holding it when there are too
many to list. The memory validator accepts every form above, and checks nested
chronology files exactly like flat ones.

A project that already kept chronology under `logs/<subdirectory>/` was not
being checked there before: the validator walked only the top level, so those
files were invisible to its link, placeholder, and empty-file checks. They are
checked now, so the first run after upgrading can report findings in files that
have been sitting in the tree unchanged. Relative links are the usual one,
because a path that resolved from `logs/` does not resolve from one level
deeper.

## Optional page families

- **Area**: a major workstream, domain, responsibility, initiative, audience,
  component, research theme, or project surface. Current state names the
  trigger: when one of its sections swells past the rest, the workstream that
  section describes has outgrown a line on a briefing page and wants a page of
  its own. Standing facts about that workstream move there, current state keeps
  the link, and the branch that owns the workstream owns the page.
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

# Project Memory Instructions

## Reading order

1. Read `index.md`.
2. Read `wiki/project/current-state.md`.
3. Read a linked active delivery page when the requested work belongs to it.
4. Open only other relevant maintained pages.
5. Open raw sources only for evidence or provenance.

## Maintenance rules

- Map project paths by role: Evidence, Events, Synthesis, and rebuildable Views.
  By default, `raw/**` is retained Evidence, `logs/**` is append-only Events,
  and `wiki/**` is maintained Synthesis.
- During normal maintenance, never overwrite or delete retained raw Evidence.
  Explicit Compact may remove a whole artifact only after an active-evidence
  check, exact path plan, recoverability review, and approval.
- When the project keeps replaceable current visuals, name their asset location
  and retention rule here. Keep temporary or reproducible captures out of
  project memory.
- Keep current state concise and link to detailed pages. Replace it rather than
  appending: a line that no longer changes what the next session does moves to
  chronology, a delivery, a decision, a milestone, or an area page.
- When branches, worktrees, or sessions run in parallel, update `index.md`,
  current state, and open questions from the integrating branch after merge;
  each parallel writer appends to its own log file. Ask Projipsa to finish or
  integrate after a merge to get that write.
- Give maintained pages stable IDs and required frontmatter.
- Mark assumptions, disputes, staleness, and supersession explicitly.
- Add optional page families only when the project needs them.
- Keep one maintained delivery page for each active substantial delegated
  engagement; do not turn it into a transcript.
- Preserve project implementation during docs-only work.

## Updates

When project-memory maintenance is in scope, update affected maintained pages,
append the chronology log, validate links and frontmatter, and report remaining
unknowns. Do not infer Maker approval or acceptance.

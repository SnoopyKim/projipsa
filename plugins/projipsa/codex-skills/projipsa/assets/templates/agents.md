# Project Memory Instructions

## Reading order

1. Read `index.md`.
2. Read `wiki/project/current-state.md`.
3. Find relevant decisions, constraints, prior failures, and open questions.
4. Open evidence when a claim matters; verify volatile facts against current state.

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
  chronology, a decision, a milestone, or an area page.
- When branches, worktrees, or sessions run in parallel, update `index.md`,
  current state, and open questions from the integrating branch after merge;
  each parallel writer appends to its own log file. Ask Projipsa to finish or
  integrate after a merge to get that write.
- Give maintained pages stable IDs and required frontmatter.
- If evidence checkpoints are used, preserve `.projipsa/evidence-baseline.json`
  as review state. Only checkpoint pages whose evidence was actually reviewed;
  read-only queries never clear review candidates.
- Mark assumptions, disputes, staleness, and supersession explicitly.
- Add optional page families only when the project needs them.
- Preserve useful decisions, outcomes, and corrections with their evidence and
  applicability; avoid storing complete transcripts as current understanding.
- Preserve project implementation during docs-only work.

## Updates

When project-memory maintenance is in scope, update affected maintained pages,
append the chronology log, validate links and frontmatter, and report remaining
unknowns. Do not infer Maker approval or acceptance.

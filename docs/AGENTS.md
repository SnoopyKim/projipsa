# Project Memory Instructions

## Reading order

1. Read `index.md`.
2. Read `wiki/project/current-state.md`.
3. Open only other relevant maintained pages.
4. Open preserved sources only for evidence or provenance.

## Maintenance rules

- Treat `wiki/**` as maintained synthesis.
- Treat `raw/**` as preserved source material; never rewrite it.
- Treat `logs/**` as append-only chronology, not current truth.
- Keep current state concise and link to detailed pages.
- Give maintained pages stable IDs and required frontmatter.
- Mark assumptions, disputes, staleness, and supersession explicitly.
- Add optional page families only when this project actually needs them.
- Preserve project implementation during docs-only work.

## This memory is public

`SnoopyKim/projipsa` is a public repository. Everything written here is visible
to anyone reading the repository, and to anyone who installs the Plugin from
source. Write accordingly:

- Prefer linking a stable path — a merged pull request, a commit, a CI run, or
  a file under `plugins/` — over copying its contents into `raw/`.
- When something must be preserved verbatim, preserve the artifact, not the
  conversation that produced it.
- Write for a public reader. Record decisions, evidence, and open questions.
  Do not record assessments of people, or of other products and tools.

These rules constrain what enters memory; they do not weaken provenance. For
this project a cited pull request or repository path is stronger evidence than
a pasted excerpt, because it is versioned and cannot be silently edited.

## Updates

When project-memory maintenance is in scope, update affected maintained pages,
append the monthly log, validate links and frontmatter, and report remaining
unknowns. Do not infer Maker approval or acceptance.

# Repair and Upgrade

Use this workflow only after a project has adopted Projipsa. First creation and
adoption of general documentation belong to Projipsa Init; ongoing contract
repair and upgrades belong to Projipsa Repair.

## Preserve the adopted project

- Treat `<memory-root>/AGENTS.md` as the project's memory profile. Plugin
  defaults fill gaps; they do not erase intentional local conventions.
- Keep stable IDs, working paths, useful optional pages, chronology units, and
  surrounding root instructions.
- Repair navigation, frontmatter, provenance, pointer blocks, and missing core
  responsibilities in place.
- Do not append duplicate adoption or initialization entries.
- Do not normalize a tree merely because a newer template is smaller.
- Do not remove raw files or assets during Repair. Size cleanup belongs to the
  separately approved Compact workflow.

An installed plugin update never rewrites adopter memory. Repair requires an
explicit user request or an already authorized project-memory maintenance task.

## Upgrade from 0.3.x or 0.4.x

Treat the upgrade as a capability audit, not a schema rewrite. Project memory
does not carry a reliable installed-plugin version, so compare behavior with
the current contract instead of inferring a version from fields or paths.

1. Preserve `wiki/project/overview.md`,
   `wiki/questions/open-questions.md`, and stated `type`, `status`,
   `confidence`, or `related` fields. Optional does not mean deprecated.
2. Merge current-state eviction, single-writer ownership, post-merge Integrate,
   and the Evidence/Events/Synthesis/Views role model into the project's
   existing profile only where they solve a real gap.
3. Preserve monthly chronology by default. Switch only when concurrent writers
   make one append target unsafe; record a deliberate cutover and leave old
   logs in place.
4. Apply current-state eviction claim by claim. Move history only to an
   existing or justified destination and prune a source only with the claim it
   supported.
5. Update the marked root pointer block only when its discovery path or layer
   rules changed, preserving every surrounding instruction.
6. Append one upgrade chronology entry only when files actually changed.

For 0.5.0, review ingestion policy as well: stable artifacts should be linked,
durable unique evidence retained, replaceable visuals managed by project
policy, and temporary or reproducible captures kept out of memory. This policy
changes future ingestion; it does not retroactively authorize deletion.

## Upgrade to 0.6.0

The plugin now provides memory management only. Outsource is no longer a
public Skill. Preserve existing delivery pages, their stable IDs, source
artifacts, and chronology. Remove obsolete invocation guidance from active
project instructions only within authorized Repair; do not run old contracts
or erase their records. For new handoffs, use a milestone or the project's
existing task artifact.

## Validate

Run the memory validator, inspect warnings, inspect the documentation diff, and
report preserved customizations separately from repaired findings. A no-op is
a successful upgrade when the adopted tree already satisfies the contract.

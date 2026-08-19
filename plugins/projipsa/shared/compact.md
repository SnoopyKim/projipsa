# Projipsa Compact Workflow

Audit and deliberately reduce the cost of an adopted project's memory without
erasing the evidence needed to understand or verify it. Compact is for
infrequent cleanup of oversized synthesis, repeated captures, obsolete visual
iterations, and other accumulated artifacts. It does not create or approve
project decisions.

The explicit host invocations are `$projipsa:compact` in Codex and
`/projipsa:compact` in Claude Code.

This is an explicit, infrequent workflow. Do not load or run it merely because
a memory tree exists or because a file is large. Each host adapter enforces the
explicit-only policy mechanically.

## Start with the project profile

1. Read repository instructions, the memory index, current state, and the
   memory root's `AGENTS.md`.
2. Treat that `AGENTS.md` as the project profile for Evidence, Events,
   Synthesis, Views, and replaceable visual assets. Do not impose a new folder
   schema when the project already has a coherent mapping.
3. Inspect version-control status and preserve unrelated work.
4. Establish the memory root and repository baseline. Never audit a broad home
   directory or an unresolved path.

## Audit before proposing change

Audit is read-only. The default response to a Compact invocation is an Audit,
not an Apply.

Run the bundled analyzer when available:

```bash
python3 <plugin-root>/codex-skills/compact/scripts/audit_compaction.py <memory-root>
```

The analyzer reports size, exact image duplicates, local image references,
Git recoverability, and conservative filename groups for semantic review. A
matching hash proves byte identity, not which copy should survive. A filename
group proves neither duplicate meaning nor obsolescence.

Supplement the deterministic report with judgment:

- identify synthesis that repeats chronology or no longer steers work;
- trace every candidate artifact to the active claims, decisions, and
  verification records it may support;
- visually inspect comparison boards, crops, screenshots, and edited variants
  before calling them semantic duplicates;
- distinguish a replaceable current visual from durable historical evidence;
- flag secrets or private data without reproducing them in the report.

Never delete the only evidence for an active claim. Never infer that an old
capture is obsolete solely from its age, size, name, or hash relationship.

## Produce an exact plan

After Audit, propose a plan with one row per exact path:

| Path | Proposed action | Reason | Evidence dependency | Recoverability | Bytes |
|---|---|---|---|---|---:|

The exact plan must also name:

- the repository baseline SHA when Git provides one;
- every maintained page or reference that must change with the artifact;
- the retained replacement or canonical artifact for a duplicate;
- candidates deliberately kept because their meaning is uncertain;
- expected working-tree bytes removed, kept separate from Git-history size.

Do not use directory-wide globs, approximate descriptions, or “delete all old
screenshots” as an approval target. Deduplication is not permission to rewrite
or recompress a surviving original.

## Require explicit approval for Apply

Do not Apply without explicit approval of the exact plan. Approval of an Audit,
general cleanup, or a size goal is not deletion approval.

Before Apply, recheck status, baseline, paths, hashes, and references. Stop if
they drifted. An unmodified tracked artifact is recoverable from the recorded
Git baseline; preserve a tracked file whose current bytes differ from that
baseline unless the exact current version has its own recovery path. Untracked
artifacts require a verified backup or separate explicit approval that
acknowledges they are unrecoverable. Do not silently create a backup in a
location the user did not authorize.

Apply only the approved path actions. Preserve unrelated work, do not broaden
the list based on newly noticed candidates, and never rewrite product history
to make the smaller tree look canonical in retrospect.

## Verify the compacted memory

After Apply:

1. rerun the analyzer and memory validator;
2. check every changed link and every active claim that depended on a removed
   artifact;
3. inspect the exact diff and version-control status;
4. report actual working-tree bytes removed and note that Git history is
   unchanged unless separately rewritten;
5. append one compact chronology entry only when project-memory maintenance was
   authorized and files changed.

The same Audit on unchanged inputs should be idempotent. A repeated Apply with
the same plan should have nothing left to do, not discover a broader deletion
scope.

# Compaction Review Guide

Use this guide when deterministic inventory is not enough to decide whether a
candidate should be kept.

## Candidate classes

- **Exact duplicate**: byte-identical files. Choose a survivor from references,
  provenance, and project convention; hash equality alone does not choose it.
- **Semantic duplicate**: different bytes representing substantially the same
  state. Comparison boards, crops, resized exports, and edited screenshots need
  visual review.
- **Superseded view**: a replaceable presentation of current state whose newer
  canonical view is identified and linked.
- **Durable evidence**: supports an active claim, decision, acceptance result,
  incident, or otherwise costly-to-reconstruct fact. Preserve it or establish
  an approved equivalent.
- **Reproducible intermediate**: generated during exploration and cheap to
  recreate from durable inputs. It may be a removal candidate if nothing live
  references it.

## Evidence dependency check

For each proposed removal, search maintained pages, logs, source lists, code,
and project instructions. Ask:

1. What claim or decision would become harder to verify?
2. Is this the only evidence for that claim?
3. Does the proposed survivor show the same state and context?
4. Is provenance preserved after references change?
5. Would a future incident, audit, or design comparison need the old state?

Uncertainty means keep and report, not delete.

## Recovery classes

- **Tracked at baseline**: recoverable from the recorded Git SHA without
  rewriting repository history.
- **Tracked but modified**: preserve the current user change; the baseline may
  not contain it.
- **Untracked with verified backup**: apply only within the separately approved
  plan.
- **Untracked without backup**: block deletion unless the user separately
  approves the acknowledged unrecoverable loss.

Working-tree cleanup does not reduce existing Git history. History rewriting is
a different destructive operation and is never implied by Compact.

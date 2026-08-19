---
id: project.overview
type: project
status: active
confidence: confirmed
updated: 2026-08-19
sources:
  - README.md
  - CONTRIBUTING.md
  - logs/2026-08.md
  - plugins/projipsa/codex-skills/projipsa/references/memory-contract.md
  - plugins/projipsa/codex-skills/compact/scripts/audit_compaction.py
  - plugins/projipsa/codex-skills/outsource/references/execution-strategies.md
  - plugins/projipsa/shared/outsource.md
  - plugins/projipsa/.claude-plugin/plugin.json
  - plugins/projipsa/.codex-plugin/plugin.json
  - wiki/decisions/2026-08-02-host-adapter-separation.md
  - wiki/decisions/2026-08-17-explicit-memory-compaction.md
  - https://docs.x.ai/build/features/skills-plugins-marketplaces
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - https://www.aibuilderclub.com/blog/graph-engineering-guide-2026
related:
  - project.current-state
  - decision.host-adapter-separation.2026-08-02
  - decision.explicit-memory-compaction.2026-08-17
---

# Project Overview

## Purpose

An agent rebuilds its understanding of a project at the start of every session
and discards it at the end. Two costs follow. The context is re-derived every
time, and substantial work cannot be delegated at all, because work spanning
sessions has nothing to resume from.

Projipsa answers both with one mechanism. It keeps the project's understanding
in maintained Markdown that an agent updates, and then lets substantial work be
delegated against that memory under a contract with explicit verification and
Maker acceptance.

Memory and delivery are not two products. **The memory is the durable shared
state the delegated work runs on.** Agent orchestration normally keeps such
state inside a process, so it ends with the run. Projipsa keeps it in version
control, so it survives sessions, hosts, and people.

Running on Codex, Claude Code, and Grok Build is a distribution constraint that
follows from the Maker working across multiple hosts. It is not the purpose. This page
previously stated it as the purpose; the correction and its origin are in the
2026-08-03 log entry.

## Design lineage

- The memory layer follows the LLM-wiki pattern: an agent incrementally
  maintains a synthesized Markdown wiki over retained evidence, so
  understanding compounds instead of being rediscovered per query. Normal
  maintenance never rewrites evidence; explicit Compact may remove a whole
  artifact under a separately approved, recoverable plan.
- The delivery layer takes its vocabulary from agent loop design and from
  multi-node agent graphs, where specialized nodes pass shared state along
  explicit edges. Projipsa's contribution is not the topology. It is answering
  where that shared state lives once the run is over.

The correspondence is visible in the shipped contract rather than only in
framing. `memory-contract.md` defines the Evidence, Events, Synthesis, and Views
roles and forbids a View from being a fact's only home.
`execution-strategies.md` escalates
direct → sequential → parallel → graph and adds a graph only when explicit
routing is required for correctness, governance, or recovery.
`shared/outsource.md` designates one `wiki/deliveries/<slug>.md` page as an
engagement's durable state and requires linking canonical pages instead of
duplicating them.

## Scope

- Four portable Skills: `projipsa` for everyday memory and repair,
  `projipsa-init` for first adoption, `compact` for explicit memory compaction,
  and `outsource` for substantial delivery.
- A source-backed memory model of Evidence, Events, Synthesis, and rebuildable
  Views, mapped to each project's established paths.
- Durable delivery state for a delegated engagement, kept in that same layout.
- Two deterministic validators: one for the package contract across hosts, one
  for a project's memory tree.

## Non-goals

- Runtime infrastructure. Projipsa requires no environment variables,
  database, background daemon, MCP server, or hosted state service.
- Execution orchestration. Projipsa selects a topology and names accountable
  roles, but does not ship a runtime, scheduler, or agent framework.
- Replacing a host's normal workflow for ordinary, bounded work.
- Acting on the Maker's behalf. Recommending is in scope; approving,
  accepting, and authorizing are not.

## Audience And Stakeholders

The primary audience is the Maker, working across Codex, Claude Code, and Grok
Build.
Secondary audience is anyone installing the Plugin from a marketplace or a
source checkout.

## Success

- A project that adopted Projipsa can be resumed by an agent that was not
  present for the earlier work.
- A delegated engagement survives a pause, a session boundary, and a change of
  host without losing its contract, evidence, or next action.
- Claims in memory can be traced to evidence.
- Accumulated memory can be audited and compacted without silently deleting the
  only evidence for a live claim.
- The same request produces the same workflow on any supported host.

## Operating Constraints

- Three hosts read two thin adapter dialects that point to one shared workflow
  body per Skill. Grok Build intentionally reuses Claude Code compatibility;
  adapter divergence stays small and mechanical.
- Claude Code copies a plugin's root into a local cache with no ignore
  mechanism, so only `plugins/projipsa/` may hold shipped content.
- Validators use the Python standard library only, and must run on Python 3.9.

---
id: project.overview
type: project
status: active
confidence: confirmed
updated: 2026-07-31
sources:
  - README.md
  - plugins/projipsa/.claude-plugin/plugin.json
related:
  - project.current-state
---

# Project Overview

## Purpose

Projipsa is a project butler distributed as one Plugin for both Codex and
Claude Code. It helps an agent understand an existing project, keep its
operating context current, and manage substantial work through verified review
and handoff.

It exists because the same person works across more than one agent host, and
wants one workflow rather than one per host.

## Scope

- Three portable Skills: `projipsa` for everyday project memory,
  `projipsa-init` for explicit onboarding and repair, and `outsource` for
  substantial delivery.
- A source-backed memory layout of maintained wiki pages, preserved sources,
  and append-only monthly logs.
- Two deterministic validators: one for the package contract across hosts, one
  for a project's memory tree.

## Non-goals

- Runtime infrastructure. Projipsa requires no environment variables,
  database, background daemon, MCP server, or hosted state service.
- Replacing a host's normal workflow for ordinary, bounded work.
- Acting on the Maker's behalf. Recommending is in scope; approving,
  accepting, and authorizing are not.

## Audience And Stakeholders

The primary audience is the Maker, working across Codex and Claude Code.
Secondary audience is anyone installing the Plugin from the SnoopyDev
marketplace.

## Success

- The same request produces the same workflow on either host.
- A project that adopted Projipsa can be resumed by an agent that was not
  present for the earlier work.
- Claims in memory can be traced to evidence.

## Operating Constraints

- Both hosts read one shared `SKILL.md` per Skill, so per-host divergence must
  stay small and mechanical.
- Claude Code copies a plugin's root into a local cache with no ignore
  mechanism, so only `plugins/projipsa/` may hold shipped content.
- Validators use the Python standard library only, and must run on Python 3.9.

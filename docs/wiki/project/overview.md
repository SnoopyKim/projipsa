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
  - decision.claude-code-only.2026-07-31
---

# Project Overview

## Purpose

Projipsa is a project butler distributed as one Claude Code Plugin. It helps an
agent understand an existing project, keep its operating context current, and
manage substantial work through verified review and handoff.

It exists because project context that lives only in a conversation is lost at
the end of it, and the next agent starts from nothing.

The host scope was narrowed to Claude Code alone on 2026-07-31. See
[the host scope decision](../decisions/2026-07-31-claude-code-only.md).

## Scope

- Three Skills: `projipsa` for everyday project memory, `projipsa-init` for
  explicit onboarding and repair, and `outsource` for substantial delivery.
- A source-backed memory layout of maintained wiki pages, preserved sources,
  and append-only monthly logs.
- Two deterministic validators: one for the package contract, one for a
  project's memory tree.

## Non-goals

- Runtime infrastructure. Projipsa requires no environment variables,
  database, background daemon, MCP server, or hosted state service.
- Replacing a host's normal workflow for ordinary, bounded work.
- Acting on the Maker's behalf. Recommending is in scope; approving,
  accepting, and authorizing are not.

## Audience And Stakeholders

The primary audience is the Maker, working in Claude Code. Secondary audience
is anyone installing the Plugin from the SnoopyDev marketplace.

## Success

- A project that adopted Projipsa can be resumed by an agent that was not
  present for the earlier work.
- Claims in memory can be traced to evidence.
- The Skill that fits a request is the one the host loads.

## Operating Constraints

- Claude Code copies a plugin's root into a local cache with no ignore
  mechanism, so only `plugins/projipsa/` may hold shipped content.
- `disable-model-invocation` in `SKILL.md` frontmatter is the only mechanical
  loading-policy gate the package has.
- Root `AGENTS.md` holds the canonical memory-pointer block and root
  `CLAUDE.md` imports it, because Claude Code never reads `AGENTS.md` itself.
- Validators use the Python standard library only, and must run on Python 3.9.

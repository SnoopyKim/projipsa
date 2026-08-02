---
name: projipsa
description: Query and maintain source-backed project memory for a project that has adopted Projipsa. Use when the user invokes $projipsa:projipsa, or asks for current project context, source ingestion, a post-work memory update, memory lint or repair, or a milestone, pause, handoff, or restart snapshot. May load implicitly for project briefing or memory lookup; implicit use remains read-only, while ingestion, update, repair, and snapshot require authorized write scope.
---

# Projipsa for Codex

Read the [shared Projipsa workflow](../../shared/projipsa.md) completely, then
follow it. This is the Codex adapter; its invocation policy lives in
`agents/openai.yaml`.

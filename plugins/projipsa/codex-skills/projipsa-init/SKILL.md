---
name: projipsa-init
description: Initialize, migrate, audit, or repair Projipsa project memory in an existing project. Use when the user explicitly invokes $projipsa:projipsa-init or explicitly asks to adopt, install, migrate, or repair Projipsa documentation. Treat initialization as docs-only unless the user expands the scope. Do not invoke merely because project memory would be useful.
---

# Projipsa Init for Codex

Read the
[shared Projipsa Init workflow](../../shared/projipsa-init.md) completely, then
follow it. This is the Codex adapter; `agents/openai.yaml` keeps the workflow
explicit-only while still allowing direct `$projipsa:projipsa-init` invocation.

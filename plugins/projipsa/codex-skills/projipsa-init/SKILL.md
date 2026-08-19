---
name: projipsa-init
description: Initialize Projipsa project memory or adopt an existing project's general documentation into it. Use when the user explicitly invokes $projipsa:projipsa-init or explicitly asks for first adoption. Treat initialization as docs-only unless the user expands the scope. Do not invoke merely because project memory would be useful, and do not use Init to repair or upgrade an already adopted memory root.
---

# Projipsa Init for Codex

Read the
[shared Projipsa Init workflow](../../shared/projipsa-init.md) completely, then
follow it. This is the Codex adapter; `agents/openai.yaml` keeps the workflow
explicit-only while still allowing direct `$projipsa:projipsa-init` invocation.

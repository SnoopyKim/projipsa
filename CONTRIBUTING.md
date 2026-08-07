# Contributing to Projipsa

This document covers the repository itself. For what Projipsa is and how to use
it, see the [README](README.md).

## Repository layout

Installing the Plugin copies its plugin root into a local cache, and Claude Code
has no ignore mechanism for that copy. The ship boundary is therefore a
directory boundary:

```text
plugins/projipsa/            the shipped plugin root — everything users get
  .codex-plugin/             Codex manifest
  .claude-plugin/            Claude Code manifest
  codex-skills/              Codex adapters, plus the canonical references,
                             templates, and scripts both hosts link to
  claude-skills/             Claude Code adapters
  shared/                    host-neutral workflow body, one per Skill

.agents/plugins/             Codex development marketplace manifest
.claude-plugin/              Claude Code development marketplace manifest
docs/                        this project's own Projipsa memory
scripts/  tests/             validators and their tests
.github/                     CI
CONTRIBUTING.md  README.md  LICENSE
```

Only `plugins/projipsa/` ships. Everything else stays in the repository. This is
what lets the project adopt Projipsa on itself: `docs/` can hold real memory
without being copied to everyone who installs the Plugin. See
[the ship boundary decision](docs/wiki/decisions/2026-07-30-plugin-ship-boundary.md).

Note the two `.claude-plugin/` directories. The one at the repository root is a
*marketplace* manifest for local development installs; the one inside
`plugins/projipsa/` is the *plugin* manifest. They are different files with
different schemas.

## The `skills/` invariant

**The package must never contain a directory named `plugins/projipsa/skills/`,
for either host.** This is the single most important layout rule here, and it is
not obvious.

Claude Code *adds* its manifest-declared Skill directory to the default `skills/`
scan rather than replacing it. While Codex adapters lived at `skills/`,
`claude plugin details projipsa` reported six Skills — two per public name.
Codex behaves the opposite way: it resolves only the declared path and ignores a
sibling `skills/` entirely.

Only one host scans `skills/` implicitly, and only the other one can be moved
off it, so the fix is to leave the name unused. Each host gets its own directory:

- `.codex-plugin/plugin.json` declares `"skills": "./codex-skills/"`
- `.claude-plugin/plugin.json` declares `"skills": "./claude-skills/"`

`scripts/validate_package.py` fails if a `skills/` directory exists, if either
manifest declares `./skills/`, or if both manifests name the same directory. Two
tests cover those cases. See
[the host adapter decision](docs/wiki/decisions/2026-08-02-host-adapter-separation.md).

## Adapters and shared workflows

Each public Skill has one thin adapter per host plus one shared workflow body:

```text
codex-skills/<name>/SKILL.md          Codex adapter
codex-skills/<name>/agents/openai.yaml  Codex loading policy + interface
claude-skills/<name>/SKILL.md         Claude Code adapter
shared/<name>.md                      the workflow both adapters load
```

Adapters exist because the two hosts express loading policy incompatibly. Codex
uses `allow_implicit_invocation` in `agents/openai.yaml`; Claude Code uses
`disable-model-invocation` in the adapter's frontmatter. Neither key belongs in
the other host's tree, and the validator enforces that separation.

Keep adapters thin. Workflow content belongs in `shared/`. Adding a Skill means
declaring its loading policy once in `SKILL_POLICY` in
`scripts/validate_package.py`, not editing several parallel constants.

Canonical references, templates, and `validate_memory.py` currently live under
`codex-skills/projipsa/`, and Claude Code readers follow `../codex-skills/...`
links to reach them. Keeping one copy is deliberate; moving them to a
host-neutral home is deferred, not decided against.

## Validation

The validators require Python 3.9 or newer and otherwise use only the standard
library.

```bash
python3 scripts/validate_package.py
python3 -m unittest discover -s tests
claude plugin validate ./plugins/projipsa --strict
```

`scripts/validate_package.py` checks cross-host alignment. It scans the shipped
tree and the repository README for prose, links, and Skill contracts, and it
additionally reads the two development marketplace manifests at the repository
root. Nothing under `docs/` is in scope — memory content must never gate package
validation. Specifically it checks:

- shared manifest fields, semantic versioning, and matching display names;
- the `skills/` invariant and one isolated adapter per host per Skill;
- loading policy agreement between `agents/openai.yaml` and adapter frontmatter;
- both host invocations documented in every adapter description, every shared
  workflow, and the README;
- the load-bearing guardrail phrases each Skill contract must keep;
- the two development marketplace manifests;
- required references, templates, and scripts;
- templates that would ship `confidence: confirmed` with empty `sources`;
- broken relative links and unresolved `[TODO:` markers.

`tests/test_memory_fixture.py` builds the minimum useful core from the shipped
templates and requires the shipped memory validator to accept it, so a template
cannot drift out of contract with its own validator.

The memory validator is separate and owns everything under a memory root:

```bash
python3 plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py docs
```

Its root-pointer checks are known to be incomplete; the reproduced gaps are
recorded in [open questions](docs/wiki/questions/open-questions.md).

GitHub Actions runs the package validator and the test suite on Python 3.9 and
3.13.

## This project's own memory

The repository uses Projipsa on itself. Start at [docs/index.md](docs/index.md),
then read `docs/wiki/project/current-state.md`. The rules for maintaining it are
in `docs/AGENTS.md`.

The memory root is public, so prefer citing a stable path — a merged pull
request, a commit, a file under `plugins/` — over copying content into `raw/`.

## Before publishing

- Bump the version in both host manifests. The installed copy is version-pinned,
  so an unbumped edit never reaches an installed plugin.
- Run all three commands under [Validation](#validation).
- Validate each public Skill with the host Skill validators, and the package
  with the Codex plugin validator.
- Update `docs/wiki/project/current-state.md` and append the monthly log.

## Provenance

The `outsource` Skill was integrated from
[`SnoopyKim/Outsource`](https://github.com/SnoopyKim/Outsource) at commit
`c4a5292e9579b67ecf6eda74558a9785f6305c77`. That repository may remain as a
temporary compatibility and migration surface, but Projipsa is the intended
canonical home for the capability.

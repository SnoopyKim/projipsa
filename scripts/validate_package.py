#!/usr/bin/env python3
"""Validate cross-host Projipsa package alignment."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
SKILL_ROOT = ROOT / "skills"
TEMPLATE_ROOT = SKILL_ROOT / "projipsa" / "assets" / "templates"

# One declaration per public Skill. Adding a Skill means declaring its
# host-loading policy here, not editing several parallel constants.
SKILL_POLICY = {
    "projipsa": {"implicit": True},
    "projipsa-init": {"implicit": False},
    "outsource": {"implicit": True},
}
EXPECTED_SKILLS = set(SKILL_POLICY)

DISALLOWED_ROLE = "steward"
SHARED_FIELDS = {
    "name",
    "version",
    "description",
    "author",
    "repository",
    "license",
    "keywords",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+]\(([^)]+)\)")
LINK_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
CODEX_IMPLICIT_POLICY = re.compile(
    r"^\s*allow_implicit_invocation:\s*(true|false)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
EMPTY_SOURCES = re.compile(r"^sources:\s*\[\s*\]\s*$", re.MULTILINE)

# Short, load-bearing terms of art rather than whole sentences: a contract may
# be reworded freely, but it may not drop these boundaries. Behavioural cover
# for the memory contract lives in tests/test_memory_fixture.py.
SKILL_GUARDRAILS = {
    "projipsa": {
        "implicit use stays read-only": (
            "implicit loading",
            "read-only",
        ),
        "writes require authorized scope": (
            "project-memory maintenance",
        ),
        "missing memory does not auto-initialize": (
            "$projipsa-init",
        ),
    },
    "projipsa-init": {
        "initialization is explicit": (
            "explicit, infrequent workflow",
        ),
        "memory usefulness is not a trigger": (
            "merely because",
        ),
        "default scope is docs-only": (
            "docs-only operation",
        ),
        "initialization is idempotent": (
            "initialization is idempotent",
        ),
        "the memory root stays discoverable per host": (
            "projipsa:memory-pointer",
            "claude.md",
            "agents.md",
        ),
    },
    "outsource": {
        "automatic loading only qualifies": (
            "qualification is read-only",
        ),
        "automatic loading is not delegation": (
            "automatic loading is not delegation or consent",
        ),
        "Maker opts in before the engagement starts": (
            "opt in before starting a deep interview",
        ),
        "ordinary work routes out": (
            "ordinary workflow",
            "leave outsource",
        ),
    },
}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def discovered_skills(root: Path) -> set[str]:
    return {
        path.parent.name for path in root.glob("*/SKILL.md") if path.is_file()
    }


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").lower().split())


def frontmatter_body(path: Path) -> str | None:
    match = re.match(
        r"\A---\s*\n(?P<body>.*?)\n---\s*(?:\n|\Z)",
        path.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    return match.group("body") if match else None


def frontmatter_field(body: str, key: str) -> str | None:
    match = re.search(
        rf"^{re.escape(key)}:[ \t]*(.+?)[ \t]*$",
        body,
        re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def mentions_invocation(text: str, invocation: str) -> bool:
    """Match a whole invocation token, so `$projipsa` is not satisfied by
    `$projipsa-init`."""
    return re.search(rf"{re.escape(invocation)}(?![\w-])", text) is not None


def codex_implicit_policy(path: Path) -> bool | None:
    match = CODEX_IMPLICIT_POLICY.search(path.read_text(encoding="utf-8"))
    if not match:
        return None
    return match.group(1).lower() == "true"


def validate_local_links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith("#") or LINK_SCHEME.match(target):
            continue
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if target and not (path.parent / target).resolve().exists():
            errors.append(f"{relative(path)}: broken local link {raw_target!r}")
    return errors


def validate_manifests(errors: list[str]) -> tuple[dict[str, Any], ...] | None:
    try:
        codex = load_json(CODEX_MANIFEST)
        claude = load_json(CLAUDE_MANIFEST)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(str(exc))
        return None

    for field in sorted(SHARED_FIELDS):
        if codex.get(field) != claude.get(field):
            errors.append(f"manifest field {field!r} differs between hosts")

    if codex.get("name") != ROOT.name:
        errors.append("plugin folder and manifest name must both be 'projipsa'")

    version = codex.get("version")
    if not isinstance(version, str) or not re.fullmatch(
        r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",
        version,
    ):
        errors.append("plugin version must use strict semantic versioning")

    if codex.get("skills") != "./skills/":
        errors.append("Codex manifest must use the portable skills/ entry point")
    if claude.get("skills") != "./skills/":
        errors.append("Claude manifest must use the portable skills/ entry point")

    codex_interface = codex.get("interface")
    codex_display = (
        codex_interface.get("displayName")
        if isinstance(codex_interface, dict)
        else None
    )
    if not codex_display:
        errors.append("Codex manifest must declare interface.displayName")
    if claude.get("displayName") != codex_display:
        errors.append(
            "displayName must match across hosts; Claude Code otherwise shows "
            "no name where Codex shows one"
        )

    if "project butler" not in (codex.get("description") or "").lower():
        errors.append("plugin description must state the project butler concept")

    return codex, claude


def validate_skill_surface(errors: list[str]) -> None:
    actual_skills = discovered_skills(SKILL_ROOT)
    if actual_skills != EXPECTED_SKILLS:
        errors.append(
            f"default discovery must expose {sorted(EXPECTED_SKILLS)}; "
            f"found {sorted(actual_skills)}"
        )

    all_skill_files = {
        path.relative_to(ROOT)
        for path in ROOT.rglob("SKILL.md")
        if ".git" not in path.parts
    }
    expected_skill_files = {
        Path("skills") / skill / "SKILL.md" for skill in EXPECTED_SKILLS
    }
    if all_skill_files != expected_skill_files:
        errors.append(
            "every cross-host public Skill needs a SKILL_POLICY row; "
            f"found {[str(path) for path in sorted(all_skill_files)]}"
        )

    legacy_capabilities = [
        relative(path)
        for path in ROOT.rglob("CAPABILITY.md")
        if ".git" not in path.parts
    ]
    if legacy_capabilities:
        errors.append(
            "legacy capability entrypoints must be removed; "
            f"found {sorted(legacy_capabilities)}"
        )

    nested_manifests = [
        path
        for path in ROOT.rglob("plugin.json")
        if path not in {CODEX_MANIFEST, CLAUDE_MANIFEST}
    ]
    if nested_manifests:
        errors.append("the package must not contain nested plugin manifests")


def validate_skill(skill: str, errors: list[str]) -> None:
    skill_path = SKILL_ROOT / skill / "SKILL.md"
    metadata_path = SKILL_ROOT / skill / "agents" / "openai.yaml"
    if not skill_path.is_file():
        return

    expected_implicit = bool(SKILL_POLICY[skill]["implicit"])

    body = frontmatter_body(skill_path)
    if body is None:
        errors.append(f"{relative(skill_path)}: missing YAML frontmatter")
        body = ""

    if frontmatter_field(body, "name") != skill:
        errors.append(f"{relative(skill_path)}: frontmatter name mismatch")

    description = frontmatter_field(body, "description") or ""
    if not description:
        errors.append(f"{relative(skill_path)}: frontmatter needs a description")
    for invocation in (f"${skill}", f"/projipsa:{skill}"):
        if not mentions_invocation(description, invocation):
            errors.append(
                f"{relative(skill_path)}: description must document the "
                f"{invocation} invocation so both hosts can trigger it"
            )

    # Claude Code enforces explicit-only loading through frontmatter; Codex
    # enforces the same policy through agents/openai.yaml. Both must agree.
    claude_policy = frontmatter_field(body, "disable-model-invocation")
    if expected_implicit and claude_policy is not None:
        errors.append(
            f"{relative(skill_path)}: disable-model-invocation must be absent "
            "for a Skill Claude Code may load implicitly"
        )
    if not expected_implicit and claude_policy != "true":
        errors.append(
            f"{relative(skill_path)}: disable-model-invocation must be true so "
            "Claude Code enforces the explicit-only policy mechanically"
        )

    if not metadata_path.is_file():
        errors.append(f"missing Codex metadata: {relative(metadata_path)}")
    else:
        actual_policy = codex_implicit_policy(metadata_path)
        if actual_policy is not expected_implicit:
            errors.append(
                f"{relative(metadata_path)}: allow_implicit_invocation must be "
                f"{str(expected_implicit).lower()}"
            )
        metadata = metadata_path.read_text(encoding="utf-8")
        if not mentions_invocation(metadata, f"${skill}"):
            errors.append(
                f"{relative(metadata_path)}: default prompt must mention ${skill}"
            )

    skill_text = normalized_text(skill_path)
    for label, phrases in SKILL_GUARDRAILS[skill].items():
        missing = [phrase for phrase in phrases if phrase not in skill_text]
        if missing:
            errors.append(
                f"{skill} contract missing guardrail: {label} "
                f"(absent: {missing})"
            )


def validate_templates(errors: list[str]) -> None:
    for path in sorted(TEMPLATE_ROOT.glob("*.md")):
        body = frontmatter_body(path)
        if body is None:
            continue
        if (
            frontmatter_field(body, "confidence") == "confirmed"
            and EMPTY_SOURCES.search(body)
        ):
            errors.append(
                f"{relative(path)}: a template must not ship "
                "confidence: confirmed with an empty sources list, because the "
                "memory validator rejects that page on sight"
            )

    delivery_template = TEMPLATE_ROOT / "delivery.md"
    if delivery_template.is_file():
        delivery_text = delivery_template.read_text(encoding="utf-8")
        for marker in (
            "status: draft",
            "confidence: assumed",
            "Contract status: draft",
            "Confirmed by: pending",
        ):
            if marker not in delivery_text:
                errors.append(f"delivery template must preserve {marker!r}")


def validate_resources(errors: list[str]) -> None:
    required_files = (
        SKILL_ROOT / "projipsa" / "references" / "memory-contract.md",
        SKILL_ROOT / "projipsa" / "assets" / "templates" / "delivery.md",
        SKILL_ROOT / "projipsa" / "assets" / "templates" / "root-pointer.md",
        SKILL_ROOT / "projipsa" / "scripts" / "validate_memory.py",
        SKILL_ROOT / "projipsa-init" / "references" / "initialization.md",
        SKILL_ROOT / "outsource" / "references" / "delivery-contract.md",
        SKILL_ROOT / "outsource" / "references" / "projipsa-integration.md",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing Skill resource: {relative(path)}")

    if (
        SKILL_ROOT / "outsource" / "references" / "learning-protocol.md"
    ).exists():
        errors.append("Outsource must not create an automatic learning-state protocol")


def validate_prose(errors: list[str]) -> None:
    markdown_paths = [
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
        and not {"assets", "templates"}.issubset(path.parts)
    ]
    for path in markdown_paths:
        errors.extend(validate_local_links(path))

    text_extensions = {".md", ".json", ".yaml", ".yml"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in text_extensions:
            continue
        if "__pycache__" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(rf"\b{DISALLOWED_ROLE}(?:ship)?\b", text, re.IGNORECASE):
            errors.append(
                f"{relative(path)}: use the Projipsa butler concept instead"
            )
        if "[TODO:" in text:
            errors.append(f"{relative(path)}: unresolved scaffold TODO")


def validate_readme(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for skill in sorted(EXPECTED_SKILLS):
        for invocation in (f"${skill}", f"/projipsa:{skill}"):
            if not mentions_invocation(readme, invocation):
                errors.append(f"README must document {invocation}")


def validate() -> list[str]:
    errors: list[str] = []
    if validate_manifests(errors) is None:
        return errors

    validate_skill_surface(errors)
    for skill in sorted(EXPECTED_SKILLS):
        validate_skill(skill, errors)
    validate_templates(errors)
    validate_resources(errors)
    validate_prose(errors)
    validate_readme(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"Package validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Projipsa package is aligned for Codex and Claude Code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

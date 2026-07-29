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
EXPECTED_SKILLS = {"projipsa", "projipsa-init", "outsource"}
EXPECTED_IMPLICIT_POLICY = {
    "projipsa": True,
    "projipsa-init": False,
    "outsource": True,
}
DISALLOWED_ROLE = "ste" + "ward"
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
IMPLICIT_POLICY = re.compile(
    r"^\s*allow_implicit_invocation:\s*(true|false)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
SKILL_GUARDRAILS = {
    "projipsa": {
        "implicit use stays read-only": (
            "implicit loading",
            "read-only",
        ),
        "writes require authorized scope": (
            "require either an explicit user request",
            "project-memory maintenance",
        ),
        "missing memory does not auto-initialize": (
            "do not",
            "initialize it automatically",
            "$projipsa-init",
        ),
    },
    "projipsa-init": {
        "initialization is explicit": (
            "explicit, infrequent workflow",
            "$projipsa-init",
        ),
        "memory usefulness is not a trigger": (
            "do not load or run it merely because",
            "memory would be useful",
        ),
        "default scope is docs-only": (
            "docs-only operation",
        ),
        "initialization is idempotent": (
            "initialization is idempotent",
        ),
    },
    "outsource": {
        "broad or long work can trigger qualification": (
            "loaded automatically",
            "broad, long-running, risky, or",
            "qualification is read-only",
        ),
        "automatic loading is not delegation": (
            "automatic loading is not delegation or consent",
        ),
        "Maker opts in before the engagement starts": (
            "ask the maker to opt in",
            "deep interview",
            "delivery contract as active",
        ),
        "ordinary work routes out": (
            "ordinary workflow",
            "leave outsource",
        ),
    },
}


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


def frontmatter_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.match(
        r"\A---\s*\n(?P<body>.*?)\n---\s*(?:\n|\Z)",
        text,
        re.DOTALL,
    )
    if not match:
        return None
    name = re.search(r"^name:\s*(.+?)\s*$", match.group("body"), re.MULTILINE)
    return name.group(1).strip() if name else None


def implicit_policy(path: Path) -> bool | None:
    match = IMPLICIT_POLICY.search(path.read_text(encoding="utf-8"))
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
            errors.append(
                f"{path.relative_to(ROOT)}: broken local link {raw_target!r}"
            )
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    try:
        codex = load_json(CODEX_MANIFEST)
        claude = load_json(CLAUDE_MANIFEST)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]

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
            "Projipsa must expose exactly three cross-host public Skills; "
            f"found {[str(path) for path in sorted(all_skill_files)]}"
        )

    legacy_capabilities = [
        path.relative_to(ROOT)
        for path in ROOT.rglob("CAPABILITY.md")
        if ".git" not in path.parts
    ]
    if legacy_capabilities:
        errors.append(
            "legacy capability entrypoints must be removed; "
            f"found {[str(path) for path in legacy_capabilities]}"
        )

    for skill in sorted(EXPECTED_SKILLS):
        skill_path = SKILL_ROOT / skill / "SKILL.md"
        metadata_path = SKILL_ROOT / skill / "agents" / "openai.yaml"
        if not skill_path.is_file():
            continue
        if frontmatter_name(skill_path) != skill:
            errors.append(f"{skill_path.relative_to(ROOT)}: frontmatter name mismatch")
        if not metadata_path.is_file():
            errors.append(f"missing Codex metadata: {metadata_path.relative_to(ROOT)}")
        else:
            actual_policy = implicit_policy(metadata_path)
            expected_policy = EXPECTED_IMPLICIT_POLICY[skill]
            if actual_policy is not expected_policy:
                errors.append(
                    f"{metadata_path.relative_to(ROOT)}: "
                    f"allow_implicit_invocation must be "
                    f"{str(expected_policy).lower()}"
                )
            metadata = metadata_path.read_text(encoding="utf-8")
            if f"${skill}" not in metadata:
                errors.append(
                    f"{metadata_path.relative_to(ROOT)}: default prompt must "
                    f"mention ${skill}"
                )

        skill_text = normalized_text(skill_path)
        for label, phrases in SKILL_GUARDRAILS[skill].items():
            if not all(phrase in skill_text for phrase in phrases):
                errors.append(f"{skill} contract missing guardrail: {label}")

    markdown_paths = [
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
        and not {"assets", "templates"}.issubset(path.parts)
    ]
    for path in markdown_paths:
        errors.extend(validate_local_links(path))

    nested_manifests = [
        path
        for path in ROOT.rglob("plugin.json")
        if path not in {CODEX_MANIFEST, CLAUDE_MANIFEST}
    ]
    if nested_manifests:
        errors.append("the package must not contain nested plugin manifests")

    required_files = (
        SKILL_ROOT / "projipsa" / "references" / "memory-contract.md",
        SKILL_ROOT / "projipsa" / "assets" / "templates" / "delivery.md",
        SKILL_ROOT / "projipsa" / "scripts" / "validate_memory.py",
        SKILL_ROOT / "projipsa-init" / "references" / "initialization.md",
        SKILL_ROOT / "outsource" / "references" / "delivery-contract.md",
        SKILL_ROOT / "outsource" / "references" / "projipsa-integration.md",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing Skill resource: {path.relative_to(ROOT)}")

    delivery_template = (
        SKILL_ROOT / "projipsa" / "assets" / "templates" / "delivery.md"
    )
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

    if (
        SKILL_ROOT / "outsource" / "references" / "learning-protocol.md"
    ).exists():
        errors.append("Outsource must not create an automatic learning-state protocol")

    text_extensions = {".md", ".json", ".yaml", ".yml"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in text_extensions:
            continue
        if "__pycache__" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(
            rf"\b{DISALLOWED_ROLE}(?:ship)?\b",
            text,
            re.IGNORECASE,
        ):
            errors.append(
                f"{path.relative_to(ROOT)}: use the Projipsa butler concept instead"
            )
        if "[TODO:" in text:
            errors.append(f"{path.relative_to(ROOT)}: unresolved scaffold TODO")

    if "project butler" not in (codex.get("description") or "").lower():
        errors.append("plugin description must state the project butler concept")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for invocation in (
        "$projipsa",
        "$projipsa-init",
        "$outsource",
        "/projipsa:projipsa",
        "/projipsa:projipsa-init",
        "/projipsa:outsource",
    ):
        if invocation not in readme:
            errors.append(f"README must document {invocation}")

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

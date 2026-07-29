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
DEFAULT_SKILLS = {"projipsa"}
EXPECTED_CAPABILITIES = {"outsource", "projipsa-init", "projipsa-memory"}
MODE_TARGETS = {
    "init": "../../capabilities/projipsa-init/CAPABILITY.md",
    "memory": "../../capabilities/projipsa-memory/CAPABILITY.md",
    "outsource": "../../capabilities/outsource/CAPABILITY.md",
}
DEFAULT_SKILL_ROOT = ROOT / "skills"
CAPABILITY_ROOT = ROOT / "capabilities"
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
ROUTER_GUARDRAILS = {
    "implicit selection stays read-only": (
        "selected implicitly",
        "remain read-only",
    ),
    "mode dispatch uses the first token": (
        "first argument token",
        "dispatch literally",
    ),
    "only the selected capability is loaded": (
        "load only the selected capability",
    ),
    "Outsource is not inferred from complexity": (
        "complexity alone is not consent",
    ),
    "memory mode does not imply write authority": (
        "does not select a write operation",
    ),
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

    actual_default_skills = discovered_skills(DEFAULT_SKILL_ROOT)
    if actual_default_skills != DEFAULT_SKILLS:
        errors.append(
            "default skill discovery must expose only the implicit Projipsa router; "
            f"found {sorted(actual_default_skills)}"
        )

    all_skill_files = {
        path.relative_to(ROOT)
        for path in ROOT.rglob("SKILL.md")
        if ".git" not in path.parts
    }
    expected_skill_files = {Path("skills/projipsa/SKILL.md")}
    if all_skill_files != expected_skill_files:
        errors.append(
            "Projipsa must expose one cross-host public Skill; "
            f"found {[str(path) for path in sorted(all_skill_files)]}"
        )

    actual_capabilities = {
        path.parent.name
        for path in CAPABILITY_ROOT.glob("*/CAPABILITY.md")
        if path.is_file()
    }
    if actual_capabilities != EXPECTED_CAPABILITIES:
        errors.append(
            f"expected capabilities {sorted(EXPECTED_CAPABILITIES)}, "
            f"found {sorted(actual_capabilities)}"
        )

    main_metadata = DEFAULT_SKILL_ROOT / "projipsa" / "agents" / "openai.yaml"
    if not main_metadata.is_file():
        errors.append(
            f"missing Codex router metadata: {main_metadata.relative_to(ROOT)}"
        )
    elif "allow_implicit_invocation: false" in main_metadata.read_text(
        encoding="utf-8"
    ):
        errors.append("the main Projipsa router must remain implicitly invocable")

    router_path = DEFAULT_SKILL_ROOT / "projipsa" / "SKILL.md"
    if router_path.is_file():
        router_source = router_path.read_text(encoding="utf-8")
        router_text = " ".join(router_source.lower().split())
        for label, phrases in ROUTER_GUARDRAILS.items():
            if not all(phrase.lower() in router_text for phrase in phrases):
                errors.append(f"router contract missing guardrail: {label}")
        for mode, target in MODE_TARGETS.items():
            mapping = re.compile(
                rf"- `{re.escape(mode)}` loads\s+"
                rf"\[[^\]]+\]\({re.escape(target)}\)",
                re.MULTILINE,
            )
            if not mapping.search(router_source):
                errors.append(
                    f"router must map mode {mode!r} to {target!r}"
                )

    markdown_entrypoints = (
        list(DEFAULT_SKILL_ROOT.glob("*/SKILL.md"))
        + list(CAPABILITY_ROOT.glob("*/CAPABILITY.md"))
    )
    for path in markdown_entrypoints:
        errors.extend(validate_local_links(path))

    nested_manifests = [
        path
        for path in ROOT.rglob("plugin.json")
        if path not in {CODEX_MANIFEST, CLAUDE_MANIFEST}
    ]
    if nested_manifests:
        errors.append("the package must not contain nested plugin manifests")

    required_files = (
        DEFAULT_SKILL_ROOT / "projipsa" / "references" / "butler-contract.md",
        CAPABILITY_ROOT
        / "projipsa-memory"
        / "assets"
        / "templates"
        / "delivery.md",
        CAPABILITY_ROOT / "outsource" / "references" / "delivery-contract.md",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing integrated capability file: {path.relative_to(ROOT)}")

    delivery_template = required_files[1]
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

    if (CAPABILITY_ROOT / "outsource" / "references" / "learning-protocol.md").exists():
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
        "$projipsa init",
        "$projipsa memory",
        "$projipsa outsource",
    ):
        if invocation not in readme:
            errors.append(f"README must document {invocation}")
    for invocation in (
        "/projipsa:projipsa",
        "/projipsa:projipsa init",
        "/projipsa:projipsa memory",
        "/projipsa:projipsa outsource",
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

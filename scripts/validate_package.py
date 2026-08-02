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
# Only this directory is copied into a user's plugin cache. Project memory under
# docs/, tests, scripts, and CI stay in the repository and are deliberately
# outside every scan below: memory content must never gate package validation.
PACKAGE_ROOT = ROOT / "plugins" / "projipsa"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MANIFEST = PACKAGE_ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST = PACKAGE_ROOT / ".claude-plugin" / "plugin.json"
CODEX_SKILL_ROOT = PACKAGE_ROOT / "skills"
CLAUDE_SKILL_ROOT = PACKAGE_ROOT / "claude-skills"
SHARED_WORKFLOW_ROOT = PACKAGE_ROOT / "shared"
RESOURCE_SKILL_ROOT = CODEX_SKILL_ROOT
TEMPLATE_ROOT = RESOURCE_SKILL_ROOT / "projipsa" / "assets" / "templates"

# One declaration per public Skill. Adding a Skill means declaring its
# host-loading policy here, not editing several parallel constants.
SKILL_POLICY = {
    "projipsa": {"implicit": True},
    "projipsa-init": {"implicit": False},
    "outsource": {"implicit": True},
}
EXPECTED_SKILLS = set(SKILL_POLICY)
CODEX_PLUGIN_NAMESPACE = "projipsa"

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
            "$projipsa:projipsa-init",
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
    """Match a whole invocation token, so an unqualified name is not
    satisfied by a namespaced plugin invocation."""
    return re.search(rf"{re.escape(invocation)}(?![\w-])", text) is not None


def codex_invocation(skill: str) -> str:
    return f"${CODEX_PLUGIN_NAMESPACE}:{skill}"


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

    if codex.get("name") != PACKAGE_ROOT.name:
        errors.append("plugin folder and manifest name must both be 'projipsa'")

    version = codex.get("version")
    if not isinstance(version, str) or not re.fullmatch(
        r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",
        version,
    ):
        errors.append("plugin version must use strict semantic versioning")

    if codex.get("skills") != "./skills/":
        errors.append("Codex manifest must use the standard skills/ entry point")
    if claude.get("skills") != "./claude-skills/":
        errors.append("Claude manifest must use the isolated claude-skills/ entry point")

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


def validate_marketplaces(errors: list[str]) -> None:
    try:
        codex = load_json(CODEX_MARKETPLACE)
        claude = load_json(CLAUDE_MARKETPLACE)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(str(exc))
        return

    if codex.get("name") != "projipsa" or claude.get("name") != "projipsa":
        errors.append("both development marketplaces must be named 'projipsa'")

    codex_plugins = codex.get("plugins")
    claude_plugins = claude.get("plugins")
    if not isinstance(codex_plugins, list) or len(codex_plugins) != 1:
        errors.append("Codex marketplace must expose exactly one plugin")
        codex_entry: dict[str, Any] = {}
    else:
        codex_entry = codex_plugins[0] if isinstance(codex_plugins[0], dict) else {}
    if not isinstance(claude_plugins, list) or len(claude_plugins) != 1:
        errors.append("Claude marketplace must expose exactly one plugin")
        claude_entry: dict[str, Any] = {}
    else:
        claude_entry = (
            claude_plugins[0] if isinstance(claude_plugins[0], dict) else {}
        )

    if codex_entry.get("name") != "projipsa":
        errors.append("Codex marketplace must expose the projipsa plugin")
    if claude_entry.get("name") != "projipsa":
        errors.append("Claude marketplace must expose the projipsa plugin")
    if codex_entry.get("source") != {
        "source": "local",
        "path": "./plugins/projipsa",
    }:
        errors.append("Codex marketplace must use its local structured source")
    if claude_entry.get("source") != "./plugins/projipsa":
        errors.append("Claude marketplace must use its local plugin source")
    if codex_entry.get("policy") != {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }:
        errors.append("Codex marketplace must declare its installation policy")


def validate_skill_surface(errors: list[str]) -> None:
    codex_skills = discovered_skills(CODEX_SKILL_ROOT)
    claude_skills = discovered_skills(CLAUDE_SKILL_ROOT)
    if codex_skills != EXPECTED_SKILLS:
        errors.append(
            f"Codex discovery must expose {sorted(EXPECTED_SKILLS)}; "
            f"found {sorted(codex_skills)}"
        )
    if claude_skills != EXPECTED_SKILLS:
        errors.append(
            f"Claude discovery must expose {sorted(EXPECTED_SKILLS)}; "
            f"found {sorted(claude_skills)}"
        )

    package_prefix = PACKAGE_ROOT.relative_to(ROOT)
    all_skill_files = {
        path.relative_to(ROOT) for path in PACKAGE_ROOT.rglob("SKILL.md")
    }
    expected_skill_files = {
        package_prefix / host_root / skill / "SKILL.md"
        for host_root in ("skills", "claude-skills")
        for skill in EXPECTED_SKILLS
    }
    if all_skill_files != expected_skill_files:
        errors.append(
            "every public Skill needs one isolated adapter per host; "
            f"found {[str(path) for path in sorted(all_skill_files)]}"
        )

    shared_workflows = {
        path.stem for path in SHARED_WORKFLOW_ROOT.glob("*.md") if path.is_file()
    }
    if shared_workflows != EXPECTED_SKILLS:
        errors.append(
            f"shared workflows must match {sorted(EXPECTED_SKILLS)}; "
            f"found {sorted(shared_workflows)}"
        )

    claude_metadata = sorted(CLAUDE_SKILL_ROOT.glob("*/agents/openai.yaml"))
    if claude_metadata:
        errors.append(
            "Codex metadata must not live in the Claude adapter tree; "
            f"found {[relative(path) for path in claude_metadata]}"
        )

    legacy_capabilities = [
        relative(path) for path in PACKAGE_ROOT.rglob("CAPABILITY.md")
    ]
    if legacy_capabilities:
        errors.append(
            "legacy capability entrypoints must be removed; "
            f"found {sorted(legacy_capabilities)}"
        )

    nested_manifests = [
        path
        for path in PACKAGE_ROOT.rglob("plugin.json")
        if path not in {CODEX_MANIFEST, CLAUDE_MANIFEST}
    ]
    if nested_manifests:
        errors.append("the package must not contain nested plugin manifests")


def validate_skill(skill: str, errors: list[str]) -> None:
    codex_skill_path = CODEX_SKILL_ROOT / skill / "SKILL.md"
    claude_skill_path = CLAUDE_SKILL_ROOT / skill / "SKILL.md"
    shared_workflow_path = SHARED_WORKFLOW_ROOT / f"{skill}.md"
    metadata_path = CODEX_SKILL_ROOT / skill / "agents" / "openai.yaml"
    if not codex_skill_path.is_file() or not claude_skill_path.is_file():
        return

    expected_implicit = bool(SKILL_POLICY[skill]["implicit"])

    adapter_bodies: dict[str, str] = {}
    for host, skill_path, invocation in (
        ("Codex", codex_skill_path, codex_invocation(skill)),
        ("Claude", claude_skill_path, f"/projipsa:{skill}"),
    ):
        body = frontmatter_body(skill_path)
        if body is None:
            errors.append(f"{relative(skill_path)}: missing YAML frontmatter")
            body = ""
        adapter_bodies[host] = body

        if frontmatter_field(body, "name") != skill:
            errors.append(f"{relative(skill_path)}: frontmatter name mismatch")

        description = frontmatter_field(body, "description") or ""
        if not description:
            errors.append(f"{relative(skill_path)}: frontmatter needs a description")
        if not mentions_invocation(description, invocation):
            errors.append(
                f"{relative(skill_path)}: description must document the "
                f"{host} invocation {invocation}"
            )

        adapter_text = skill_path.read_text(encoding="utf-8")
        shared_target = f"../../shared/{skill}.md"
        if shared_target not in adapter_text:
            errors.append(
                f"{relative(skill_path)}: adapter must load {shared_target}"
            )

    codex_policy = frontmatter_field(
        adapter_bodies.get("Codex", ""), "disable-model-invocation"
    )
    if codex_policy is not None:
        errors.append(
            f"{relative(codex_skill_path)}: Claude-only "
            "disable-model-invocation must be absent"
        )

    # Claude Code enforces explicit-only loading through its adapter
    # frontmatter; Codex uses only agents/openai.yaml in its separate tree.
    claude_policy = frontmatter_field(
        adapter_bodies.get("Claude", ""), "disable-model-invocation"
    )
    if expected_implicit and claude_policy is not None:
        errors.append(
            f"{relative(claude_skill_path)}: disable-model-invocation must be absent "
            "for a Skill Claude Code may load implicitly"
        )
    if not expected_implicit and claude_policy != "true":
        errors.append(
            f"{relative(claude_skill_path)}: disable-model-invocation must be true so "
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
        invocation = codex_invocation(skill)
        if not mentions_invocation(metadata, invocation):
            errors.append(
                f"{relative(metadata_path)}: default prompt must mention "
                f"{invocation}"
            )

    if not shared_workflow_path.is_file():
        errors.append(f"missing shared workflow: {relative(shared_workflow_path)}")
        return

    shared_text = shared_workflow_path.read_text(encoding="utf-8")
    for invocation in (codex_invocation(skill), f"/projipsa:{skill}"):
        if not mentions_invocation(shared_text, invocation):
            errors.append(
                f"{relative(shared_workflow_path)}: shared workflow must "
                f"document {invocation}"
            )

    skill_text = normalized_text(shared_workflow_path)
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
        RESOURCE_SKILL_ROOT / "projipsa" / "references" / "memory-contract.md",
        RESOURCE_SKILL_ROOT / "projipsa" / "assets" / "templates" / "delivery.md",
        RESOURCE_SKILL_ROOT / "projipsa" / "assets" / "templates" / "root-pointer.md",
        RESOURCE_SKILL_ROOT / "projipsa" / "scripts" / "validate_memory.py",
        RESOURCE_SKILL_ROOT / "projipsa-init" / "references" / "initialization.md",
        RESOURCE_SKILL_ROOT / "outsource" / "references" / "delivery-contract.md",
        RESOURCE_SKILL_ROOT / "outsource" / "references" / "projipsa-integration.md",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing Skill resource: {relative(path)}")

    if (
        RESOURCE_SKILL_ROOT / "outsource" / "references" / "learning-protocol.md"
    ).exists():
        errors.append("Outsource must not create an automatic learning-state protocol")


def scanned_files() -> list[Path]:
    """The prose surface this validator owns: everything that ships, plus the
    repository README. Anything under docs/ belongs to validate_memory.py."""
    files = [path for path in PACKAGE_ROOT.rglob("*") if path.is_file()]
    readme = ROOT / "README.md"
    if readme.is_file():
        files.append(readme)
    return sorted(files)


def validate_prose(errors: list[str]) -> None:
    text_extensions = {".md", ".json", ".yaml", ".yml"}
    for path in scanned_files():
        if "__pycache__" in path.parts:
            continue
        if path.suffix == ".md" and not {"assets", "templates"}.issubset(
            path.parts
        ):
            errors.extend(validate_local_links(path))
        if path.suffix not in text_extensions:
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
        for invocation in (codex_invocation(skill), f"/projipsa:{skill}"):
            if not mentions_invocation(readme, invocation):
                errors.append(f"README must document {invocation}")


def validate() -> list[str]:
    errors: list[str] = []
    if validate_manifests(errors) is None:
        return errors

    validate_marketplaces(errors)
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

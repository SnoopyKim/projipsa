#!/usr/bin/env python3
"""Validate cross-host Projipsa package alignment."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
EXPECTED_SKILLS = {"projipsa", "projipsa-init"}
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


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


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

    skill_root = ROOT / "skills"
    actual_skills = {
        path.parent.name for path in skill_root.glob("*/SKILL.md") if path.is_file()
    }
    if actual_skills != EXPECTED_SKILLS:
        errors.append(
            f"expected skills {sorted(EXPECTED_SKILLS)}, found {sorted(actual_skills)}"
        )

    for skill in EXPECTED_SKILLS:
        metadata = skill_root / skill / "agents" / "openai.yaml"
        if not metadata.is_file():
            errors.append(f"missing Codex skill metadata: {metadata.relative_to(ROOT)}")

    text_extensions = {".md", ".json", ".yaml", ".yml"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in text_extensions:
            continue
        if "__pycache__" in path.parts:
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

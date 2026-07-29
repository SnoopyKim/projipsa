#!/usr/bin/env python3
"""Validate the structural contract of a Projipsa project-memory tree."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = (
    "AGENTS.md",
    "index.md",
    "wiki/project/overview.md",
    "wiki/project/current-state.md",
)
REQUIRED_FRONTMATTER = (
    "id",
    "type",
    "status",
    "confidence",
    "updated",
    "sources",
    "related",
)
ALLOWED_STATUSES = {"active", "draft", "stale", "superseded", "archived"}
ALLOWED_CONFIDENCE = {"confirmed", "assumed", "inferred", "disputed"}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
LINK_PATTERN = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
SCHEME_PATTERN = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


def resolve_memory_root(candidate: Path) -> Path:
    candidate = candidate.resolve()
    if (candidate / "index.md").is_file():
        return candidate
    if (candidate / "docs" / "index.md").is_file():
        return candidate / "docs"
    return candidate


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration:
        return None

    values: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([a-z_]+):(?:\s*(.*))?$", line)
        if match:
            values[match.group(1)] = (match.group(2) or "").strip().strip("\"'")
    return values, text


def local_markdown_links(path: Path, text: str, root: Path) -> list[str]:
    errors: list[str] = []
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().strip("<>")
        if (
            not target
            or target.startswith("#")
            or SCHEME_PATTERN.match(target)
        ):
            continue

        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue

        relative = Path(target)
        candidates = [(path.parent / relative).resolve()]
        if not relative.is_absolute():
            candidates.append((root / relative).resolve())
        if not any(candidate.exists() for candidate in candidates):
            errors.append(f"{path}: broken link target {raw_target!r}")
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    wiki_root = root / "wiki"
    wiki_files = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
    if not wiki_files:
        errors.append("no maintained Markdown pages found under wiki/")
        return errors

    seen_ids: dict[str, Path] = {}
    files_to_check = [path for path in (root / "index.md", *wiki_files) if path.is_file()]

    for path in wiki_files:
        parsed = parse_frontmatter(path)
        if parsed is None:
            errors.append(f"{path}: missing or unterminated YAML frontmatter")
            continue
        values, text = parsed

        missing = [key for key in REQUIRED_FRONTMATTER if key not in values]
        if missing:
            errors.append(f"{path}: missing frontmatter keys: {', '.join(missing)}")

        page_id = values.get("id", "")
        if page_id and not ID_PATTERN.fullmatch(page_id):
            errors.append(f"{path}: invalid page id {page_id!r}")
        if page_id in seen_ids:
            errors.append(
                f"{path}: duplicate page id {page_id!r}; first seen in {seen_ids[page_id]}"
            )
        elif page_id:
            seen_ids[page_id] = path

        status = values.get("status")
        if status and status not in ALLOWED_STATUSES:
            errors.append(f"{path}: unsupported status {status!r}")

        confidence = values.get("confidence")
        if confidence and confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"{path}: unsupported confidence {confidence!r}")

        updated = values.get("updated")
        if updated:
            try:
                date.fromisoformat(updated)
            except ValueError:
                errors.append(f"{path}: updated must be an ISO date, got {updated!r}")

        if "[TODO:" in text or "YYYY-MM-DD" in text:
            errors.append(f"{path}: unresolved template placeholder")

    for path in files_to_check:
        text = path.read_text(encoding="utf-8")
        errors.extend(local_markdown_links(path, text, root))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Projipsa project-memory root."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        type=Path,
        help="Memory root or project root containing docs/ (default: current directory)",
    )
    args = parser.parse_args()

    root = resolve_memory_root(args.path)
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"Projipsa validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    page_count = len(list((root / "wiki").rglob("*.md")))
    print(f"Projipsa memory is valid: {page_count} maintained page(s) in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

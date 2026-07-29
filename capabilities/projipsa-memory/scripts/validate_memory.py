#!/usr/bin/env python3
"""Validate the structural contract of a Projipsa project-memory tree."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Union
from urllib.parse import unquote, urlparse


REQUIRED_FILES = (
    "AGENTS.md",
    "index.md",
    "wiki/project/overview.md",
    "wiki/project/current-state.md",
    "wiki/questions/open-questions.md",
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
LIST_FIELDS = {
    "sources",
    "related",
    "supersedes",
    "superseded_by",
    "depends_on",
    "blocks",
}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
ADOPTION_ID_PATTERN = re.compile(
    r"^decision\.projipsa-adoption\.\d{4}-\d{2}-\d{2}$"
)
ADOPTION_FILE_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}-projipsa-adoption\.md$"
)
MONTHLY_LOG_PATTERN = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])\.md$")
LINK_PATTERN = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
SCHEME_PATTERN = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
PLACEHOLDER_PATTERN = re.compile(r"\[TODO:|YYYY-MM(?:-DD)?")

FrontmatterValue = Union[str, list[str]]


def resolve_memory_root(candidate: Path) -> Path:
    candidate = candidate.resolve()
    if (candidate / "index.md").is_file():
        return candidate
    if (candidate / "docs" / "index.md").is_file():
        return candidate / "docs"
    return candidate


def parse_inline_list(raw: str) -> list[str] | None:
    if not (raw.startswith("[") and raw.endswith("]")):
        return None
    contents = raw[1:-1].strip()
    if not contents:
        return []
    return [
        item.strip().strip("\"'")
        for item in contents.split(",")
        if item.strip()
    ]


def parse_frontmatter(
    path: Path,
) -> tuple[dict[str, FrontmatterValue], str] | None:
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

    values: dict[str, FrontmatterValue] = {}
    current_list_key: str | None = None
    for line in lines[1:end]:
        match = re.match(r"^([a-z_]+):(?:\s*(.*))?$", line)
        if match:
            key = match.group(1)
            raw = (match.group(2) or "").strip()
            inline_list = parse_inline_list(raw)
            if key in LIST_FIELDS and (not raw or inline_list is not None):
                values[key] = inline_list if inline_list is not None else []
                current_list_key = key
            else:
                values[key] = raw.strip("\"'")
                current_list_key = None
            continue

        list_item = re.match(r"^\s+-\s*(.+?)\s*$", line)
        if list_item and current_list_key:
            current_value = values[current_list_key]
            if isinstance(current_value, list):
                current_value.append(list_item.group(1).strip().strip("\"'"))
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


def local_markdown_targets(path: Path, text: str) -> set[Path]:
    targets: set[Path] = set()
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith("#") or SCHEME_PATTERN.match(target):
            continue
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if target:
            targets.add((path.parent / target).resolve())
    return targets


def find_project_boundary(root: Path) -> Path:
    for candidate in (root, *root.parents):
        if (candidate / ".git").exists():
            return candidate.resolve()
    if root.name in {"docs", "documentation", "project-docs"}:
        return root.parent.resolve()
    return root.resolve()


def is_within(path: Path, boundary: Path) -> bool:
    try:
        path.relative_to(boundary)
    except ValueError:
        return False
    return True


def resolve_source_target(
    source: str,
    page: Path,
    root: Path,
    project_boundary: Path,
) -> str | Path | None:
    target = source.strip().strip("<>")
    if not target:
        return None
    parsed_url = urlparse(target)
    if parsed_url.scheme.lower() in {"http", "https"}:
        return target if parsed_url.netloc else None
    if SCHEME_PATTERN.match(target):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    relative = Path(target)
    if relative.is_absolute():
        return None
    candidates = (
        (root / relative).resolve(),
        (project_boundary / relative).resolve(),
        (page.parent / relative).resolve(),
    )
    for candidate in candidates:
        if is_within(candidate, project_boundary) and candidate.is_file():
            return candidate
    return None


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    project_boundary = find_project_boundary(root)

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    wiki_root = root / "wiki"
    wiki_files = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
    if not wiki_files:
        errors.append("no maintained Markdown pages found under wiki/")

    decision_root = wiki_root / "decisions"
    decision_files = (
        sorted(decision_root.rglob("*.md")) if decision_root.is_dir() else []
    )
    if not decision_files:
        errors.append("missing required decision page under wiki/decisions/")

    logs_root = root / "logs"
    monthly_logs = (
        sorted(
            path
            for path in logs_root.glob("*.md")
            if MONTHLY_LOG_PATTERN.fullmatch(path.name)
        )
        if logs_root.is_dir()
        else []
    )
    if not monthly_logs:
        errors.append("missing required monthly log matching logs/YYYY-MM.md")

    seen_ids: dict[str, Path] = {}
    valid_decision_pages = 0
    adoption_decision_pages: list[Path] = []
    confirmed_pages: set[Path] = set()
    direct_evidence_pages: set[Path] = set()
    maintained_source_edges: dict[Path, set[Path]] = {}
    files_to_check = [
        path
        for path in (root / "index.md", *wiki_files, *monthly_logs)
        if path.is_file()
    ]

    for path in wiki_files:
        parsed = parse_frontmatter(path)
        if parsed is None:
            errors.append(f"{path}: missing or unterminated YAML frontmatter")
            continue
        values, text = parsed

        missing = [key for key in REQUIRED_FRONTMATTER if key not in values]
        if missing:
            errors.append(f"{path}: missing frontmatter keys: {', '.join(missing)}")

        page_id_value = values.get("id")
        page_id = ""
        if "id" in values:
            if not isinstance(page_id_value, str) or not page_id_value.strip():
                errors.append(f"{path}: id must be a non-empty scalar value")
            else:
                page_id = page_id_value
                if not ID_PATTERN.fullmatch(page_id):
                    errors.append(f"{path}: invalid page id {page_id!r}")
        if page_id in seen_ids:
            errors.append(
                f"{path}: duplicate page id {page_id!r}; first seen in {seen_ids[page_id]}"
            )
        elif page_id:
            seen_ids[page_id] = path

        page_type = values.get("type")
        if "type" in values and (
            not isinstance(page_type, str) or not page_type.strip()
        ):
            errors.append(f"{path}: type must be a non-empty scalar value")
        is_decision_page = decision_root in path.parents and page_type == "decision"
        adoption_marker = values.get("projipsa_adoption")
        if adoption_marker is not None and adoption_marker not in {
            "true",
            "false",
        }:
            errors.append(f"{path}: projipsa_adoption must be true or false")
        if adoption_marker == "true" and not is_decision_page:
            errors.append(
                f"{path}: projipsa_adoption is valid only on a decision page"
            )
        if is_decision_page:
            valid_decision_pages += 1
            is_canonical_adoption = bool(
                ADOPTION_ID_PATTERN.fullmatch(page_id)
                and ADOPTION_FILE_PATTERN.fullmatch(path.name)
            )
            if adoption_marker == "false" and is_canonical_adoption:
                errors.append(
                    f"{path}: canonical adoption decision cannot set "
                    "projipsa_adoption to false"
                )
            elif adoption_marker == "true" or is_canonical_adoption:
                adoption_decision_pages.append(path)

        status = values.get("status")
        if "status" in values and (
            not isinstance(status, str) or not status.strip()
        ):
            errors.append(f"{path}: status must be a non-empty scalar value")
        elif isinstance(status, str) and status not in ALLOWED_STATUSES:
            errors.append(f"{path}: unsupported status {status!r}")

        confidence = values.get("confidence")
        if "confidence" in values and (
            not isinstance(confidence, str) or not confidence.strip()
        ):
            errors.append(f"{path}: confidence must be a non-empty scalar value")
        elif (
            isinstance(confidence, str)
            and confidence not in ALLOWED_CONFIDENCE
        ):
            errors.append(f"{path}: unsupported confidence {confidence!r}")

        updated = values.get("updated")
        if "updated" in values and (
            not isinstance(updated, str) or not updated.strip()
        ):
            errors.append(f"{path}: updated must be a non-empty scalar value")
        elif isinstance(updated, str):
            try:
                date.fromisoformat(updated)
            except ValueError:
                errors.append(f"{path}: updated must be an ISO date, got {updated!r}")

        sources = values.get("sources")
        related = values.get("related")
        if "sources" in values and not isinstance(sources, list):
            errors.append(f"{path}: sources must be a YAML list")
        if "related" in values and not isinstance(related, list):
            errors.append(f"{path}: related must be a YAML list")
        if confidence == "confirmed" and isinstance(sources, list) and not sources:
            errors.append(f"{path}: confirmed pages require at least one source")
        if confidence == "confirmed":
            confirmed_pages.add(path.resolve())
        if isinstance(sources, list):
            for source in sources:
                resolved_source = resolve_source_target(
                    source,
                    path,
                    root,
                    project_boundary,
                )
                if resolved_source is None:
                    errors.append(f"{path}: source target not found: {source!r}")
                elif isinstance(resolved_source, str):
                    direct_evidence_pages.add(path.resolve())
                elif resolved_source == path.resolve():
                    errors.append(f"{path}: a page cannot cite itself as a source")
                elif wiki_root.resolve() in resolved_source.parents:
                    maintained_source_edges.setdefault(path.resolve(), set()).add(
                        resolved_source
                    )
                else:
                    direct_evidence_pages.add(path.resolve())

    if decision_files and not valid_decision_pages:
        errors.append("wiki/decisions/ must contain at least one decision page")
    if not adoption_decision_pages:
        errors.append(
            "missing Projipsa adoption decision under wiki/decisions/"
        )
    elif len(adoption_decision_pages) > 1:
        errors.append(
            "multiple Projipsa adoption decisions found; initialization must be idempotent"
        )

    evidence_anchored_pages = set(direct_evidence_pages)
    changed = True
    while changed:
        changed = False
        for page, targets in maintained_source_edges.items():
            if page not in evidence_anchored_pages and (
                targets & evidence_anchored_pages
            ):
                evidence_anchored_pages.add(page)
                changed = True

    for page in sorted(confirmed_pages):
        if page not in evidence_anchored_pages:
            errors.append(
                f"{page}: confirmed sources do not reach primary project evidence"
            )

    index_path = root / "index.md"
    if index_path.is_file():
        index_text = index_path.read_text(encoding="utf-8")
        index_targets = local_markdown_targets(index_path, index_text)
        for relative in (
            "wiki/project/overview.md",
            "wiki/project/current-state.md",
            "wiki/questions/open-questions.md",
        ):
            if (root / relative).resolve() not in index_targets:
                errors.append(f"index.md must link required page: {relative}")
        if decision_files and not any(
            path.resolve() in index_targets for path in decision_files
        ):
            errors.append("index.md must link at least one decision page")
        if monthly_logs and not any(
            path.resolve() in index_targets for path in monthly_logs
        ):
            errors.append("index.md must link at least one monthly log")

    for path in files_to_check:
        text = path.read_text(encoding="utf-8")
        errors.extend(local_markdown_links(path, text, root))
        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"{path}: unresolved template placeholder")
        if path in monthly_logs and not text.strip():
            errors.append(f"{path}: monthly log must not be empty")

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
    print(
        "Projipsa memory structure is valid: "
        f"{page_count} maintained page(s) in {root}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

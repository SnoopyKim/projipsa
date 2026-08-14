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


# Without these a tree cannot be read at all: no stated rules, no entry point,
# no briefing. Overview and open questions are not here, because forcing them
# onto a project with nothing yet to say produces template filler, which is the
# unresolved placeholder this script rejects elsewhere.
REQUIRED_FILES = (
    "AGENTS.md",
    "index.md",
    "wiki/project/current-state.md",
)
# A page needs an identity to be linked and a date to be judged stale, and a
# claim needs its evidence. `type` is read from the page's directory when the
# page does not state it; `status` and `confidence` carry defaults; `related`
# was satisfied by an empty list, so requiring it changed nothing.
REQUIRED_FRONTMATTER = (
    "id",
    "updated",
    "sources",
)
DEFAULT_STATUS = "active"
DEFAULT_CONFIDENCE = "inferred"
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
# Chronology defaults to one file per month. Finer units are first-class so
# that parallel writers stop appending to one shared file: `2026-08-12.md` for
# a day, and a day plus `-<slug>` for one branch, session, or engagement. Any
# of them may sit directly under `logs/` or in a subdirectory, as in
# `logs/2026-08/2026-08-12-adapter-split.md`.
CHRONOLOGY_LOG_PATTERN = re.compile(
    r"^(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])"
    r"(?:-(?P<day>0[1-9]|[12]\d|3[01])"
    r"(?:-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*))?"
    r")?"
    r"\.md$"
)
# A dated entry heading, bracketed as the log template writes it or bare. The
# optional operation makes an append-only `integrate` entry an integration
# watermark without adding mutable frontmatter to a shared page.
ENTRY_HEADING_PATTERN = re.compile(
    r"^#{1,6}\s*\[?(?P<date>\d{4}-\d{2}-\d{2})\]?"
    r"(?:\s+(?P<operation>[a-z][a-z0-9-]*))?",
    re.IGNORECASE | re.MULTILINE,
)
# Current state is read at the start of every session, so its length is a
# recurring context cost. Past this much text a briefing page has normally
# absorbed completed history that belongs in chronology. A warning, never an
# error: only the project can say which of its content is still current.
CURRENT_STATE_WARN_CHARS = 12000
CURRENT_STATE_SECTIONS = (
    "Confirmed Current",
    "In Progress",
    "Explicitly Not Current",
    "Active Defaults",
    "Validation",
    "Next Work",
)
POINTER_OPEN = "<!-- projipsa:memory-pointer -->"
POINTER_CLOSE = "<!-- /projipsa:memory-pointer -->"
# Codex reads AGENTS.md; Claude Code reads CLAUDE.md and never reads AGENTS.md.
ROOT_INSTRUCTION_FILES = {"AGENTS.md": "Codex", "CLAUDE.md": "Claude Code"}
# Claude Code resolves an `@path` import anywhere in the text, and `@./AGENTS.md`
# is as valid as `@AGENTS.md`.
AGENTS_IMPORT = re.compile(r"(?:^|\s)@(?:\./)?AGENTS\.md(?![\w./-])")
LINK_PATTERN = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
SCHEME_PATTERN = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
PLACEHOLDER_PATTERN = re.compile(r"\[TODO:|YYYY-MM(?:-DD)?")
CODE_FENCE_PATTERN = re.compile(r"^[ \t]*(`{3,}|~{3,}).*?(?:^[ \t]*\1|\Z)", re.MULTILINE | re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]+`")

FrontmatterValue = Union[str, list[str]]


def resolve_memory_root(candidate: Path) -> Path:
    candidate = candidate.resolve()
    if (candidate / "index.md").is_file():
        return candidate
    if (candidate / "docs" / "index.md").is_file():
        return candidate / "docs"
    return candidate


def prose_only(text: str) -> str:
    """Drop fenced blocks and inline code from the body so documented
    conventions are not mistaken for unresolved placeholders. Frontmatter is
    scanned verbatim, so a backticked placeholder there cannot hide."""
    match = re.match(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if match:
        head, body = text[: match.end()], text[match.end() :]
    else:
        head, body = "", text
    without_fences = CODE_FENCE_PATTERN.sub("", body)
    return head + INLINE_CODE_PATTERN.sub("", without_fences)


def pointer_block(text: str) -> tuple[str | None, str | None]:
    """The single pointer block's contents, or a reason it is unusable. Both
    values are None when the file simply has no block."""
    opened = text.count(POINTER_OPEN)
    closed = text.count(POINTER_CLOSE)
    if opened == 0:
        return None, None
    if opened != 1 or closed != opened:
        return None, "must hold exactly one balanced projipsa:memory-pointer block"
    return text.split(POINTER_OPEN, 1)[1].split(POINTER_CLOSE, 1)[0], None


def names_root(block: str, declared: str) -> bool:
    """Match the declared root as a whole path segment, so a block naming
    `docs-archive/` does not satisfy a memory root of `docs`."""
    return (
        re.search(rf"(?<![\w.-]){re.escape(declared)}(?![\w.-])", block)
        is not None
    )


def validate_root_pointers(root: Path) -> list[str]:
    """Each host discovers the memory root through its own instruction file.
    Require exactly one pointer block naming this root, so a second
    initialization run cannot silently append a competing one."""
    resolved_root = root.resolve()
    boundary = locate_project_boundary(resolved_root)
    if boundary is None:
        return [
            "cannot locate the project root, so the AGENTS.md and CLAUDE.md "
            "memory pointers were not checked; keep the memory root inside a "
            "repository or name it docs/"
        ]

    if boundary == resolved_root:
        # The memory root is the project root, so no outer file points inward.
        # Claude Code still needs CLAUDE.md, because it never reads AGENTS.md.
        claude = boundary / "CLAUDE.md"
        if not claude.is_file():
            return [
                "missing CLAUDE.md: Claude Code never reads AGENTS.md, so it "
                "cannot discover this memory root"
            ]
        text = claude.read_text(encoding="utf-8")
        block, problem = pointer_block(text)
        if problem:
            return [f"{claude}: {problem}"]
        if block is None and not AGENTS_IMPORT.search(text):
            return [
                f"{claude}: must import AGENTS.md or carry a "
                "projipsa:memory-pointer block"
            ]
        return []

    declared = resolved_root.relative_to(boundary).as_posix()
    errors: list[str] = []
    for name, host in ROOT_INSTRUCTION_FILES.items():
        path = boundary / name
        if not path.is_file():
            errors.append(
                f"missing root instruction file {name}: {host} cannot discover "
                f"{declared}/"
            )
            continue

        text = path.read_text(encoding="utf-8")
        block, problem = pointer_block(text)
        if problem:
            errors.append(f"{path}: {problem}")
            continue
        if block is None:
            if name == "CLAUDE.md" and AGENTS_IMPORT.search(text):
                continue
            errors.append(
                f"{path}: no projipsa:memory-pointer block, so {host} never "
                f"learns about {declared}/"
            )
            continue
        if not names_root(block, declared):
            errors.append(
                f"{path}: pointer block does not name the memory root "
                f"{declared!r}"
            )
    return errors


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


def locate_project_boundary(root: Path) -> Path | None:
    """The project root holding the instruction files each host reads. None when
    it cannot be determined, which callers must not treat as a pass."""
    for candidate in (root, *root.parents):
        if (candidate / ".git").exists():
            return candidate.resolve()
    if root.name in {"docs", "documentation", "project-docs"}:
        return root.parent.resolve()
    return None


def find_project_boundary(root: Path) -> Path:
    """Widest path a source citation may reference. Falls back to the memory
    root when the project root cannot be determined."""
    return locate_project_boundary(root) or root.resolve()


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

    instructions = root / "AGENTS.md"
    if instructions.is_file() and not instructions.read_text(
        encoding="utf-8"
    ).strip():
        errors.append("AGENTS.md must state this project's memory rules")

    errors.extend(validate_root_pointers(root))

    wiki_root = root / "wiki"
    wiki_files = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
    if not wiki_files:
        errors.append("no maintained Markdown pages found under wiki/")

    decision_root = wiki_root / "decisions"
    decision_files = (
        sorted(decision_root.rglob("*.md")) if decision_root.is_dir() else []
    )

    logs_root = root / "logs"
    # Walk the whole tree: a nested chronology file used to be invisible here,
    # which silently exempted it from every content check below.
    log_files = sorted(logs_root.rglob("*.md")) if logs_root.is_dir() else []
    chronology_logs: list[Path] = []
    for path in log_files:
        matched = CHRONOLOGY_LOG_PATTERN.fullmatch(path.name)
        if not matched:
            continue
        if matched.group("day"):
            try:
                date(
                    int(matched.group("year")),
                    int(matched.group("month")),
                    int(matched.group("day")),
                )
            except ValueError:
                errors.append(
                    f"{path}: chronology filename must contain a real calendar date"
                )
                continue
        chronology_logs.append(path)
    if not chronology_logs:
        errors.append(
            "missing required chronology log matching logs/YYYY-MM.md; a finer "
            "unit may add -DD or -DD-<slug> and may sit in a subdirectory"
        )

    seen_ids: dict[str, Path] = {}
    valid_decision_pages = 0
    adoption_decision_pages: list[Path] = []
    files_to_check = [
        path
        for path in (root / "index.md", *wiki_files, *log_files)
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
            page_type = None
        # The directory answers this when the page does not. A page filed under
        # wiki/decisions/ is a decision unless it names itself something else.
        is_decision_page = decision_root in path.parents and page_type in (
            None,
            "decision",
        )
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

        # Absent means the default. A page states status or confidence when it
        # departs from `active` and `inferred`, and stating either wrongly is
        # still an error, because a reader acts on both.
        status = values.get("status", DEFAULT_STATUS)
        if "status" in values and (
            not isinstance(status, str) or not status.strip()
        ):
            errors.append(f"{path}: status must be a non-empty scalar value")
        elif isinstance(status, str) and status not in ALLOWED_STATUSES:
            errors.append(f"{path}: unsupported status {status!r}")

        confidence = values.get("confidence", DEFAULT_CONFIDENCE)
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
                elif resolved_source == path.resolve():
                    errors.append(f"{path}: a page cannot cite itself as a source")

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

    index_path = root / "index.md"
    if index_path.is_file():
        index_text = index_path.read_text(encoding="utf-8")
        index_targets = local_markdown_targets(index_path, index_text)
        relative = "wiki/project/current-state.md"
        if (root / relative).resolve() not in index_targets:
            errors.append(f"index.md must link required page: {relative}")
        # A per-session chronology has too many files to list, so linking the
        # directory that holds them is an equally good reading entry point.
        chronology_targets = {path.resolve() for path in chronology_logs}
        resolved_logs_root = logs_root.resolve()
        for chronology_log in chronology_logs:
            for parent in chronology_log.resolve().parents:
                if parent == resolved_logs_root:
                    chronology_targets.add(parent)
                    break
                if resolved_logs_root in parent.parents:
                    chronology_targets.add(parent)
        if chronology_logs and not (index_targets & chronology_targets):
            errors.append(
                "index.md must link the chronology: a log file or the "
                "directory holding it"
            )

    for path in files_to_check:
        text = path.read_text(encoding="utf-8")
        errors.extend(local_markdown_links(path, text, root))
        if PLACEHOLDER_PATTERN.search(prose_only(text)):
            errors.append(f"{path}: unresolved template placeholder")
        if path in log_files and not text.strip():
            errors.append(f"{path}: chronology log must not be empty")

    return errors


def chronology_dates(path: Path) -> list[date]:
    """Dates a chronology file claims: the day its own name carries, when it
    has one, plus every dated entry heading inside it. A monthly file names no
    day, so its headings are the only precise signal it offers."""
    dates: list[date] = []
    named = CHRONOLOGY_LOG_PATTERN.fullmatch(path.name)
    if named and named.group("day"):
        try:
            dates.append(
                date(
                    int(named.group("year")),
                    int(named.group("month")),
                    int(named.group("day")),
                )
            )
        except ValueError:
            # A name like 2026-02-31 is well formed but not a real day.
            pass
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return dates
    for matched_heading in ENTRY_HEADING_PATTERN.finditer(text):
        try:
            dates.append(date.fromisoformat(matched_heading.group("date")))
        except ValueError:
            continue
    return dates


def integration_dates(path: Path) -> list[date]:
    """Dates of append-only Integrate entries. This is a watermark rather than
    a claim that current state changed: Integrate may correctly conclude that
    merged writer work has no project-level consequence for that page."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []

    dates: list[date] = []
    for matched_heading in ENTRY_HEADING_PATTERN.finditer(text):
        if (matched_heading.group("operation") or "").lower() != "integrate":
            continue
        try:
            dates.append(date.fromisoformat(matched_heading.group("date")))
        except ValueError:
            continue
    return dates


def pending_integration(root: Path, current_state: Path) -> list[str]:
    """Per-writer chronology newer than the last shared-state or Integrate
    watermark. This proves work still needs integration after it merges, not
    that the current checkout already contains the merged result. Monthly and
    day logs are single-writer units and never trigger this signal."""
    parsed = parse_frontmatter(current_state)
    if parsed is None:
        return []
    values, _ = parsed
    updated = values.get("updated")
    if not isinstance(updated, str):
        return []
    try:
        written = date.fromisoformat(updated.strip())
    except ValueError:
        return []

    logs_root = root / "logs"
    if not logs_root.is_dir():
        return []
    log_files = sorted(logs_root.rglob("*.md"))
    chronology_files: list[tuple[Path, re.Match[str]]] = []
    for path in log_files:
        matched = CHRONOLOGY_LOG_PATTERN.fullmatch(path.name)
        if not matched:
            continue
        if matched.group("day"):
            try:
                date(
                    int(matched.group("year")),
                    int(matched.group("month")),
                    int(matched.group("day")),
                )
            except ValueError:
                continue
        chronology_files.append((path, matched))

    writer_dates = [
        entry
        for path, matched in chronology_files
        if matched.group("slug")
        for entry in chronology_dates(path)
    ]
    latest_writer = max(writer_dates, default=None)
    integration_watermarks = [written]
    for path, _ in chronology_files:
        integration_watermarks.extend(integration_dates(path))
    integrated_through = max(integration_watermarks)
    if latest_writer is None or latest_writer <= integrated_through:
        return []
    return [
        f"{current_state}: per-writer chronology reaches "
        f"{latest_writer.isoformat()} but shared state is integrated only "
        f"through {integrated_through.isoformat()}; after those writer logs "
        "merge, run Integrate on the branch holding the merged result; on a "
        "writer branch report the integration as pending instead"
    ]


def unanchored_confirmed_pages(root: Path) -> list[Path]:
    """Pages claiming `confirmed` whose source chain never reaches primary
    evidence, because it only ever cites other maintained pages. The claim may
    well be true, and only the project can either produce the evidence or lower
    the claim, so this reports instead of failing."""
    wiki_root = root / "wiki"
    if not wiki_root.is_dir():
        return []
    project_boundary = find_project_boundary(root)
    wiki_resolved = wiki_root.resolve()

    confirmed: set[Path] = set()
    anchored: set[Path] = set()
    edges: dict[Path, set[Path]] = {}
    for path in sorted(wiki_root.rglob("*.md")):
        parsed = parse_frontmatter(path)
        if parsed is None:
            continue
        values, _ = parsed
        resolved_page = path.resolve()
        if values.get("confidence", DEFAULT_CONFIDENCE) == "confirmed":
            confirmed.add(resolved_page)
        sources = values.get("sources")
        if not isinstance(sources, list):
            continue
        for source in sources:
            target = resolve_source_target(source, path, root, project_boundary)
            if target is None or target == resolved_page:
                continue
            if isinstance(target, Path) and wiki_resolved in target.parents:
                edges.setdefault(resolved_page, set()).add(target)
            else:
                anchored.add(resolved_page)

    changed = True
    while changed:
        changed = False
        for page, targets in edges.items():
            if page not in anchored and (targets & anchored):
                anchored.add(page)
                changed = True

    return [page for page in sorted(confirmed) if page not in anchored]


def collect_warnings(root: Path) -> list[str]:
    """Drift signals that never fail validation. A tree can satisfy every
    structural rule while a page has quietly stopped doing its job, and only
    the project can decide which of its content is still current."""
    warnings: list[str] = []
    current_state = root / "wiki" / "project" / "current-state.md"
    if current_state.is_file():
        warnings.extend(pending_integration(root, current_state))
        text = current_state.read_text(encoding="utf-8")
        if len(text) > CURRENT_STATE_WARN_CHARS:
            warnings.append(
                f"{current_state}: {len(text)} characters for a page every "
                "session reads; move work that is no longer current into "
                "chronology, delivery, decision, or milestone pages and link it"
            )
            headings = {
                line.lstrip("#").strip()
                for line in text.splitlines()
                if line.startswith("#")
            }
            # A page within budget may name its sections however it likes.
            missing_sections = [
                section
                for section in CURRENT_STATE_SECTIONS
                if section not in headings
            ]
            if missing_sections:
                warnings.append(
                    f"{current_state}: this long page has no section for "
                    f"{', '.join(missing_sections)}; check whether that content "
                    "was absorbed into a summary or a list of completed work"
                )

    warnings.extend(
        f"{page}: confirmed sources do not reach primary project evidence; "
        "add the evidence, or lower the claim to assumed or inferred"
        for page in unanchored_confirmed_pages(root)
    )

    return warnings


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
    for warning in collect_warnings(root):
        print(f"warning: {warning}", file=sys.stderr)
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

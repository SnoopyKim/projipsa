#!/usr/bin/env python3
"""Read-only inventory for Projipsa memory compaction."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import unquote, urlparse


IMAGE_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_IMAGE = re.compile(
    r"<img\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"]",
    re.IGNORECASE,
)
SEMANTIC_NOISE = {
    "after",
    "before",
    "board",
    "capture",
    "comparison",
    "component",
    "copy",
    "crop",
    "cropped",
    "detail",
    "export",
    "final",
    "image",
    "new",
    "old",
    "screen",
    "screenshot",
    "variant",
    "보드",
    "비교",
    "사본",
    "스크린샷",
    "이전",
    "이후",
    "최종",
    "캡처",
    "컴포넌트",
    "크롭",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_git(cwd: Path, *args: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout


def repository_info(root: Path) -> dict[str, Any]:
    top_output = run_git(root, "rev-parse", "--show-toplevel")
    if top_output is None:
        return {
            "repository_root": None,
            "baseline": None,
            "tracked_paths": set(),
            "modified_paths": set(),
            "status": [],
        }

    repository_root = Path(top_output.strip()).resolve()
    try:
        root_pathspec = root.relative_to(repository_root).as_posix() or "."
    except ValueError:
        root_pathspec = "."

    baseline_output = run_git(repository_root, "rev-parse", "HEAD")
    tracked_output = run_git(
        repository_root, "ls-files", "-z", "--", root_pathspec
    )
    tracked_paths = set()
    if tracked_output:
        for repo_relative in tracked_output.split("\0"):
            if not repo_relative:
                continue
            absolute = (repository_root / repo_relative).resolve()
            try:
                tracked_paths.add(absolute.relative_to(root).as_posix())
            except ValueError:
                continue

    status_output = run_git(
        repository_root,
        "status",
        "--short",
        "--untracked-files=all",
        "--",
        root_pathspec,
    )
    modified_output = run_git(
        repository_root,
        "diff",
        "--name-only",
        "-z",
        "HEAD",
        "--",
        root_pathspec,
    )
    modified_paths = set()
    if modified_output:
        for repo_relative in modified_output.split("\0"):
            if not repo_relative:
                continue
            absolute = (repository_root / repo_relative).resolve()
            try:
                modified_paths.add(absolute.relative_to(root).as_posix())
            except ValueError:
                continue
    return {
        "repository_root": str(repository_root),
        "baseline": baseline_output.strip() if baseline_output else None,
        "tracked_paths": tracked_paths,
        "modified_paths": modified_paths,
        "status": sorted(status_output.splitlines()) if status_output else [],
    }


def files_under(root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file() and not path.is_symlink() and ".git" not in path.parts
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def extract_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    if target[:1] in {"'", '"'} and target[0] in target[1:]:
        return target[1 : target[1:].index(target[0]) + 1]
    if " " in target:
        target = target.split(" ", 1)[0]
    return target.strip("'\"<>")


def resolve_local_image(
    root: Path,
    markdown: Path,
    target: str,
    prefer_root: bool = False,
) -> Optional[str]:
    target = unquote(target.strip())
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc or target.startswith("#"):
        return None
    clean = parsed.path
    if not clean or Path(clean).suffix.lower() not in IMAGE_EXTENSIONS:
        return None
    target_path = Path(clean)
    if target_path.is_absolute():
        candidates = [root / clean.lstrip("/")]
    elif prefer_root:
        candidates = [root / target_path, markdown.parent / target_path]
    else:
        candidates = [markdown.parent / target_path, root / target_path]
    for candidate in candidates:
        candidate = candidate.resolve()
        try:
            relative = candidate.relative_to(root).as_posix()
        except ValueError:
            continue
        if candidate.is_file():
            return relative
    return None


def referenced_images(root: Path, markdown_files: Iterable[Path]) -> set[str]:
    references = set()
    for markdown in markdown_files:
        text = markdown.read_text(encoding="utf-8", errors="replace")
        linked_targets = [
            extract_link_target(value) for value in MARKDOWN_LINK.findall(text)
        ]
        linked_targets.extend(HTML_IMAGE.findall(text))
        source_targets = [
            extract_link_target(value)
            for value in re.findall(r"^\s*-\s+(.+?)\s*$", text, re.MULTILINE)
        ]
        for target in linked_targets:
            resolved = resolve_local_image(root, markdown, target)
            if resolved:
                references.add(resolved)
        for target in source_targets:
            resolved = resolve_local_image(
                root, markdown, target, prefer_root=True
            )
            if resolved:
                references.add(resolved)
    return references


def normalized_stem(path: Path) -> str:
    tokens = re.split(r"[\W_]+", path.stem.lower())
    meaningful = []
    for token in tokens:
        if not token or token in SEMANTIC_NOISE:
            continue
        if token.isdigit() or re.fullmatch(r"v\d+", token):
            continue
        if re.fullmatch(r"\d+x\d+", token):
            continue
        meaningful.append(token)
    return "-".join(meaningful)


def audit_memory(memory_root: Path) -> dict[str, Any]:
    root = memory_root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"memory root is not a directory: {root}")

    files = files_under(root)
    images = [path for path in files if path.suffix.lower() in IMAGE_EXTENSIONS]
    markdown_files = [path for path in files if path.suffix.lower() == ".md"]
    references = referenced_images(root, markdown_files)
    git = repository_info(root)
    tracked_paths = git.pop("tracked_paths")
    modified_paths = git.pop("modified_paths")

    def recoverability(relative: str) -> str:
        if relative not in tracked_paths:
            return "untracked"
        if relative in modified_paths:
            return "current-content-not-at-baseline"
        if git["baseline"]:
            return "baseline"
        return "tracked-without-baseline"

    hashes: dict[str, list[Path]] = defaultdict(list)
    for path in images:
        hashes[sha256(path)].append(path)

    duplicate_groups = []
    for digest, paths in sorted(hashes.items()):
        if len(paths) < 2:
            continue
        paths = sorted(paths, key=lambda path: path.relative_to(root).as_posix())
        bytes_each = paths[0].stat().st_size
        relative_paths = [path.relative_to(root).as_posix() for path in paths]
        duplicate_groups.append(
            {
                "sha256": digest,
                "bytes_each": bytes_each,
                "reclaimable_bytes": bytes_each * (len(paths) - 1),
                "paths": relative_paths,
                "tracked": [path in tracked_paths for path in relative_paths],
                "recoverability": [
                    recoverability(path) for path in relative_paths
                ],
            }
        )

    semantic_candidates: dict[tuple[str, str], list[str]] = defaultdict(list)
    for path in images:
        normalized = normalized_stem(path)
        if not normalized:
            continue
        relative = path.relative_to(root)
        semantic_candidates[(relative.parent.as_posix(), normalized)].append(
            relative.as_posix()
        )
    semantic_groups = [
        {"directory": directory, "normalized_stem": stem, "paths": sorted(paths)}
        for (directory, stem), paths in sorted(semantic_candidates.items())
        if len(paths) > 1
    ]

    unreferenced = []
    for path in images:
        relative = path.relative_to(root).as_posix()
        if relative in references:
            continue
        unreferenced.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "tracked": relative in tracked_paths,
                "recoverability": recoverability(relative),
            }
        )

    raw_files = [path for path in files if "raw" in path.relative_to(root).parts]
    raw_images = [
        path for path in images if "raw" in path.relative_to(root).parts
    ]
    image_bytes = sum(path.stat().st_size for path in images)
    image_paths = {path.relative_to(root).as_posix() for path in images}
    largest_files = []
    for path in sorted(
        files,
        key=lambda candidate: (
            -candidate.stat().st_size,
            candidate.relative_to(root).as_posix(),
        ),
    )[:25]:
        relative = path.relative_to(root).as_posix()
        is_image = path.suffix.lower() in IMAGE_EXTENSIONS
        largest_files.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "kind": (
                    "image"
                    if is_image
                    else "markdown"
                    if path.suffix.lower() == ".md"
                    else "other"
                ),
                "in_raw": "raw" in path.relative_to(root).parts,
                "referenced": relative in references if is_image else None,
                "tracked": relative in tracked_paths,
                "recoverability": recoverability(relative),
            }
        )
    report = {
        "memory_root": str(root),
        "summary": {
            "file_count": len(files),
            "total_bytes": sum(path.stat().st_size for path in files),
            "raw_file_count": len(raw_files),
            "raw_bytes": sum(path.stat().st_size for path in raw_files),
            "raw_image_file_count": len(raw_images),
            "raw_image_bytes": sum(path.stat().st_size for path in raw_images),
            "image_file_count": len(images),
            "image_bytes": image_bytes,
            "referenced_image_count": len(references.intersection(image_paths)),
            "unreferenced_image_count": len(unreferenced),
            "exact_duplicate_group_count": len(duplicate_groups),
            "exact_duplicate_reclaimable_bytes": sum(
                group["reclaimable_bytes"] for group in duplicate_groups
            ),
            "semantic_review_group_count": len(semantic_groups),
        },
        "git": git,
        "largest_files": largest_files,
        "exact_duplicates": duplicate_groups,
        "unreferenced_images": unreferenced,
        "semantic_review_groups": semantic_groups,
        "warnings": [
            "Unreferenced images are review candidates, not automatic deletions.",
            "Semantic filename groups require visual review and active-evidence checks.",
            "Working-tree bytes do not measure bytes retained in Git history.",
            "Modified tracked content may not be recoverable from the reported baseline.",
        ],
    }
    return report


def render_text(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"Memory root: {report['memory_root']}",
        f"Files: {summary['file_count']} ({summary['total_bytes']} bytes)",
        f"Raw: {summary['raw_file_count']} ({summary['raw_bytes']} bytes)",
        (
            "Raw images: "
            f"{summary['raw_image_file_count']} ({summary['raw_image_bytes']} bytes)"
        ),
        f"Images: {summary['image_file_count']} ({summary['image_bytes']} bytes)",
        (
            "Exact image duplicate groups: "
            f"{summary['exact_duplicate_group_count']} "
            f"({summary['exact_duplicate_reclaimable_bytes']} reclaimable bytes)"
        ),
        f"Unreferenced image candidates: {summary['unreferenced_image_count']}",
        f"Semantic review groups: {summary['semantic_review_group_count']}",
        f"Git baseline: {report['git']['baseline'] or 'not available'}",
    ]
    if report["largest_files"]:
        lines.append("\nLargest files:")
        for item in report["largest_files"][:10]:
            lines.append(f"- {item['bytes']} bytes: {item['path']}")
    if report["exact_duplicates"]:
        lines.append("\nExact duplicate groups:")
        for group in report["exact_duplicates"]:
            lines.append(
                f"- {group['sha256']}: {', '.join(group['paths'])}"
            )
    if report["semantic_review_groups"]:
        lines.append("\nSemantic review groups (not deletion findings):")
        for group in report["semantic_review_groups"]:
            lines.append(f"- {', '.join(group['paths'])}")
    lines.append("\nWarnings:")
    lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only inventory for Projipsa memory compaction."
    )
    parser.add_argument("memory_root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = audit_memory(args.memory_root)
    except ValueError as exc:
        raise SystemExit(str(exc))
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Explicit memory relations, evidence drift, and bounded task context. Python 3.9+."""

from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit

from validate_memory import (
    CODE_FENCE_PATTERN, INLINE_CODE_PATTERN, ID_PATTERN, LIST_FIELDS,
    find_project_boundary, is_within, parse_frontmatter, resolve_memory_root,
)

RELATIONS = ("related", "supersedes", "superseded_by", "depends_on", "blocks")
DEPENDENCIES = {"sources", "depends_on"}
STATE_FILE = ".projipsa/evidence-baseline.json"
SCHEMA_VERSION = 1
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>\n]+>|(?:[^()\n]|\([^()\n]*\))+)\)")
REFERENCE_DEF = re.compile(r"^ {0,3}\[([^\]\n]+)\]:\s*(.+)$", re.MULTILINE)
REFERENCE_USE = re.compile(r"!?\[([^\]\n]+)\](?:\[([^\]\n]*)\])?")


def body_only(text):
    return re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", text, count=1, flags=re.S)


def link_destination(raw):
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1:raw.index(">")]
    return re.split(r'\s+[\'\"]', raw, maxsplit=1)[0].strip()


def markdown_links(body):
    prose = INLINE_CODE_PATTERN.sub("", CODE_FENCE_PATTERN.sub("", body))
    targets = [link_destination(m.group(1)) for m in INLINE_LINK.finditer(prose)]
    definitions = {m.group(1).casefold(): link_destination(m.group(2))
                   for m in REFERENCE_DEF.finditer(prose)}
    for match in REFERENCE_USE.finditer(REFERENCE_DEF.sub("", prose)):
        key = (match.group(2) or match.group(1)).casefold()
        if key in definitions:
            targets.append(definitions[key])
    return sorted(set(targets))


def digest_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def terms(text):
    return sorted(set(re.findall(r"[\w.-]+", text.casefold(), re.UNICODE)))


class Memory:
    def __init__(self, root):
        self.root = resolve_memory_root(Path(root).expanduser())
        if not (self.root / "wiki").is_dir():
            raise ValueError("No wiki directory; pass the adopted memory root explicitly")
        self.boundary = find_project_boundary(self.root)
        self.nodes = {}
        self.edges = []
        self.warnings = []
        self.path_ids = {}
        self._edge_keys = set()
        self._load_documents()
        for node in list(self.nodes.values()):
            if node["kind"] not in {"page", "event"}:
                continue
            for source in node.get("metadata", {}).get("sources", []):
                target = self._target(source, node, source_field=True)
                self._edge(node["id"], target, "sources", source)
            for relation in RELATIONS:
                for target in node.get("metadata", {}).get(relation, []):
                    if target not in self.nodes:
                        self.nodes[target] = {"id": target, "kind": "unresolved",
                                              "title": target, "availability": "missing"}
                        self.warnings.append(f"{node['id']}: unresolved {relation}: {target}")
                    self._edge(node["id"], target, relation, target)
            for reference in markdown_links(node["_body"]):
                if not reference.startswith("#"):
                    target = self._target(reference, node, source_field=False)
                    self._edge(node["id"], target, "links", reference)
        self.edges.sort(key=lambda e: (e["from"], e["relation"], e["to"], e["reference"]))

    def _load_documents(self):
        for directory, kind in (("wiki", "page"), ("logs", "event")):
            for path in sorted((self.root / directory).rglob("*.md")):
                if not is_within(path.resolve(), self.boundary):
                    raise ValueError(f"Document escapes project boundary: {path}")
                parsed = parse_frontmatter(path) if kind == "page" else None
                if kind == "page" and not parsed:
                    raise ValueError(f"Missing frontmatter: {path}")
                metadata, text = parsed if parsed else ({}, path.read_text(encoding="utf-8"))
                if kind == "page":
                    page_id = metadata.get("id", "")
                    if not isinstance(page_id, str) or not ID_PATTERN.fullmatch(page_id):
                        raise ValueError(f"Invalid page ID: {path}")
                    for field in LIST_FIELDS:
                        if field in metadata and not isinstance(metadata[field], list):
                            raise ValueError(f"{path}: {field} must be a list")
                    if "sources" not in metadata:
                        raise ValueError(f"{path}: sources must be stated")
                else:
                    page_id = "event:" + path.relative_to(self.root).as_posix()
                if page_id in self.nodes or path.resolve() in self.path_ids:
                    raise ValueError(f"Duplicate page identity or file: {page_id}")
                body = body_only(text)
                heading = re.search(r"^#\s+(.+)$", body, re.M)
                self.nodes[page_id] = {
                    "id": page_id, "kind": kind,
                    "path": path.relative_to(self.boundary).as_posix(),
                    "memory_path": path.relative_to(self.root).as_posix(),
                    "title": heading.group(1) if heading else path.stem,
                    "status": metadata.get("status", "active") if kind == "page" else "historical",
                    "confidence": metadata.get("confidence", "inferred") if kind == "page" else "event",
                    "type": metadata.get("type", path.parent.name),
                    "updated": metadata.get("updated"), "metadata": metadata,
                    "sha256": digest_file(path),
                    "availability": "present", "_body": body, "_file": path,
                }
                self.path_ids[path.resolve()] = page_id

    def _target(self, reference, owner, source_field):
        target = reference.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            key = "url:" + target
            self.nodes.setdefault(key, {"id": key, "kind": "evidence", "title": target,
                                        "url": target, "availability": "external_unchecked"})
            return key
        clean = unquote(parsed.path)
        relative = Path(clean)
        if not clean or parsed.scheme or parsed.netloc or relative.is_absolute():
            return self._unresolved(owner, reference, "unsupported")
        page_dir = owner["_file"].parent
        bases = (self.root, self.boundary, page_dir) if source_field else (page_dir, self.root)
        candidates = list(dict.fromkeys((base / relative).resolve() for base in bases))
        safe = [p for p in candidates if is_within(p, self.boundary)
                and ".git" not in p.relative_to(self.boundary).parts
                and not is_within(p, self.root / ".projipsa")]
        found = next((p for p in safe if p.is_file()), None)
        # Keep missing files addressable for impact queries without guessing a
        # memory-relative path ahead of a repository path whose parent exists.
        path = found or next((p for p in safe if p.parent.is_dir()), None)
        if path is None:
            return self._unresolved(owner, reference, "missing" if safe else "outside_project")
        if path in self.path_ids:
            return self.path_ids[path]
        key = "file:" + path.relative_to(self.boundary).as_posix()
        if key not in self.nodes:
            node = {"id": key, "kind": "evidence", "title": path.name,
                    "path": path.relative_to(self.boundary).as_posix(), "availability": "missing"}
            if found:
                try:
                    node.update(availability="present", sha256=digest_file(path))
                except OSError:
                    node["availability"] = "unreadable"
            self.nodes[key] = node
        return key

    def _unresolved(self, owner, reference, reason):
        key = "unresolved:" + owner["id"] + ":" + reference
        self.nodes.setdefault(key, {"id": key, "kind": "unresolved", "title": reference,
                                    "availability": reason})
        self.warnings.append(f"{owner['id']}: {reason} reference: {reference}")
        return key

    def _edge(self, source, target, relation, reference):
        key = (source, target, relation, reference)
        if key not in self._edge_keys:
            self._edge_keys.add(key)
            self.edges.append({"from": source, "to": target, "relation": relation,
                               "reference": reference, "origin": "explicit",
                               "declared_in": self.nodes[source]["path"]})

    def walk(self, seeds, reverse=False, relations=None, depth=None):
        found = set(seeds)
        queue = deque((s, 0) for s in seeds)
        adjacency = {}
        for edge in self.edges:
            if relations is not None and edge["relation"] not in relations:
                continue
            left, right = (edge["to"], edge["from"]) if reverse else (edge["from"], edge["to"])
            adjacency.setdefault(left, set()).add(right)
        while queue:
            node_id, distance = queue.popleft()
            if depth is not None and distance >= depth:
                continue
            for target in sorted(adjacency.get(node_id, [])):
                if target not in found:
                    found.add(target)
                    queue.append((target, distance + 1))
        return found

    def source_ids(self, source):
        if source in self.nodes:
            return {source}
        paths = {(self.boundary / source).resolve(), (self.root / source).resolve()}
        found = {key for key, node in self.nodes.items()
                 if node.get("url") == source or
                 (node.get("path") and (self.boundary / node["path"]).resolve() in paths)}
        found.update(edge["to"] for edge in self.edges if edge["reference"] == source)
        if not found:
            raise ValueError(f"Source has no indexed references: {source}")
        return found

    def evidence_state(self, page_id):
        deps = self.walk({page_id}, relations=DEPENDENCIES) - {page_id}
        return {key: {k: self.nodes[key][k] for k in ("path", "url", "sha256", "availability")
                      if k in self.nodes[key]} for key in sorted(deps)}

    def public_node(self, key):
        return {k: v for k, v in self.nodes[key].items() if not k.startswith("_")}


def state_path(memory):
    path = memory.root / STATE_FILE
    if not is_within(path.resolve(), memory.root) or path.is_symlink():
        raise ValueError("Evidence baseline must be a local regular file inside the memory root")
    return path


def load_baseline(memory):
    path = state_path(memory)
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "pages": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION or not isinstance(data.get("pages"), dict):
        raise ValueError("Unsupported or malformed evidence baseline; do not reset it silently")
    for key, record in data["pages"].items():
        if not isinstance(record, dict) or not isinstance(record.get("sources"), dict) or not isinstance(record.get("page_sha256"), str):
            raise ValueError(f"Malformed baseline entry: {key}")
        if any(not isinstance(value, dict) for value in record["sources"].values()):
            raise ValueError(f"Malformed source baseline: {key}")
    return data


def review(memory):
    baseline = load_baseline(memory)
    results = []
    for key, node in sorted(memory.nodes.items()):
        if node["kind"] != "page":
            continue
        current = memory.evidence_state(key)
        previous = baseline["pages"].get(key)
        reasons = []
        for source, state in current.items():
            if state["availability"] not in {"present", "external_unchecked"}:
                reasons.append({"code": "evidence_unavailable", "source": source,
                                "availability": state["availability"]})
        if previous:
            if previous["page_sha256"] != node["sha256"]:
                reasons.append({"code": "page_changed_since_checkpoint"})
            old = previous["sources"]
            if set(old) != set(current):
                reasons.append({"code": "evidence_set_changed", "added": sorted(set(current) - set(old)),
                                "removed": sorted(set(old) - set(current))})
            for source in sorted(set(current) & set(old)):
                before, after = old[source], current[source]
                if after.get("sha256") != before.get("sha256") or after.get("availability") != before.get("availability"):
                    reasons.append({"code": "source_changed", "source": source,
                                    "before": before, "after": after})
        results.append({"id": key, "path": node["path"], "page_status": node["status"],
                        "review_status": "candidate" if reasons else "unchanged" if previous else "no_checkpoint",
                        "checked_at": previous.get("checked_at") if previous else None,
                        "external_unchecked": [k for k, v in current.items() if v["availability"] == "external_unchecked"],
                        "reasons": reasons})
    return {"schema_version": SCHEMA_VERSION, "pages": results,
            "orphaned_checkpoints": sorted(set(baseline["pages"]) - set(memory.nodes)),
            "warnings": memory.warnings,
            "meaning": "Candidates need review; unchanged hashes do not prove factual correctness. External content was not fetched."}


def checkpoint(memory, page_ids):
    if not page_ids:
        raise ValueError("Checkpoint requires explicit --page IDs already reviewed by the caller")
    entries = {}
    for key in sorted(set(page_ids)):
        node = memory.nodes.get(key, {})
        if node.get("kind") != "page":
            raise ValueError(f"Unknown maintained page: {key}")
        sources = memory.evidence_state(key)
        if any(v["availability"] not in {"present", "external_unchecked"} for v in sources.values()):
            raise ValueError(f"Resolve unavailable evidence before checkpointing {key}")
        entries[key] = {"page_sha256": node["sha256"], "sources": sources,
                        "checked_at": datetime.now(timezone.utc).isoformat()}
    path = state_path(memory)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(".lock")
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("Another checkpoint owns the baseline lock; inspect it before retrying")
    os.close(fd)
    temporary = None
    try:
        data = load_baseline(memory)
        data["pages"].update(entries)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
        lock.unlink()
    return {"schema_version": SCHEMA_VERSION, "checkpointed": sorted(entries),
            "path": STATE_FILE, "external_content_checked": False}


def select(memory, query="", pages=(), sources=(), limit=8):
    seeds = set()
    for key in pages:
        if memory.nodes.get(key, {}).get("kind") != "page":
            raise ValueError(f"Unknown maintained page: {key}")
        seeds.add(key)
    for source in sources:
        seeds.update(memory.walk(memory.source_ids(source), reverse=True, relations=DEPENDENCIES))
    scores = {}
    query_terms = terms(query)
    for key, node in memory.nodes.items():
        if node["kind"] not in {"page", "event"}:
            continue
        title = (key + " " + node["title"]).casefold()
        body = node["_body"].casefold()
        score = sum(6 * (term in title) + (term in body) for term in query_terms)
        if score:
            scores[key] = score
    ranked = sorted(scores, key=lambda k: (-scores[k], k))
    seeds.update(ranked[:limit])
    connected = (memory.walk(seeds, depth=1) | memory.walk(seeds, reverse=True, depth=1)) - seeds
    documents = [key for key in seeds | connected if memory.nodes[key]["kind"] in {"page", "event"}]
    documents.sort(key=lambda k: (k not in seeds, -scores.get(k, 0),
                                 memory.nodes[k]["status"] in {"superseded", "archived", "historical"}, k))
    return documents, seeds


def excerpt(body, query, cap):
    # Rank sections, not just the first N bytes: outcomes and rejected options
    # are often near the end of a decision. These are excerpts, not new claims.
    sections = re.split(r"(?=^#{1,6}\s)", body, flags=re.M)
    tokens = terms(query)
    useful = re.compile(r"decision|reason|alternative|constraint|outcome|revisit|failure|question|결정|이유|대안|제약|결과|실패|질문", re.I)
    ranked = sorted(enumerate(sections), key=lambda pair: (
        -sum(t in pair[1].casefold() for t in tokens),
        -bool(useful.search(pair[1].split('\n', 1)[0])), pair[0]))
    result = []
    remaining = cap
    for _, section in ranked:
        content = section.strip()
        if not content or remaining < 80:
            continue
        piece = content[:min(remaining - 2, 650)]
        if len(piece) < len(content):
            piece = piece[:-1] + "…"
        result.append(piece)
        remaining -= len(piece) + 2
    return "\n\n".join(result)


def brief(memory, query="", pages=(), sources=(), limit=8, budget=8000):
    if not query.strip() and not pages and not sources:
        raise ValueError("Brief needs --query, --page, or --source to select relevant memory")
    documents, seeds = select(memory, query, pages, sources, limit)
    reviews = {item["id"]: item for item in review(memory)["pages"]}
    chunks = ["# Task memory\n\nSource excerpts; use linked originals for decisions. Historical and superseded records are not current truth."]
    included = []
    for key in documents[:limit]:
        node = memory.nodes[key]
        state = reviews.get(key, {}).get("review_status", "historical")
        warning = " | external evidence unchecked" if reviews.get(key, {}).get("external_unchecked") else ""
        header = f"\n\n## {node['title']}\n{key} | {node['status']} | {node['confidence']} | {state}{warning}\nSource: {node['path']}\n"
        follow = sorted({f"{e['relation']}: {e['to']}" for e in memory.edges
                         if e["from"] == key and e["relation"] in RELATIONS})
        if follow:
            header += "Follow: " + "; ".join(follow)[:500] + "\n"
        reasons = sorted({r["code"] for r in reviews.get(key, {}).get("reasons", [])})
        if reasons:
            header += "Review: " + ", ".join(reasons) + "\n"
        available = budget - sum(len(s) for s in chunks) - len(header) - 180
        if available < 120:
            break
        chunks.append(header + excerpt(node["_body"], query, min(available, 1400)))
        included.append(key)
    omitted = len(documents) - len(included)
    footer = f"\n\nIncluded {len(included)}; omitted {omitted} from selected neighborhood. Warnings: {len(memory.warnings)}."
    if not documents:
        footer += " No matches; broaden terms and inspect the index. This is not proof that no relevant memory exists."
    text = "".join(chunks) + footer
    return {"schema_version": SCHEMA_VERSION, "text": text, "characters": len(text),
            "budget": budget, "included": included, "omitted": omitted,
            "selection": "lexical matches and explicit relations; no semantic inference",
            "relations": [e for e in memory.edges if e["from"] in included or e["to"] in included],
            "review": [reviews[key] for key in included if key in reviews], "warnings": memory.warnings}


def graph(memory, pages=(), sources=(), limit=40):
    seeds = set()
    focus = set(pages)
    for source in sources:
        focus.update(memory.source_ids(source))
    if pages or sources:
        documents, seeds = select(memory, pages=pages, sources=sources, limit=limit)
        keys = memory.walk(seeds, depth=1) | memory.walk(seeds, reverse=True, depth=1) | set(documents)
    else:
        keys = set(memory.nodes)
    ordered = sorted(keys, key=lambda k: (k not in focus, k not in seeds, memory.nodes[k]["kind"] != "page", k))
    included = set(ordered[:limit])
    reviews = {p["id"]: p for p in review(memory)["pages"]}
    return {"schema_version": SCHEMA_VERSION,
            "nodes": [dict(memory.public_node(k), review_status=reviews.get(k, {}).get("review_status"),
                           review_candidate=reviews.get(k, {}).get("review_status") == "candidate")
                      for k in sorted(included)],
            "edges": [e for e in memory.edges if e["from"] in included and e["to"] in included],
            "omitted_nodes": len(keys) - len(included), "warnings": memory.warnings}


def mermaid(data):
    lines = ["flowchart LR"]
    aliases = {node["id"]: f"n{i}" for i, node in enumerate(data["nodes"])}
    for node in data["nodes"]:
        status = node.get("status", node["availability"])
        if node.get("review_status"):
            status += " / " + node["review_status"]
        label = html.escape(f"{node['title'][:75]} ({status})", quote=True)
        label = label.replace("\n", " ").replace("\\", "&#92;").replace("`", "&#96;")
        lines.append(f'  {aliases[node["id"]]}["{label}"]' + (":::review" if node["review_candidate"] else ""))
    seen = set()
    for edge in data["edges"]:
        value = (edge["from"], edge["to"], edge["relation"])
        if value not in seen:
            seen.add(value)
            lines.append(f'  {aliases[edge["from"]]} -->|{edge["relation"]}| {aliases[edge["to"]]}')
    lines.extend(["  classDef review fill:#fff2cc,stroke:#9a6700,color:#24292f",
                  f"  %% {data['omitted_nodes']} nodes omitted; highlighted pages need review, not automatic invalidation."])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Adopted memory root (or project with docs/)")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("graph", "brief", "review", "checkpoint"):
        command = sub.add_parser(name)
        if name != "review":
            command.add_argument("--page", action="append", default=[])
        if name in {"graph", "brief"}:
            command.add_argument("--source", action="append", default=[])
            command.add_argument("--limit", type=int, default=8 if name == "brief" else 40)
        formats = ("json", "mermaid") if name == "graph" else ("json", "markdown") if name == "brief" else ("json",)
        command.add_argument("--format", choices=formats,
                             default="markdown" if name == "brief" else "json")
        if name == "brief":
            command.add_argument("--query", default="")
            command.add_argument("--budget", type=int, default=8000, help="Maximum Markdown characters; JSON metadata is separate")
    args = parser.parse_args(argv)
    try:
        if getattr(args, "limit", 1) < 1 or getattr(args, "budget", 1000) < 1000:
            raise ValueError("limit must be positive; briefing budget must be at least 1000 characters")
        memory = Memory(args.root)
        if args.command == "checkpoint":
            result = checkpoint(memory, args.page)
        elif args.command == "review":
            result = review(memory)
        elif args.command == "brief":
            result = brief(memory, args.query, args.page, args.source, args.limit, args.budget)
        else:
            result = graph(memory, args.page, args.source, args.limit)
        if args.format == "mermaid":
            print(mermaid(result))
        elif args.format == "markdown" and args.command == "brief":
            print(result["text"])
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print(f"memory_context: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

"""Observable retrieval, evidence drift, and checkpoint invariants."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("memory_context", SCRIPT)
memory_context = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(memory_context)
sys.path.pop(0)


class MemoryContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / "project"
        self.root = self.project / "docs"
        (self.project / ".git").mkdir(parents=True)
        (self.root / "wiki/decisions").mkdir(parents=True)
        (self.root / "logs").mkdir()
        (self.root / "index.md").write_text("# Memory\n", encoding="utf-8")
        (self.project / "src").mkdir()
        self.code = self.project / "src/refund.py"
        self.code.write_text("WINDOW = 30\n", encoding="utf-8")
        self.page("decision.refund", sources=["src/refund.py"], body=(
            "# Refund window\n\n## Decision\nRefunds use a 30 day window.\n\n"
            "## Alternatives Considered\nA 90 day window was rejected.\n\n"
            "## Outcome And Revisit\nReview when regional requirements change.\n"))

    def page(self, key, sources=(), related=(), body="# Page\n", **fields):
        path = self.root / "wiki/decisions" / (key + ".md")
        metadata = {"id": key, "updated": "2026-09-23", "sources": list(sources),
                    "related": list(related), **fields}
        lines = ["---"]
        for field, value in metadata.items():
            lines.append(field + ": " + (json.dumps(value) if isinstance(value, list) else str(value)))
        path.write_text("\n".join(lines) + "\n---\n\n" + body, encoding="utf-8")
        return path

    def memory(self):
        return memory_context.Memory(self.root)

    def statuses(self):
        return {x["id"]: x for x in memory_context.review(self.memory())["pages"]}

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_sources_relations_and_markdown_links_are_explicit(self):
        self.page("area.payments", sources=["wiki/decisions/decision.refund.md"],
                  related=["decision.refund"], body=(
                      '# Payments\n[Refund](decision.refund.md "Policy")\n'
                      '[Reference][refund]\n[refund]: decision.refund.md\n'
                      '`[Example](fake.md)`\n```md\n[Example](fake2.md)\n```\n'))
        graph = memory_context.graph(self.memory())
        relations = {e["relation"] for e in graph["edges"] if e["from"] == "area.payments"}
        self.assertEqual(relations, {"sources", "related", "links"})
        self.assertTrue(all(e["origin"] == "explicit" for e in graph["edges"]))
        self.assertFalse(any("fake" in n["id"] for n in graph["nodes"]))

    def test_queries_do_not_create_or_advance_a_baseline(self):
        before = self.files()
        memory_context.graph(self.memory())
        memory_context.brief(self.memory(), query="refund")
        self.assertEqual(self.statuses()["decision.refund"]["review_status"], "no_checkpoint")
        self.assertEqual(self.files(), before)
        memory_context.checkpoint(self.memory(), ["decision.refund"])
        before = self.files()
        self.code.write_text("WINDOW = 14\n", encoding="utf-8")
        self.assertEqual(self.statuses()["decision.refund"]["review_status"], "candidate")
        memory_context.brief(self.memory(), query="refund")
        self.assertEqual(self.files(), before)

    def test_content_change_not_mtime_and_does_not_invalidate_decision(self):
        memory_context.checkpoint(self.memory(), ["decision.refund"])
        self.code.touch()
        self.assertEqual(self.statuses()["decision.refund"]["review_status"], "unchanged")
        self.code.write_text("WINDOW = 14\n", encoding="utf-8")
        row = self.statuses()["decision.refund"]
        self.assertEqual(row["review_status"], "candidate")
        self.assertEqual(row["page_status"], "active")
        self.assertIn("source_changed", [x["code"] for x in row["reasons"]])

    def test_transitive_evidence_and_cycles(self):
        self.page("area.payments", sources=["wiki/decisions/decision.refund.md"], depends_on=["area.payments"])
        memory_context.checkpoint(self.memory(), ["area.payments"])
        self.code.write_text("WINDOW = 14\n", encoding="utf-8")
        self.assertEqual(self.statuses()["area.payments"]["review_status"], "candidate")
        documents, _ = memory_context.select(self.memory(), sources=["src/refund.py"])
        self.assertEqual(set(documents), {"area.payments", "decision.refund"})

    def test_missing_source_is_visible_and_cannot_be_checkpointed(self):
        memory_context.checkpoint(self.memory(), ["decision.refund"])
        original = (self.root / memory_context.STATE_FILE).read_bytes()
        self.code.unlink()
        self.assertEqual(self.statuses()["decision.refund"]["review_status"], "candidate")
        with self.assertRaises(ValueError):
            memory_context.checkpoint(self.memory(), ["decision.refund"])
        self.assertEqual((self.root / memory_context.STATE_FILE).read_bytes(), original)

    def test_external_revision_change_and_unchecked_remote_content(self):
        self.page("decision.remote", sources=["https://example.com/blob/aaa/file.py"])
        memory_context.checkpoint(self.memory(), ["decision.remote"])
        row = self.statuses()["decision.remote"]
        self.assertEqual(row["review_status"], "unchanged")
        self.assertEqual(len(row["external_unchecked"]), 1)
        self.page("decision.remote", sources=["https://example.com/blob/bbb/file.py"])
        self.assertIn("evidence_set_changed", [r["code"] for r in self.statuses()["decision.remote"]["reasons"]])

    def test_scoped_checkpoint_does_not_clear_other_candidates(self):
        self.page("decision.other", sources=["src/refund.py"])
        memory_context.checkpoint(self.memory(), ["decision.refund", "decision.other"])
        self.code.write_text("WINDOW = 14\n", encoding="utf-8")
        memory_context.checkpoint(self.memory(), ["decision.refund"])
        rows = self.statuses()
        self.assertEqual(rows["decision.refund"]["review_status"], "unchanged")
        self.assertEqual(rows["decision.other"]["review_status"], "candidate")

    def test_failed_atomic_save_preserves_previous_state_and_releases_lock(self):
        memory_context.checkpoint(self.memory(), ["decision.refund"])
        before = self.files()
        with patch.object(memory_context.os, "replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                memory_context.checkpoint(self.memory(), ["decision.refund"])
        self.assertEqual(self.files(), before)

    def test_existing_lock_and_malformed_state_are_not_silently_overwritten(self):
        memory_context.checkpoint(self.memory(), ["decision.refund"])
        path = self.root / memory_context.STATE_FILE
        lock = path.with_suffix(".lock")
        lock.write_text("another writer", encoding="utf-8")
        with self.assertRaises(ValueError):
            memory_context.checkpoint(self.memory(), ["decision.refund"])
        self.assertTrue(lock.exists())
        lock.unlink()
        path.write_text('{"schema_version":999,"pages":{}}', encoding="utf-8")
        before = self.files()
        with self.assertRaises(ValueError):
            memory_context.checkpoint(self.memory(), ["decision.refund"])
        self.assertEqual(before, self.files())

    def test_unknown_ids_and_escaping_sources_are_reported(self):
        outside = self.project.parent / "secret.txt"
        outside.write_text("not project evidence", encoding="utf-8")
        (self.project / "src/escape.txt").symlink_to(outside)
        self.page("decision.bad", sources=["src/escape.txt"], related=["decision.unknown"])
        memory = self.memory()
        self.assertTrue(memory.warnings)
        self.assertFalse(any(n.get("sha256") == memory_context.digest_file(outside) for n in memory.nodes.values()))
        with self.assertRaises(ValueError):
            memory_context.checkpoint(memory, ["decision.bad"])
        with self.assertRaises(ValueError):
            memory_context.brief(memory, pages=["decision.unknown"])

    def test_duplicate_identity_fails_instead_of_overwriting(self):
        p = self.root / "wiki/duplicate.md"
        p.write_bytes((self.root / "wiki/decisions/decision.refund.md").read_bytes())
        with self.assertRaises(ValueError):
            self.memory()

    def test_brief_retrieves_outcomes_and_keeps_history_explicit_with_budget(self):
        self.page("decision.old", sources=["src/refund.py"], status="superseded",
                  superseded_by=["decision.refund"], body="# Refund history\n\nOld window failed regionally.\n")
        (self.root / "logs/2026-09.md").write_text("# Event\n\nRefund trial failed.\n", encoding="utf-8")
        result = memory_context.brief(self.memory(), query="refund", budget=2200)
        self.assertLessEqual(result["characters"], 2200)
        self.assertIn("superseded", result["text"])
        self.assertIn("historical", result["text"])
        self.assertIn("regional requirements", result["text"])
        self.assertTrue(any(e["relation"] == "superseded_by" for e in result["relations"]))

    def test_non_english_query_and_search_miss(self):
        self.page("decision.korean", body="# 환불 정책\n\n지역별 제약을 확인한다.\n")
        result = memory_context.brief(self.memory(), query="환불")
        self.assertEqual(result["included"], ["decision.korean"])
        miss = memory_context.brief(self.memory(), query="utterlynonexistent")
        self.assertEqual(miss["included"], [])
        self.assertIn("broaden", miss["text"])

    def test_mermaid_marks_review_candidates_and_escapes_labels(self):
        self.page("decision.refund", sources=["src/refund.py"], body='# A "quote" <script>\n')
        memory_context.checkpoint(self.memory(), ["decision.refund"])
        self.code.write_text("WINDOW = 14\n", encoding="utf-8")
        diagram = memory_context.mermaid(memory_context.graph(self.memory()))
        self.assertIn(":::review", diagram)
        self.assertIn("&quot;quote&quot;", diagram)
        self.assertNotIn("<script>", diagram)

    def test_cli_works_from_an_unrelated_directory_and_query_is_read_only(self):
        before = self.files()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root), "brief", "--source", "src/refund.py", "--format", "json"],
                                cwd=self.tmp.name, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["included"], ["decision.refund"])
        self.assertEqual(before, self.files())

    def test_bounded_graph_retains_requested_source_and_discloses_unknown_freshness(self):
        result = memory_context.graph(self.memory(), sources=["src/refund.py"], limit=1)
        self.assertEqual(result["nodes"][0]["id"], "file:src/refund.py")
        self.assertGreater(result["omitted_nodes"], 0)
        full = memory_context.graph(self.memory())
        self.assertIn("no_checkpoint", memory_context.mermaid(full))

    def test_shipped_plugin_works_without_repository_scripts(self):
        package = SCRIPT.parents[3]
        installed = Path(self.tmp.name) / "installed-projipsa"
        shutil.copytree(package, installed, ignore=shutil.ignore_patterns("__pycache__"))
        script = installed / SCRIPT.relative_to(package)
        result = subprocess.run([sys.executable, str(script), str(self.root), "graph", "--format", "json"],
                                cwd=self.tmp.name, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sources", {e["relation"] for e in json.loads(result.stdout)["edges"]})


if __name__ == "__main__":
    unittest.main()

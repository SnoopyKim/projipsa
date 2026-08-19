from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "projipsa"
    / "codex-skills"
    / "compact"
    / "scripts"
    / "audit_compaction.py"
)
SPEC = importlib.util.spec_from_file_location("audit_compaction", SCRIPT)
assert SPEC and SPEC.loader
audit_compaction = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_compaction)


class CompactAuditTests(unittest.TestCase):
    def make_memory(self, parent: Path) -> Path:
        root = parent / "docs"
        raw = root / "raw" / "2026-08"
        wiki = root / "wiki"
        raw.mkdir(parents=True)
        wiki.mkdir()

        (raw / "keep.png").write_bytes(b"same")
        (raw / "duplicate.png").write_bytes(b"same")
        (raw / "appointment-comparison-board.png").write_bytes(b"board")
        (raw / "appointment-component-crop.png").write_bytes(b"crop")
        (raw / "source-only.png").write_bytes(b"source")
        (wiki / "current.md").write_text(
            "---\nsources:\n  - raw/2026-08/source-only.png\n---\n\n"
            "![current](<../raw/2026-08/keep.png>)\n",
            encoding="utf-8",
        )
        return root

    def test_reports_exact_duplicates_and_reclaimable_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_memory(Path(temporary))
            report = audit_compaction.audit_memory(root)

        self.assertEqual(1, report["summary"]["exact_duplicate_group_count"])
        self.assertEqual(4, report["summary"]["exact_duplicate_reclaimable_bytes"])
        self.assertEqual(5, report["summary"]["raw_image_file_count"])
        self.assertEqual(23, report["summary"]["raw_image_bytes"])
        largest_image = next(
            item for item in report["largest_files"] if item["kind"] == "image"
        )
        self.assertEqual("raw/2026-08/source-only.png", largest_image["path"])
        self.assertEqual(
            [
                "raw/2026-08/duplicate.png",
                "raw/2026-08/keep.png",
            ],
            report["exact_duplicates"][0]["paths"],
        )

    def test_distinguishes_references_from_review_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_memory(Path(temporary))
            report = audit_compaction.audit_memory(root)

        self.assertEqual(2, report["summary"]["referenced_image_count"])
        candidates = {
            candidate["path"] for candidate in report["unreferenced_images"]
        }
        self.assertNotIn("raw/2026-08/keep.png", candidates)
        self.assertNotIn("raw/2026-08/source-only.png", candidates)
        self.assertIn("raw/2026-08/duplicate.png", candidates)

    def test_semantic_groups_are_not_reported_as_exact_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_memory(Path(temporary))
            report = audit_compaction.audit_memory(root)

        semantic_paths = {
            tuple(group["paths"]) for group in report["semantic_review_groups"]
        }
        self.assertIn(
            (
                "raw/2026-08/appointment-comparison-board.png",
                "raw/2026-08/appointment-component-crop.png",
            ),
            semantic_paths,
        )
        duplicate_paths = {
            path
            for group in report["exact_duplicates"]
            for path in group["paths"]
        }
        self.assertNotIn(
            "raw/2026-08/appointment-comparison-board.png", duplicate_paths
        )

    def test_audit_is_idempotent_and_does_not_modify_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_memory(Path(temporary))
            before = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            first = audit_compaction.audit_memory(root)
            second = audit_compaction.audit_memory(root)
            after = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }

        self.assertEqual(first, second)
        self.assertEqual(before, after)

    def test_semantic_normalization_keeps_unicode_subjects(self) -> None:
        normalized = audit_compaction.normalized_stem(
            Path("예약-비교-보드-스크린샷.png")
        )
        self.assertEqual("예약", normalized)

    def test_reports_git_baseline_and_tracking_per_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "repository"
            raw = repository / "docs" / "raw"
            raw.mkdir(parents=True)
            (raw / "tracked.png").write_bytes(b"tracked")
            (raw / "clean.png").write_bytes(b"clean")
            subprocess.run(["git", "init", "-q", str(repository)], check=True)
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.email", "test@example.com"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "add",
                    "docs/raw/tracked.png",
                    "docs/raw/clean.png",
                ],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "commit", "-qm", "fixture"],
                check=True,
            )
            (raw / "tracked.png").write_bytes(b"modified")
            (raw / "untracked.png").write_bytes(b"untracked")
            report = audit_compaction.audit_memory(repository / "docs")

        candidates = {
            candidate["path"]: candidate["tracked"]
            for candidate in report["unreferenced_images"]
        }
        self.assertIsNotNone(report["git"]["baseline"])
        self.assertTrue(candidates["raw/tracked.png"])
        self.assertFalse(candidates["raw/untracked.png"])
        recovery = {
            candidate["path"]: candidate["recoverability"]
            for candidate in report["unreferenced_images"]
        }
        self.assertEqual("baseline", recovery["raw/clean.png"])
        self.assertEqual(
            "current-content-not-at-baseline", recovery["raw/tracked.png"]
        )
        self.assertEqual("untracked", recovery["raw/untracked.png"])


if __name__ == "__main__":
    unittest.main()

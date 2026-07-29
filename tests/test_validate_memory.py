from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "projipsa"
    / "scripts"
    / "validate_memory.py"
)
SPEC = importlib.util.spec_from_file_location("validate_memory", SCRIPT)
assert SPEC and SPEC.loader
validate_memory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_memory)


def page(
    page_id: str,
    title: str,
    page_type: str = "project",
    *,
    status: str = "active",
    confidence: str = "confirmed",
    sources: tuple[str, ...] = ("README.md",),
) -> str:
    source_lines = (
        "sources: []"
        if not sources
        else "sources:\n" + "\n".join(f"  - {source}" for source in sources)
    )
    return f"""---
id: {page_id}
type: {page_type}
status: {status}
confidence: {confidence}
updated: 2026-07-28
{source_lines}
related: []
---

# {title}
"""


class ValidateMemoryTests(unittest.TestCase):
    def make_valid_tree(self, root: Path) -> Path:
        docs = root / "docs"
        (docs / "wiki" / "project").mkdir(parents=True)
        (docs / "wiki" / "questions").mkdir(parents=True)
        (docs / "wiki" / "decisions").mkdir(parents=True)
        (docs / "logs").mkdir(parents=True)
        (docs / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
        (docs / "README.md").write_text("# Evidence\n", encoding="utf-8")
        (docs / "index.md").write_text(
            "\n".join(
                (
                    "# Project Memory",
                    "",
                    "- [Overview](wiki/project/overview.md)",
                    "- [Current state](wiki/project/current-state.md)",
                    "- [Adoption decision](wiki/decisions/2026-07-28-projipsa-adoption.md)",
                    "- [Questions](wiki/questions/open-questions.md)",
                    "- [Project log](logs/2026-07.md)",
                )
            ),
            encoding="utf-8",
        )
        (docs / "wiki" / "project" / "overview.md").write_text(
            page("project.overview", "Overview"),
            encoding="utf-8",
        )
        (docs / "wiki" / "project" / "current-state.md").write_text(
            page("project.current-state", "Current State"),
            encoding="utf-8",
        )
        (docs / "wiki" / "questions" / "open-questions.md").write_text(
            page(
                "question.open",
                "Open Questions",
                "question",
                confidence="assumed",
                sources=(),
            ),
            encoding="utf-8",
        )
        (
            docs
            / "wiki"
            / "decisions"
            / "2026-07-28-projipsa-adoption.md"
        ).write_text(
            page(
                "decision.projipsa-adoption.2026-07-28",
                "Adopt Projipsa",
                "decision",
            ),
            encoding="utf-8",
        )
        (docs / "logs" / "2026-07.md").write_text(
            "# 2026-07 Project Log\n\n## 2026-07-28\n\n- Adopted Projipsa.\n",
            encoding="utf-8",
        )
        return docs

    def test_valid_tree_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            self.assertEqual([], validate_memory.validate(docs))

    def test_duplicate_id_and_broken_link_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            question = docs / "wiki" / "questions" / "open-questions.md"
            question.write_text(
                page("project.current-state", "Open Questions"),
                encoding="utf-8",
            )
            with (docs / "index.md").open("a", encoding="utf-8") as handle:
                handle.write("\n- [Missing](wiki/missing.md)\n")

            errors = validate_memory.validate(docs)
            self.assertTrue(any("duplicate page id" in error for error in errors))
            self.assertTrue(any("broken link target" in error for error in errors))

    def test_delivery_page_is_valid_maintained_memory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            deliveries = docs / "wiki" / "deliveries"
            deliveries.mkdir()
            delivery = deliveries / "projipsa-v02.md"
            delivery.write_text(
                page(
                    "delivery.projipsa-v02",
                    "Projipsa v0.2",
                    "delivery",
                    status="draft",
                    confidence="assumed",
                    sources=(),
                ),
                encoding="utf-8",
            )
            with (docs / "index.md").open("a", encoding="utf-8") as handle:
                handle.write("\n- [Active delivery](wiki/deliveries/projipsa-v02.md)\n")

            self.assertEqual([], validate_memory.validate(docs))

    def test_missing_decision_and_monthly_log_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            (
                docs
                / "wiki"
                / "decisions"
                / "2026-07-28-projipsa-adoption.md"
            ).unlink()
            (docs / "logs" / "2026-07.md").unlink()

            errors = validate_memory.validate(docs)
            self.assertTrue(
                any("missing required decision page" in error for error in errors)
            )
            self.assertTrue(
                any("missing required monthly log" in error for error in errors)
            )

    def test_confirmed_page_requires_a_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            overview = docs / "wiki" / "project" / "overview.md"
            overview.write_text(
                page(
                    "project.overview",
                    "Overview",
                    confidence="confirmed",
                    sources=(),
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(
                any(
                    "confirmed pages require at least one source" in error
                    for error in errors
                )
            )

    def test_required_scalar_and_index_navigation_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            current_state = docs / "wiki" / "project" / "current-state.md"
            current_state.write_text(
                page("project.current-state", "Current State").replace(
                    "type: project",
                    "type:",
                ),
                encoding="utf-8",
            )
            index = docs / "index.md"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "- [Project log](logs/2026-07.md)",
                    "",
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(
                any("type must be a non-empty scalar value" in error for error in errors)
            )
            self.assertTrue(
                any("index.md must link at least one monthly log" in error for error in errors)
            )

    def test_missing_source_target_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            overview = docs / "wiki" / "project" / "overview.md"
            overview.write_text(
                page(
                    "project.overview",
                    "Overview",
                    sources=("missing-evidence.md",),
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(
                any("source target not found" in error for error in errors)
            )

    def test_source_must_be_a_project_file_or_http_url(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            overview = docs / "wiki" / "project" / "overview.md"
            overview.write_text(
                page(
                    "project.overview",
                    "Overview",
                    sources=(".", str(Path(__file__).resolve())),
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            source_errors = [
                error for error in errors if "source target not found" in error
            ]
            self.assertEqual(2, len(source_errors))

    def test_http_source_requires_a_host(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            overview = docs / "wiki" / "project" / "overview.md"
            overview.write_text(
                page(
                    "project.overview",
                    "Overview",
                    sources=("https://",),
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(
                any("source target not found" in error for error in errors)
            )

    def test_confirmed_page_cannot_cite_itself(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            overview = docs / "wiki" / "project" / "overview.md"
            overview.write_text(
                page(
                    "project.overview",
                    "Overview",
                    sources=("wiki/project/overview.md",),
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(any("cannot cite itself" in error for error in errors))
            self.assertTrue(
                any("do not reach primary project evidence" in error for error in errors)
            )

    def test_confirmed_source_cycle_requires_primary_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            overview = docs / "wiki" / "project" / "overview.md"
            current = docs / "wiki" / "project" / "current-state.md"
            overview.write_text(
                page(
                    "project.overview",
                    "Overview",
                    sources=("wiki/project/current-state.md",),
                ),
                encoding="utf-8",
            )
            current.write_text(
                page(
                    "project.current-state",
                    "Current State",
                    sources=("wiki/project/overview.md",),
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            cycle_errors = [
                error
                for error in errors
                if "do not reach primary project evidence" in error
            ]
            self.assertEqual(2, len(cycle_errors))

    def test_source_cycle_with_primary_evidence_is_anchored(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            overview = docs / "wiki" / "project" / "overview.md"
            current = docs / "wiki" / "project" / "current-state.md"
            overview.write_text(
                page(
                    "project.overview",
                    "Overview",
                    sources=("wiki/project/current-state.md",),
                ),
                encoding="utf-8",
            )
            current.write_text(
                page(
                    "project.current-state",
                    "Current State",
                    sources=("wiki/project/overview.md", "README.md"),
                ),
                encoding="utf-8",
            )

            self.assertEqual([], validate_memory.validate(docs))

    def test_duplicate_standard_adoption_decisions_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            duplicate = (
                docs
                / "wiki"
                / "decisions"
                / "2026-07-29-projipsa-adoption.md"
            )
            duplicate.write_text(
                page(
                    "decision.projipsa-adoption.2026-07-29",
                    "Adopt Projipsa Again",
                    "decision",
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(
                any("initialization must be idempotent" in error for error in errors)
            )

    def test_unrelated_decision_does_not_replace_adoption_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            adoption = (
                docs
                / "wiki"
                / "decisions"
                / "2026-07-28-projipsa-adoption.md"
            )
            adoption.unlink()
            unrelated = docs / "wiki" / "decisions" / "2026-07-28-color.md"
            unrelated.write_text(
                page(
                    "decision.color.2026-07-28",
                    "Choose Color",
                    "decision",
                ),
                encoding="utf-8",
            )
            index = docs / "index.md"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "wiki/decisions/2026-07-28-projipsa-adoption.md",
                    "wiki/decisions/2026-07-28-color.md",
                ),
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(
                any("missing Projipsa adoption decision" in error for error in errors)
            )

    def test_marked_equivalent_adoption_decision_keeps_stable_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            adoption = (
                docs
                / "wiki"
                / "decisions"
                / "2026-07-28-projipsa-adoption.md"
            )
            adoption.unlink()
            equivalent = docs / "wiki" / "decisions" / "memory-system.md"
            equivalent.write_text(
                page(
                    "decision.memory-system.2026-07-28",
                    "Adopt Project Memory",
                    "decision",
                ).replace(
                    "related: []",
                    "related: []\nprojipsa_adoption: true",
                ),
                encoding="utf-8",
            )
            index = docs / "index.md"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "wiki/decisions/2026-07-28-projipsa-adoption.md",
                    "wiki/decisions/memory-system.md",
                ),
                encoding="utf-8",
            )

            self.assertEqual([], validate_memory.validate(docs))


if __name__ == "__main__":
    unittest.main()

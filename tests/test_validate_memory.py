from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "projipsa"
    / "codex-skills"
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
        (root / "AGENTS.md").write_text(
            "# Project Instructions\n\n"
            f"{validate_memory.POINTER_OPEN}\n"
            "Memory root: `docs/`. Read `docs/index.md` first.\n"
            f"{validate_memory.POINTER_CLOSE}\n",
            encoding="utf-8",
        )
        (root / "CLAUDE.md").write_text(
            "# Project Instructions\n\n@AGENTS.md\n", encoding="utf-8"
        )
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

    def test_missing_adoption_decision_and_chronology_log_fail(self) -> None:
        """Decision pages in general are no longer required, but the adoption
        decision is: it is how a re-run of initialization knows it already ran."""
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
                any("missing Projipsa adoption decision" in error for error in errors)
            )
            self.assertTrue(
                any("missing required chronology log" in error for error in errors)
            )

    def test_a_minimal_tree_needs_only_what_a_reader_needs(self) -> None:
        """Stated rules, an entry point, a briefing, and an identity plus a date
        and evidence per page. Overview, open questions, a general decision page,
        `type`, `status`, `confidence`, and `related` are all optional, and the
        adoption decision is recognized from its directory without `type`."""
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            (docs / "wiki" / "project" / "overview.md").unlink()
            (docs / "wiki" / "questions" / "open-questions.md").unlink()
            (
                docs / "wiki" / "decisions" / "2026-07-28-projipsa-adoption.md"
            ).write_text(
                "---\n"
                "id: decision.projipsa-adoption.2026-07-28\n"
                "updated: 2026-07-28\n"
                "sources:\n"
                "  - README.md\n"
                "---\n"
                "\n"
                "# Adopt Projipsa\n",
                encoding="utf-8",
            )
            (docs / "index.md").write_text(
                "# Project Memory\n"
                "\n"
                "- [Current state](wiki/project/current-state.md)\n"
                "- [Project log](logs/2026-07.md)\n",
                encoding="utf-8",
            )

            self.assertEqual([], validate_memory.validate(docs))

    def test_session_granular_chronology_is_accepted(self) -> None:
        """One file per writer is how parallel branches stop colliding, so a
        day- and slug-qualified log in a subdirectory must be first-class."""
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            (docs / "logs" / "2026-07.md").unlink()
            session_logs = docs / "logs" / "2026-07"
            session_logs.mkdir()
            (session_logs / "2026-07-28-adapter-split.md").write_text(
                "# Adapter split\n\n- updated: wiki/project/current-state.md\n",
                encoding="utf-8",
            )
            index = docs / "index.md"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "- [Project log](logs/2026-07.md)",
                    "- [Project log](logs/2026-07/2026-07-28-adapter-split.md)",
                ),
                encoding="utf-8",
            )

            self.assertEqual([], validate_memory.validate(docs))

    def test_index_may_link_the_chronology_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            index = docs / "index.md"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "- [Project log](logs/2026-07.md)",
                    "- [Chronology](logs/)",
                ),
                encoding="utf-8",
            )

            self.assertEqual([], validate_memory.validate(docs))

    def test_nested_chronology_is_content_checked(self) -> None:
        """A non-recursive walk used to make nested logs invisible, which
        exempted them from link and placeholder checking entirely."""
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            session_logs = docs / "logs" / "2026-07"
            session_logs.mkdir()
            (session_logs / "2026-07-28-adapter-split.md").write_text(
                "# Adapter split\n\n- [Missing](../../wiki/missing.md)\n"
                "- updated: [TODO: fill in]\n",
                encoding="utf-8",
            )

            errors = validate_memory.validate(docs)
            self.assertTrue(any("broken link target" in error for error in errors))
            self.assertTrue(
                any("unresolved template placeholder" in error for error in errors)
            )

    def bloat_current_state(self, docs: Path, sections: bool) -> None:
        current_state = docs / "wiki" / "project" / "current-state.md"
        body = (
            "".join(
                f"\n## {section}\n\n- Nothing yet.\n"
                for section in validate_memory.CURRENT_STATE_SECTIONS
            )
            if sections
            else ""
        )
        history = "\n- Completed an earlier delivery." * 500
        current_state.write_text(
            current_state.read_text(encoding="utf-8") + body + history,
            encoding="utf-8",
        )

    def test_oversized_current_state_warns_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            self.bloat_current_state(docs, sections=True)

            self.assertEqual([], validate_memory.validate(docs))
            warnings = validate_memory.collect_warnings(docs)
            self.assertEqual(1, len(warnings), warnings)
            self.assertIn("every session reads", warnings[0])

    def test_long_current_state_missing_its_sections_warns_twice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            self.bloat_current_state(docs, sections=False)

            warnings = validate_memory.collect_warnings(docs)
            self.assertEqual(2, len(warnings), warnings)
            self.assertIn("Explicitly Not Current", warnings[1])

    def test_short_current_state_may_name_its_own_sections(self) -> None:
        """A page within budget is not nagged for using its own headings."""
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))

            self.assertEqual([], validate_memory.collect_warnings(docs))

    def add_writer_log(self, docs: Path, name: str) -> None:
        """A per-writer chronology file whose date lives only in its name."""
        session_logs = docs / "logs" / "2026-08"
        session_logs.mkdir(exist_ok=True)
        (session_logs / name).write_text(
            "# Adapter split\n\n- changed: the host adapter\n", encoding="utf-8"
        )

    def test_chronology_after_current_state_warns_integration_outstanding(
        self,
    ) -> None:
        """A merged writer's log is dated later than the shared page that should
        have absorbed it, which is exactly the post-merge condition."""
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            self.add_writer_log(docs, "2026-08-03-adapter-split.md")

            self.assertEqual([], validate_memory.validate(docs))
            warnings = validate_memory.collect_warnings(docs)
            self.assertEqual(1, len(warnings), warnings)
            self.assertIn("Integrate", warnings[0])
            self.assertIn("2026-08-03", warnings[0])

    def test_integration_warning_clears_when_current_state_catches_up(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            self.add_writer_log(docs, "2026-08-03-adapter-split.md")
            current_state = docs / "wiki" / "project" / "current-state.md"
            current_state.write_text(
                current_state.read_text(encoding="utf-8").replace(
                    "updated: 2026-07-28", "updated: 2026-08-03"
                ),
                encoding="utf-8",
            )

            self.assertEqual([], validate_memory.collect_warnings(docs))

    def test_the_command_prints_warnings_and_still_succeeds(self) -> None:
        """The contract that makes a warning a warning: it reaches the operator
        on stderr, and it leaves the exit code alone."""
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            self.add_writer_log(docs, "2026-08-03-adapter-split.md")

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(
                io.StringIO()
            ), unittest.mock.patch.object(sys, "argv", ["validate_memory", str(docs)]):
                exit_code = validate_memory.main()

            self.assertEqual(0, exit_code)
            self.assertIn("warning: ", stderr.getvalue())
            self.assertNotIn("error: ", stderr.getvalue())

    def test_a_dated_entry_in_a_monthly_log_drives_the_comparison(self) -> None:
        """A monthly filename names no day, so the entry heading is the signal
        that keeps this check working for a single-writer project."""
        with tempfile.TemporaryDirectory() as temporary:
            docs = self.make_valid_tree(Path(temporary))
            log = docs / "logs" / "2026-07.md"
            log.write_text(
                log.read_text(encoding="utf-8")
                + "\n## [2026-07-30] update | Later work\n\n- changed: a page.\n",
                encoding="utf-8",
            )

            warnings = validate_memory.collect_warnings(docs)
            self.assertEqual(1, len(warnings), warnings)
            self.assertIn("2026-07-30", warnings[0])

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
                any("index.md must link the chronology" in error for error in errors)
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
            # Self-evidence is a defect the script can settle; whether the claim
            # itself holds is not, so the chain is reported rather than failed.
            self.assertTrue(
                any(
                    "do not reach primary project evidence" in warning
                    for warning in validate_memory.collect_warnings(docs)
                )
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

            self.assertEqual([], validate_memory.validate(docs))
            cycle_warnings = [
                warning
                for warning in validate_memory.collect_warnings(docs)
                if "do not reach primary project evidence" in warning
            ]
            self.assertEqual(2, len(cycle_warnings))

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

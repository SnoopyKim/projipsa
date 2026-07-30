"""Behavioural cover for the memory contract.

The package validator can only check that words appear in a contract. This
builds the minimum useful core exactly as `projipsa-init` describes it, from the
shipped templates, and requires the shipped validator to accept it. A template
that cannot pass its own validator fails here.
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "projipsa" / "scripts" / "validate_memory.py"
TEMPLATES = ROOT / "skills" / "projipsa" / "assets" / "templates"
SPEC = importlib.util.spec_from_file_location("validate_memory", SCRIPT)
assert SPEC and SPEC.loader
validate_memory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_memory)

ADOPTION_DATE = "2026-07-30"
ADOPTION_MONTH = "2026-07"
CORE = {
    "agents.md": "AGENTS.md",
    "index.md": "index.md",
    "project-overview.md": "wiki/project/overview.md",
    "current-state.md": "wiki/project/current-state.md",
    "question.md": "wiki/questions/open-questions.md",
    "decision.md": f"wiki/decisions/{ADOPTION_DATE}-projipsa-adoption.md",
    "log.md": f"logs/{ADOPTION_MONTH}.md",
}


def fill(text: str) -> str:
    """Resolve template placeholders the way initialization is told to."""
    return text.replace("YYYY-MM-DD", ADOPTION_DATE).replace(
        "YYYY-MM", ADOPTION_MONTH
    )


def pointer_block() -> str:
    """The block exactly as root-pointer.md ships it."""
    text = (TEMPLATES / "root-pointer.md").read_text(encoding="utf-8")
    start = text.index(validate_memory.POINTER_OPEN)
    end = text.index(validate_memory.POINTER_CLOSE) + len(
        validate_memory.POINTER_CLOSE
    )
    return text[start:end]


def build_core(project: Path) -> Path:
    (project / ".git").mkdir(parents=True)
    (project / "README.md").write_text(
        "# Fixture\n\nPrimary project evidence.\n", encoding="utf-8"
    )
    (project / "AGENTS.md").write_text(
        f"# Project Instructions\n\n{pointer_block()}\n", encoding="utf-8"
    )
    (project / "CLAUDE.md").write_text(
        "# Project Instructions\n\n@AGENTS.md\n", encoding="utf-8"
    )

    root = project / "docs"
    for relative in (
        "wiki/project",
        "wiki/decisions",
        "wiki/questions",
        "logs",
        f"raw/{ADOPTION_MONTH}",
    ):
        (root / relative).mkdir(parents=True)

    for template, destination in CORE.items():
        (root / destination).write_text(
            fill((TEMPLATES / template).read_text(encoding="utf-8")),
            encoding="utf-8",
        )

    replace_in(
        root / CORE["decision.md"],
        "id: decision.slug.",
        "id: decision.projipsa-adoption.",
    )
    replace_in(
        root / CORE["question.md"],
        "id: question.slug",
        "id: question.open-questions",
    )
    return root


def replace_in(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{path} no longer contains {old!r}"
    path.write_text(text.replace(old, new), encoding="utf-8")


class MemoryFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / "project"
        self.root = build_core(self.project)

    def test_minimum_core_from_templates_is_valid(self) -> None:
        self.assertEqual([], validate_memory.validate(self.root))

    def test_confirmed_page_still_requires_a_source(self) -> None:
        replace_in(
            self.root / "wiki/project/overview.md",
            "confidence: inferred",
            "confidence: confirmed",
        )
        errors = validate_memory.validate(self.root)
        self.assertTrue(
            any("require at least one source" in error for error in errors),
            errors,
        )

    def test_documented_convention_is_not_a_placeholder(self) -> None:
        page = self.root / "wiki/project/current-state.md"
        page.write_text(
            page.read_text(encoding="utf-8")
            + "\n## Conventions\n\n"
            "- Sources live under `raw/YYYY-MM/` and logs under `logs/YYYY-MM.md`.\n"
            "\n```text\nlogs/YYYY-MM.md\n```\n",
            encoding="utf-8",
        )
        self.assertEqual([], validate_memory.validate(self.root))

    def test_unresolved_frontmatter_placeholder_still_fails(self) -> None:
        replace_in(
            self.root / "wiki/project/overview.md",
            f"updated: {ADOPTION_DATE}",
            "updated: YYYY-MM-DD",
        )
        errors = validate_memory.validate(self.root)
        self.assertTrue(
            any("unresolved template placeholder" in error for error in errors),
            errors,
        )

    def test_claude_md_may_carry_the_block_instead_of_the_import(self) -> None:
        (self.project / "CLAUDE.md").write_text(
            f"# Curated instructions\n\nKeep this line.\n\n{pointer_block()}\n",
            encoding="utf-8",
        )
        self.assertEqual([], validate_memory.validate(self.root))

    def test_missing_root_claude_md_fails(self) -> None:
        (self.project / "CLAUDE.md").unlink()
        errors = validate_memory.validate(self.root)
        self.assertTrue(
            any("Claude Code cannot discover" in error for error in errors),
            errors,
        )

    def test_root_claude_md_without_pointer_or_import_fails(self) -> None:
        (self.project / "CLAUDE.md").write_text(
            "# Curated instructions\n\nNothing about project memory.\n",
            encoding="utf-8",
        )
        errors = validate_memory.validate(self.root)
        self.assertTrue(
            any("never learns about docs/" in error for error in errors),
            errors,
        )

    def test_second_pointer_block_fails(self) -> None:
        """A repeated initialization run must repair in place, not append."""
        path = self.project / "AGENTS.md"
        path.write_text(
            path.read_text(encoding="utf-8") + f"\n{pointer_block()}\n",
            encoding="utf-8",
        )
        errors = validate_memory.validate(self.root)
        self.assertTrue(
            any("exactly one balanced" in error for error in errors),
            errors,
        )

    def test_pointer_block_must_name_the_memory_root(self) -> None:
        path = self.project / "AGENTS.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("docs/", "notes/"),
            encoding="utf-8",
        )
        errors = validate_memory.validate(self.root)
        self.assertTrue(
            any("does not name the memory root" in error for error in errors),
            errors,
        )

    def test_memory_instructions_must_not_be_empty(self) -> None:
        (self.root / "AGENTS.md").write_text("\n", encoding="utf-8")
        errors = validate_memory.validate(self.root)
        self.assertTrue(
            any("memory rules" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()

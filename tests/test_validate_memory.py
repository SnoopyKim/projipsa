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


def page(page_id: str, title: str) -> str:
    return f"""---
id: {page_id}
type: project
status: active
confidence: confirmed
updated: 2026-07-28
sources: []
related: []
---

# {title}
"""


class ValidateMemoryTests(unittest.TestCase):
    def make_valid_tree(self, root: Path) -> Path:
        docs = root / "docs"
        (docs / "wiki" / "project").mkdir(parents=True)
        (docs / "wiki" / "questions").mkdir(parents=True)
        (docs / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
        (docs / "index.md").write_text(
            "\n".join(
                (
                    "# Project Memory",
                    "",
                    "- [Overview](wiki/project/overview.md)",
                    "- [Current state](wiki/project/current-state.md)",
                    "- [Questions](wiki/questions/open-questions.md)",
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
            page("question.open", "Open Questions"),
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


if __name__ == "__main__":
    unittest.main()

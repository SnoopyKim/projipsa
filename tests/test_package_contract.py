from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_package.py"
SPEC = importlib.util.spec_from_file_location("validate_package", SCRIPT)
assert SPEC and SPEC.loader
validate_package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_package)

IGNORED = shutil.ignore_patterns("__pycache__")


@contextmanager
def package_copy() -> Iterator[Path]:
    """Yield the plugin root of a throwaway copy of the validated surface.

    The validator resolves every path from module-level constants, so a
    negative case has to redirect those constants rather than edit the real
    package. Each check below then runs against a tree that differs from the
    shipped one in exactly one way. `README.md` and `docs/` come along because
    the validator reads the README and follows its local links.
    """
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        package = root / "plugins" / "projipsa"
        package.parent.mkdir(parents=True)
        shutil.copytree(ROOT / "plugins" / "projipsa", package, ignore=IGNORED)
        shutil.copytree(ROOT / "docs", root / "docs", ignore=IGNORED)
        shutil.copy2(ROOT / "README.md", root / "README.md")
        skills = package / "skills"
        with mock.patch.multiple(
            validate_package,
            ROOT=root,
            PACKAGE_ROOT=package,
            CLAUDE_MANIFEST=package / ".claude-plugin" / "plugin.json",
            SKILL_ROOT=skills,
            TEMPLATE_ROOT=skills / "projipsa" / "assets" / "templates",
        ):
            yield package


class PackageContractTests(unittest.TestCase):
    def assertReports(self, fragment: str, errors: list[str]) -> None:
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_package_and_skill_contracts_are_aligned(self) -> None:
        self.assertEqual([], validate_package.validate())

    def test_copied_surface_is_a_faithful_baseline(self) -> None:
        # Without this, a negative case below could pass because the copy is
        # broken rather than because the check it targets fired.
        with package_copy():
            self.assertEqual([], validate_package.validate())

    def test_foreign_host_skill_metadata_is_rejected(self) -> None:
        with package_copy() as package:
            agents = package / "skills" / "projipsa" / "agents"
            agents.mkdir()
            (agents / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: true\n",
                encoding="utf-8",
            )
            errors = validate_package.validate()
        self.assertReports("another host's metadata", errors)

    def test_foreign_host_manifest_directory_is_rejected(self) -> None:
        with package_copy() as package:
            codex = package / ".codex-plugin"
            codex.mkdir()
            (codex / "plugin.json").write_text("{}\n", encoding="utf-8")
            errors = validate_package.validate()
        self.assertReports("another host's metadata", errors)

    def test_manifest_must_not_carry_another_hosts_interface(self) -> None:
        with package_copy() as package:
            errors = self.with_manifest(
                package, lambda manifest: manifest.update(
                    {"interface": {"displayName": "Projipsa"}}
                )
            )
        self.assertReports("must not carry the 'interface' field", errors)

    def test_manifest_must_declare_a_display_name(self) -> None:
        with package_copy() as package:
            errors = self.with_manifest(
                package, lambda manifest: manifest.pop("displayName")
            )
        self.assertReports("must declare 'displayName'", errors)

    def with_manifest(self, package: Path, mutate) -> list[str]:
        path = package / ".claude-plugin" / "plugin.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        mutate(manifest)
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return validate_package.validate()

    def test_description_must_not_advertise_a_dollar_invocation(self) -> None:
        with package_copy() as package:
            path = package / "skills" / "projipsa" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "Use when the user invokes /projipsa:projipsa,",
                    "Use when the user invokes $projipsa or /projipsa:projipsa,",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_package.validate()
        self.assertReports("must not advertise the $projipsa invocation", errors)

    def test_description_must_document_the_slash_invocation(self) -> None:
        with package_copy() as package:
            path = package / "skills" / "outsource" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "/projipsa:outsource", "outsource", 1
                ),
                encoding="utf-8",
            )
            errors = validate_package.validate()
        self.assertReports(
            "must document the /projipsa:outsource invocation", errors
        )

    def test_explicit_only_skill_must_keep_its_frontmatter_gate(self) -> None:
        with package_copy() as package:
            path = package / "skills" / "projipsa-init" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "disable-model-invocation: true\n", "", 1
                ),
                encoding="utf-8",
            )
            errors = validate_package.validate()
        self.assertReports("disable-model-invocation must be true", errors)


if __name__ == "__main__":
    unittest.main()

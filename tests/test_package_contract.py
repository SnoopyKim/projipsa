from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_package.py"
SPEC = importlib.util.spec_from_file_location("validate_package", SCRIPT)
assert SPEC and SPEC.loader
validate_package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_package)


class PackageContractTests(unittest.TestCase):
    def test_package_and_skill_contracts_are_aligned(self) -> None:
        self.assertEqual([], validate_package.validate())

    def test_codex_plugin_invocations_are_namespace_qualified(self) -> None:
        for skill in ("projipsa", "projipsa-init", "outsource"):
            with self.subTest(skill=skill):
                self.assertEqual(
                    f"$projipsa:{skill}",
                    validate_package.codex_invocation(skill),
                )

    def test_hosts_declare_distinct_skill_roots_and_avoid_the_default_one(
        self,
    ) -> None:
        """Claude Code adds its declared Skill directory to the default
        skills/ scan. Sharing that name with Codex exposed all three public
        Skills twice, so each host now names its own directory."""
        codex = validate_package.load_json(validate_package.CODEX_MANIFEST)
        claude = validate_package.load_json(validate_package.CLAUDE_MANIFEST)
        self.assertNotEqual(codex["skills"], claude["skills"])
        for host, manifest in (("Codex", codex), ("Claude", claude)):
            with self.subTest(host=host):
                self.assertNotEqual("./skills/", manifest["skills"])

    def test_a_default_skill_directory_fails_validation(self) -> None:
        self.assertFalse(validate_package.DEFAULT_SKILL_ROOT.exists())
        # Any shipped directory stands in for a reintroduced skills/: the
        # check is that the path exists at all.
        with mock.patch.object(
            validate_package,
            "DEFAULT_SKILL_ROOT",
            validate_package.SHARED_WORKFLOW_ROOT,
        ):
            errors: list[str] = []
            validate_package.validate_skill_surface(errors)
        self.assertTrue(
            any("must not exist" in error for error in errors),
            errors,
        )

    def test_unqualified_codex_name_does_not_match_plugin_invocation(self) -> None:
        invocation = validate_package.codex_invocation("projipsa-init")
        self.assertFalse(
            validate_package.mentions_invocation("Use $projipsa-init", invocation)
        )
        self.assertTrue(
            validate_package.mentions_invocation(
                "Use $projipsa:projipsa-init", invocation
            )
        )


if __name__ == "__main__":
    unittest.main()

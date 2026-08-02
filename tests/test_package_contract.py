from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


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

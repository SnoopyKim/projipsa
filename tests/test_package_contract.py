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


if __name__ == "__main__":
    unittest.main()

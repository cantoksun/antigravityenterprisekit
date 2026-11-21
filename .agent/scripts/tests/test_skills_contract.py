# agkit: allow-secret allow-pattern
from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from component_registry import load_frontmatter


class SkillsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills_dir = TOOLKIT / "skills"
        cls.skill_files = sorted(cls.skills_dir.glob("*/SKILL.md"))
        cls.python_scripts = sorted(cls.skills_dir.glob("*/scripts/*.py"))

    def test_total_skills_count_is_exact(self):
        self.assertEqual(97, len(self.skill_files), "Expected exactly 97 enterprise skills")

    def test_all_skills_have_valid_frontmatter(self):
        for path in self.skill_files:
            data = load_frontmatter(path)
            skill_folder = path.parent.name
            self.assertIn("name", data, f"Missing 'name' in {path}")
            self.assertTrue(
                "description" in data or "when_to_use" in data,
                f"Missing description or when_to_use in {path}",
            )
            # allowed-tools or tools
            has_tools = "allowed-tools" in data or "tools" in data
            self.assertTrue(has_tools, f"Missing allowed-tools in {path}")

    def test_all_skill_python_scripts_have_valid_syntax(self):
        for script in self.python_scripts:
            try:
                content = script.read_text("utf-8", errors="replace")
                ast.parse(content, filename=str(script))
            except SyntaxError as e:
                self.fail(f"Python syntax error in {script.relative_to(TOOLKIT)}: {e}")

    def test_total_skill_scripts_count_matches_architecture(self):
        self.assertEqual(19, len(self.python_scripts), "Expected exactly 19 skill python scripts")


if __name__ == "__main__":
    unittest.main()

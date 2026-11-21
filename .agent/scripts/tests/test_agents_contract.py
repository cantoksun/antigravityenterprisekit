# agkit: allow-secret allow-pattern
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from component_registry import load_frontmatter, normalize_list


class AgentsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agents_dir = (TOOLKIT / "agents") if (TOOLKIT / "agents").is_dir() else (TOOLKIT / "agent")
        cls.skills_dir = TOOLKIT / "skills"
        cls.agent_files = sorted(cls.agents_dir.glob("*.md"))
        cls.known_skills = {p.parent.name for p in cls.skills_dir.glob("*/SKILL.md")}

    def test_total_agents_count_is_exact(self):
        self.assertEqual(20, len(self.agent_files), "Expected exactly 20 enterprise specialist agents")

    def test_all_agents_have_valid_frontmatter(self):
        for path in self.agent_files:
            data = load_frontmatter(path)
            self.assertIn("name", data, f"Missing 'name' in {path.name}")
            self.assertIn("description", data, f"Missing 'description' in {path.name}")
            self.assertIn("tools", data, f"Missing 'tools' in {path.name}")
            self.assertIn("model", data, f"Missing 'model' in {path.name}")
            self.assertEqual(path.stem, data.get("name"), f"Agent filename must match name in {path.name}")

    def test_agent_skills_exist_in_toolkit(self):
        for path in self.agent_files:
            data = load_frontmatter(path)
            agent_skills = normalize_list(data.get("skills"))
            for skill in agent_skills:
                self.assertIn(
                    skill,
                    self.known_skills,
                    f"Agent '{path.stem}' references missing skill: '{skill}'",
                )

    def test_agent_guidance_contains_critical_rules(self):
        for path in self.agent_files:
            text = path.read_text("utf-8")
            self.assertTrue(
                "temel kural" in text.lower() or "kural" in text.lower(),
                f"Agent '{path.name}' should reference core rules",
            )


if __name__ == "__main__":
    unittest.main()

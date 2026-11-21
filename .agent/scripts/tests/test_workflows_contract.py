# agkit: allow-secret allow-pattern
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from component_registry import load_frontmatter, normalize_list


class WorkflowsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflows_dir = TOOLKIT / "workflows"
        cls.workflow_files = sorted(cls.workflows_dir.glob("*.md"))
        agents_dir = (TOOLKIT / "agents") if (TOOLKIT / "agents").is_dir() else (TOOLKIT / "agent")
        cls.known_agents = {p.stem for p in agents_dir.glob("*.md")}
        cls.known_skills = {p.parent.name for p in (TOOLKIT / "skills").glob("*/SKILL.md")}

    def test_total_workflows_count_is_exact(self):
        self.assertEqual(14, len(self.workflow_files), "Expected exactly 14 enterprise workflows")

    def test_workflows_have_valid_frontmatter(self):
        for path in self.workflow_files:
            data = load_frontmatter(path)
            self.assertIn("name", data, f"Missing 'name' in {path.name}")
            self.assertIn("description", data, f"Missing 'description' in {path.name}")
            self.assertIn("version", data, f"Missing 'version' in {path.name}")

    def test_workflow_referenced_agents_exist(self):
        for path in self.workflow_files:
            data = load_frontmatter(path)
            req_agents = normalize_list(data.get("requires_agents"))
            for agent in req_agents:
                self.assertIn(
                    agent,
                    self.known_agents,
                    f"Workflow '{path.name}' references missing agent: '{agent}'",
                )

    def test_workflow_referenced_skills_exist(self):
        for path in self.workflow_files:
            data = load_frontmatter(path)
            req_skills = normalize_list(data.get("requires_skills"))
            for skill in req_skills:
                self.assertIn(
                    skill,
                    self.known_skills,
                    f"Workflow '{path.name}' references missing skill: '{skill}'",
                )


if __name__ == "__main__":
    unittest.main()

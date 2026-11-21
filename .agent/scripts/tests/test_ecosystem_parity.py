# agkit: allow-secret allow-pattern
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = TOOLKIT.parent
SCRIPTS = TOOLKIT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from github_automator import get_git_info, build_pr_body, create_github_pr
from media_extractor import extract_youtube_id, generate_mock_transcript, format_transcript_markdown
from skill_aggregator import get_local_skills_inventory, normalize_skill_content


class EcosystemParityTests(unittest.TestCase):
    def test_github_actions_workflow_exists_and_valid(self):
        wf_path = WORKSPACE_ROOT / ".github" / "workflows" / "verify-kit.yml"
        self.assertTrue(wf_path.is_file(), "Missing .github/workflows/verify-kit.yml")
        content = wf_path.read_text("utf-8")
        self.assertIn("verify_kit.py", content)
        self.assertIn("ubuntu-latest", content)
        self.assertIn("windows-latest", content)
        self.assertIn("3.11", content)
        self.assertIn("3.13", content)

    def test_installer_scripts_exist_and_consistent(self):
        ps1_path = WORKSPACE_ROOT / "install.ps1"
        sh_path = WORKSPACE_ROOT / "install.sh"
        self.assertTrue(ps1_path.is_file(), "Missing install.ps1")
        self.assertTrue(sh_path.is_file(), "Missing install.sh")

        ps1_txt = ps1_path.read_text("utf-8")
        sh_txt = sh_path.read_text("utf-8")

        self.assertIn(".agent", ps1_txt)
        self.assertIn(".gitignore", ps1_txt)
        self.assertIn(".agent", sh_txt)
        self.assertIn(".gitignore", sh_txt)

    def test_official_plugin_manifest_structure(self):
        plugin_path = WORKSPACE_ROOT / "plugin.json"
        self.assertTrue(plugin_path.is_file(), "Missing plugin.json")
        data = json.loads(plugin_path.read_text("utf-8"))
        
        self.assertEqual(data.get("name"), "antigravity-ai-os")
        self.assertIn("displayName", data)
        self.assertIn("version", data)
        self.assertIn("suggestedPrompts", data)
        self.assertEqual(len(data["suggestedPrompts"]), 3)
        self.assertIn("capabilities", data)
        self.assertEqual(data["capabilities"]["rules"], 48)

    def test_github_automator_dry_run_and_body_generation(self):
        body = build_pr_body(
            summary="Test PR creation",
            rules_applied=[1, 2, 3],
            test_summary="49/49 passed",
            neural_node="test-node",
        )
        self.assertIn("Test PR creation", body)
        self.assertIn("1. kural, 2. kural, 3. kural", body)
        self.assertIn("[[test-node]]", body)

        res = create_github_pr(title="Test PR", summary="Summary", dry_run=True)
        self.assertEqual(res["status"], "dry-run")
        self.assertIn("body", res)

    def test_media_extractor_youtube_id_and_mock_transcripts(self):
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            "dQw4w9WgXcQ",
        ]
        for u in valid_urls:
            self.assertEqual(extract_youtube_id(u), "dQw4w9WgXcQ")

        mock_segs = generate_mock_transcript("dQw4w9WgXcQ")
        self.assertEqual(len(mock_segs), 4)
        md = format_transcript_markdown({"title": "Test Video", "video_id": "dQw4w9WgXcQ"}, mock_segs)
        self.assertIn("Medya Transkript Raporu", md)
        self.assertIn("[00:00]", md)

    def test_skill_aggregator_local_inventory_and_normalizer(self):
        inv = get_local_skills_inventory()
        self.assertGreaterEqual(len(inv), 90, "Expected at least 90 local skills")
        self.assertIn("clean-code", inv)
        
        normalized = normalize_skill_content(
            name="custom-skill",
            description="Özel beceri açıklaması",
            raw_content="# custom-skill\nİçerik buraya.",
        )
        self.assertTrue(normalized.startswith("---"))
        self.assertIn("name: custom-skill", normalized)
        self.assertIn("description: Özel beceri açıklaması", normalized)


if __name__ == "__main__":
    unittest.main()

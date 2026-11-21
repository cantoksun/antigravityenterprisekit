# agkit: allow-secret allow-pattern
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
sys.path.insert(0, str(SCRIPTS))


class RulesContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules_file = TOOLKIT / "rules" / "GEMINI.md"
        cls.rules_text = cls.rules_file.read_text("utf-8")

    def test_rules_file_exists(self):
        self.assertTrue(self.rules_file.is_file(), "Missing .agent/rules/GEMINI.md")

    def test_all_48_rules_present_sequentially(self):
        for num in range(1, 49):
            pattern = rf"\b{num}\.\s*kural\b"
            match = re.search(pattern, self.rules_text, re.IGNORECASE)
            self.assertIsNotNone(match, f"Missing rule definition for: {num}. kural in GEMINI.md")

    def test_rule_1_language_is_strictly_turkish_lowercase(self):
        # Verify Rule 1 mentions turkish, lowercase and characters
        rule_1_match = re.search(r"1\.\s*kural.*", self.rules_text, re.IGNORECASE)
        self.assertIsNotNone(rule_1_match)
        line = rule_1_match.group(0).lower()
        self.assertIn("türkçe", line)
        self.assertIn("küçük harf", line)

    def test_critical_security_rules_present(self):
        # 6 (api security), 7 (secrets), 8 (idor/bola), 20 (idempotency), 21 (soft delete), 22 (audit log)
        critical_keywords = [
            "api güvenliği",
            "hassas veri",
            "idor",
            "idempotency",
            "soft delete",
            "audit",
        ]
        text_lower = self.rules_text.lower()
        for kw in critical_keywords:
            self.assertIn(kw, text_lower, f"Critical security rule keyword '{kw}' missing from GEMINI.md")


if __name__ == "__main__":
    unittest.main()

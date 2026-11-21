# agkit: allow-secret allow-pattern
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from rule_dispatcher import (
    load_rules_matrix,
    resolve_rule_ids,
    get_active_rules_metadata,
    render_markdown_prompt,
)
from skill_loader import load_l0_metadata, load_l1_index, list_skills
from neural_os_rag import ProactiveNeuralRAG, get_proactive_memory_context
from context_budget import audit_context_budget, estimate_tokens


class ContextOptimizationTests(unittest.TestCase):
    def test_rules_matrix_structure_and_tiers(self):
        matrix = load_rules_matrix(TOOLKIT.parent)
        self.assertIn("tiers", matrix)
        self.assertIn("rules", matrix)
        
        tiers = matrix["tiers"]
        self.assertIn("tier_0_universal", tiers)
        self.assertIn("tier_1_backend", tiers)
        self.assertIn("tier_1_frontend", tiers)
        self.assertIn("tier_1_security", tiers)

        # 48 total rules in matrix
        self.assertEqual(len(matrix["rules"]), 48, "Rules matrix must contain exactly 48 rules")

        # Tier 0 has universal rules
        t0_rules = tiers["tier_0_universal"]["rule_ids"]
        self.assertIn(1, t0_rules)  # language & character
        self.assertIn(2, t0_rules)  # modular planning
        self.assertIn(3, t0_rules)  # single module execution
        self.assertIn(4, t0_rules)  # simplicity
        self.assertIn(17, t0_rules) # zero friction
        self.assertIn(18, t0_rules) # zero assumptions

    def test_rule_dispatcher_filters_and_always_includes_tier_0(self):
        matrix = load_rules_matrix(TOOLKIT.parent)
        
        # Universal domain (Tier 0 only)
        u_ids = resolve_rule_ids(matrix, domain="universal")
        self.assertEqual(len(u_ids), 11)
        self.assertEqual(u_ids, [1, 2, 3, 4, 7, 17, 18, 19, 45, 46, 47])

        # Frontend domain
        fe_ids = resolve_rule_ids(matrix, domain="frontend")
        self.assertIn(15, fe_ids) # 15. kural responsive ux
        self.assertIn(16, fe_ids) # 16. kural typography
        self.assertIn(23, fe_ids) # 23. kural keyboard accessibility
        # Tier 0 must be included in frontend
        for t0 in [1, 2, 3, 4, 17, 18]:
            self.assertIn(t0, fe_ids)

        # Backend domain
        be_ids = resolve_rule_ids(matrix, domain="backend")
        self.assertIn(5, be_ids)  # 5. kural db modeling
        self.assertIn(20, be_ids) # 20. kural idempotency
        self.assertIn(21, be_ids) # 21. kural soft delete
        self.assertIn(25, be_ids) # 25. kural db transaction

        # Token savings verification
        meta_fe = get_active_rules_metadata(domain="frontend", root=TOOLKIT.parent)
        self.assertGreaterEqual(meta_fe["token_reduction_percent"], 50.0)

    def test_progressive_skill_loader_levels(self):
        # L0 test
        l0_meta = load_l0_metadata("clean-code", root=TOOLKIT.parent)
        self.assertEqual(l0_meta["level"], "L0")
        self.assertIn("yalın", l0_meta["description"].lower())

        # L1 test
        l1_data = load_l1_index("clean-code", max_lines=50, root=TOOLKIT.parent)
        self.assertEqual(l1_data["level"], "L1")
        self.assertLessEqual(l1_data["returned_lines"], 50)
        self.assertIn("clean code", l1_data["content"].lower())

        # List all skills
        all_skills = list_skills(root=TOOLKIT.parent)
        self.assertGreaterEqual(len(all_skills), 90, "Expected at least 90 skills in workspace")

    def test_proactive_neural_rag_retrieval(self):
        rag = ProactiveNeuralRAG(root=TOOLKIT.parent)
        results = rag.retrieve("owasp idor güvenlik zafiyeti", limit=3)
        self.assertTrue(len(results) > 0, "RAG should return matching security nodes")
        
        # Test markdown output with wikilinks
        md = rag.format_markdown("owasp idor güvenlik zafiyeti", limit=3)
        self.assertIn("[[", md)
        self.assertIn("]]", md)
        self.assertIn("proactive rag", md)

    def test_context_budget_ceiling_compliance(self):
        report = audit_context_budget(domain="frontend", sample_skill="clean-code")
        self.assertTrue(report["passed"], "Context budget must pass ceiling limit")
        self.assertEqual(report["status"], "pass")
        self.assertLessEqual(
            report["tokens"]["total_baseline"],
            report["limits"]["total_baseline_ceiling_tokens"],
            "Total baseline tokens must be strictly under 4,000",
        )


if __name__ == "__main__":
    unittest.main()

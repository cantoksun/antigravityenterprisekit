# agkit: allow-secret allow-pattern
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
NEURAL_OS_ENGINE = TOOLKIT / "neural_os" / "engine"
sys.path.insert(0, str(NEURAL_OS_ENGINE))

from graph_engine import EnterpriseGraphEngine
from semantic_search import LocalHybridSearchEngine


class NeuralOsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = EnterpriseGraphEngine()
        cls.search = LocalHybridSearchEngine(graph_engine=cls.engine)

    def test_graph_has_nodes_and_edges(self):
        export = self.engine.get_graph_export()
        self.assertGreaterEqual(export["total_nodes"], 120, "Expected at least 120 nodes in knowledge graph")
        self.assertGreaterEqual(export["total_edges"], 250, "Expected at least 250 edges in knowledge graph")

    def test_graph_has_zero_broken_links(self):
        audit = self.engine.audit()
        broken = audit.get("broken_links", {})
        self.assertEqual(0, len(broken), f"Neural OS graph must have zero broken links: {broken}")

    def test_pagerank_computed_for_all_nodes(self):
        for node in self.engine.nodes.values():
            self.assertGreater(node.metrics.pagerank, 0.0, f"PageRank missing for node {node.id}")

    def test_semantic_search_returns_ranked_results(self):
        results = self.search.search("güvenlik owasp idor", limit=5)
        self.assertTrue(len(results) > 0, "Semantic search should return results for security query")
        # Check scores are sorted descending
        scores = [r.score for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_standalone_preview_html_is_healthy(self):
        preview = TOOLKIT / "neural_os" / "ui" / "graph-preview.html"
        self.assertTrue(preview.is_file(), "Missing graph-preview.html")
        self.assertGreater(preview.stat().st_size, 500_000, "graph-preview.html size too small")
        content = preview.read_text("utf-8")
        self.assertIn("__EMBEDDED_GRAPH_DATA__", content)
        self.assertIn("buildGraph", content)


if __name__ == "__main__":
    unittest.main()

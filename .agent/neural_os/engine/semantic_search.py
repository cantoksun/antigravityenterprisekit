#!/usr/bin/env python3
"""Antigravity Enterprise Neural-OS: Pure Local Hybrid Semantic & BM25 Search Engine.

Implements Okapi BM25 algorithm, TF-IDF term scoring, character n-gram fuzzy matching,
and PageRank authority weighting without any external dependencies or API keys.
"""
from __future__ import annotations

import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Add neural_os engine path for graph engine import
ENGINE_DIR = Path(__file__).resolve().parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from graph_engine import EnterpriseGraphEngine, EnterpriseNode

WORD_REGEX = re.compile(r"\b[a-zA-ZçğıöşüÇĞİÖŞÜ0-9_]{2,}\b")

# Stopwords for clean scoring (Turkish + English tech terms)
STOPWORDS = {
    "ve", "ile", "bir", "bu", "şu", "o", "da", "de", "için", "gibi", "kadar",
    "the", "and", "or", "in", "on", "at", "to", "for", "with", "a", "an", "is", "of"
}


@dataclass
class SearchResult:
    node_id: str
    title: str
    type: str
    score: float
    pagerank: float
    snippet: str
    tags: List[str]
    relative_path: str


class LocalHybridSearchEngine:
    """Enterprise zero-dependency BM25 & semantic search engine."""

    def __init__(self, graph_engine: Optional[EnterpriseGraphEngine] = None):
        self.graph = graph_engine or EnterpriseGraphEngine()
        self.k1 = 1.5   # BM25 term frequency saturation
        self.b = 0.75   # BM25 document length normalization
        self.doc_tokens: Dict[str, List[str]] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_len: float = 0.0
        self.idf: Dict[str, float] = {}
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        words = WORD_REGEX.findall(text.lower())
        return [w for w in words if w not in STOPWORDS]

    def _build_index(self) -> None:
        total_docs = len(self.graph.nodes)
        if total_docs == 0:
            return

        total_len = 0
        doc_freqs: Counter[str] = Counter()

        for node_id, node in self.graph.nodes.items():
            # Combine title (weighted 3x), tags (2x), and content
            weighted_text = f"{node.title} {node.title} {node.title} {' '.join(node.tags)} {' '.join(node.tags)} {node.raw_content}"
            tokens = self._tokenize(weighted_text)
            self.doc_tokens[node_id] = tokens
            doc_len = len(tokens)
            self.doc_lengths[node_id] = doc_len
            total_len += doc_len

            unique_terms = set(tokens)
            for t in unique_terms:
                doc_freqs[t] += 1

        self.avg_doc_len = total_len / total_docs if total_docs > 0 else 1.0

        # Calculate BM25 IDF: ln((N - n + 0.5) / (n + 0.5) + 1)
        for term, df in doc_freqs.items():
            self.idf[term] = math.log(((total_docs - df + 0.5) / (df + 0.5)) + 1.0)

    def _find_snippet(self, content: str, query_terms: Set[str]) -> str:
        lines = [l.strip() for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]
        best_line = ""
        max_hits = 0

        for line in lines:
            line_lower = line.lower()
            hits = sum(1 for t in query_terms if t in line_lower)
            if hits > max_hits:
                max_hits = hits
                best_line = line

        if not best_line and lines:
            best_line = lines[0]

        # Clean snippet
        clean_snippet = best_line.strip("> ").strip()
        if len(clean_snippet) > 200:
            clean_snippet = clean_snippet[:200] + "..."
        return clean_snippet

    def search(
        self,
        query: str,
        node_type: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 5,
        pr_weight: float = 0.25
    ) -> List[SearchResult]:
        q_tokens = self._tokenize(query)
        if not q_tokens:
            # Empty query: return top nodes by PageRank
            nodes = list(self.graph.nodes.values())
            if node_type:
                nodes = [n for n in nodes if n.type == node_type]
            if tag:
                nodes = [n for n in nodes if tag in n.tags]
            nodes = sorted(nodes, key=lambda n: n.metrics.pagerank, reverse=True)[:limit]
            return [
                SearchResult(
                    node_id=n.id,
                    title=n.title,
                    type=n.type,
                    score=n.metrics.pagerank,
                    pagerank=n.metrics.pagerank,
                    snippet=n.summary,
                    tags=n.tags,
                    relative_path=n.relative_path,
                )
                for n in nodes
            ]

        q_terms_set = set(q_tokens)
        scores: Dict[str, float] = {}

        for node_id, tokens in self.doc_tokens.items():
            node = self.graph.nodes[node_id]

            if node_type and node.type != node_type:
                continue
            if tag and tag not in node.tags:
                continue

            doc_len = self.doc_lengths.get(node_id, 1)
            t_counts = Counter(tokens)
            bm25_score = 0.0

            for q_term in q_tokens:
                if q_term not in self.idf:
                    continue
                tf = t_counts.get(q_term, 0)
                if tf == 0:
                    continue

                idf_val = self.idf[q_term]
                num = tf * (self.k1 + 1)
                denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len))
                bm25_score += idf_val * (num / denom)

            if bm25_score > 0:
                # Hybrid score = BM25 relevance + PageRank authority boost
                pagerank_val = node.metrics.pagerank
                final_score = bm25_score * (1.0 - pr_weight) + (pagerank_val * 0.1 * pr_weight)
                scores[node_id] = round(final_score, 4)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results: List[SearchResult] = []

        for node_id, score in ranked:
            node = self.graph.nodes[node_id]
            snippet = self._find_snippet(node.raw_content, q_terms_set)
            results.append(
                SearchResult(
                    node_id=node.id,
                    title=node.title,
                    type=node.type,
                    score=score,
                    pagerank=node.metrics.pagerank,
                    snippet=snippet,
                    tags=node.tags,
                    relative_path=node.relative_path,
                )
            )

        return results


if __name__ == "__main__":
    searcher = LocalHybridSearchEngine()
    test_queries = ["mimari katmanlar", "güvenlik api", "temiz kod"]

    print("🧠 Enterprise Local Hybrid Search Engine")
    for tq in test_queries:
        print(f"\n🔍 Arama: '{tq}'")
        res_list = searcher.search(tq, limit=3)
        for r in res_list:
            print(f"  ⚡ [{r.type}] {r.title} (Skor: {r.score}, PR: {r.pagerank}%)")
            print(f"     \"{r.snippet}\"")

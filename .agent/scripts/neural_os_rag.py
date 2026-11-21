#!/usr/bin/env python3
"""
neural_os_rag.py
Antigravity AI-OS v1.0 - Proactive RAG Neural Memory Hook

Performs proactive, low-token RAG retrieval against the 124+ node Neural Knowledge Graph.
Instead of loading the full graph or reading entire vault directories, retrieves only
the top 2-3 most semantically relevant nodes (~200-300 tokens total) to inject into
the agent prompt or session context.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
NEURAL_OS_ENGINE = WORKSPACE_ROOT / ".agent" / "neural_os" / "engine"
if str(NEURAL_OS_ENGINE) not in sys.path:
    sys.path.insert(0, str(NEURAL_OS_ENGINE))

try:
    from graph_engine import EnterpriseGraphEngine
    from semantic_search import LocalHybridSearchEngine, SearchResult
except ImportError:
    EnterpriseGraphEngine = None  # type: ignore
    LocalHybridSearchEngine = None  # type: ignore


class ProactiveNeuralRAG:
    """Proactive RAG interface for the Antigravity Neural-OS Graph."""

    def __init__(self, root: Optional[Path] = None):
        self.root = root or WORKSPACE_ROOT
        if EnterpriseGraphEngine is None or LocalHybridSearchEngine is None:
            self.graph = None
            self.search = None
        else:
            self.graph = EnterpriseGraphEngine(vault_root=self.root / ".agent" / "vault")
            self.search = LocalHybridSearchEngine(graph_engine=self.graph)

    def retrieve(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        if not self.search:
            return []
        if not query or not query.strip():
            return []

        results = self.search.search(query.strip(), limit=limit)
        items: List[Dict[str, Any]] = []

        for r in results:
            node = self.graph.nodes.get(r.node_id) if self.graph else None
            outlinks = sorted(list(node.outlinks)) if node else []
            backlinks = sorted(list(node.backlinks)) if node else []

            # Clean and truncate snippet to avoid context bloating (max 200 chars)
            clean_snippet = " ".join(r.snippet.split())
            if len(clean_snippet) > 200:
                clean_snippet = clean_snippet[:197] + "..."

            items.append({
                "node_id": r.node_id,
                "title": r.title,
                "type": r.type,
                "score": round(r.score, 4),
                "pagerank": round(r.pagerank, 4),
                "snippet": clean_snippet,
                "tags": r.tags[:5],
                "outlinks": outlinks[:3],
                "backlinks": backlinks[:3],
            })
        return items

    def format_markdown(self, query: str, limit: int = 3) -> str:
        nodes = self.retrieve(query, limit=limit)
        if not nodes:
            return "<!-- Proactive Neural RAG: Eşleşen nöral bellek kaydı bulunamadı. -->"

        lines = [
            f"### 🧠 nöral bellek hatırlatıcıları (proactive rag: {len(nodes)} odak düğüm)\n"
        ]
        for item in nodes:
            links_str = ""
            if item["outlinks"]:
                links_str = f" | bağlantılar: {', '.join(item['outlinks'])}"
            lines.append(
                f"- **[[{item['node_id']}]] ({item['title']})** [{item['type']} - sk: {item['score']}]{links_str}\n"
                f"  > {item['snippet']}"
            )
        return "\n".join(lines)


def get_proactive_memory_context(query: str, limit: int = 3) -> str:
    """Helper function to retrieve proactive RAG memory markdown."""
    rag = ProactiveNeuralRAG()
    return rag.format_markdown(query, limit=limit)


def main() -> int:
    parser = argparse.ArgumentParser(description="Proactive RAG Neural Memory Hook")
    parser.add_argument("--query", "-q", required=True, help="Task query, domain, or user prompt")
    parser.add_argument("--limit", "-l", type=int, default=3, help="Max nodes to retrieve (default: 3)")
    parser.add_argument("--format", choices=["markdown", "json", "compact"], default="markdown", help="Output format")
    args = parser.parse_args()

    rag = ProactiveNeuralRAG()
    try:
        if args.format == "json":
            data = rag.retrieve(args.query, limit=args.limit)
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.format == "compact":
            data = rag.retrieve(args.query, limit=args.limit)
            summary = [f"{d['node_id']} ({d['title']}) [{d['score']}]" for d in data]
            print(" | ".join(summary) if summary else "Eşleşme yok")
        else:
            print(rag.format_markdown(args.query, limit=args.limit))
        return 0
    except Exception as e:
        print(f"Hata: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

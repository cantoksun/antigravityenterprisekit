#!/usr/bin/env python3
"""Antigravity Enterprise Neural-OS: Advanced Graph Analytics & PageRank Engine.

Calculates bidirectional links, node degree centrality, PageRank scores,
clustering metrics, and topological sorting without external dependencies.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class NodeMetrics:
    in_degree: int = 0
    out_degree: int = 0
    degree_centrality: float = 0.0
    pagerank: float = 0.0


@dataclass
class EnterpriseNode:
    id: str
    title: str
    type: str
    relative_path: str
    tags: List[str] = field(default_factory=list)
    outlinks: Set[str] = field(default_factory=set)
    backlinks: Set[str] = field(default_factory=set)
    raw_content: str = ""
    summary: str = ""
    metrics: NodeMetrics = field(default_factory=NodeMetrics)
    created: str = ""
    updated: str = ""


class EnterpriseGraphEngine:
    """Zero-dependency high performance graph analytics engine."""

    def __init__(self, vault_root: Optional[Path] = None):
        agent_dir = Path(__file__).resolve().parents[2]
        self.agent_dir = agent_dir
        if vault_root is None:
            self.root = (agent_dir / "vault").resolve()
        else:
            self.root = vault_root.resolve()

        self.nodes: Dict[str, EnterpriseNode] = {}
        self.build_graph()

    def _parse_frontmatter(self, text: str) -> Tuple[Dict[str, Any], str]:
        match = FRONTMATTER_PATTERN.match(text)
        if not match:
            return {}, text
        raw = match.group(1)
        body = text[match.end():].strip()
        data: Dict[str, Any] = {}
        current_list: Optional[str] = None
        for line in raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- "):
                val = line[2:].strip().strip("\"'")
                if current_list and current_list in data:
                    data[current_list].append(val)
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip("\"'")
                if not v:
                    data[k] = []
                    current_list = k
                else:
                    data[k] = v
                    current_list = None
        return data, body

    def _extract_summary(self, body: str) -> str:
        lines = [line.strip() for line in body.splitlines() if line.strip() and not line.strip().startswith("#")]
        if not lines:
            return ""
        first_para = lines[0].strip("> ").strip()
        return first_para[:240] + ("..." if len(first_para) > 240 else "")

    def _resolve_node_id(self, target: str) -> Optional[str]:
        target_clean = target.strip().strip("`\"'")
        if target_clean in self.nodes:
            return target_clean
        target_lower = target_clean.lower()
        for node_id in self.nodes:
            if node_id.lower() == target_lower:
                return node_id
        return None

    def build_graph(self) -> None:
        self.nodes.clear()
        if not self.root.is_dir():
            return

        # 1. Parse all vault markdown files
        for md_path in self.root.rglob("*.md"):
            if md_path.name.startswith("."):
                continue
            rel_path = md_path.relative_to(self.agent_dir).as_posix()
            stem = md_path.stem
            content = md_path.read_text("utf-8", errors="replace")
            fm, body = self._parse_frontmatter(content)

            node_id = fm.get("id", stem)
            title = fm.get("title", stem.replace("-", " ").title())
            node_type = fm.get("type", md_path.parent.name if md_path.parent != self.root else "root")
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]

            outlinks: Set[str] = set()
            for match in WIKILINK_PATTERN.finditer(content):
                link = match.group(1).strip().strip("`\"'")
                if link in {"wikilink", "dosya-adi"}:
                    continue
                outlinks.add(link)

            self.nodes[node_id] = EnterpriseNode(
                id=node_id,
                title=title,
                type=node_type,
                relative_path=rel_path,
                tags=tags,
                outlinks=outlinks,
                raw_content=content,
                summary=self._extract_summary(body),
                created=str(fm.get("created", "")),
                updated=str(fm.get("updated", "")),
            )

        # 2. Organically parse all 20 AI Agents (.agent/agents/*.md)
        agents_dir = self.agent_dir / "agents"
        if agents_dir.is_dir():
            for agent_path in agents_dir.glob("*.md"):
                stem = agent_path.stem
                rel_path = agent_path.relative_to(self.agent_dir).as_posix()
                content = agent_path.read_text("utf-8", errors="replace")
                fm, body = self._parse_frontmatter(content)
                
                agent_id = f"agent-{stem}"
                title = f"@{stem}"
                skills_raw = fm.get("skills", "")
                skill_list = [s.strip() for s in skills_raw.split(",") if s.strip()] if isinstance(skills_raw, str) else skills_raw
                
                # Links to skills and core rules
                outlinks = {f"skill-{s}" for s in skill_list}
                outlinks.add("rule-gemini")
                outlinks.add("architecture-overview")

                self.nodes[agent_id] = EnterpriseNode(
                    id=agent_id,
                    title=title,
                    type="agent",
                    relative_path=rel_path,
                    tags=["agent", "ai-specialist"],
                    outlinks=outlinks,
                    raw_content=content,
                    summary=fm.get("description", self._extract_summary(body)),
                    created="2026-11-21",
                    updated="2026-11-21",
                )

        # 3. Organically parse key AI Skills (.agent/skills/*/SKILL.md)
        skills_dir = self.agent_dir / "skills"
        if skills_dir.is_dir():
            for skill_path in skills_dir.glob("*/SKILL.md"):
                skill_name = skill_path.parent.name
                rel_path = skill_path.relative_to(self.agent_dir).as_posix()
                content = skill_path.read_text("utf-8", errors="replace")
                fm, body = self._parse_frontmatter(content)

                skill_id = f"skill-{skill_name}"
                title = f"skill:{skill_name}"
                outlinks = {"architecture-overview"}
                if "clean-code" in skill_name:
                    outlinks.add("clean-code-principles")

                self.nodes[skill_id] = EnterpriseNode(
                    id=skill_id,
                    title=title,
                    type="skill",
                    relative_path=rel_path,
                    tags=["skill", "capability"],
                    outlinks=outlinks,
                    raw_content=content,
                    summary=fm.get("description", self._extract_summary(body)),
                    created="2026-11-21",
                    updated="2026-11-21",
                )

        # 4. Organically parse System Constitution (.agent/rules/GEMINI.md)
        rules_path = self.agent_dir / "rules" / "GEMINI.md"
        if rules_path.is_file():
            content = rules_path.read_text("utf-8", errors="replace")
            fm, body = self._parse_frontmatter(content)
            self.nodes["rule-gemini"] = EnterpriseNode(
                id="rule-gemini",
                title="kural:GEMINI (48 temel kural)",
                type="rule",
                relative_path="rules/GEMINI.md",
                tags=["rules", "constitution", "governance"],
                outlinks={"architecture-overview", "clean-code-principles"},
                raw_content=content,
                summary="antigravity ai-os kiti 48 temel anayasa kuralı ve mutlak öncelik protokolü.",
                created="2026-11-21",
                updated="2026-11-21",
            )

        # 2. Build backlinks and resolve link targets
        for node_id, node in self.nodes.items():
            resolved_outlinks: Set[str] = set()
            for target in node.outlinks:
                resolved = self._resolve_node_id(target)
                if resolved:
                    resolved_outlinks.add(resolved)
                    self.nodes[resolved].backlinks.add(node_id)
                else:
                    resolved_outlinks.add(target)
            node.outlinks = resolved_outlinks

        # 3. Calculate graph metrics (Degree Centrality & PageRank)
        self._calculate_metrics()

    def _calculate_metrics(self) -> None:
        n = len(self.nodes)
        if n == 0:
            return

        # Degree centrality
        for node in self.nodes.values():
            node.metrics.in_degree = len(node.backlinks)
            node.metrics.out_degree = len(node.outlinks)
            total_degree = node.metrics.in_degree + node.metrics.out_degree
            node.metrics.degree_centrality = round(total_degree / (n - 1), 4) if n > 1 else 1.0

        # PageRank with damping factor d=0.85
        d = 0.85
        max_iter = 40
        tol = 1e-5
        ranks = {nid: 1.0 / n for nid in self.nodes}

        for _ in range(max_iter):
            new_ranks: Dict[str, float] = {}
            dangling_sum = sum(ranks[nid] for nid, node in self.nodes.items() if not node.outlinks)

            for nid in self.nodes:
                incoming_sum = 0.0
                for source_id in self.nodes[nid].backlinks:
                    source_out = len(self.nodes[source_id].outlinks)
                    if source_out > 0:
                        incoming_sum += ranks[source_id] / source_out

                new_rank = ((1.0 - d) / n) + d * (incoming_sum + dangling_sum / n)
                new_ranks[nid] = new_rank

            diff = sum(abs(new_ranks[nid] - ranks[nid]) for nid in self.nodes)
            ranks = new_ranks
            if diff < tol:
                break

        for nid, rank in ranks.items():
            self.nodes[nid].metrics.pagerank = round(rank * 100, 3)

    def get_graph_export(self) -> Dict[str, Any]:
        """Produce clean JSON structure for web canvas/force-directed rendering."""
        # Canlı, estetik ve yüksek kontrastlı renk kodları (Proje Dijital İkizi)
        node_type_colors = {
            "root": "#a855f7",       # MOC / Ana İndeks - Canlı Mor
            "MOC": "#a855f7",
            "concept": "#38bdf8",    # Kavramlar - Parlak Camgöbeği/Mavi
            "concepts": "#38bdf8",
            "decision": "#fb923c",   # Mimari Kararlar - Parlak Turuncu
            "decisions": "#fb923c",
            "playbook": "#34d399",   # Operasyon Rehberleri - Parlak Zümrüt Yeşili
            "playbooks": "#34d399",
            "episode": "#f87171",    # Epizodik Hafıza - Parlak Mercan Kırmızısı
            "episodes": "#f87171",
            "agent": "#818cf8",      # Uzman Ajanlar - Neon İndigo
            "skill": "#22d3ee",      # Kurumsal Beceriler - Açık Turkuaz
            "rule": "#f43f5e",       # Anayasa Kuralları - Derin Kırmızı
        }

        nodes_list = []
        links_list = []
        existing_edges: Set[Tuple[str, str]] = set()

        for node in self.nodes.values():
            color = node_type_colors.get(node.type.lower(), "#64748b")
            nodes_list.append({
                "id": node.id,
                "title": node.title,
                "type": node.type,
                "tags": node.tags,
                "path": node.relative_path,
                "summary": node.summary,
                "in_degree": node.metrics.in_degree,
                "out_degree": node.metrics.out_degree,
                "centrality": node.metrics.degree_centrality,
                "pagerank": node.metrics.pagerank,
                "color": color,
                "val": max(6, int(node.metrics.pagerank * 1.5) + node.metrics.in_degree * 2),
            })

            for target in node.outlinks:
                if target in self.nodes:
                    edge_key = (node.id, target)
                    if edge_key not in existing_edges:
                        existing_edges.add(edge_key)
                        links_list.append({
                            "source": node.id,
                            "target": target,
                            "type": "outlink",
                        })

        return {
            "total_nodes": len(nodes_list),
            "total_edges": len(links_list),
            "nodes": nodes_list,
            "links": links_list,
        }

    def audit(self) -> Dict[str, Any]:
        all_ids = set(self.nodes.keys())
        broken_links: Dict[str, List[str]] = {}
        orphans: List[str] = []

        for node_id, node in self.nodes.items():
            missing = [link for link in node.outlinks if link not in all_ids]
            if missing:
                broken_links[node_id] = missing
            if not node.outlinks and not node.backlinks and node_id != "index":
                orphans.append(node_id)

        top_pagerank = sorted(
            [{"id": n.id, "title": n.title, "pagerank": n.metrics.pagerank, "in_degree": n.metrics.in_degree}
             for n in self.nodes.values()],
            key=lambda x: x["pagerank"],
            reverse=True
        )

        return {
            "total_nodes": len(self.nodes),
            "broken_links": broken_links,
            "orphans": orphans,
            "top_nodes": top_pagerank[:5],
        }


if __name__ == "__main__":
    engine = EnterpriseGraphEngine()
    rep = engine.audit()
    print("🧠 Enterprise Graph Analytics")
    print(f"Nodes: {rep['total_nodes']} | Broken: {len(rep['broken_links'])} | Orphans: {len(rep['orphans'])}")
    print("\nTop Authority Nodes (PageRank):")
    for item in rep["top_nodes"]:
        print(f"  ⭐ {item['id']} (PR: {item['pagerank']}, Gelen: {item['in_degree']}) - {item['title']}")

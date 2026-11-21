#!/usr/bin/env python3
"""Antigravity Neural Vault & Autonomous Memory Engine.

Provides bidirectional link generation, semantic node querying,
knowledge graph validation, and automatic memory synthesis for the 20 AI agents.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class VaultNode:
    id: str
    title: str
    type: str
    path: str
    tags: List[str] = field(default_factory=list)
    outlinks: Set[str] = field(default_factory=set)
    backlinks: Set[str] = field(default_factory=set)
    created: str = ""
    updated: str = ""


class NeuralVault:
    def __init__(self, root: Optional[Path] = None):
        if root is None:
            # .agent/scripts -> .agent/vault
            self.root = (Path(__file__).resolve().parents[1] / "vault").resolve()
        else:
            self.root = root.resolve()
        self.nodes: Dict[str, VaultNode] = {}
        self._build_graph()

    def _parse_frontmatter(self, text: str) -> Dict[str, Any]:
        match = FRONTMATTER_PATTERN.match(text)
        if not match:
            return {}
        raw = match.group(1)
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
        return data

    def _resolve_target(self, target: str) -> Optional[str]:
        """Resolve a wikilink target to an existing node ID, case-insensitively."""
        if target in self.nodes:
            return target
        target_lower = target.lower()
        for node_id in self.nodes:
            if node_id.lower() == target_lower:
                return node_id
        return None

    def _build_graph(self) -> None:
        if not self.root.is_dir():
            return
        
        # 1. Parse all markdown files
        for md_path in self.root.rglob("*.md"):
            if md_path.name.startswith("."):
                continue
            rel_path = md_path.relative_to(self.root).as_posix()
            stem = md_path.stem
            content = md_path.read_text("utf-8", errors="replace")
            fm = self._parse_frontmatter(content)
            
            node_id = fm.get("id", stem)
            title = fm.get("title", stem.replace("-", " ").title())
            node_type = fm.get("type", md_path.parent.name if md_path.parent != self.root else "root")
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            
            # Find all [[wikilinks]] (strip backticks, quotes, and normalize case for lookup)
            outlinks: Set[str] = set()
            for match in WIKILINK_PATTERN.finditer(content):
                link_target = match.group(1).strip().strip("`\"'")
                # ignore documentation placeholders
                if link_target in {"wikilink", "dosya-adi"}:
                    continue
                outlinks.add(link_target)
            
            node = VaultNode(
                id=node_id,
                title=title,
                type=node_type,
                path=rel_path,
                tags=tags,
                outlinks=outlinks,
                created=str(fm.get("created", "")),
                updated=str(fm.get("updated", "")),
            )
            self.nodes[node_id] = node

        # 2. Build backlinks and resolve targets
        for node_id, node in self.nodes.items():
            resolved_outlinks: Set[str] = set()
            for target in node.outlinks:
                resolved = self._resolve_target(target)
                if resolved:
                    resolved_outlinks.add(resolved)
                    self.nodes[resolved].backlinks.add(node_id)
                else:
                    resolved_outlinks.add(target)
            node.outlinks = resolved_outlinks

    def query(self, query_str: str, tag: Optional[str] = None, node_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query vault nodes with token-saving summaries and bidirectional relations."""
        q = query_str.lower()
        results = []
        for node in self.nodes.values():
            if tag and tag not in node.tags:
                continue
            if node_type and node.type != node_type:
                continue
            if q and (q not in node.id.lower() and q not in node.title.lower() and not any(q in t.lower() for t in node.tags)):
                continue
            
            results.append({
                "id": node.id,
                "title": node.title,
                "type": node.type,
                "path": node.path,
                "tags": node.tags,
                "outlinks": sorted(list(node.outlinks)),
                "backlinks": sorted(list(node.backlinks)),
            })
        return results

    def add_decision(self, title: str, context: str, decision: str, consequences: str, tags: Optional[List[str]] = None) -> Path:
        """Create a new ADR node linked with wikilinks."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        filename = f"adr-{slug}.md"
        target_path = self.root / "decisions" / filename
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        tags_list = tags or ["adr", "architecture"]
        tags_yaml = "\n".join(f"  - {t}" for t in tags_list)
        
        content = f"""---
id: adr-{slug}
title: "{title}"
status: accepted
date: {date_str}
type: decision
tags:
{tags_yaml}
links:
  - "[[INDEX]]"
  - "[[architecture-overview]]"
---

# ⚖️ {title}

## 1. bağlam (context)
{context}

## 2. karar (decision)
{decision}

## 3. sonuçlar (consequences)
{consequences}

---

## 📌 ilgili bağlantılar
- ana indeks: [[INDEX]]
- sistem mimarisi: [[architecture-overview]]
"""
        target_path.write_text(content, encoding="utf-8")
        self._build_graph()
        return target_path

    def add_episode(self, title: str, summary: str, related_nodes: Optional[List[str]] = None) -> Path:
        """Log an episodic memory node."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        filename = f"episode-{date_str}-{slug}.md"
        target_path = self.root / "episodes" / filename
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        links = ["[[INDEX]]"]
        if related_nodes:
            links.extend([f"[[{n}]]" for n in related_nodes])
        links_yaml = "\n".join(f"  - \"{l}\"" for l in links)
        
        content = f"""---
id: episode-{date_str}-{slug}
title: "{title}"
type: episode
tags:
  - episode
  - memory
created: {date_str}
links:
{links_yaml}
---

# 📜 {title}

- **tarih:** {date_str}
- **özet:** {summary}

---

## 📌 ilgili bağlantılar
- ana indeks: [[INDEX]]
"""
        target_path.write_text(content, encoding="utf-8")
        self._build_graph()
        return target_path

    def audit_graph(self) -> Dict[str, Any]:
        """Audit vault integrity: find broken links, orphan nodes, and hub nodes."""
        all_ids = set(self.nodes.keys())
        broken_links: Dict[str, List[str]] = {}
        orphans: List[str] = []
        
        for node_id, node in self.nodes.items():
            # Check broken outlinks
            missing = [link for link in node.outlinks if link not in all_ids]
            if missing:
                broken_links[node_id] = missing
            # Check orphans (no outlinks and no backlinks, except root INDEX)
            if not node.outlinks and not node.backlinks and node_id != "index":
                orphans.append(node_id)
                
        return {
            "total_nodes": len(self.nodes),
            "broken_links": broken_links,
            "orphans": orphans,
            "hub_nodes": sorted(
                [{"id": n.id, "connections": len(n.outlinks) + len(n.backlinks)} for n in self.nodes.values()],
                key=lambda x: x["connections"],
                reverse=True
            )[:5]
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity Neural Memory & Vault CLI")
    parser.add_argument("--query", "-q", help="Search vault nodes by text/id")
    parser.add_argument("--tag", "-t", help="Filter by tag")
    parser.add_argument("--type", help="Filter by node type (concept, decision, playbook, episode)")
    parser.add_argument("--audit", action="store_true", help="Perform integrity check on vault graph")
    parser.add_argument("--json", action="store_true", help="Output results in JSON")
    args = parser.parse_args()

    engine = NeuralVault()
    
    if args.audit:
        report = engine.audit_graph()
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print("🧠 Antigravity Neural Vault Audit Report")
            print(f"Toplam Düğüm (Nodes): {report['total_nodes']}")
            print(f"Kırık Bağlantılar (Broken Links): {len(report['broken_links'])}")
            for src, targets in report['broken_links'].items():
                print(f"  ❌ {src} -> {', '.join(targets)}")
            print(f"Yetim Düğümler (Orphans): {len(report['orphans'])}")
            for orphan in report['orphans']:
                print(f"  ⚠️ {orphan}")
            print("\nEn Bağlantılı Merkez Düğümler (Hubs):")
            for hub in report['hub_nodes']:
                print(f"  ⭐ {hub['id']}: {hub['connections']} bağlantı")
        return 0

    results = engine.query(args.query or "", tag=args.tag, node_type=args.type)
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"Bulunan Düğümler ({len(results)}):")
        for res in results:
            print(f"- [{res['type']}] [[{res['id']}]] : {res['title']} (Gelen: {len(res['backlinks'])}, Giden: {len(res['outlinks'])})")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

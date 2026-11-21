#!/usr/bin/env python3
"""Antigravity Enterprise Neural-OS: Autonomous Agent Memory Bridge.

Enables agents to transparently read relevant architectural context and
automatically record decisions & episodic milestones without user intervention.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add neural_os engine path
SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
NEURAL_OS_DIR = PROJECT_ROOT / "neural_os"
ENGINE_DIR = NEURAL_OS_DIR / "engine"
VAULT_DIR = PROJECT_ROOT / "vault"

for p in [str(SCRIPTS_DIR), str(NEURAL_OS_DIR), str(ENGINE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from graph_engine import EnterpriseGraphEngine
from semantic_search import LocalHybridSearchEngine


class AutonomousMemoryBridge:
    """Seamless memory bridge for AI agents."""

    def __init__(self):
        self.engine = EnterpriseGraphEngine(vault_root=VAULT_DIR)
        self.searcher = LocalHybridSearchEngine(self.engine)

    def get_context_for_prompt(self, user_prompt: str, max_nodes: int = 3) -> str:
        """Silently searches the neural vault and returns concise context for the agent."""
        results = self.searcher.search(query=user_prompt, limit=max_nodes)
        if not results:
            return ""

        context_blocks = []
        for r in results:
            context_blocks.append(
                f"- [[{r.node_id}]] ({r.type.upper()}) {r.title}: \"{r.snippet}\""
            )

        return "\n".join(context_blocks)

    def record_decision(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: str,
        tags: Optional[List[str]] = None,
        related_nodes: Optional[List[str]] = None
    ) -> Path:
        """Autonomously records an Architectural Decision Record (ADR)."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        filename = f"adr-{slug}.md"
        target_path = VAULT_DIR / "decisions" / filename
        target_path.parent.mkdir(parents=True, exist_ok=True)

        tags_list = tags or ["adr", "architecture", "auto-recorded"]
        tags_yaml = "\n".join(f"  - {t}" for t in tags_list)

        links = ["[[INDEX]]", "[[architecture-overview]]"]
        if related_nodes:
            links.extend([f"[[{n}]]" for n in related_nodes if f"[[{n}]]" not in links])
        links_yaml = "\n".join(f"  - \"{l}\"" for l in links)

        related_md = "\n".join(f"- {l}" for l in links)

        content = f"""---
id: adr-{slug}
title: "{title}"
status: accepted
date: {date_str}
type: decision
tags:
{tags_yaml}
links:
{links_yaml}
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
{related_md}
"""
        target_path.write_text(content, encoding="utf-8")
        # Refresh engine
        self.engine.build_graph()
        self.searcher._build_index()
        return target_path

    def record_milestone(
        self,
        task_name: str,
        summary: str,
        agent_name: str = "orchestrator",
        related_nodes: Optional[List[str]] = None
    ) -> Path:
        """Autonomously records an episodic memory node upon task completion."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = re.sub(r"[^a-z0-9]+", "-", task_name.lower()).strip("-")
        filename = f"episode-{date_str}-{slug}.md"
        target_path = VAULT_DIR / "episodes" / filename
        target_path.parent.mkdir(parents=True, exist_ok=True)

        links = ["[[INDEX]]", "[[clean-code-principles]]"]
        if related_nodes:
            links.extend([f"[[{n}]]" for n in related_nodes if f"[[{n}]]" not in links])
        links_yaml = "\n".join(f"  - \"{l}\"" for l in links)

        related_md = "\n".join(f"- {l}" for l in links)

        content = f"""---
id: episode-{date_str}-{slug}
title: "{task_name}"
type: episode
agent: "{agent_name}"
tags:
  - episode
  - memory
  - auto-recorded
created: {date_str}
links:
{links_yaml}
---

# 📜 {task_name}

- **tarih:** {date_str}
- **icra eden ajan:** @[{agent_name}]
- **özet:** {summary}

---

## 📌 ilgili bağlantılar
{related_md}
"""
        target_path.write_text(content, encoding="utf-8")
        # Refresh engine
        self.engine.build_graph()
        self.searcher._build_index()
        return target_path


# Global singleton instance for quick script calls
_bridge_instance: Optional[AutonomousMemoryBridge] = None

def get_bridge() -> AutonomousMemoryBridge:
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = AutonomousMemoryBridge()
    return _bridge_instance


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity Autonomous Agent Memory Bridge")
    subparsers = parser.add_subparsers(dest="action")

    # query context
    ctx_p = subparsers.add_parser("context", help="Get context for a prompt")
    ctx_p.add_argument("prompt", help="User prompt to search context for")

    # record milestone
    ms_p = subparsers.add_parser("milestone", help="Auto record a milestone episode")
    ms_p.add_argument("--task", required=True, help="Task name")
    ms_p.add_argument("--summary", required=True, help="Task summary")
    ms_p.add_argument("--agent", default="orchestrator", help="Agent name")
    ms_p.add_argument("--nodes", nargs="*", default=["architecture-overview"], help="Related nodes")

    args = parser.parse_args()
    bridge = get_bridge()

    if args.action == "context":
        ctx = bridge.get_context_for_prompt(args.prompt)
        print(ctx if ctx else "(İlgili geçmiş kayıt bulunamadı)")
    elif args.action == "milestone":
        path = bridge.record_milestone(args.task, args.summary, args.agent, args.nodes)
        print(f"✅ Hafıza düğümü otomatik kaydedildi: {path.name}")
    else:
        print("Kullanım: python auto_memory.py [context|milestone]")

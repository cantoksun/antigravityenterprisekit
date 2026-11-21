#!/usr/bin/env python3
"""
rule_dispatcher.py
Antigravity AI-OS v1.0 - Tier-Based Dynamic Rule Matrix Dispatcher

Dispatches active rules based on agent persona, task domain, or query keywords.
Guarantees Tier 0 universal rules are always active while selectively loading
Tier 1 domain-specific rules (Backend, Frontend, Security) to prevent context bloat.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

AGENT_DOMAIN_MAP: Dict[str, str] = {
    "backend-specialist": "backend",
    "golang-pro": "backend",
    "rust-pro": "backend",
    "c-pro": "backend",
    "frontend-specialist": "frontend",
    "mobile-developer": "frontend",
    "game-developer": "frontend",
    "security-auditor": "security",
    "orchestrator": "universal",
    "project-planner": "universal",
    "debugger": "universal",
    "architect-review": "universal",
}

DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "backend": [
        "api", "sql", "db", "database", "postgres", "redis", "orm", "endpoint",
        "route", "server", "docker", "migration", "k8s", "graphql", "rest",
        "idempotency", "soft delete", "transaction", "dlq", "circuit breaker",
    ],
    "frontend": [
        "ui", "ux", "component", "react", "next", "vue", "tailwind", "css",
        "modal", "drawer", "responsive", "page", "button", "layout", "font",
        "typography", "screen", "mobile", "desktop", "lazy loading", "scroll",
    ],
    "security": [
        "auth", "jwt", "session", "idor", "bola", "xss", "csrf", "csp",
        "reverse engineering", "penetration", "red-team", "vulnerability",
        "secret", "token", "audit", "owasp", "hash", "hmac", "encryption",
    ],
}


def find_workspace_root() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / ".agent" / "rules" / "rules_matrix.json").is_file():
            return candidate
    # Fallback to file parent
    file_root = Path(__file__).resolve().parent.parent.parent
    if (file_root / ".agent" / "rules" / "rules_matrix.json").is_file():
        return file_root
    return cwd


def load_rules_matrix(root: Optional[Path] = None) -> Dict[str, Any]:
    if root is None:
        root = find_workspace_root()
    matrix_path = root / ".agent" / "rules" / "rules_matrix.json"
    if not matrix_path.is_file():
        raise FileNotFoundError(f"Rules matrix not found at {matrix_path}")
    with open(matrix_path, "r", encoding="utf-8") as f:
        return json.load(f)


def infer_domain_from_agent(agent_name: str) -> Optional[str]:
    clean_name = agent_name.lower().strip().replace("@", "").replace("[", "").replace("]", "")
    if clean_name in AGENT_DOMAIN_MAP:
        return AGENT_DOMAIN_MAP[clean_name]
    for key, domain in AGENT_DOMAIN_MAP.items():
        if key in clean_name:
            return domain
    return None


def infer_domain_from_task(task_text: str) -> Set[str]:
    text_lower = task_text.lower()
    detected = set()
    for domain, kws in DOMAIN_KEYWORDS.items():
        for kw in kws:
            if re.search(rf"\b{re.escape(kw)}\b", text_lower):
                detected.add(domain)
                break
    return detected


def resolve_rule_ids(
    matrix: Dict[str, Any],
    domain: Optional[str] = None,
    agent: Optional[str] = None,
    task: Optional[str] = None,
    include_all: bool = False,
) -> List[int]:
    tiers = matrix.get("tiers", {})
    tier_0_rules = tiers.get("tier_0_universal", {}).get("rule_ids", [])
    
    if include_all:
        all_ids = set()
        for t_info in tiers.values():
            all_ids.update(t_info.get("rule_ids", []))
        return sorted(list(all_ids))

    active_rule_ids: Set[int] = set(tier_0_rules)
    selected_domains: Set[str] = set()

    if domain:
        norm_domain = domain.lower().strip()
        if norm_domain in ("all", "full"):
            return resolve_rule_ids(matrix, include_all=True)
        if norm_domain in ("backend", "frontend", "security"):
            selected_domains.add(norm_domain)

    if agent:
        agent_dom = infer_domain_from_agent(agent)
        if agent_dom and agent_dom != "universal":
            selected_domains.add(agent_dom)

    if task:
        task_doms = infer_domain_from_task(task)
        selected_domains.update(task_doms)

    for dom in selected_domains:
        tier_key = f"tier_1_{dom}"
        if tier_key in tiers:
            active_rule_ids.update(tiers[tier_key].get("rule_ids", []))

    return sorted(list(active_rule_ids))


def get_active_rules_metadata(
    domain: Optional[str] = None,
    agent: Optional[str] = None,
    task: Optional[str] = None,
    include_all: bool = False,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    matrix = load_rules_matrix(root)
    rule_ids = resolve_rule_ids(matrix, domain=domain, agent=agent, task=task, include_all=include_all)
    rules_dict = matrix.get("rules", {})
    
    selected_rules: Dict[str, Dict[str, Any]] = {}
    for r_id in rule_ids:
        r_str = str(r_id)
        if r_str in rules_dict:
            selected_rules[r_str] = rules_dict[r_str]
        else:
            selected_rules[r_str] = {"title": f"kural {r_id}", "scope": "unknown", "summary": ""}

    return {
        "active_rule_ids": rule_ids,
        "count": len(rule_ids),
        "total_rules": len(rules_dict),
        "token_reduction_percent": round((1.0 - (len(rule_ids) / max(len(rules_dict), 1))) * 100, 1),
        "rules": selected_rules,
    }


def render_markdown_prompt(
    domain: Optional[str] = None,
    agent: Optional[str] = None,
    task: Optional[str] = None,
    include_all: bool = False,
    root: Optional[Path] = None,
) -> str:
    data = get_active_rules_metadata(domain=domain, agent=agent, task=task, include_all=include_all, root=root)
    rule_ids = data["active_rule_ids"]
    rules = data["rules"]

    lines = [
        f"### 🛡️ aktif kural matrisi (tier-based active rules: {data['count']}/{data['total_rules']} kurallar - %{data['token_reduction_percent']} token tasarrufu)\n"
    ]
    for r_id in rule_ids:
        r_str = str(r_id)
        info = rules.get(r_str, {})
        title = info.get("title", f"kural {r_id}")
        summary = info.get("summary", "")
        lines.append(f"- **{r_id}. kural ({title}):** {summary}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Tier-based Dynamic Rule Matrix Dispatcher")
    parser.add_argument("--domain", choices=["backend", "frontend", "security", "universal", "all"], help="Filter by domain")
    parser.add_argument("--agent", help="Filter by agent persona (e.g. frontend-specialist)")
    parser.add_argument("--task", help="Filter by task description or keywords")
    parser.add_argument("--all", action="store_true", help="Include all 48 rules")
    parser.add_argument("--format", choices=["markdown", "json", "ids", "summary"], default="markdown", help="Output format")
    args = parser.parse_args()

    try:
        if args.format == "ids":
            matrix = load_rules_matrix()
            ids = resolve_rule_ids(matrix, domain=args.domain, agent=args.agent, task=args.task, include_all=args.all)
            print(",".join(map(str, ids)))
        elif args.format == "json":
            meta = get_active_rules_metadata(domain=args.domain, agent=args.agent, task=args.task, include_all=args.all)
            print(json.dumps(meta, ensure_ascii=False, indent=2))
        elif args.format == "summary":
            meta = get_active_rules_metadata(domain=args.domain, agent=args.agent, task=args.task, include_all=args.all)
            print(f"Aktif Kural Sayısı: {meta['count']}/{meta['total_rules']} (Tasarruf: %{meta['token_reduction_percent']})")
            print(f"Kural ID'leri: {meta['active_rule_ids']}")
        else:
            print(render_markdown_prompt(domain=args.domain, agent=args.agent, task=args.task, include_all=args.all))
        return 0
    except Exception as e:
        print(f"Hata: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

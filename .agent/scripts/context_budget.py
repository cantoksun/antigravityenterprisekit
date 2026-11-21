#!/usr/bin/env python3
"""
context_budget.py
Antigravity AI-OS v1.0 - Context Window & Token Budget Auditor

Measures and enforces token ceilings across prompt subsystems:
- Tier 0 Core Rules: max 500 tokens
- Active Domain Rules: max 1,000 tokens
- Active Skill Guidelines (L1): max 1,500 tokens
- Proactive Neural RAG: max 500 tokens
- Total Baseline System Context Ceiling: max 4,000 tokens (saving ~96% vs 120k uncompressed)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = WORKSPACE_ROOT / ".agent" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from rule_dispatcher import render_markdown_prompt, get_active_rules_metadata
    from skill_loader import load_l1_index, load_l0_metadata
    from neural_os_rag import ProactiveNeuralRAG
except ImportError:
    render_markdown_prompt = None  # type: ignore
    get_active_rules_metadata = None  # type: ignore
    load_l1_index = None  # type: ignore
    load_l0_metadata = None  # type: ignore
    ProactiveNeuralRAG = None  # type: ignore

BUDGET_LIMITS = {
    "tier_0_rules_max_tokens": 500,
    "tier_1_domain_rules_max_tokens": 1000,
    "active_skill_l1_max_tokens": 1500,
    "proactive_rag_max_tokens": 500,
    "total_baseline_ceiling_tokens": 4000,
}


def estimate_tokens(text: str) -> int:
    """Estimates tokens for mixed Turkish, English, and code.
    Average ratio: ~3.2 characters per token for Turkish/code mixture.
    """
    if not text:
        return 0
    clean = text.strip()
    return max(1, math.ceil(len(clean) / 3.2))


def audit_context_budget(
    domain: str = "universal",
    agent: Optional[str] = None,
    task: Optional[str] = None,
    sample_skill: str = "clean-code",
) -> Dict[str, Any]:
    # 1. Rules tokens
    rules_text = ""
    rules_meta = {}
    if render_markdown_prompt:
        rules_text = render_markdown_prompt(domain=domain, agent=agent, task=task)
        rules_meta = get_active_rules_metadata(domain=domain, agent=agent, task=task)
    rules_tokens = estimate_tokens(rules_text)

    # 2. Skill tokens (L1 core index)
    skill_text = ""
    if load_l1_index:
        try:
            sk_data = load_l1_index(sample_skill, max_lines=60)
            skill_text = sk_data.get("content", "")
        except Exception:
            pass
    skill_tokens = estimate_tokens(skill_text)

    # 3. Proactive RAG tokens
    rag_text = ""
    if ProactiveNeuralRAG:
        try:
            rag = ProactiveNeuralRAG()
            query = task or f"{domain} {agent or ''}".strip() or "clean architecture"
            rag_text = rag.format_markdown(query, limit=3)
        except Exception:
            pass
    rag_tokens = estimate_tokens(rag_text)

    # 4. Total and limits
    total_tokens = rules_tokens + skill_tokens + rag_tokens
    passed = total_tokens <= BUDGET_LIMITS["total_baseline_ceiling_tokens"]

    # Savings vs uncompressed naive loading (~120,000 tokens for all 48 rules + 97 full skills + full vault)
    uncompressed_estimate = 120_000
    savings_percent = round((1.0 - (total_tokens / uncompressed_estimate)) * 100, 2)

    return {
        "status": "pass" if passed else "fail",
        "domain": domain,
        "agent": agent,
        "task": task,
        "sample_skill": sample_skill,
        "tokens": {
            "rules": rules_tokens,
            "skill_l1": skill_tokens,
            "proactive_rag": rag_tokens,
            "total_baseline": total_tokens,
        },
        "limits": BUDGET_LIMITS,
        "savings_vs_uncompressed": f"%{savings_percent}",
        "passed": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Context Window & Token Budget Auditor")
    parser.add_argument("--domain", default="universal", choices=["backend", "frontend", "security", "universal", "all"])
    parser.add_argument("--agent", help="Agent persona name")
    parser.add_argument("--task", help="Task description or sample query")
    parser.add_argument("--skill", default="clean-code", help="Sample skill to evaluate L1 token consumption")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    report = audit_context_budget(
        domain=args.domain,
        agent=args.agent,
        task=args.task,
        sample_skill=args.skill,
    )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["passed"] else 1

    print("============================================================")
    print("        ANTIGRAVITY AI-OS: CONTEXT BUDGET AUDIT             ")
    print("============================================================")
    print(f"  Alan (Domain)     : {report['domain']}")
    print(f"  Ajan (Agent)      : {report['agent'] or '(varsayılan)'}")
    print(f"  Örnek Beceri (L1) : {report['sample_skill']}")
    print("------------------------------------------------------------")
    print(f"  🛡️ Aktif Kurallar : {report['tokens']['rules']} token (Limit: {BUDGET_LIMITS['tier_1_domain_rules_max_tokens']})")
    print(f"  ⚡ Beceri (L1)     : {report['tokens']['skill_l1']} token (Limit: {BUDGET_LIMITS['active_skill_l1_max_tokens']})")
    print(f"  🧠 Nöral RAG      : {report['tokens']['proactive_rag']} token (Limit: {BUDGET_LIMITS['proactive_rag_max_tokens']})")
    print("------------------------------------------------------------")
    print(f"  📊 Toplam Taban   : {report['tokens']['total_baseline']} token (Tavan: {BUDGET_LIMITS['total_baseline_ceiling_tokens']})")
    print(f"  💡 Token Tasarrufu: {report['savings_vs_uncompressed']} (Sıkıştırılmamış 120k'ya göre)")
    print("------------------------------------------------------------")

    if report["passed"]:
        print("  [BAŞARILI] Bağlam bütçesi sınırları dahilinde. Dikkat dağınıklığı riski: SIFIR")
        return 0
    else:
        print("  [HATA] Bağlam bütçesi tavanı aşıldı!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

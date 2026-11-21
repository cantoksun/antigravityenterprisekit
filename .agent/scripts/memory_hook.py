#!/usr/bin/env python3
"""Hook script that runs automatically on key agent milestones
to log episodic memory and update the neural knowledge vault.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from neural_memory import NeuralVault


def log_milestone(title: str, summary: str, related_nodes: list[str] | None = None) -> None:
    vault = NeuralVault()
    path = vault.add_episode(title=title, summary=summary, related_nodes=related_nodes)
    print(f"✅ Nöral vault epizodu kaydedildi: {path.name}")
    
    # Audit graph to ensure high integrity
    report = vault.audit_graph()
    broken_count = len(report.get("broken_links", {}))
    if broken_count > 0:
        print(f"⚠️ Dikkat: Grafikte {broken_count} kırık bağlantı mevcut.")
    else:
        print(f"🌐 Grafik bütünlüğü kusursuz (Düğüm sayısı: {report.get('total_nodes', 0)}, Kırık bağlantı: 0)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity Memory Hook")
    parser.add_argument("--title", required=True, help="Milestone / task title")
    parser.add_argument("--summary", required=True, help="Summary of changes")
    parser.add_argument("--nodes", nargs="*", default=["clean-code-principles"], help="Related node IDs")
    args = parser.parse_args()

    log_milestone(args.title, args.summary, args.nodes)
    return 0


if __name__ == "__main__":
    sys.exit(main())

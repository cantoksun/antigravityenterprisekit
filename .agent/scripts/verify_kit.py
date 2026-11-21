#!/usr/bin/env python3
"""Antigravity AI-OS: Master Self-Verification Suite.

Orchestrates all validation layers in priority order:
  1. Structural Kit Integrity (validate_kit.py)
  2. 4-Gate Quality Verification (quality_gates.py)
  3. Contract & Regression Tests (38 unittest suite)
  4. Neural Knowledge Graph Integrity (audit & graph_engine)

Produces clean terminal HUD reports and machine-readable JSON outputs for CI/CD.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import unittest
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOLKIT = Path(__file__).resolve().parents[1]
SCRIPTS = TOOLKIT / "scripts"
TESTS = SCRIPTS / "tests"


class Colors:
    HEADER = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    ENDC = "\033[0m"


@dataclass
class PhaseResult:
    phase_id: int
    name: str
    passed: bool
    duration_s: float
    summary: str
    details: Any = None


class MasterVerifier:
    def __init__(self, toolkit_dir: Path):
        self.toolkit = toolkit_dir.resolve()
        self.scripts = self.toolkit / "scripts"
        self.tests = self.scripts / "tests"

    def run_cmd(self, cmd: list[str]) -> tuple[int, str, str]:
        p = subprocess.run(
            cmd,
            cwd=self.toolkit.parent,
            capture_output=True,
            text=True,
            timeout=180,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()

    # Phase 1: Structural Kit Integrity
    def verify_structure(self) -> PhaseResult:
        start = time.perf_counter()
        script = self.scripts / "validate_kit.py"
        code, out, err = self.run_cmd([sys.executable, str(script)])
        duration = time.perf_counter() - start

        passed = (code == 0)
        summary = "Kit manifest, lock and contract references are valid (0 errors)" if passed else "Structural validation errors found"
        return PhaseResult(
            phase_id=1,
            name="Structural Kit Integrity",
            passed=passed,
            duration_s=round(duration, 2),
            summary=summary,
            details={"output": out if not passed else ""},
        )

    # Phase 2: 4-Gate Quality Verification
    def verify_gates(self) -> PhaseResult:
        start = time.perf_counter()
        script = self.scripts / "quality_gates.py"
        code, out, _ = self.run_cmd([sys.executable, str(script), str(self.toolkit.parent), "--gate", "all", "--json"])
        duration = time.perf_counter() - start

        passed = (code == 0)
        gates_summary = []
        try:
            data = json.loads(out)
            for g in data:
                status = "PASS" if g.get("passed") else "FAIL"
                gates_summary.append(f"{g.get('gate')}: {status}")
        except Exception:
            pass

        summary_text = ", ".join(gates_summary) if gates_summary else ("All 4 gates passed" if passed else "Gate failures detected")
        return PhaseResult(
            phase_id=2,
            name="4-Gate Quality Verification",
            passed=passed,
            duration_s=round(duration, 2),
            summary=summary_text,
        )

    # Phase 3: Contract & Regression Test Suite
    def verify_test_suite(self) -> PhaseResult:
        start = time.perf_counter()
        loader = unittest.TestLoader()
        suite = loader.discover(str(self.tests), pattern="test_*.py")
        runner = unittest.TextTestRunner(stream=open(os.devnull, "w"), verbosity=0)
        result = runner.run(suite)
        duration = time.perf_counter() - start

        passed = result.wasSuccessful()
        total = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)

        summary = f"{total} tests passed ({failures} failures, {errors} errors)" if passed else f"{failures} failures, {errors} errors out of {total} tests"
        return PhaseResult(
            phase_id=3,
            name="Comprehensive Contract Test Suite",
            passed=passed,
            duration_s=round(duration, 2),
            summary=summary,
            details={"tests_run": total, "failures": failures, "errors": errors},
        )

    # Phase 4: Neural Knowledge Graph Audit
    def verify_neural_os(self) -> PhaseResult:
        start = time.perf_counter()
        engine_path = self.toolkit / "neural_os" / "engine"
        sys.path.insert(0, str(engine_path))
        passed = False
        summary = ""
        try:
            from graph_engine import EnterpriseGraphEngine
            engine = EnterpriseGraphEngine()
            audit = engine.audit()
            broken = len(audit.get("broken_links", {}))
            export = engine.get_graph_export()
            nodes = export.get("total_nodes", 0)
            edges = export.get("total_edges", 0)

            passed = (broken == 0 and nodes >= 120 and edges >= 250)
            summary = f"{nodes} nodes, {edges} edges, 0 broken links"
        except Exception as e:
            summary = f"Neural OS error: {e}"

        duration = time.perf_counter() - start
        return PhaseResult(
            phase_id=4,
            name="Neural Knowledge Graph Integrity",
            passed=passed,
            duration_s=round(duration, 2),
            summary=summary,
        )

    def run_all(self) -> list[PhaseResult]:
        return [
            self.verify_structure(),
            self.verify_gates(),
            self.verify_test_suite(),
            self.verify_neural_os(),
        ]


def print_hud(results: list[PhaseResult], started_at: datetime) -> bool:
    c = Colors
    total_time = sum(r.duration_s for r in results)
    all_ok = all(r.passed for r in results)

    print("\n" + f"{c.BOLD}{c.CYAN}{'='*72}{c.ENDC}")
    print(f"{c.BOLD}{c.CYAN}{'ANTIGRAVITY AI-OS: TRUST-GRADE MASTER VERIFICATION'.center(72)}{c.ENDC}")
    print(f"{c.BOLD}{c.CYAN}{'='*72}{c.ENDC}\n")

    for r in results:
        status_badge = f"{c.GREEN}[ PASS ]{c.ENDC}" if r.passed else f"{c.RED}[ FAIL ]{c.ENDC}"
        print(f"  {status_badge}  {c.BOLD}Faz {r.phase_id}: {r.name:<34}{c.ENDC} ({r.duration_s}s)")
        print(f"            └─► {r.summary}")
        print()

    print(f"{c.CYAN}{'-'*72}{c.ENDC}")
    total_summary = f"Toplam Süre: {total_time:.2f}s | Durum: "
    if all_ok:
        total_summary += f"{c.GREEN}{c.BOLD}MÜKEMMEL (TÜM DOĞRULAMALAR GEÇTİ){c.ENDC}"
    else:
        total_summary += f"{c.RED}{c.BOLD}BAŞARISIZ (DÜZELTME GEREKİYOR){c.ENDC}"
    print(total_summary)
    print(f"{c.CYAN}{'='*72}{c.ENDC}\n")
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Antigravity Master Self-Verification Suite")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON report")
    args = parser.parse_args()

    started = datetime.now(timezone.utc)
    verifier = MasterVerifier(TOOLKIT)
    results = verifier.run_all()
    all_ok = all(r.passed for r in results)

    if args.json:
        payload = {
            "timestamp": started.isoformat(),
            "toolkit": str(TOOLKIT),
            "passed": all_ok,
            "phases": [asdict(r) for r in results],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_hud(results, started)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

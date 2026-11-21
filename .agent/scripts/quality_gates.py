#!/usr/bin/env python3
"""Antigravity Quality Gates Engine (besync-labs standard aligned).

Implements the 4-Gate Verification System:
  1. session-start : environment health, toolkit manifest, neural vault status
  2. pre-commit    : secrets scanning, supply chain lockfiles, code linting
  3. task-complete : core constitution rules (idor, rls, idempotency, tests, ux)
  4. session-end   : workspace hygiene (auto-teardown), graph preview sync
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# Color formatting
class GateColors:
    HEADER = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


@dataclass
class GateCheckResult:
    name: str
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info
    duration_s: float = 0.0


@dataclass
class GateReport:
    gate: str
    project: str
    timestamp: str
    passed: bool
    checks: list[GateCheckResult]


class QualityGatesEngine:
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()
        self.toolkit_root = self._locate_toolkit()

    def _locate_toolkit(self) -> Path:
        for candidate in (self.project_path / ".agent", self.project_path / ".agents", self.project_path):
            if (candidate / "scripts").is_dir() and (candidate / "skills").is_dir():
                return candidate
        return self.project_path / ".agent"

    def run_command(self, cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
        try:
            p = subprocess.run(
                cmd,
                cwd=cwd or self.project_path,
                capture_output=True,
                text=True,
                timeout=120,
            )
            return p.returncode, p.stdout.strip(), p.stderr.strip()
        except Exception as e:
            return 1, "", str(e)

    # -------------------------------------------------------------
    # GATE 1: session-start
    # -------------------------------------------------------------
    def run_session_start(self) -> GateReport:
        checks: list[GateCheckResult] = []

        # 1.1 Python version
        py_ver = sys.version_info
        py_pass = py_ver >= (3, 10)
        checks.append(GateCheckResult(
            name="Python Environment (>= 3.10)",
            passed=py_pass,
            message=f"Python {py_ver.major}.{py_ver.minor}.{py_ver.micro}",
            severity="error",
        ))

        # 1.2 Toolkit structural validity
        val_script = self.toolkit_root / "scripts" / "validate_kit.py"
        if val_script.is_file():
            code, out, _ = self.run_command([sys.executable, str(val_script)])
            checks.append(GateCheckResult(
                name="Toolkit Manifest Integrity (validate_kit)",
                passed=code == 0,
                message="Manifest and contract definitions are valid" if code == 0 else "Validation errors found",
                severity="error",
            ))

        # 1.3 Neural Vault presence
        vault_idx = self.toolkit_root / "vault" / "INDEX.md"
        checks.append(GateCheckResult(
            name="Neural Vault Core (INDEX.md)",
            passed=vault_idx.is_file(),
            message="Vault root index present" if vault_idx.is_file() else "Missing .agent/vault/INDEX.md",
            severity="warning",
        ))

        passed = all(c.passed for c in checks if c.severity == "error")
        return GateReport(
            gate="session-start",
            project=str(self.project_path),
            timestamp=datetime.now(timezone.utc).isoformat(),
            passed=passed,
            checks=checks,
        )

    # -------------------------------------------------------------
    # GATE 2: pre-commit
    # -------------------------------------------------------------
    def run_pre_commit(self) -> GateReport:
        checks: list[GateCheckResult] = []

        # 2.1 Secret Scanning
        sec_script = self.toolkit_root / "skills" / "vulnerability-scanner" / "scripts" / "security_scan.py"
        if sec_script.is_file():
            code, out, _ = self.run_command([sys.executable, str(sec_script), str(self.project_path), "--scan-type", "secrets"])
            no_secrets = True
            try:
                data = json.loads(out)
                crit = data.get("summary", {}).get("critical", 0)
                high = data.get("summary", {}).get("high", 0)
                no_secrets = (crit == 0 and high == 0)
            except Exception:
                no_secrets = (code == 0)

            checks.append(GateCheckResult(
                name="Zero Secrets Policy (security_scan)",
                passed=no_secrets,
                message="No exposed API keys or tokens" if no_secrets else "Exposed secrets detected!",
                severity="error",
            ))

        # 2.2 Dependency Lockfile
        dep_script = self.toolkit_root / "skills" / "vulnerability-scanner" / "scripts" / "dependency_analyzer.py"
        if dep_script.is_file():
            code, out, _ = self.run_command([sys.executable, str(dep_script), str(self.project_path)])
            dep_pass = True
            try:
                data = json.loads(out)
                dep_pass = (data.get("status") == "pass")
            except Exception:
                dep_pass = (code == 0)
            checks.append(GateCheckResult(
                name="Supply Chain Integrity (dependency_analyzer)",
                passed=dep_pass,
                message="Lockfiles and package bounds valid" if dep_pass else "Missing lockfile or unbounded deps",
                severity="warning",
            ))

        # 2.3 Root Hygiene (no stray task files)
        stray_mds = [p.name for p in self.project_path.glob("*.md") if p.name not in ("README.md", "CHANGELOG.md", "ARCHITECTURE.md", "LICENSE.md")]
        checks.append(GateCheckResult(
            name="Workspace Root Hygiene",
            passed=len(stray_mds) == 0,
            message="Root clean" if len(stray_mds) == 0 else f"Stray task files in root: {stray_mds}",
            severity="warning",
        ))

        passed = all(c.passed for c in checks if c.severity == "error")
        return GateReport(
            gate="pre-commit",
            project=str(self.project_path),
            timestamp=datetime.now(timezone.utc).isoformat(),
            passed=passed,
            checks=checks,
        )

    # -------------------------------------------------------------
    # GATE 3: task-complete
    # -------------------------------------------------------------
    def run_task_complete(self) -> GateReport:
        checks: list[GateCheckResult] = []

        # 3.1 Code Linting
        lint_script = self.toolkit_root / "skills" / "lint-and-validate" / "scripts" / "lint_runner.py"
        if lint_script.is_file():
            code, _, _ = self.run_command([sys.executable, str(lint_script), str(self.project_path)])
            checks.append(GateCheckResult(
                name="Lint & Syntax Audit (lint_runner)",
                passed=(code == 0),
                message="Clean syntax" if code == 0 else "Lint errors detected",
                severity="error",
            ))

        # 3.2 Security Patterns (OWASP, IDOR, Injection)
        sec_script = self.toolkit_root / "skills" / "vulnerability-scanner" / "scripts" / "security_scan.py"
        if sec_script.is_file():
            code, out, _ = self.run_command([sys.executable, str(sec_script), str(self.project_path), "--scan-type", "patterns"])
            crit = 0
            try:
                data = json.loads(out)
                crit = data.get("summary", {}).get("critical", 0)
            except Exception:
                pass
            checks.append(GateCheckResult(
                name="Security Patterns & Injection (OWASP A05)",
                passed=(crit == 0),
                message="No dangerous code patterns" if crit == 0 else f"{crit} critical patterns found",
                severity="error",
            ))

        # 3.3 Unit & Regression Tests
        test_script = self.toolkit_root / "scripts" / "tests" / "test_toolkit.py"
        if test_script.is_file():
            code, _, _ = self.run_command([sys.executable, str(test_script)])
            checks.append(GateCheckResult(
                name="Regression Test Suite (test_toolkit)",
                passed=(code == 0),
                message="All regression tests passed" if code == 0 else "Test failures detected",
                severity="error",
            ))

        # 3.4 UX & Accessibility (if applicable)
        ux_script = self.toolkit_root / "skills" / "frontend-design" / "scripts" / "ux_audit.py"
        if ux_script.is_file():
            code, out, _ = self.run_command([sys.executable, str(ux_script), str(self.project_path)])
            checks.append(GateCheckResult(
                name="UX & Design Integrity (ux_audit)",
                passed=(code == 0),
                message="UX guidelines satisfied" if code == 0 else "UX warnings detected",
                severity="warning",
            ))

        passed = all(c.passed for c in checks if c.severity == "error")
        return GateReport(
            gate="task-complete",
            project=str(self.project_path),
            timestamp=datetime.now(timezone.utc).isoformat(),
            passed=passed,
            checks=checks,
        )

    # -------------------------------------------------------------
    # GATE 4: session-end
    # -------------------------------------------------------------
    def run_session_end(self) -> GateReport:
        checks: list[GateCheckResult] = []

        # 4.1 Auto-Teardown (Rule 45): Temporary and orphan test scripts
        temp_patterns = ["test_*.tmp", "*_scratch.*", "*.py.tmp"]
        found_temps = []
        for pat in temp_patterns:
            found_temps.extend([p.name for p in self.project_path.glob(pat)])
        checks.append(GateCheckResult(
            name="Auto-Teardown & Process Hygiene (Rule 45)",
            passed=len(found_temps) == 0,
            message="No orphan temp files" if len(found_temps) == 0 else f"Found temp files: {found_temps}",
            severity="warning",
        ))

        # 4.2 Graph Preview Freshness (Rule 48)
        preview_html = self.toolkit_root / "neural_os" / "ui" / "graph-preview.html"
        checks.append(GateCheckResult(
            name="Neural Graph Preview Freshness (Rule 48)",
            passed=preview_html.is_file() and preview_html.stat().st_size > 500_000,
            message="Standalone graph preview ready" if preview_html.is_file() else "Missing or empty graph preview",
            severity="info",
        ))

        # 4.3 Git Working Tree Cleanliness
        code, out, _ = self.run_command(["git", "status", "--porcelain"])
        is_clean = (out.strip() == "")
        checks.append(GateCheckResult(
            name="Git Working Tree Cleanliness",
            passed=is_clean,
            message="Working tree clean" if is_clean else f"Uncommitted modifications present ({len(out.splitlines())} items)",
            severity="info",
        ))

        passed = all(c.passed for c in checks if c.severity == "error")
        return GateReport(
            gate="session-end",
            project=str(self.project_path),
            timestamp=datetime.now(timezone.utc).isoformat(),
            passed=passed,
            checks=checks,
        )

    # -------------------------------------------------------------
    # Dispatcher
    # -------------------------------------------------------------
    def execute_gate(self, gate_name: str) -> GateReport:
        dispatch: dict[str, Callable[[], GateReport]] = {
            "session-start": self.run_session_start,
            "pre-commit": self.run_pre_commit,
            "task-complete": self.run_task_complete,
            "session-end": self.run_session_end,
        }
        if gate_name not in dispatch:
            raise ValueError(f"Unknown gate: '{gate_name}'. Supported gates: {list(dispatch.keys())}")
        return dispatch[gate_name]()

    def execute_all_gates(self) -> list[GateReport]:
        return [
            self.run_session_start(),
            self.run_pre_commit(),
            self.run_task_complete(),
            self.run_session_end(),
        ]


def print_gate_report(report: GateReport) -> bool:
    c = GateColors
    line = "=" * 65
    print(f"\n{c.BOLD}{c.CYAN}{line}")
    print(f" QUALITY GATE: {report.gate.upper()} ")
    print(f"{line}{c.ENDC}")
    print(f"Timestamp: {report.timestamp}")
    print(f"Status: {c.GREEN + 'PASSED' if report.passed else c.RED + 'FAILED'}{c.ENDC}\n")

    for check in report.checks:
        if check.passed:
            mark = f"{c.GREEN}[PASS]{c.ENDC}"
        elif check.severity == "warning":
            mark = f"{c.YELLOW}[WARN]{c.ENDC}"
        elif check.severity == "info":
            mark = f"{c.CYAN}[INFO]{c.ENDC}"
        else:
            mark = f"{c.RED}[FAIL]{c.ENDC}"
        print(f"  {mark} {check.name}: {check.message}")

    print(f"\n{c.BOLD}{c.CYAN}{'-' * 65}{c.ENDC}")
    return report.passed


def main():
    parser = argparse.ArgumentParser(description="Antigravity Quality Gates Runner (4-Gate Architecture)")
    parser.add_argument("project", nargs="?", default=".", help="Project path to inspect")
    parser.add_argument(
        "--gate",
        choices=["session-start", "pre-commit", "task-complete", "session-end", "all"],
        default="all",
        help="Quality gate stage to evaluate",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    engine = QualityGatesEngine(Path(args.project))

    if args.gate == "all":
        reports = engine.execute_all_gates()
        if args.json:
            print(json.dumps([asdict(r) for r in reports], indent=2))
        else:
            all_ok = True
            for r in reports:
                if not print_gate_report(r):
                    all_ok = False
            sys.exit(0 if all_ok else 1)
    else:
        report = engine.execute_gate(args.gate)
        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            ok = print_gate_report(report)
            sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

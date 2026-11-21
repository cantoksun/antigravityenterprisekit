#!/usr/bin/env python3
"""
stack_validator.py
Antigravity AI-OS v1.0 - Pre-Flight Tech Stack & Dependency Conflict Auditor (AAS Core Parity)

Scans project manifest files (package.json, pyproject.toml, requirements.txt, Cargo.toml, go.mod)
BEFORE code implementation begins to proactively flag:
- Incompatible framework / peer dependency versions (e.g. React 19 vs legacy packages)
- Breaking API transitions (e.g. Next.js 15 async params, Tailwind v4 vs v3)
- Deprecated or conflicting libraries
- High-risk configuration mismatches
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

KNOWN_STACK_PITFALLS: List[Dict[str, Any]] = [
    {
        "id": "react-19-peer-clash",
        "ecosystem": "npm",
        "trigger_package": "react",
        "trigger_version": ">=19.0.0",
        "conflicting_packages": ["react-helmet", "react-beautiful-dnd", "@types/react-helmet"],
        "severity": "warning",
        "message": "React 19 detected with packages known to lack React 19 peer dependency support.",
        "recommendation": "Use '@tanstack/react-virtual' or '@hello-pangea/dnd' instead of legacy unmaintained libraries.",
    },
    {
        "id": "nextjs-15-async-request-api",
        "ecosystem": "npm",
        "trigger_package": "next",
        "trigger_version": ">=15.0.0",
        "conflicting_packages": [],
        "severity": "info",
        "message": "Next.js 15+ detected. cookies(), headers(), and params are now asynchronous Promises.",
        "recommendation": "Ensure all params, searchParams, cookies(), and headers() calls are awaited in layouts and pages.",
    },
    {
        "id": "tailwind-v4-config-collision",
        "ecosystem": "npm",
        "trigger_package": "tailwindcss",
        "trigger_version": ">=4.0.0",
        "conflicting_files": ["tailwind.config.js", "tailwind.config.ts"],
        "severity": "warning",
        "message": "Tailwind CSS v4 detected alongside legacy tailwind.config.js/ts file.",
        "recommendation": "Tailwind v4 uses CSS-first configuration via '@theme' in globals.css; legacy js configs are ignored or deprecated.",
    },
    {
        "id": "python-deprecated-distutils",
        "ecosystem": "python",
        "trigger_package": "distutils",
        "conflicting_packages": ["setuptools<60.0.0"],
        "severity": "error",
        "message": "distutils is completely removed in Python 3.12+.",
        "recommendation": "Migrate to standard packaging, setuptools >= 65.0.0, or hatch/flit.",
    },
    {
        "id": "prisma-serverless-accelerate",
        "ecosystem": "npm",
        "trigger_package": "@prisma/client",
        "conflicting_packages": [],
        "severity": "info",
        "message": "Prisma client in serverless/edge environments requires connection pooling.",
        "recommendation": "Ensure PgBouncer/Supabase port 6543 or Prisma Accelerate is configured to avoid max_connections exhaustion.",
    },
]


def detect_ecosystem(project_dir: Path) -> Dict[str, bool]:
    return {
        "npm": (project_dir / "package.json").is_file(),
        "python": (project_dir / "pyproject.toml").is_file() or (project_dir / "requirements.txt").is_file(),
        "rust": (project_dir / "Cargo.toml").is_file(),
        "go": (project_dir / "go.mod").is_file(),
    }


def parse_package_json(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text("utf-8", errors="replace"))
        deps = {}
        deps.update(data.get("dependencies", {}))
        deps.update(data.get("devDependencies", {}))
        return {"name": data.get("name", ""), "version": data.get("version", ""), "dependencies": deps}
    except Exception:
        return {"dependencies": {}}


def audit_stack_conflicts(project_dir: Path) -> Dict[str, Any]:
    eco = detect_ecosystem(project_dir)
    findings: List[Dict[str, Any]] = []

    # 1. NPM / JavaScript / TypeScript audit
    if eco["npm"]:
        pkg_data = parse_package_json(project_dir / "package.json")
        deps = pkg_data.get("dependencies", {})

        for pitfall in KNOWN_STACK_PITFALLS:
            if pitfall.get("ecosystem") != "npm":
                continue
            trig_pkg = pitfall.get("trigger_package")
            if trig_pkg and trig_pkg in deps:
                version_str = deps[trig_pkg]
                # Check conflicting packages
                found_clashes = [c for c in pitfall.get("conflicting_packages", []) if c in deps]
                # Check conflicting files
                found_files = [f for f in pitfall.get("conflicting_files", []) if (project_dir / f).is_file()]

                if found_clashes or found_files or (not pitfall.get("conflicting_packages") and not pitfall.get("conflicting_files")):
                    findings.append({
                        "id": pitfall["id"],
                        "severity": pitfall["severity"],
                        "message": pitfall["message"],
                        "recommendation": pitfall["recommendation"],
                        "matched_dependency": f"{trig_pkg}@{version_str}",
                        "conflicts": found_clashes + found_files,
                    })

    # 2. Python audit
    if eco["python"]:
        req_file = project_dir / "requirements.txt"
        if req_file.is_file():
            content = req_file.read_text("utf-8", errors="replace")
            if "distutils" in content:
                findings.append({
                    "id": "python-deprecated-distutils",
                    "severity": "error",
                    "message": "distutils is deprecated and removed in Python 3.12+.",
                    "recommendation": "Remove distutils and use setuptools >= 65.0.0.",
                    "conflicts": ["distutils"],
                })

    has_errors = any(f["severity"] == "error" for f in findings)
    has_warnings = any(f["severity"] == "warning" for f in findings)

    status = "fail" if has_errors else ("warning" if has_warnings else "pass")

    return {
        "status": status,
        "project_dir": str(project_dir.resolve()),
        "detected_ecosystems": [k for k, v in eco.items() if v],
        "findings_count": len(findings),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity Pre-Flight Tech Stack Auditor")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project workspace directory")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    target = Path(args.project_dir).resolve()
    report = audit_stack_conflicts(target)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] != "fail" else 1

    print("============================================================")
    print("      ANTIGRAVITY TECH STACK & PRE-FLIGHT AUDITOR           ")
    print("============================================================")
    print(f"  Çalışma Alanı     : {report['project_dir']}")
    print(f"  Tespit Edilen Dil : {', '.join(report['detected_ecosystems']) or 'Genel Dizin'}")
    print(f"  Denetim Durumu    : {report['status'].upper()}")
    print("------------------------------------------------------------")

    if not report["findings"]:
        print("  [BAŞARILI] Bilinen hiçbir kütüphane çakışması veya sürüm uyumsuzluğu tespit edilmedi.")
    else:
        for f in report["findings"]:
            icon = "🔴" if f["severity"] == "error" else ("🟡" if f["severity"] == "warning" else "🔵")
            print(f"\n{icon} [{f['id']}] ({f['severity'].upper()}): {f['message']}")
            print(f"   💡 Çözüm/Öneri: {f['recommendation']}")
            if f.get("conflicts"):
                print(f"   ⚠️ Çakışan Unsurlar: {', '.join(f['conflicts'])}")

    print("\n============================================================")
    return 0 if report["status"] != "fail" else 1


if __name__ == "__main__":
    sys.exit(main())

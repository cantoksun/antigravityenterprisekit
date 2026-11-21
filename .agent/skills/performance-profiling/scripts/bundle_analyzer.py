#!/usr/bin/env python3
"""Asset and bundle size performance analyzer.

Inspects distribution and build directories to detect oversized assets,
prevent bundle bloat, and uphold Core Web Vitals performance standards.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def analyze(
    root: Path,
    file_warn_kib: float = 250.0,
    file_fail_kib: float = 500.0,
    total_fail_kib: float = 2000.0,
) -> dict[str, Any]:
    root = Path(root).resolve()
    findings: list[dict[str, Any]] = []
    asset_dirs = [root / "dist", root / "build", root / ".next/static", root / "out"]

    total_size_bytes = 0
    scanned_files = 0

    for adir in asset_dirs:
        if not adir.is_dir():
            continue
        for path in adir.rglob("*"):
            if not path.is_file():
                continue
            # Skip maps and manifest metadata
            if path.suffix in (".map", ".json", ".txt"):
                continue

            size_bytes = path.stat().st_size
            total_size_bytes += size_bytes
            scanned_files += 1

            size_kib = size_bytes / 1024.0
            if size_kib >= file_fail_kib:
                findings.append({
                    "file": path.relative_to(root).as_posix(),
                    "size_kib": round(size_kib, 2),
                    "threshold_kib": file_fail_kib,
                    "severity": "high",
                    "issue": f"Oversized asset ({round(size_kib, 1)} KiB >= {file_fail_kib} KiB threshold)",
                })
            elif size_kib >= file_warn_kib:
                findings.append({
                    "file": path.relative_to(root).as_posix(),
                    "size_kib": round(size_kib, 2),
                    "threshold_kib": file_warn_kib,
                    "severity": "medium",
                    "issue": f"Large asset ({round(size_kib, 1)} KiB >= {file_warn_kib} KiB threshold)",
                })

    total_kib = total_size_bytes / 1024.0
    if total_kib >= total_fail_kib:
        findings.append({
            "file": "total_bundle",
            "size_kib": round(total_kib, 2),
            "threshold_kib": total_fail_kib,
            "severity": "high",
            "issue": f"Total bundle size exceeded ({round(total_kib, 1)} KiB >= {total_fail_kib} KiB threshold)",
        })

    return {
        "status": "fail" if any(f["severity"] == "high" for f in findings) else "pass",
        "scanned_files": scanned_files,
        "total_bundle_kib": round(total_kib, 2),
        "findings": findings,
    }


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    res = analyze(target)
    print(json.dumps(res, indent=2))

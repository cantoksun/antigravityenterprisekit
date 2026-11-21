#!/usr/bin/env python3
"""
skill_loader.py
Antigravity AI-OS v1.0 - Progressive Skill Loader (Aşamalı Beceri Yükleyici)

Implements progressive skill loading across 3 levels:
- L0: Metadata / Discovery (name + single-sentence description, ~25 tokens)
- L1: Core Index / SKILL.md (essential guidelines and section map, ~400 tokens)
- L2: On-Demand Deep Drill (specific script or reference file, only when requested)

Prevents massive context bloat and attention drift across 97+ skills.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_workspace_root() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / ".agent" / "skills").is_dir():
            return candidate
    file_root = Path(__file__).resolve().parent.parent.parent
    if (file_root / ".agent" / "skills").is_dir():
        return file_root
    return cwd


def extract_frontmatter(path: Path) -> Dict[str, str]:
    try:
        text = path.read_text("utf-8", errors="replace")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---\n", 3)
    if end < 0:
        end = text.find("\n---", 3)
    if end < 0:
        return {}
    raw = text[3:end]
    meta: Dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            k, v = match.groups()
            meta[k.strip()] = v.strip().strip('"\'')
    return meta


def list_skills(root: Optional[Path] = None) -> Dict[str, Dict[str, str]]:
    if root is None:
        root = find_workspace_root()
    skills_dir = root / ".agent" / "skills"
    if not skills_dir.is_dir():
        return {}

    registry: Dict[str, Dict[str, str]] = {}
    for skill_path in sorted(skills_dir.iterdir()):
        if skill_path.is_dir():
            skill_md = skill_path / "SKILL.md"
            if skill_md.is_file():
                meta = extract_frontmatter(skill_md)
                name = meta.get("name", skill_path.name)
                desc = meta.get("description", "")
                registry[skill_path.name] = {
                    "name": name,
                    "description": desc,
                    "path": str(skill_md),
                }
    return registry


def load_l0_metadata(skill_name: str, root: Optional[Path] = None) -> Dict[str, str]:
    if root is None:
        root = find_workspace_root()
    skill_dir = root / ".agent" / "skills" / skill_name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"Skill not found: {skill_name} at {skill_md}")
    meta = extract_frontmatter(skill_md)
    return {
        "level": "L0",
        "skill": skill_name,
        "name": meta.get("name", skill_name),
        "description": meta.get("description", "Açıklama bulunamadı"),
    }


def load_l1_index(
    skill_name: str,
    max_lines: int = 150,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    if root is None:
        root = find_workspace_root()
    skill_dir = root / ".agent" / "skills" / skill_name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"Skill not found: {skill_name}")

    text = skill_md.read_text("utf-8", errors="replace")
    lines = text.splitlines()

    # Determine sub-resources if any
    resources = []
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for f in scripts_dir.iterdir():
            if f.is_file():
                resources.append(f"scripts/{f.name}")
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for f in refs_dir.iterdir():
            if f.is_file():
                resources.append(f"references/{f.name}")

    content = "\n".join(lines[:max_lines])
    is_truncated = len(lines) > max_lines

    return {
        "level": "L1",
        "skill": skill_name,
        "total_lines": len(lines),
        "returned_lines": min(len(lines), max_lines),
        "is_truncated": is_truncated,
        "available_l2_resources": resources,
        "content": content,
    }


def load_l2_resource(
    skill_name: str,
    rel_path: str,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    if root is None:
        root = find_workspace_root()
    skill_dir = root / ".agent" / "skills" / skill_name
    target = (skill_dir / rel_path).resolve()
    # Path traversal check
    if not str(target).startswith(str(skill_dir.resolve())):
        raise PermissionError("Access denied: path traversal attempt")
    if not target.is_file():
        raise FileNotFoundError(f"L2 Resource not found: {rel_path} in skill {skill_name}")

    content = target.read_text("utf-8", errors="replace")
    return {
        "level": "L2",
        "skill": skill_name,
        "resource": rel_path,
        "lines": len(content.splitlines()),
        "content": content,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Progressive Skill Loader (Aşamalı Beceri Yükleyici)")
    parser.add_argument("--list", action="store_true", help="List all skills (L0 index)")
    parser.add_argument("--skill", help="Name of the skill to load")
    parser.add_argument("--level", choices=["L0", "L1", "L2"], default="L0", help="Progressive detail level")
    parser.add_argument("--file", help="Relative file path for L2 resource")
    parser.add_argument("--max-lines", type=int, default=150, help="Max lines for L1")
    parser.add_argument("--format", choices=["json", "text", "markdown"], default="text", help="Output format")
    args = parser.parse_args()

    try:
        if args.list:
            registry = list_skills()
            if args.format == "json":
                print(json.dumps(registry, ensure_ascii=False, indent=2))
            else:
                print(f"Toplam {len(registry)} beceri bulundu:\n")
                for sk_name, info in registry.items():
                    print(f"- {sk_name}: {info['description']}")
            return 0

        if not args.skill:
            print("Hata: --skill parametresi gereklidir. Beceri listesi için --list kullanın.", file=sys.stderr)
            return 1

        if args.level == "L0":
            data = load_l0_metadata(args.skill)
            if args.format == "json":
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print(f"[L0 Beceri Keşfi] {data['skill']}: {data['description']}")
        elif args.level == "L1":
            data = load_l1_index(args.skill, max_lines=args.max_lines)
            if args.format == "json":
                print(json.dumps(data, ensure_ascii=False, indent=2))
            elif args.format == "markdown":
                print(f"### [L1 Çekirdek Dizin] `{data['skill']}` ({data['returned_lines']}/{data['total_lines']} satır)\n")
                if data["available_l2_resources"]:
                    print(f"**Mevcut L2 Kaynakları:** {', '.join(data['available_l2_resources'])}\n")
                print("```markdown")
                print(data["content"])
                print("```")
            else:
                print(data["content"])
        elif args.level == "L2":
            if not args.file:
                print("Hata: L2 seviyesi için --file belirtilmelidir.", file=sys.stderr)
                return 1
            data = load_l2_resource(args.skill, args.file)
            if args.format == "json":
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print(data["content"])
        return 0
    except Exception as e:
        print(f"Hata: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

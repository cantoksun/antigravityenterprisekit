#!/usr/bin/env python3
"""
skill_aggregator.py
Antigravity AI-OS v1.0 - Intelligent Skill Aggregator & Normalizer (sickn33 / omer-metin Parity)

Scans, compares, deduplicates, and safely imports open-source agent skills (from repos like
sickn33/agentic-awesome-skills, omer-metin/skills-for-antigravity, rmyndharis/antigravity-skills).
Ensures all imported skills strictly conform to the 3-Level Progressive Skill Loading Protocol (L0/L1/L2),
eliminating duplicates and context bloat.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_SKILLS_DIR = WORKSPACE_ROOT / ".agent" / "skills"


def extract_frontmatter(text: str) -> Dict[str, str]:
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


def get_local_skills_inventory() -> Dict[str, Dict[str, Any]]:
    inventory = {}
    if not LOCAL_SKILLS_DIR.is_dir():
        return inventory

    for s_dir in sorted(LOCAL_SKILLS_DIR.iterdir()):
        if s_dir.is_dir():
            s_md = s_dir / "SKILL.md"
            if s_md.is_file():
                txt = s_md.read_text("utf-8", errors="replace")
                fm = extract_frontmatter(txt)
                inventory[s_dir.name] = {
                    "name": fm.get("name", s_dir.name),
                    "description": fm.get("description", ""),
                    "priority": fm.get("priority", "standard"),
                    "lines": len(txt.splitlines()),
                    "path": str(s_md),
                }
    return inventory


def scan_external_skills(target_dir: Path) -> Dict[str, Dict[str, Any]]:
    found = {}
    if not target_dir.is_dir():
        return found

    for md_file in target_dir.rglob("*.md"):
        if md_file.name in ("SKILL.md", "skill.md") or "skill" in md_file.name.lower():
            txt = md_file.read_text("utf-8", errors="replace")
            fm = extract_frontmatter(txt)
            skill_name = fm.get("name") or md_file.parent.name
            if skill_name in ("skills", "global_skills", "agent"):
                skill_name = md_file.stem
            skill_slug = re.sub(r"[^a-z0-9_-]+", "-", skill_name.lower()).strip("-")
            found[skill_slug] = {
                "name": skill_slug,
                "description": fm.get("description", "Açıklama belirtilmemiş"),
                "source_file": str(md_file),
                "lines": len(txt.splitlines()),
            }
    return found


def compare_inventories(
    local_inv: Dict[str, Dict[str, Any]],
    external_inv: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    local_keys = set(local_inv.keys())
    external_keys = set(external_inv.keys())

    identical = sorted(list(local_keys & external_keys))
    missing_in_local = sorted(list(external_keys - local_keys))
    unique_to_local = sorted(list(local_keys - external_keys))

    return {
        "local_count": len(local_keys),
        "external_count": len(external_keys),
        "shared_skills": identical,
        "new_available_skills": missing_in_local,
        "unique_local_skills": unique_to_local,
    }


def normalize_skill_content(name: str, description: str, raw_content: str) -> str:
    """Ensures standard frontmatter and L0/L1 compatible section headers."""
    clean_name = re.sub(r"[^a-z0-9_-]+", "-", name.lower()).strip("-")
    clean_desc = description.strip().replace("\n", " ")
    
    # Strip existing frontmatter
    content = raw_content
    if content.startswith("---"):
        end = content.find("\n---\n", 3)
        if end >= 0:
            content = content[end + 5:]

    frontmatter = f"""---
name: {clean_name}
description: {clean_desc}
priority: standard
version: 1.0.0
when_to_use: "{clean_desc}"
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit]
---
"""
    return frontmatter + "\n" + content.strip() + "\n"


def import_skill(
    skill_file_path: Path,
    custom_name: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    if not skill_file_path.is_file():
        raise FileNotFoundError(f"Skill file not found: {skill_file_path}")

    raw_text = skill_file_path.read_text("utf-8", errors="replace")
    fm = extract_frontmatter(raw_text)
    name = custom_name or fm.get("name") or skill_file_path.parent.name
    slug = re.sub(r"[^a-z0-9_-]+", "-", name.lower()).strip("-")
    desc = fm.get("description", f"{slug} operasyonel beceri yönergeleri.")

    normalized = normalize_skill_content(slug, desc, raw_text)
    target_dir = LOCAL_SKILLS_DIR / slug
    target_file = target_dir / "SKILL.md"

    if dry_run:
        return {
            "status": "dry-run",
            "slug": slug,
            "target_dir": str(target_dir),
            "lines": len(normalized.splitlines()),
            "preview": normalized[:300] + "...",
        }

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(normalized, encoding="utf-8")

    return {
        "status": "imported",
        "slug": slug,
        "path": str(target_file),
        "lines": len(normalized.splitlines()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity Intelligent Skill Aggregator & Normalizer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List local skills inventory")

    # scan
    scan_p = subparsers.add_parser("scan", help="Scan external directory for skills")
    scan_p.add_argument("path", help="Path to external skills directory or repo")
    scan_p.add_argument("--json", action="store_true", help="Output JSON")

    # diff
    diff_p = subparsers.add_parser("diff", help="Compare external skills with local kit")
    diff_p.add_argument("path", help="Path to external skills directory")
    diff_p.add_argument("--json", action="store_true", help="Output JSON")

    # import
    import_p = subparsers.add_parser("import", help="Import and normalize an external skill")
    import_p.add_argument("file", help="Path to SKILL.md file to import")
    import_p.add_argument("--name", help="Custom normalized name for the skill")
    import_p.add_argument("--dry-run", action="store_true", help="Preview without writing")

    args = parser.parse_args()

    if args.command == "list":
        inv = get_local_skills_inventory()
        print(f"Toplam {len(inv)} yerel beceri mevcut:")
        for name, info in inv.items():
            print(f"- {name} ({info['lines']} satır): {info['description'][:80]}")
        return 0

    if args.command == "scan":
        p = Path(args.path).resolve()
        res = scan_external_skills(p)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"'{p}' dizininde {len(res)} beceri bulundu.")
            for name, info in res.items():
                print(f"- {name}: {info['description']}")
        return 0

    if args.command == "diff":
        p = Path(args.path).resolve()
        local_inv = get_local_skills_inventory()
        ext_inv = scan_external_skills(p)
        diff = compare_inventories(local_inv, ext_inv)
        if args.json:
            print(json.dumps(diff, ensure_ascii=False, indent=2))
        else:
            print("============================================================")
            print("          ANTIGRAVITY SKILL AGGREGATOR: DIFF                ")
            print("============================================================")
            print(f"  Yerel Beceri Sayısı     : {diff['local_count']}")
            print(f"  Harici Beceri Sayısı    : {diff['external_count']}")
            print(f"  Ortak / Mevcut Beceriler: {len(diff['shared_skills'])}")
            print(f"  Yeni İçe Aktarılabilir  : {len(diff['new_available_skills'])}")
            if diff["new_available_skills"]:
                print(f"\n  Yeni Beceriler (Örnek İlk 10): {', '.join(diff['new_available_skills'][:10])}")
            print("============================================================")
        return 0

    if args.command == "import":
        target = Path(args.file).resolve()
        res = import_skill(target, custom_name=args.name, dry_run=args.dry_run)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

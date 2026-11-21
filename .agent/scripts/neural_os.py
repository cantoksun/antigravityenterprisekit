#!/usr/bin/env python3
"""Antigravity Enterprise Neural-OS: Main Command-Line Interface.

Provides CLI access to launch the local web server (--serve), run hybrid searches (--search),
audit knowledge graph integrity (--audit), and export offline standalone graph packages (--export).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add neural_os paths
SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
NEURAL_OS_DIR = PROJECT_ROOT / "neural_os"
ENGINE_DIR = NEURAL_OS_DIR / "engine"

for p in [str(NEURAL_OS_DIR), str(ENGINE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from graph_engine import EnterpriseGraphEngine
from semantic_search import LocalHybridSearchEngine
from server import NeuralOSServer
from exporter import StandaloneGraphExporter


def run_audit() -> int:
    engine = EnterpriseGraphEngine()
    rep = engine.audit()
    print("🧠 Antigravity Enterprise Neural-OS - Grafik Denetim Raporu")
    print(f"Toplam Düğüm (Nodes): {rep['total_nodes']}")
    print(f"Kırık Bağlantılar (Broken Links): {len(rep['broken_links'])}")
    for src, missing in rep["broken_links"].items():
        print(f"  ❌ {src} -> {', '.join(missing)}")
    print(f"Yetim Düğümler (Orphans): {len(rep['orphans'])}")
    for orphan in rep["orphans"]:
        print(f"  ⚠️ {orphan}")

    print("\nEn Yüksek Otorite Düğümleri (PageRank):")
    for item in rep["top_nodes"]:
        print(f"  ⭐ {item['id']} (PR: {item['pagerank']}%, Gelen: {item['in_degree']}) - {item['title']}")
    return 0


def run_search(query: str, limit: int = 5) -> int:
    searcher = LocalHybridSearchEngine()
    results = searcher.search(query=query, limit=limit)
    print(f"🔍 Arama Sonuçları ('{query}'):")
    if not results:
        print("  (Eşleşen düğüm bulunamadı)")
        return 0

    for r in results:
        print(f"\n⚡ [{r.type}] {r.title} (Skor: {r.score}, PR: {r.pagerank}%)")
        print(f"   Düğüm ID: [[{r.node_id}]] | Dosya: {r.relative_path}")
        print(f"   \"{r.snippet}\"")
    return 0


def run_export(output_path_str: str) -> int:
    target = Path(output_path_str).resolve()
    exporter = StandaloneGraphExporter()
    out = exporter.export(target)
    print(f"✅ Bağımsız tek dosya HTML başarıyla üretildi: {out}")
    print(f"   Dosya Boyutu: {out.stat().st_size:,} bytes")
    print("   (Bu dosyayı herhangi bir tarayıcıda doğrudan internet/sunucu olmadan açabilirsiniz)")
    return 0


def run_serve(port: int = 8990) -> int:
    server = NeuralOSServer(port=port)
    print(f"🧠 Antigravity Enterprise Neural-OS Web Arayüzü Başlatıldı!")
    print(f"👉 Tarayıcıda açın: {server.get_url()}")
    print("   (Durdurmak için Ctrl+C tuşlarına basın)\n")
    server.serve_forever()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity Enterprise Neural-OS CLI")
    subparsers = parser.add_subparsers(dest="command", help="Komutlar")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Yerel interaktif web grafiği ve arayüz sunucusunu başlatır")
    serve_parser.add_argument("--port", "-p", type=int, default=8990, help="Sunucu portu (varsayılan: 8990)")

    # Audit command
    subparsers.add_parser("audit", help="Bilgi ağı grafik bütünlüğünü denetler")

    # Search command
    search_parser = subparsers.add_parser("search", help="BM25 ve PageRank destekli yerel arama yapar")
    search_parser.add_argument("query", help="Aranacak ifade")
    search_parser.add_argument("--limit", "-l", type=int, default=5, help="Maksimum sonuç sayısı")

    # Export command
    export_parser = subparsers.add_parser("export", help="Grafiği bağımsız tek bir HTML dosyası olarak dışa aktarır")
    export_parser.add_argument("--out", "-o", default="neural-os-export.html", help="Çıktı dosyası yolu")

    args = parser.parse_args()

    if args.command == "serve":
        return run_serve(args.port)
    elif args.command == "audit":
        return run_audit()
    elif args.command == "search":
        return run_search(args.query, args.limit)
    elif args.command == "export":
        return run_export(args.out)
    else:
        # Default action: run audit and show usage
        run_audit()
        print("\nİpucu: Web arayüzünü açmak için 'python .agent/scripts/neural_os.py serve' komutunu kullanın.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

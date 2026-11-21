#!/usr/bin/env python3
"""Antigravity Enterprise Neural-OS: Standalone Single-File HTML Exporter.

Bundles HTML, CSS, JavaScript, and the full graph database into a single,
self-contained, offline-compatible HTML file without any external dependencies.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

NEURAL_OS_DIR = Path(__file__).resolve().parent.parent
ENGINE_DIR = NEURAL_OS_DIR / "engine"
UI_DIR = NEURAL_OS_DIR / "ui"

for p in [str(NEURAL_OS_DIR), str(ENGINE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from graph_engine import EnterpriseGraphEngine


class StandaloneGraphExporter:
    """Exports the entire neural knowledge graph into one portable HTML file."""

    def __init__(self, engine: Optional[EnterpriseGraphEngine] = None):
        self.engine = engine or EnterpriseGraphEngine()
        self.ui_dir = UI_DIR

    def export(self, output_path: Path) -> Path:
        graph_data = self.engine.get_graph_export()
        
        # Build node details lookup for offline inspection
        node_details_map = {}
        for nid, node in self.engine.nodes.items():
            node_details_map[nid] = {
                "id": node.id,
                "title": node.title,
                "type": node.type,
                "path": node.relative_path,
                "tags": node.tags,
                "outlinks": sorted(list(node.outlinks)),
                "backlinks": sorted(list(node.backlinks)),
                "summary": node.summary,
                "content": node.raw_content,
                "in_degree": node.metrics.in_degree,
                "out_degree": node.metrics.out_degree,
                "pagerank": node.metrics.pagerank,
            }

        html_template = (self.ui_dir / "index.html").read_text("utf-8")
        css_content = (self.ui_dir / "styles.css").read_text("utf-8")
        js_content = (self.ui_dir / "app.js").read_text("utf-8")

        # Embed CSS
        html_bundled = html_template.replace(
            '<link rel="stylesheet" href="styles.css">',
            f"<style>\n{css_content}\n</style>"
        )

        # Safe JSON embedding: escape both opening <script and closing </script> tags
        # so HTML parsers never treat embedded JSON strings as new script blocks.
        def _safe_json(obj):
            raw = json.dumps(obj, ensure_ascii=False)
            # Escape closing tag first (order matters)
            raw = raw.replace("</script>", "<\\/script>").replace("</SCRIPT>", "<\\/SCRIPT>")
            # Escape opening tag to prevent browser from starting a new script context
            raw = raw.replace("<script", "<\\u0073cript").replace("<SCRIPT", "<\\u0053CRIPT")
            return raw

        graph_json = _safe_json(graph_data)
        details_json = _safe_json(node_details_map)

        # Patch app.js to use embedded data when running as static file (no server)
        embedded_db_js = f"""
  // Embedded Offline Knowledge Base
  window.__EMBEDDED_GRAPH_DATA__ = {graph_json};
  window.__EMBEDDED_NODE_DETAILS__ = {details_json};

  // Override fetch for offline mode
  const originalFetch = window.fetch;
  window.fetch = async function(url) {{
    if (url === '/api/graph') {{
      return {{ json: async () => window.__EMBEDDED_GRAPH_DATA__ }};
    }}
    if (url.startsWith('/api/node/')) {{
      const nid = decodeURIComponent(url.replace('/api/node/', ''));
      const det = window.__EMBEDDED_NODE_DETAILS__[nid] || {{}};
      return {{ json: async () => det }};
    }}
    if (url.startsWith('/api/search')) {{
      const query = new URL(url, 'http://localhost').searchParams.get('q') || '';
      const qLower = query.toLowerCase();
      const results = [];
      for (const [nid, det] of Object.entries(window.__EMBEDDED_NODE_DETAILS__)) {{
        if (det.title.toLowerCase().includes(qLower) || det.content.toLowerCase().includes(qLower) || (det.tags || []).some(t => t.includes(qLower))) {{
          results.push({{
            node_id: det.id,
            title: det.title,
            type: det.type,
            score: 1.0,
            snippet: det.summary,
            tags: det.tags,
            path: det.path
          }});
        }}
      }}
      return {{ json: async () => results.slice(0, 10) }};
    }}
    return originalFetch.apply(this, arguments);
  }};
"""
        patched_js = embedded_db_js + "\n" + js_content

        # Embed JS
        html_bundled = html_bundled.replace(
            '<script src="app.js"></script>',
            f"<script>\n{patched_js}\n</script>"
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_bundled, encoding="utf-8")
        return output_path


if __name__ == "__main__":
    out_file = Path("neural-os-export.html").resolve()
    exporter = StandaloneGraphExporter()
    exporter.export(out_file)
    print(f"✅ Tek dosya taşınabilir HTML başarıyla üretildi: {out_file} ({out_file.stat().st_size} bytes)")

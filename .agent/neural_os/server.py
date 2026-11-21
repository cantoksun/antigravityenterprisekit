#!/usr/bin/env python3
"""Antigravity Enterprise Neural-OS: Lightweight, Zero-Dependency Local Web Server.

Serves the interactive neural knowledge graph, REST API endpoints (/api/graph, /api/node/{id}, /api/search),
and provides strict path traversal security and automatic port collision avoidance.
"""
from __future__ import annotations

import json
import mimetypes
import socket
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional

# Add neural_os engine path
NEURAL_OS_DIR = Path(__file__).resolve().parent
ENGINE_DIR = NEURAL_OS_DIR / "engine"
UI_DIR = NEURAL_OS_DIR / "ui"

for p in [str(NEURAL_OS_DIR), str(ENGINE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from graph_engine import EnterpriseGraphEngine
from semantic_search import LocalHybridSearchEngine


class NeuralOSHandler(BaseHTTPRequestHandler):
    """Custom HTTP handler with REST endpoints and static file serving."""

    server_engine: EnterpriseGraphEngine
    server_searcher: LocalHybridSearchEngine
    ui_dir: Path

    def _set_headers(self, status: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        # Security headers (Rule 29 & Rule 30)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # 1. API: Graph Data
        if path == "/api/graph":
            data = self.server_engine.get_graph_export()
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        # 2. API: Node Details
        if path.startswith("/api/node/"):
            node_id = urllib.parse.unquote(path[len("/api/node/"):].strip())
            # Path traversal / invalid character prevention
            if not node_id or "/" in node_id or "\\" in node_id or ".." in node_id:
                self._set_headers(400, "application/json")
                self.wfile.write(json.dumps({"error": "geçersiz düğüm kimliği"}).encode("utf-8"))
                return

            if node_id in self.server_engine.nodes:
                node = self.server_engine.nodes[node_id]
                resp = {
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
                self._set_headers(200, "application/json")
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            else:
                self._set_headers(404, "application/json")
                self.wfile.write(json.dumps({"error": "düğüm bulunamadı"}).encode("utf-8"))
            return

        # 3. API: Hybrid Search
        if path == "/api/search":
            q = query_params.get("q", [""])[0].strip()
            node_type = query_params.get("type", [None])[0]
            tag = query_params.get("tag", [None])[0]
            limit_val = int(query_params.get("limit", [10])[0])

            results = self.server_searcher.search(query=q, node_type=node_type, tag=tag, limit=limit_val)
            resp = [
                {
                    "node_id": r.node_id,
                    "title": r.title,
                    "type": r.type,
                    "score": r.score,
                    "pagerank": r.pagerank,
                    "snippet": r.snippet,
                    "tags": r.tags,
                    "path": r.relative_path,
                }
                for r in results
            ]
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        # 4. API: Health Check
        if path == "/health/live" or path == "/health/ready":
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({"status": "healthy", "nodes": len(self.server_engine.nodes)}).encode("utf-8"))
            return

        # 5. Static Files Serving (UI)
        if path == "/" or path == "":
            rel_file = "index.html"
        else:
            rel_file = path.lstrip("/")

        target_file = (self.ui_dir / rel_file).resolve()

        # Strict security: prevent path traversal outside UI directory
        try:
            target_file.relative_to(self.ui_dir.resolve())
        except ValueError:
            self._set_headers(403, "text/plain")
            self.wfile.write(b"Erisim engellendi.")
            return

        if target_file.is_file():
            mime_type, _ = mimetypes.guess_type(str(target_file))
            mime_type = mime_type or "application/octet-stream"
            content = target_file.read_bytes()
            self._set_headers(200, mime_type)
            self.wfile.write(content)
        else:
            self._set_headers(404, "text/plain")
            self.wfile.write(b"Dosya bulunamadi.")

    def log_message(self, format: str, *args: Any) -> None:
        # Silent or concise logging to avoid console pollution
        pass


class NeuralOSServer:
    """Enterprise local HTTP server runner."""

    def __init__(self, port: int = 8990, host: str = "127.0.0.1"):
        self.host = host
        self.port = self._find_free_port(port)
        self.engine = EnterpriseGraphEngine()
        self.searcher = LocalHybridSearchEngine(self.engine)
        self.ui_dir = UI_DIR

        # Ensure UI directory exists
        self.ui_dir.mkdir(parents=True, exist_ok=True)

        NeuralOSHandler.server_engine = self.engine
        NeuralOSHandler.server_searcher = self.searcher
        NeuralOSHandler.ui_dir = self.ui_dir

        self.httpd = ThreadingHTTPServer((self.host, self.port), NeuralOSHandler)

    def _find_free_port(self, starting_port: int) -> int:
        port = starting_port
        while port < starting_port + 100:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                res = s.connect_ex((self.host, port))
                if res != 0:
                    return port
                port += 1
        return starting_port

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def serve_forever(self) -> None:
        print(f"🚀 Antigravity Neural-OS sunucusu aktif: {self.get_url()}")
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Sunucu durduruldu.")
        finally:
            self.httpd.server_close()


if __name__ == "__main__":
    server = NeuralOSServer()
    print(f"Server ready on {server.get_url()}")
    server.serve_forever()

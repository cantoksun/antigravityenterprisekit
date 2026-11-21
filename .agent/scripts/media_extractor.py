#!/usr/bin/env python3
"""
media_extractor.py
Antigravity AI-OS v1.0 - Browserless Media & YouTube Transcript Engine (screencut Parity)

Extracts video metadata, subtitles, and timed transcripts from YouTube and web media
without needing a headless browser or heavy third-party drivers.
Provides structured, timestamped markdown summaries for research and engineering agents.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

YOUTUBE_ID_REGEX = re.compile(
    r"(?:v=|\/|youtu\.be\/|embed\/|shorts\/|^)([A-Za-z0-9_-]{11})(?:[&?\/]|$)"
)


def extract_youtube_id(input_str: str) -> Optional[str]:
    """Extracts standard 11-character YouTube video ID from URL or bare ID."""
    clean = input_str.strip()
    if len(clean) == 11 and re.match(r"^[A-Za-z0-9_-]{11}$", clean):
        return clean
    match = YOUTUBE_ID_REGEX.search(clean)
    return match.group(1) if match else None


def fetch_youtube_metadata(video_id: str) -> Dict[str, Any]:
    """Fetches public video metadata via YouTube oEmbed API (zero auth required)."""
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    oembed_url = f"https://www.youtube.com/oembed?url={urllib.parse.quote(video_url)}&format=json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    req = urllib.request.Request(oembed_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "video_id": video_id,
                "title": data.get("title", f"YouTube Video {video_id}"),
                "author_name": data.get("author_name", "Unknown Author"),
                "author_url": data.get("author_url", ""),
                "thumbnail_url": data.get("thumbnail_url", ""),
                "url": video_url,
            }
    except Exception:
        return {
            "video_id": video_id,
            "title": f"YouTube Video ({video_id})",
            "author_name": "YouTube",
            "author_url": "",
            "thumbnail_url": "",
            "url": video_url,
        }


def fetch_youtube_transcript(video_id: str, lang: str = "en") -> List[Dict[str, Any]]:
    """Attempts to retrieve caption tracks via YouTube timedtext endpoints."""
    # First, try direct timedtext endpoint
    timedtext_url = f"https://video.google.com/timedtext?v={video_id}&lang={lang}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(timedtext_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read().decode("utf-8", errors="replace")
            if "<transcript>" in xml_data:
                root = ET.fromstring(xml_data)
                segments = []
                for p in root.findall("text"):
                    start = float(p.attrib.get("start", "0.0"))
                    dur = float(p.attrib.get("dur", "0.0"))
                    txt = html.unescape(p.text or "").strip()
                    if txt:
                        segments.append({"start": start, "duration": dur, "text": txt})
                if segments:
                    return segments
    except Exception:
        pass

    # If direct fetch fails or is gated by consent/bot verification, return empty
    return []


def generate_mock_transcript(video_id: str) -> List[Dict[str, Any]]:
    """Generates realistic deterministic mock transcript for tests and offline usage."""
    return [
        {"start": 0.0, "duration": 4.5, "text": "Antigravity AI-OS mimarisine ve açık kaynak ekosistemine hoş geldiniz."},
        {"start": 5.0, "duration": 6.2, "text": "Bu oturumda 48 anayasa kuralını ve katmanlı kural matrisini inceliyoruz."},
        {"start": 12.0, "duration": 5.8, "text": "Aşamalı beceri yükleyici sayesinde token maliyeti yüzde 97 oranında düşürüldü."},
        {"start": 18.5, "duration": 7.0, "text": "Proaktif RAG nöral bellek motoru ise sadece en alakalı düğümleri bağlama enjekte ediyor."},
    ]


def format_seconds(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def format_transcript_markdown(metadata: Dict[str, Any], segments: List[Dict[str, Any]]) -> str:
    lines = [
        f"# 🎬 Medya Transkript Raporu: {metadata.get('title', 'Video')}",
        "",
        f"- **Kanal / Yazar:** {metadata.get('author_name', 'Bilinmiyor')}",
        f"- **Video ID:** `{metadata.get('video_id', '')}`",
        f"- **Video URL:** {metadata.get('url', '')}",
        f"- **Toplam Segment:** {len(segments)} parça",
        "",
        "## 📜 Zaman Damgalı Transkript İçeriği",
        "",
    ]
    if not segments:
        lines.append("*Altyazı veya transkript kaydı bulunamadı (kapalı altyazı mevcut olmayabilir).*")
    else:
        for seg in segments:
            ts = format_seconds(seg["start"])
            lines.append(f"- **`[{ts}]`** {seg['text']}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Browserless Media & YouTube Transcript Engine")
    parser.add_argument("--url", "-u", required=True, help="YouTube URL or 11-char Video ID")
    parser.add_argument("--lang", "-l", default="en", help="Subtitle language code (e.g. en, tr)")
    parser.add_argument("--format", choices=["markdown", "json", "text"], default="markdown", help="Output format")
    parser.add_argument("--output", "-o", help="Optional file path to save output")
    parser.add_argument("--mock", action="store_true", help="Simulate transcript extraction for offline testing")
    args = parser.parse_args()

    video_id = extract_youtube_id(args.url)
    if not video_id:
        print(f"Hata: Geçersiz YouTube URL veya Video ID: {args.url}", file=sys.stderr)
        return 1

    if args.mock:
        meta = {
            "video_id": video_id,
            "title": "Antigravity AI-OS Architecture & Overview",
            "author_name": "Antigravity Engineering",
            "author_url": "https://youtube.com/@antigravity",
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }
        segments = generate_mock_transcript(video_id)
    else:
        meta = fetch_youtube_metadata(video_id)
        segments = fetch_youtube_transcript(video_id, lang=args.lang)
        if not segments:
            # Fallback to simulated message
            segments = []

    if args.format == "json":
        result = {"metadata": meta, "segments": segments}
        output_str = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.format == "text":
        output_str = " ".join(s["text"] for s in segments)
    else:
        output_str = format_transcript_markdown(meta, segments)

    if args.output:
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_str, encoding="utf-8")
        print(f"✅ Transkript başarıyla kaydedildi: {out_path}")
    else:
        print(output_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())

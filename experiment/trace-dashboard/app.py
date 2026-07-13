#!/usr/bin/env python3
"""Trace Dataset Dashboard – Live counter for the experiment."""

import json
import glob
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

MANIFEST = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces/manifest.jsonl"

BASE = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"
TRACKS = {
    "sft": os.path.join(BASE, "sft"),
    "agentic": os.path.join(BASE, "agentic"),
    "distill": os.path.join(BASE, "distill"),
}

def load_data():
    stats = {"tracks": {}, "total_sessions": 0, "total_traces": 0, "updated_at": ""}

    if os.path.exists(MANIFEST):
        with open(MANIFEST) as f:
            for line in f:
                try:
                    json.loads(line)
                    stats["total_sessions"] += 1
                except:
                    pass

    for track_name, track_dir in TRACKS.items():
        total = 0
        quality = {"great": 0, "good": 0, "mediocre": 0, "poor": 0}
        tasks = {}
        for fp in glob.glob(os.path.join(track_dir, "*.jsonl")):
            with open(fp) as fh:
                for line in fh:
                    total += 1
                    try:
                        t = json.loads(line)
                        q = t.get("quality", "unknown")
                        if q in quality:
                            quality[q] += 1
                        tt = t.get("task_type", "unknown")
                        tasks[tt] = tasks.get(tt, 0) + 1
                    except:
                        pass
        stats["tracks"][track_name] = {
            "total": total,
            "quality": quality,
            "tasks": tasks,
        }
        stats["total_traces"] += total

    stats["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return stats


class StatsHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_GET(self):
        if self.path == "/api/stats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(load_data()).encode())
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8765), StatsHandler)
    print("Dashboard running at http://localhost:8765/")
    server.serve_forever()

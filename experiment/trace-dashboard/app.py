#!/usr/bin/env python3
"""Generate stats.json for the trace dataset monitor."""

import json
import os
import glob
from datetime import datetime, timezone

TRACES_DIR = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"
STATS_FILE = "/Users/georgemalenclaw/.openclaw/workspace/experiment/trace-dashboard/stats.json"

GOAL = 200  # Target traces per label

TRACKS = ["sft", "agentic", "distill"]

DEFS = {
    "sft": "Plain text only. Compatible with every fine-tuning API (OpenAI, Together, Fireworks, Unsloth, LLaMA-Factory).",
    "agentic": "Tool calls + results. Compatible with OpenAI, Together, Fireworks, vLLM.",
    "distill": "SFT + internal reasoning/thinking. Captures full thought process for distillation.",
}


def build_stats():
    tracks = {}
    for track_name in TRACKS:
        dirpath = os.path.join(TRACES_DIR, track_name)
        total = 0
        quality = {"great": 0, "good": 0, "mediocre": 0, "poor": 0}
        labels = {}

        for fp in sorted(glob.glob(os.path.join(dirpath, "*.jsonl"))):
            with open(fp) as fh:
                for line in fh:
                    try:
                        t = json.loads(line)
                        total += 1
                        q = t.get("quality", "unknown")
                        if q in quality:
                            quality[q] += 1
                        lab = t.get("label", "unclassified")
                        labels[lab] = labels.get(lab, 0) + 1
                    except json.JSONDecodeError:
                        pass

        tracks[track_name] = {
            "total": total,
            "quality": quality,
            "labels": labels,
        }

    stats = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "tracks": tracks,
        "defs": DEFS,
    }

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"stats.json written — {os.path.getsize(STATS_FILE)} bytes")
    return stats


if __name__ == "__main__":
    s = build_stats()
    for tn, td in s["tracks"].items():
        print(f"\n  {tn}: {td['total']} total")
        print(f"    quality: {td['quality']}")
        print(f"    labels ({len(td['labels'])}): {td['labels']}")

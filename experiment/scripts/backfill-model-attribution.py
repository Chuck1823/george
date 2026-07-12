#!/usr/bin/env python3
"""Backfill model attribution by querying OpenRouter's Generations API.

For each trace, extracts the runId (gen-xxx) from the trajectory file,
queries OpenRouter's /api/v1/generation/{id} endpoint, and patches the
trace metadata with the actual resolved model name.

OpenRouter Generations API docs:
  https://openrouter.ai/docs/client-sdks/python/sdks/generations/README

Requires: OPENROUTER_API_KEY environment variable.
"""

import json
import os
import time
import traceback
from pathlib import Path
import urllib.request
import urllib.error

TRACES_DIR = Path("/Users/georgemalenclaw/.openclaw/workspace/experiment/traces")
SESSIONS_DIR = Path("/Users/georgemalenclaw/.openclaw/agents/main/sessions")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")


def extract_gen_ids_from_trajectory(session_id):
    """Extract generation IDs from trajectory JSONL file."""
    traj_file = SESSIONS_DIR / f"{session_id}.trajectory.jsonl"
    if not traj_file.exists():
        return []
    
    gen_ids = set()
    try:
        with open(traj_file) as f:
            for line in f:
                d = json.loads(line)
                run_id = d.get("runId", "")
                if run_id and run_id.startswith("gen-"):
                    gen_ids.add(run_id)
    except Exception as e:
        print(f"  Error reading trajectory for {session_id}: {e}")
    return list(gen_ids)


def query_openrouter_generation(gen_id):
    """Query OpenRouter API for generation metadata."""
    if not OPENROUTER_API_KEY:
        return None
    
    url = f"https://openrouter.ai/api/v1/generation/{gen_id}"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": "not_found"}
        elif e.code == 401:
            print(f"  ERROR: OpenRouter API key invalid or missing")
            return {"error": "auth_failed"}
        elif e.code == 429:
            return {"error": "rate_limited"}
        else:
            print(f"  HTTP {e.code} for {gen_id}")
            return {"error": f"http_{e.code}"}
    except Exception as e:
        return {"error": str(e)}


def get_resolved_model(gen_id):
    """Get the actual model name from OpenRouter's generation metadata."""
    result = query_openrouter_generation(gen_id)
    if not result or "error" in result:
        return None, result
    
    # The response includes the model that was actually used
    # Check common field names for the model
    model = (
        result.get("model") or
        result.get("model_id") or
        result.get("generation", {}).get("model") or
        result.get("generation", {}).get("model_id") or
        result.get("data", {}).get("model_id")
    )
    
    return model, result


def enrich_trace(trace_path, session_id):
    """Add model attribution to a trace file."""
    # Check if already enriched
    try:
        with open(trace_path) as f:
            first_line = json.loads(f.readline())
        meta = first_line.get("metadata", {})
        if meta.get("model_attribution") == "resolved":
            return "skipped", meta.get("generation_model", "")
    except Exception:
        return "error", None
    
    # Get generation IDs from trajectory
    gen_ids = extract_gen_ids_from_trajectory(session_id)
    if not gen_ids:
        return "no_gens", None
    
    # Query the most recent generation ID first (likely the main model)
    gen_id = gen_ids[-1]
    model, response = get_resolved_model(gen_id)
    
    if model:
        # Update the trace metadata
        try:
            with open(trace_path) as f:
                lines = f.readlines()
            
            first_line = json.loads(lines[0])
            meta = first_line.get("metadata", {})
            meta["generation_model"] = model
            meta["model_attribution"] = "resolved"
            meta["openrouter_gen_id"] = gen_id
            meta["all_gen_ids"] = gen_ids[:5]  # Keep up to 5 for reference
            first_line["metadata"] = meta
            
            with open(trace_path, "w") as f:
                f.write(json.dumps(first_line) + "\n")
                f.writelines(lines[1:])
            
            return "resolved", model
        except Exception as e:
            print(f"  ERROR writing trace: {e}")
            return "error", None
    else:
        return "not_found", None


def main():
    if not OPENROUTER_API_KEY:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        print("  export OPENROUTER_API_KEY='sk-or-...'")
        return
    
    print("=== FamCloud Model Attribution Backfill ===\n")
    
    tracks = ["sft", "agentic", "distill"]
    stats = {
        "total": 0, "resolved": 0, "skipped": 0,
        "no_gens": 0, "not_found": 0, "error": 0
    }
    
    for track in tracks:
        track_dir = TRACES_DIR / track
        if not track_dir.exists():
            continue
        
        trace_files = sorted(track_dir.glob("*.jsonl"))
        print(f"\nTrack: {track} ({len(trace_files)} traces)")
        
        for i, trace_path in enumerate(trace_files):
            session_id = trace_path.stem
            stats["total"] += 1
            
            status, model = enrich_trace(str(trace_path), session_id)
            stats[status] += 1
            
            if model:
                print(f"  [{i+1}] {session_id}: {model}")
            else:
                print(f"  [{i+1}] {session_id}: {status}")
            
            # Rate limit: 1 query per second
            if i < len(trace_files) - 1:
                time.sleep(0.5)
        
        print(f"  Track complete: {stats}")
    
    print(f"\n=== Final Stats ===")
    print(f"Total:     {stats['total']}")
    print(f"Resolved:  {stats['resolved']}")
    print(f"Skipped:   {stats['skipped']}")
    print(f"No gens:   {stats['no_gens']}")
    print(f"Not found: {stats['not_found']}")
    print(f"Errors:    {stats['error']}")


if __name__ == "__main__":
    main()

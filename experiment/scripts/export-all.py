#!/usr/bin/env python3
"""Export all sessions to dual-track training traces."""

import json
import os
import glob

SESSIONS = "/Users/georgemalenclaw/.openclaw/agents/main/sessions"
OUTPUT = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"

os.makedirs(os.path.join(OUTPUT, "text"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT, "trajectory"), exist_ok=True)

# Find all session JSONL files
session_files = sorted(glob.glob(os.path.join(SESSIONS, "*.jsonl")))
session_files = [f for f in session_files if "trajectory" not in f]

manifest = []

for sp in session_files:
    fname = os.path.basename(sp).replace(".jsonl", "")
    
    # Parse messages
    messages = []
    full_messages = []
    
    with open(sp) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except Exception:
                continue
            if entry.get("type") != "message":
                continue
            msg = entry.get("message", {})
            role = msg.get("role", "")
            content = msg.get("content")
            
            # Extract text
            text = ""
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "text":
                        t = block.get("text", "").strip()
                        if t:
                            text += t + "\n"
            elif isinstance(content, str):
                text = content.strip()
            text = text.strip()
            
            if role == "toolResult":
                # Track 2 only: map tool results
                tool_id = msg.get("toolCallId", "")
                tool_name = msg.get("toolName", "")
                full_messages.append({
                    "role": "tool",
                    "content": text or f"[empty: {tool_name}]",
                    "tool_call_id": tool_id
                })
                continue
            
            if not text:
                continue
            
            if role == "user":
                messages.append({"role": "user", "content": text})
                full_messages.append({"role": "user", "content": text})
            elif role == "assistant":
                # Track 1: just text
                messages.append({"role": "assistant", "content": text})
                # Track 2: include tool_calls
                assistant_msg = {"role": "assistant", "content": text}
                if isinstance(content, list):
                    tool_calls = []
                    for block in content:
                        if block.get("type") == "toolCall":
                            tool_calls.append({
                                "id": block.get("id", ""),
                                "type": "function",
                                "function": {
                                    "name": block.get("name", ""),
                                    "arguments": json.dumps(block.get("arguments", {}))
                                }
                            })
                    if tool_calls:
                        assistant_msg["tool_calls"] = tool_calls
                full_messages.append(assistant_msg)

    # Split into traces
    for track, msgs, track_dir in [
        ("text", messages, "text"),
        ("trajectory", full_messages, "trajectory")
    ]:
        traces = []
        current = []
        for m in msgs:
            current.append(m)
            if m["role"] == "assistant":
                tc = sum(1 for x in current if x["role"] in ("user", "assistant"))
                if tc >= 15 or m == msgs[-1]:
                    if tc >= 2:
                        traces.append({"messages": current})
                    current = []
        if len(current) >= 2:
            traces.append({"messages": current})
        
        out_path = os.path.join(OUTPUT, track_dir, fname + ".jsonl")
        with open(out_path, "w") as f:
            for t in traces:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")
        
        manifest.append({
            "session_id": fname,
            "date": fname[:10],
            "track": track,
            "traces": len(traces),
            "messages": len(msgs)
        })
        print(f"  {fname} -> {track}: {len(traces)} traces ({len(msgs)} msgs)")

# Write manifest
with open(os.path.join(OUTPUT, "manifest.jsonl"), "w") as f:
    for entry in manifest:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"\nDone. Exported {len(set(e['session_id'] for e in manifest))} sessions.")
print(f"Manifest: {os.path.join(OUTPUT, 'manifest.jsonl')}")

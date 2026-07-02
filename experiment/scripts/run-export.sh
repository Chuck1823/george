#!/usr/bin/env python3
import json, sys, os

session = "/Users/georgemalenclaw/.openclaw/agents/main/sessions/56a7da72-187e-4b49-83a4-6366a3279533.jsonl"
output_dir = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"
os.makedirs(output_dir + "/text", exist_ok=True)
os.makedirs(output_dir + "/trajectory", exist_ok=True)

messages = []

with open(session) as f:
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
        if role == "toolResult":
            continue
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
        if not text:
            continue
        clean_role = "user" if role == "user" else "assistant"
        messages.append({"role": clean_role, "content": text})

traces = []
current = []
for msg in messages:
    current.append({"role": msg["role"], "content": msg["content"]})
    if msg["role"] == "assistant":
        tc = sum(1 for m in current if m["role"] in ("user", "assistant"))
        is_end = tc >= 15 or msg == messages[-1]
        if is_end and tc >= 2:
            traces.append({"messages": current})
            current = []
if len(current) >= 2:
    traces.append({"messages": current})

t1_file = output_dir + "/text/56a7da72.jsonl"
with open(t1_file, "w") as f:
    for t in traces:
        f.write(json.dumps(t, ensure_ascii=False) + "\n")

print("Track 1: " + str(len(messages)) + " msgs, " + str(len(traces)) + " traces")
print("Written: " + t1_file)

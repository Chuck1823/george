#!/usr/bin/env python3
"""Capture this session's traces to dual-track format."""
import json, os, glob, datetime

session_id = "56a7da72-187e-4b49-83a4-6366a3279533"
sessions_dir = "/Users/georgemalenclaw/.openclaw/agents/main/sessions"
output_dir = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"
today = datetime.date.today().isoformat()

os.makedirs(output_dir + "/text", exist_ok=True)
os.makedirs(output_dir + "/trajectory", exist_ok=True)

session_file = sessions_dir + "/" + session_id + ".jsonl"
messages = []
full_messages = []

with open(session_file) as f:
    for line in f:
        try:
            entry = json.loads(line)
        except:
            continue
        if entry.get("type") != "message":
            continue
        msg = entry.get("message", {})
        role = msg.get("role", "")
        content = msg.get("content")
        
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
            tool_id = msg.get("toolCallId", "")
            tool_name = msg.get("toolName", "")
            full_messages.append({
                "role": "tool",
                "content": text or "[empty: " + tool_name + "]",
                "tool_call_id": tool_id
            })
            continue
        
        if not text:
            continue
        
        if role == "user":
            messages.append({"role": "user", "content": text})
            full_messages.append({"role": "user", "content": text})
        elif role == "assistant":
            messages.append({"role": "assistant", "content": text})
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
def split_traces(msgs, max_turns=15):
    traces = []
    current = []
    for m in msgs:
        current.append(m)
        if m["role"] == "assistant":
            tc = sum(1 for x in current if x["role"] in ("user", "assistant"))
            if tc >= max_turns or m == msgs[-1]:
                if tc >= 2:
                    traces.append({"messages": current})
                current = []
    if len(current) >= 2:
        traces.append({"messages": current})
    return traces

t1 = split_traces(messages)
t2 = split_traces(full_messages)

t1_file = output_dir + "/text/" + today + ".jsonl"
with open(t1_file, "w") as f:
    for t in t1:
        f.write(json.dumps(t, ensure_ascii=False) + "\n")

t2_file = output_dir + "/trajectory/" + today + ".jsonl"
with open(t2_file, "w") as f:
    for t in t2:
        f.write(json.dumps(t, ensure_ascii=False) + "\n")

# Update manifest
mfile = output_dir + "/manifest.jsonl"
entry1 = {"session_id": session_id, "date": today, "track": "text", "traces": len(t1), "messages": len(messages)}
entry2 = {"session_id": session_id, "date": today, "track": "trajectory", "traces": len(t2), "messages": len(full_messages)}
with open(mfile, "a") as f:
    f.write(json.dumps(entry1) + "\n")
    f.write(json.dumps(entry2) + "\n")

print("Captured " + today + ":")
print("  Text: " + str(len(t1)) + " traces (" + str(len(messages)) + " msgs)")
print("  Trajectory: " + str(len(t2)) + " traces (" + str(len(full_messages)) + " msgs)")

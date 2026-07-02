import json
import sys

session = "/Users/georgemalenclaw/.openclaw/agents/main/sessions/56a7da72-187e-4b49-83a4-6366a3279533.jsonl"
output = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces/2026-06-30.jsonl"

messages = []
with open(session, "r") as f:
    for line in f:
        try:
            entry = json.loads(line.strip())
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
                    bt = block.get("text", "").strip()
                    if bt:
                        text += bt + "\n"
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
        is_end = tc >= 10 or msg == messages[-1]
        if is_end and tc >= 2:
            traces.append({"messages": current})
            current = []

if len(current) >= 2:
    traces.append({"messages": current})

with open(output, "w") as f:
    for t in traces:
        f.write(json.dumps(t, ensure_ascii=False) + "\n")

print(f"{len(messages)} clean messages, {len(traces)} traces")
if traces:
    t0 = traces[0]
    print(f"\nFirst trace: {len(t0['messages'])} turns")
    for m in t0["messages"][:4]:
        print(f"  {m['role']}: {m['content'][:200]}")
        print()

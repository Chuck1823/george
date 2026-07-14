#!/usr/bin/env python3
"""Label existing traces by hand.

These are the first 47 traces — all Charles's real personal/agent usage.
Not SMB vertical data. They go to devops_research.

When we simulate nail_salon / barber / etc. customers, we'll use:
  VERTICAL=nail_salon python3 export-all.py
and the classifier assigns capabilities via LLM.
"""

import json, glob, os

TRACES_DIR = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"

# All current traces are devops/personal agent usage
LABEL_VERTICAL = "devops_research"
BYPASS_CAPABILITIES = {
    # Map of session-id patterns -> likely capability
    "devops": "devops",
    "research": "research",
    "coding": "coding",
    "workflow": "workflow_automation",
}

for track in ["sft", "agentic", "distill"]:
    for fp in sorted(glob.glob(os.path.join(TRACES_DIR, track, "*.jsonl"))):
        filename = os.path.basename(fp)
        traces = []
        with open(fp) as f:
            for line in f:
                if line.strip():
                    traces.append(json.loads(line))

        for t in traces:
            t["vertical"] = LABEL_VERTICAL

            # Try to pick a capability from the content
            content = " ".join(
                m.get("content", "") for m in t.get("messages", [])
            ).lower()

            capability = "general_assistant"
            if "git commit" in content or "push" in content or "npm" in content or "install" in content:
                capability = "devops"
            elif "search" in content or "web_fetch" in content or "article" in content or "research" in content:
                capability = "research"
            elif "write" in content or "read file" in content or "code" in content or "script" in content:
                capability = "coding"
            elif "schedule" in content or "cron" in content or "reminder" in content:
                capability = "workflow_automation"
            elif "session" in content or "send message" in content or "subagent" in content:
                capability = "workflow_automation"
            elif "image" in content or "generate" in content or "video" in content:
                capability = "general_assistant"

            t["capability"] = capability
            t.pop("task_type", None)
            t.pop("labels", None)

        with open(fp, "w") as f:
            for t in traces:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")

        caps = {}
        for t in traces:
            c = t.get("capability", "?")
            caps[c] = caps.get(c, 0) + 1

        print(f"{track}/{filename}: vertical={LABEL_VERTICAL}, caps={caps}")

print("\nAll classified. Labels are heuristic — will be refined by LLM on export.")
print("Next: python3 experiment/trace-dashboard/app.py")

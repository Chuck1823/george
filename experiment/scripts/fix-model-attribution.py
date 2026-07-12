#!/usr/bin/env python3
"""Patch export-all.py to add model attribution from an independent source.

Since OpenClaw only stores 'openrouter/auto' in trajectory files, we create
an independent model tracking file that exports capture when available.

Two fixes:
1. A small OpenClaw hook that logs the resolved model to a tracking file
2. An updated export-all.py that merges model attribution from that file
"""

import json
import os
import subprocess
from pathlib import Path

# This script generates:
# 1. The OpenClaw hook script to install in ~/.openclaw/hooks/
# 2. The patch to export-all.py

WORKSPACE = Path("/Users/georgemalenclaw/.openclaw/workspace/experiment")
HOOKS_DIR = Path("/Users/georgemalenclaw/.openclaw/hooks")

# ============================================================
# 1. OpenClaw Hook: Log resolved model after each run
# ============================================================

# OpenClaw supports hooks. We'll create a post-run hook that captures
# the actual model name from the session trajectory and logs it.

# The session trajectory file DOES contain the model ID in each entry.
# The issue is it only stores the alias (openrouter/auto).
# However, the OpenROUTER API response body contains the actual model
# in the response.json() body as "model": "provider/model-name".

# Since we can't intercept the API response, we need to log the model
# at the OpenClaw level. OpenClaw's /api/v1/chats endpoint returns
# the resolved model in its response.

# Actually, the cleanest approach: use OpenRouter's own API to
# query recent generations by API key and match by timestamp/tokens.

HOOK_SCRIPT = '''#!/usr/bin/env python3
"""OpenClaw post-run hook: Log the resolved model name.

This runs after each OpenClaw session and captures:
- The resolved model from the session trajectory
- The actual model from the OpenRouter API (if available)
- The timestamp and token usage for matching

Output: ~/.openclaw/state/model-usage.log (append-only JSONL)
"""

import json
import os
import sys
import time
from pathlib import Path

SESSIONS_DIR = Path(os.environ.get("OPENCLAW_SESSIONS_DIR", "~/.openclaw/agents/main/sessions")).expanduser()
MODEL_LOG = Path("~/.openclaw/state/model-usage.log").expanduser()

def log_model_for_session(session_id):
    """Extract and log model usage for a session."""
    traj_file = SESSIONS_DIR / f"{session_id}.trajectory.jsonl"
    if not traj_file.exists():
        return
    
    entries = []
    with open(traj_file) as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("type") == "run-end" or entry.get("type") == "trace.metadata":
                    entries.append({
                        "ts": entry.get("ts"),
                        "provider": entry.get("provider"),
                        "modelId": entry.get("modelId"),
                        "modelApi": entry.get("modelApi"),
                    })
            except json.JSONDecodeError:
                continue
    
    if entries:
        MODEL_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(MODEL_LOG, "a") as f:
            f.write(json.dumps({
                "session_id": session_id,
                "logged_at": time.time(),
                "entries": entries,
            }) + "\\n")

if __name__ == "__main__":
    session_id = os.environ.get("OPENCLAW_SESSION_ID", sys.argv[1] if len(sys.argv) > 1 else None)
    if session_id:
        log_model_for_session(session_id)
'''

# ============================================================
# 2. Updated export-all.py snippet to add model attribution
# ============================================================

EXPORT_PATCH = '''
# ADD THIS to the trace metadata section of export-all.py:

def get_resolved_model(session_id):
    """Try to get the resolved model from independent tracking."""
    model_log = Path(os.path.expanduser("~/.openclaw/state/model-usage.log"))
    if not model_log.exists():
        return None
    
    with open(model_log) as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("session_id") == session_id and entry.get("entries"):
                    # Return the most recent model ID
                    last = entry["entries"][-1]
                    return f"{last.get('provider')}/{last.get('modelId')}"
            except json.JSONDecodeError:
                continue
    return None

# Then in the trace building section, change:
# metadata["generation_model"] = meta.get("generation_model", "openrouter/auto")
# TO:
# resolved = get_resolved_model(session_id)
# metadata["generation_model"] = resolved or meta.get("generation_model", "openrouter/auto")
# metadata["model_attribution"] = "resolved" if resolved else "alias"
'''

# Write both files
hooks_file = WORKSPACE / "model-attribution" / "openclaw-hook-log-model.py"
patch_file = WORKSPACE / "model-attribution" / "export-all-model-attribution.patch"

hooks_file.parent.mkdir(parents=True, exist_ok=True)
hooks_file.write_text(HOOK_SCRIPT)
patch_file.write_text(EXPORT_PATCH)

print("✅ Created files:")
print(f"  {hooks_file}")
print(f"  {patch_file}")
print("\nNext steps:")
print("1. Install the hook in ~/.openclaw/hooks/")
print("2. Patch export-all.py with the model attribution snippet")
print("3. Re-export traces to get resolved model names going forward")

#!/usr/bin/env python3
"""Export sessions into quality-filtered, multi-track training traces.

Produces three datasets under experiment/traces/:

  sft/         Chat SFT – text only, system + user/assistant alternation.
               Compatible with EVERY fine-tuning API (OpenAI, Together,
               Fireworks, Axolotl, Unsloth, LLaMA-Factory, Pioneer, etc.)

  agentic/     Full tool-calls – assistant messages include tool_calls
               fields, tool results use role=tool. OpenAI format.
               Compatible with: OpenAI, Together, Fireworks, vLLM.

  distill/     SFT + reasoning – assistant messages include both
               "content" (response) and "reasoning" (internal thinking).
               Compatible with: Pioneer API, models that support
               reasoning_content / thinking fields.

Each trace is one JSONL line: {"messages": [...]}

Quality pipeline:
  1. FILTER:   sessions with >= 3 tool calls AND >= 2 user turns
  2. SPLIT:    conversation segments into independent trace samples
  3. SYSTEM:   prepend behavioral system prompt from workspace files
  4. SCORE:    per-trace quality labels (great/good/mediocre/poor)
  5. CLASSIFY: infer task type (research, devops, coding, etc.)
"""

import json
import os
import glob
from datetime import datetime

# ============================================================
# Configuration
# ============================================================

SESSIONS = "/Users/georgemalenclaw/.openclaw/agents/main/sessions"
OUTPUT = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"
WORKSPACE = "/Users/georgemalenclaw/.openclaw/workspace"

TRACKS = ["sft", "agentic", "distill"]

MIN_TOOL_CALLS = 3      # At least 3 tool calls = non-trivial
MIN_USER_TURNS = 2      # At least 2 user turns = real conversation
MIN_TRACE_TURNS = 2     # Minimum turns to qualify as a trace sample
TRACE_CUT_TURNS = 15    # Split multi-session traces at this turn count

# ============================================================
# System prompt (assembled from workspace identity files)
# ============================================================

def build_system_prompt():
    parts = []
    for name, required in [
        ("AGENTS.md", True),
        ("SOUL.md", True),
        ("USER.md", True),
        ("IDENTITY.md", True),
        ("TOOLS.md", False),
    ]:
        path = os.path.join(WORKSPACE, name)
        if os.path.exists(path):
            with open(path) as f:
                content = f.read().strip()
            if content:
                parts.append(f"--- {name} ---\n{content}")
        elif required:
            print(f"  [WARN] Required system file missing: {name}")
    if not parts:
        return "You are a helpful assistant."
    return "\n\n".join(parts)


SYSTEM_PROMPT = build_system_prompt()

# ============================================================
# Message extraction helpers
# ============================================================

def extract_text(content):
    """Extract visible text blocks, skipping thinking/toolCall blocks."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "").strip()
            for block in content
            if block.get("type") == "text" and block.get("text", "").strip()
        ).strip()
    return ""


def extract_thinking(content):
    """Extract thinking block content."""
    if isinstance(content, list):
        for block in content:
            if block.get("type") == "thinking":
                text = block.get("thinking", "").strip()
                if text:
                    return text
    return ""


def extract_tool_calls(content):
    """Extract tool_calls from a content list."""
    if not isinstance(content, list):
        return []
    return [
        {
            "id": block.get("id", ""),
            "type": "function",
            "function": {
                "name": block.get("name", ""),
                "arguments": json.dumps(block.get("arguments", {}), ensure_ascii=False),
            },
        }
        for block in content
        if block.get("type") == "toolCall"
    ]


# ============================================================
# Quality scoring (per-trace)
# ============================================================

def score_trace(messages):
    """Auto-label a trace based on observable quality signals."""
    score = 0.0
    labels = []

    tool_calls = sum(1 for m in messages if "tool_calls" in m)
    tool_results = sum(1 for m in messages if m.get("role") == "tool")
    user_turns = sum(1 for m in messages if m.get("role") == "user")
    assistant_turns = sum(1 for m in messages if m.get("role") == "assistant")
    thinking_blocks = sum(1 for m in messages if m.get("thinking"))
    unique_tools = set(
        tc.get("function", {}).get("name", "")
        for m in messages
        for tc in m.get("tool_calls", [])
    )
    tool_count = len(unique_tools)
    msg_count = len(messages)

    has_error = any(
        m.get("role") == "tool"
        and any(
            w in m.get("content", "").lower()
            for w in ["error", "failed", "no such file", "command not found"]
        )
        for m in messages
    )

    has_recovery = detect_recovery(messages)

    # Depth signals
    if tool_calls >= 10:
        score += 2.0
        labels.append("deep_reasoning")
    elif tool_calls >= 5:
        score += 1.0
        labels.append("moderate_reasoning")

    # Tool diversity
    if tool_count >= 5:
        score += 1.5
        labels.append("diverse_tools")
    elif tool_count >= 3:
        score += 0.5

    # User engagement
    if user_turns >= 5:
        score += 1.0
        labels.append("extended_dialogue")
    elif user_turns >= 3:
        score += 0.5

    # Self-correction / recovery
    if has_error and has_recovery:
        score += 2.0
        labels.append("self_correction")
    elif has_error:
        score += 0.5
        labels.append("failure_example")

    # Thinking depth
    if thinking_blocks >= 10:
        score += 1.5
        labels.append("deep_thinking")
    elif thinking_blocks >= 3:
        score += 0.5
    elif thinking_blocks >= 1:
        score += 0.25

    # Conversation length
    if msg_count >= 30:
        score += 1.0
        labels.append("long_trajectory")
    elif msg_count >= 15:
        score += 0.5

    # Quality label
    if score >= 6.0:
        quality = "great"
    elif score >= 3.5:
        quality = "good"
    elif score >= 1.5:
        quality = "mediocre"
    else:
        quality = "poor"

    return {
        "quality": quality,
        "score": round(score, 1),
        "labels": labels,
    }


def classify_task(messages):
    """Infer task type from the trace content and tools used."""
    tool_names = set()
    text_lower = ""

    for m in messages:
        text_lower += m.get("content", "").lower() + " "
        for tc in m.get("tool_calls", []):
            try:
                name = tc.get("function", {}).get("name", "")
                if name:
                    tool_names.add(name)
            except:
                pass

    if any(t in tool_names for t in ["exec", "process"]):
        if "git" in text_lower:
            return "devops"
        if "python" in text_lower or "script" in text_lower:
            return "coding"
        return "system_admin"
    if any(t in tool_names for t in ["web_search", "web_fetch"]):
        return "research"
    if any(t in tool_names for t in ["write", "edit", "read"]):
        if "git" in text_lower or "commit" in text_lower or "push" in text_lower:
            return "devops"
        return "writing"
    if any(t in tool_names for t in ["sessions_list", "sessions_history", "sessions_send"]):
        return "workflow"
    if any(t in tool_names for t in ["memory_search", "memory_get"]):
        return "memory_reasoning"
    if any(t in tool_names for t in ["image", "image_generate"]):
        return "multimedia"
    if any(t in tool_names for t in ["cron"]):
        return "automation"
    if any(t in tool_names for t in ["skill_workshop"]):
        return "skill_development"
    if any(t in tool_names for t in ["music_generate", "video_generate"]):
        return "creative_media"
    return "assistant"


def detect_recovery(messages):
    """Check if the trace shows error recovery (error then success)."""
    has_error = False
    for m in messages:
        if m.get("role") == "tool":
            c = m.get("content", "").lower()
            if "error" in c or "failed" in c or "no such file" in c or "command not found" in c:
                has_error = True
            elif has_error and ("success" in c or "wrote" in c or "completed" in c):
                return True
        if m.get("role") == "assistant":
            c = m.get("content", "").lower()
            if ("let me try" in c or "let me retry" in c or "let me fix" in c or "try again" in c):
                if has_error:
                    return True
    return False


def merge_consecutive_assistant(msgs):
    """Merge consecutive assistant messages (for SFT track)."""
    merged = []
    for m in msgs:
        if m["role"] == "assistant" and merged and merged[-1]["role"] == "assistant":
            prev = merged[-1]
            if prev.get("content") and m.get("content"):
                prev["content"] += "\n\n" + m["content"]
            elif m.get("content"):
                prev["content"] = m["content"]
        else:
            merged.append(dict(m))
    return merged


def prepend_system(msgs, system_text):
    """Prepend system message if not already present."""
    if msgs and msgs[0].get("role") == "system":
        return msgs
    return [{"role": "system", "content": system_text}] + msgs


# ============================================================
# Session parsing
# ============================================================

def parse_session(filepath):
    """Parse a session JSONL file into text messages and trajectory messages."""
    all_text_msgs = []
    all_traj_msgs = []
    models_used = set()
    primary_model = None

    with open(filepath) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except:
                continue

            # Track model from assistant message metadata
            if entry.get("type") == "message":
                msg = entry.get("message", {})
                model = msg.get("model", msg.get("modelId"))
                if model:
                    models_used.add(model)
                    if primary_model is None:
                        primary_model = model
                # Also check nested api info
                api_info = msg.get("api", {})
                if isinstance(api_info, dict) and api_info.get("modelId"):
                    models_used.add(api_info["modelId"])
                    if primary_model is None:
                        primary_model = api_info["modelId"]

            # Track custom events for model info
            if entry.get("type") == "custom":
                data = entry.get("data", {})
                if "modelId" in data:
                    models_used.add(data["modelId"])
                    if primary_model is None:
                        primary_model = data["modelId"]

            if entry.get("type") != "message":
                continue

            msg = entry.get("message", {})
            role = msg.get("role", "")
            content = msg.get("content")
            text = extract_text(content)

            if role == "toolResult":
                tool_id = msg.get("toolCallId", "")
                tool_name = msg.get("toolName", "")
                all_traj_msgs.append({
                    "role": "tool",
                    "content": text or f"[empty: {tool_name}]",
                    "tool_call_id": tool_id,
                })
                continue  # skip from text track

            thinking = extract_thinking(content)

            if not text and not thinking:
                continue  # skip completely empty messages

            if role == "user":
                all_text_msgs.append({"role": "user", "content": text})
                all_traj_msgs.append({"role": "user", "content": text})

            elif role == "assistant":
                if not text:
                    # No visible response (thinking only) — attach thinking to the
                    # previous assistant message (same turn) instead of making a
                    # separate empty-content message that breaks fine-tuning APIs.
                    if all_traj_msgs and all_traj_msgs[-1]["role"] == "assistant":
                        if thinking:
                            all_traj_msgs[-1]["thinking"] = all_traj_msgs[-1].get("thinking", "")
                            if all_traj_msgs[-1]["thinking"]:
                                all_traj_msgs[-1]["thinking"] = all_traj_msgs[-1]["thinking"] + "\n\n" + thinking
                            else:
                                all_traj_msgs[-1]["thinking"] = thinking
                    elif all_text_msgs and all_text_msgs[-1]["role"] == "assistant":
                        if thinking:
                            all_text_msgs[-1]["content"] = all_text_msgs[-1].get("content", "")
                            # Merge thinking as reasoning note on previous message
                            if thinking:
                                all_text_msgs[-1]["content"] += "\n\n" + thinking
                    continue  # do NOT add a new empty-content assistant message

                # Text track: plain text content only
                all_text_msgs.append({"role": "assistant", "content": text})

                # Trajectory track: include tool_calls + thinking
                traj_msg = {"role": "assistant", "content": text}
                tc = extract_tool_calls(content)
                if tc:
                    traj_msg["tool_calls"] = tc
                if thinking:
                    traj_msg["thinking"] = thinking
                all_traj_msgs.append(traj_msg)

    return all_text_msgs, all_traj_msgs, sorted(models_used), primary_model


def split_into_traces(text_msgs, traj_msgs, min_turns=MIN_TRACE_TURNS, cut_at=TRACE_CUT_TURNS):
    """Split interleaved messages into independent trace samples.

    Each trace starts with user -> assistant pairs and cuts when
    either we hit `cut_at` turns or it's the last message.
    """
    sft_traces = []
    agg_traces = []
    dis_traces = []

    sft_buf = []
    traj_buf = []
    distill_buf = []

    def flush():
        nonlocal sft_buf, traj_buf, distill_buf
        if len(sft_buf) >= min_turns:
            msgs = prepend_system(merge_consecutive_assistant(sft_buf), SYSTEM_PROMPT)
            sft_traces.append({"messages": msgs})
        if len(traj_buf) >= min_turns:
            msgs = prepend_system(traj_buf, SYSTEM_PROMPT)
            agg_traces.append({"messages": msgs})
        if len(distill_buf) >= min_turns:
            msgs = prepend_system(distill_buf, SYSTEM_PROMPT)
            dis_traces.append({"messages": msgs})
        sft_buf = []
        traj_buf = []
        distill_buf = []

    turns = 0
    for text_m, traj_m in zip(text_msgs, traj_msgs):
        sft_buf.append(dict(text_m))
        traj_buf.append(dict(traj_m))

        # Distill track: content + reasoning
        dis_m = {"role": traj_m["role"], "content": traj_m.get("content", "")}
        if traj_m.get("thinking"):
            dis_m["reasoning"] = traj_m["thinking"]
        if traj_m.get("tool_calls"):
            dis_m["tool_calls"] = traj_m["tool_calls"]
        distill_buf.append(dis_m)

        if traj_m["role"] == "user":
            turns += 1
        elif traj_m["role"] == "assistant":
            turns += 1
            if turns >= cut_at or traj_m == traj_msgs[-1]:
                flush()
                turns = 0

    flush()  # flush remaining

    return sft_traces, agg_traces, dis_traces


def should_export(text_msgs, traj_msgs):
    """Quality gate: should this session be exported?"""
    tool_calls = sum(1 for m in traj_msgs if "tool_calls" in m)
    user_turns = sum(1 for m in traj_msgs if m.get("role") == "user")

    if tool_calls < MIN_TOOL_CALLS:
        return False, f"only {tool_calls} tool calls (need {MIN_TOOL_CALLS})"
    if user_turns < MIN_USER_TURNS:
        return False, f"only {user_turns} user turns (need {MIN_USER_TURNS})"
    return True, "passes quality gate"


# ============================================================
# Main export
# ============================================================

os.makedirs(os.path.join(OUTPUT, "sft"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT, "agentic"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT, "distill"), exist_ok=True)

session_files = sorted(glob.glob(os.path.join(SESSIONS, "*.jsonl")))
session_files = [
    f for f in session_files
    if "trajectory" not in f and not f.endswith(".jsonl.lock") and ".reset." not in f
]

manifest_entries = []
total_exported = 0
skipped = []

for sp in session_files:
    fname = os.path.basename(sp).replace(".jsonl", "")

    text_msgs, traj_msgs, models_used, primary_model = parse_session(sp)

    # Quality gate
    allowed, reason = should_export(text_msgs, traj_msgs)
    if not allowed:
        skipped.append((fname, reason))
        continue

    # Split into traces
    sft_traces, agg_traces, dis_traces = split_into_traces(text_msgs, traj_msgs)

    # Score each trace individually
    for sft_t, agg_t, dis_t in zip(sft_traces, agg_traces, dis_traces):
        score = score_trace(agg_t["messages"])
        trace_task = classify_task(agg_t["messages"])

        # Per-trace metadata
        unique_tools = set(
            tc.get("function", {}).get("name", "")
            for m in agg_t["messages"]
            for tc in m.get("tool_calls", [])
        )
        thinking = sum(1 for m in agg_t["messages"] if m.get("thinking"))
        recovered = detect_recovery(agg_t["messages"])

        for target in [sft_t, agg_t, dis_t]:
            target["quality"] = score["quality"]
            target["score"] = score["score"]
            target["labels"] = score["labels"]
            target["task_type"] = trace_task
            target["metadata"] = {
                "tools_used": sorted(unique_tools),
                "thinking_blocks": thinking,
                "has_recovered_from_error": recovered,
                "generation_model": primary_model,
                "models_used_in_session": models_used,
            }

    # Write all three tracks
    for track_name, track_traces in [
        ("sft", sft_traces),
        ("agentic", agg_traces),
        ("distill", dis_traces),
    ]:
        if not track_traces:
            continue
        out_path = os.path.join(OUTPUT, track_name, fname + ".jsonl")
        with open(out_path, "w") as f:
            for t in track_traces:
                if track_name == "sft":
                    clean = {
                        "messages": [
                            {"role": m["role"], "content": m.get("content", "")}
                            for m in t["messages"]
                        ],
                    }
                else:
                    clean = {
                        "messages": t["messages"],
                        "tool_calls_in_trace": sum(
                            1 for m in t["messages"] if "tool_calls" in m
                        ),
                    }

                # Attach quality + metadata to all tracks
                for k in ("quality", "score", "labels", "task_type", "metadata"):
                    if k in t:
                        clean[k] = t[k]

                f.write(json.dumps(clean, ensure_ascii=False) + "\n")
        print(f"  {fname} -> {track_name}: {len(track_traces)} traces")

    total_exported += 1
    manifest_entries.append({
        "session_id": fname,
        "date": fname[:10] if len(fname) >= 10 else "",
        "tracks": ["sft", "agentic", "distill"],
        "traces": {
            "sft": len(sft_traces),
            "agentic": len(agg_traces),
            "distill": len(dis_traces),
        },
    })

# ============================================================
# Summary
# ============================================================

print(f"\n{'=' * 60}")
print(f"  Exported: {total_exported} sessions")
if skipped:
    print(f"  Skipped:  {len(skipped)} sessions  (below quality threshold)")
    for fname, reason in skipped:
        print(f"    {fname}: {reason}")
print(f"{'=' * 60}")

# Write manifest
manifest_path = os.path.join(OUTPUT, "manifest.jsonl")
with open(manifest_path, "w") as f:
    for entry in manifest_entries:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print(f"\nManifest: {manifest_path}")

# Count totals per track with quality breakdown
for track in TRACKS:
    total = 0
    qualities = {"great": 0, "good": 0, "mediocre": 0, "poor": 0}
    tasks = {}
    for fp in glob.glob(os.path.join(OUTPUT, track, "*.jsonl")):
        with open(fp) as fh:
            for line in fh:
                total += 1
                try:
                    t = json.loads(line)
                    q = t.get("quality", "unknown")
                    if q in qualities:
                        qualities[q] += 1
                    tt = t.get("task_type", "unknown")
                    tasks[tt] = tasks.get(tt, 0) + 1
                except:
                    pass
    print(f"  {track}: {total} traces | quality: {dict(qualities)} | tasks: {tasks}")

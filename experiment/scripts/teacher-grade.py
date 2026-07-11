#!/usr/bin/env python3
"""Teacher model grading for trace distillation.

Sends exported traces to a premium teacher model for:
  1. Independent quality grading (great/good/mediocre/poor)
  2. Enriched reasoning traces (richer versions of agent thinking)

Output: enriched distill track traces with teacher_quality, enriched reasoning,
        and teacher_metadata fields.

Configuration: Reads TEACHER_MODEL and TEACHER_API_KEY from environment.
Supported teacher models: claude (Anthropic), openai (OpenAI)
"""

import json
import os
import glob
import sys
from typing import Optional

# ============================================================
# Configuration
# ============================================================

OUTPUT = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"
DISTILL_DIR = os.path.join(OUTPUT, "distill")

# Teacher model config (from env or defaults)
TEACHER_MODEL = os.environ.get("TEACHER_MODEL", "claude-sonnet-4-20250514")
TEACHER_API_KEY = os.environ.get("TEACHER_API_KEY", "")
TEACHER_API_BASE = os.environ.get("TEACHER_API_BASE", "")

# Detection: use Anthropic API or OpenAI-compatible
def detect_provider():
    if not TEACHER_API_KEY:
        return None
    if TEACHER_API_BASE or TEACHER_MODEL.startswith(("gpt-", "o1", "o3")):
        return "openai"
    return "anthropic"

# ============================================================
# Grading Prompt
# ============================================================

GRADING_SYSTEM = """You are an expert AI agent grader. You evaluate reasoning traces from an AI assistant
that uses tools to solve problems. For each trace, provide:

1. **Quality assessment**: great/good/mediocre/poor based on:
   - great: Excellent reasoning, correct tool usage, optimal path, good self-correction
   - good: Solid execution, minor inefficiencies
   - mediocre: Gets there but takes wrong turns, inefficient
   - poor: Failed or produced incorrect output

2. **Enriched reasoning**: Rewrite the reasoning trace to show what a stronger model would think.
   Show alternative paths considered, uncertainty, decision rationale, and self-correction.
   The enriched reasoning should be richer and more explicit than the original.

Respond with valid JSON:
{
  "teacher_quality": "great|good|mediocre|poor",
  "teacher_score": 8.5,
  "teacher_notes": "brief explanation of why",
  "enriched_reasoning": "the enriched, multi-step reasoning that captures..."
}

The enriched_reasoning should be a single string that could replace the agent's thinking blocks
with richer, more explicit reasoning that shows the teacher model's thought process at each step."""

# ============================================================
# Helper to extract one trace's context for grading
# ============================================================

def trace_to_grading_input(trace):
    """Convert a trace to a concise representation for the teacher model.
    
    We don't send the full conversation (too expensive and slow).
    Instead, we send the structure + key content + original reasoning.
    """
    msgs = trace["messages"]
    system_msg = ""
    conversation = []
    reasoning_parts = []
    
    for m in msgs:
        role = m.get("role", "")
        if role == "system":
            system_msg = m.get("content", "")[:500]  # Truncate long system prompts
        elif role == "assistant":
            content = m.get("content", "")
            thinking = m.get("reasoning", "")
            tools = []
            for tc in m.get("tool_calls", []):
                fn = tc.get("function", {})
                tools.append(f"{fn.get('name', '?')}({fn.get('arguments', '{}')})")
            
            entry = {"role": "assistant", "content": content[:300]}
            if tools:
                entry["tools_called"] = tools
            if thinking:
                reasoning_parts.append(thinking)
                entry["reasoning"] = thinking[:500]  # Truncate for brevity
            conversation.append(entry)
        elif role == "user":
            conversation.append({"role": "user", "content": m.get("content", "")[:300]})
        elif role == "tool":
            conversation.append({
                "role": "tool",
                "content": m.get("content", "")[:200],
                "tool_call_id": m.get("tool_call_id", "")
            })
    
    grading_input = {
        "trace_structure": {
            "turns": len(conversation),
            "tool_calls_in_trace": sum(1 for m in msgs if "tool_calls" in m),
            "messages_count": len(msgs),
        },
        "self_assessed_quality": trace.get("quality", "unknown"),
        "self_score": trace.get("score", 0),
        "metadata": trace.get("metadata", {}),
        "conversation": conversation,
        "original_reasoning_summary": "\n---\n".join(reasoning_parts[:3])  # Max 3 reasoning blocks
    }
    
    return json.dumps(grading_input, ensure_ascii=False, indent=2)


# ============================================================
# API Calls
# ============================================================

def call_teacher(prompt):
    """Send prompt to teacher model via API. Returns parsed JSON response."""
    provider = detect_provider()
    if not provider:
        raise RuntimeError(
            "No teacher API key configured. Set TEACHER_API_KEY env var.\n"
            "For OpenAI: TEACHER_API_BASE=https://api.openai.com/v1 TEACHER_MODEL=gpt-4o\n"
            "For Anthropic: TEACHER_MODEL=claude-sonnet-4-20250514"
        )
    
    if provider == "openai":
        return call_openai_teacher(prompt)
    else:
        return call_anthropic_teacher(prompt)


def call_anthropic_teacher(prompt):
    try:
        from anthropic import Anthropic
    except ImportError:
        raise RuntimeError("pip install anthropic for Anthropic API access")
    
    client = Anthropic(api_key=TEACHER_API_KEY)
    
    response = client.messages.create(
        model=TEACHER_MODEL,
        system=GRADING_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.0,  # Deterministic grading
    )
    
    text = response.content[0].text
    # Extract JSON from response
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    
    return json.loads(text)


def call_openai_teacher(prompt):
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("pip install openai for OpenAI API access")
    
    if TEACHER_API_BASE:
        client = OpenAI(api_key=TEACHER_API_KEY, base_url=TEACHER_API_BASE)
    else:
        client = OpenAI(api_key=TEACHER_API_KEY)
    
    response = client.chat.completions.create(
        model=TEACHER_MODEL,
        messages=[
            {"role": "system", "content": GRADING_SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    
    text = response.choices[0].message.content
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    
    return json.loads(text)


# ============================================================
# Main grading loop
# ============================================================

def load_distill_traces():
    """Load all distill track traces."""
    traces_by_file = {}
    for fp in sorted(glob.glob(os.path.join(DISTILL_DIR, "*.jsonl"))):
        fname = os.path.basename(fp)
        traces = []
        with open(fp) as f:
            for line in f:
                traces.append(json.loads(line))
        traces_by_file[fname] = traces
    return traces_by_file


def save_enriched_traces(traces_by_file):
    """Write enriched traces back to distill directory."""
    for fname, traces in traces_by_file.items():
        out_path = os.path.join(DISTILL_DIR, fname)
        with open(out_path, "w") as f:
            for t in traces:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")


def grade_traces(traces_by_file, output_file=None, dry_run=False, limit=None):
    """Grade and enrich all (or limited) distill track traces.
    
    Args:
        traces_by_file: dict of filename -> [traces]
        output_file: optional, save to this file instead of overwriting
        dry_run: if True, show what would be graded without calling API
        limit: grade only first N traces (for testing)
    """
    total = sum(len(t) for t in traces_by_file.values())
    print(f"Found {total} distill traces across {len(traces_by_file)} files")
    
    graded = 0
    skipped_already = 0
    errors = 0
    
    for fname, traces in traces_by_file.items():
        for i, trace in enumerate(traces):
            if limit is not None and graded + skipped_already >= limit:
                break
            
            # Skip already graded
            if trace.get("enriched_by"):
                skipped_already += 1
                continue
            
            # Get original reasoning for comparison
            reasoning_blocks = [
                m.get("reasoning", "")
                for m in trace["messages"]
                if m.get("reasoning")
            ]
            
            if not reasoning_blocks:
                print(f"  [SKIP] {fname}:{i+1} no reasoning blocks to enrich")
                continue
            
            if dry_run:
                print(f"  [DRY RUN] {fname}:{i+1} would grade (current quality: {trace.get('quality')})")
                graded += 1
                continue
            
            try:
                grading_input = trace_to_grading_input(trace)
                
                prompt = f"""Grade this reasoning trace and provide enriched reasoning.

TRACE INPUT:
{grading_input}

Original reasoning blocks ({len(reasoning_blocks)} total):
{reasoning_blocks[0][:400]}{"..." if len(reasoning_blocks[0]) > 400 else ""}{"\n...\n" + reasoning_blocks[-1][:400] if len(reasoning_blocks) > 1 else ""}

Grade the quality and provide enriched reasoning:"""
                
                result = call_teacher(prompt)
                
                # Apply results to trace
                trace["teacher_quality"] = result.get("teacher_quality", trace.get("quality"))
                trace["teacher_score"] = result.get("teacher_score", trace.get("score"))
                trace["teacher_notes"] = result.get("teacher_notes", "")
                trace["enriched_by"] = TEACHER_MODEL
                
                # Enrich reasoning in each assistant message
                enriched_text = result.get("enriched_reasoning", "")
                if enriched_text and reasoning_blocks:
                    # Replace reasoning in all assistant messages with enriched version
                    reasoning_idx = 0
                    for m in trace["messages"]:
                        if m.get("role") == "assistant" and m.get("reasoning"):
                            # Split enriched reasoning by turns if multiple blocks
                            if len(reasoning_blocks) > 1:
                                # Just append to the main reasoning, keep others
                                if reasoning_idx == 0:
                                    m["reasoning"] = enriched_text
                                    reasoning_idx += 1
                            else:
                                m["reasoning"] = enriched_text
                else:
                    # No enriched reasoning provided, at least mark it
                    trace["enriched_reasoning_available"] = False
                
                graded += 1
                print(f"  [OK] {fname}:{i+1} graded: {result.get('teacher_quality')} (score: {result.get('teacher_score')})")
                
            except Exception as e:
                errors += 1
                print(f"  [ERROR] {fname}:{i+1} grading failed: {e}")
    
    print(f"\nGrade {graded} traces, skipped {skipped_already} already-graded, {errors} errors")
    
    if not dry_run:
        save_enriched_traces(traces_by_file)
        print(f"Enriched traces saved to {DISTILL_DIR}/")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Teacher model grading for trace distillation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be graded without calling API")
    parser.add_argument("--limit", type=int, default=None, help="Grade only first N traces")
    parser.add_argument("--model", type=str, default=None, help="Override teacher model")
    parser.add_argument("--api-key", type=str, default=None, help="Override teacher API key")
    args = parser.parse_args()
    
    if args.model:
        global TEACHER_MODEL
        TEACHER_MODEL = args.model
    if args.api_key:
        global TEACHER_API_KEY
        TEACHER_API_KEY = args.api_key
    
    traces = load_distill_traces()
    
    if args.dry_run:
        print("=== DRY RUN MODE ===")
        grade_traces(traces, dry_run=True, limit=args.limit)
        return
    
    # Check if we have API credentials
    provider = detect_provider()
    if not provider:
        print("ERROR: Teacher model API credentials not configured.")
        print("Set environment variables:")
        print("  TEACHER_API_KEY=sk-xxx")
        print("  TEACHER_MODEL=claude-sonnet-4-20250514")
        print("  (For OpenAI: TEACHER_API_BASE=https://api.openai.com/v1)")
        print()
        print("Or run with --dry-run to see what would be graded.")
        sys.exit(1)
    
    print(f"Teacher model: {TEACHER_MODEL} ({provider})")
    grade_traces(traces, limit=args.limit)


if __name__ == "__main__":
    main()

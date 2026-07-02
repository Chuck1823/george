# Experiment: Agentic Reasoning Traces

## Goal
Collect my reasoning traces → distill knowledge from premium models via their full reasoning chains → fine-tune a small model capable of running on a home GPU rig with near-frontier performance.

Based on Hinton et al. knowledge distillation (https://arxiv.org/abs/1503.02531) applied to LLM reasoning traces.

## Toggle
`experiment/trace-collector.json` — `enabled` is the master switch. Charles controls this.

## How It Works

I wake up fresh each session, so I can't auto-capture in real-time. The loop is:

### Phase 1: Capture (automatic, each session)
1. At the end of a session, I review the conversation
2. If it meets the criteria below → extract the session into trace format
3. Record it in `experiment/traces/manifest.jsonl`
4. This happens every time a substantive conversation concludes

### Phase 2: Distillation (future, manual batch)  
1. Export session JSONL from `~/.openclaw/agents/main/sessions/`
2. Send each trace to the strongest model available (Claude Opus / GPT-5.5)
3. The premium model produces its own full reasoning trace for the same problem
4. The teacher's reasoning (not just the answer) becomes the distilled training target
5. The student model learns to replicate *how* the premium model thinks, not just *what* it says

### Phase 3: Fine-tune (future, Pioneer API)
1. Upload distilled dataset to Pioneer
2. LoRA fine-tune a small base model (Qwen 3B/8B, Llama 3.2 3B/1B, GPT-OSS 20B)
3. Evaluate against held-out tasks
4. Deploy locally on a small GPU rig

## Trace Format
One JSONL line per conversation. Pioneer Chat SFT format:
```json
{"messages": [
  {"role":"system","content":"..."},
  {"role":"user","content":"..."},
  {"role":"assistant","content":"..."}
]}
```

## Distillation Format (future)
```json
{
  "messages": [
    {"role":"system","content":"..."},
    {"role":"user","content":"..."},
    {"role":"assistant","content":"<teacher's full reasoning>"}
  ],
  "teacher_thinking": "<full chain-of-thought from premium model>",
  "original_reasoning": "<my original chain-of-thought>"
}
```

## Collection Criteria
Capture a session when:
- The conversation has a clear, self-contained goal
- 3+ tool calls were made (complex reasoning)
- There was self-correction or interesting course-correction
- The session solved something end-to-end
- OR the session failed/notably in a useful way (negative examples)

Skip:
- Simple chitchat
- Single-turn Q&A
- Purely administrative (file reads with no decisions)

## Storage
```
experiment/traces/
├── manifest.jsonl          # Index: session_id, date, quality, tool_count, captured
```

## Repo Commitment
The repo contains this spec and the toggle. Session data itself lives in OpenClaw's session store (~/.openclaw/agents/main/sessions/). The manifest references session IDs so the data is recoverable.

## Pioneer Upload Format
Chat SFT format. Pioneer base models:
- Qwen3 8B/32B, Qwen2.5 7B/14B
- Llama 3.2 3B/1B/70B, Llama 3.1 8B/70B  
- GPT-OSS 20B/120B
- DeepSeek V3.1
- Gemma 4 31B

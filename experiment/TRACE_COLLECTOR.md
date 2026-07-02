# Trace Collector - Agentic Reasoning Traces

## Overview

Collects George's reasoning traces for the self-improving fine-tuning experiment.
Captures conversations where George uses tools, reasons through problems, and arrives at decisions.

## Toggle Control

**To enable/disable:** Set `traceCollection.enabled` in `experiment/trace-collector.json`

```json
{
  "enabled": false,
  "mode": "quality",
  "minComplexity": 3,
  "autoRotate": true,
  "maxFileSizeMB": 50,
  "compressOlder": true
}
```

Fields:
- `enabled`: Master toggle. Set to `false` to stop all trace collection. Set to `true` to enable.
- `mode`: `all` (every conversation), `quality` (only good/bad quality examples), `complex` (tool-using/multi-step only)
- `minComplexity`: Minimum number of tool calls to qualify as a "complex" trace (default 3)
- `compressAfterDays`: How many days before gzipping old files (default 1). Yesterday gets compressed, today stays readable.

## Trace Format

Each trace is one JSONL line. Pioneer-compatible decoder (Chat SFT) format:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

Extended format with metadata for our own bookkeeping (stored separately, not uploaded):

```json
{
  "id": "trace-YYYY-MM-DD-HHMMSS",
  "messages": [...],
  "quality": "great|good|mediocre|poor",
  "quality_notes": "brief reason for the quality rating",
  "task_type": "reasoning|coding|analysis|assistant|creative|debugging|planning",
  "tools_used": ["exec", "read", "web_search"],
  "tool_count": 5,
  "turn_count": 8,
  "timestamp": "2026-06-30T18:00:00Z",
  "self_assessed": true
}
```

## Collection Criteria

**Capture when:**
- The conversation has a clear goal or informative objective
- George uses 3+ tools (complex reasoning)
- There's self-correction or course-correction
- A problem is solved end-to-end
- Notable failure or suboptimal path (for negative examples)

**Skip when:**
- Simple chitchat with no reasoning
- Single-turn factual Q&A
- Purely administrative (reading files, status checks with no interesting decisions)

## Storage Layout

```
experiment/traces/
├── 2026-06-30.jsonl          # Today's traces (plain text, easy to inspect)
├── 2026-06-29.jsonl.gz       # Yesterday's compressed (to save space)
├── manifest.jsonl            # Index: id, quality, file, turn_count for each trace
└── stats.json                # Running stats: counts by quality, type, date
```

That's it. Each day gets one JSONL file. Next day, George compresses yesterday's with gzip. Simple.

## Quality Assessment

Every captured trace gets two passes:
1. **Self-assessment** (immediate): George rates quality after the conversation — was reasoning sound? efficient? correct? Did I self-correct?
2. **Premium model grading** (later batch): A stronger model (Claude/GPT) reviews the same trace independently and assigns its own quality rating.

Both ratings are stored. The gap between self-assessment and premium grading is itself a training signal — when George learns to judge its own quality more accurately, that's improvement. Eventually the combined dataset (with premium model distilled reasoning) becomes the fine-tuning data for smaller models.

## Pioneer API Integration

When ready to upload:

1. Extract traces from `experiment/traces/active/*.jsonl`
2. Convert to Pioneer's decoder Chat SFT format (already compatible)
3. Upload via presigned URL flow:
   - POST /felix/datasets/upload/url
   - PUT to presigned URL
   - POST /felix/datasets/upload/process

Training job format (for later experimentation):
```json
{
  "model_name": "george-agentic",
  "base_model": "meta-llama/Llama-3.2-3B-Instruct",
  "datasets": [{"name": "george-traces-v1"}],
  "training_type": "lora"
}
```

Base models within Pioneer's gated/open-source bounds:
- Llama 3.2 3B / 1B / 70B
- Qwen3 8B / 4B / 32B
- Qwen2.5 7B / 14B
- Gemma 4 31B
- GPT-OSS 20B / 120B
- DeepSeek V3.1

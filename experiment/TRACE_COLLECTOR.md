# Trace Collector - Agentic Reasoning Traces

## Overview

Collects George's reasoning traces for the self-improving fine-tuning experiment.
Captures conversations where George uses tools, reasons through problems, and arrives at decisions.

## Toggle Control

**To enable/disable:** Set `traceCollection.enabled` in `experiment/trace-collector.json`

```json
{
  "enabled": true,
  "mode": "quality",
  "minComplexity": 3
}
```

Fields:
- `enabled`: Master toggle
- `mode`: `quality` = only sessions with 3+ tool calls and 2+ user turns
- `minComplexity`: Minimum number of tool calls to qualify

## Export Tracks

The weekly export (`experiment/scripts/export-all.py`) produces **three datasets** under `experiment/traces/`:

| Track | Format | Use |
|---|---|---|
| `sft/` | system + user/assistant turns | Universal fine-tuning (OpenAI, Together, Fireworks, Unsloth, LLaMA-Factory) |
| `agentic/` | full tool_calls + tool results | OpenAI fine-tuning, Together, Fireworks |
| `distill/` | sft + assistant reasoning traces | Pioneer API, models that support reasoning_content |

## Export Script

```bash
python3 experiment/scripts/export-all.py
```

Each trace gets:
- **System prompt**: assembled from AGENTS.md + SOUL.md + USER.md + IDENTITY.md
- **Quality label**: great/good/mediocre/poor (auto-scored from observable trace metrics)
- **Task type**: research, devops, coding, writing, workflow, memory_reasoning, multimedia, automation, skill_development, creative_media, assistant
- **Metadata**: tools used, thinking block count, self-correction flag

## Quality Scoring (auto)

Based on per-trace observable metrics:
- tool call count (10+ = deep_reasoning, 5+ = moderate_reasoning)
- tool diversity (5+ unique tools = diverse_tools)
- user turns (5+ = extended_dialogue)
- thinking blocks (10+ = deep_thinking)
- error + recovery = self_correction (+2 points)
- long trajectories (30+ messages, 15+)

Thresholds:
- >= 6.0 → great
- >= 3.5 → good
- >= 1.5 → mediocre
- < 1.5 → poor

## Teacher Grading (weekly)

After export, a premium teacher model (Claude/GPT) grades each trace independently:
1. Assigns independent quality label (great/good/mediocre/poor)
2. Produces **enriched reasoning traces** — richer versions of the agent's reasoning, showing what a stronger model would think at each step
3. The enriched traces go into the distillation dataset for fine-tuning

The enriched reasoning is the signal — Hinton distillation uses the teacher's output distribution (rich reasoning with uncertainty, alternative paths considered) not just quality scores.

## Pioneer API Integration

When ready to upload:

1. Extract traces from `experiment/traces/{track}/*.jsonl`
2. Convert to Pioneer's decoder Chat SFT format (already compatible)
3. Upload via presigned URL flow:
   - POST /felix/datasets/upload/url
   - PUT to presigned URL
   - POST /felix/datasets/upload/process

Training job format:
```json
{
  "model_name": "george-agentic",
  "base_model": "meta-llama/Llama-3.2-3B-Instruct",
  "datasets": [{"name": "george-traces-v1"}],
  "training_type": "lora"
}
```

Base models within Pioneer's bounds:
- Llama 3.2 3B / 1B / 70B
- Qwen3 8B / 4B / 32B
- Qwen2.5 7B / 14B
- Gemma 4 31B
- GPT-OSS 20B / 120B
- DeepSeek V3.1

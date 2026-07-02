# Trace Collection: Dual-Track System

## Overview
Captures every qualifying session into two training data formats for distillation.

## Data Sources

**Primary:** Built-in OpenClaw `/export-trajectory` command
- Produces trajectory bundles with full tool calls, results, and reasoning
- Located in `.openclaw/trajectory-exports/`
- OpenAI fine-tuning format included

**Secondary:** Manual extraction from session store (for text-only track)
- `experiment/scripts/export-all.py` reads session JSONL directly
- Produces clean text-only traces for Pioneer fine-tuning

## Two Datasets

### Track 1: Text-Only (Pioneer-compatible)
- Format: `{"messages": [{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}`
- Strips all tool calls, tool results, and thinking blocks
- Location: `experiment/traces/text/*.jsonl`

### Track 2: Full Trajectory (OpenAI fine-tuning format)  
- Format: Full OpenAI tool_calls format with tool results
- Preserves tool decisions, parameters, and outputs
- Location: `.openclaw/trajectory-exports/` (from slash command)
- Also exported to: `experiment/traces/trajectory/*.jsonl`

## Capturing Current Session

**From chat:** Type `/export-trajectory` or `/trajectory`
- Creates trajectory bundle in workspace
- Includes both OpenAI fine-tuning format and raw events

**Programmatic export of all sessions:**
```bash
python3 experiment/scripts/export-all.py
```

## When to Capture
- Session ends with clear goal achieved or abandoned
- 3+ tool calls made (complex reasoning)
- Self-correction or notable reasoning path
- Both good examples and bad (balanced dataset)

## File Layout
```
experiment/traces/
├── text/                    # Pioneer format (text only)
├── trajectory/              # OpenAI format (full tool calls)
├── manifest.jsonl           # Index of all exports
└── README.md               # This file
```

## Toggle
Check `experiment/trace-collector.json` → `enabled` field.

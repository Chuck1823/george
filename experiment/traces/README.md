# experiment/traces/

## Directory structure

```
traces/
├── text/                    # Pioneer-compatible text-only traces
│   ├── 2026-06-30.jsonl
│   └── 2026-07-02.jsonl
├── trajectory/              # Full tool-use traces (OpenAI format)
│   ├── 2026-06-30.jsonl
│   └── 2026-07-02.jsonl
└── manifest.jsonl           # Index of everything captured
```

## What gets captured

Every session with 3+ tool calls or interesting reasoning:
1. **Text trace** — user + assistant text only (Pioneer fine-tuning)
2. **Trajectory trace** — full tool calls, results, thinking (agentic training)
3. **Manifest entry** — what happened, quality rating, session ID

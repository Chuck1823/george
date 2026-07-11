# Dataset Format: Agentic Reasoning Traces

## Primary Format: JSONL (OpenAI-Compatible)

Every major fine-tuning API (OpenAI, Anthropic, Together, Fireworks, etc.) accepts:

```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

## Three Export Tracks

### Track 1: SFT (Chat SFT)
- Clean user/assistant alternation, system prompt prepended
- No tool calls, no reasoning blocks
- Compatible with: OpenAI, Together, Fireworks, Axolotl, Unsloth, LLaMA-Factory, Pioneer
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "What's the weather?"},
    {"role": "assistant", "content": "Let me check..."}
  ],
  "quality": "good",
  "score": 4.5,
  "labels": ["extended_dialogue"],
  "task_type": "research",
  "metadata": {"tools_used": ["web_search", "web_fetch"], "thinking_blocks": 5, "has_recovered_from_error": false}
}
```

### Track 2: Agentic (Tool Calls)
- Full OpenAI format: assistant messages include `tool_calls` field, tool results use role=tool
- Compatible with: OpenAI fine-tuning, Together, Fireworks, vLLM
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "Fix this bug"},
    {"role": "assistant", "content": "Let me read the file...", "tool_calls": [{"id": "...", "type": "function", "function": {"name": "read", "arguments": "{\"path\": \"main.py\"}"}}]},
    {"role": "tool", "content": "class Foo:...", "tool_call_id": "..."},
    {"role": "assistant", "content": "Found it. The issue is..."}
  ],
  "quality": "great",
  "score": 6.0,
  "labels": ["deep_reasoning", "self_correction"],
  "task_type": "coding"
}
```

### Track 3: Distill (SFT + Reasoning)
- SFT + reasoning field on assistant messages
- Before teacher grading: reasoning = agent's raw thinking blocks
- After teacher grading: reasoning = enriched reasoning from premium teacher model
- Compatible with: Pioneer API, models that support reasoning_content / thinking
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..." },
    {"role": "assistant", "content": "The fix is...", "reasoning": "The user needs X. I should first check Y. Option A would work but has downside Z, so option B is better because..."}
  ],
  "quality": "great",
  "teacher_quality": "great",
  "enriched_by": "claude-opus-4-2026-01",
  "score": 8.5,
  "labels": ["deep_reasoning", "diverse_tools", "self_correction"],
  "task_type": "devops",
  "metadata": {"tools_used": ["exec", "write", "read"], "thinking_blocks": 12, "has_recovered_from_error": true}
}
```

## Teacher Grading

A premium teacher model (Claude/GPT) grades each trace independently:

1. **Quality label**: great/good/mediocre/poor (independent assessment)
2. **Enriched reasoning**: rewrites the reasoning field to show what a stronger model would think at each step — alternatives considered, uncertainty expressed, decision rationale

The enriched reasoning is the distillation signal (Hinton approach: teacher's output distribution is richer than just answers).

## Quality Labels

- **great**: Excellent reasoning, correct tool usage, optimal path, good self-correction
- **good**: Solid execution, minor inefficiencies
- **mediocre**: Gets there but takes wrong turns, inefficient
- **poor**: Failed or produced incorrect output, useful negative example

Both great and poor examples are valuable for fine-tuning.

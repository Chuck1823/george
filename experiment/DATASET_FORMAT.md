# Dataset Format: Agentic Reasoning Traces

## Primary Format: JSONL (OpenAI-Compatible)

Most fine-tuning APIs (OpenAI, Anthropic, Together, Fireworks, etc.) accept JSONL with the `messages` format:

```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

This IS the most widely supported format. Every major fine-tuning API accepts it.

## Extended Format for Reasoning Traces

For distillation of agentic reasoning, we also capture intermediate thinking/reasoning. Some APIs support a `reasoning` or `thinking` field:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "reasoning_content": "..."
}
```

## Dataset Structure

Each sample captures one agent trajectory:

```json
{
  "id": "trace-YYYY-MM-DD-NNN",
  "messages": [
    {"role": "system", "content": "<full system prompt>"},
    {"role": "user", "content": "<user message>"},
    {"role": "assistant", "content": "<final response>", "reasoning": "<internal reasoning trace>"}
  ],
  "metadata": {
    "timestamp": "ISO 8601",
    "model": "model identifier",
    "tools_used": ["tool1", "tool2"],
    "quality": "great|good|mediocre|poor",
    "task_type": "reasoning|coding|analysis|creative|assistant|etc",
    "notes": "brief notes on why this trajectory is good/poor"
  }
}
```

## Quality Labels

- **great**: Excellent reasoning, correct tool usage, optimal path, good self-correction
- **good**: Solid execution, minor inefficiencies
- **mediocre**: Gets there but takes wrong turns, inefficient, could be better
- **poor**: Failed or produced incorrect output, useful negative example

Both great and poor examples are valuable for fine-tuning.

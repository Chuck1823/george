# Dual-Track Trace Capture System

## Two datasets, every qualifying session

### Track 1: Text-only (Pioneer-compatible)
Format: `{"messages": [{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}`

Use: Fine-tuning reasoning quality, general conversation skills
Target models: Pioneer (Qwen/Llama small models), Hugging Face

### Track 2: Full trajectory (OpenAI tool_calls format)  
Format: `{"messages": [
  {"role":"user","content":"..."},
  {"role":"assistant","content":"...","tool_calls":[{"type":"function","function":{"name":"...","arguments":"..."}}]},
  {"role":"tool","content":"...","tool_call_id":"..."},
  {"role":"assistant","content":"..."}
]}`

Use: Fine-tuning tool-use, agentic routing, function calling
Target: OpenAI, Anthropic, Together AI, local training with TRL/axolotl

## When to capture
- Session ends with a clear goal achieved or abandoned
- 3+ tool calls made
- Self-correction or notable reasoning path
- Clear good OR bad example (balanced dataset)

## Export script
`scripts/export-traces.py` — reads OpenClaw session JSONL, writes both formats

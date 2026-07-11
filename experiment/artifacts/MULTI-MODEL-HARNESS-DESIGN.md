# Multi-Model Agentic Harness — Design Reference

## Purpose
Orchestrate multiple local small models (router, synthesizer, memory compressor,
entity extractor) as a multi-model agentic harness on home GPU.

## Architecture

### Model Roles

| Role | Size | Purpose |
|---|---|---|
| Router | 7B-8B | Classify intent, decide which model(s) to call |
| Synthesizer | 7B-8B | Generate final response to user |
| Memory Compressor | 1B-3B | Summarize/compact daily logs into MEMORY.md |
| Entity Extractor | 300M-1B | GLiNER or similar for structured data extraction |
| Text Classifier | 300M-1B | Classify incoming messages by type/urgency |

### Execution Flow
1. Router receives user message → classifies intent
2. Based on intent, dispatch to specialized model(s):
   - Simple question → Synthesizer only
   - Memory-heavy task → Memory Compressor → Synthesizer
   - Structured data request → Entity Extractor → Synthesizer
3. Collect outputs → merge → deliver to user

### Target
- RTX 4090 (24GB VRAM) with Ollama or llama.cpp
- Keep 3-4 models in VRAM simultaneously
- Fall back to OpenRouter if local model produces poor output
- Continue capturing traces even after migration for ongoing self-improvement

## Current State
Still in dogfooding phase. No GPU rig yet. Continue using OpenRouter and capturing traces via trace distillation pipeline.

---

Saved as a reference artifact, not a skill. To be activated when GPU rig is operational.

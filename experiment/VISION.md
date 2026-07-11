# The Vision

**Privacy-first, self-improving personal AI for every household.**

## Core Principles
- Everything stays on your hardware
- No data leaves your home
- Self-contained self-improvement
- Gets to know your family over time

## Architecture
- Compact GPU rig (NCore 100 Max + RTX 4090 or equivalent) in every home
- Local models (7B-8B) via Ollama/vLLM
- Fine-tuned via distillation from premium teacher models
- Custom OpenClaw fork with built-in memory & self-improvement
- Weights published to HuggingFace, downloaded via one-line bootstrap

## Business Model (Phase 1)
- Manual installation service
- We go to their home, set up the rig, install everything
- Monthly support fee for updates, troubleshooting
- Remote support access ONLY for maintenance (gateway restart, etc.)
- All user data stays on their hardware — we can't see it

## Phase 1 Scope
- Static distilled model (no self-improving loop yet)
- Strong local memory system (compression, search, recall)
- Access to all tools OpenClaw provides (code, files, web, email, calendar, etc.)
- Proven distillation pipeline running on our own hardware

## Phase 2 Goals
- On-device self-improving loop (customer rig adapts locally)
- Model updates published to HuggingFace, auto-updated on rigs
- Self-service installation (no manual setup needed)
- Scalable distribution

## Key Technical Decisions
- Phase 1: distillation loop runs on founder's infra, weights published publicly
- Phase 1: customers use static model updates, no local fine-tuning
- Memory + search replaces self-improvement for customer adaptation in Phase 1
- GPU targets: RTX 4090 24GB (best balance of VRAM, size, price)
- Model targets: 7B-8B quantized (Qwen2.5, Llama 3.x)

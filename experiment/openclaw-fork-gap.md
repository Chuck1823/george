# OpenClaw vs "The Desk" — What Already Exists vs What to Build

## ✅ OpenClaw Already Provides (Ship Day 1)
- **Gateway daemon** — single process owning messaging, agent runs, scheduling, state
- **WhatsApp/Telegram/Discord/Slack/Signal/iMessage + 15 more channels** — multi-account, DM isolation, group routing
- **Agent runtime** — model loop, tool execution, streaming, compaction, retries, fallback chains
- **Session management** — routing, isolation, daily/idle reset, compaction, write locks, JSONL transcripts
- **20+ agent tools** — exec (with sandbox + approvals), read/write/edit, web search/fetch, memory (semantic), cron from chat, sub-agents, image/video/music gen, TTS, goals
- **Automation** — cron (SQLite-backed, recurring + one-shot, timezone-aware, webhook/Gmail integration), heartbeat (periodic check-ins with task blocks), lifecycle hooks
- **Memory** — file-based (MEMORY.md, daily notes) + semantic search (hybrid vector/keyword) + auto-flush before compaction + optional dreaming
- **Skills** — SKILL.md system, Workshop proposal lifecycle, ClawHub marketplace, 50+ bundled skills
- **Multi-agent** — isolated agents with separate workspaces/state/sessions, deterministic routing bindings, per-agent sandbox + tool policies
- **Config** — JSON5 config, model auth profiles, sandbox, tool allow/deny
- **Observability** — OpenTelemetry, Prometheus, structured logging

**~80% of infrastructure is production-ready.**

## 🔨 The Desk Must Build (Product Layer)
- **Onboarding** — guided, friendly setup (currently CLI-first)
- **Admin UI** — web dashboard for managing agents, channels, cron, memory
- **Billing/subscription** — Stripe integration for SaaS pricing
- **Multi-tenant SaaS** — true user isolation, data separation, resource limits (current multi-agent is single-owner)
- **Branding** — rename, logo, tone from "OpenClaw" to "The Desk"
- **Simplified config** — flatten JSON5 into human-friendly forms
- **Template library** — pre-built personas with example configs
- **Mobile app** — iOS/Android companion (optional)

**~20% of work, but it's the product-facing layer that makes it consumer-ready.**

## Bottom Line
OpenClaw is the engine. The Desk is the car. The fork is a **productization problem**, not a **capability problem**.

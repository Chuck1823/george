# THE DESK / FAMCLOUD — CANONICAL ARCHITECTURE

> **One source of truth for humans + coding agents.** Concise but comprehensive.

---

## TABLE OF CONTENTS

1. [Vision & Product Overview](#1-vision--product-overview)
2. [Business Model & Pricing](#2-business-model--pricing)
3. [System Architecture](#3-system-architecture)
4. [Per-Box Stack](#4-per-box-stack)
5. [Canonical Schema](#5-canonical-schema)
6. [Trace & Distillation Pipeline](#6-trace--distillation-pipeline)
7. [Fleet Management & Oncall](#7-fleet-management--oncall)
8. [Integration Strategy](#8-integration-strategy)
9. [Skills Architecture](#9-skills-architecture)
10. [Hardware](#10-hardware)
11. [Open Action Items / Decisions Needed](#11-open-action-items--decisions-needed)

---

## 1. VISION & PRODUCT OVERVIEW

### What It Is

Edge-deployed AI agent platform for **small businesses** (The Desk) and **families** (FamCloud). Each box runs a local model on OpenClaw harness. Canonical skills enforce architecture. One mothership handles distillation.

### Two Products, One Platform

| | The Desk (SMB) | FamCloud (Family) |
|--|--|--|
| **Target** | Nail salons, dry cleaners, barbers, restaurants, auto repair, hair salons | Families, households with kids 5-17 |
| **Agent Role** | Receptionist, booker, inventory tracker, review monitor, daily briefing | Family assistant, homework helper, calendar manager, reminder system |
| **Pitch** | "Never miss a customer call again." | "AI that knows your family. On every app. In your home." |
| **Scale** | ~8 concurrent, ~300 regulars per box | ~4-8 household members |
| **Vertical** | nail_salon, barber, dry_cleaner, restaurant, salon_hair, auto_repair | family (no vertical field) |
| **Channels** | Phone (primary), WhatsApp/SMS, website chat, IG DM, email | WhatsApp, iMessage, Telegram, Discord, email, voice |
| **Key Moat** | Bilingual (KO/VI/EN), local-first, cheap | Cross-platform + privacy + personal context |

### Core Principles

```
1. Simpler is better — SQLite over Postgres, npm over Docker, bash over K8s
2. Skills enforce architecture — agents follow skills, users don't override
3. Offline-capable — boxes work without mothership for days/weeks
4. Structured outputs — PIDL/Protobuf everywhere, no loose JSON
5. Small business scale — ~8 concurrent, ~300 regulars, not enterprise
6. Local-first inference — models run on box GPU, zero cloud AI costs ($0/mo)
7. Data stays on box — all data local, nothing leaves
8. Privacy as differentiator (not the hook) — utility sells, privacy closes
```

### OpenClaw Relationship

OpenClaw = the engine (~80% infrastructure). `@thedesk/openclaw` npm fork = the car (~20% product-facing layer). Fork `openclaw/openclaw` → keep additions in separate dirs → `git pull upstream main` + rebase. CI tests upstream changes don't break additions.

**Already production-ready in OpenClaw:** Gateway daemon, 15+ channel plugins (WhatsApp/Baileys, Telegram/grammY, iMessage/imsg, Signal/signal-cli, SMS/Twilio, Discord, Slack, Email via gog, etc.), agent runtime, session management, memory (SQLite + semantic search), cron scheduler, skills system (SKILL.md + ClawHub), multi-agent, config, sub-agents, heartbeats, webhooks, Canvas UI, OpenTelemetry, Prometheus.

**We build (~20%):** Onboarding UI, billing/subscriptions (Stripe), branding (The Desk/FamCloud), simplified config, distillation pipeline, OTA updates, SMB vertical skills, template library.

### Phases

| Dimension | Phase 1 (Now) | Phase 2 (Future) |
|-----------|---------------|------------------|
| Model | Static distilled downloads from HuggingFace | Per-box LoRA adapters, local adaptation |
| Self-improve | Distillation on founder's infra only | Each rig learns locally, no data leaves |
| Installation | Manual / pre-configured boxes shipped | Self-service install (plug in + wizard) |
| Customer adapts | Memory + RAG (compression, search, recall) | On-box LoRA re-training nightly |
| Distillation | Proven pipeline on our hardware | Self-service, auto model updates |

---

## 2. BUSINESS MODEL & PRICING

### SMB Pricing (The Desk)

| Tier | Upfront | Monthly | What They Get | Payback at $400 rig |
|------|---------|---------|---------------|---------------------|
| Starter | $150 | $40 | Phone answering + WhatsApp + FAQs + booking | ~7 mo |
| Business | $200 | $65 | + reminders + reviews + bilingual | ~4 mo |
| Growth | $300 | $95 | + retention + POS + IG DM + analytics | ~3 mo |
| Lease | $0 | $85 | Full Business, box leased, return if cancel | ~5 mo |

### Family Pricing (FamCloud)

| Tier | Upfront | Monthly | What They Get | Payback at $400 rig |
|------|---------|---------|---------------|---------------------|
| Basic | $100 | $30 | Text only (WhatsApp/Tel), 7B model, memory 30d, ≤2 members | ~11 mo |
| Pro | $150 | $50 | + voice (Pipecat), 14B model, Google integrations, homework help | ~5 mo |
| Premium | $275 | $75 | Everything + LoRA adapter, priority support, personalized model | ~2 mo |
| Lease | $0 | $65 | Pro features, box leased, 12-month commitment | ~6 mo |

**Sweet spot: $150 upfront + $50/month Pro tier.**

### Unit Economics

```
Hardware: ~$400 per box (used OptiPlex + RTX 3060)
Monthly ops per household: $2-6 (shared phone amortized + domain)
AI inference: $0/month (runs local on box GPU)

KEY INSIGHT: Hardware is a one-time CAC, not recurring cost.
Year 1 margins low (1-61%) — hardware eats them.
Year 2+: ~91% margins (hardware paid off, pure recurring).
Same model as SaaS: Adobe 95%, SaaS 80-95%.
```

### Revenue Scale (Mixed Tiers)

| Customers | Year 1 Revenue | Year 2+ Recurring | Year 2+ Profit |
|-----------|---------------|-------------------|----------------|
| 50 | ~$28K | ~$25K | ~$22K |
| 100 | ~$57K | ~$51K | ~$48K |
| 200 | ~$114K | ~$103K | ~$100K |
| 500 | ~$285K | ~$260K | ~$255K |
| 2K | ~$1.34M | ~$1.06M | ~$1M+ (S-Corp saves ~$60K/yr) |

At 2K customers: acquisition value $4M-7M (MicroAcquire) or $10M-21M (strategic buyer). Or keep forever → $730K-770K/yr take-home.

### Go-To-Market

Phase 1 (mo 1-3): Friends/family (5-10), $0 CAC. Phase 2 (mo 3-6): Word of mouth + referrals ($50 credit each side), 20-30. Phase 3 (mo 6-12): Organic content (Twitter/X, YouTube, Reddit r/selfhosted/r/LocalLLaMA, HN), 30-50. Phase 4 (mo 12+): Paid ads at scale ($50 blended CAC).

**SMB Wedge — Nail Salons:** NJ has ~3,000+. Walk-in demo, free 30-day trial, $40/mo Starter. Bilingual (KO/VI/EN) is a moat. Standard services, repeat customers, owners talk. ROI: "Catches 2 missed calls/week = $80 → $40/mo pays."

### Legal Path

Sole proprietor (now) → LLC at 10+ customers → LLC+S-Corp at $30K+/yr profit. NOT VC — revenue too small ($100M+ needed), diluted ownership, extreme pressure. Bootstrap/lifestyle preferred.

---

## 3. SYSTEM ARCHITECTURE

### High-Level Diagram

```
┌──────────────────────────────────────────────────────────┐
│                     MOTHERSHIP (Founders)                 │
│  (Mac mini with 32B model / GPU VM)                      │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Trace    │→ │ Label    │→ │ Distill  │→ │ Publish  │ │
│  │ Ingest   │  │ (32B)    │  │ (2-3B)   │  │ (Hugging │ │
│  │(anonymiz)│  │           │  │           │  │  Face)   │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                          │
│  OTA orchestration + encrypted backups + health dashboard│
└───────────────┬───────────────────┬──────────────────────┘
                │ Tailscale VPN      │ HTTPS/OTA
       ┌────────┴──────┐       ┌────┴─────────┐
       │   Box #1       │       │   Box #N      │
       │ OpenClaw       │       │ OpenClaw      │
       │ Gateway        │       │ Gateway       │
       │ SQLite(WAL)    │       │ SQLite(WAL)   │
       | ChromaDB       │       | ChromaDB      │
       │ Ollama/vLLM    │       │ Ollama/vLLM   │
       │ (Qwen 2-3B Q4) │       │ (Qwen 2-3B Q4)│
       │ Channels       │       │ Channels      │
       └────┬───────────┘       └────┬──────────┘
            │                        │
       WhatsApp/Tel              WhatsApp/Tel
```

### Box-to-Mothership

- **Trace sync:** anonymized (PII stripped, IDs hashed), HTTPS POST
- **Backup:** nightly encrypted SQLite dump → mothership
- **Model update:** mothership notifies, box pulls from HuggingFace
- **Health:** every 5 min → mothership dashboard

### Mothership Functions

1. Trace ingestion (PII stripped, IDs hashed)
2. Labeling via 32B model (classifies vertical, capability, quality score)
3. Distillation (trains 2-3B model from labeled traces)
4. Publish GGUF to HuggingFace
5. OTA orchestration (notify all boxes of new version)
6. Encrypted backup aggregation (nightly SQLite dumps)
7. Health dashboard for all fleet boxes

---

## 4. PER-BOX STACK

### What Runs on Each

| Component | Technology | Purpose |
|-----------|------------|---------|
| Node.js | `@thedesk/openclaw` npm package | Agent harness (our OpenClaw fork) |
| SQLite (WAL mode) | Embedded DB | Canonical schema (Customer, Booking, Service, Inventory, Staff, Reminder, Business) |
| Local model | Ollama or vLLM | Distilled Qwen 2-3B, Q4/Q5 quantized, from HuggingFace |
| Tailscale | VPN | Fleet SSH, zero open ports, device identity per box |
| Gateway daemon | OpenClaw | Messaging, agent runs, scheduling, agent state |
| Canvas UI | Web dashboard | Local config (18789 or Tailscale IP) — SMB owner/household |
| Pipecat (Phase 2) | Voice | Whisper STT → local LLM → Kokoro TTS (all local, $0/mo) |

### deploy-all.sh — One-Command Provisioning

```bash
# Idempotent. Installs everything on a fresh Ubuntu box.
curl -sL https://deploy.thedesk.ai/deploy-all.sh | bash
```

Steps: (1) Install Node.js + npm (2) `npm install @thedesk/openclaw` (3) Download model weights from HuggingFace (4) Create SQLite + run canonical schema migration (5) Install Tailscale + join fleet network (6) Configure OpenClaw with canonical skills (7) Start gateway daemon (8) Health check → report online to mothership.

### Update Flow

- **npm update:** `openclaw update` → gateway restarts → health check → auto-rollback if fail
- **Model OTA:** (nightly cron) check HuggingFace for new weight hash → download → test against 20 saved queries → swap if better → rollback if worse → zero downtime (old model stays active until new passes)
- **No Docker, no K8s — npm + bash scripts.**

### Config / Onboarding

No mobile app. Each box serves a web dashboard. Config through guided skill prompts: "What's your business name?" → canonical config set. "What are your hours?" → schedule set. "What services?" → service catalog. Agent handles config behind the scenes.

### Shared Infrastructure (One Instance, All HH)

| Service | Cost | Notes |
|---------|------|-------|
| Discord umbrella bot | FREE | One bot, filters by server |
| Slack umbrella app | FREE | One app, installs to each workspace |
| famcloud.ai domain | $15/yr ($1.25/mo amortized) | Cloudflare Email Routing (free) |
| Shared phone (Photon Business) | $250/mo ÷ N HH | iMessage+SMS+voice. $2.50/HH at 100, $0.50/HH at 500 |
| VPS for updates | ~$10-20/mo total | Hosts update notifications |
| SSH bastion (Tailscale) | ~$5/mo total | Remote support |

Total ops per household: $2-6/month at 100+ scale.

---

## 5. CANONICAL SCHEMA

### Entities (PIDL/Protobuf — Single Source of Truth)

Bindings generated in Rust (telemetry), Python (ML), TypeScript (agent + Canvas UI).

```yaml
Business:
  id: uuid
  name: string
  vertical: string              # nail_salon|barber|dry_cleaner|restaurant|salon_hair|auto_repair|family
  timezone: string              # default America/New_York
  hours: ServiceHour[]
  phone: string
  website: string?

ServiceHour:
  day: mon|tue|wed|thu|fri|sat|sun
  open: string
  close: string

Customer:
  id: uuid
  phone: string?
  email: string?
  name: string?
  business_id: uuid             → Business.id
  created_at: timestamp
  last_seen_at: timestamp?

Service:
  id: uuid
  name: string
  duration_min: int
  price_cents: int
  category: string?
  business_id: uuid             → Business.id

Booking:
  id: uuid
  customer_id: uuid             → Customer.id
  service_id: uuid              → Service.id
  staff_id: uuid?               → Staff.id
  datetime: timestamp
  status: booked|confirmed|completed|cancelled|no_show
  channel: whatsapp|telegram|sms|voice|email|imessage|discord

Staff:
  id: uuid
  name: string
  role: string?
  schedule: ServiceHour[]?
  contact: string?

Inventory:
  id: uuid
  name: string
  quantity: int
  unit: string?
  reorder_threshold: int
  last_reorder: timestamp?

Reminder:
  id: uuid
  booking_id: uuid              → Booking.id
  scheduled_at: timestamp
  sent_at: timestamp?
  channel: sms|whatsapp|telegram|email
  status: pending|sent|failed
```

### SQLite Implementation (Box-Level)

WAL mode enabled. Skills embed fixed SQL. SQL Agent generates safe constrained ad-hoc queries, validated against canonical schema — can't break things. Read-only by default. No DROP/ALTER/INSERT outside admin skill.

```sql
PRAGMA journal_mode = WAL;

business     (id TEXT PK, name TEXT, vertical TEXT, timezone TEXT, hours TEXT, phone TEXT, website TEXT)
customer     (id TEXT PK, phone TEXT, email TEXT, name TEXT, business_id TEXT REFERENCES business(id), created_at INT, last_seen_at INT)
service      (id TEXT PK, name TEXT NOT NULL, duration_min INT NOT NULL DEFAULT 30, price_cents INT, category TEXT, business_id TEXT REFERENCES business(id))
booking      (id TEXT PK, customer_id TEXT REFERENCES customer(id), service_id TEXT REFERENCES service(id), staff_id TEXT REFERENCES staff(id), datetime INT, status TEXT DEFAULT 'booked', channel TEXT)
staff        (id TEXT PK, name TEXT NOT NULL, role TEXT, schedule TEXT, contact TEXT)
inventory    (id TEXT PK, name TEXT NOT NULL, quantity INT DEFAULT 0, unit TEXT, reorder_threshold INT DEFAULT 5, last_reorder INT)
reminder     (id TEXT PK, booking_id TEXT REFERENCES booking(id), scheduled_at INT, sent_at INT, channel TEXT, status TEXT DEFAULT 'pending')
```

### Knowledge Graph (FamCloud)

Local SQLite + NetworkX per household: people, relationships, events, preferences, facts, patterns. Extracted async from conversations via LLM. ~1-5MB per family. Query: `query_events(person?, timeframe?)`, `query_people(person?)`, `query_relationships(p1, p2?)`, `query_preferences(person?)`.

### Vertical Service Catalog (`verticals/registry.jsonl`)

| Vertical | Services | Hours |
|----------|----------|-------|
| nail_salon | manicure, pedicure, gel, acrylic full/fill, nail art, dip powder, SNS, shellac | 9-7 |
| barber | men's cut, beard trim, hot towel shave, line-up, fade, taper, scissor | 9-6 |
| dry_cleaner | dry clean, press shirt, alter hem, stain removal, leather, tailoring | 7-6 |
| restaurant | dine-in, takeout, catering, delivery, private dining, happy hour | 11-10 |
| salon_hair | cut+style, blowout, balayage, highlights, keratin, extensions, updo | 9-8 |
| auto_repair | oil change, brake inspection, tire rotation, state inspection | 8-5 |

---

## 6. TRACE & DISTILLATION PIPELINE

### Three Export Tracks (JSONL)

| Track | Format | Compatible With |
|-------|--------|-----------------|
| **SFT** | `messages[{role,content}]` system+user+assistant | OpenAI, Together, Fireworks, Unsloth, LLaMA-Factory, Pioneer |
| **Agentic** | Full tool_calls + tool results (OpenAI format) | OpenAI FT, Together, Fireworks, vLLM |
| **Distill** | SFT + `reasoning` field on assistant messages | Pioneer API, reasoning_content/thinking models |

Before teacher: `reasoning` = agent's raw thinking.
After teacher: `reasoning` = enriched reasoning with alternatives, uncertainty, decision rationale.

### Auto Quality Scoring

| Signal | Threshold |
|--------|-----------|
| deep_reasoning | 10+ tool calls |
| moderate_reasoning | 5+ tool calls |
| diverse_tools | 5+ unique tools |
| extended_dialogue | 5+ user turns |
| deep_thinking | 10+ thinking blocks |
| self_correction | error+recovery (+2 pts) |

Score: ≥6.0 = great, ≥3.5 = good, ≥1.5 = mediocre, <1.5 = poor. Both great AND poor have training value.

### Teacher Grading (`scripts/teacher-grade.py`)

Premium teacher model (Claude Opus / GPT-4o) grades each trace AND produces enriched reasoning traces. This is the Hinton distillation signal — teacher output distribution is richer than binary.

### Pipeline Steps

```
1. export-all.py → SFT + Agentic + Distill JSONL
2. Auto-quality score each trace
3. teacher-grade.py → independent labels + enriched reasoning
4. Aggregate (filter great+good, weight by score)
5. Distill: LoRA fine-tune 2-3B (Llama 3.2 3B, Qwen2.5 7B, Qwen3 4B)
6. Upload to HuggingFace (GGUF)
7. OTA: mothership notifies boxes → download → test 20 queries → swap if better
```

### Trace Files

```
experiment/traces/
├── sft/         # Universal fine-tuning
├── agentic/     # Full tool_calls
├── distill/     # SFT + reasoning
├── text/        # Text-only (legacy)
├── trajectory/  # OpenAI FT format
├── manifest.jsonl
└── README.md
```

394 total traces (118 agentic, 66 distill, 118 sft, 92 text).

### Trace Collection Toggle

```json
{"enabled": true, "mode": "quality", "minComplexity": 3}
```
Quality mode = only 3+ tool calls + 2+ user turns.

---

## 7. FLEET MANAGEMENT & ONCALL

### Tailscale Fleet

Every box joins Tailscale → secure SSH, zero open ports, device identity per box. Remote support only via Tailscale.

### Health Monitor (5-min cron per box)

Check: Gateway HTTP 200, model inference test, disk usage (>80% warn), memory, GPU (nvidia-smi), network. Auto-recover on failure → alert mothership → create ticket.

### Support Agent Flow

User reports issue → Support agent (mothership) → SSH health check → Categorize (hw/sw/model/channel) → Create ticket → Route: Tier 1 (auto-fix) / Tier 2 (human) / Tier 3 (hardware RMA).

### Backup & Disaster Recovery

Nightly encrypted SQLite dumps → mothership. Box dies → deploy-all.sh + restore backup. Model weights on HuggingFace → always downloadable. Mothership down → boxes work fully offline for days/weeks.

---

## 8. INTEGRATION STRATEGY

### Channel Connectivity

1. Setup at `localhost:18789` or Tailscale IP
2. QR scan for WhatsApp (Baileys)
3. Bot token for Telegram (@BotFather)
4. OAuth for email/Google services
5. Invite link for Slack/Discord

### Channel Costs

| Channel | Cost | Support | Setup |
|---------|------|---------|-------|
| WhatsApp (Baileys QR) | FREE | ✅ Native | QR scan with phone |
| Telegram (grammY) | FREE | ✅ Native | BotFather → token paste |
| Discord bot | FREE | ✅ Native | Dev Portal → invite to server |
| Slack bot | FREE | ✅ Native | Slack API → install to workspace |
| Signal (signal-cli) | FREE | ✅ Native | Register + captcha |
| SMS (Twilio) | $1-2/mo | ✅ Native | Twilio account + number |
| iMessage (imsg) | FREE (needs macOS) | Via imsg CLI | macOS host OR AgentPhone |
| Email (gog/Google) | FREE | gog plugin | OAuth → Gmail/Calendar/Drive |

### Shared Number Strategy (Photon)

| Tier | Cost | Max | Per-HH at 100 |
|------|------|-----|---------------|
| Photon Free | FREE | 10 users | — |
| Photon Pro | $25/mo | 100 users | $0.50/HH |
| Photon Business | $250/mo | Unlimited | $2.50/HH ($0.50 at 500) |

One dedicated number shared across all HHs, routed by sender identity. AgentPhone alternative: unified phone+iMessage+SMS+voice, pay-as-you-go.

**Total ops per HH: $2-6/month.**

---

## 9. SKILLS ARCHITECTURE

### Canonical Skills (Every Box)

| Skill | Purpose | SQL |
|-------|---------|-----|
| **Front Office** | Booking, inquiry, no-show, retention | Embedded fixed SQL |
| **Back Office** | Inventory, schedule, compliance, reporting | Embedded fixed SQL |
| **Admin** | DB migrations, auth, config | No |
| **SQL Agent** | Safe constrained ad-hoc SQL | Generated, validated |

Skills are `SKILL.md` files. Auto-discovered via `<available_skills>` at startup. Agent reads when task matches. Re-reads if version changed. Lifecycle: `create` → `revise` → `inspect` → `apply`/`reject`/`quarantine`.

### SQL Agent Guardrails

Constrained to canonical schema. Read-only by default. No DROP/ALTER/INSERT outside admin skill. Can't break things.

### Knowledge Graph Skill (FamCloud)

Tools: `query_events`, `query_people`, `query_relationships`, `query_preferences`, `add_entity`, `update_entity`, `weekly_summary`. Extraction async from messages. Feeds LoRA for Premium tier.

### Premium Differentiator

Premium ($75/mo): LoRA adapter per HH. Model fine-tuned on their data, local storage. KG feeds training. Custom personality. Nightly updates.

---

## 10. HARDWARE

### Budget Path: Used OptiPlex + RTX 3060 (~$375-485)

| Component | Spec | Used Price |
|-----------|------|-----------|
| Dell OptiPlex 7090 MT | i7-10700, 16GB DDR4, 256GB SSD | $200-250 |
| RTX 3060 12GB | Standard height | $150-200 |
| 500GB NVMe SSD | optional upgrade | $25-35 |
| **Total** | | **$375-485** |

RTX 3060 12GB is the sweet spot. 170W TDP fits OptiPlex PSU. Enterprise parts at surplus prices.

### Model Size vs VRAM

| Model | VRAM | Speed | Verdict |
|-------|------|-------|---------|
| Qwen 14B Q4 | ~8-9GB | 15-20 tok/s | ✅ Sweet spot |
| Qwen 14B Q5 | ~10-11GB | 12-15 tok/s | ✅ Max usable |
| Qwen 7B Q4 | ~4-5GB | 25-35 tok/s | Fast, OK quality |

### Mac Mini Dev/Test

Mac mini 16GB RAM, Intel i3 → runs Qwen 7B via Ollama (CPU, ~2-3 tok/s). Good for bootstrap/stack validation before buying hardware.

### Hardware Longevity

3-5 years realistic for used parts. Amortized at $400 / 5yr = ~$6.67/mo.

---

## 11. OPEN ACTION ITEMS / DECISIONS NEEDED

### 🔴 Contradictions / Resolved

**1. Model size on boxes: HAS SHIFTED**
- REPO_ARCHITECTURE: "2-3B distilled"
- VISION.md: "7B-8B quantized"
- HARDWARE docs: "14B on RTX 3060"
- Pricing: Basic=7B, Pro=14B
- **Decision:** Start Phase 1 with 7B Q4 (proven good on 12GB, no distillation needed yet). Move to distilled 2-3B in Phase 2 once pipeline proven.

**2. Container vs npm: RESOLVED** → npm (`deploy-all.sh`, no Docker/K8s)
**3. SQLite vs Postgres: RESOLVED** → SQLite WAL mode
**4. Multi-tenant SaaS vs single-tenant edge: RESOLVED** → single-tenant edge

### 🟡 Open Decisions

**5. Brand name:** Docs reference Hearth, Kin, Oikos, Vell, The Desk, FamCloud → need one company name + two product names.
**6. Shared phone vendor:** AgentPhone was original → Photon now preferred. AgentPhone may add WhatsApp later. Need commitment.
**7. First vertical to pilot:** Nail salon strategy is most developed but not started → need to commit and visit 5-10 shops.
**8. Pipecat voice validation:** Needs real-world testing before Phase 2 commitment. Local Whisper+LLM+TTS performance unknown at scale.
**9. Self-serve onboarding completeness:** Currently manual install → need to build and test full wizard before Phase 1 launch.
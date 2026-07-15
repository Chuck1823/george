# The Desk — Canonical Architecture

## 1. Vision & Product

**Edge-deployed AI agent platform for small businesses.** One box per business, local model, zero cloud dependency for core operations. The agent handles the front desk — phone answering, booking, customer inquiries, reminders — across WhatsApp, phone, iMessage, etc. It connects to the business's existing tools (QuickBooks, Square, Google Calendar, POS) rather than replacing them.

**Scale:** 8 concurrent clients per box, ~300 regulars. Not enterprise.

## 2. Business Model & Pricing

### Tiers (SMB)
| Tier | Upfront | Monthly | Target |
|------|---------|---------|--------|
| Starter | $60 + $170 setup | $60 | Text-only |
| Business | $85 + $220 setup | $85 | Full feature |
| Growth | $115 + $320 setup | $115 | Multi-channel + analytics |
| Lease | $0 | $100/mo 12mo min | No upfront, hardware return |

**Hardware cost:** ~$400/rig (Dell OptiPlex MT + RTX 3060 12GB). Setup fee offsets hardware cost. Setup fee = hardware cost recovery.

## 3. System Architecture

### Edge Box (Per Business)
```
┌─────────────────────────────────────────┐
│           The Desk Box                  │
│  ┌───────────────────────────────────┐  │
│  │        OpenClaw Gateway           │  │  ← Agent runtime, messaging
│  └──────────────┬────────────────────┘  │
│                 │                       │
│  ┌──────────────▼────────────────────┐  │
│  │    Local Model (vLLM/Ollama)      │  │  ← 14B quantized, from HF
│  └──────────────┬────────────────────┘  │
│                 │                       │
│  ┌──────────────▼────────────────────┐  │
│  │    SQLite (canonical schema)      │  │  ← Customer, Booking, Service
│  └──────────────┬────────────────────┘  │
│                 │                       │
│  ┌──────────────▼────────────────────┐  │
│  │    Tailscale (fleet SSH)          │  │  ← Zero open ports
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```
**Components:**
- **Runtime:** Node.js → `@thedesk/openclaw` (npm package, our fork)
- **Model:** 14B quantized, downloaded from HuggingFace
- **Database:** SQLite WAL mode with canonical schema
- **Network:** Tailscale for fleet SSH, no open ports
- **Gateway:** OpenClaw with WhatsApp, phone, iMessage
- **UI:** Canvas web dashboard (served locally)

### Mothership (Distillation Hub)
- High-RAM machine running 32B model for trace enrichment
- Receives anonymized traces from all boxes
- Labels, grades, distills → publishes 14B model to HuggingFace
- Nightly SQLite backups from all boxes (encrypted `scp`)
- Orchestrates OTA updates

### Model Delivery
- From HuggingFace → boxes pull via cron or OTA trigger
- Health check + auto-rollback on failure
- Same update mechanism as OpenClaw (npm)

## 4. Per-Box Stack

### deploy-all.sh (One Command)
```bash
curl -sL https://raw.githubusercontent.com/mom-and-pop-labs/the-desk/main/setup/deploy-all.sh | bash
```
1. Install Node.js + npm
2. `npm install @thedesk/openclaw`
3. Download model weights from HuggingFace
4. Create SQLite + run canonical schema migration
5. Install Tailscale + join fleet
6. Configure OpenClaw with canonical skills
7. Start gateway daemon
8. Health check → ping mothership

### Updates
- `openclaw update` pulls new npm version
- Health check + auto-rollback on failure
- No Docker, no K8s

## 5. Canonical Schema

Single source of truth. Generated bindings via Protobuf for TypeScript (agent + frontend), Python (ML pipeline), Rust (telemetry).

```
Customer:     id, phone, email, name, business_id, created_at, last_seen_at
Booking:      id, customer_id, service_id, staff_id, datetime, status, channel
Service:      id, name, duration_min, price, category
Inventory:    id, name, quantity, unit, reorder_threshold, last_reorder
Staff:        id, name, role, schedule, contact
Reminder:     id, booking_id, scheduled_at, sent_at, channel, status
Business:     id, name, vertical, hours, timezone
```

SQLite WAL mode. Enough for 8 concurrent clients, 300 regulars. Nightly backup to mothership.

## 6. Trace & Distillation Pipeline

### Trace Collection
- OpenClaw captures JSONL session transcripts automatically
- Weekly export produces: `sft/`, `agentic/`, `distill/` tracks

### Auto-Labeling
- `classify-traces.py` sends last 12 messages through OpenRouter to label
- Fixed label set prevents drift
- Twice weekly cron (Mon + Wed 10am ET)

### Flow
Box → Anonymize → Mothership → Label (32B) → Distill → Publish 14B to HF → Boxes pull

## 7. Fleet Management & Oncall

### Health Monitoring
- Use OpenClaw's existing OTel + Prometheus + structured logging
- Boxes phone home via Tailscale
- If a box goes silent → flag for investigation

### Oncall Agents
- Fleet agents SSH into boxes via Tailscale
- Diagnose, fix, restart, rollback

### Disaster Recovery
- Nightly SQLite backup to mothership (encrypted)
- Box dies → `deploy-all.sh` + restore from backup → back online

## 8. Integration Strategy

The Desk is **an integration layer**, not a replacement:
Google Calendar, Gmail, QuickBooks, Square/Toast, Google Business Profile, MindBody/Vagaro, POS systems.

Each integration is a canonical skill.

## 9. Skills Architecture

Skills are the **architecture enforcers**:
- Front Office (booking, inquiries, retention)
- Back Office (inventory, scheduling, compliance)
- Admin (DB migrations, Google auth, Tailscale)
- SQL Agent (constrained ad-hoc queries)

Users can't override architecture.

## 10. Hardware

| Component | Spec | Price |
|-----------|------|-------|
| Dell OptiPlex 7090 MT | i7-10700, 16GB DDR4 | $200-250 |
| RTX 3060 12GB | Used | $150-200 |
| 500GB NVMe | Optional | $25 |
| **Total** | | **$375-475** |

12GB VRAM runs 14B Q4 comfortably.

## 11. Resolved Decisions

| Decision | Resolution |
|----------|-----------|
| SaaS vs edge | Single-tenant edge boxes |
| Postgres vs SQLite | SQLite WAL mode |
| Docker vs npm | npm package update |
| Container vs script | deploy-all.sh |
| Model size | 14B |
| Telemetry | OpenClaw's existing OTel/Prometheus |
| Model delivery | HuggingFace |

## 12. Open Questions

| Question | Context |
|----------|---------|
| Onboarding UI | Canvas works but might need something nicer for SMB |
| Admin panel framework | TypeScript — which framework? |
| Fleet repo name | "fleet", "the-fleet", "ops-fleet"? |
| GitHub org | `mom-and-pop-labs` or different? |
| Brand name | The Desk? Something else? |
| Integration priority | Which tools first? |
| Phone number strategy | One shared vs per-business? |

## 13. Repo Structure (Proposed)
```
mom-and-pop-labs/the-desk/          # monorepo
├── the-desk/                       # OpenClaw fork + harness
│   ├── skills/                     # Canonical skills
│   ├── hardware/                   # BOM
│   └── setup/deploy-all.sh
├── schema/                         # Protobuf
├── distillation/                   # ML pipeline
├── fleet/                          # Ops + oncall
├── mothership/                     # Backup, OTA
├── experiment/                     # Traces, scripts, dashboard
└── docs/                           # Architecture, runbooks
```
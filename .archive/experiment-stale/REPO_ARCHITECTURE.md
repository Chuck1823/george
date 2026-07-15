# The Desk — Architecture

## Overview

Edge-deployed AI agent platform for small businesses (8 concurrent clients, ~300 regulars). Each box runs a local model with OpenClaw as the agent harness, canonical skills enforce architecture, and a single mothership handles distillation.

---

## Per Box (Edge)

### What runs on each box

- **Node.js** → `@thedesk/openclaw` (our fork, npm package)
- **SQLite WAL mode** — canonical schema (Customer, Booking, Service, Inventory, Staff, Reminder)
- **Local model** — 2-3B quantized, downloaded from HuggingFace
- **Tailscale** — secure fleet SSH, zero open ports, device identity per box
- **Gateway daemon** — OpenClaw gateway with messaging surfaces (WhatsApp, Telegram, etc.)
- **Canvas UI** — web dashboard served locally for SMB owner configuration

### `deploy-all.sh` — one command, idempotent

```bash
# Installs everything on a fresh box
curl -sL https://raw.githubusercontent.com/mom-and-pop-labs/the-desk/main/setup/deploy-all.sh | bash
```

1. Installs Node.js + npm
2. `npm install @thedesk/openclaw`
3. Downloads model weights from HuggingFace
4. Creates SQLite + runs canonical schema migration
5. Installs Tailscale + joins fleet network
6. Configures OpenClaw with canonical skills
7. Starts gateway daemon
8. Health check → reports online to mothership

### Updates

- `openclaw update` pulls new npm version
- Gateway restarts automatically
- Health check → if it fails, auto-rollback to previous version
- No Docker, no K8s — just npm and a script

---

## Canonical Schema (PIDL/Protobuf)

Single source of truth, generated bindings in Rust (telemetry), Python (ML), TypeScript (agent harness, frontend).

```
entities:
  Customer:     id, phone, email, name, business_id, created_at, last_seen_at
  Booking:      id, customer_id, service_id, staff_id, datetime, status, channel
  Service:      id, name, duration_min, price, category
  Inventory:    id, name, quantity, unit, reorder_threshold, last_reorder
  Staff:        id, name, role, schedule, contact
  Reminder:     id, booking_id, scheduled_at, sent_at, channel, status
  Business:     id, name, vertical, hours, timezone, timezone
```

---

## Skills Layer

Every box gets the same canonical skills:

- **Front Office**: booking flow, inquiry handling, no-show reduction, customer retention
- **Back Office**: inventory tracking, schedule management, compliance, reporting
- **Admin**: database migrations, Google API auth, Tailscale management, config updates
- **SQL Agent**: generates safe constrained SQL for ad-hoc queries, validated against canonical schema

Skills embed fixed SQL for standard operations. For ad-hoc queries, the SQL Agent generates queries constrained by the schema so it can't break things.

---

## SMB Configuration (Canvas UI)

No mobile app. Each box serves a web dashboard via OpenClaw's Canvas on `localhost:18789` (or via Tailscale IP). The SMB owner opens a browser on any device.

Configuration flows through skills — guided prompts instead of config files:
- "What's your business name?" → canonical config
- "What are your hours?" → schedule set
- "What services do you offer?" → service catalog created

The agent handles the config files behind the scenes.

---

## Mothership (Distillation Hub)

### Runs on a high-RAM Mac mini with a 32B model

1. **Trace ingestion** — boxes send anonymized traces (PII stripped, IDs hashed)
2. **Labeling** — 32B model reads traces and classifies (vertical, capability, quality score)
3. **Distillation** — aggregates labeled data, trains a smaller 2-3B model
4. **Publish** — uploads distilled model weights to HuggingFace
5. **OTA orchestration** — notifies boxes of new model version

### Nightly backups
- Boxes sync their SQLite files to mothership (encrypted)
- If a box dies, restore from backup to a new instance

---

## Repo Structure

```
mom-and-pop-labs/the-desk/          # monorepo
├── the-desk/                       # OpenClaw fork + harness additions
│   ├── package.json
│   ├── src/                        # OpenClaw source
│   ├── skills/                     # Canonical skills
│   ├── hardware/                   # Hardware list, BOM
│   └── setup/                      # deploy-all.sh
├── distillation/                   # ML pipeline
│   ├── label.py                    # Auto-labeling via 32B model
│   ├── train.py                    # Distillation training
│   └── requirements.txt
├── telemetry/                      # Rust telemetry daemon
│   ├── Cargo.toml
│   └── src/
├── schema/                         # PIDL/Protobuf schemas
│   └── canonical.proto
├── fleet/                          # Ops runbooks, SSH tools
│   └── oncall/
├── mothership/                     # Ingestion, backup, deploy coordination
│   └── jobs/
└── docs/                           # Architecture, runbooks
```

---

## Sync with Upstream OpenClaw

- Fork `openclaw/openclaw` into `the-desk/`
- Add `upstream` remote pointing to `openclaw/openclaw`
- Regular `git pull upstream main` and rebase
- Keep our harness additions in separate directories or patches
- CI tests that upstream changes don't break our additions

---

## Principles

- **Simpler is better** — SQLite over Postgres, npm over Docker, bash over K8s
- **Skills enforce architecture** — agents follow skills, users don't override
- **Offline-capable** — boxes work fully without mothership for days/weeks
- **Structured outputs** — PIDL/Protobuf everywhere, no loose JSON
- **Small business scale** — 8 concurrent, 300 regulars, not enterprise
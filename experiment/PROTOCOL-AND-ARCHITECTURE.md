# Protocol & Architecture Analysis — FamCloud / The Desk Platform

> **Date:** 2026-07-15 | **Status:** Draft for Charles review | **Pinned**

---

## What We're Building (Recap)

N independent edge boxes (homes or SMBs), each running a local AI agent, with:
- **Offline-first** — each box works fully standalone for days/weeks
- **Mothership** — distillation hub, OTA model updates, fleet health, backups
- **Multi-channel messaging** — each box handles iMessage, WhatsApp, Telegram, etc.
- **Per-box SQLite** — canonical entity store (customers, bookings, reminders, etc.)
- **Distillation pipeline** — anonymized traces flow edge → mothership → fine-tuned weights → edge

The architecture question: **how does each box communicate with the mothership and (optionally) with other boxes?**

---

## Option A: Simple WebSockets / HTTPS Polling (Current Approach)

### How it works
- Each box runs OpenClaw gateway (already has WebSocket server)
- Mothership calls health check endpoints or boxes POST traces/events on a schedule
- Cron job on each box fires periodic sync

### Pros
- **Already works.** OpenClaw gateway is running this today.
- No new dependency, no new daemon, no new package.
- Simple to understand. `requests.post()` → done.

### Cons
- No event model. Everything is pull or scheduled push.
- No offline queue. If the box is down when cron fires, events are lost unless you build retry logic.
- No real-time mothership → box signaling (model update alerts, config pushes, SOS triggers).
- Doesn't scale elegantly to 500+ boxes with 6 events/minute each.

### Verdict
**Fine for < 10 boxes.** This is what we have today and it's not broken. But it's not an architecture — it's a hack that works.

---

## Option B: MQTT + Broker (HiveMQ, EMQX, Mosquitto)

### How it works
- Mothership runs an MQTT broker
- Each box connects as an MQTT client, publishes to `famcloud/<box_id>/<topic>`
- Boxes subscribe to `famcloud/<box_id>/commands` for mothership → box messages
- MQTT broker handles QoS, offline message queueing, last-will

### Pros
- Built for IoT. Every edge device ever built speaks MQTT.
- **QoS levels:** QoS 1 (at-least-once) and QoS 2 (exactly-once) are built-in. No custom retry.
- **Offline resilience:** Messages queue on the broker, deliver when box reconnects.
- Tiny memory footprint (~5MB for Mosquitto). Can run on the mothership Mac mini.
- TLS everywhere. Per-box client certs for authentication.

### Cons
- New service running on mothership. Brokers are simple but it's still a new thing to maintain.
- Not ideal for large payloads. MQTT is optimized for small messages (< 256KB typically). Trace bundles can be larger.
- Hub-and-spoke only. No box-to-box communication.
- Topic schema is manual. You define `famcloud/<id>/traces`, `famcloud/<id>/health`, etc. No schema enforcement.

### Broker candidates
| Broker | Memory | Docker? | Cluster? | Good for us? |
|--------|--------|---------|----------|-------------|
| **Mosquitto** | ~5MB | Yes | No (single-node) | ✅ Great for 1-50 boxes on one broker |
| **EMQX** | ~120MB | Yes | Yes | Overkill for now |
| **HiveMQ CE** | ~70MB | Yes | No | Middle ground, but Mosquitto is simpler |

### Verdict
**Strong contender.** MQTT is the right protocol for edge → mothership telemetry + commands. Mosquitto is the simplest broker.

---

## Option C: NATS + JetStream (The modern choice)

### How it works
- Mothership runs a NATS server with JetStream (persistent event store)
- Boxes publish events as NATS subjects: `famcloud.box.health`, `famcloud.box.traces`, `famcloud.box.backup`
- Mothership subscribes and persists to JetStream
- NATS Core for real-time (sub-millisecond), JetStream for durable/persistent
- NATS has built-in MQTT adapter for IoT devices that only speak MQTT

### Pros
- **10-100x faster than MQTT.** 4-12M msgs/sec vs MQTT's ~100K. Overkill for us, but means it never bottlenecks.
- **JetStream = persistent event log.** All events durable across restarts. Built-in replay (re-process past events).
- **Service mesh + pub/sub in one.** NATS does both fire-and-forget AND durable events.
- **KV store built in.** NATS JetStream KV — perfect for per-box config/state.
- **Object store built in.** Trace bundles, backup snapshots, model binaries — NATS ObjectStore (like mini-S3).
- **Single binary.** `nats-server` is a single Go binary, ~50MB memory, zero dependencies.
- **Multi-tenant.** Accounts/streams per box or per customer.

### Cons
- Less "IoT standard" than MQTT (though NATS has an MQTT adapter).
- Younger ecosystem. MQTT has 20+ years. NATS is ~10 years old.
- Still a new service on mothership (but single binary, very simple).

### Verdict
**Best option if we want to be right long-term.** NATS gives us protocol + persistence + KV + object store in one tool. One binary on the mothership.

---

## Option D: Tailscale + gRPC (What we already have, extended)

### How it works
- Boxes are already on Tailscale (for SSH and fleet access)
- Mothership calls each box via gRPC over the Tailscale IP
- `POST` traces, `GET` health, `POST` config updates

### Pros
- **Already have Tailscale.** No new network dependency.
- Tailscale = secure mesh by default. Zero config, zero open ports.
- gRPC = typed contracts, auto-generated clients.

### Cons
- **Polling-based.** Mothership has to initiate every interaction. No box → mothership push without the box also running a gRPC client.
- No offline queue. If mothership is down when a box tries to push, event is lost.
- No event model. No publish/subscribe. No replay.
- gRPC on a Tailscale IP works but isn't designed for this pattern.

### Verdict
**Good for admin SSH and health checks.** Not good as the primary data plane.

---

## My Recommendation: Hybrid Architecture

### Layer 1: NATS + JetStream on Mothership (Event Backbone)

NATS JetStream server running on the mothership Mac mini. Each box connects via NATS client (Python SDK, single dependency).

**What flows over NATS:**
| Subject | Direction | Content | Persistence |
|---------|-----------|---------|-------------|
| `famcloud.<id>.health` | box → mothership | Heartbeat, CPU/RAM/disk metrics | 7-day retention |
| `famcloud.<id>.traces` | box → mothership | Anonymized trace bundles (JSONL) | Permanent |
| `famcloud.<id>.backup.done` | box → mothership | SQLite backup confirmation | 30-day retention |
| `famcloud.<id>.command` | mothership → box | "Update model to v3.2", "Run export" | At-least-once delivery |
| `famcloud.<id>.config` | mothership → box | Config diff push | KV store |
| `famcloud.<id>.alert` | box → mothership | "Gateway crashed 3x", "Disk 90%" | 30-day retention |

### Layer 2: Tailscale (Existing, for Admin)
Keep Tailscale for SSH access, ad-hoc debugging, model binary transfers (large files go over SCP/Tailscale, not NATS).

### Layer 3: SQLite (Local, on Each Box)
Each box already has SQLite WAL mode. This is the local data store. NATS events flow *from* SQLite changes and *into* SQLite on config updates.

### Why not just MQTT?
MQTT handles messaging well, but we also need:
- **Durable event replay** (JetStream) — if mothership goes down, events are safe and replayable
- **Key-Value config store** (JetStream KV) — per-box config without a separate K8s/Redis
- **Object store** — trace bundles, backup snapshots without setting up S3/MinIO
- **Service mesh** — future need for mothership → real-time box commands

NATS does all four. MQTT does one.

### Why not Kafka?
Kafka is overkill. JVM. 500MB+ memory. We need sub-50MB. NATS is a single 50MB binary.

---

## Per-Box Architecture (What Runs on Each FamCloud Rig)

```
┌────────────────────────────────────────────┐
│              FamCloud Box                  │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │       OpenClaw Gateway               │ │  ← Existing, handles all channels
│  │       (Node.js)                      │ │
│  └──────────┬───────────────┬───────────┘ │
│             │               │              │
│  ┌──────────▼────┐  ┌──────▼───────────┐ │
│  │   SQLite WAL  │  │  NATS Client     │ │  ← New: publishes to mothership
│  │   (entities,  │  │  (nats-py)       │ │
│  │    memory)    │  │                  │ │
│  └──────────┬────┘  └────────┬─────────┘ │
│             │                │            │
│  ┌──────────▼────────────────▼─────────┐ │
│  │       Ollama / vLLM                 │ │  ← Local model inference
│  │       (Qwen 7B distilled)          │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌──────────────────────────────────────┐ │
│  │       Trace Collector                │ │  ← Existing, exports JSONL
│  │       → POST to NATS subject         │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │       Health Monitor                 │ │  ← Every 5 min: publishes health
│  │       → POST to NATS subject         │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
                    │
              Tailscale
                    ▼
┌────────────────────────────────────────────┐
│              Mothership                    │
│                                            │
│  ┌──────────────────┐  ┌────────────────┐ │
│  │  NATS Server     │  │  SQLite/PG     │ │
│  │  + JetStream     │◄─┤  (fleet DB)    │ │
│  │  (50MB binary)   │  │                │ │
│  └────────┬─────────┘  └───────┬────────┘ │
│           │                    │           │
│  ┌────────▼─────────┐  ┌──────▼─────────┐ │
│  │  Distillation    │  │  Health        │ │
│  │  Pipeline        │  │  Dashboard     │ │
│  │  (export → grade │  │  + Alerts      │ │
│  │   → upload HF)   │  │                │ │
│  └──────────────────┘  └────────────────┘ │
│                                            │
│  ┌──────────────────┐                      │
│  │  OTA Model Push  │  ← via Tailscale SCP │
│  │  (new weights)   │  (large files)       │
│  └──────────────────┘                      │
└────────────────────────────────────────────┘
```

---

## The Simplest Thing That Could Work (Phase 1)

If NATS is too much for now, here's the **minimal** architecture:

1. **Tailscale** (already have) — fleet networking, SSH
2. **SQLite on each box** (already have) — canonical data store
3. **Scheduled cron export** (already have) — traces → JSONL → POST to mothership API
4. **Add: a lightweight mothership API** — FastAPI server on mothership that accepts:
   - `POST /traces` — trace bundle ingestion
   - `POST /health` — box heartbeat with metrics
   - `GET /config/<box_id>` — box fetches its config
   - `POST /alert` — box reports issues
5. **Add: per-box cron** — heartbeat every 5 min, trace export weekly, config fetch on startup

This is basically what we have now, just formalized with a real API on the mothership. No NATS, no MQTT, no new services. Just a FastAPI server and cron jobs that POST to it.

---

## Decision: What to Build When

| Phase | Protocol | Why | When |
|-------|----------|-----|------|
| **Now** | HTTPS POST + cron | We already have this. Just formalize the mothership API. | Today |
| **At 20 boxes** | Add NATS + JetStream | Need event durability, offline queue, real-time commands. | When fleet grows |
| **At 100+ boxes** | Add MQTT adapter | If we need to support non-OpenClaw devices or IoT peripherals. | If the product diverges |

---

## Summary

**Don't over-engineer yet.** The pattern everyone recommends (NATS, MQTT, Kafka) is right for scale. But at 0 customers, the best architecture is the one that works.

My honest take: build the mothership FastAPI API + keep cron-based sync for now. When you have 10-20 boxes and the cron jobs become painful, drop in NATS JetStream. It's a single binary addition, zero downtime migration (NATS has a MQTT adapter so existing boxes can keep using MQTT patterns via NATS).

The thing that matters right now is **getting the first rig working**, not picking the perfect protocol. Charles, you know this. Let me know what you think.

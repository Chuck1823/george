# OpenClaw Capability Map

## Table of Contents

1. [Core Architecture](#core-architecture)
2. [Available Channels](#available-channels)
3. [Agent Tools & Capabilities](#agent-tools--capabilities)
4. [Skill System](#skill-system)
5. [Scheduling & Automation](#scheduling--automation)
6. [Memory System](#memory-system)
7. [Configuration System](#configuration-system)
8. [Multi-Agent & Sub-Agent Capabilities](#multi-agent--sub-agent-capabilities)
9. [Data Flow & Traces](#data-flow--traces)
10. [Production-Ready vs In-Development](#production-ready-vs-in-development)

---

## Core Architecture

### Gateway

The **Gateway** is the central daemon that owns everything: messaging surfaces, agent runs, scheduling, and state. It exposes:

- **WebSocket API** on port 18789 (default) — typed JSON protocol for all interactions
- **HTTP server** for canvas (`/__openclaw__/canvas/`) and A2UI (`/__openclaw__/a2ui/`)
- **Health/Status RPC** via the WS API

Key properties:
- One Gateway per host
- Maintains provider connections
- Validates inbound frames against JSON Schema
- Emits events: `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`
- Process supervision via launchd/systemd
- Protocol uses TypeBox schemas with generated JSON Schema and Swift models

### Agent Runtime

OpenClaw has a built-in embedded agent runtime (`openclaw`) and supports plugin runtimes:

| Runtime | Description |
|---------|-------------|
| `openclaw` | Built-in embedded runtime — owns the full model loop, tool execution, compaction |
| `codex` | OpenAI Codex app-server runtime (subscription-backed ChatGPT/Codex) |
| `claude-cli` | Claude CLI backend |
| `copilot` | GitHub Copilot CLI (opt-in external plugin) |
| `acp` | External harnesses via ACP/acpx (Claude Code, Gemini CLI, etc.) |

Runtime selection order: model-scoped policy → provider-scoped policy → plugin claims in `auto` mode → fallback to `openclaw`.

The agent loop:
1. Gateway receives `agent` RPC → validates params, resolves session
2. `runEmbeddedAgent` → serializes runs via per-session + global queues
3. Resolves model + auth profile, builds session, loads skills
4. Subscribes to runtime events, streams assistant/tool deltas
5. Enforces timeout, handles compaction, retries
6. Emits lifecycle events (`start`, `end`, `error`)

### Session Management

Conversations are organized into **sessions** with deterministic routing:

| Source | Behavior |
|--------|----------|
| Direct messages | Shared session by default (configurable) |
| Group chats | Isolated per group |
| Rooms/channels | Isolated per room |
| Cron jobs | Fresh session per run |

**Session lifecycle:**
- **Daily reset** at 4:00 AM local time (configurable)
- **Idle reset** after configurable inactivity
- **Manual reset** via `/new` or `/reset`

**Storage:**
- Store: `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Transcripts: `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`

**Compaction:** Auto-compaction when context limits are approached. Summarizes older turns, saves summary to transcript, keeps recent messages. Memory flush before compaction to preserve important context.

**Queue modes:** `steer` (default, injects into active run), `followup`, `collect` (coalesce), `interrupt` (abort current run).

### Workspace

Each agent's working directory contains:
- `AGENTS.md` — operating instructions
- `SOUL.md` — persona and tone
- `USER.md` — who the user is
- `TOOLS.md` — local tool conventions
- `HEARTBEAT.md` — heartbeat checklist
- `MEMORY.md` — curated long-term memory
- `memory/YYYY-MM-DD.md` — daily notes
- `skills/` — workspace-specific skills
- `canvas/` — Canvas UI files

### Heartbeat

Periodic main-session agent turns (default 30min) that surface anything needing attention:
- Can target last contact, specific channel, or none (internal only)
- `HEARTBEAT_OK` response suppresses delivery
- Supports `tasks:` blocks for interval-based checks
- Active hours, isolated sessions, and light context for cost control

---

## Available Channels

| Channel | Account Support | Auth Method | Notes |
|---------|----------------|-------------|-------|
| **WhatsApp** | Multiple accounts (Baileys) | QR pairing | Primary use case |
| **Telegram** | Multiple bots | Bot token | BotFather setup |
| **Discord** | Multiple bots | Bot token | Message Content Intent required |
| **Slack** | Multiple workspaces | Bot token | |
| **Signal** | Multiple accounts | signal-cli | |
| **iMessage** | Direct | Messages.app or BlueBubbles | macOS only |
| **SMS** | Yes | Various providers | |
| **Matrix** | Yes | MXID/password | Migration support |
| **IRC** | Yes | IRC connection | |
| **Google Chat** | Yes | OAuth | |
| **MS Teams** | Yes | OAuth | |
| **Mattermost** | Yes | Token | |
| **Nextcloud Talk** | Yes | | |
| **Discord** | Yes | | |
| **Line** | Yes | | |
| **WeChat** | Yes | | |
| **Nostr** | Yes | | |
| **Twitch** | Yes | | |
| **Zalo** | Yes | | |
| **Feishu** | Yes | | |
| **QQ Bot** | Yes | | |
| **Yuanbao** | Yes | | |
| **Synology Chat** | Yes | | |
| **Tlon** | Yes | | |
| **WebChat** | Built-in | Gateway auth | Static web UI |

**Channel features:**
- Multi-account per channel with `accountId` routing
- Broadcast groups
- DM isolation modes (`main`, `per-peer`, `per-channel-peer`, `per-account-channel-peer`)
- Channel docking (move session between channels)
- Presence tracking
- Typing indicators
- Streaming (partial or block mode)

---

## Agent Tools & Capabilities

### Core Tools

| Tool | Capability |
|------|-----------|
| `exec` | Shell command execution with approval gates |
| `read` | File reading with offset/limit |
| `write` | File creation/overwrite |
| `edit` | Precise text replacement |
| `apply_patch` | Multi-file patch application |

### Web Tools

| Tool | Capability |
|------|-----------|
| `web_search` | Web search (Brave, Perplexity, Exa, Tavily, DuckDuckGo, SearXNG) |
| `web_fetch` | Fetch URL and extract readable markdown |

### Session Management Tools

| Tool | Capability |
|------|-----------|
| `session_status` | Get current session info |
| `sessions_list` | List all sessions |
| `sessions_history` | Get bounded, sanitized session history |
| `sessions_send` | Send messages to other sessions |
| `sessions_spawn` | Spawn subagent runs |

### Scheduling Tools

| Tool | Capability |
|------|-----------|
| `cron` | Create/manage cron jobs from chat |

### Memory Tools

| Tool | Capability |
|------|-----------|
| `memory_search` | Semantic search of memory (hybrid vector + keyword) |
| `memory_get` | Read specific memory file/line range |

### Skills

| Tool | Capability |
|------|-----------|
| `skill_workshop` | Create/update/inspect/apply skill proposals |

### Media Generation

| Tool | Capability |
|------|-----------|
| `image_generate` | Image generation (multiple providers) |
| `video_generate` | Video generation |
| `music_generate` | Music/audio generation |
| `tts` | Text-to-speech |

### Specialized Tools

| Tool | Capability |
|------|-----------|
| `goal` | Goal creation/management |
| `browser` | Browser control/automation |
| `canvas` | Canvas presentation |
| `nodes` | Node device commands |
| `thinking` | Extended reasoning/thinking |
| `llm_task` | LLM task delegation |
| `pdf` | PDF processing |

---

## Skill System

### How It Works

Skills are markdown files (`SKILL.md`) that provide specialized instructions for specific tasks. The agent system:

1. Loads skills from multiple sources with precedence:
   - Workspace skills (highest)
   - Project agent skills
   - Personal agent skills
   - Managed skills
   - Bundled skills (lowest)

2. Skills declare `<available_skills>` with name, description, location, and version hash
3. Agent reads a skill's `SKILL.md` when task matches its description
4. If skill version changed from previous turn, re-read before using
5. Can include support files (scripts, templates, examples)

### Skill Workshop

Reusable procedure capture system:
- `create` — new skill proposal
- `update` — existing approved skill
- `revise` — pending proposal
- `list` / `inspect` — discovery
- `apply` / `reject` / `quarantine` — lifecycle

Proposals are stored as `PROPOSAL.md` with optional support files.

### ClawHub

Plugin/skill marketplace:
- Search for skills
- Install, verify, update, publish
- Sync skills across installations

---

## Scheduling & Automation

### Cron System

Built-in Gateway scheduler with SQLite persistence:

**Schedule types:**
- `at` — one-shot timestamp
- `every` — fixed interval
- `cron` — 5/6-field cron expression with timezone

**Execution styles:**
- Main session — cron-owned run lane, optionally wakes heartbeat
- Isolated — fresh session per run
- Current session — bound at creation time
- Custom session — persistent named session

**Delivery modes:**
- `announce` — deliver to chat channel
- `webhook` — POST to URL
- `none` — no delivery

**Features:**
- Command payloads (deterministic scripts)
- Model/thinking/model override
- Per-job fallback chains
- Retry with exponential backoff
- Run history in SQLite
- Gmail PubSub integration

### Heartbeat

Periodic checks (see Core Architecture section)

### Webhooks

HTTP endpoints for external triggers:
- `/hooks/wake` — enqueue system event
- `/hooks/agent` — run isolated agent turn
- `/hooks/<name>` — custom mapped hooks

### TaskFlow

Multi-step detached task coordination:
- Owner context, state, waits, child tasks
- Durable job tracking

### Standing Orders

Persistent instructions in workspace files

---

## Memory System

### File-Based Memory

Three tiers:

1. **`MEMORY.md`** — Long-term curated facts, preferences, decisions
2. **`memory/YYYY-MM-DD.md`** — Daily working notes
3. **`DREAMS.md`** — Dream diary (optional consolidation)

### Memory Backends

| Backend | Description |
|---------|-------------|
| **SQLite (default)** | Built-in, hybrid search, no extra deps |
| **QMD** | Local-first sidecar, reranking, query expansion |
| **Honcho** | AI-native cross-session memory |
| **LanceDB** | OpenAI-compatible embeddings |

### Memory Features

- Semantic search (vector + keyword hybrid)
- Embedding providers (OpenAI, Gemini, Voyage, Mistral, Ollama, Bedrock)
- Memory flush before compaction
- Dreaming (background consolidation, opt-in)
- Grounded backfill from historical notes
- Memory Wiki plugin (provenance-rich knowledge vault)
- Inferred commitments (short-lived follow-ups)

---

## Configuration System

### Config File

`~/.openclaw/openclaw.json` (JSON5) — primary configuration

**Key sections:**
- `agents.defaults.*` — global agent settings
- `agents.list[]` — per-agent overrides
- `channels.<name>.*` — channel configuration
- `bindings[]` — message routing rules
- `tools.*` — tool policies
- `cron.*` — scheduler settings
- `memory.*` — memory backend config
- `hooks.*` — webhook hooks

### Auth Profiles

Per-agent auth profiles at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`:
- OAuth profiles (for subscription services)
- API key profiles
- Per-provider model auth

### Agent Configuration

Each agent has:
- Workspace directory
- State directory (`agentDir`)
- Model selection + fallback chains
- Sandbox settings
- Tool allow/deny lists
- Heartbeat config
- Skill allowlists

### Multi-Agent Setup

- Isolated agents with separate workspaces, state, sessions
- Bindings for deterministic routing (peer → parentPeer → guildId → teamId → accountId → default)
- Per-agent sandbox and tool restrictions
- Cross-agent QMD memory search

---

## Multi-Agent & Sub-Agent Capabilities

### Multi-Agent

Run multiple isolated agents in one Gateway:
- Each agent: workspace, auth, sessions, personality
- Channel account routing (different phone numbers, bots)
- Per-peer routing within same channel
- Cross-agent communication (disabled by default, explicit allowlist)

### Sub-Agents

Background agent runs:
- Spawned via `sessions_spawn`
- Detached execution with task tracking
- Separate lanes (`subagent`, `nested`, `cron-nested`)
- Auto-announce results back to parent
- Depth-limited spawning

### Queue Lanes

- `main` — inbound + main heartbeats (default concurrency: 4)
- `subagent` — subagent runs (default concurrency: 8)
- `cron` — scheduled jobs
- `cron-nested` — isolated agent-turn execution
- `nested` — shared nested flows
- Per-session lanes guarantee one run at a time

---

## Data Flow & Traces

### Message Flow

1. **Inbound** → Channel → Gateway WS → Queue → Agent run
2. **Agent** → Prompt assembly → Model inference → Tool execution → Reply
3. **Outbound** → Channel delivery → User receives

### Session State

- Transcript: JSONL with session header
- Store: `sessions.json` with lifecycle timestamps
- Per-session write lock for consistency

### Heartbeat/Task State

- `memory/heartbeat-state.json` — check tracking
- Session state for heartbeat task timestamps
- Dream state in `.dreams/` directory

### Cron State

- SQLite store for jobs and run history
- Background task records for executions

### Observability

- OpenTelemetry support
- Prometheus metrics
- Structured logging
- Diagnostic state for session lifecycle

### Tracing

- Lifecycle events emitted on WS streams
- Tool start/update/end events
- Assistant streaming deltas
- Compaction events
- System events

---

## Production-Ready vs In-Development

### Production-Ready

| Feature | Status |
|---------|--------|
| Gateway daemon | ✅ Mature, battle-tested |
| WhatsApp/Telegram/Discord/Slack | ✅ Full support |
| WebSocket protocol | ✅ Stable with schema validation |
| Session management | ✅ Daily reset, idle, manual |
| Multi-agent routing | ✅ Bindings, isolation |
| Agent runtime (embedded) | ✅ Core loop, tools, compaction |
| Memory (SQLite backend) | ✅ Working, configurable |
| Cron scheduler | ✅ SQLite-backed, retries |
| Heartbeat | ✅ Configurable cadence/targets |
| Exec tool | ✅ Approval gates, sandboxing |
| Web search/fetch | ✅ Multiple providers |
| Skills system | ✅ SKILL.md, workshop |
| Compaction | ✅ Auto + manual |
| Queue modes | ✅ steer/followup/collect/interrupt |
| Canvas | ✅ HTML presentation |
| Config system | ✅ JSON5, multi-agent |
| Sandbox support | ✅ Docker-based |
| Plugin hooks | ✅ Lifecycle interception |
| OpenTelemetry | ✅ Tracing support |
| Prometheus metrics | ✅ Monitoring |
| Sub-agents | ✅ Detached runs |
| Background tasks | ✅ TaskFlow, task records |
| Webhooks | ✅ HTTP endpoints |
| Gmail PubSub | ✅ Integration |
| Memory Wiki | ✅ Plugin vault |
| Dreaming | ✅ Opt-in consolidation |
| Commitments | ✅ Inferred follow-ups |
| Codex harness | ✅ Native app-server |
| ACP/acpx | ✅ External harnesses |
| Model fallback | ✅ Configurable chains |
| DM isolation | ✅ Per-channel-peer |
| Channel docking | ✅ Session migration |

### Stable but Evolving

| Feature | Status | Notes |
|---------|--------|-------|
| Honcho memory | ✅ Plugin | AI-native memory integration |
| QMD memory | ✅ Plugin | Advanced search with reranking |
| LanceDB memory | ✅ Plugin | OpenAI-compatible embeddings |
| Copilot runtime | ✅ Plugin | GitHub Copilot CLI |
| Copilot harness | ⚠️ | Separate opt-in plugin |
| Memory Wiki | ✅ Plugin | Provenance-rich knowledge |
| Dreaming | ✅ Opt-in | Background consolidation |
| Broadcast groups | ✅ | Multi-channel broadcast |

### In Development / Experimental

| Feature | Status | Notes |
|---------|--------|-------|
| Parallel specialist lanes | 🔄 | Multiple concurrent specialist agents |
| Queue steering refinements | 🔄 | Codex-specific timing |
| Session maintenance improvements | 🔄 | High-water buffer cleanup |
| Gateway security hardening | 🔄 | Ongoing improvements |
| Plugin ecosystem | 🔄 | Growing catalog |

---

## Key Paths Summary

```
~/.openclaw/
├── openclaw.json                 # Main config (JSON5)
├── agents/
│   └── <agentId>/
│       ├── agent/
│       │   └── auth-profiles.json  # Model auth (OAuth + API keys)
│       └── sessions/
│           ├── sessions.json       # Session store
│           └── <sessionId>.jsonl   # Session transcript
├── workspace/                    # Agent workspace
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── USER.md
│   ├── IDENTITY.md
│   ├── TOOLS.md
│   ├── HEARTBEAT.md
│   ├── MEMORY.md
│   └── memory/
│       └── YYYY-MM-DD.md
├── credentials/                  # Channel/provider state
├── cron/                         # (legacy, migrated to SQLite)
└── skills/                       # Managed skills
```

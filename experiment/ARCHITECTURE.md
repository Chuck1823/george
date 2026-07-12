# FamCloud Architecture & Operations

## System Architecture

### On-Device Stack (per household GPU rig)
```
┌─────────────────────────────────────────┐
│              FamCloud Rig               │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │        OpenClaw Gateway           │  │  ← Main conversation router
│  │     (message handling, memory)    │  │
│  └──────────────┬────────────────────┘  │
│                 │                       │
│  ┌──────────────▼────────────────────┐  │
│  │       Model Router Layer          │  │  ← Decides which model to call
│  │  (intent → synthesizer/memory/    │  │
│  │   entity extractor/text classify) │  │
│  └──────────────┬────────────────────┘  │
│                 │                       │
│  ┌──────────────▼────────────────────┐  │
│  │          Ollama / vLLM            │  │  ← Model runtime
│  │  (Qwen2.5-7B, distilled weights)  │  │
│  └──────────────┬────────────────────┘  │
│                 │                       │
│  ┌──────────────▼────────────────────┐  │
│  │       Local Vector Store          │  │  ← Embeddings for memory/search
│  │       (SQLite + ChromaDB)         │  │
│  └──────────────┬────────────────────┘  │
│                 │                       │
│  ┌──────────────▼────────────────────┐  │
│  │         Persistent Store          │  │  ← Conversations, files, keys
│  │         (SQLite + local files)    │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │       Channel Adapters            │  │
│  │   (WhatsApp, iMessage, Telegram,  │  │
│  │    SMS, Slack, Discord, Email)    │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
     WhatsApp    iMessage    Telegram ...
```

### Channel Connectivity
Users tell FamCloud which channels to connect via:
1. **Onboarding flow** (web portal on local rig → `famcloud.local:18789/setup`)
2. **Scan QR code** for WhatsApp/Telegram (standard OAuth)
3. **Enter credentials** for email, iMessage (via Mac mini pairing)
4. **Invite link** for Slack/Discord

Each channel is a plugin with its own auth flow and message adapter.

## Model Updates

### Phase 1: Manual Updates (Founder-Driven)
- You run the distillation loop on your own hardware
- When a better model is ready, you publish weights to HuggingFace
- Customer rigs run a nightly cron that checks for new versions:
  ```bash
  # Nightly check (if new version)
  0 3 * * * /opt/famcloud/update-models.sh
  ```
- Update script:
  1. Check HuggingFace for new weight hash
  2. Download new GGUF files in background
  3. Test new model against current (benchmark on 20 saved queries)
  4. If quality improved → swap in, restart Ollama
  5. If worse → rollback, log alert to support
- Zero downtime: the old model stays active until the new one passes tests

### Phase 2: Self-Improving (Per-Rig)
- Each rig learns its household's patterns locally
- No data leaves the house
- Self-grading via reflection on high-signal traces
- LoRA adapters trained during off-hours
- Published model updates still come from you (quality bar)

## Guardrails & Parental Controls

### Per-Person Profiles
Each household member gets their own profile with:
- Name, relationship, age
- Memory isolation (what they can see about others)
- Privacy boundaries (what the AI can/can't share between members)

### Parental Controls
- **Age-based filtering**: Content filtered by age group
- **Approval workflows**: Kids under 13 → certain actions require parent approval
- **View logs**: Parents can view what their kids asked/received
- **Time windows**: Can set when FamCloud is active (e.g., no late-night messages)
- **Spending locks**: Kids can't make purchases without approval
- **Content categories filterable**: violence, explicit, political, etc.

### Privacy Across Individuals
- **Shared memory**: Things the whole household should know (WiFi password, family schedule, pet's name)
- **Private memory**: Individual conversations that stay with that person
- **Family rules**: "Don't share Sarah's messages with Dad" type controls
- The rig is the boundary — all data stays on it, but within the rig, isolation profiles control access

## Self-Healing System

### What Can Break & Auto-Fix:
| Problem | Detection | Auto-Recovery |
|---------|-----------|---------------|
| Gateway crash | Process monitor | Auto-restart in 30s |
| Ollama crash | Health check endpoint | Auto-restart, fall back to cached responses |
| Channel auth expired | Failed message send | Alert user to re-auth, fallback to web portal |
| Model corrupt | Inference errors | Rollback to previous model version |
| Disk full | Cron check | Compress old conversations, alert user |
| Network down | Ping test | Switch to local-only mode, queue outbound |
| GPU driver gone | nvidia-smi fails | Alert support, fall back to CPU inference |

### Health Monitor Daemon
Runs on the rig:
```python
# Every 5 minutes:
- Check gateway health (HTTP 200)
- Check model inference (simple test query)
- Check disk usage
- Check memory usage
- Check GPU status
- Check network connectivity
# If anything fails:
- Try auto-recovery (restart, rollback, cleanup)
- If recovery fails → create support ticket
```

## Support System

### Tiers:
**Free (self-serve):**
- Community documentation
- Auto-healing (as above)
- Model updates delivered automatically

**$100/month (standard):**
- Everything above
- Weekly automated health checks reported to the user
- Remote support access (you SSH in when needed)
- 24h response SLA for reported issues
- Model updates from your distillation pipeline

**$250/month (premium):**
- Everything above
- 4h response SLA
- Priority support queue
- Custom model fine-tuning for the household (personalized weights)
- Dedicated support contact (you or a hired person)

### Support Agent Flow
When a user reports an issue:
1. **FamCloud Support Agent** (running on your server) receives the message
2. **Auto-diagnosis**: Agent checks the rig's health (SSH, health endpoint)
3. **Categorization**: Hardware? Software? Model? Channel?
4. **Ticket creation**: Auto-creates ticket with diagnostics attached
5. **Routing**:
   - Tier 1: Auto-fixable → agent applies fix, notifies user
   - Tier 2: Needs human → creates ticket, assigns to you
   - Tier 3: Hardware failure → RMA process, ship replacement part

## Onboarding Flow

1. **Unbox the rig** — it comes with Ubuntu + FamCloud pre-installed
2. **Plug in ethernet** — rig boots, starts gateway
3. **Go to famcloud.local** — browser auto-discovers on local network
4. **Create household account** — name, email, phone
5. **Set up profiles** — add family members, set ages, relationships
6. **Connect channels** — scan QR codes, enter credentials
7. **Set preferences** — parental controls, privacy settings, notification rules
8. **First conversation** — FamCloud says hi, learns about the household

## Key Design Principles

1. **Nothing leaves the house** — all data, all inference, all memory. Period.
2. **The rig is the boundary** — inside = personal, outside = nothing
3. **Self-healing first** — most problems fix themselves without user or support involvement
4. **Progressive disclosure** — starts simple, advanced options for power users
5. **You remain the teacher** — model quality comes from your distillation pipeline, not from customer data

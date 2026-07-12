# FamCloud Agent-Native Tool Stack (Final)

## Philosophy: Agent-owned, local-first where possible

The agent is its own entity. It has its own phone number, email, WhatsApp, etc.
We own the stack where we can (local GPU inference, local voice via Pipecat).
External APIs only for what we can't self-host (phone numbers, iMessage relay, WhatsApp relay).

---

## Unified Phone + iMessage + SMS: AgentPhone (agentphone.ai)

**What it gives us:**
- Agent-owned phone numbers (API-provisioned)
- iMessage-enabled numbers (no customer Mac needed!)
- SMS send/receive
- Voice calls with real-time transcript webhook
- Webhook-based: inbound messages sent to our rig
- Pay-as-you-go pricing

**Why not Telnyx:**
Telnyx is fine but AgentPhone is built specifically for AI agents. One API gives us phone numbers + iMessage + SMS + voice with transcripts. Telnyx gives us phone numbers and telecom plumbing but we'd still need a separate iMessage relay solution.

**Pricing:** Pay-as-you-go, TBD exact rates (typically $1-5/mo per number + usage)

---

## WhatsApp: Self-hosted Baileys OR WASSender OR AgentPhone (coming)

**Option A: OpenClaw @openclaw/whatsapp plugin (Baileys)** — FREE, self-hosted, QR pair
**Option B: WASSender** — managed API, dedicated agent-owned number
**Option C: AgentPhone WhatsApp** — they're adding this soon (per their roadmap)

**Recommendation:** Phase 1 = Baileys (QR pair). When AgentPhone launches WhatsApp → migrate.

---

## Voice Calls: Pipecat (self-hosted, owns the stack)

**Pipecat.ai** — open-source Python framework for voice agents. MIT license.

**Stack on our rig:**
- STT: Whisper Large-v3 (local, GPU-accelerated)
- LLM: Our distilled Qwen2.5-7B (local, GPU)
- TTS: Kokoro TTS (local, CPU) or open TTS model
- Pipeline: Pipecat orchestrates STT → LLM → TTS
- Telephony: AgentPhone handles inbound call → streams audio to Pipecat → Pipecat returns TTS audio → AgentPhone sends to caller

**Cost: $0/month** — everything local on the rig. No per-minute fees.

**Why not Vapi/Bland/Retell:**
- Vapi: $0.05/min orchestration + components stack to $0.23-0.33/min
- Bland: $0.12-0.14/min minimum
- Retell: $0.07-0.31/min component-billed
- Pipecat: FREE (self-hosted on our GPU)

Pipecat gives us full control, no vendor lock-in, and costs nothing since the rig already has the GPU.

---

## iMessage: AgentPhone (agent-owned number, blue bubbles)

**Key insight:** AgentPhone provides iMessage-enabled phone numbers. The agent's messages show as blue bubbles in recipients' iPhones. No customer Mac needed.

**How it works:**
1. Bootstrap script provisions agent phone number via AgentPhone API
2. Number is iMessage-enabled (managed relay handles the Apple hardware)
3. Family members who have iPhones see blue bubbles when they text the agent
4. Agent responds via iMessage (via AgentPhone relay)
5. All through one API — same number handles SMS + iMessage + voice

**This eliminates:**
- Customer needing a Mac running 24/7
- BlueBubbles/imsg CLI complexity
- Risk of Apple banning customer's personal Apple ID

---

## Email: famcloud.ai aliases via Cloudflare Email Routing

- We own famcloud.ai domain ($15/year)
- Cloudflare Email Routing (FREE) forwards to customer's real inbox
- Agent can send from alias via our SMTP or customer's OAuth Gmail
- Per-household alias: {family}@famcloud.ai

---

## Remaining Channels (all FREE, OpenClaw native)

| Channel | Setup | Monthly Cost |
|---------|-------|-------------|
| Telegram bot | @BotFather → paste token | FREE |
| Discord bot | Developer Portal → create bot | FREE |
| Slack bot | Slack API → create app | FREE |
| Signal | signal-cli register | FREE |

---

## Final Agent Identity (Per Household)

| Identity | Provider | Monthly Cost |
|----------|---------|-------------|
| Phone number (SMS + iMessage + voice) | AgentPhone | $1-5/mo |
| WhatsApp | Baileys (self-hosted on rig) | FREE |
| Telegram bot | @BotFather | FREE |
| Discord bot | Discord Dev Portal | FREE |
| Slack bot | Slack API | FREE |
| Signal | signal-cli | FREE |
| Email | famcloud.ai + Cloudflare | $0 |
| **Total** | | **$1-5/month** |

Plus famcloud.ai domain amortized: $1.25/mo

**Grand total per household: $2-6/month**

---

## Agent Access to Customer's Accounts (Context)

- **Google OAuth:** Gmail (read), Calendar (read/write), Drive, Contacts
- **Apple Calendar:** customer shares calendar URL with agent
- **Future:** Photos, Smart home, Health

Agent uses customer's accounts for context and actions but communicates through its own identity.

---

## Self-Serve Onboarding (Updated)

```
1. Plug in ethernet + power → rig boots → bootstrap runs
2. Open famcloud.local:18789/setup in browser
3. Create household account
4. We auto-provision (one click):
   - AgentPhone number (SMS + iMessage + voice enabled)
   - famcloud.ai email alias
5. Customer connects (click to authorize):
   - WhatsApp → QR code → scan with phone
   - Telegram → opens @BotFather → paste token
   - Discord → opens Dev Portal → create bot → paste token
   - Slack → opens Slack API → create app → install
   - Google → OAuth popup → grant access
6. Add family members, set parental controls
7. Agent live on all channels
```

**The bootstrap script handles:**
- OS + NVIDIA drivers + Docker
- OpenClaw + all plugins
- Model weights download
- Pipecat install + configuration
- AgentPhone number provisioning (via our master API key)
- Email alias creation (via Cloudflare API)
- Health monitor daemon
- Model update cron
- Web UI setup

**Customer only needs to:**
- Plug in the rig
- Open browser to famcloud.local
- Follow setup wizard (QR scan, token paste, OAuth)
- Done

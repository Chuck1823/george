# FamCloud Agent-Native Tool Stack (Updated)

## Philosophy: Local-first, Agent-owned, Self-Hosted Where Possible

The agent has its own identity and we own as much of the stack as possible. Local inference, local voice, local memory. External APIs only for channels we can't self-host (phone numbers, iMessage relay, WhatsApp relay).

---

## 1. Phone Numbers + iMessage + SMS + Voice: **AgentPhone**

**Why AgentPhone:**
- Agent-native by design — provision numbers, attach to agent personas
- iMessage-enabled numbers (no customer Mac needed!)
- SMS + voice calls through the same API
- Webhook-based: inbound calls/messages sent to FamCloud rig
- Open-source SDK + MCP server
- Pay-as-you-go pricing

**Pricing (pay-as-you-go):**
- Phone number provision (cost TBD — typical $1-5/month)
- Inbound SMS: ~$0.004/msg (similar to Telnyx)
- Voice calls: ~$0.02-0.05/min
- iMessage relay included with number

**Setup:**
1. Get API key from agentphone.ai
2. `curl POST /agents` → create agent persona
3. `curl POST /numbers` → provision number
4. `curl POST /agents/{id}/numbers` → attach number
5. Configure webhook → point to FamCloud rig's local URL
6. Agent receives messages and calls

**One API, everything:** phone numbers, SMS, iMessage, voice, transcripts. This replaces Telnyx + Twilio + separate iMessage relay provider.

**OpenClaw Integration:** AgentPhone doesn't have a native OpenClaw plugin yet, but we can write one. The webhook receives inbound messages → we route them to OpenClaw's message handler. Outbound messages → we call AgentPhone's API.

---

## 2. WhatsApp: **Self-hosted Baileys** or **AgentPhone (when available)**

### Option A: Self-hosted Baileys (OpenClaw plugin already exists)
- OpenClaw's `@openclaw/whatsapp` plugin uses Baileys
- QR code pair with customer's phone
- FREE, runs locally on the rig
- Against WhatsApp ToS (but widely used)

### Option B: WASSender (managed API)
- WhatsApp API provider
- Cost: TBD per number
- Legit route: uses WhatsApp Business API

### Option C: AgentPhone (when WhatsApp support launches)
- Coming soon according to docs
- Would unify with the rest of AgentPhone stack
- One API for phone, SMS, iMessage, voice, AND WhatsApp

**Recommendation for Phase 1:** Use OpenClaw's Baileys plugin (QR pair). When AgentPhone launches WhatsApp support, migrate to their API. For customers who want a dedicated number (not QR pair), use WASSender as interim.

---

## 3. Voice Calls: **Pipecat (self-hosted)**

**Why Pipecat over cloud platforms (Vapi, Bland, Retell):**
- Open-source (MIT license) — we own the stack
- Local inference → uses the rig's GPU for STT (Whisper) + LLM + TTS
- No per-minute fees — everything runs locally
- Modular: swap STT, LLM, TTS components as needed
- LocalAudioTransport for direct mic/speaker → perfect for rig

**Stack on the rig:**
- **STT:** Whisper Large-v3 (local, runs on GPU)
- **LLM:** Qwen2.5-7B or distilled model (local, runs on GPU)
- **TTS:** Kokoro TTS or OpenAI-compatible local TTS (runs on GPU)
- **Pipeline:** Pipecat orchestrates the full STT → LLM → TTS flow
- **Telephony:** AgentPhone handles inbound calls → streams audio to Pipecat → Pipecat processes → AgentPhone streams TTS output back

**Cost: $0/month** — everything runs on the GPU rig. No per-minute fees. No cloud LLM costs. No Twilio/Vapi/Retell fees.

**Setup:**
1. Install Pipecat framework on rig
2. Configure with local STT (Whisper) + local LLM (Ollama) + local TTS
3. AgentPhone webhook receives call → streams audio to Pipecat
4. Pipecat runs full pipeline → returns TTS audio → AgentPhone sends to caller

---

## 4. Email, SMS, Voice: **Pingram (coming)**

Pingram (formerly NotificationAPI):
- Email ✅ (live now)
- SMS ✅ (live now)
- WhatsApp 🔄 (coming soon)
- AI Voice 🔄 (coming soon)

**Pingram can replace separate email + SMS providers.** One API for everything.

**But AgentPhone already covers phone/SMS/voice/iMessage.** Pingram's email + SMS is redundant with AgentPhone's phone + messaging.

**Recommendation:** Use Pingram for email (the one thing AgentPhone doesn't cover). Use AgentPhone for phone/SMS/iMessage/voice. Skip redundant APIs.

---

## 5. Telegram, Discord, Slack, Signal: **Same as before**

These are all FREE and supported natively by OpenClaw:

| Channel | Provider | Cost | Notes |
|---------|---------|------|-------|
| Telegram | GrammY (built-in) | FREE | BotFather token |
| Discord | Discord API | FREE | Developer Portal |
| Slack | Slack API | FREE | Slack App |
| Signal | signal-cli | FREE | Phone registration |

---

## Updated Agent Identity Stack

### What the agent owns (per household):

| Identity | Provider | Monthly Cost | Notes |
|----------|---------|-------------|-------|
| **Phone number** (SMS/iMessage/voice calls) | AgentPhone | ~$1-5/mo | Includes iMessage relay |
| **WhatsApp** | Baileys (self-hosted) | FREE | QR pair, runs on rig |
| **Telegram bot** | @BotFather | FREE | Auto-created |
| **Discord bot** | Discord Developer Portal | FREE | One account |
| **Slack bot** | Slack API | FREE | One app |
| **Signal** | signal-cli | FREE | Same number as phone |
| **Email address** | famcloud.ai (Cloudflare) | $0 | name@famcloud.ai |

### What the agent accesses (customer's accounts):
- **Google** (OAuth): Gmail (read), Calendar, Drive, Contacts
- **Apple Calendar** (share URL): customer shares family calendar
- **iCloud Photos** (future): if customer grants access

---

## Cost Per Household (Final, Corrected)

| Item | Monthly Cost | Notes |
|------|-------------|-------|
| **AgentPhone number** (SMS/iMessage/voice) | $1-5/mo | Unified phone identity |
| **WhatsApp** | FREE | Self-hosted Baileys on rig |
| **All other channels** | FREE | Telegram, Discord, Slack, Signal, Email |
| **famcloud.ai domain** | $1.25/mo | $15/year amortized |
| **AI inference (local)** | $0 | Runs on GPU, no cloud costs |
| **Voice calls (local Pipecat)** | $0 | Local STT/LLM/TTS on GPU |
| **Model updates** | $0 | Your update server (shared) |
| **Total per household** | **$2-6/month** | |

**Margins:**
- $49/mo plan → $43-47/mo profit
- $99/mo plan → $93-97/mo profit
- $149/mo plan → $143-147/mo profit

---

## Bootstrap Script — Updated Provider List

```bash
#!/usr/bin/env bash
# FamCloud Bootstrap Script
# Runs once on first boot

# 1. OS + GPU
apt update && apt install -y nvidia-driver-560 docker.io docker-compose python3 python3-pip

# 2. Models
curl -L https://models.famcloud.ai/qwen2.5-7b-q4.gguf -o /models/qwen.gguf

# 3. OpenClaw
npm install -g openclaw

# 4. Channel plugins
openclaw plugins install @openclaw/whatsapp    # Baileys
openclaw plugins install @openclaw/signal      # signal-cli
# Telegram, Discord, Slack built-in

# 5. Pipecat (for voice)
pip install pipecat-ai whisper kokoro-tts

# 6. AgentPhone client (for phone numbers)
pip install agentphone  # or use REST API directly

# 7. Configure & start gateway
# (UI wizard handles channel setup)

# 8. Health monitor + model update cron
# (configured by bootstrap)

echo "✅ Open famcloud.local:18789 to set up your family's agent!"
```

---

## Self-Serve Onboarding — Updated Flow

1. **Plug in** → rig boots → bootstrap runs once
2. **Go to `famcloud.local:18789/setup`**
3. **Create household** → name, email, password
4. **Choose channels:**

   **What we auto-provision (via API):**
   - Phone number via AgentPhone (SMS + iMessage + voice) → we buy it, attach to household
   
   **What customer sets up (with guidance):**
   - WhatsApp → shows QR code → they scan with phone
   - Telegram → opens @BotFather → they paste token
   - Discord → opens Developer Portal → they create bot
   - Slack → opens Slack API → they create app
   - Google → OAuth popup → grant Gmail/Calendar/Drive access

5. **Family members** → add names, ages, relationships, parental controls
6. **Test conversation** → agent says hi on all channels
7. **Done** → agent runs 24/7

---

## No Mac Required

Key insight: **AgentPhone provides iMessage-enabled numbers** — no customer Mac needed. The agent has its own phone number that works for:
- SMS
- iMessage (blue bubbles!)
- Voice calls
- All through one API

This eliminates the need for customer's macOS device. Pipecat provides local voice processing. Everything runs on the rig.

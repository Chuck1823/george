# FamCloud Agent Provisioning Guide

## Core Concept: Who Owns What

Each FamCloud rig runs **one agent** for **one household**. The agent needs to connect to the channels that household chooses. There are two ways to think about provisioning:

1. **Customer's own credentials** — they use their existing Google, WhatsApp, Telegram, etc. accounts (best for privacy)
2. **FamCloud-provisioned accounts** — we create managed accounts for them (more control, more cost, more complexity)

The answer is **both**: we support either, but default to customer-owned credentials for privacy.

---

## Channel-by-Channel Provisioning

### 1. WhatsApp
**How it works:**
- Requires a Meta Business Account + WhatsApp Business API access
- Each business needs a verified phone number
- You **cannot** share one WhatsApp number across multiple end-users
- Each customer household = their own WhatsApp Business number (or they use their personal WhatsApp via QR pairing)

**Two approaches:**

**A. Customer's personal WhatsApp (recommended for Phase 1)**
- Customer scans QR code on their FamCloud rig's local web UI
- Uses their existing personal WhatsApp account
- Messages from that account go through FamCloud instead of their phone
- **Cost:** $0 (customer's account)
- **Risk:** Against WhatsApp ToS but everyone does it (what OpenClaw does)

**B. WhatsApp Business API (recommended for Phase 2)**
- We provision a dedicated phone number per household ($1-5/month via Twilio)
- Verified Meta Business Account per household (or one FamCloud umbrella account)
- Per-conversation pricing: ~$0.005-0.09 per message depending on region
- **Cost:** ~$5-10/month per household
- **Pros:** Legitimate, scalable, supports multiple users per household
- **Cons:** Expensive at $100/month total plan

**Verdict:** Phase 1 = personal QR pairing ($0). Phase 2 = Business API ($5-10/month, can add to plan price).

---

### 2. iMessage
**How it works:**
- **macOS ONLY** — cannot run on Linux
- Requires Messages.app signed into an Apple ID
- Each Apple ID = one iMessage identity
- Can be paired with a FamCloud rig via relay

**Approach:**
- Customer's Mac mini / MacBook runs Messages.app (can be their existing machine)
- FamCloud rig on Ubuntu connects via relay (like BlueBubbles server)
- Or: customer has a Mac mini acting as iMessage bridge
- **Cost:** $0 (uses customer's Apple ID)
- **Risk:** Apple can revoke access at any time

**Verdict:** Optional channel. Customer provides their own Apple ID. We provide relay setup instructions.

---

### 3. SMS (via Twilio)
**How it works:**
- Buy a phone number from Twilio ($1-2/month)
- Twilio forwards messages to your webhook
- Agent responds via Twilio API
- **Each agent needs its own number** — can't share one number across customers

**Approach:**
- We provision a Twilio number per household
- Or customer provides their own Twilio account + number
- **Cost:** $1-2/month per household (Twilio number) + ~$0.0079 per message
- **Verdict:** Good for customers without WhatsApp. Optional add-on ($5/month).

---

### 4. Telegram
**How it works:**
- Create a bot via @BotFather on Telegram (free)
- Get a bot token (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
- One bot per household
- **Cannot share one bot across multiple end-user groups** (but one bot CAN serve multiple people in the same household)

**Approach:**
- Bootstrap script auto-creates bot via BotFather API (or customer does it manually)
- Token stored in rig's local config
- **Cost:** FREE
- **Verdict:** Include in bootstrap. Zero cost. Best free messaging channel.

---

### 5. Discord
**How it works:**
- Create a Discord App on developer.discord.com (free)
- Get bot token
- Bot joins customer's Discord server
- **Can use one bot across multiple servers** or one bot per household

**Approach:**
- Option A: One FamCloud umbrella bot → joins customer's Discord → filters by role/channel
- Option B: One bot per household (clean isolation, but more setup)
- **Cost:** FREE
- **Verdict:** Option A (one umbrella bot) for simplicity. Zero cost.

---

### 6. Slack
**How it works:**
- Create a Slack App on api.slack.com (free)
- Install to customer's Slack workspace
- Bot gets an OAuth token
- **One app per workspace** or one app across multiple workspaces

**Approach:**
- One FamCloud umbrella Slack App → installed to customer's workspace
- **Cost:** FREE
- **Verdict:** Umbrella app approach. Zero cost.

---

### 7. Email
**How it works:**
- Each agent needs an email address to send/receive
- Options:
  - Google Workspace ($6/user/month)
  - Custom domain email (Cloudflare Email Routing — free)
  - Gmail personal account (free, but shared access issues)

**Approach:**
- Option A: Each household gets their own email address (e.g., `alice@famcloud.ai`) via G Suite
- Option B: Customer brings their own email (Gmail, Outlook, etc.)
- Option C: We provision email via Cloudflare + our domain (free, custom domain)

**Cost Analysis:**
- Option A: $6/month × N households = scales poorly
- Option B: $0 but customer setup friction
- Option C: Free (Cloudflare Email Routing) + our domain

**Verdict:** Phase 1 = customer brings their own email + OAuth. Phase 2 = subdomain email alias (`{name}@famcloud.ai`) via Cloudflare Email Routing (free).

---

### 8. Voice Calls
**How it works:**
- Twilio provides phone numbers with voice capability
- Agent can answer calls, do speech-to-text, respond with text-to-speech
- Same phone number can handle SMS + Voice
- **Cost:** ~$1/month for voice-enabled number + ~$0.013/min for calls

**Verdict:** Phase 3 feature. Not needed for launch.

---

## What the Agent Actually Needs (Minimum Viable)

### Required (Phase 1):
| Surface | Provisioning | Cost | Who Owns It |
|---------|-------------|------|-------------|
| **Telegram Bot** | Auto-created by bootstrap script | FREE | Household |
| **WhatsApp (QR pair)** | Customer scans QR on setup | FREE | Household |
| **Email (OAuth)** | Customer connects their Gmail | FREE | Household |
| **OpenRouter API** | Customer provides key (or we provision) | Included in $100/mo | FamCloud |

### Optional Add-ons (Phase 1):
| Surface | Provisioning | Cost | Who Owns It |
|---------|-------------|------|-------------|
| **SMS (Twilio number)** | Auto-provisioned | $1-2/month | FamCloud or household |
| **Discord bot** | One umbrella bot | FREE | FamCloud |
| **Slack bot** | One umbrella bot | FREE | FamCloud |

### Future (Phase 2):
| Surface | Provisioning | Cost | Who Owns It |
|---------|-------------|------|-------------|
| **WhatsApp Business API** | Per-household number | $5-10/month | FamCloud |
| **iMessage relay** | Customer's Mac + Apple ID | FREE | Household |
| **Custom email alias** | Cloudflare Email Routing | FREE | FamCloud |
| **Voice calls** | Twilio voice number | $1-5/month | Household |

---

## Shared vs. Per-Household Services

### Can Be Shared (One Instance, Many Households):
- **OpenRouter API key** — one FamCloud Org key, usage metered per household ✅
- **Discord bot** — one bot, filters by server/role ✅
- **Slack app** — one app, installed to multiple workspaces ✅
- **famcloud.ai domain** — one domain, subdomains for email ✅

### Must Be Per-Household:
- **Telegram bot** — one bot per household (can't isolate messages otherwise) ❌
- **WhatsApp** — either personal QR (customer's account) or Business API number ❌
- **SMS phone number** — one Twilio number per household ❌
- **iMessage** — customer's Apple ID ❌
- **Email** — either customer's or aliased per household ❌

---

## Bootstrap Script — What It Sets Up

```bash
#!/usr/bin/env bash
# FamCloud Bootstrap Script
# Installs everything needed for the agent to run

# 1. OS-level
# - NVIDIA drivers (for GPU inference)
# - Docker & Docker Compose (for containerized services)
# - System dependencies (python3, pip, sqlite3)

# 2. Model Runtime
# - Ollama or vLLM (model inference server)
# - Download base models (Qwen2.5-7B or our distilled model)
# - Configure model routing (which models for which tasks)

# 3. Agent Runtime
# - OpenClaw (main agent framework)
# - Configure agent identity, profiles, memory system

# 4. Channel Setup
# - Telegram: Auto-create bot via BotFather API (or customer pastes token)
# - WhatsApp: Display QR code for customer to scan (personal account)
# - Email: OAuth flow for connecting customer's Gmail
# - Discord: Instructions to invite FamCloud bot to their server
# - Slack: Instructions to add FamCloud bot to their workspace

# 5. Agent Configuration
# - Create household profile(s)
# - Set up memory system (ChromaDB)
# - Configure privacy boundaries (shared vs private memory)
# - Set parental controls if applicable

# 6. Model Update System
# - Cron job to check for new model weights nightly
# - Auto-download, test, and swap models
# - Rollback on failure

# 7. Health Monitor
# - System health checks (GPU, memory, disk, network)
# - Auto-recovery (restart services, rollback models)
# - Alert support if recovery fails

# 8. Remote Support
# - SSH key for FamCloud support access
# - Health endpoint for remote monitoring
# - Ticket creation for complex issues

echo "✅ FamCloud rig setup complete!"
echo "   Local UI: http://localhost:18789"
echo "   SSH: ssh -i ~/.ssh/famcloud-support support@famcloud.ai"
```

---

## Pricing Implications

### $100/month Plan (Standard):
Covers:
- OpenRouter API usage (models)
- Twilio SMS number (if enabled) — $2/mo
- WhatsApp Business API (if Phase 2) — $5/mo
- Remote support access
- Model updates
- Health monitoring

**Cost per household:** ~$7-12/month (variable, depending on channels enabled)
**Revenue per household:** $100/month
**Margin:** ~$88-93/month per household

### $250/month Plan (Premium):
Everything above, plus:
- Custom fine-tuning for household
- Priority support (4h SLA)
- Voice calls (Phase 3) — $3-5/mo
- Email alias management

**Cost per household:** ~$10-20/month
**Revenue per household:** $250/month
**Margin:** ~$230-240/month per household

---

## Customer Onboarding Flow

1. **Unbox rig** → plug in ethernet → rig boots
2. **Go to famcloud.local** (local web UI)
3. **Create household account** → name, admin email, phone
4. **Choose channels:**
   - [x] Telegram — auto-create bot, show QR to scan
   - [x] WhatsApp — display QR for customer to scan with their phone
   - [ ] SMS — enter phone number (we provision Twilio)
   - [ ] Discord — click to invite FamCloud bot
   - [ ] Slack — click to add FamCloud bot
   - [ ] Email — OAuth to connect your Gmail
5. **Set up family members** → name, age, relationships
6. **Set privacy/boundaries** → shared memory, parental controls
7. **Connect API key** → OpenRouter key (or we provision one)
8. **Test message** → send "Hi" to the connected channel
9. **Done** → rig runs 24/7, agent is live

---

## Key Decisions

1. **Don't provision WhatsApp Business for Phase 1** — too expensive, too complex. Use QR pairing.
2. **Telegram is the free hero channel** — auto-provision in bootstrap, zero cost
3. **Shared Discord/Slack bots** — one umbrella bot, not per-household
4. **Email: customer brings their own** → Phase 2 = Cloudflare email alias
5. **OpenRouter: one FamCloud Org key** → usage tracked per household
6. **Everything else: customer's own credentials** → we just provide the bridge

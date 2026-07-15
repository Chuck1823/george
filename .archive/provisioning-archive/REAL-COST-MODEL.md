# FamCloud — Cost Model (LOCAL MODELS only, no cloud AI costs)

## The Point
- **Every rig runs models locally. No OpenRouter. No API costs. Ever.**
- Inference = $0/month (just electricity)
- The agent has its OWN identity — phone number, email, WhatsApp, Telegram bot

---

## Agent Identity (Own Accounts)

The agent is its own entity. It has:

| Identity | Monthly Cost | Notes |
|----------|-------------|-------|
| **WhatsApp number** | $1-5/mo (Twilio/Meta) | Agent's own number for the family |
| **Phone number (SMS/calls)** | $1-2/mo (Twilio) | Agent's own number |
| **Email address** | $0 | Cloudflare routing on famcloud.ai |
| **Telegram bot** | FREE | Auto-created in BotFather |
| **Discord bot** | FREE | Auto-created in Developer Portal |
| **Slack bot** | FREE | Auto-created in Slack API |
| **iMessage** | FREE | Relay via customer's Mac (if they have one) |

---

## Agent Access to Customer's Accounts

The agent connects to family's accounts for context:

| Family Account | Agent Can | Monthly Cost |
|----------------|-----------|--------------|
| Google (OAuth) | Read calendar, send emails, access Drive | FREE (customer's account) |
| Apple Calendar | Read family calendar events | FREE (customer's iCloud) |
| Contacts | Read family's contacts | FREE |

---

## What Actually Costs Money

### Per Household:
| Item | Cost | Notes |
|------|------|-------|
| WhatsApp number | $1-5/mo | Agent's own phone number via Twilio |
| SMS/voice number | $1-2/mo | Twilio number for calls/SMS |
| famcloud.ai domain | $1.25/mo | $15/year |
| **Total** | **$3-8/month** | |

### Shared (We Run Once, All Households):
| Item | Cost | Notes |
|------|------|-------|
| Model update server | $10-20/mo total | VPS for hosting new model weights |
| SSH bastion | $5/mo total | Remote support jump server |
| Stripe fees | ~3% of revenue | Payment processing |
| **Total** | **$18-25/month** | Shared across ALL households |

### $0 Monthly (Everything Local):
- **AI inference** — runs on customer's GPU, $0
- **Memory system** — local SQLite + ChromaDB, $0
- **Message routing** — OpenClaw Gateway on rig, $0
- **Health monitoring** — local daemon, $0

---

## Pricing (Zero Cloud AI Costs)

### FamCloud — $49/month
- 1 channel (WhatsApp OR Telegram)
- Agent has own number/bot
- Local AI inference ($0 cloud costs)
- Basic memory/search (30 days)
- Up to 2 household members
- Self-serve support

### FamCloud Family — $99/month
- 3 channels (WhatsApp, Telegram, Discord/Slack/SMS)
- Agent own accounts on all channels
- Extended memory (6 months + semantic search)
- Up to 4 household members
- Per-person profiles, shared/private memory
- Basic parental controls
- Email integration (family's Gmail OAuth)
- Priority support (24h)

### FamCloud Premium — $149/month
- All channels (WhatsApp, Telegram, Discord, Slack, Signal, SMS, iMessage)
- Unlimited memory retention + advanced search
- Unlimited household members
- Advanced parental controls
- Custom email aliases (name@famcloud.ai)
- Voice calls (inbound/outbound)
- Priority support (4h)

---

## Payback Analysis

| Plan | Setup | Monthly | Our Cost | Profit | Payback |
|------|-------|---------|----------|--------|---------|
| $49/mo | $500 | $49 | $3-5 | $44-46 | 6.9 mo |
| $99/mo | $800 | $99 | $5-8 | $91-94 | 3.5 mo |
| $149/mo | $800 | $149 | $8-12 | $137-141 | 3.1 mo |

---

## Self-Serve Setup (Pre-Configured Box)

1. Customer plugs in rig → boots → goes to `famcloud.local`
2. Creates household account
3. Chooses channels to activate → we auto-provision agent's identity:
   - **We buy** a WhatsApp number for the agent ($1-5/mo)
   - **We create** a Telegram bot for the agent (FREE)
   - **We create** a phone number for SMS/calls ($1-2/mo)
   - **We create** email alias (name@famcloud.ai, FREE)
4. Customer connects their own Google account (OAuth) for calendar/email access
5. Family members message the agent at its own identities
6. Done — agent runs 24/7, all local

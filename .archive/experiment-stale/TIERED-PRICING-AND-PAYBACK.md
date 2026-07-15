# FamCloud Tiered Pricing — Payback & Economics

## Charles's Proposed Tiers

| Tier | Upfront | Monthly | Target Customer |
|------|---------|---------|----------------|
| Basic | $100 | $30 | Budget-conscious, text-only, no voice |
| Pro | $150 | $50 | Main offering, full assistant |
| Premium | $275 | $75 | Everything included, priority support |
| Lease (Low-Risk) | $0 | $65 | No upfront, they return hardware if they cancel |

## Hardware Cost Assumption: $400/rig
(Dell OptiPlex 7090 MT used + RTX 3060 12GB used + optional NVMe upgrade)

## Payback Per Tier: What YOU Pay Out of Pocket

| Tier | Customer Upfront | Your Net Hardware Cost | Monthly Profit (after shared number) | Payback Time | Total Profit Year 1 | Year 2 Annual |
|------|-----------------|----------------------|--------------------------------------|--------------|---------------------|---------------|
| Basic ($100 + $30) | $100 | $300 | $30 - $2.50 = $27.50 | 10.9 months | $230 | $330 |
| Pro ($150 + $50) | $150 | $250 | $50 - $2.50 = $47.50 | 5.3 months | $480 | $570 |
| Premium ($275 + $75) | $275 | $125 | $75 - $2.50 = $72.50 | 1.7 months | $660 | $870 |
| Lease ($0 + $65) | $0 | $400 | $65 - $2.50 = $62.50 | 6.4 months | $450 | $750 |

## What YOU Pay Out of Pocket

Yes, you're understanding correctly. If the rig costs $400 and the customer pays $100 upfront:
- **You pay $300 out of pocket per rig**
- The customer's $100 covers part of it
- The remaining $300 is covered by their monthly payments
- Payback time tells you how long until their payments have covered your $300

## Tier Breakdown: What Each Gets

### BASIC ($100 Upfront + $30/month)
- ✅ Text channels: iMessage, WhatsApp, Telegram, Discord (NO voice)
- ✅ Local memory + RAG (remembers the family's life)
- ✅ Qwen 7B model (fast, but less capable)
- ✅ Self-serve onboarding
- ❌ No voice assistant (no STT/TTS)
- ❌ No premium support
- ❌ No priority updates
- ❌ No advanced features (calendar integration, email, etc.)

### PRO ($150 Upfront + $50/month) — THE SWEET SPOT
- ✅ Everything in Basic PLUS:
- ✅ Voice assistant (STT/LLM/TTS pipeline via Pipecat)
- ✅ Qwen 14B model (better reasoning)
- ✅ Google Calendar, Gmail, Drive, Contacts integration
- ✅ Email assistant (reads/summarizes/responds)
- ✅ Homework help mode
- ✅ Priority model updates
- ✅ Standard support (automated + email)

### PREMIUM ($275 Upfront + $75/month)
- ✅ Everything in Pro PLUS:
- ✅ Priority support (live chat with Charles, 24hr response)
- ✅ Advanced distillation (model personalized from family data)
- ✅ Multi-device voice (Pipecat on multiple speakers/mics)
- ✅ Custom agent personality
- ✅ Early access to new features
- ✅ Advanced family analytics ("what did my kids ask about this week?")
- ✅ Backup + remote health monitoring

### LEASE ($0 Upfront + $65/month)
- ✅ Everything in Pro
- ❌ YOU retain hardware ownership. If they cancel, they return the box (you ship return label)
- ❌ No voice assistant for lease tier? Or charge $75/month to include voice?
- ✅ Same 12-month minimum commitment (or charge $100 cancellation fee)

## Support Automation

**Charles's idea is correct:** automate ALL support with AI agents. This is the killer feature.

### What agents can handle:
- ✅ Initial setup troubleshooting (automated wizard handles 95%)
- ✅ Connection issues (agent detects, re-pairs, restarts services)
- ✅ Performance monitoring (agent alerts you before customer notices)
- ✅ FAQ (agent answers common questions, points to self-help)
- ✅ Model updates (automated nightly updates, no customer intervention)
- ✅ Health dashboard (agent monitors rig, auto-fixes issues)

### What might need human support:
- ⚠️ Hardware failure (rig stops working, needs replacement/RMA)
- ⚠️ Customer wants custom feature not in the product
- ⚠️ Edge case bugs (something the agent can't diagnose)

**If you can get support to < 15 minutes customer/month through automation:**
- You save $35-40/customer/month in labor
- That's pure profit added to each tier
- This is actually the key to making this business work

## Hardware Longevity

### Dell OptiPlex 7090 MT + RTX 3060 Used
| Component | Expected Life | Failure Risk |
|-----------|---------------|--------------|
| OptiPlex motherboard/CPU | 5-8 years from original deployment | Low (enterprise parts, already 2 years old) |
| RTX 3060 used GPU | 3-5 years from purchase (used card) | Medium (unknown history, possible mining abuse) |
| NVMe SSD | 5+ years | Low |
| Power supply (OptiPlex OEM) | 5+ years | Low |
| DDR4 RAM | 10+ years | Very low |

**Realistic expectation: 3-5 years of reliable operation for $400/rig.**

### Why 3-5 years, not 10?
- GPU is used, unknown history — could fail any time
- OptiPlex was built 2020-2021 — already 4-5 years old at point of purchase
- Consumer hardware doesn't last forever in 24/7 operation

### At $400 and 5-year lifespan:
- **Amortized hardware cost: $6.67/month over 5 years**
- At $50/month customer payment: you're paying ~$15/month in actual hardware cost
- Remaining $35/month (minus shared number) is profit

## 100-Customer Scenarios (Mixed Tiers)

### Conservative Mix (70% Pro, 20% Basic, 10% Premium)
- 70 Pro customers: $70 × $480/year = $33,600
- 20 Basic customers: $20 × $230/year = $4,600
- 10 Premium customers: $10 × $660/year = $6,600
- **Revenue: $44,800**
- Hardware amortization: 100 × $400 = $40,000 (one-time, then profit)
- Year 1 profit: $4,800
- Year 2 recurring: $44,800 (pure profit, no hardware to buy)
- Year 2 profit: $41,800 (minus $3,000 shared number)

### Ideal Mix (50% Pro, 20% Basic, 20% Premium, 10% Lease)
- 50 Pro: $50 × $480 = $24,000
- 20 Basic: $20 × $230 = $4,600
- 20 Premium: $20 × $660 = $13,200
- 10 Lease: $10 × $450 = $4,500
- **Revenue: $46,300**
- Year 1 profit: $200
- Year 2: $43,300 pure recurring

### Premium-Heavy Mix (40% Pro, 10% Basic, 40% Premium, 10% Lease)
- 40 Pro: $40 × $480 = $19,200
- 10 Basic: $10 × $230 = $2,300
- 40 Premium: $40 × $660 = $26,400
- 10 Lease: $10 × $450 = $4,500
- **Revenue: $52,400**
- Year 1 profit: $12,400
- Year 2: $49,400 pure recurring

## Bottom Line

| Metric | Value |
|--------|-------|
| Payback per tier | 1.7 months (Premium) to 10.9 months (Basic) |
| Hardware lifespan | 3-5 years (realistic, used parts) |
| Support automation | The key to making margins work |
| Year 1 at 100 customers (mixed tiers) | $4,800 - $12,400 profit |
| Year 2 at 100 customers (pure recurring) | $41,800 - $49,400 profit |
| Support hours/customer/month (automated) | < 15 minutes |
| Effective hourly rate (if support is 15 min) | $200/hour at Pro tier |

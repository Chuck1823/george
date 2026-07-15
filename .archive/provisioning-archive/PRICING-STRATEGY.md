# FamCloud Pricing Strategy

## The Core Question: How Do We Make Money?

### Hardware Economics
- Hardware costs ~$1,120/unit
- Without setup fee: 11+ months to break even at $100/mo
- With setup fee: can break even in 3-6 months

### The Setup Fee (One-Time)
This is the biggest lever. Two models:

**Model A: You Buy Hardware, They Subscribe**
- Customer pays $100/mo, you eat the $1,120 hardware cost
- Payback: 11 months
- Risk: high upfront cost for you, but customer gets low barrier to entry
- Good for: getting first customers quickly

**Model B: Customer Pays for Hardware + Subscribe**
- Setup fee: $1,200-1,500 (you buy hardware, they reimburse + assembly fee)
- Monthly: $75-100/mo (service only)
- Payback: same day (customer covers hardware)
- Good for: your cash flow, but higher barrier for customer

**Model C: Hybrid — Partial Hardware Fee**
- Customer pays $500 setup fee (partial hardware cost)
- You cover the rest ($620)
- Monthly: $100/mo
- Payback: ~6 months
- **Best balance** of customer acquisition speed and your risk

---

## Tiered Plans

### Plan 1: FamCloud — $99/month
**Target:** Single adult or couple using basic channels
- 1-2 channels (WhatsApp QR, Telegram)
- Basic memory/search
- Basic parental controls (if kids present)
- Email integration
- Standard support
- 1 household, up to 4 members

### Plan 2: FamCloud+ — $149/month
**Target:** Family with kids, multiple channels
- **All** free channels: WhatsApp QR, Telegram, Discord, Slack
- iMessage (if customer has Apple device)
- Advanced parental controls
- Shared memory across household members
- Priority support (SLA: 24h)
- Voice calls (inbound/outbound)

### Plan 3: FamCloud Family+ — $199/month
**Target:** Premium family, all features, priority care
- **All channels** including:
  - WhatsApp Business API (dedicated number)
  - iMessage (relay via customer's Mac)
  - SMS via Twilio (dedicated number)
  - Telegram, Discord, Slack
  - Email (custom alias: name@famcloud.ai)
  - Voice calls (inbound/outbound)
- Advanced parental controls
- Shared + private memory isolation per member
- Priority support (SLA: 12h → 4h)
- Monthly model distillation from household's usage
- Early access to new features

---

## Feature-Gated Channels & Add-Ons

### Premium Channels (Gate Behind Higher Tiers or Add-Ons)

| Feature | Tier | Cost to You | Monthly Price | Notes |
|---------|------|-------------|---------------|-------|
| **iMessage** | FamCloud+ ($149) or $20/mo add-on | $0 (customer's Apple ID) | $20/mo add-on | Requires customer's Apple ID + Mac relay |
| **Voice Calls** | FamCloud+ ($149) or $15/mo add-on | $1-2/mo (Twilio) | $15/mo add-on | Inbound/outbound, agent answers phone |
| **WhatsApp Business API** | FamCloud Family+ ($199) or $10/mo add-on | $1-5/mo (Twilio/Meta) | $10/mo add-on | Dedicated number, verified |
| **SMS (Twilio)** | FamCloud+ ($149) or $5/mo add-on | $1-2/mo | $5/mo add-on | Dedicated number |
| **Custom Email Alias** | FamCloud Family+ ($199) or $5/mo add-on | $0 (Cloudflare routing) | $5/mo add-on | name@famcloud.ai |

### Free Channels (Included in All Plans)
- Telegram bot (free, auto-provisioned)
- Discord bot (free, umbrella bot)
- Slack bot (free, umbrella app)
- WhatsApp personal (QR pair, free, customer's account)

### Functionality Gates

| Feature | FamCloud | FamCloud+ | FamCloud Family+ |
|---------|----------|-----------|------------------|
| **Basic memory** (last 30 days) | ✅ | ✅ | ✅ |
| **Extended memory** (unlimited + semantic search) | ❌ | ✅ | ✅ |
| **Shared memory across household** | ❌ | ✅ | ✅ |
| **Private memory (per-person)** | ❌ | ❌ | ✅ |
| **Basic parental controls** | ✅ | ✅ | ✅ |
| **Advanced parental controls** (approval flows, spending locks) | ❌ | ✅ | ✅ |
| **Auto model updates from distillation** | ❌ | ❌ | ✅ |
| **Priority support SLA** | ❌ | 24h | 4h |

---

## What People Will Pay

### Value Perception:
- **Personal AI that knows the whole family:** $99-149/month (vs $20 ChatGPT, this is $20 for 1 person → $99 for whole family, each member gets personalized AI)
- **Privacy guarantee (your data never leaves your house):** $50/month premium vs cloud-only
- **Family parental controls + safety:** $30-50/month premium
- **iMessage (seamless Apple ecosystem):** $20/month premium (Apple users pay for ecosystem)
- **Voice calls (agent answers phone for you):** $15/month (saves missed calls, answers basic questions)
- **WhatsApp Business API (verified, reliable):** $10/month premium

### Target Customer Profile:
- Parent (30-45 years old)
- 2+ kids in household
- Income: $80k+ household
- Tech-comfortable but busy
- Already uses WhatsApp or iMessage
- Values privacy
- Willing to pay for convenience + safety

### Estimated WTP (Willingness To Pay):
- **Single adult, basic use:** $49-79/month
- **Family, 1-2 channels:** $99-149/month
- **Family, all channels, premium features:** $149-199/month
- **Power family (wants every feature):** $199-249/month

---

## Setup Fee Structure

### Recommended: $500-800 One-Time Setup Fee
This covers:
- **Hardware assembly** ($1,120 cost → you cover $320-620, customer covers $500-800)
- **Manual installation** at customer's home (your time: 2-3 hours)
- **Configuration:** channel setup, profiles, parental controls
- **First month of support**

### Why a Setup Fee Works:
1. **Reduces your risk:** $500 setup + $100/mo = hardware pays back in ~6 months, not 11
2. **Filters serious customers:** People who pay setup fees are committed
3. **Covers your installation time:** $500 / 3 hours = $167/hour (worth your time)
4. **Psychological commitment:** Sunk cost = lower churn

### Alternative: $0 Setup, Higher Monthly
- $149-199/month, no setup fee
- Customer gets hardware "free" (you absorb cost)
- You own the hardware, customer rents it
- Risk: customer churn after 3 months = you lose money
- Risk: you need $1,120 per customer upfront = $11,200 for 10 customers

**Recommendation: Offer BOTH options**
- **Plan A:** $500 setup + $99/mo (customer pays partial hardware, lower monthly)
- **Plan B:** $0 setup + $149/mo (you cover hardware, higher monthly, you own hardware)

---

## Summary: Recommended Pricing Structure

### Two-Tier Monthly Plans:

| Plan | Setup Fee | Monthly | Channels | Memory | Parental | Support |
|------|-----------|---------|----------|--------|----------|---------|
| **FamCloud** | $500 | $99 | 1-2 | Basic | Basic | Standard |
| **FamCloud+** | $800 | $149 | All | Extended | Advanced | Priority |

### Add-Ons (Any Plan):
- **iMessage relay:** +$20/mo
- **Voice calls:** +$15/mo
- **WhatsApp Business API:** +$10/mo
- **Custom email alias:** +$5/mo
- **SMS via Twilio:** +$5/mo

### Payback Scenarios:
| Plan | Your Hardware Cost | Monthly | Setup Fee | Payback Time | Year 1 Revenue | Margin After Year 1 |
|------|-------------------|---------|-----------|--------------|----------------|-------------------|
| $500 setup + $99/mo | $1,120 | $99 | $500 | 6.3 mo | $1,688 | $1,188/year |
| $800 setup + $149/mo | $1,120 | $149 | $800 | 2.1 mo | $2,588 | $1,788/year |

---

## Implementation Timeline

### Phase 1 (Month 1-3): Basic Offer
- **FamCloud:** $100/month, $500 setup
- Channels: WhatsApp QR, Telegram
- Basic memory, basic parental controls
- Test with 2-3 households (friends/family)

### Phase 2 (Month 4-6): Add Premium Features
- **FamCloud+:** $149/month, $800 setup
- Add iMessage, voice calls, WhatsApp Business API
- Extended memory, advanced parental controls
- Priority support SLA

### Phase 3 (Month 7-12): Scale + Automation
- **Self-serve onboarding** (no manual install)
- Hardware ships pre-configured
- Reduce setup fee to $300 (automation saves your time)
- **FamCloud Family+:** $199/month, auto model distillation from household usage
- Target: 50 households, $7,500/month MRR

---

## Key Questions to Answer

1. **Can iMessage work without a Mac at customer's house?**
   - NO. iMessage requires macOS + Apple ID. Customer needs an Apple device.
   - Your relay just connects their Mac to the FamCloud rig on the network.

2. **Do we need a WhatsApp Business Account per household?**
   - YES, if using WhatsApp Business API. Each household gets a dedicated number.
   - QR pairing (Phase 1) = customer's personal account, one per household.

3. **Can one Discord bot serve multiple customers?**
   - YES. One FamCloud umbrella bot → joins each household's Discord → filters by server.
   - OR: you can spin up one bot per household for isolation (cleaner, but more setup).

4. **Can one Slack app serve multiple workspaces?**
   - YES. Install the FamCloud Slack app to each household's workspace.
   - One app, many workspaces. Each installation gets its own OAuth token.

5. **Can we share one Twilio phone number across customers?**
   - NO. Each household needs their own number (SMS routing, voice routing).
   - You'd need separate Twilio numbers (or separate Twilio accounts).

6. **Can we share one email alias domain across customers?**
   - YES. `@famcloud.ai` domain → email aliases per customer (name@famcloud.ai).
   - Cloudflare Email Routing (free) forwards to their actual inbox.
   - Outbound from FamCloud via their real email (OAuth) or via SMTP.

---

## What to Feature Date (Launch Sequence)

### Month 1: MVP Launch
- ✅ WhatsApp QR (personal)
- ✅ Telegram bot (auto-provisioned)
- ✅ Basic memory
- ✅ Basic parental controls
- ✅ Standard support
- **Price: $100/month + $500 setup**

### Month 3: v1.1
- ✅ Discord integration
- ✅ Slack integration
- ✅ Extended memory + search
- ✅ Priority support (24h SLA)
- **Add: FamCloud+ tier at $149/month**

### Month 6: v2.0
- ✅ iMessage relay (requires customer's Mac)
- ✅ Voice calls
- ✅ Advanced parental controls
- ✅ WhatsApp Business API
- ✅ Custom email aliases
- **Add: $199/month Family+ tier**

### Month 9: v3.0
- ✅ Auto model distillation from household usage
- ✅ Self-serve onboarding (no manual install)
- ✅ Pre-configured hardware shipping
- **Reduce setup fee to $300**
- **Target: 50 households**

# FamCloud Agent-Native Tool Stack (Final with Pricing)

## The Reality: AgentPhone numbers are expensive

AgentPhone's pricing page doesn't list exact costs but the model is pay-as-you-go for phone numbers provisioned for agents. Based on market research and the pricing model, expect $5-25/month per number for phone + iMessage + SMS + voice routing.

**Photon (Spectrum) is the better alternative for iMessage:**
- **Free tier:** Shared iMessage lines — Photon maintains a pool, assigns each user a fresh number. Up to 10 users. FREE.
- **Pro tier:** $25/month — shared lines, up to 100 users. Includes iMessage + RCS + SMS + Telegram.
- **Business tier:** $250/month — dedicated iMessage line. All users get same dedicated number. Unlimited users. Unlimited messages.

**Key insight: We can share ONE dedicated number ($250/mo) across MULTIPLE households.**

---

## Shared Number Model

### Concept: One dedicated iMessage + phone number, shared across households

Instead of buying one number per household ($250/mo × N households = insane), we buy ONE Business-tier number from Photon ($250/mo) and route messages to individual household agents based on sender context.

### How it works:
1. We buy ONE Business-tier iMessage number from Photon ($250/month)
2. This number is shared across all FamCloud households
3. When a family member texts the number, Photon receives it
4. Photon routes the message to the right household's agent based on:
   - The sender's phone number/Apple ID (we maintain a mapping)
   - The message content (context-based routing)
5. The household agent processes locally on their rig
6. The agent's response goes back through Photon → iMessage → recipient

### Cost per household (amortized):
| Metric | Value |
|--------|-------|
| Business-tier number | $250/month |
| Households supported | 100+ (Photon Business allows unlimited users) |
| Cost per household | $2.50/month at 100 households |
| Cost per household | $1.25/month at 200 households |
| Cost per household | $0.63/month at 400 households |

### Why this works:
- Photon's Business tier explicitly supports "unlimited users" and "full group messaging iMessage API access"
- We're not cold-calling — we're handling inbound messages from known households
- Cold outreach support (50 new contacts/day) is separate from our use case (inbound family messages)
- One number = one identity for all FamCloud agents (like how a company has one support number)

### The customer experience:
- Family member texts the FamCloud number (e.g., +1-555-123-4567) with their message
- Photon routes to the right rig based on sender identity
- Agent processes on the rig, responds
- Family member sees the response from the same number (blue bubble if iMessage)
- No difference from texting a personal assistant

### The trade-off:
- All households share one phone number (not unique per household)
- But each household has their own agent instance with their own memory, context, identity
- The number is just the routing mechanism, not the agent identity
- Family members don't know or care that the number is shared — they just text it

---

## Alternative: Photon Free/Pro Tiers (no dedicated number)

### Photon Free: Shared lines, up to 10 users
- Photon maintains a pool of numbers
- Each recipient gets a fresh number they've never seen before
- Different recipients may see different sending numbers
- Each conversation stays stable (same number for same contact)
- **Cost: FREE**
- Limit: 10 users (i.e., 10 household contacts per agent)

### Photon Pro: Shared lines, $25/month, up to 100 users
- Same as Free but with 100 users instead of 10
- Priority support
- **Cost: $25/month shared across all households**

### Pro-tier sharing math:
- $25/month ÷ 50 households = $0.50/household/month
- $25/month ÷ 100 households = $0.25/household/month
- $25/month ÷ 200 households = $0.125/household/month

### Pro vs Business:
- Pro: Different contacts may see different numbers. Stable per-contact but not unified.
- Business: Everyone sees the same dedicated number. One consistent identity.

**Recommendation for Phase 1:** Start with Photon Free (up to 10 users, free). As we scale, upgrade to Pro ($25/month, 100 users). At 50+ households, Business ($250/month, dedicated number) makes sense.

---

## Updated Per-Household Cost (Amortized)

### Phase 1 (Photon Free, shared lines):
| Item | Monthly Cost |
|------|-------------|
| Photon Free (shared iMessage lines) | FREE |
| WhatsApp (self-hosted Baileys) | FREE |
| Telegram, Discord, Slack, Signal | FREE |
| famcloud.ai domain (amortized) | $1.25 |
| **Total** | **$1.25/month** |

### Phase 2 (Photon Pro, shared lines):
| Item | Monthly Cost |
|------|-------------|
| Photon Pro ($25/mo ÷ 50 households) | $0.50 |
| Everything else (same as Phase 1) | $1.25 |
| **Total** | **$1.75/month** |

### Phase 3 (Photon Business, dedicated number):
| Item | Monthly Cost |
|------|-------------|
| Photon Business ($250/mo ÷ 100 households) | $2.50 |
| Everything else (same as Phase 1) | $1.25 |
| **Total** | **$3.75/month** |

### Phase 3 at scale (Photon Business ÷ 500 households):
| Item | Monthly Cost |
|------|-------------|
| Photon Business ($250/mo ÷ 500 households) | $0.50 |
| Everything else | $1.25 |
| **Total** | **$1.75/month** |

---

## Final Pricing Tiers (With Updated Costs)

| Plan | Monthly | Setup Fee | Our Cost | Profit | Margin |
|------|---------|-----------|$49+$500 | $1.25-3.75 | $45-48 | 92% |
| Family ($99/mo) | $99 | $800 | $1.25-3.75 | $95-98 | 96% |
| Premium ($149/mo) | $149 | $800 | $1.25-3.75 | $145-148 | 97% |

**Key insight:** Amortizing the shared number cost across multiple households brings per-household cost down to $0.50-3.75/month depending on scale and tier. This is MUCH cheaper than one number per household.

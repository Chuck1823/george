# Nail Salon Vertical — Deep Dive

**Date:** 2026-07-12
**Status:** Exploring
**Region:** New Jersey (dense nail salon market)

---

## Why Nail Salons Are a Perfect First Vertical

1. **Density.** NJ has ~3,000+ nail salons. Charles can walk into 50 in a month.
2. **Pain is obvious.** Phone rings constantly. Owner answers between clients. Missed calls = lost money.
3. **Simple service structure.** Fixed menu, fixed prices, fixed time blocks. Easy for an agent to learn.
4. **Repeat business model.** Customers come back every 2-3 weeks. Retention matters.
5. **Language barriers common.** Korean/Vietnamese/Chinese-speaking owners, English-speaking customers. An AI that's bilingual is a huge unlock.
6. **Low tech adoption.** Most use paper books, whiteboards, or a basic booking app. Nobody has an AI agent.
7. **Word of mouth travels fast.** Salon owners talk to each other. One happy customer = 5 referrals.
8. **Low price sensitivity for tools.** If it saves 5 hours/week of phone management, $40-85/mo is nothing.

---

## What Nail Salons Actually Do All Day

### Customer-Facing (What the Agent Handles)
- "What are your hours?"
- "Do you take walk-ins or appointments only?"
- "How much is a full set/gel/fill?"
- "How long does a full set take?"
- "Do you have availability today at 3?"
- "Can I book a full set and gel color for 4pm?"
- "Is [technician name] working today?"
- "I have a coupon from Instagram — can I use it?"
- "Do you do nail art?"
- "Is [X design] extra?"
- "My nails are lifting after 5 days, can I come in for a fix?"
- "I canceled — can I reschedule?"
- "What's your address? Parking?"
- "Do you accept credit cards?"
- "Can I bring my kid?"
- Review replies on Google/Yelp
- Reminder texts for appointments
- Follow-up: "Thanks for visiting, when's your next fill?"

### Owner-Facing (What the Agent Helps With)
- Daily briefing: today's 12 appointments, 3 walk-ins expected
- "Call [supplier] and reorder acetone and tips"
- Staff schedule: "Who's working Thursday?"
- "Text everyone with appointments tomorrow — remind them"
- "How many no-shows this month?"
- "Who hasn't come in 6 weeks? Send them a text"
- "What was our busiest service last week?"

### Pain Points (Where Money Is Lost)
| Pain | Cost |
|------|------|
| Missed calls (owner answering while doing nails) | 10-20 calls/day × even 2 customers lost/week = $200-400/week |
| No-shows (no reminders) | 2-3 no-shows/week × $35 avg = $70-105/week |
| Customer attrition (no follow-up) | 5-10 customers/month who never come back |
| Owner time on phone | 2-4 hours/day answering the same 5 questions |
| Language barrier | Lost customers who call and can't communicate |
| Double bookings | Messy customer experience |

---

## Architecture: What It Plugs Into

### Simple Setup (MVP)
1. **Shared phone number** — port their number or get a new one via Twilio
   - Or: agent calls their existing line and answers incoming calls
   - Or: use WhatsApp Business number (many salons already have this)

2. **WhatsApp/SMS** — most salon customers text already
   - "Hey, do you have space today?" → texts the agent
   - Agent responds with availability, books, confirms

3. **Google Business Profile integration** — reads/responds to reviews
4. **Simple booking calendar** — shared Google Calendar or a basic booking tool
5. **Business info database** — services, prices, hours, tech availability (structured JSON)

### Advanced Setup (Phase 2-3)
- **POS integration** — Square (common at salons), reads transactions, customer history
- **Booking software** — Vagaro, Boulevard, Fresha, Mindbody (major salon booking platforms)
- **Website chat widget** — embed a chat bubble on their existing site
- **Instagram DM automation** — many salon bookings happen via IG DMs
- **Voice (Pipecat)** — incoming calls answered by the agent

### How the Box Works In-Store
```
[Owner] ───→ Sets up box, enters business info (services, prices, hours, staff)
              │
              ├── Agent learns: 20 services, prices, durations
              ├── Agent connects to: Google Calendar (bookings), WhatsApp Business
              └── Agent connects to: Google Business Profile (reviews)

[Customer calls/texts] ───→ Twilio routes to agent on box
                              │
                              ├── Answers: hours, prices, availability
                              ├── Books: adds to Google Calendar
                              └── Confirms: sends confirmation text

[Owner asks agent] ───→ "Send reminder to everyone tomorrow"
                         │
                         └── Agent texts 12 customers with appointments
```

---

## Agent Skills for Nail Salons (Priority Order)

### P0 — Launch (Week 1-4)
| Skill | Details |
|-------|---------|
| **Phone answering** | Answers 24/7. Uses business script. Takes messages if booking not available. |
| **FAQ responses** | Hours, prices, services, walk-in policy, address, parking |
| **Booking via text** | Reads calendar, offers times, adds to calendar |
| **Appointment reminders** | 24hr and 2hr reminder texts |
| **Review monitoring** | Monitors Google reviews, drafts responses for owner approval |

### P1 — Month 2-3
| Skill | Details |
|-------|---------|
| **Order status for returns/fixes** | "My gel lifted after 3 days" → books a fix appointment |
| **Customer retention texts** | "Haven't seen you in 3 weeks — time for a fill?" |
| **Staff schedule management** | "Who's working Saturday?" |
| **Bilingual support** | Auto-detects English/Korean/Vietnamese, responds in same language |
| **Coupon/promo tracking** | Validates Instagram coupon codes, applies discounts |

### P2 — Month 4-6
| Skill | Details |
|-------|---------|
| **POS integration** | Reads Square for customer history, average spend |
| **Instagram DM** | Auto-replies to booking questions on IG |
| **Supply reorder alerts** | "You're running low on Gel-X tips, order more?" |
| **Revenue tracking** | "How much did you make last week vs. this week?" |
| **No-show prediction** | Identifies customers likely to no-show, sends extra reminders |

---

## Training Data Needed

### Synthetic Q&A (Generate with 32B)
Generate ~2,000 Q&A pairs per salon:

**Standard questions:**
- Hours, location, parking
- Service pricing (full set, gel fill, SNS, nail art, removals, pedicures, combos)
- Duration estimates ("how long for a full set?")
- Walk-in policy
- Accepted payment methods
- Gift cards
- Kids policy
- COVID/sanitize questions

**Booking flow:**
- Check availability
- Book appointment
- Cancel/reschedule
- Add person to existing appointment
- Request specific technician

**Complaint/handling:**
- "My nails broke/lifted/popped off"
- "I hate this color"
- "The technician was rude"
- Escalation to owner

**Upsell/cross-sell:**
- "Do you recommend gel or regular?"
- "What's the difference between SNS and gel?"
- "Do you do nail art?" → "Yes, add $10-25 depending on design"

**Bilingual:**
- Same QA pairs in Korean and Vietnamese (common for NJ salons)

### Real Data to Collect
1. Record/observe 20-30 real phone interactions at partner salons
2. Get their most-asked questions from the front desk
3. Review their existing website/Instagram for service info
4. Study 5 local salon websites for pricing/service structure
5. Google/Yelp reviews for common questions and complaints

### Enrichment (Opus/Sol)
- Grade all synthetic responses for realism, warmth, accuracy
- Add industry-appropriate tone (friendly but professional)
- Flag unrealistic responses ("Sure, I can paint your nails in 30 seconds!")
- Add context: "We use CND Shellac for all gel services"

---

## Pricing for Nail Salons

Same hardware ($400/rig), reframed.

| Tier | Upfront | Monthly | What They Get | Payback | ROI Pitch |
|------|---------|---------|---------------|---------|-----------|
| **Starter** | $150 | $40 | Phone answering + WhatsApp + FAQs + booking | ~7 mo | "Catches 2 missed calls/week = $80" |
| **Business** | $200 | $65 | Everything + reminders + reviews + bilingual | ~4 mo | "Reduces no-shows 50% = saves $150/week" |
| **Growth** | $300 | $95 | Everything + retention texts + POS + IG DMs | ~3 mo | "Brings back 5 lost customers/month = $500" |

### ROI Math (Selling the Owner)
"Let's say you do ~40 customers/week at $35 average = $1,400/week."
"You probably miss 5-10 calls/day because you're working. Even if 2 of those book elsewhere, that's $70/week lost."
"Our agent catches those calls. $40/month pays for itself with ONE extra customer."
"Plus reminders cut no-shows in half. Another $75/week."
"Plus customer retention texts bring back people who forgot. Another $50/month."
"Total value: $250+/month. Your cost: $40-95/month."
"You're leaving $150+/month on the table by not having this."

---

## Go-To-Market: The NJ Nail Salon Sprint

### Week 1-2: Research & Prep
- Visit 10-15 nail salons in Charles's area (just to observe and ask questions)
- Map out typical service menus, prices, hours, booking methods
- Record the 20 most common questions every salon gets
- Build a demo: configure a box with a fake salon's data
- Prepare a one-pager: "Never miss a customer call again"

### Week 3-4: Pilot (3-5 Salons)
- Approach 5 salons with the demo
- Offer: free for 30 days, then $40/mo or return the box
- Install the box, set up services/prices/hours in the system
- Connect their WhatsApp Business number
- Monitor accuracy for 2 weeks, fix gaps

### Week 5-8: Iterate & Close
- Fix all the gaps the pilot shows
- Get testimonials from pilot salons ("We got 8 extra bookings this week")
- Use testimonials to close more salons
- Build a case study PDF

### Month 3-6: Scale
- Target 20-30 salons
- Referral program: $50/mo credit per referral
- NJ has 3,000+ nail salons. Getting to 100 is a real target in year 1.

---

## The Bilingual Angle (Competitive Moat)

Most NJ nail salon owners are Vietnamese or Korean. Their staff speaks Vietnamese/Korean. Their customers speak English.

If the agent can:
- Answer customer calls in English
- Switch to Korean/Vietnamese when talking to the owner/staff
- Handle booking in any language
- Translate messages between staff and customers

**That alone is a competitive moat.** No existing tool does this well, and certainly not at $40/mo.

This could even be the **primary sales pitch** in NJ: "Your customers call in English. You speak Korean. Our agent handles both."

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Salon doesn't have Wi-Fi | Mobile hotspot or Ethernet. Box has both. |
| Salon doesn't understand tech | White-glove setup. "Just plug it in." |
| Agent gives wrong price | Owner approves all prices during setup. Agent reads from config. |
| Double-booking | Agent reads Google Calendar in real-time. Won't book conflicting times. |
| Customer wants a human | "Let me have the owner call you back" → routes to owner's cell |
| Agent sounds robotic | Use Pipecat with a warm, natural TTS voice. Or limit to text first. |
| Salon goes out of business | They're small but the market is huge. Volume > retention. |

---

## Nail Salon vs. Other SMB Verticals (Comparison)

| Factor | Nail Salons | Dry Cleaners | Restaurants | Hair Salons |
|--------|------------|-------------|-------------|------------|
| Call volume | Very high | Medium | Very high (takeout) | Medium |
| Booking complexity | Low-medium | Very low | Medium | Medium-high |
| Repeat customer rate | Very high | High | Low-medium | High |
| Service standardization | High | High | Low | Low |
| Bilingual need | Very high | Medium | Low | Low |
| Willingness to pay | Medium | Low | Medium-high | Medium |
| Owner on phone? | Always | Sometimes | Often | Often |
| Easy to demo? | Yes | Yes | No (busy hours) | No (styling) |

**Nail salons win on: call volume, repeat rate, standardization, bilingual need, and demo-friendliness.**

---

## Next Steps

1. Pick 5-10 salons within driving distance
2. Visit them, ask about their biggest pain points
3. Build a demo with a fake salon (use a real salon's public info)
4. Test the demo: "Call this number, ask about pricing"
5. Get 3 pilot customers (free for 30 days)
6. Measure: calls answered, bookings made, no-shows reduced
7. Package results into a case study
8. Use case study to sell the next 20

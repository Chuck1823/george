# FamCloud Customer Acquisition & Agent Architecture

## Customer Acquisition Strategy

### Phase 1: Friends & Family (Months 1-3)
**Target: 5-10 customers**

- **Who:** People you know who already talk to you about AI
- **How:** "I built something. Can you try it?" — personal ask, no sales pitch
- **Cost:** $0 (you already know them)
- **Why it works:** They'll give you honest feedback, tolerate bugs, refer others
- **Expected conversion:** 20-30% of people you ask

### Phase 2: Word of Mouth (Months 3-6)
**Target: 20-30 customers**

- **How:** Each happy customer refers 1-2 friends/families
- **Mechanism:** "I use this family AI thing, it's actually really good. Want an intro?"
- **Cost:** $0 (organic)
- **Why it works:** Trust transfer. If their friend uses it and loves it, they'll try it
- **Referral incentive:** $50 credit for both referrer and new customer

### Phase 3: Organic Content (Months 6-12)
**Target: 30-50 customers**

**Where to post:**
- **Twitter/X:** Build in public. Share daily progress, screenshots, wins. Tech Twitter loves hardware + AI combos.
- **YouTube:** 10-min video: "I Built a Family AI That Lives in My House" — demo the rig, show it working
- **Reddit:** r/selfhosted, r/homelab, r/LocalLLaMA — communities that care about local-first AI
- **Hacker News:** "Show HN: FamCloud — Personal AI Assistant That Lives in Your Home"
- **Discord servers:** AI/tech communities, homelab communities

**Cost:** $0 (your time)
**Expected:** 1-5 customers per month from organic content
**Timeline:** Takes 3-6 months to build audience. Content compounds over time.

### Phase 4: Paid Campaigns (Months 12+)
**Target: 50-100+ customers**

**Only start paid ads AFTER you have 20-30 customers who are happy.**

**Google Ads:**
- Keywords: "family AI assistant", "local AI assistant", "personal AI at home"
- Cost: $1-3 per click
- Conversion rate: 2-5% (landing page → sign up)
- **Cost per customer: $50-150**
- Monthly budget: $500-1,000 → 5-20 new customers
- **ROI:** At $600/year revenue per customer (Pro tier), spending $50-150 to acquire is profitable

**Facebook/Instagram Ads:**
- Target: Parents 30-50, income $80k+, interested in AI/tech
- Cost: $3-8 per click
- Video ad: "This AI remembers everything about your family"
- **Cost per customer: $80-200**
- Monthly budget: $500-1,000 → 5-10 new customers
- **ROI:** Similar to Google, but harder to prove intent

**YouTube Ads:**
- Target: Tech YouTubers' audiences, homelab channels
- Cost: $0.05-0.15 per view
- Video ad: 15-second demo of FamCloud
- **Cost per customer: $30-80**
- Monthly budget: $300-500 → 5-10 new customers
- **ROI:** Better than Facebook for this product (tech audience)

### Total Customer Acquisition Cost Summary

| Channel | Cost per Customer | Monthly Budget | Customers/Month | Timeline |
|---------|-------------------|----------------|-----------------|----------|
| Friends/family | $0 | N/A | 5-10 total | Months 1-3 |
| Word of mouth | $0 (referral credit) | $50/month (credits) | 5-10 | Months 3-6 |
| Organic content | $0 (time) | N/A | 1-5 | Months 6+ |
| Google Ads | $50-150 | $500-1,000 | 5-20 | Months 12+ |
| YouTube Ads | $30-80 | $300-500 | 5-10 | Months 12+ |
| Facebook Ads | $80-200 | $500-1,000 | 5-10 | Months 12+ |

**Total blended cost per customer: $30-150** (depending on channel mix)

**Break-even on acquisition cost:**
- Customer pays $150 upfront + $50/month
- If CAC = $100, you net $50 from upfront on acquisition
- Monthly profit starts immediately
- **No negative cash flow on customer acquisition**

---

## Customer Acquisition Math: Reaching 100 Customers

### Timeline:
- **Month 1-3:** 5-10 (friends/family)
- **Month 3-6:** +15-25 (word of mouth)
- **Month 6-9:** +10-20 (organic content starts working)
- **Month 9-12:** +15-25 (paid ads start)
- **Month 12-18:** +40-60 (ads + referrals compound)
- **Goal: 100 customers in 12-18 months**

---

## Agent Architecture (Charles's Ideas)

### 1. The Agent Harness
This is the orchestration layer. It manages:
- **Message routing** (iMessage → agent, WhatsApp → agent, etc.)
- **Memory retrieval** (find relevant family context for each query)
- **Tool execution** (calendar, email, search, etc.)
- **Response generation** (run model, format output)
- **Health monitoring** (is the agent alive? responding? stuck?)
- **Model updates** (push new distilled model versions to rigs)

**What Charles builds:**
- Agent harness = code in the OpenClaw workspace
- Pipecat for voice pipeline
- Channel plugins (WhatsApp, Telegram, etc.)
- Memory system (vector DB or RAG)
- Model distillation scripts

**What runs on each customer's rig:**
- OpenClaw (the agent harness)
- Ollama (serves the model)
- Pipecat (voice pipeline)
- Memory store (family's data)
- AgentPhone/Baileys (message routing)

### 2. Family Knowledge Graph + Memory

**This is the real competitive advantage.** Not just "the agent remembers your messages" — but "the agent knows your family's structure."

**What the knowledge graph tracks:**
- Family members: Mom, Dad, Sarah (8), Jake (5), Grandma Linda
- Relationships: Sarah is Mom's daughter, Jake is Dad's son
- Schedules: Soccer (Tue 4pm), Dentist (Wed 10am), Movie Night (Fri)
- Preferences: Mom hates early meetings, Jake loves dinosaurs
- History: What was discussed, decisions made, questions asked
- Patterns: "Family asks about calendar 40% of queries, homework 30%"

**How it's stored:**
- Local vector DB (Chroma/FAISS) — semantic search over conversations
- Structured JSON/graph DB — family structure, preferences, schedules
- Both stored on the customer's rig, never leaves the home

**What the agent does with it:**
- When Sarah asks "When is my soccer game?", it queries: "Find schedule for [Sarah] [soccer] this week"
- When Mom asks "What did we eat last Friday?", it queries: "Find conversation about meals on [2026-07-07]"
- When Jake asks "Tell me about dinosaurs", it knows he likes dinosaurs, responds accordingly

### 3. LoRA Adapters Per Family

**The idea:** Each family gets their own fine-tuned adapter that personalizes the base model.

**How it works:**
1. Base model: Qwen 14B (general, distilled from public data)
2. Family adapter: LoRA trained on THAT family's conversations (stored locally)
3. Inference: Base model + Family adapter = personalized responses
4. Privacy: Adapter stays on the family's rig, never leaves

**When to train adapters:**
- Nightly (automated): re-train adapter from last 24h of conversations
- Weekly: full re-training from all historical conversations
- Trigger-based: re-train when adapter quality degrades

**Premium Tier Addition:**
- Basic/Pro: Memory + RAG only (no LoRA)
- Premium: LoRA adapter + nightly updates
- Premium customer gets: Model that gets noticeably better about their family every week

**Why it's premium:**
- LoRA training uses more GPU (slower inference, more VRAM)
- Requires more sophisticated distillation pipeline (Charles' work)
- Higher compute cost per family
- Justifies the $75/month Premium tier

### 4. Automating Support (Charles's Plan: 100% Automated)

**If you can actually do this, the business model changes dramatically:**

**What agents handle:**
- ✅ Initial setup: Wizard guides user through QR pairing, channel config
- ✅ Connection issues: Agent detects disconnects, re-pairs, restarts services
- ✅ Performance: Agent monitors GPU temps, memory usage, alerts you BEFORE customer notices
- ✅ FAQ: Agent answers common questions, links to docs
- ✅ Model updates: Automated push, no customer intervention
- ✅ Health checks: Daily rig health report sent to your dashboard
- ✅ Troubleshooting: Agent runs diagnostics, suggests fixes
- ✅ Billing: Automated invoice generation, payment processing

**What might need Charles:**
- ⚠️ Hardware failure (rig physically breaks → need to send replacement)
- ⚠️ Edge case bugs (agent can't diagnose → Charles investigates)
- ⚠️ Customer wants custom feature not in the product

**If 95% automated:**
- Support hours: ~20 minutes/customer/month total
- At 100 customers: ~33 hours/month → ~1 hour/day
- Effective hourly rate: $5,000/month ÷ 33 hours = **~$150/hour**
- This is an amazing business

---

## Revenue at 100 Customers (Mixed Tiers, Automated Support)

| Metric | Value |
|--------|-------|
| Tier Mix | 20 Basic, 50 Pro, 20 Premium, 10 Lease |
| Monthly Revenue | $10,300 |
| Shared Number Cost | $250 |
| Hardware Amortization | $667/month ($400 × 100 ÷ 60 months) |
| Ad/Marketing Cost | $500/month (conservative) |
| **Monthly Profit** | **$8,883** |
| Annual Profit | **$106,596** |
| Time to Build | 12-18 months |
| Ongoing Work | ~1-2 hours/day (automated support) |

---

## The Agent Harness: What Charles Actually Builds

### Core Components:
1. **OpenClaw config** — agent definition, channel routing, memory
2. **Pipecat pipeline** — STT → LLM → TTS for voice
3. **Memory system** — vector DB + knowledge graph (local)
4. **Model distillation loop** — export → grade → distill → deploy
5. **LoRA adapter system** — per-family training, deployment, update
6. **Monitoring dashboard** — rig health, usage, billing
7. **Self-serve onboarding wizard** — famcloud.local:18789/setup
8. **Support agent** — automated troubleshooting, FAQ, diagnostics

### What Runs Where:
- **On each customer's rig:** OpenClaw + Ollama + Pipecat + Memory + Model + Adapter
- **On Charles's server (your Mac mini):** Distillation pipeline, monitoring dashboard, model update server
- **On Charles's server:** Shared number pool (AgentPhone/Baileys) — or self-hosted

### Distillation Pipeline:
1. Export traces from all rigs (metadata only, never raw messages)
2. Grade/filter traces
3. Distill: train smaller model from teacher (large model) + synthetic data
4. Deploy: push new model to all rigs overnight
5. LoRA adapter: nightly per-family adapter training on each rig

---

## Bottom Line: What Charles Actually Needs to Build

**Phase 1 (Weeks 1-4):**
- VM test of bootstrap + OpenClaw
- Basic agent harness (message routing, model serving, memory)
- Self-serve onboarding (QR scan → channels → done)
- First customer: a friend/family member

**Phase 2 (Weeks 5-12):**
- Family knowledge graph (structured memory)
- Model distillation pipeline (general improvement)
- Monitoring dashboard (rig health)
- Support agent (automated troubleshooting)
- 10 customers (friends + referrals)

**Phase 3 (Months 4-8):**
- LoRA adapter system (per-family personalization)
- Premium tier (adapter + nightly updates)
- Paid acquisition starts
- 30-50 customers

**Phase 4 (Months 9-18):**
- Scale to 100+ customers
- Fully automated support
- Model update pipeline mature
- $10k/month revenue

**This is a 2-person part-time job for 12-18 months, then scales to a full-time income with <2 hrs/day maintenance.**

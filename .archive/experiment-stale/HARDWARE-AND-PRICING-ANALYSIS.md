# Dell OptiPlex MT + RTX 3060 — Hardware Deep Dive

## What is a Dell OptiPlex MT?

Dell OptiPlex is Dell's **enterprise desktop line**. Sold to corporations, schools, government offices in bulk. When those organizations upgrade (every 3-5 years), thousands of these go on the used market **dirt cheap**.

**MT = Mini Tower.** The FULL-size version. Not the slim SFF variant. This is critical because:
- **MT (Mini Tower):** Fits FULL-size desktop GPUs (standard height, standard power connectors)
- **SFF (Small Form Factor):** Only fits LOW-PROFILE GPUs (shorter, less powerful, more expensive)
- **Micro/Tiny:** No dedicated GPU slot at all — forget it

**Why OptiPlex is great for FamCloud:**
- Enterprise-grade motherboards, PSUs, cases — way better quality than consumer boxes
- i7 10th/11th gen processors available
- 16-32GB RAM common
- Proper cooling, proper PSU (usually 260-500W, enough for RTX 3060)
- Standard PCIe x16 slot for GPU
- Multiple USB ports, ethernet
- Dell BIOS supports booting Ubuntu
- **And they're dirt cheap** because corporate surplus floods the used market

## RTX 3060 12GB

**The sweet spot GPU for local AI:**
- **12GB VRAM** — this is the key spec. Enough to run:
  - Qwen2.5-14B Q4 quantized (~8-9GB VRAM) ✅
  - Qwen2.5-7B Q4 quantized (~4-5GB VRAM) ✅
  - Llama 3.1 8B Q5 quantized (~6GB VRAM) ✅
- **PCIe x16** — fits in OptiPlex MT
- **170W TDP** — most OptiPlex 260W-500W PSUs can handle it
- **No separate power connector needed** on many variants (just draws from PCIe slot)
- **Used price: $150-200** on eBay right now

**RTX 3060 vs RTX 4060 Ti vs RTX 4070:**

| GPU | VRAM | Used Price | New Price | Performance (local AI) | Worth It? |
|-----|------|-----------|-----------|----------------------|-----------|
| RTX 3060 12GB | 12GB | $150-200 | $280-300 | Good for 7B-14B models | ✅ Best value for AI |
| RTX 4060 Ti 16GB | 16GB | $380-420 | $450 | Better for 14B+ models | ✅ Good but expensive |
| RTX 4070 12GB | 12GB | $350-400 | $550 | Faster but same VRAM | ❌ Not worth the extra cost |
| RTX 3060 Ti 8GB | 8GB | $130-170 | N/A | Faster but only 8GB VRAM | ❌ 8GB too limiting for 14B |
| RTX 3090 24GB | 24GB | $500-600 | N/A | Best for local AI | ⚠️ Power hungry, used only, risky |

**The 3060 12GB is the best value because:**
- VRAM is everything for local AI (more VRAM = bigger models)
- $150-200 used is unbeatable
- 12GB runs 14B models comfortably
- Low power draw (170W) — works in office desktops
- Not a "mining GPU" — these were mid-range GPUs during the mining boom, so less abuse

## Complete Rig: $370-450

| Component | Spec | Price |
|-----------|------|-------|
| Dell OptiPlex 7090 MT | i7-10700, 16GB DDR4, 256GB SSD | $200-250 |
| RTX 3060 12GB | Used, standard height | $150-200 |
| 500GB NVMe (optional upgrade) | If OptiPlex came with 256GB SSD | $25 |
| **Total** | | **$375-475** |

**This is the cheapest viable FamCloud rig.** Same GPU capability as a $920 custom build, just in an office chassis. The customer won't care — it's a box that sits in their closet.

**Form Factor Note:** OptiPlex MT is ~6" wide × 14" tall × 15" deep. Not pretty. Not mini-ITX cute. But it works perfectly for "AI appliance in the closet."

---

## Running Qwen2.5-14B vs 7B

| Model | VRAM Needed | Speed on RTX 3060 | Quality |
|-------|-------------|-------------------|---------|
| Qwen 14B Q4 | ~8-9GB | ~15-20 tokens/sec (good) | Excellent |
| Qwen 14B Q5 | ~10-11GB | ~12-15 tokens/sec (good) | Better |
| Qwen 7B Q4 | ~4-5GB | ~25-35 tokens/sec (fast) | Good but generic |
| Qwen 7B Q5 | ~5-6GB | ~20-30 tokens/sec (fast) | Better |

**14B Q4 is the sweet spot:** Runs comfortably, good speed, noticeably better than 7B for complex reasoning and homework help.

---

## Lifestyle Business Scenarios

### What's a lifestyle business?
Enough income for one person to live on, working part-time, no employees, self-sustaining.

### Scenario A: 30 Customers (Barely Lifestyle)
- Revenue: 30 × $50/month = **$1,500/month recurring**
- Shared number: $2.50 × 30 = $75/month
- **Net: $1,425/month** → ~$17k/year
- Not enough for comfortable living, but nice side income
- Support load: ~60 hours/month (2 hrs/customer) → part-time work
- **Verdict:** Side hustle, not lifestyle

### Scenario B: 50 Customers (Decent Lifestyle)
- Revenue: 50 × $50/month = **$2,500/month recurring**
- Shared number cost: $125/month
- **Net: $2,375/month** → ~$28.5k/year
- Support load: ~100 hours/month → 2-3 hours/day
- **Verdict:** Part-time income. If Charles has another job, this works well.

### Scenario C: 100 Customers (Comfortable Lifestyle)
- Revenue: 100 × $50/month = **$5,000/month recurring**
- Shared number cost: $250/month
- **Net: $4,750/month** → ~$57k/year
- Support load: ~200 hours/month → ~5 hours/day
- **Verdict:** Full-time income for one person. Comfortable but busy.

### Scenario D: 200 Customers (Great Lifestyle)
- Revenue: 200 × $50/month = **$10,000/month recurring**
- Shared number cost: $500/month
- **Net: $9,500/month** → ~$114k/year
- Support load: ~400 hours/month → too much for one person
- **Verdict:** Need to hire help or automate more. Could bring in another person for support.

### Scenario E: 500 Customers (Full Business)
- Revenue: 500 × $50/month = **$25,000/month recurring**
- Shared number cost: $1,250/month
- **Net: $23,750/month** → ~$285k/year
- Support load: ~1,000 hours/month → definitely need employees
- **Verdict:** This is a real business now, not a lifestyle side gig.

---

## Different Pricing Scenarios

### 1. Low Price: $100 Upfront + $30/month
| Metric | Value |
|--------|-------|
| Customer cost year one | $460 |
| Payback (at $400 hardware) | 10 months |
| 100 customers → recurring | $3,000/month |
| Why choose this | Compete with ChatGPT on price |
| Risk | Low revenue, need MORE customers for same income |

### 2. Sweet Spot: $150 Upfront + $50/month (Charles's target)
| Metric | Value |
|--------|-------|
| Customer cost year one | $750 |
| Payback (at $400 hardware) | 5 months |
| 100 customers → recurring | $5,000/month |
| Why choose this | Great value for customer, fast payback for you |
| Risk | Moderate. $50/month is reasonable for a family assistant |

### 3. Premium: $200 Upfront + $75/month
| Metric | Value |
|--------|-------|
| Customer cost year one | $1,100 |
| Payback (at $400 hardware) | 2.5 months |
| 50 customers → recurring | $3,750/month |
| Why choose this | Faster payback, higher margins, premium positioning |
| Risk | May price out budget-conscious families. Need to justify premium |

### 4. Ultra-Premium: $300 Upfront + $99/month
| Metric | Value |
|--------|-------|
| Customer cost year one | $1,488 |
| Payback (at $400 hardware) | 1 month |
| 30 customers → recurring | $2,970/month |
| Why choose this | Luxury positioning, fastest payback, highest per-customer revenue |
| Risk | Few will pay this for a family AI. Very early adopters only |

### 5. Volume Play: $50 Upfront + $20/month
| Metric | Value |
|--------|-------|
| Customer cost year one | $290 |
| Payback (at $400 hardware) | Never profitable (customer pays $290, you spend $400) |
| 200 customers → recurring | $4,000/month |
| Why choose this | Mass market access. Competes directly with ChatGPT Plus |
| Risk | **Hardware cost not covered by upfront.** Need to find another way to absorb hardware cost. NOT VIABLE with current hardware setup. |

### 6. Hardware Lease Model: $0 Upfront + $65/month
| Metric | Value |
|--------|-------|
| Customer cost year one | $780 |
| Payback to you | 8 months (hardware), then pure profit |
| Customer owns hardware | No — it's a lease. They return it if they cancel |
| Monthly revenue (100 customers) | $6,500/month |
| Why choose this | Lowest barrier to entry. No upfront cost. $65/month is reasonable |
| Risk | YOU take on hardware risk. If they cancel after 3 months, you lose $400 |

---

## The Support Question

At $50/month, customers WILL expect support. How much?

### Support Load Estimates (per customer per month):
| Scenario | Setup Calls | Questions | Issues | Total Time |
|----------|-------------|-----------|--------|------------|
| Fully automated, simple onboarding | 0 | 1-2 | 0-1 | 1-2 hours |
| Semi-automated, some hand-holding | 0-1 | 3-4 | 1-2 | 2-4 hours |
| Manual install, complex | 1-2 | 5-6 | 2-3 | 4-6 hours |

### If Support = 3 hours/customer/month at $50/month:
- **Effective hourly rate: $16/hour** — not great
- This means support MUST be automated or reduced to 1 hour/customer/month
- At 1 hour/customer/month: **Effective hourly rate: $50/hour** — excellent

### How to Reduce Support:
1. **Dead simple onboarding** — QR scan + done. No command line.
2. **Self-serve troubleshooting** — built-in diagnostic tools in the web UI
3. **Automated health monitoring** — you see issues before customers do
4. **Pre-configured boxes** — customer just plugs in and follows wizard
5. **FAQ + video walkthroughs** — common issues solved without your time
6. **Charge $80-120/hour for premium support** — "need help beyond setup? book time"

---

## Recommended Path (My Honest Take)

**Pricing: $150 Upfront + $50/month** for the first 50 customers (early adopter pricing)
- $150 covers ~37% of hardware cost at $400/rig
- $50/month is reasonable for a family-wide assistant
- Payback: 5 months
- At 50 customers: $2,500/month recurring
- At 100 customers: $5,000/month recurring

**Hardware: Dell OptiPlex MT + RTX 3060 ($375-475 total)**
- Proven, cheap, enterprise quality
- 12GB VRAM = runs 14B models comfortably
- Ugly but invisible in the closet

**Customer Acquisition:**
- Waitlist at famcloud.ai (start NOW)
- Target tech-friendly families first
- Free 14-day trial
- "Early adopter pricing" creates urgency

**Support:**
- Target 1 hour/customer/month maximum
- Automated onboarding + self-serve troubleshooting
- Premium support: $75/hour (optional, not included in $50)

**Lifestyle Target:**
- 100 customers = $5,000/month recurring ($57k/year)
- This is a comfortable part-time-to-full-time income
- Achievable in 12-18 months with consistent marketing

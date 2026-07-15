# FamCloud — Hardware, Pricing & Margins

## Hardware Options (Cost-Ordered)

### Option A: Use Mac Mini Now (Free)
Already have it. Run Qwen 7B via Ollama (CPU, ~2-3 tok/s). Tests everything except shippable form factor. Do this first.

### Option B: Used Desktop + GPU ($450-550)
Buy used Dell OptiPlex MT (Mini Tower, not SFF): $150-200 on eBay. Add RTX 4060 Ti 16GB ($450). **Total: $450-550**. OptiPlex MT fits standard GPUs + has decent PSU. Sweet spot after validation.

### Option C: Custom Mini-ITX Build ($920-1,120)
- RTX 4060 Ti 16GB ($450) — 16GB VRAM = key spec for 7B+ models
- Ryzen 5 3600/5600X ($100-150)
- 16-32GB DDR4/DDR5 ($40-80)
- Mini-ITX case ($50-100) — NR200 or similar
- 500W PSU or SFX 750W ($50-100)
- 250-500GB NVMe ($25-40)
- Mini-ITX B650 mobo ($200) — WiFi+BT included

Only build this when producing customer units.

## Per-Customer Ongoing Cost
- Shared number: ~$2.50/month (amortized)
- Domain/hosting: ~$0.10/month
- Software/ops: ~$2/month
- **Total: ~$4.60/month per customer** (not counting hardware)

## Pricing Tiers
| Tier | Monthly | Setup | Payback (at $450 hw) |
|------|---------|-------|---------------------|
| Early Adopter | $49 | $299 | 9 months |
| Standard | $79 | $499 | 7 months |
| Premium | $99 | $799 | 6 months |
| Lease | $65/mo, $0 setup | $0 | 9 months |

## Margins
- Year 1: hardware cost eats margins. Pro tier breaks even Year 1.
- **Year 2+: 90%+ margins across all tiers.** Hardware is paid off, customer keeps paying. Hardware is a one-time CAC, not recurring cost.
- At 500 customers mixed tiers: ~$25k/month profit at 91% margin → $304k/year.

## Recommended Validation Path
1. Mac mini → prove software stack works (this week)
2. Used desktop + GPU → prove hardware works (after validation)
3. Custom build → only when scaling to customers

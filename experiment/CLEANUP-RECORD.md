# Repo Cleanup — 2026-07-15

## What Changed

### Moved to `.archive/` (preserved, not deleted):
- **Whisper outputs** (14 UUID files): whisper transcripts from old speech-to-text sessions
- **Google setup scripts**: `.gog_keyring_pass`, `gen_url.py`, `gen_oath_url.py`, `oauth_setup.sh` — one-time OAuth helpers. Kept `oauth/client_secret.json`
- **Stale experiment docs** (archived, not deleted — content absorbed or superseded):
  - `REPO_ARCHITECTURE.md` → folded into CANONICAL.md
  - `VISION.md` → folded into CANONICAL.md
  - `ARCHITECTURE.md` → folded into CANONICAL.md
  - `EXECUTION-PLAN.md` → outdated weekly plan
  - `TRACE_COLLECTOR.md` → content was in TRACES.md already
  - `PROVISIONING-AND-DEPLOYMENT.md` → replaced by COMPLETE-PROVISIONING.md
  - `PROVISIONING-PLAN.md` → replaced by COMPLETE-PROVISIONING.md

### Consolidated into `experiment/business/`:
| New File | Source Files |
|----------|-------------|
| `business/llc-and-tax.md` | BUSINESS-STRUCTURE-AND-GROWTH-PATHS, LLC-SCORP-AND-BOOTSTRAP-2000, LLC-SETUP-CHECKLIST |
| `business/hardware-and-pricing.md` | HARDWARE-AND-PRICING-ANALYSIS, HARDWARE-COST-REDUCTION, HARDWARE-SHOPPING-LIST, MARGIN-ANALYSIS, PRICING-150-50, TIERED-PRICING-AND-PAYBACK |
| `business/go-to-market.md` | CUSTOMER-ACQUISITION, MARKETING-STRATEGY, MOAT-ANALYSIS, VALUE-PROPOSITION, WAITLIST-AND-MARKET, SMB-PIVOT-STRATEGY, NAIL-SALON-STRATEGY, KNOWLEDGE-GRAPH-AND-EXTRACTION |

### Moved to `.archive/experiment-stale/`:
- `BUSINESS-STRUCTURE-AND-GROWTH-PATHS.md`
- `LLC-SCORP-AND-BOOTSTRAP-2000.md`
- `LLC-SETUP-CHECKLIST.md`
- `HARDWARE-AND-PRICING-ANALYSIS.md`
- `HARDWARE-COST-REDUCTION.md`
- `HARDWARE-SHOPPING-LIST.md`
- `MARGIN-ANALYSIS.md`
- `PRICING-150-50.md`
- `TIERED-PRICING-AND-PAYBACK.md`
- `CUSTOMER-ACQUISITION.md`
- `MARKETING-STRATEGY.md`
- `MOAT-ANALYSIS.md`
- `VALUE-PROPOSITION.md`
- `WAITLIST-AND-MARKET.md`
- `SMB-PIVOT-STRATEGY.md`
- `NAIL-SALON-STRATEGY.md`
- `KNOWLEDGE-GRAPH-AND-EXTRACTION.md`

### Old trace formats moved to `.archive/traces-old-format/`:
- `traces/text/` → superseded by `traces/sft/`
- `traces/trajectory/` → superseded by `traces/agentic/`
- `traces/2026-07-02.jsonl` → empty/deleted

### Updated:
- `.gitignore` — added patterns for whisper outputs, runtime state, sensitive files

## What Stayed (all working/current):
- All `experiment/scripts/*` (12 scripts)
- All `experiment/traces/sft/`, `agentic/`, `distill/`
- `CANONICAL.md`, `DATASET_FORMAT.md`, `TRACES.md`, `MODEL-ATTRIBUTION-FIX.md`
- `openclaw-capability-map.md`, `openclaw-fork-gap.md`
- `trace-collector.json`, `trace-dashboard/`
- `vm-test/`, `verticals/`, `artifacts/`
- `provisioning/COMPLETE-PROVISIONING.md`, `AGENT-NATIVE-TOOL-STACK-FINAL.md`
- `memory/` daily notes
- `sites/mom-and-pop-site/index.html`

## Result
~69 files → ~40 files. All knowledge preserved via consolidation. Nothing permanently deleted.

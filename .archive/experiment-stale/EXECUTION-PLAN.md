# FamCloud Execution Plan

## Current State
- ✅ Domain: famcloud.ai (3 years, Namecheap)
- ✅ Vision, architecture, docs, pricing, moat analysis — all documented
- ✅ Codebase: github.com/Chuck1823/george (workspace committed)
- ✅ Bootstrap script drafted (untested)
- ❌ No rig built
- ❌ No model distillation working
- ❌ No company formed
- ❌ No actual product
- ❌ No distillation pipeline tested
- ❌ No hardware
- ❌ No gog OAuth setup
- ❌ No Ubuntu VM simulation

---

## Phase 1: Prove It Works (Weeks 1-4)

### Priority 1: Build the Rig + Prove the Stack
**Why first:** Without a working rig, nothing else matters. The entire product is "AI on a box in your house." We need to prove that box works.

1. **Buy hardware** (use the shopping list in HARDWARE-SHOPPING-LIST.md)
   - Mini-ITX case: Cooler Master NR200 (~$100)
   - GPU: RTX 4060 Ti 16GB (~$450)
   - CPU: AMD Ryzen 5 5600X (~$150)
   - RAM: 32GB DDR5 (~$80)
   - Storage: 500GB NVMe (~$40)
   - PSU: SFX 750W (~$100)
   - **Total: ~$920**

2. **Assemble the rig** (30-45 minutes)

3. **Ubuntu VM first** (test bootstrap on VM before real hardware)
   - Set up Ubuntu VM on your Mac mini (VirtualBox or UTM)
   - Run `bootstrap-gpu-rig.sh` in the VM
   - Verify OpenClaw installs, configures, runs
   - Test model download + inference (CPU mode in VM, GPU on real hardware)

4. **Run bootstrap on real hardware**
   - Install Ubuntu
   - Run `bootstrap-gpu-rig.sh`
   - Verify GPU inference works (Ollama/vLLM loads model, runs queries)
   - Verify OpenClaw gateway starts

5. **Test channels**
   - WhatsApp: QR pair, send/receive messages
   - Telegram: BotFather token, send/receive
   - Discord: Bot token, send/receive
   - Verify all channels work end-to-end

6. **Test self-serve onboarding UI**
   - famcloud.local:18789/setup
   - Walk through the wizard
   - Fix any broken flows

**Done when:** You can plug in the rig, open the browser, follow the wizard, and chat with the agent on WhatsApp + Telegram.

---

### Priority 2: Test Distillation Pipeline
**Parallel with rig build:** While waiting for hardware, test the distillation loop on your Mac mini.

1. **Export traces** — run `export-all.py` on your existing OpenClaw sessions
2. **Grade/filter** — run `teacher-grade.py` on the traces
3. **Distill** — use the distillation script to create a smaller model from the traces
4. **Test** — run the distilled model, compare quality to base model
5. **Document** — what works, what doesn't, what needs improvement

**Done when:** You can distill a model from traces and verify it's better than the base model on specific tasks.

---

### Priority 3: Complete gog OAuth Setup
**Dependency:** Need this for email integration in FamCloud.

1. Run `gog auth add georgia.ai.assistant@gmail.com --services gmail,calendar,drive,contacts,docs,sheets`
2. Verify `GOG_KEYRING_BACKEND=file` is set
3. Verify `~/.openclaw/workspace/google/oauth/client_secret.json` exists
4. Test: `gog gmail list` or `gog calendar list`

**Done when:** gog can access Gmail, Calendar, Drive, and Contacts via CLI.

---

### Priority 4: Form LLC
**Parallel with hardware:** Do the legal stuff while waiting for parts to ship.

1. File LLC with your state (30 minutes, ~$50-200)
2. Get EIN from IRS (10 minutes, free)
3. Open business bank account (Mercury, free, or local bank)
4. Write operating agreement (30 minutes, template available)

**Done when:** LLC exists, EIN obtained, business bank account open.

---

## Phase 2: First Customer (Weeks 5-8)

1. **Find 1-2 beta customers** (friends/family)
2. **Install for them** (manual — go to their house, set up the rig)
3. **Onboard them** through the self-serve wizard
4. **Monitor** for 2-4 weeks
5. **Fix everything that breaks**
6. **Document** setup process, common issues, fixes

**Done when:** 2 households are using FamCloud daily with no major issues.

---

## Phase 3: Scale (Weeks 9+)

1. **Launch website** (famcloud.ai landing page)
2. **Start taking orders** (pre-configured boxes shipped to customers)
3. **Self-serve onboarding** (no manual install)
4. **Model update pipeline** (nightly distilled model updates pushed to all rigs)
5. **Support infrastructure** (remote monitoring, health dashboard, ticketing)

---

## What to Do RIGHT NOW

This week, focus on three things:

### 1. Order the Hardware
**Today:** Buy all the parts from the shopping list. Total ~$920.
- Get everything shipping ASAP (Amazon Prime for 2-day delivery)
- Or build it yourself from parts you already have (Mac mini + external GPU?)

### 2. Set Up Ubuntu VM (Test Bootstrap)
**This weekend:** Create an Ubuntu VM on your Mac mini.
- Install VirtualBox or UTM
- Download Ubuntu 24.04 ISO
- Create VM, run bootstrap script
- Test OpenClaw + model inference (CPU mode)

### 3. Complete gog OAuth
**When:** 30 minutes anytime this week
- Run the auth command
- Verify all services work

### 4. Test Distillation Pipeline
**When:** 2-3 hours this week
- Run export-all.py on your sessions
- Grade + distill
- Test quality

---

## The Hard Truth

We have docs, we don't have a product. The difference between docs and a product is a working rig + working onboarding + working distillation.

Everything I've written so far is theory. The only way to make it real is to build the thing and see if it works.

So the answer to "what's next?" is:

1. **Order hardware** (today)
2. **Test bootstrap in VM** (this weekend)
3. **Build the rig** (when parts arrive)
4. **Prove it works** (when rig is built)
5. **First customer** (when proven)

Nothing else matters until we can plug in a box, open a browser, and chat with the agent.

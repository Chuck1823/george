# FamCloud Waitlist & Market Research

## Charles's Concerns (2026-07-11)
1. Does Qwen 7B need fine-tuning/distillation BEFORE VM test?
2. Should we create a waitlist website to gauge interest?
3. Will this actually sell? Parallels from successful companies?

---

## Qwen 7B for VM Test

**No, we don't need fine-tuning/distillation before the VM test.**

The VM test validates:
- Bootstrap script works on fresh Ubuntu
- Ollama installs and serves models
- OpenClaw gateway starts
- Channel plugins connect
- End-to-end message flow works

Qwen 7B as a base model is FINE for testing the plumbing. The distillation loop is a SEPARATE concern from "can we get the box working."

**What we're testing:** Does the software stack work? Not "is the model the best possible."

**When we'll need distillation:** After we know the box works, and before we ship to customers (because we need the model to be good enough to justify $100/month).

---

## Waitlist Website

**Yes, we should do this. It's low effort, high signal.**

### What to build:
Simple landing page at famcloud.ai:
- Hero: "Your family's personal AI assistant. Lives in your home. Works everywhere you text."
- Email signup
- "Get early access" CTA
- No pricing yet, no tech details

### Why:
- If 100+ people sign up in a week → real interest
- If nobody signs up → we need to rethink the value prop
- Waitlist signals to potential investors/beta customers that we're real
- Gives us actual people to talk to about what they want

### Timeline:
- 1-2 hours to build a simple page (Next.js + Vercel, or even Carrd)
- Launch on Reddit, Twitter, family/friends
- Run for 2-4 weeks before buying hardware

---

## Will It Sell? Parallels from Successful Companies

### Companies that sold "appliance AI" or "home-first" products:

**1. Ubiquiti / UniFi — Personal Networking Appliances**
- Sold: A box that runs in your house, gives you network control
- Price: $100-500 for hardware, free software
- Why it worked: "Your network, your control, no cloud subscription"
- **Parallel to FamCloud:** Sell a box, local inference, privacy, no cloud lock-in

**2. Tablo TV — Local DVR**
- Sold: A box that records OTA TV, streams to your devices
- Price: $140-180 hardware + optional $30/year guide data
- Why it worked: "Record TV without a cable subscription, watch anywhere in your house"
- **Parallel:** Box in your home, does a specific thing well, no cloud dependency

**3. Nextcloud — Self-Hosted Cloud Storage**
- Sold: Software to run your own Google Drive/Dropbox at home
- Price: Free (open source), paid enterprise support
- Why it worked: "Your data, on your hardware, no big tech"
- **Parallel:** Local-first, privacy-respecting, self-hosted

**4. Jellyfin / Plex — Personal Media Servers**
- Sold: Box that streams your media to every device
- Price: Free (Jellyfin) or $5/month (Plex Pass), hardware separate
- Why it worked: "Your media, your server, no subscription to Netflix"
- **Parallel:** Home appliance that does one thing (media for Plex, AI for FamCloud)

**5. Eufy / Local Security Cameras**
- Sold: Security cameras that store footage locally
- Price: $200-500 for hardware
- Why it worked: "No monthly fees, your video stays local"
- **Parallel:** Local storage = privacy = no subscription anxiety

**6. Apple HomePod / Echo — Home Assistants**
- Sold: Voice assistant in every room
- Price: $100-350 hardware
- Why it worked: "Hey Siri/Alexa, just works"
- **Caveat:** These are cloud-dependent, locked to one ecosystem (Apple or Amazon)
- **FamCloud's advantage:** We're cross-platform AND local-first

**7. Raspberry Pi — Home Server Hobby**
- Sold: Cheap computer for home automation, media, learning
- Price: $35-80
- Why it worked: "Run whatever you want, in your house, cheap"
- **FamCloud:** More polished, less DIY, but same "box in your house" philosophy

---

## The Pattern in All These Companies:

**They sold "appliance + local control + no cloud dependency"**

And they all succeeded because they offered something cloud services couldn't:
- Ubiquiti: "Your network isn't someone else's cloud"
- Tablo: "Your recordings aren't locked to a cable box"
- Jellyfin: "Your media isn't on Netflix's servers"
- Eufy: "Your video isn't in Amazon's cloud"

**FamCloud:** "Your AI assistant isn't on OpenAI's servers, doesn't train on your data, works on every platform"

---

## Risk Assessment

### Signs this WILL sell:
- People buy home appliances that do one thing well (Plex, Eufy, Tablo)
- People already pay $100-300/month for personal assistants / services
- AI anxiety is growing (privacy concerns, data usage, always-on listening)
- ChatGPT is great but people want something personalized
- Cross-platform messaging is what families actually use

### Signs this might NOT sell:
- $100/month is expensive for an unproven product
- People SAY they want privacy but pay $0 for it (GPT is free)
- Setup might be too technical for non-tech families (even with simplified wizard)
- Model quality might not justify price (7B vs 70B+ cloud models)
- Big players could copy the concept (cloud-based family AI)

### Mitigations:
- Start with $49-79/month for early adopters (not $99-149)
- Offer free trial (14 days)
- Make setup dead simple (QR code → done)
- Build the best 7B model we can (distillation loop)
- Move fast before big players copy the concept

---

## Bottom Line on "Will It Sell?"

The parallels suggest: **Yes, it could sell.** Home appliances that do one thing well, local-first, no-cloud-dependency, have a proven track record.

But the price point is the risk: $100/month is much more than Tablo ($30/year) or Plex ($60/year) or Jellyfin (free).

My recommendation: **Launch at $49/month for the first 50 customers (early adopter pricing). Prove the product works, then raise to $99/month.**

The waitlist will tell us if people actually want this before we spend $920 on hardware.

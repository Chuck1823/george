# FamCloud — Complete Channel Provisioning & Self-Serve Onboarding

## Approach: Piggyback on OpenClaw's Native Channel Support

OpenClaw already supports all the channels we need. We don't build bridges from scratch — we configure what exists and provide a clean self-serve UI for customer setup.

**What we're shipping in every box:**
- Ubuntu Linux with OpenClaw pre-installed
- All channel plugins pre-installed (only need API keys/tokens from customer)
- Local web UI at `famcloud.local:18789` for onboarding
- One-liner: go to URL → connect channels → start chatting

---

## Channel-by-Channel: What OpenClaw Supports & What We Need

### 1. WhatsApp — Production-Ready via Baileys
**OpenClaw support:** Native plugin (`@openclaw/whatsapp`)
**Setup:** QR code scan (WhatsApp Web link)
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/whatsapp`
2. QR code displayed on screen
3. Customer scans with their phone's WhatsApp
4. Plugin connects, session persisted
5. Done — agent is now on that WhatsApp account

**Cost:** FREE (uses customer's personal WhatsApp)
**Caveats:** Against WhatsApp ToS (everyone does it). Can get banned if detected.
**Business API alternative (Phase 2):** Via Twilio + Meta Business Account — $1-5/month.

### 2. Telegram — Production-Ready via grammY
**OpenClaw support:** Native plugin
**Setup:** Bot token from @BotFather
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/telegram`
2. Instructions: "Open Telegram → search @BotFather → send /newbot → follow prompts"
3. Customer pastes the bot token into the form
4. Plugin connects, bot goes live
5. Customer messages the bot on Telegram

**Cost:** FREE (Telegram bots are always free)
**Caveats:** None. Telegram is the easiest, cheapest, most reliable channel.

### 3. iMessage — Native imsg CLI
**OpenClaw support:** `imsg` CLI (stdio JSON-RPC)
**Setup:** Requires macOS host (customer's Mac)
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/imessage`
2. Instructions: "On your Mac, run: `brew install steipete/tap/imsg && imsg launch`"
3. Customer signs into Messages.app on their Mac
4. OpenClaw relays via SSH or local network connection
5. Agent can now send/receive iMessages

**Cost:** FREE (uses customer's Apple ID + Mac)
**Caveats:** ONLY works on macOS. Customer needs a Mac mini or MacBook running in their house.
**Our workaround:** SSH from the FamCloud rig to the customer's Mac (imsg SSH relay).

### 4. Signal — Via signal-cli
**OpenClaw support:** Native plugin (`@openclaw/signal`)
**Setup:** Register phone number with Signal, solve captcha
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/signal`
2. We provision a Signal number OR they bring their own
3. Customer solves captcha in browser
4. signal-cli registers, connects
5. Agent on Signal

**Cost:** FREE (Signal is free)
**Caveats:** Registration requires a phone number that can receive SMS.

### 5. SMS (Twilio) — Via Webhook
**OpenClaw support:** Native plugin (`@openclaw/sms`)
**Setup:** Twilio account + phone number
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/sms`
2. Instructions: "Create Twilio account at twilio.com → buy a phone number"
3. Customer pastes Account SID, Auth Token, and phone number
4. Twilio webhook configured to FamCloud's public URL
5. Agent on SMS

**Cost:** $1-2/month (Twilio number) + ~$0.0079 per message
**Caveats:** Requires public HTTPS URL (Tailscale or similar for inbound webhooks).

### 6. Discord — Via Developer Portal Bot
**OpenClaw support:** Native plugin
**Setup:** Create Discord App + Bot
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/discord`
2. Link to Discord Developer Portal: "Create New Application → Bot → Copy Token"
3. Customer pastes bot token
4. Link to invite: "Add bot to your Discord server"
5. Agent on Discord

**Cost:** FREE (Discord bot accounts are free)
**Caveats:** Customer needs a Discord server.

### 7. Slack — Via Slack API App
**OpenClaw support:** Native plugin
**Setup:** Create Slack App
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/slack`
2. Link to Slack API: "Create New App → From Scratch"
3. Customer authorizes FamCloud bot in their workspace
4. Agent on Slack

**Cost:** FREE (Slack app is free for small workspaces)
**Caveats:** Slack free tier has message history limits.

### 8. Email (Gmail/Google) — Via gog plugin
**OpenClaw support:** `gog` plugin (Google Workspace CLI)
**Setup:** Google OAuth
**Self-serve flow:**
1. Customer opens `famcloud.local/setup/email`
2. Google OAuth popup: "Connect your Gmail account"
3. Customer grants access to Gmail, Calendar, Drive, Contacts
4. Agent can read/send emails on their behalf

**Cost:** FREE (personal Gmail is free)
**Alternative:** Google Workspace ($6/month) for custom domain email.

---

## What We Pre-Install in Every Box

### OpenClaw + All Channel Plugins:
```bash
# In bootstrap-gpu-rig.sh or pre-image:
npm install -g openclaw
openclaw plugins install @openclaw/whatsapp
openclaw plugins install @openclaw/signal
openclaw plugins install @openclaw/sms
openclaw plugins install @openclaw/discord
openclaw plugins install @openclaw/slack
# gog is a separate plugin (Google Workspace):
openclaw plugins install @openclaw/gog
# Telegram comes built-in (grammY)
# iMessage uses imsg CLI (needs macOS host — customer's Mac)
```

### What's Ready Out of the Box:
- ✅ Telegram (just needs a BotFather token)
- ✅ WhatsApp (just needs QR scan)
- ✅ Discord (just needs a Developer Portal bot token)
- ✅ Slack (just needs a Slack App auth)
- ✅ Signal (just needs registration + captcha)
- ✅ SMS (just needs Twilio credentials)
- ✅ Email (just needs Google OAuth)
- ⚠️ iMessage (needs customer's Mac on network + imsg CLI)

### What We DON'T Pre-Install (Customer's Own):
- Google OAuth tokens (customer authorizes in browser)
- Discord bot token (customer creates in Developer Portal)
- Slack app auth (customer creates in Slack API)
- Twilio credentials (customer creates account)
- WhatsApp session (customer scans QR)
- Signal number (customer registers or we provision)

---

## Self-Serve Onboarding Flow (Pre-Configured Box)

### Step 1: Unbox & Connect
```
1. Plug in ethernet cable
2. Connect power
3. Box boots automatically (Ubuntu + OpenClaw pre-installed)
```

### Step 2: Go to famcloud.local
```
Browser → http://famcloud.local:18789/setup
(Local network discovery via mDNS/Bonjour)
If mDNS fails: http://192.168.1.XXX:18789/setup
```

### Step 3: Create Household Account
```
Name: [Your full name]
Household name: [The Smith Family]
Admin email: [charles@example.com]
Phone: [+1 555-123-4567]
Password: [••••••••]
```

### Step 4: Choose Channels (Pick What You Want)
```
☑️ Telegram bot    — FREE — Setup: Create token in @BotFather
☑️ WhatsApp        — FREE — Setup: Scan QR code with your phone
☑️ Discord bot     — FREE — Setup: Create bot on Discord Developer Portal
☑️ Slack bot       — FREE — Setup: Create app on Slack API
☐ SMS (Twilio)     — $2/mo — Setup: Create Twilio account, buy number
☐ Signal           — FREE — Setup: Register phone number, solve captcha
☐ iMessage         — FREE — Setup: Have a Mac on your network + sign in
☐ Gmail/Google     — FREE — Setup: OAuth → grant access to your Gmail
```

### Step 5: Connect Each Channel
**Telegram:**
```
1. Open Telegram → search @BotFather
2. Send: /newbot
3. Follow prompts → get bot token (e.g., 123456:ABC-DEF1234ghIkl-zyx57W2v1u1234567)
4. Paste token → click Connect → ✅ Telegram connected
```

**WhatsApp:**
```
1. Click "Show QR Code"
2. Open WhatsApp on your phone → Settings → Linked Devices → Link a Device
3. Scan the QR code on screen
4. ✅ WhatsApp connected
```

**Discord:**
```
1. Click "Create Discord Bot" → opens Discord Developer Portal
2. Create New Application → Bot → Copy Token
3. Paste token → click Connect
4. Click "Add to Server" → invite to your Discord server
5. ✅ Discord connected
```

**Slack:**
```
1. Click "Create Slack App" → opens Slack API
2. Create New App → From Scratch → Name: "FamCloud Bot"
3. Choose workspace → Add features & functionality → Bots
4. Copy OAuth token → paste → click Connect
5. ✅ Slack connected
```

**Gmail/Google:**
```
1. Click "Connect Google Account" → Google OAuth popup
2. Sign in → Grant access (Gmail, Calendar, Drive, Contacts)
3. ✅ Email connected
```

**iMessage (if customer has Mac):**
```
1. On your Mac, open Terminal
2. Run: brew install steipete/tap/imsg && imsg launch
3. Sign into Messages.app with your Apple ID
4. FamCloud rig auto-detects Mac on network → connects
5. ✅ iMessage connected
```

### Step 6: Setup Family Members
```
[+] Add household member
Name: [Alice]
Age: [8]
Relationship: [daughter]
Channels: [iMessage, WhatsApp]
Parental controls: ON
Time window: 7AM-9PM
Approval required for: Purchases, sharing personal info
```

### Step 7: First Conversation
```
Agent: "Hi! I'm FamCloud. I'm set up for the Johnson family 🏠
I can help with:
- Messages (WhatsApp, Telegram, iMessage)
- Email management
- Calendar
- Homework help for Alice
- Family scheduling
- General questions (your data stays local)

What would you like to ask?"
```

### Step 8: Done
```
✅ Rig runs 24/7
✅ Agent responds on all connected channels
✅ Memory system active (searchable)
✅ Model updates scheduled nightly
✅ Health monitoring active
✅ Remote support SSH enabled (with your permission)
```

---

## What FamCloud Provides (Shared Infrastructure)

### Things We Run (One Instance, Many Households):

1. **Discord Umbrella Bot**
   - One Discord Application → "FamCloud"
   - Customers join → we detect household → route to their rig
   - Cost: FREE
   - Scale: unlimited households

2. **Slack Umbrella App**
   - One Slack App → "FamCloud Bot"
   - Install to each household's workspace
   - Cost: FREE
   - Scale: unlimited workspaces

3. **famcloud.ai Domain**
   - Subdomains: alice@famcloud.ai, bob@famcloud.ai
   - Cloudflare Email Routing (free) → forwards to their real email
   - Cost: $15/year domain + $0 routing
   - Scale: unlimited aliases

4. **OpenClaw Gateway Update Server**
   - Push model updates to all rigs
   - Push config changes
   - Push feature updates
   - Cost: ~$10/month (VPS for update server)
   - Scale: unlimited rigs

5. **Remote Support Platform**
   - SSH into customer rigs (with permission)
   - Health dashboard (all rigs reporting status)
   - Automated ticket creation
   - Cost: ~$5/month (SSH bastion)
   - Scale: ~100 rigs per bastion

### Things Each Household Needs (Per-Household):

1. **WhatsApp Session** (customer's personal account) — FREE
2. **Telegram Bot Token** (one per household) — FREE
3. **Twilio Number** (optional, for SMS) — $2/month
4. **iMessage Bridge** (if customer has Mac) — FREE
5. **Google OAuth Token** (customer's Gmail) — FREE
6. **Signal Registration** (optional phone number) — FREE

---

## Pricing (Revised)

### Setup Fee (One-Time): $500-800
- Covers hardware assembly ($1,120 cost → you cover $320-620)
- Pre-configured Ubuntu + OpenClaw + all plugins
- Shipped to customer's house
- Customer does self-serve onboarding (web UI)

### Monthly Plans:

**FamCloud — $79/month**
- 1 channel (WhatsApp OR Telegram OR Discord OR Slack)
- Basic memory/search (30 days)
- 1 household member
- Self-serve support

**FamCloud Family — $129/month**
- 3 channels (any combination)
- Extended memory/search (6 months + semantic search)
- Up to 4 household members
- Per-person profiles with shared/private memory
- Basic parental controls (age filtering, time windows)
- Email integration (Gmail OAuth)
- Priority support (24h response)

**FamCloud Premium — $199/month**
- **All channels** (WhatsApp, Telegram, Discord, Slack, Signal, SMS, iMessage if Mac)
- Unlimited memory retention + advanced search
- Unlimited household members
- Advanced parental controls (approval workflows, spending locks)
- Custom email aliases (name@famcloud.ai)
- Voice calls (via Twilio)
- Priority support (4h response)
- Monthly model updates from distillation pipeline

### Payback Analysis:

| Metric | $79/mo | $129/mo | $199/mo |
|--------|--------|---------|---------|
| Setup fee | $500 | $800 | $800 |
| Monthly cost to you | ~$15 | ~$20 | ~$25 |
| Your monthly profit | $64 | $109 | $174 |
| Setup fee covers hardware | $500 | $800 | $800 |
| Remaining hardware cost | $620 | $320 | $320 |
| Payback (months) | 9.7 | 3.0 | 1.8 |
| Year 1 revenue | $1,448 | $2,348 | $3,188 |
| Year 2+ profit/year | $960 | $1,548 | $2,340 |

---

## What to Build (Self-Serve Web UI)

The local web UI at `famcloud.local:18789/setup` needs:

1. **Channel wizard pages:**
   - Telegram: Instructions + token input
   - WhatsApp: QR code display + status
   - Discord: Link to Developer Portal + token input
   - Slack: Link to Slack API + OAuth
   - Signal: Captcha form + phone number input
   - SMS: Twilio credential input
   - iMessage: Instructions for Mac + status check
   - Gmail: Google OAuth popup

2. **Household management:**
   - Add/edit family members
   - Set ages, relationships
   - Configure parental controls per member
   - Privacy settings (shared vs private memory)

3. **Status dashboard:**
   - Rig health (GPU, CPU, memory, disk)
   - Channel connectivity
   - Model version
   - Memory usage
   - Support ticket status

4. **Settings:**
   - Model preferences
   - Notification settings
   - Support access toggle (on/off for remote support)

---

## Summary: What We Do vs What Customer Does

### We Provide (in the box):
- ✅ Pre-configured Ubuntu + OpenClaw
- ✅ All channel plugins pre-installed
- ✅ Hardware assembled and tested
- ✅ Model weights pre-downloaded
- ✅ Local web UI for onboarding
- ✅ Remote support infrastructure
- ✅ Model update pipeline
- ✅ Health monitoring

### Customer Does:
- ✅ Plug in ethernet + power
- ✅ Open famcloud.local in browser
- ✅ Create account + household
- ✅ Connect their own channels (tokens, QR, OAuth)
- ✅ Setup family members

### What's Shared (We Run Once, Serves Many):
- Discord umbrella bot
- Slack umbrella app
- famcloud.ai domain + email routing
- Model update server
- Health monitoring server
- SSH bastion for remote support

### What's Per-Household (Unique):
- WhatsApp session
- Telegram bot token
- Twilio number (if enabled)
- iMessage Mac (if enabled)
- Google OAuth token
- Customer's own rig hardware

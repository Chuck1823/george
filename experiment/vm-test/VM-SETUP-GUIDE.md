# FamCloud VM Test — Setup & Validation

## Purpose
Test the FamCloud bootstrap script and OpenClaw setup on a LOCAL Ubuntu VM before buying hardware. This validates the entire software stack without GPU.

## VM Specs
- **CPU:** 4 cores (i3-8100B on Mac mini)
- **RAM:** 8GB (of 16GB total)
- **Disk:** 40GB (of 74GB free)
- **GPU:** None (CPU inference only — slower but functional)
- **Model:** Qwen2.5-7B Q4_K_M quantized (fits in 8GB RAM)

## Setup Script: `setup-vm.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# FamCloud VM Setup — run on Mac mini

echo "=== FamCloud VM Setup ==="

# 1. Install VirtualBox (interactive — sudo required)
echo "[1/6] Installing VirtualBox..."
if command -v VBoxManage &>/dev/null; then
    echo "  VirtualBox already installed."
else
    echo "  Installing VirtualBox via Homebrew..."
    echo "  ⚠️ This requires sudo approval. Enter your password when prompted."
    brew install --cask virtualbox || {
        echo "  ❌ VirtualBox install failed. Try manual install from virtualbox.org"
        exit 1
    }
fi

# 2. Download Ubuntu Server ISO
echo "[2/6] Downloading Ubuntu Server 24.04 LTS..."
ISO_URL="https://releases.ubuntu.com/24.04/ubuntu-24.04.1-live-server-amd64.iso"
ISO_PATH="$HOME/Downloads/ubuntu-24.04.1-live-server-amd64.iso"

if [ -f "$ISO_PATH" ]; then
    echo "  ISO already downloaded: $ISO_PATH"
else
    echo "  Downloading Ubuntu Server ISO (~1.6GB)..."
    curl -L "$ISO_URL" -o "$ISO_PATH" || {
        echo "  ❌ Download failed. Manual download from: $ISO_URL"
        exit 1
    }
    echo "  Download complete."
fi

# 3. Create VM
VM_NAME="FamCloud-Test"
echo "[3/6] Creating VM: $VM_NAME..."

if VBoxManage list vms 2>/dev/null | grep -q "$VM_NAME"; then
    echo "  VM already exists. Skipping creation."
else
    # Create VM
    VBoxManage createvm --name "$VM_NAME" --register --basefolder "$HOME/VirtualBox VMs"
    
    # Configure VM
    VBoxManage modifyvm "$VM_NAME" --memory 8192 --cpus 4 --ostype Ubuntu_64
    VBoxManage modifyvm "$VM_NAME" --ioapic on
    VBoxManage modifyvm "$VM_NAME" --nic1 nat
    VBoxManage modifyvm "$VM_NAME" --natpf1 "ssh,tcp,,2222,,22"
    VBoxManage modifyvm "$VM_NAME" --natpf1 "gateway,tcp,,18789,,18789"
    
    # Storage
    VBoxManage storagectl "$VM_NAME" --name "SATA" --add sata --controller IntelAhci
    VBoxManage storagectl "$VM_NAME" --name "IDE" --add ide
    
    # Create virtual disk (40GB)
    DISK_PATH="$HOME/VirtualBox VMs/$VM_NAME/ubuntu.vdi"
    VBoxManage createhd --filename "$DISK_PATH" --size 40960 --format VDI
    VBoxManage storageattach "$VM_NAME" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "$DISK_PATH"
    
    # Attach ISO
    VBoxManage storageattach "$VM_NAME" --storagectl "IDE" --port 0 --device 0 --type dvddrive --medium "$ISO_PATH"
    
    # Boot order: DVD first, then disk
    VBoxManage modifyvm "$VM_NAME" --boot1 dvd --boot2 disk --boot3 none --boot4 none
    
    echo "  VM created: $VM_NAME"
fi

# 4. Instructions for manual Ubuntu install
echo ""
echo "============================================"
echo "[4/6] Manual step: Install Ubuntu Server"
echo "============================================"
echo ""
echo "1. Start the VM:"
echo "   VBoxManage startvm '$VM_NAME' --type gui"
echo ""
echo "2. Follow Ubuntu Server installer:"
echo "   - Choose English, default keyboard"
echo "   - Select 'Ubuntu Server (minimized)'"
echo "   - Set hostname: famcloud-vm"
echo "   - Create user: famcloud / password: famcloud"
echo "   - DO NOT install SSH server (we'll use NAT port forwarding)"
echo "   - Wait for install to complete, then power off"
echo ""
echo "3. After install, detach ISO and start again:"
echo "   VBoxManage storageattach '$VM_NAME' --storagectl 'IDE' --port 0 --device 0 --type dvddrive --medium none"
echo "   VBoxManage startvm '$VM_NAME' --type headless"
echo ""
echo "4. SSH into VM:"
echo "   ssh -p 2222 famcloud@localhost"
echo ""
echo "============================================"
echo "After VM is running, continue with steps 5-6"
echo "============================================"

# 5. Bootstrap script for the VM
echo ""
echo "[5/6] Bootstrap script for VM (run AFTER Ubuntu is installed)"
echo ""
echo "SSH into VM: ssh -p 2222 famcloud@localhost"
echo "Then run:"
echo ""
echo "  curl -sL https://raw.githubusercontent.com/Chuck1823/george/main/experiment/scripts/bootstrap-gpu-rig.sh | bash"
echo ""

# 6. Verification checklist
echo "[6/6] Verification checklist (run after bootstrap):"
echo ""
echo "  ✅ ollama list — shows qwen2.5:7b"
echo "  ✅ ollama run qwen2.5:7b 'Say hello' — responds correctly"
echo "  ✅ openclaw status — gateway running"
echo "  ✅ curl http://localhost:18789 — OpenClaw UI loads"
echo "  ✅ Test WhatsApp QR pair"
echo "  ✅ Test Telegram bot"
echo ""
echo "============================================"
echo "Setup scaffolding complete!"
echo "============================================"
```

## Verification Checklist (After VM Running)

| Test | Command | Expected |
|------|---------|----------|
| Model loads | `ollama list` | `qwen2.5:7b` listed |
| Inference works | `ollama run qwen2.5:7b 'Say hello'` | Response in <30s |
| OpenClaw running | `openclaw status` | Gateway: online |
| UI accessible | `curl http://localhost:18789` | HTML response |
| Port forwarding | `curl http://localhost:18789` (from Mac mini) | Same HTML response |
| NVIDIA check | `nvidia-smi` | ❌ Expected to fail (CPU only) |
| SSH access | `ssh -p 2222 famcloud@localhost` | Connected |

## Port Forwarding Setup

The VM uses NAT with port forwarding:
- `localhost:2222` → VM port 22 (SSH)
- `localhost:18789` → VM port 18789 (OpenClaw Gateway)
- `localhost:18790` → VM port 18790 (FamCloud Setup UI)

## What This Validates

- ✅ Bootstrap script works on fresh Ubuntu
- ✅ OpenClaw installs and configures correctly
- ✅ Model inference works (CPU mode, slower but functional)
- ✅ Channel plugins install (WhatsApp, Telegram, etc.)
- ✅ Gateway starts and serves UI
- ✅ Port forwarding works for local access
- ❌ GPU inference (not applicable — VM has no GPU)

## What This DOES NOT Validate

- ❌ GPU performance and model speed
- ❌ Physical hardware assembly
- ❌ Customer onboarding experience
- ❌ Self-serve wizard (we're testing the bootstrap, not the UI)
- ❌ Scale/load testing

## Next Steps After Successful VM Test

1. **Order hardware** — buy parts from shopping list
2. **Assemble rig** — 30-45 min build
3. **Run bootstrap on real hardware** — GPU inference, full validation
4. **Test channels end-to-end** — WhatsApp + Telegram
5. **First customer** — install for friend/family

#!/usr/bin/env bash
set -euo pipefail

# FamCloud VM Setup — run on Mac mini
# Creates VirtualBox VM with Ubuntu Server, pre-configured for FamCloud testing

echo "=== FamCloud VM Setup ==="
echo ""

# 1. Install VirtualBox (interactive — sudo required)
echo "[1/5] Checking VirtualBox..."
if command -v VBoxManage &>/dev/null; then
    echo "   ✅ VirtualBox already installed."
else
    echo "   ⚠️ VirtualBox not found. Installing via Homebrew..."
    echo "   ⚠️ This requires sudo approval. Enter your password when prompted."
    echo ""
    brew install --cask virtualbox || {
        echo "   ❌ Brew install failed or needs approval."
        echo "   Try: brew install --cask virtualbox"
        echo "   Or: Download from virtualbox.org"
        exit 1
    }
    echo "   ✅ VirtualBox installed."
fi

# 2. Download Ubuntu Server ISO
echo ""
echo "[2/5] Checking Ubuntu ISO..."
ISO_URL="https://releases.ubuntu.com/24.04/ubuntu-24.04.1-live-server-amd64.iso"
ISO_PATH="$HOME/Downloads/ubuntu-24.04-server.iso"

if [ -f "$ISO_PATH" ]; then
    echo "   ✅ ISO already downloaded."
else
    echo "   Downloading Ubuntu Server 24.04 LTS (~2.1GB)..."
    curl -L "$ISO_URL" -o "$ISO_PATH" || {
        echo "   ❌ Download failed. Manual download from: $ISO_URL"
        exit 1
    }
    echo "   ✅ Download complete."
fi

# 3. Create VM
VM_NAME="FamCloud-Test"
echo ""
echo "[3/5] Setting up VM: $VM_NAME..."

if VBoxManage list vms 2>/dev/null | grep -q "$VM_NAME"; then
    echo "   ⏭️  VM already exists. Skipping creation."
else
    VM_DIR="$HOME/VirtualBox VMs"
    mkdir -p "$VM_DIR"
    
    # Create VM
    VBoxManage createvm --name "$VM_NAME" --register --basefolder "$VM_DIR"
    
    # Configure
    VBoxManage modifyvm "$VM_NAME" --memory 8192 --cpus 4 --ostype Ubuntu_64
    VBoxManage modifyvm "$VM_NAME" --ioapic on
    VBoxManage modifyvm "$VM_NAME" --nic1 nat
    VBoxManage modifyvm "$VM_NAME" --natpf1 "ssh,tcp,,2222,,22"
    VBoxManage modifyvm "$VM_NAME" --natpf1 "gateway,tcp,,18789,,18789"
    
    # Storage
    VBoxManage storagectl "$VM_NAME" --name "SATA" --add sata --controller IntelAhci
    VBoxManage storagectl "$VM_NAME" --name "IDE" --add ide
    
    # Virtual disk
    VBoxManage createhd --filename "$VM_DIR/$VM_NAME/ubuntu.vdi" --size 40960 --format VDI
    VBoxManage storageattach "$VM_NAME" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "$VM_DIR/$VM_NAME/ubuntu.vdi"
    
    # Attach ISO
    VBoxManage storageattach "$VM_NAME" --storagectl "IDE" --port 0 --device 0 --type dvddrive --medium "$ISO_PATH"
    
    # Boot order
    VBoxManage modifyvm "$VM_NAME" --boot1 dvd --boot2 disk --boot3 none --boot4 none
    
    echo "   ✅ VM created."
fi

# 4. Print manual instructions
echo ""
echo "============================================"
echo "[4/5] Manual step: Install Ubuntu"
echo "============================================"
echo ""
echo "Start the VM:"
echo "   VBoxManage startvm '$VM_NAME' --type gui"
echo ""
echo "Follow Ubuntu Server installer:"
echo "   - Language: English, Keyboard: default"
echo "   - Install type: Ubuntu Server (minimized)"
echo "   - Hostname: famcloud-vm"
echo "   - User: famcloud / Password: famcloud"
echo "   - Skip SSH server setup"
echo "   - Wait for install → power off VM"
echo ""
echo "After install:"
echo "   VBoxManage storageattach '$VM_NAME' --storagectl 'IDE' --port 0 --device 0 --type dvddrive --medium none"
echo "   VBoxManage startvm '$VM_NAME' --type headless"
echo ""

# 5. Bootstrap instructions for the VM
echo "============================================"
echo "[5/5] After VM is running:"
echo "============================================"
echo ""
echo "SSH in:"
echo "   ssh -p 2222 famcloud@localhost"
echo ""
echo "Run bootstrap:"
echo "   curl -sL https://raw.githubusercontent.com/Chuck1823/george/main/experiment/scripts/bootstrap-gpu-rig.sh | bash"
echo ""
echo "Verify:"
echo "   ollama list                    # Shows qwen2.5:7b"
echo "   ollama run qwen2.5:7b 'hi'    # Should respond"
echo "   openclaw status               # Gateway online"
echo "   curl http://localhost:18789    # OpenClaw UI (from Mac mini)"
echo ""
echo "============================================"
echo "Scaffolding complete!"
echo "Run: open famcloud-vm-setup.sh"
echo "============================================"

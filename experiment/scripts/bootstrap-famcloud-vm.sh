#!/usr/bin/env bash
set -euo pipefail

# FamCloud Bootstrap — runs inside the Ubuntu VM
# This is what the customer would run on their actual rig

echo "=== FamCloud Bootstrap ==="
echo ""

# Check we're running as root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  This script needs root. Run with: sudo bash bootstrap-famcloud-vm.sh"
    exit 1
fi

echo "[1/8] Installing system dependencies..."
apt update && apt install -y \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    build-essential \
    software-properties-common \
    lsb-release \
    ca-certificates \
    gnupg \
    jq \
    htop \
    net-tools \
    2>&1 | tail -1
echo "   ✅ System dependencies installed"

echo "[2/8] Installing Docker..."
if command -v docker &>/dev/null; then
    echo "   ⏭️  Docker already installed"
else
    curl -fsSL https://get.docker.com | sh 2>&1 | tail -3
    systemctl enable docker
    systemctl start docker
    usermod -aG docker famcloud
    echo "   ✅ Docker installed"
fi

echo "[3/8] Installing Node.js..."
if command -v node &>/dev/null; then
    echo "   ⏭️  Node.js already installed: $(node --version)"
else
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - 2>&1 | tail -1
    apt install -y nodejs 2>&1 | tail -1
    echo "   ✅ Node.js installed: $(node --version)"
fi

echo "[4/8] Installing Ollama..."
if command -v ollama &>/dev/null; then
    echo "   ⏭️  Ollama already installed: $(ollama --version 2>/dev/null || echo 'unknown')"
else
    curl -fsSL https://ollama.com/install.sh | sh 2>&1 | tail -3
    echo "   ✅ Ollama installed"
fi

echo "[5/8] Downloading model: Qwen2.5:7b Q4_K_M..."
ollama list 2>/dev/null | grep -q "qwen2.5" && {
    echo "   ⏭️  Model already downloaded"
} || {
    ollama pull qwen2.5:7b 2>&1 | tail -3
    echo "   ✅ Model downloaded"
}

echo "[6/8] Installing OpenClaw..."
if command -v openclaw &>/dev/null; then
    echo "   ⏭️  OpenClaw already installed: $(openclaw --version 2>/dev/null || echo 'unknown')"
else
    npm install -g openclaw 2>&1 | tail -3
    echo "   ✅ OpenClaw installed"
fi

echo "[7/8] Installing channel plugins..."
for plugin in @openclaw/whatsapp @openclaw/signal; do
    openclaw plugins list 2>/dev/null | grep -q "$plugin" && {
        echo "   ⏭️  $plugin already installed"
    } || {
        openclaw plugins install "$plugin" 2>&1 | tail -1
        echo "   ✅ $plugin installed"
    }
done
echo "   (Telegram, Discord, Slack built-in)"

echo "[8/8] Configuring OpenClaw Gateway..."
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
mkdir -p "$HOME/.openclaw"

if [ -f "$CONFIG_FILE" ]; then
    echo "   ⏭️  Config already exists"
else
    cat > "$CONFIG_FILE" << 'EOF'
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "model": "ollama/qwen2.5:7b"
    }
  },
  "channels": {
    "whatsapp": { "enabled": true },
    "telegram": { "enabled": false },
    "discord": { "enabled": false }
  }
}
EOF
    echo "   ✅ Config created: $CONFIG_FILE"
fi

echo ""
echo "============================================"
echo "✅ FamCloud Bootstrap Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Ollama service:"
echo "   sudo systemctl enable ollama --now"
echo ""
echo "2. Verify model loads:"
echo "   ollama list"
echo "   ollama run qwen2.5:7b 'Say hello from FamCloud'"
echo ""
echo "3. Start OpenClaw Gateway:"
echo "   openclaw gateway start"
echo ""
echo "4. Verify gateway:"
echo "   openclaw status"
echo "   curl http://localhost:18789"
echo ""
echo "5. From Mac mini, access:"
echo "   http://localhost:18789 (OpenClaw UI)"
echo "   http://localhost:2222 (SSH to VM, port 2222→22)"
echo ""

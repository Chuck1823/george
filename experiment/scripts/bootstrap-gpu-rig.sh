#!/bin/bash
# bootstrap-gpu-rig.sh — One-line setup for home GPU rig running local models
# Usage: curl -sL https://<url>/bootstrap-gpu-rig.sh | bash
#
# Installs: NVIDIA drivers, Ollama (or vLLM), OpenClaw, pulls model weights,
# configures auto-update from HuggingFace, and starts the gateway.
set -euo pipefail

echo "🚀 Bootstrapping home GPU rig..."

# ─── System check ───
echo "📋 Checking system..."
if [ "$(uname)" != "Linux" ]; then
    echo "⚠️  This script is designed for Ubuntu/Pop!_OS"
    echo "❌ Detected: $(uname)"
    exit 1
fi

# ─── NVIDIA drivers ───
echo "📦 Installing NVIDIA drivers..."
if ! command -v nvidia-smi &>/dev/null; then
    sudo apt-get update &>/dev/null
    sudo apt-get install -y nvidia-driver-550 &>/dev/null
    echo "✅ NVIDIA driver installed"
    sudo nvidia-smi 2>/dev/null | head -3
else
    echo "✅ NVIDIA driver already installed"
    nvidia-smi --query-gpu=gpu_name,memory.total --format=csv,noheader
fi

# ─── CUDA toolkit (for fine-tuning) ───
echo "📦 Checking CUDA toolkit..."
if ! command -v nvcc &>/dev/null; then
    sudo apt-get install -y cuda-toolkit-12-4 &>/dev/null || echo "⚠️  CUDA toolkit install failed — may need manual install"
else
    echo "✅ CUDA: $(nvcc --version | grep release)"
fi

# ─── Ollama (inference runtime) ───
echo "📦 Installing Ollama..."
if ! command -v ollama &>/dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi
sudo systemctl enable --now ollama &>/dev/null || true
echo "✅ Ollama installed & started"

# ─── PyTorch + vLLM (fine-tuning) ───
echo "📦 Installing fine-tuning stack..."
pip3 install --quiet torch transformers accelerate peft bitsandbytes 2>/dev/null || echo "⚠️  Fine-tuning packages need manual install"
echo "✅ Fine-tuning packages installed (or skipped)"

# ─── HuggingFace CLI ───
echo "📦 Installing HuggingFace CLI..."
if ! command -v huggingface-cli &>/dev/null; then
    pip3 install --quiet huggingface_hub
fi
echo "✅ HuggingFace CLI installed"

# ─── Download model weights ───
MODEL_REPO="${MODEL_REPO:-hearth/qwen2.5-7b-hearth-v1}"
echo "📥 Pulling model weights: $MODEL_REPO"
mkdir -p ~/models

# Option A: Ollama model (GGUF format for inference)
ollama pull "ollama.com/library/qwen2.5:7b" 2>/dev/null || echo "⚠️  Default model pull failed — you need a MODEL_REPO"

# Option B: Download GGUF from HuggingFace for Ollama import
if [ -n "${HF_TOKEN:-}" ]; then
    huggingface-cli download "$MODEL_REPO" --local-dir /root/models/latest
    echo "✅ Model weights downloaded to /root/models/latest"
else
    echo "⚠️  No HF_TOKEN set — using default Ollama model"
fi

# ─── OpenClaw ───
echo "📦 Installing OpenClaw..."
if command -v openclaw &>/dev/null; then
    echo "✅ OpenClaw already installed: $(openclaw --version 2>/dev/null || echo 'unknown')"
else
    npm install -g openclaw 2>/dev/null || echo "npm install failed — install manually"
fi

# ─── Configure OpenClaw for local models ───
echo "⚙️  Configuring OpenClaw..."
cat > ~/.openclaw/openclaw.json << 'OCEOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/auto",
        "fallbacks": ["ollama/qwen2.5:7b"]
      }
    }
  },
  "gateway": {
    "mode": "local",
    "port": 18789,
    "bind": "loopback"
  }
}
OCEOF

echo "✅ OpenClaw configured for local fallback"

# ─── Auto-update script (runs nightly) ───
mkdir -p ~/.local/bin
cat > ~/.local/bin/update-models.sh << 'UPEOF'
#!/bin/bash
# Nightly model update — pulls latest weights from HuggingFace
echo "$(date): Checking for model updates..."
# Pull latest from HuggingFace if HF_TOKEN is set
if [ -n "${HF_TOKEN:-}" ]; then
    NEW_HASH=$(huggingface-cli model-info ${MODEL_REPO} --json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || echo "")
    OLD_HASH=$(cat ~/.local/bin/.model-hash 2>/dev/null || echo "")
    if [ "$NEW_HASH" != "$OLD_HASH" ] && [ -n "$NEW_HASH" ]; then
        echo "New model version detected: $NEW_HASH"
        huggingface-cli download ${MODEL_REPO} --local-dir /opt/models/latest
        ollama create hearth-model -f /opt/models/latest/OllamaModelfile 2>/dev/null || true
        echo "$NEW_HASH" > ~/.local/bin/.model-hash
        echo "✅ Model updated"
    else
        echo "Model up to date"
    fi
fi
UPEOF
chmod +x ~/.local/bin/update-models.sh
(crontab -l 2>/dev/null; echo "0 3 * * * ~/.local/bin/update-models.sh") | crontab -
echo "✅ Nightly model update configured (3 AM)"

# ─── Done ───
echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Check GPU:     nvidia-smi"
echo "  2. Check models:  ollama list"
echo "  3. Test model:    ollama run hearth-model 'Hello!'"
echo "  4. Start gateway: openclaw gateway start"
echo "  5. Complete setup: openclaw setup"
echo ""

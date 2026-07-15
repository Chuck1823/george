#!/usr/bin/env zsh
# Weekly trace export, labeling, and dashboard refresh
set -e

WORKSPACE="/Users/georgemalenclaw/.openclaw/workspace"
TRACES="$WORKSPACE/experiment/traces"
DASHBOARD="$WORKSPACE/experiment/trace-dashboard"
SESSIONS_DIR="/Users/georgemalenclaw/.openclaw/agents/main/sessions"

echo "=== Weekly Export $(date -u '+%Y-%m-%d %H:%M UTC') ==="

# Step 1: Export new sessions to traces
echo ""
echo "1. Exporting sessions..."
python3 "$WORKSPACE/experiment/scripts/export-all.py"

# Step 2: Auto-label traces via OpenRouter
echo ""
echo "2. Classifying traces..."
python3 "$WORKSPACE/experiment/scripts/classify-traces.py"

# Step 3: Rebuild dashboard stats
echo ""
echo "3. Rebuilding stats.json..."
python3 "$DASHBOARD/app.py"

# Step 4: Push dashboard to GitHub Pages
echo ""
echo "4. Pushing dashboard..."
DASH_TMP="/tmp/trace-dashboard-push-$$"
rm -rf "$DASH_TMP"
gh repo clone Chuck1823/trace-dashboard "$DASH_TMP" -- --depth 1
cp "$DASHBOARD/index.html" "$DASH_TMP/index.html"
cp "$DASHBOARD/stats.json" "$DASH_TMP/stats.json"
cp "$DASHBOARD/app.py" "$DASH_TMP/app.py"
cd "$DASH_TMP"
git add -A
git commit -m "Weekly update $(date -u '+%Y-%m-%d')"
git push origin main
cd "$WORKSPACE"
rm -rf "$DASH_TMP"

echo ""
echo "=== Weekly export complete ==="

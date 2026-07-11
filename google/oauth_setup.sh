#!/bin/bash
# Run this to generate the OAuth URL and do a full gog auth setup
# This script runs locally so it can interact with your terminal

cd "$(dirname "$0")/.."
export GOG_KEYRING_BACKEND=file

# Step 1: Register credentials
echo "=== Registering OAuth credentials ==="
gog auth credentials google/oauth/client_secret.json

# Step 2: Add account (this opens browser)
echo ""
echo "=== Adding mcharlesantoine@gmail.com ==="
echo "Browser should open — sign in and allow access."
gog auth add mcharlesantoine@gmail.com --services gmail,calendar,drive,contacts,sheets

# Step 3: Verify
echo ""
echo "=== Auth status ==="
gog auth list

# Step 4: Quick test
echo ""
echo "=== Quick Gmail test ==="
gog gmail search 'newer_than:7d' --max 1

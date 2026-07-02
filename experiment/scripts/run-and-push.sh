#!/bin/bash
# Run this one script to export all traces and push to git

# Export all sessions to dual-track traces
python3 ~/.openclaw/workspace/experiment/scripts/export-all.py

# Commit everything to git
cd ~/.openclaw/workspace
git add -A
git commit -m "Dual-track trace exports, SOUL.md update, export scripts"
git push

echo "Done. Traces exported and repo updated."

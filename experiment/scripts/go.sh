#!/bin/zsh
cd /Users/georgemalenclaw/.openclaw/workspace/experiment/scripts
/usr/bin/python3 export-all.py
cd /Users/georgemalenclaw/.openclaw/workspace
/usr/bin/git add -A
/usr/bin/git commit -m "Dual-track trace exports + soul update"
/usr/bin/git push

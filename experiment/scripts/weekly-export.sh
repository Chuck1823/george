# Export pipeline for the distillation experiment.
# Runs weekly to export + (optionally) teacher-grade all sessions.

set -e
cd /Users/georgemalenclaw/.openclaw/workspace

echo "=== Step 1: Export traces ==="
python3 experiment/scripts/export-all.py

echo ""
echo "=== Step 2: Teacher grading ==="
if [ -n "$TEACHER_API_KEY" ]; then
    echo "TEACHER_API_KEY set — running teacher grading..."
    TEACHER_MODEL="${TEACHER_MODEL:-claude-sonnet-4-20250514}" export TEACHER_MODEL
    python3 experiment/scripts/teacher-grade.py
else
    echo "No TEACHER_API_KEY set. Grading skipped."
    echo "Set env vars to enable:"
    echo "  TEACHER_API_KEY=xxx"
    echo "  TEACHER_MODEL=claude-sonnet-4-20250514"
fi

echo ""
echo "=== Step 3: Commit and push ==="
cd /Users/georgemalenclaw/.openclaw/workspace
if git diff --quiet experiment/traces/ 2>/dev/null; then
    echo "No changes to commit."
else
    git add experiment/traces/
    git commit -m "Weekly trace export $(date +%Y-%m-%d)"
    git push
fi

python3 experiment/scripts/export-all.py
fi

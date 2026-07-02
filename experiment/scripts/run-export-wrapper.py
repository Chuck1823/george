#!/usr/bin/env python3
import subprocess, os, sys

os.chdir("/Users/georgemalenclaw/.openclaw/workspace/experiment/scripts")
result = subprocess.run(
    [sys.executable, "export-all.py"],
    capture_output=False,
    timeout=60
)
print("exit code:", result.returncode)

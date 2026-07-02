#!/usr/bin/env python3
"""
Dual-track trace export from OpenClaw sessions.

Track 1: Text-only (Pioneer-compatible fine-tuning)
Track 2: Full trajectory (OpenAI tool_calls format for agentic training)

Usage: python3 ~/george/experiment/scripts/export-traces.py <session.jsonl> [--output-dir DIR]
"""

import json
import sys
import os
from pathlib import Path

def extract_track1(session_path):
    """Text-only traces: user text + assistant text, no tools/thinking."""
    messages = []
    with open(session_path) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except:
                continue
            if entry.get('type') != 'message':
                continue
            msg = entry.get('message', {})
            role = msg.get('role', '')
            content = msg.get('content')
            if role == 'toolResult':
                continue

            text = ''
            if isinstance(content, list):
                for block in content:
                    if block.get('type') == 'text':
                        t = block.get('text', '').strip()
                        if t:
                            text += t + '\n'
            elif isinstance(content, str):
                text = content.strip()
            text = text.strip()
            if not text:
                continue

            clean_role = 'user' if role == 'user' else 'assistant'
            messages.append({'role': clean_role, 'content': text})

    # Split into traces (max 15 turns each)
    traces = []
    current = []
    for msg in messages:
        current.append({'role': msg['role'], 'content': msg['content']})
        if msg['role'] == 'assistant':
            tc = sum(1 for m in current if m['role'] in ('user', 'assistant'))
            is_end = tc >= 15 or msg == messages[-1]
            if is_end and tc >= 2:
                traces.append({'messages': current})
                current = []
    if len(current) >= 2:
        traces.append({'messages': current})
    return traces

def extract_track2(session_path):
    """Full trajectory: preserves tool calls, results, and thinking."""
    messages = []
    tool_call_ids_seen = set()

    with open(session_path) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except:
                continue
            if entry.get('type') != 'message':
                continue
            msg = entry.get('message', {})
            role = msg.get('role', '')
            content = msg.get('content')

            if role == 'user':
                text = ''
                if isinstance(content, list):
                    for block in content:
                        if block.get('type') == 'text':
                            t = block.get('text', '').strip()
                            if t:
                                text += t + '\n'
                elif isinstance(content, str):
                    text = content.strip()
                text = text.strip()
                if text:
                    messages.append({'role': 'user', 'content': text})

            elif role == 'assistant':
                track2_msg = {'role': 'assistant', 'content': ''}
                tool_calls = []

                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        btype = block.get('type', '')
                        if btype == 'text':
                            t = block.get('text', '').strip()
                            if t:
                                text_parts.append(t)
                        elif btype == 'toolCall':
                            tc = {
                                'id': block.get('id', f"call_{len(tool_calls)}"),
                                'type': 'function',
                                'function': {
                                    'name': block.get('name', ''),
                                    'arguments': json.dumps(block.get('arguments', {}))
                                }
                            }
                            tool_calls.append(tc)
                            tool_call_ids_seen.add(block.get('id', ''))

                    if text_parts:
                        track2_msg['content'] = '\n'.join(text_parts)
                    if tool_calls:
                        track2_msg['tool_calls'] = tool_calls

                elif isinstance(content, str) and content.strip():
                    track2_msg['content'] = content.strip()

                # Only add if has content or tool calls
                if track2_msg['content'] or tool_calls:
                    messages.append(track2_msg)

            elif role == 'toolResult':
                # Map to OpenAI tool role
                tool_call_id = msg.get('toolCallId', '')
                tool_name = msg.get('toolName', '')
                text = ''
                if isinstance(content, list):
                    for block in content:
                        if block.get('type') == 'text':
                            t = block.get('text', '').strip()
                            if t:
                                text += t + '\n'
                elif isinstance(content, str):
                    text = content.strip()
                text = text.strip()

                messages.append({
                    'role': 'tool',
                    'content': text if text else f'[Empty result from {tool_name}]',
                    'tool_call_id': tool_call_id
                })

    # Split into traces (break at assistant response after tool round-trip)
    traces = []
    current = []
    max_turns = 20

    for msg in messages:
        current.append(msg)
        if msg['role'] == 'assistant':
            tc = sum(1 for m in current if m['role'] in ('user', 'assistant'))
            is_end = tc >= max_turns or msg == messages[-1]
            if is_end and tc >= 2:
                traces.append({'messages': current})
                current = []
    if len(current) >= 2:
        traces.append({'messages': current})
    return traces

def main():
    if len(sys.argv) < 2:
        print("Usage: export-traces.py <session.jsonl> [session2.jsonl ...] [--output-dir DIR]")
        sys.exit(1)

    session_files = []
    output_dir = None
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--output-dir' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            session_files.append(arg)
            i += 1

    track1_output = Path(output_dir) / 'text' if output_dir else Path('text')
    track2_output = Path(output_dir) / 'trajectory' if output_dir else Path('trajectory')
    track1_output.mkdir(parents=True, exist_ok=True)
    track2_output.mkdir(parents=True, exist_ok=True)

    manifest_entries = []

    for session_path in session_files:
        sp = Path(session_path)
        if not sp.exists():
            print(f"SKIP: {sp} not found")
            continue

        date_str = sp.stem.split('.')[0] if '.' in sp.stem else sp.stem

        # Track 1
        t1 = extract_track1(sp)
        t1_file = track1_output / f'{date_str}.jsonl'
        with open(t1_file, 'w') as f:
            for t in t1:
                f.write(json.dumps(t, ensure_ascii=False) + '\n')

        # Track 2
        t2 = extract_track2(sp)
        t2_file = track2_output / f'{date_str}.jsonl'
        with open(t2_file, 'w') as f:
            for t in t2:
                f.write(json.dumps(t, ensure_ascii=False) + '\n')

        print(f"{sp.name}:")
        print(f"  Track 1 (text): {len(t1)} traces -> {t1_file}")
        print(f"  Track 2 (trajectory): {len(t2)} traces -> {t2_file}")

        manifest_entries.append({
            'session_id': sp.stem,
            'date': date_str,
            'text_traces': len(t1),
            'trajectory_traces': len(t2)
        })

    # Write manifest
    manifest_file = track1_output.parent / 'manifest.jsonl'
    with open(manifest_file, 'w') as f:
        for entry in manifest_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(f"\nManifest: {manifest_file}")

if __name__ == '__main__':
    main()

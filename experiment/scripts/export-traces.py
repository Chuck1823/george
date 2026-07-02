#!/usr/bin/env python3
"""
Export OpenClaw session to Pioneer-compatible training traces.

Usage: python3 export-traces.py <session_jsonl_path> [--output OUTPUT]

Reads session JSONL (from ~/.openclaw/agents/main/sessions/), extracts
user messages and assistant responses, and outputs JSONL in Pioneer's
Chat SFT format.

Pioneer format:
{"messages": [
  {"role": "system", "content": "..."},
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."}
]}
"""

import json
import sys
import argparse
from pathlib import Path


def extract_messages(session_path):
    """Extract user/assistant messages from an OpenClaw session JSONL file."""
    messages = []
    system_msg = None
    
    with open(session_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            
            if entry.get('type') != 'message':
                continue
            
            msg = entry.get('message', {})
            role = msg.get('role')
            content = msg.get('content')
            
            if role is None or content is None:
                continue
            
            # Handle content as string or list of content blocks
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = '\n'.join(
                    block.get('text', '') 
                    for block in content 
                    if isinstance(block, dict) and block.get('type') == 'text'
                )
            else:
                text = str(content)
            
            if not text.strip():
                continue
            
            # System prompt
            if role == 'system':
                if system_msg is None:
                    system_msg = {"role": "system", "content": text}
                continue
            
            # User or assistant message
            messages.append({
                "role": "user" if role == "user" else "assistant",
                "content": text
            })
    
    return system_msg, messages


def split_into_traces(system_msg, messages, max_turns_per_trace=20):
    """
    Split a long conversation into training traces.
    Each trace is self-contained: system prompt + conversation segments.
    We split at natural boundaries (user messages).
    """
    traces = []
    
    if not messages:
        return traces
    
    # Split into chunks - each chunk ends with an assistant response
    current_messages = []
    if system_msg:
        current_messages.append(system_msg)
    
    for i, msg in enumerate(messages):
        current_messages.append(msg)
        
        # Break at assistant response when we have enough turns, 
        # or when this is the last message
        if msg['role'] == 'assistant':
            should_split = len(current_messages) >= max_turns_per_trace or i == len(messages) - 1
            
            if should_split and len(current_messages) >= 3:  # Need at least system + user + assistant
                trace = {"messages": current_messages}
                traces.append(trace)
                current_messages = [system_msg] if system_msg else []
    
    # Don't forget any remaining messages
    if len(current_messages) >= 3:
        traces.append({"messages": current_messages})
    
    return traces


def main():
    parser = argparse.ArgumentParser(description='Export OpenClaw sessions to training traces')
    parser.add_argument('session_paths', nargs='+', help='Session JSONL file(s)')
    parser.add_argument('--output', '-o', help='Output JSONL file (default: stdout)')
    parser.add_argument('--max-turns', type=int, default=20, 
                        help='Max turns per trace for splitting long conversations')
    
    args = parser.parse_args()
    
    all_traces = []
    
    for session_path in args.session_paths:
        path = Path(session_path)
        if not path.exists():
            print(f"Warning: {path} not found, skipping", file=sys.stderr)
            continue
        
        system_msg, messages = extract_messages(path)
        
        if not messages:
            print(f"Warning: No messages found in {path}", file=sys.stderr)
            continue
        
        traces = split_into_traces(system_msg, messages, args.max_turns)
        all_traces.extend(traces)
        print(f"Extracted {len(traces)} trace(s) from {path.name}")
    
    # Write output
    output_file = args.output
    if output_file:
        with open(output_file, 'w') as f:
            for trace in all_traces:
                f.write(json.dumps(trace, ensure_ascii=False) + '\n')
        print(f"Written {len(all_traces)} traces to {output_file}")
    else:
        for trace in all_traces:
            print(json.dumps(trace, ensure_ascii=False))


if __name__ == '__main__':
    main()

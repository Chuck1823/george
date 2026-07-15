#!/usr/bin/env python3
"""Classify traces into VERTICAL + CAPABILITY labels via OpenRouter.

Two-track taxonomy:
  VERTICAL   = industry (nail_salon, barber_shop, etc.)
  CAPABILITY = what the AI does — GENERIC across verticals

Usage:
  python3 classify-traces.py                          # LLM classify all traces
  VERTICAL=nail_salon python3 classify-traces.py      # force vertical

Uses OpenRouter (same as current session model: openrouter/auto).
"""

import json, os, glob, sys, time, re, urllib.request

API_KEY = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("Need OPENROUTER_API_KEY or OPENAI_API_KEY")
    sys.exit(1)

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.environ.get("OPENROUTER_MODEL", "openrouter/auto")
BATCH_SIZE = 5
TRACES_DIR = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"
FORCE_VERTICAL = os.environ.get("VERTICAL", None)

VERTICALS = [
    "nail_salon","barber_shop","dry_cleaner","restaurant",
    "hair_salon","auto_repair","medical_clinic","fitness_gym",
    "general_retail","pet_grooming","devops_research","unclassified"
]
CAPABILITIES = [
    "booking_appointment","customer_qa","no_show_reduction",
    "customer_retention","inventory_management","staff_scheduling",
    "compliance_tracking","complaint_handling","payment_billing",
    "marketing_promotions","data_entry_reporting","workflow_automation",
    "research","devops","coding","general_assistant"
]

def classify_batch(traces):
    samples = []
    for i, t in enumerate(traces):
        msgs = t.get("messages", [])[-12:]
        parts = []
        for m in msgs:
            c = m.get("content","")
            if isinstance(c, str) and c.strip():
                parts.append(f"[{m['role']}]: {c[:250]}")
            elif isinstance(c, list):
                for b in c:
                    if b.get("type")=="text" and b.get("text","").strip():
                        parts.append(f"[{m['role']}]: {b['text'][:250]}")
        samples.append(f"--- Sample {i} ---\n" + "\n".join(parts))

    ctx = f"\nContext: All traces are from a {FORCE_VERTICAL.replace('_',' ')} business." if FORCE_VERTICAL else ""
    v_list = ", ".join(VERTICALS)
    c_list = ", ".join(CAPABILITIES)
    prompt = f"""Classify each trace. ONE vertical + ONE capability per sample.{ctx}

VERTICALS: {v_list}
CAPABILITIES: {c_list}

Respond as JSON array:
[{{"vertical":"...","capability":"..."}}]

Samples:
{chr(10).join(samples)}"""

    body = json.dumps({
        "model": MODEL,
        "messages": [{"role":"user","content":prompt}],
        "temperature": 0.1,
        "max_tokens": 512,
    }).encode()

    req = urllib.request.Request(API_URL, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("HTTP-Referer", "http://localhost")
    req.add_header("X-Title", "Trace Classifier")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        content = data.get("choices",[{}])[0].get("message",{}).get("content","[]")
        m = re.search(r'\[[\s\S]*\]', content)
        labels = json.loads(m.group()) if m else []
        if isinstance(labels, list) and len(labels) >= len(traces):
            return [{"vertical":l.get("vertical","unclassified"),"capability":l.get("capability","general_assistant")} for l in labels[:len(traces)]]
        raise ValueError("bad response")
    except Exception as e:
        print(f"  API error: {e}")
        return [{"vertical":"unclassified","capability":"general_assistant"} for _ in traces]

def main():
    if FORCE_VERTICAL:
        print(f"Forcing vertical: {FORCE_VERTICAL}")
    total = 0

    for track in ["sft","agentic","distill"]:
        print(f"\n=== {track} ===")
        count = 0
        for fp in sorted(glob.glob(os.path.join(TRACES_DIR, track, "*.jsonl"))):
            with open(fp) as f:
                traces = [json.loads(line) for line in f if line.strip()]
            for i in range(0, len(traces), BATCH_SIZE):
                batch = traces[i:i+BATCH_SIZE]
                if FORCE_VERTICAL:
                    labels = [{"vertical":FORCE_VERTICAL,"capability":"general_assistant"} for _ in batch]
                    print(f"  {os.path.basename(fp)}: forced")
                else:
                    labels = classify_batch(batch)
                    print(f"  {os.path.basename(fp)}: {', '.join(l['capability'] for l in labels)}")
                for j, lab in enumerate(labels):
                    if i+j < len(traces):
                        traces[i+j]["vertical"] = lab["vertical"]
                        traces[i+j]["capability"] = lab["capability"]
                        traces[i+j].pop("task_type", None)
                        traces[i+j].pop("labels", None)
                count += len(batch)
                total += 1
                time.sleep(1.5)
            with open(fp, "w") as f:
                for t in traces:
                    f.write(json.dumps(t, ensure_ascii=False) + "\n")
        print(f"{track}: {count} classified")

    print(f"\nTotal: {total} traces classified")
    print("Next: python3 experiment/trace-dashboard/app.py")

if __name__ == "__main__":
    main()

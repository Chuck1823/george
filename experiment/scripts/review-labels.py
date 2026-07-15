#!/usr/bin/env python3
"""Review current label distribution and suggest label set changes.

Checks unique labels across all traces and compares to the fixed label set
in classify-traces.py. Sends a summary via OpenClaw if there are:
- Labels with 0 traces (could be removed)
- New patterns that suggest new labels (e.g. >3 traces labeled unclassified)
- Label diversity report
"""

import json, glob, os

TRACES_DIR = "/Users/georgemalenclaw/.openclaw/workspace/experiment/traces"

CAPABILITIES = [
    "booking_appointment","customer_qa","no_show_reduction",
    "customer_retention","inventory_management","staff_scheduling",
    "compliance_tracking","complaint_handling","payment_billing",
    "marketing_promotions","data_entry_reporting","workflow_automation",
    "research","devops","coding","general_assistant"
]

VERTICALS = [
    "nail_salon","barber_shop","dry_cleaner","restaurant",
    "hair_salon","auto_repair","medical_clinic","fitness_gym",
    "general_retail","pet_grooming","devops_research","unclassified"
]

def main():
    label_counts = {}
    vertical_counts = {}
    total = 0

    for track in ["sft", "agentic", "distill"]:
        for fp in sorted(glob.glob(os.path.join(TRACES_DIR, track, "*.jsonl"))):
            with open(fp) as fh:
                for line in fh:
                    try:
                        t = json.loads(line)
                    except:
                        continue
                    total += 1
                    lab = t.get("capability", "unclassified")
                    vert = t.get("vertical", "unclassified")
                    label_counts[lab] = label_counts.get(lab, 0) + 1
                    vertical_counts[vert] = vertical_counts.get(vert, 0) + 1

    # Unused labels
    unused_caps = [c for c in CAPABILITIES if c not in label_counts]
    unused_verts = [v for v in VERTICALS if v not in vertical_counts]

    # Unclassified count (potential new label needed)
    unclass_cap = label_counts.get("unclassified", 0)
    unclass_vert = vertical_counts.get("unclassified", 0)

    # Build report
    report = []
    report.append(f"📊 Label Review — {total} total traces")
    report.append("")

    # Top capabilities
    report.append("**Top Capabilities:**")
    for cap, ct in sorted(label_counts.items(), key=lambda x: -x[1]):
        report.append(f"  • {cap}: {ct}")

    report.append("")
    report.append("**Top Verticals:**")
    for vert, ct in sorted(vertical_counts.items(), key=lambda x: -x[1]):
        report.append(f"  • {vert}: {ct}")

    report.append("")
    if unused_caps:
        report.append(f"**Unused capabilities ({len(unused_caps)}):** {', '.join(unused_caps)}")
    if unused_verts:
        report.append(f"**Unused verticals ({len(unused_verts)}):** {', '.join(unused_verts)}")

    suggestions = []
    if unclass_cap > 3:
        suggestions.append(f"{unclass_cap} traces labeled 'unclassified' — consider splitting into specific labels")
    if unclass_vert > 3:
        suggestions.append(f"{unclass_vert} traces labeled 'unclassified' vertical — need new verticals")
    if len(unused_caps) > len(CAPABILITIES) // 2:
        suggestions.append(f"More than half capabilities unused ({len(unused_caps)}/{len(CAPABILITIES)}) — consider trimming")

    if suggestions:
        report.append("")
        report.append("**Suggestions:**")
        for s in suggestions:
            report.append(f"  ⚠ {s}")

    report.append("")
    report.append(f"Dashboard: https://chuck1823.github.io/trace-dashboard/")

    print("\n".join(report))


if __name__ == "__main__":
    main()

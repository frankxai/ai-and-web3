#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from statistics import mean


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_report.py <lab-folder>")
        sys.exit(1)
    lab = Path(sys.argv[1])
    runs = lab / "runs"
    scores = []
    if runs.exists():
        for f in runs.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                scores.append(data)
            except Exception:
                pass
    report = lab / "REPORT.md"
    if not scores:
        report.write_text("# Report\n\nNo runs recorded yet.\n")
        print(f"Wrote {report}")
        return
    succ = sum(1 for s in scores if s.get("success"))
    lat = [s.get("latency_ms", 0) for s in scores]
    cost = [s.get("cost", 0.0) for s in scores]
    lines = [
        "# Report",
        f"Total runs: {len(scores)}",
        f"Successes: {succ}",
        f"Avg latency (ms): {int(mean(lat)) if lat else 0}",
        f"Avg cost: {round(mean(cost), 4) if cost else 0}",
        "\n## Runs",
    ]
    for s in scores:
        lines.append(f"- {s.get('framework')} | {s.get('task')} | success={s.get('success')} | cost={s.get('cost')} | latency_ms={s.get('latency_ms')}")
    report.write_text("\n".join(lines))
    print(f"Wrote {report}")


if __name__ == "__main__":
    main()


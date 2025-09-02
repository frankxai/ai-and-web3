#!/usr/bin/env python3
import argparse
from pathlib import Path
import re

TEMPLATE = """# Day {day:03d} — {title}

## Goals
- ...

## Prerequisites
- ...

## Tasks
1) ...

## Acceptance criteria
- [ ] ...

## Stretch
- ...
"""

def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9-]", "-", s.lower()).strip("-")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--day", type=int, required=True)
    p.add_argument("--name", type=str, required=True, help="short name, e.g. 'intent-swap-aggregator'")
    args = p.parse_args()

    day = args.day
    title = args.name.replace("-", " ").title()
    folder = Path(__file__).resolve().parents[1] / "labs" / f"day-{day:03d}-{args.name}"
    folder.mkdir(parents=True, exist_ok=True)
    readme = folder / "README.md"
    if not readme.exists():
        readme.write_text(TEMPLATE.format(day=day, title=title))
        print(f"Created {readme}")
    else:
        print(f"Exists: {readme}")

if __name__ == "__main__":
    main()


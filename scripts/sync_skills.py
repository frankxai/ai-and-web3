#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil

SKIP_DIRS = {".git", "__pycache__", "node_modules"}


def iter_skill_files(source: Path):
    for path in source.rglob("SKILL.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def build_registry(sources, dest_root: Path):
    skills = []
    for label, source in sources:
        for skill_md in iter_skill_files(source):
            rel = skill_md.parent.relative_to(source)
            parts = rel.parts
            category = parts[0] if parts else "root"
            library_path = dest_root / label / rel
            skills.append(
                {
                    "name": parts[-1] if parts else skill_md.parent.name,
                    "category": category,
                    "source": label,
                    "source_rel_path": str(rel.as_posix()),
                    "library_path": str(library_path.as_posix()),
                }
            )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": [{"label": label, "path": str(path)} for label, path in sources],
        "skills": sorted(skills, key=lambda x: (x["source"], x["category"], x["name"])),
    }


def copy_sources(sources, dest_root: Path):
    dest_root.mkdir(parents=True, exist_ok=True)
    for label, source in sources:
        dest = dest_root / label
        shutil.copytree(
            source,
            dest,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(*SKIP_DIRS),
        )


def parse_sources(values):
    sources = []
    for value in values:
        if "=" not in value:
            raise ValueError("Each --source must be in label=path format")
        label, path = value.split("=", 1)
        source = Path(path).expanduser().resolve()
        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source}")
        sources.append((label, source))
    return sources


def main():
    parser = argparse.ArgumentParser(description="Sync and index skill libraries")
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Source in label=path format. Example: claude=/path/to/.claude-skills",
    )
    parser.add_argument(
        "--registry",
        default="skills/registry.json",
        help="Registry output path (default: skills/registry.json)",
    )
    parser.add_argument(
        "--dest-root",
        default="skills/library",
        help="Destination root for copied libraries (default: skills/library)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy source trees into dest root",
    )
    args = parser.parse_args()

    sources = parse_sources(args.source)
    dest_root = Path(args.dest_root)
    registry = build_registry(sources, dest_root)

    registry_path = Path(args.registry)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(registry, indent=2))

    if args.copy:
        copy_sources(sources, dest_root)


if __name__ == "__main__":
    main()

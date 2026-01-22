# Skills Library Mirror

This folder can mirror external skill libraries for local use and search. Use the sync script to copy sources and regenerate the registry.

## Sync command
```bash
python3 scripts/sync_skills.py \
  --source claude=/mnt/c/Users/Frank/FrankX/.claude-skills \
  --source opencode=/mnt/c/Users/Frank/FrankX/.opencode \
  --copy
```

## Registry
The registry is generated at `skills/registry.json` and can be used for search and tooling.

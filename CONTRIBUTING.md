# Contributing

## Principles
- Safety first: never commit secrets, use testnets/forks
- Reproducible labs: clear steps, acceptance checks, artifacts
- Minimal dependencies: prefer small, composable tools

## How to contribute
- Fork and branch from `main`
- Add or update a lab with runnable scripts and `acceptance.md`
- Update `README.md` and `docs/` where relevant
- Include links in `resources/` when adding external projects
- Run `scripts/generate_report.py` on modified labs if applicable

## Code style
- Keep Python simple; avoid heavy frameworks unless needed
- Use clear names and avoid one-letter variables

## Security
- No private keys in code or commits
- Add policy checks for any state-changing tool

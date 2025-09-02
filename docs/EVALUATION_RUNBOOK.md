# Evaluation Runbook

## 1) Pick a lab
- Example: `day-001-wallets-and-rpc`

## 2) Choose a framework
- Start with one (e.g., LangGraph or Assistants) and wire minimal tools

## 3) Execute tasks
- Produce artifacts under `labs/<day>/runs/<timestamp>.json`

## 4) Record run
- `python scripts/evaluate_agent.py --lab <day> --framework <id> --task <id> --success --cost <c> --latency_ms <ms>`

## 5) Score
- Use `EVALS.md` rubric
- Summarize results in `labs/<day>/REPORT.md`

## 6) Regressions
- Keep task prompts and configs; re-run after changes to tools or prompts

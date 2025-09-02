.PHONY: help setup-python lab eval

help:
	@echo "Targets: setup-python, lab, eval"

setup-python:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip -q && pip install -r requirements.txt

lab:
	python scripts/scaffold_lab.py --day $(DAY) --name "$(NAME)"

eval:
	python scripts/evaluate_agent.py --lab $(LAB) --framework $(FRAMEWORK) --task $(TASK) --success --cost 0 --latency_ms 0


#!/usr/bin/env bash
set -euo pipefail

echo "Creating Python venv and installing deps..."
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt

echo "Attempting to install Foundry (optional)..."
if [ -z "${CI:-}" ]; then
  curl -L https://foundry.paradigm.xyz | bash || true
  if [ -f "$HOME/.foundry/bin/foundryup" ]; then
    "$HOME/.foundry/bin/foundryup" || true
  fi
fi

echo "Done. Run: source .venv/bin/activate"


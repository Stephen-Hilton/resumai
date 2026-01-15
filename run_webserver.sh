#!/usr/bin/env bash
set -euo pipefail
if [ -d ".venv_resumai" ]; then
  source .venv_resumai/bin/activate
fi
export FLASK_APP=src/ui/app.py
export FLASK_ENV=development
python -m src.ui.app

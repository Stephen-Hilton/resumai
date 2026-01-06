#!/bin/bash

# ResumeAI Virtual Environment Activation Script
# This script activates the Python virtual environment for ResumeAI

VENV_NAME="venv_resumai"

if [ -d "$VENV_NAME" ]; then
    echo "Activating ResumeAI virtual environment..."
    source "$VENV_NAME/bin/activate"
    echo "✓ Virtual environment activated: $VIRTUAL_ENV"
    echo ""
    echo "You can now run:"
    echo "  python src/main.py          # Main application"
    echo "  python src/ui/run.py        # Web UI"
    echo ""
    echo "To deactivate when done:"
    echo "  deactivate"
else
    echo "❌ Virtual environment '$VENV_NAME' not found."
    echo "Please run ./dependencies.sh first to set up the environment."
    exit 1
fi
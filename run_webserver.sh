#!/bin/bash

# ResumeAI Web Server Startup Script
# This script deactivates any active virtual environment, 
# activates the resumai virtual environment, and starts the web UI

echo "🚀 Starting ResumeAI Web Server..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Deactivate any currently active virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    print_status "Deactivating current virtual environment: $(basename $VIRTUAL_ENV)"
    # Note: deactivate function is only available in sourced sessions
    # In a new shell, we just unset the environment variables
    unset VIRTUAL_ENV
    unset PYTHONPATH
fi

# Get the script directory to ensure we're in the right location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_status "Working directory: $SCRIPT_DIR"

# Check if the virtual environment exists
VENV_PATH="$SCRIPT_DIR/.venv_resumai"
if [[ ! -d "$VENV_PATH" ]]; then
    print_error "Virtual environment not found at: $VENV_PATH"
    print_warning "Please create the virtual environment first by running:"
    echo "   ./dependencies.sh"
    echo ""
    echo "Or manually:"
    echo "   python3 -m venv .venv_resumai"
    echo "   source .venv_resumai/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate the resumai virtual environment
print_status "Activating virtual environment: .venv_resumai"
source "$VENV_PATH/bin/activate"

# Verify activation
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_error "Failed to activate virtual environment"
    print_warning "Try running the activation manually:"
    echo "   source .venv_resumai/bin/activate"
    exit 1
fi

print_success "Virtual environment activated: $(basename $VIRTUAL_ENV)"

# Check if the web UI script exists
WEB_UI_SCRIPT="$SCRIPT_DIR/src/ui/run.py"
if [[ ! -f "$WEB_UI_SCRIPT" ]]; then
    print_error "Web UI script not found at: $WEB_UI_SCRIPT"
    print_warning "Make sure you're running this script from the project root directory"
    exit 1
fi

# Check if required directories exist
JOBS_DIR="$SCRIPT_DIR/src/jobs"
if [[ ! -d "$JOBS_DIR" ]]; then
    print_warning "Jobs directory not found, creating: $JOBS_DIR"
    mkdir -p "$JOBS_DIR"/{1_queued,2_generated,3_applied,4_communications,5_interviews,8_errors,9_expired,9_skipped}
fi

# Check if .env file exists
ENV_FILE="$SCRIPT_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
    print_warning ".env file not found"
    print_warning "Copy .env.example to .env and configure your API keys"
    if [[ -f "$SCRIPT_DIR/.env.example" ]]; then
        print_status "Found .env.example, you can copy it:"
        echo "   cp .env.example .env"
    fi
fi

# Test Python imports
print_status "Testing Python dependencies..."
python3 -c "
import sys
try:
    import flask
    import yaml
    import pathlib
    print('✓ Core dependencies available')
except ImportError as e:
    print(f'✗ Missing dependencies: {e}')
    print('Run ./dependencies.sh to install required packages')
    sys.exit(1)
" || {
    print_error "Missing Python dependencies"
    print_warning "Run ./dependencies.sh to install required packages"
    exit 1
}

# Start the web server
print_success "All checks passed!"
echo ""
print_status "Starting web server..."
print_status "Working directory: $SCRIPT_DIR"
print_status "Python: $(which python3)"
print_status "Script: $WEB_UI_SCRIPT"
echo ""
echo "🌐 Web interface will be available at: http://127.0.0.1:5001"
echo "📂 Managing jobs in: src/jobs/2_generated/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Set error handling for the Python script
set -e

# Run the web UI script with error handling
if python3 "$WEB_UI_SCRIPT"; then
    print_success "Web server stopped normally"
else
    exit_code=$?
    print_error "Web server exited with error code: $exit_code"
    print_warning "Check the error messages above for troubleshooting"
    exit $exit_code
fi
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

# Security validation function
validate_environment() {
    # Check if we're in a reasonable directory (should contain src/ and requirements.txt)
    if [[ ! -d "src" ]] || [[ ! -f "requirements.txt" ]]; then
        print_error "This doesn't appear to be the ResumeAI project directory"
        print_warning "Expected to find 'src/' directory and 'requirements.txt' file"
        print_warning "Current directory: $(pwd)"
        exit 1
    fi
    
    # Validate script directory path doesn't contain suspicious characters
    if [[ "$SCRIPT_DIR" =~ [\;\&\|\`\$] ]]; then
        print_error "Script directory path contains suspicious characters: $SCRIPT_DIR"
        exit 1
    fi
    
    print_status "Environment validation passed"
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

# Validate environment security
validate_environment

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

# Set up library paths for WeasyPrint dependencies (macOS with Homebrew)
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_status "Setting up macOS library paths for WeasyPrint"
    # Use safer path concatenation
    HOMEBREW_LIB="/opt/homebrew/lib"
    if [[ -d "$HOMEBREW_LIB" ]]; then
        export DYLD_LIBRARY_PATH="${HOMEBREW_LIB}:${DYLD_LIBRARY_PATH:-}"
        export PKG_CONFIG_PATH="${HOMEBREW_LIB}/pkgconfig:${PKG_CONFIG_PATH:-}"
        export DYLD_FALLBACK_LIBRARY_PATH="${HOMEBREW_LIB}:${DYLD_FALLBACK_LIBRARY_PATH:-}"
    else
        print_warning "Homebrew lib directory not found at $HOMEBREW_LIB"
    fi
fi

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
import os

# Validate we're in the expected directory
expected_dir = os.path.abspath('$SCRIPT_DIR')
current_dir = os.getcwd()
if current_dir != expected_dir:
    print(f'Warning: Directory mismatch. Expected: {expected_dir}, Current: {current_dir}')

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

# Test WeasyPrint specifically
print_status "Testing WeasyPrint PDF engine..."
python3 -c "
import sys
import os

try:
    from weasyprint import HTML
    # Use minimal test HTML to avoid any injection risks
    test_html = HTML(string='<html><head><title>Test</title></head><body><p>Test</p></body></html>')
    pdf_bytes = test_html.write_pdf()
    if len(pdf_bytes) > 100:  # Sanity check for valid PDF
        print(f'✓ WeasyPrint working ({len(pdf_bytes)} bytes)')
    else:
        print('✗ WeasyPrint produced invalid PDF')
        sys.exit(1)
except Exception as e:
    print(f'✗ WeasyPrint error: {e}')
    error_str = str(e).lower()
    if 'libgobject' in error_str or 'cairo' in error_str:
        print('  Install system dependencies: brew install cairo pango gdk-pixbuf libffi')
    elif 'weasyprint' in error_str:
        print('  Install WeasyPrint: pip install weasyprint')
    else:
        print('  Check WeasyPrint installation and system dependencies')
    sys.exit(1)
" || {
    print_warning "WeasyPrint may not work properly - PDF generation will be unavailable"
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
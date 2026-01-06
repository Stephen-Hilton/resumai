#!/bin/bash

# ResumeAI Dependencies Installation Script
# This script installs all system and Python dependencies for the ResumeAI project
# 
# Features:
# - Creates and activates a Python virtual environment (venv_resumai)
# - Installs system dependencies via Homebrew (macOS only)
# - Installs all required Python packages
# - Verifies installation and provides troubleshooting info
#
# Usage:
#   ./dependencies.sh
#
# Requirements:
# - macOS (for Homebrew packages)
# - Homebrew installed
# - Python 3.7+ installed

# Improved error handling - don't exit on errors, handle them gracefully
set +e  # Don't exit on errors, handle them gracefully

echo "🚀 Starting ResumeAI Dependencies Installation..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to handle errors gracefully
handle_error() {
    local exit_code=$1
    local error_message="$2"
    
    if [ $exit_code -ne 0 ]; then
        print_error "$error_message"
        print_warning "Continuing with installation, but this may cause issues later..."
        return 1
    fi
    return 0
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. For Linux, please see PDF_SETUP.md for manual installation instructions."
    print_warning "You can still try to run the Python parts manually."
    echo "Exiting gracefully..."
    exit 0
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print_error "Homebrew is not installed. Please install Homebrew first:"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    print_warning "Continuing without Homebrew packages - some features may not work."
else
    print_success "Homebrew found"
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    echo "Exiting gracefully..."
    exit 0
fi

print_success "Python 3 found: $(python3 --version)"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 first."
    echo "Exiting gracefully..."
    exit 0
fi

print_success "pip3 found: $(pip3 --version)"

echo ""
print_status "Setting up Python virtual environment..."
echo "========================================"

# Virtual environment setup
VENV_NAME=".venv_resumai"

if [ -d "$VENV_NAME" ]; then
    print_warning "Virtual environment '$VENV_NAME' already exists"
else
    print_status "Creating virtual environment '$VENV_NAME'..."
    if python3 -m venv "$VENV_NAME"; then
        print_success "Virtual environment created successfully"
    else
        print_error "Failed to create virtual environment"
        print_warning "You may need to install python3-venv package"
        echo "Exiting gracefully..."
        exit 0
    fi
fi

# Activate virtual environment
print_status "Activating virtual environment..."
if [ -f "$VENV_NAME/bin/activate" ]; then
    source "$VENV_NAME/bin/activate"
    
    if [ "$VIRTUAL_ENV" ]; then
        print_success "Virtual environment activated: $VIRTUAL_ENV"
    else
        print_error "Failed to activate virtual environment"
        echo "Exiting gracefully..."
        exit 0
    fi
else
    print_error "Virtual environment activation script not found"
    echo "Exiting gracefully..."
    exit 0
fi

# Upgrade pip in virtual environment
print_status "Upgrading pip in virtual environment..."
if pip install --upgrade pip; then
    print_success "pip upgraded successfully"
else
    print_warning "Failed to upgrade pip, continuing with current version"
fi

echo ""
print_status "Installing system dependencies via Homebrew..."
echo "=============================================="

# Only install Homebrew packages if brew is available
if command -v brew &> /dev/null; then
    # System dependencies for WeasyPrint and other tools
    BREW_PACKAGES=(
        "pango"           # Text rendering for WeasyPrint
        "gdk-pixbuf"      # Image loading for WeasyPrint  
        "libffi"          # Foreign function interface
        "cairo"           # 2D graphics library
        "gobject-introspection"  # GObject introspection
        "pkg-config"      # Package configuration tool
    )

    for package in "${BREW_PACKAGES[@]}"; do
        print_status "Installing $package..."
        if brew list "$package" &>/dev/null; then
            print_warning "$package is already installed"
        else
            if brew install "$package"; then
                print_success "Successfully installed $package"
            else
                print_error "Failed to install $package"
                print_warning "Continuing without $package - some features may not work"
            fi
        fi
    done
else
    print_warning "Homebrew not available, skipping system dependencies"
    print_warning "PDF generation may not work without system libraries"
fi

echo ""
print_status "Installing Python dependencies..."
echo "=================================="

# Core Python dependencies identified from source code analysis
PYTHON_PACKAGES=(
    # Core dependencies
    "python-dotenv"     # Environment variable management (.env files)
    "pyyaml"           # YAML file parsing
    "requests"         # HTTP requests
    "pathlib"          # Path manipulation (usually built-in, but ensuring compatibility)
    
    # Web framework
    "flask"            # Web UI framework
    
    # Email and parsing
    "beautifulsoup4"   # HTML parsing for LinkedIn emails
    "lxml"             # XML/HTML parser (BeautifulSoup backend)
    
    # AI/LLM providers
    "openai"           # OpenAI API client
    "anthropic"        # Anthropic API client
    
    # PDF generation (dual support)
    "weasyprint"       # Primary PDF generation library
    "pdfkit"           # Fallback PDF generation library
    
    # Date/time handling
    "pytz"             # Timezone support (fallback for zoneinfo)
)

# Optional packages that might be needed
OPTIONAL_PACKAGES=(
    "pillow"           # Image processing (may be needed for WeasyPrint)
    "cffi"             # C Foreign Function Interface (WeasyPrint dependency)
    "cssselect2"       # CSS selector library (WeasyPrint dependency)
    "html5lib"         # HTML parser (WeasyPrint dependency)
    "pyphen"           # Hyphenation library (WeasyPrint dependency)
    "tinycss2"         # CSS parser (WeasyPrint dependency)
)

# Function to install Python package
install_python_package() {
    local package=$1
    local optional=${2:-false}
    
    print_status "Installing Python package: $package"
    
    if pip show "$package" &>/dev/null; then
        print_warning "$package is already installed"
        return 0
    fi
    
    if pip install "$package"; then
        print_success "Successfully installed $package"
        return 0
    else
        if [ "$optional" = true ]; then
            print_warning "Failed to install optional package $package (continuing...)"
            return 0
        else
            print_error "Failed to install required package $package"
            print_warning "Continuing anyway - some features may not work"
            return 1
        fi
    fi
}

# Install required packages
echo ""
print_status "Installing required Python packages..."
failed_packages=()
for package in "${PYTHON_PACKAGES[@]}"; do
    if ! install_python_package "$package"; then
        failed_packages+=("$package")
    fi
done

if [ ${#failed_packages[@]} -gt 0 ]; then
    print_warning "Some required packages failed to install: ${failed_packages[*]}"
    print_warning "The application may not work correctly"
fi

# Install optional packages
echo ""
print_status "Installing optional Python packages..."
for package in "${OPTIONAL_PACKAGES[@]}"; do
    install_python_package "$package" true
done

echo ""
print_status "Updating requirements.txt..."
echo "============================="

# Create/update requirements.txt with all installed packages
cat > requirements.txt << EOF
# Core dependencies
python-dotenv
pyyaml
requests
flask

# Email and parsing
beautifulsoup4
lxml

# AI/LLM providers
openai
anthropic

# PDF generation (dual support)
weasyprint
pdfkit

# Optional dependencies for better compatibility
pillow
cffi
cssselect2
html5lib
pyphen
tinycss2
pytz
EOF

print_success "Updated requirements.txt"

echo ""
print_status "Setting up environment for WeasyPrint..."
echo "========================================"

# Add library path to shell profile for WeasyPrint
SHELL_PROFILE=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [ -n "$SHELL_PROFILE" ]; then
    # Check if DYLD_LIBRARY_PATH is already set for Homebrew
    if ! grep -q "DYLD_LIBRARY_PATH.*homebrew" "$SHELL_PROFILE" 2>/dev/null; then
        echo "" >> "$SHELL_PROFILE"
        echo "# WeasyPrint library path for ResumeAI" >> "$SHELL_PROFILE"
        echo 'export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"' >> "$SHELL_PROFILE"
        print_success "Added library path to $SHELL_PROFILE"
    else
        print_warning "Library path already configured in $SHELL_PROFILE"
    fi
fi

# Set for current session
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

echo ""
print_status "Verifying installation..."
echo "========================="

# Test critical imports
python3 -c "
import sys
import os
from pathlib import Path

# Test core imports
try:
    import yaml
    print('✓ YAML support working')
except ImportError as e:
    print(f'✗ YAML import failed: {e}')
    sys.exit(1)

try:
    import requests
    print('✓ HTTP requests working')
except ImportError as e:
    print(f'✗ Requests import failed: {e}')
    sys.exit(1)

try:
    import flask
    print('✓ Flask web framework working')
except ImportError as e:
    print(f'✗ Flask import failed: {e}')
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    print('✓ BeautifulSoup HTML parsing working')
except ImportError as e:
    print(f'✗ BeautifulSoup import failed: {e}')
    sys.exit(1)

try:
    import openai
    print('✓ OpenAI client working')
except ImportError as e:
    print(f'✗ OpenAI import failed: {e}')
    sys.exit(1)

try:
    import anthropic
    print('✓ Anthropic client working')
except ImportError as e:
    print(f'✗ Anthropic import failed: {e}')
    sys.exit(1)

# Test PDF libraries
weasyprint_available = False
pdfkit_available = False

try:
    from weasyprint import HTML, CSS
    weasyprint_available = True
    print('✓ WeasyPrint PDF generation working')
except (ImportError, OSError) as e:
    print(f'⚠ WeasyPrint not available: {e}')

try:
    import pdfkit
    pdfkit_available = True
    print('✓ pdfkit PDF generation working')
except ImportError as e:
    print(f'⚠ pdfkit not available: {e}')

if not weasyprint_available and not pdfkit_available:
    print('⚠ No PDF generation libraries available - PDF features will not work')
elif weasyprint_available:
    print('✓ PDF generation ready (WeasyPrint)')
elif pdfkit_available:
    print('⚠ PDF generation ready (pdfkit only - may need wkhtmltopdf binary)')

print('\\n✓ Core dependencies verified successfully!')
" 2>/dev/null

verification_result=$?

if [ $verification_result -eq 0 ]; then
    echo ""
    print_success "🎉 Dependencies installed successfully!"
    echo ""
    echo "Virtual environment: $VIRTUAL_ENV"
    echo ""
    echo "To activate the virtual environment in future sessions:"
    echo "  source $VENV_NAME/bin/activate"
    echo ""
    echo "Next steps:"
    echo "1. Copy .env.example to .env and configure your API keys"
    echo "2. Run the application: python src/main.py"
    echo "3. Or start the web UI: python src/ui/run.py"
    echo ""
    echo "For PDF generation troubleshooting, see PDF_SETUP.md"
else
    print_error "Dependency verification failed, but installation completed"
    print_warning "Some features may not work correctly"
    echo ""
    echo "Virtual environment: $VIRTUAL_ENV"
    echo ""
    echo "You can still try to run the application:"
    echo "1. Copy .env.example to .env and configure your API keys"
    echo "2. Try running: python src/main.py"
    echo "3. Or try the web UI: python src/ui/run.py"
fi

echo ""
print_status "Installation script completed! 🚀"
#!/usr/bin/env python3
"""
Startup script for ResumeAI Web UI
"""

import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from ui.app import app, ensure_directories, logger
except ImportError as e:
    print(f"Error importing app module: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

if __name__ == '__main__':
    try:
        ensure_directories()
        print("\n" + "="*50)
        print("🚀 ResumeAI Job Manager Web UI")
        print("="*50)
        print("📂 Managing jobs in: src/jobs/2_generated/")
        print("🌐 Web interface: http://127.0.0.1:5001")
        print("📝 Features:")
        print("   • View all generated job applications")
        print("   • Edit job YAML data")
        print("   • Preview HTML resumes and cover letters")
        print("   • Open original job links")
        print("   • Mark jobs as applied (moves to 3_applied/)")
        print("="*50)
        print("Press Ctrl+C to stop the server")
        print("="*50 + "\n")
        
        logger.info("Starting ResumeAI Web UI on http://127.0.0.1:5001")
        
        app.run(debug=True, host='127.0.0.1', port=5001)
    except KeyboardInterrupt:
        print("\n👋 ResumeAI Web UI stopped")
        logger.info("ResumeAI Web UI stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting web UI: {e}")
        logger.error(f"Error starting ResumeAI Web UI: {e}")
        sys.exit(1)
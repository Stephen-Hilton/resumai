#!/usr/bin/env python3
"""
Test different Python PDF engines to find the best one for HTML to PDF conversion.
"""

import sys
import subprocess
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def test_engine_availability():
    """Test which PDF engines are available and their capabilities"""
    
    engines = {}
    
    # Test WeasyPrint
    try:
        from weasyprint import HTML
        engines['weasyprint'] = {
            'available': True,
            'description': 'Pure Python, good CSS support, but has limitations',
            'pros': ['Pure Python', 'Good CSS3 support', 'No external dependencies'],
            'cons': ['Limited font support', 'Some CSS properties not supported', 'Slower']
        }
    except ImportError:
        engines['weasyprint'] = {'available': False, 'error': 'Not installed'}
    
    # Test pdfkit (wkhtmltopdf)
    try:
        import pdfkit
        # Check if wkhtmltopdf is available
        try:
            pdfkit.configuration()
            engines['pdfkit'] = {
                'available': True,
                'description': 'Wrapper for wkhtmltopdf, excellent rendering',
                'pros': ['Excellent CSS/HTML rendering', 'Fast', 'Mature'],
                'cons': ['Requires external binary', 'Binary not available on all systems']
            }
        except OSError:
            engines['pdfkit'] = {
                'available': False, 
                'error': 'pdfkit installed but wkhtmltopdf binary not found'
            }
    except ImportError:
        engines['pdfkit'] = {'available': False, 'error': 'Not installed'}
    
    # Test Playwright (modern browser automation)
    try:
        from playwright.sync_api import sync_playwright
        engines['playwright'] = {
            'available': True,
            'description': 'Real browser engine (Chromium), perfect rendering',
            'pros': ['Perfect CSS/HTML rendering', 'Real browser engine', 'Modern'],
            'cons': ['Larger dependency', 'Requires browser download']
        }
    except ImportError:
        engines['playwright'] = {'available': False, 'error': 'Not installed'}
    
    # Test Selenium + Chrome (browser automation)
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        engines['selenium'] = {
            'available': True,
            'description': 'Browser automation with Chrome/Firefox',
            'pros': ['Perfect rendering', 'Uses real browser', 'Flexible'],
            'cons': ['Requires browser installation', 'More complex setup']
        }
    except ImportError:
        engines['selenium'] = {'available': False, 'error': 'Not installed'}
    
    # Test pyppeteer (Puppeteer for Python)
    try:
        import pyppeteer
        engines['pyppeteer'] = {
            'available': True,
            'description': 'Python port of Puppeteer (Chrome automation)',
            'pros': ['Perfect rendering', 'Chrome engine', 'Good performance'],
            'cons': ['Async only', 'Chrome dependency']
        }
    except ImportError:
        engines['pyppeteer'] = {'available': False, 'error': 'Not installed'}
    
    return engines

def recommend_best_engine(engines):
    """Recommend the best available engine"""
    
    # Priority order (best to worst for our use case)
    priority = [
        'playwright',    # Best: Real browser, perfect rendering
        'selenium',      # Good: Real browser, widely supported
        'pdfkit',        # Good: Fast, mature, but needs binary
        'pyppeteer',     # Good: Chrome engine, but async
        'weasyprint'     # Fallback: Pure Python but limited
    ]
    
    available_engines = [name for name, info in engines.items() if info.get('available', False)]
    
    for engine in priority:
        if engine in available_engines:
            return engine, engines[engine]
    
    return None, None

def install_recommendations():
    """Provide installation recommendations for missing engines"""
    
    recommendations = {
        'playwright': [
            'pip install playwright',
            'playwright install chromium'
        ],
        'selenium': [
            'pip install selenium',
            'brew install chromedriver  # or download from https://chromedriver.chromium.org/'
        ],
        'pdfkit': [
            'pip install pdfkit',
            'brew install wkhtmltopdf  # Note: May not be available in newer Homebrew'
        ],
        'pyppeteer': [
            'pip install pyppeteer',
            'pyppeteer-install  # Downloads Chromium'
        ],
        'weasyprint': [
            'pip install weasyprint'
        ]
    }
    
    return recommendations

def main():
    print("Testing PDF Engine Availability")
    print("=" * 50)
    
    engines = test_engine_availability()
    
    print("Available Engines:")
    for name, info in engines.items():
        if info.get('available', False):
            print(f"✅ {name.upper()}: {info['description']}")
            print(f"   Pros: {', '.join(info['pros'])}")
            print(f"   Cons: {', '.join(info['cons'])}")
        else:
            print(f"❌ {name.upper()}: {info.get('error', 'Unknown error')}")
        print()
    
    # Recommend best engine
    best_engine, best_info = recommend_best_engine(engines)
    
    if best_engine:
        print(f"🏆 RECOMMENDED: {best_engine.upper()}")
        print(f"   {best_info['description']}")
        print(f"   Pros: {', '.join(best_info['pros'])}")
    else:
        print("❌ No suitable PDF engines found!")
        print("\nInstallation recommendations:")
        recommendations = install_recommendations()
        
        print("\n🎯 BEST OPTION - Playwright:")
        for cmd in recommendations['playwright']:
            print(f"   {cmd}")
        
        print("\n🥈 ALTERNATIVE - Selenium:")
        for cmd in recommendations['selenium']:
            print(f"   {cmd}")
    
    return 0 if best_engine else 1

if __name__ == "__main__":
    sys.exit(main())
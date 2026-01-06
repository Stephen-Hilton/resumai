#!/usr/bin/env python3
"""
PDF Manager - Handles HTML to PDF conversion using multiple engines.

This module provides a unified interface for converting HTML files to PDF
using the best available engine (Playwright > WeasyPrint).
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging_setup

# Set up logger for this module
logger = logging_setup.get_logger(__name__)


class PDFManager:
    """
    Manages PDF conversion from HTML files using multiple engines.
    
    Supports:
    - Playwright (Chromium) - Best quality, perfect rendering
    - WeasyPrint - Fallback option, pure Python
    """
    
    def __init__(self):
        """Initialize PDF Manager and detect available engines."""
        self.available_engines = self._detect_engines()
        self.preferred_engine = self._get_preferred_engine()
        
        logger.info(f"PDF Manager initialized with {len(self.available_engines)} available engines")
        logger.info(f"Preferred engine: {self.preferred_engine}")
    
    def _detect_engines(self) -> Dict[str, Dict]:
        """Detect which PDF engines are available."""
        engines = {}
        
        # Test Playwright
        try:
            from playwright.sync_api import sync_playwright
            engines['playwright'] = {
                'available': True,
                'description': 'Real browser engine (Chromium), perfect rendering',
                'quality': 'excellent',
                'speed': 'fast'
            }
        except ImportError:
            engines['playwright'] = {
                'available': False,
                'error': 'Not installed. Install with: pip install playwright && playwright install chromium'
            }
        
        # Test WeasyPrint
        try:
            from weasyprint import HTML, CSS
            engines['weasyprint'] = {
                'available': True,
                'description': 'Pure Python, good CSS support with limitations',
                'quality': 'good',
                'speed': 'medium'
            }
        except ImportError:
            engines['weasyprint'] = {
                'available': False,
                'error': 'Not installed. Install with: pip install weasyprint'
            }
        
        return engines
    
    def _get_preferred_engine(self) -> Optional[str]:
        """Get the best available engine."""
        # Priority order (best to worst)
        priority = ['playwright', 'weasyprint']
        
        for engine in priority:
            if self.available_engines.get(engine, {}).get('available', False):
                return engine
        
        return None
    
    def get_engine_info(self) -> Dict:
        """Get information about available engines."""
        return {
            'available_engines': self.available_engines,
            'preferred_engine': self.preferred_engine,
            'total_available': len([e for e in self.available_engines.values() if e.get('available', False)])
        }
    
    def convert_html_to_pdf(
        self, 
        html_file: Union[str, Path], 
        output_path: Optional[Union[str, Path]] = None,
        engine: Optional[str] = None,
        options: Optional[Dict] = None
    ) -> Dict:
        """
        Convert a single HTML file to PDF.
        
        Args:
            html_file: Path to HTML file to convert
            output_path: Output PDF path (defaults to same location as HTML with .pdf extension)
            engine: Specific engine to use (defaults to preferred engine)
            options: Engine-specific options
        
        Returns:
            Dict with conversion results
        """
        html_file = Path(html_file)
        
        if not html_file.exists():
            return {
                'success': False,
                'error': f'HTML file not found: {html_file}',
                'file': str(html_file)
            }
        
        # Determine output path
        if output_path is None:
            output_path = html_file.parent / f"{html_file.stem}.pdf"
        else:
            output_path = Path(output_path)
        
        # Determine engine to use
        if engine is None:
            engine = self.preferred_engine
        
        if engine is None:
            return {
                'success': False,
                'error': 'No PDF engines available. Please install Playwright or WeasyPrint.',
                'file': str(html_file)
            }
        
        if not self.available_engines.get(engine, {}).get('available', False):
            return {
                'success': False,
                'error': f'Engine {engine} not available: {self.available_engines.get(engine, {}).get("error", "Unknown error")}',
                'file': str(html_file)
            }
        
        # Set default options
        if options is None:
            options = {}
        
        logger.info(f"Converting {html_file.name} to PDF using {engine}")
        
        try:
            if engine == 'playwright':
                return self._convert_with_playwright(html_file, output_path, options)
            elif engine == 'weasyprint':
                return self._convert_with_weasyprint(html_file, output_path, options)
            else:
                return {
                    'success': False,
                    'error': f'Unknown engine: {engine}',
                    'file': str(html_file)
                }
        
        except Exception as e:
            logger.error(f"Error converting {html_file.name}: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': f'Conversion failed: {str(e)}',
                'file': str(html_file)
            }
    
    def _convert_with_playwright(self, html_file: Path, output_path: Path, options: Dict) -> Dict:
        """Convert HTML to PDF using Playwright."""
        from playwright.sync_api import sync_playwright
        
        # Default Playwright options
        default_options = {
            'format': 'Letter',
            'margin': {
                'top': '0.5in',
                'right': '0.5in',
                'bottom': '0.5in',
                'left': '0.5in'
            },
            'print_background': True,
            'scale': 0.75  # 75% scaling
        }
        
        # Merge with user options
        pdf_options = {**default_options, **options}
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            try:
                # Read HTML content and fix CSS paths
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Fix CSS path to absolute path
                css_path = html_file.parent.parent / 'css' / 'styles.css'
                if css_path.exists():
                    html_content = html_content.replace(
                        'href="../../css/styles.css"',
                        f'href="file://{css_path.absolute()}"'
                    )
                
                # Create temporary HTML file with fixed paths
                temp_html = html_file.parent / f"temp_{html_file.name}"
                with open(temp_html, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                try:
                    # Navigate to the HTML file
                    page.goto(f"file://{temp_html.absolute()}")
                    
                    # Wait for page to load completely
                    page.wait_for_load_state('networkidle')
                    
                    # Ensure output directory exists
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Generate PDF
                    page.pdf(path=str(output_path), **pdf_options)
                    
                    logger.info(f"Successfully converted {html_file.name} to {output_path.name}")
                    
                    return {
                        'success': True,
                        'file': str(html_file),
                        'output': str(output_path),
                        'engine': 'playwright',
                        'size_bytes': output_path.stat().st_size if output_path.exists() else 0
                    }
                
                finally:
                    # Clean up temporary file
                    if temp_html.exists():
                        temp_html.unlink()
            
            finally:
                browser.close()
    
    def _convert_with_weasyprint(self, html_file: Path, output_path: Path, options: Dict) -> Dict:
        """Convert HTML to PDF using WeasyPrint."""
        from weasyprint import HTML, CSS
        
        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Create HTML object
        html_doc = HTML(string=html_content, base_url=str(html_file.parent))
        
        # Handle CSS for WeasyPrint compatibility
        stylesheets = []
        css_path = html_file.parent.parent / 'css' / 'styles.css'
        
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Remove problematic properties for WeasyPrint
            css_content = re.sub(r'box-shadow:[^;]+;', '', css_content)
            css_content = css_content.replace(
                '@media (max-width: 520px)', 
                '@media screen and (max-width: 520px)'
            )
            
            # Add 75% scaling for print
            weasyprint_css = css_content + """
            @media print {
                * { box-shadow: none !important; }
                html { font-size: 12px; }
                body { font-size: 0.75em; line-height: 1.2; }
                .both_h1 { font-size: 27pt !important; }
                .resume_h2 { font-size: 9.75pt !important; }
                .both_container { 
                    max-width: none !important; 
                    margin: 0 !important; 
                    padding: 15px !important; 
                    background: white !important; 
                }
            }
            """
            
            # Remove CSS link from HTML and use our modified CSS
            html_content_no_css = html_content.replace(
                '<link rel="stylesheet" href="../../css/styles.css" />',
                ''
            ).replace(
                '<link rel="stylesheet" href="../../css/styles.css"/>',
                ''
            )
            
            html_doc = HTML(string=html_content_no_css, base_url=str(html_file.parent))
            stylesheets.append(CSS(string=weasyprint_css))
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to PDF
        html_doc.write_pdf(
            str(output_path),
            stylesheets=stylesheets,
            presentational_hints=True,
            optimize_images=True
        )
        
        logger.info(f"Successfully converted {html_file.name} to {output_path.name}")
        
        return {
            'success': True,
            'file': str(html_file),
            'output': str(output_path),
            'engine': 'weasyprint',
            'size_bytes': output_path.stat().st_size if output_path.exists() else 0
        }
    
    def convert_multiple_files(
        self,
        html_files: List[Union[str, Path]],
        output_dir: Optional[Union[str, Path]] = None,
        engine: Optional[str] = None,
        options: Optional[Dict] = None
    ) -> Dict:
        """
        Convert multiple HTML files to PDF.
        
        Args:
            html_files: List of HTML file paths to convert
            output_dir: Output directory for PDFs (defaults to same location as each HTML file)
            engine: Specific engine to use (defaults to preferred engine)
            options: Engine-specific options
        
        Returns:
            Dict with batch conversion results
        """
        if not html_files:
            return {
                'success': True,
                'message': 'No files to convert',
                'converted': 0,
                'failed': 0,
                'results': []
            }
        
        logger.info(f"Starting batch conversion of {len(html_files)} files")
        
        results = []
        converted_count = 0
        failed_count = 0
        
        for html_file in html_files:
            html_file = Path(html_file)
            
            # Determine output path
            if output_dir:
                output_path = Path(output_dir) / f"{html_file.stem}.pdf"
            else:
                output_path = None  # Will default to same location as HTML file
            
            # Convert file
            result = self.convert_html_to_pdf(html_file, output_path, engine, options)
            results.append(result)
            
            if result['success']:
                converted_count += 1
            else:
                failed_count += 1
                logger.error(f"Failed to convert {html_file.name}: {result.get('error', 'Unknown error')}")
        
        success = failed_count == 0
        message = f"Converted {converted_count} files to PDF"
        if failed_count > 0:
            message += f", {failed_count} failed"
        
        logger.info(f"Batch conversion completed: {message}")
        
        return {
            'success': success,
            'message': message,
            'converted': converted_count,
            'failed': failed_count,
            'results': results,
            'engine_used': engine or self.preferred_engine
        }
    
    def find_html_files(
        self,
        directory: Union[str, Path],
        job_id: Optional[str] = None,
        file_types: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Find HTML files in a directory structure.
        
        Args:
            directory: Directory to search in
            job_id: Specific job ID to filter by
            file_types: File types to include (e.g., ['resume', 'coverletter'])
        
        Returns:
            List of HTML file paths
        """
        directory = Path(directory)
        
        if not directory.exists():
            logger.warning(f"Directory not found: {directory}")
            return []
        
        if file_types is None:
            file_types = ['resume', 'coverletter']
        
        html_files = []
        
        # Search in subdirectories (bundled jobs)
        for job_folder in directory.iterdir():
            if job_folder.is_dir():
                for html_file in job_folder.glob('*.html'):
                    # Check job ID filter
                    if job_id:
                        filename_parts = html_file.stem.split('.')
                        if len(filename_parts) >= 2 and filename_parts[1] != job_id:
                            continue
                    
                    # Check file type filter
                    if any(file_type in html_file.name.lower() for file_type in file_types):
                        html_files.append(html_file)
        
        logger.info(f"Found {len(html_files)} HTML files in {directory}")
        return html_files


# Convenience functions for backward compatibility
def print_pdf(job_id: str = None, output_dir: str = None) -> Dict:
    """
    Legacy function for backward compatibility with step2_generate.py
    
    Args:
        job_id: Specific job ID to convert
        output_dir: Output directory for PDFs
    
    Returns:
        Dict with conversion results
    """
    pdf_manager = PDFManager()
    
    # Get jobs directory
    jobs_dir = Path(__file__).parent / 'jobs' / '2_generated'
    
    if not jobs_dir.exists():
        return {
            'success': False,
            'error': 'No generated jobs directory found',
            'converted': 0,
            'failed': 0
        }
    
    # Find HTML files
    html_files = pdf_manager.find_html_files(jobs_dir, job_id)
    
    if not html_files:
        return {
            'success': True,
            'message': 'No HTML files found to convert',
            'converted': 0,
            'failed': 0
        }
    
    # Convert files
    result = pdf_manager.convert_multiple_files(html_files, output_dir)
    
    # Format result for backward compatibility
    return {
        'success': result['success'],
        'message': result['message'],
        'converted': result['converted'],
        'failed': result['failed'],
        'results': result['results'],
        'library_used': result['engine_used']
    }


if __name__ == '__main__':
    # Test the PDF manager
    pdf_manager = PDFManager()
    info = pdf_manager.get_engine_info()
    
    print("PDF Manager Test")
    print("=" * 50)
    print(f"Available engines: {info['total_available']}")
    print(f"Preferred engine: {info['preferred_engine']}")
    
    for engine, details in info['available_engines'].items():
        status = "✅" if details.get('available', False) else "❌"
        print(f"{status} {engine.upper()}: {details.get('description', details.get('error', 'Unknown'))}")
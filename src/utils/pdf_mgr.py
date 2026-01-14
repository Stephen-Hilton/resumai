#!/usr/bin/env python3
"""
PDF Manager - Handles HTML to PDF conversion using WeasyPrint.

This module provides a unified interface for converting HTML files to PDF
using WeasyPrint with proper scaling and no external dependencies.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union

# Handle logging_setup import for different contexts
try:
    from . import logging_setup
except ImportError:
    import logging_setup

# Set up logger for this module
logger = logging_setup.get_logger(__name__)


class PDFManager:
    """
    Manages PDF conversion from HTML files using WeasyPrint.
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
        
        # Test WeasyPrint only
        try:
            # Try to fix library path issues on macOS
            import os
            import platform
            if platform.system() == 'Darwin':  # macOS
                # Add Homebrew library paths
                dyld_path = os.environ.get('DYLD_LIBRARY_PATH', '')
                homebrew_lib = '/opt/homebrew/lib'
                if homebrew_lib not in dyld_path:
                    os.environ['DYLD_LIBRARY_PATH'] = f"{homebrew_lib}:{dyld_path}"
                
                # Also try DYLD_FALLBACK_LIBRARY_PATH
                fallback_path = os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')
                if homebrew_lib not in fallback_path:
                    os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = f"{homebrew_lib}:{fallback_path}"
            
            from weasyprint import HTML, CSS
            # Test actual functionality with a simple HTML string to catch runtime errors
            import io
            test_html = HTML(string='<html><body><p>Test</p></body></html>')
            # Try to actually render to catch system dependency issues
            try:
                pdf_bytes = test_html.write_pdf()
                engines['weasyprint'] = {
                    'available': True,
                    'description': 'Pure Python, good CSS support with limitations',
                    'quality': 'good',
                    'speed': 'medium'
                }
            except Exception as render_error:
                # Handle system library issues during rendering
                error_msg = str(render_error).lower()
                if any(lib in error_msg for lib in ['libgobject', 'cairo', 'pango', 'glib', 'fontconfig']):
                    engines['weasyprint'] = {
                        'available': False,
                        'error': 'System dependencies missing. On macOS, install with: brew install cairo pango gdk-pixbuf libffi'
                    }
                else:
                    engines['weasyprint'] = {
                        'available': False,
                        'error': f'Runtime error: {str(render_error)}'
                    }
        except ImportError:
            engines['weasyprint'] = {
                'available': False,
                'error': 'Not installed. Install with: pip install weasyprint'
            }
        except Exception as e:
            # Handle import-time system library issues
            error_msg = str(e).lower()
            if any(lib in error_msg for lib in ['libgobject', 'cairo', 'pango', 'glib', 'fontconfig']):
                engines['weasyprint'] = {
                    'available': False,
                    'error': 'System dependencies missing. On macOS, install with: brew install cairo pango gdk-pixbuf libffi'
                }
            else:
                engines['weasyprint'] = {
                    'available': False,
                    'error': f'Initialization error: {str(e)}'
                }
        
        return engines
    
    def _get_preferred_engine(self) -> Optional[str]:
        """Get the best available engine."""
        # Only WeasyPrint
        if self.available_engines.get('weasyprint', {}).get('available', False):
            return 'weasyprint'
        
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
                'error': 'No PDF engines available. Please install WeasyPrint.',
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
            if engine == 'weasyprint':
                return self._convert_with_weasyprint(html_file, output_path, options)
            else:
                return {
                    'success': False,
                    'error': f'Unknown engine: {engine}. Only WeasyPrint is supported.',
                    'file': str(html_file)
                }
        
        except Exception as e:
            logger.error(f"Error converting {html_file.name}: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': f'Conversion failed: {str(e)}',
                'file': str(html_file)
            }
    
    def _convert_with_weasyprint(self, html_file: Path, output_path: Path, options: Dict) -> Dict:
        """Convert HTML to PDF using WeasyPrint."""
        try:
            from weasyprint import HTML, CSS
        except ImportError as e:
            return {
                'success': False,
                'error': f'WeasyPrint not available: {str(e)}',
                'file': str(html_file)
            }
        except Exception as e:
            # Handle system library issues (common on macOS)
            if 'libgobject' in str(e) or 'cairo' in str(e) or 'pango' in str(e):
                return {
                    'success': False,
                    'error': f'WeasyPrint system dependencies missing. On macOS, install with: brew install cairo pango gdk-pixbuf libffi',
                    'file': str(html_file)
                }
            else:
                return {
                    'success': False,
                    'error': f'WeasyPrint initialization error: {str(e)}',
                    'file': str(html_file)
                }
        
        try:
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Remove CSS link from HTML completely to avoid external dependency issues
            import re
            html_content_no_css = re.sub(
                r'<link[^>]*href=["\'][^"\']*styles\.css["\'][^>]*/?>', 
                '', 
                html_content, 
                flags=re.IGNORECASE
            )
            
            # Fix SVG icon paths - convert web server paths to absolute paths
            # The HTML files use /resumes/icons/ paths for web serving
            icons_dir = Path(__file__).parent.parent / 'resources' / 'icons'
            if icons_dir.exists():
                # Replace web server SVG paths with absolute file:// URLs
                # Handle both /resumes/icons/ and /icons/ patterns
                html_content_no_css = re.sub(
                    r'src="\/resumes\/icons\/([^"]+\.svg)"',
                    lambda m: f'src="file://{icons_dir.absolute()}/{m.group(1)}"',
                    html_content_no_css
                )
                html_content_no_css = re.sub(
                    r'src="\/icons\/([^"]+\.svg)"',
                    lambda m: f'src="file://{icons_dir.absolute()}/{m.group(1)}"',
                    html_content_no_css
                )
                logger.info(f"Updated SVG icon paths to use absolute file:// URLs from {icons_dir}")
            else:
                logger.warning(f"Icons directory not found: {icons_dir}")
            
            # Create clean CSS without external dependencies, scaled down by 70%
            # Get absolute path to Material Symbols font
            font_dir = Path(__file__).parent.parent / 'resources' / 'fonts'
            material_font_path = font_dir / 'MaterialSymbolsOutlined.woff2'
            
            clean_css = f"""
            /* Clean CSS for PDF generation without external dependencies */
            
            /* Load Material Icons font locally */
            @font-face {{
                font-family: 'Material Symbols Outlined';
                src: url('file://{material_font_path.absolute()}') format('woff2');
                font-weight: normal;
                font-style: normal;
            }}
            
            @page {{
                size: A4;
                margin: 0.5in;
            }}
            
            body {{
                font-family: "Calibri", "Segoe UI", "Helvetica Neue", Arial, sans-serif !important;
                color: #222 !important; /* Consistent dark grey for all body text */
                margin: 0;
                padding: 0;
                background: white;
                font-size: 8.2pt !important;
                line-height: 1.3;
            }}
            
            .both_container {{
                max-width: none;
                margin: 0;
                background: white;
                padding: 8px 16px !important;
            }}
            
            .both_header {{
                border-bottom: 1px solid #e6e6e6;
                padding-bottom: 4px !important;
                margin-bottom: 6px !important;
                display: flex;
                justify-content: space-between;
                align-items: stretch !important; /* Make both sides same height */
                min-height: 50px !important; /* Taller to accommodate contact info */
            }}
            
            .both_header_left {{
                flex: 3;
                display: flex;
                align-items: center;
                justify-content: center;
                border-right: 1px solid #e6e6e6;
                padding-right: 8px;
            }}
            
            .both_header_right {{
                flex: 1;
                text-align: left !important; /* Change from right to left alignment */
                padding-left: 10px;
                display: flex;
                align-items: flex-start !important; /* Align to top instead of center */
                justify-content: flex-start !important; /* Align to left instead of flex-end */
            }}
            
            .both_h1 {{
                margin: 0;
                font-size: 24pt !important; /* Even smaller */
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                font-weight: bold;
                color: #1e3a8a;
                letter-spacing: 0.1px;
                text-align: center;
                width: 100%;
                line-height: 0.95;
            }}
            
            .both_meta {{
                font-size: 5.8pt !important; /* Smaller to match tighter spacing */
                color: #222 !important;
                line-height: 0.6 !important; /* Very tight line height to match HTML */
                text-align: left !important; /* Ensure left alignment */
            }}
            
            .both_meta_line {{
                margin-bottom: -4px !important; /* Even more negative margin for very tight spacing */
                display: block !important;
                line-height: 0.6 !important; /* Very tight line height to match HTML */
                white-space: nowrap;
            }}
            
            /* Style the contact icons - handle both Material Icons and local SVGs */
            .both_contact_icon {{
                width: 8px; /* Much smaller icons to match HTML */
                height: 8px; /* Much smaller icons to match HTML */
                display: inline-block !important;
                vertical-align: middle !important;
                font-size: 6px !important; /* Much smaller font for icons */
                color: #222 !important;
                line-height: 1 !important;
                margin-right: 2px !important; /* Very small margin */
            }}
            
            /* Style for local SVG images - SHOW them in PDF */
            .both_contact_icon img {{
                width: 8px !important; /* Much smaller SVG icons to match HTML */
                height: 8px !important; /* Much smaller SVG icons to match HTML */
                object-fit: contain;
                display: inline-block !important;
                vertical-align: middle !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            
            /* Hide Material Icons fallback */
            .both_contact_icon .material-symbols-outlined {{
                display: none !important;
            }}
            
            /* Hide Unicode fallback symbols when SVG images are present */
            .both_contact_icon::after {{
                display: none !important;
            }}
            
            .both_section {{
                margin-top: 6px !important; /* Slightly increased for better section separation */
            }}
            
            .both_muted, p, div, span {{
                color: #222 !important; /* Consistent dark grey */
                font-size: 8.2pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                font-weight: normal;
                line-height: 1.1;
                margin: 2px 0;
            }}
            
            /* Specific styles for body content paragraphs (NOT contact section) */
            .both_section p, 
            .both_section div:not(.both_meta):not(.both_meta_line):not(.both_contact_icon),
            .both_section span:not(.both_contact_icon) {{
                line-height: 1.3 !important; /* Increased spacing for body content only */
                margin: 3px 0 !important; /* Slightly more margin for body content */
            }}
            
            .resume_h2, .both_h2 {{
                font-size: 10.2pt !important; /* Slightly smaller */
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                font-weight: bold;
                margin: 3px 0; /* Even smaller */
                color: #1e3a8a;
            }}
            
            .resume_company {{
                font-weight: 600;
                color: #222 !important; /* Consistent dark grey */
                font-size: 9.8pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                line-height: 1.1;
                page-break-after: avoid;
                margin: 1px 0;
            }}
            
            .resume_role {{
                font-weight: 600;
                color: #222 !important; /* Consistent dark grey */
                font-size: 8.2pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                margin-left: 2ch;
                line-height: 1.1;
                page-break-after: avoid;
                page-break-inside: avoid;
                margin-top: 1px;
                margin-bottom: 1px;
            }}
            
            .resume_ul {{
                margin: 1px 0 2px 4ch !important; /* Very tight */
                padding: 0;
                page-break-before: avoid;
            }}
            
            .resume_li, li {{
                margin-bottom: 1px !important; /* Slightly increased for body content */
                line-height: 1.25 !important; /* Slightly increased for body content */
                font-size: 8.2pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                color: #222 !important; /* Consistent dark grey */
            }}
            
            .resume_role_meta {{
                font-size: 8.2pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                color: #222 !important; /* Consistent dark grey */
                margin-bottom: 1px;
                page-break-before: avoid;
            }}
            
            .resume_company + .resume_role_meta {{
                margin-left: 0;
            }}
            
            .resume_role + .resume_role_meta {{
                margin-left: 2ch;
            }}
            
            .resume_skills {{
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 8px; /* Even smaller gap */
                margin-top: 2px; /* Very small */
                margin-left: 2ch;
                margin-right: 2ch;
            }}
            
            .resume_skill_item {{
                font-size: 8.2pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                color: #222 !important; /* Consistent dark grey */
                margin-bottom: 0px !important;
                line-height: 1.0;
            }}
            
            .resume_experience_item {{
                margin-bottom: 6px; /* Even smaller */
                page-break-inside: avoid;
            }}
            
            .cover_p {{
                color: #222 !important; /* Consistent dark grey */
                line-height: 1.2;
                margin: 8px 0; /* Increased margin for better spacing */
                font-size: 8.2pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
            }}
            
            /* Handle <br> tags in cover letters for PDF */
            .cover_letter_body br {{
                display: block;
                margin: 6px 0; /* Visible line break in PDF */
                content: "";
            }}
            
            /* Cover letter spacing divs */
            .cover_letter_body div[style*="margin-bottom: 30px"] {{
                margin-bottom: 20px !important; /* Two newlines equivalent in PDF */
            }}
            
            .cover_letter_body div[style*="margin-bottom: 15px"] {{
                margin-bottom: 10px !important; /* Single newline equivalent in PDF */
            }}
            
            .cover_ul {{
                margin: 1px 0 2px 13px;
                padding: 0;
                color: #222 !important; /* Consistent dark grey */
            }}
            
            .cover_li {{
                margin-bottom: 0px !important;
                font-size: 8.2pt !important;
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                color: #222 !important; /* Consistent dark grey */
            }}
            
            .both_link {{
                color: #0366d6 !important;
                text-decoration: none;
                font-size: 5.8pt !important; /* Match meta font size */
                font-family: "Calibri", "Segoe UI", Arial, sans-serif !important;
                display: inline !important;
                vertical-align: middle !important;
                white-space: nowrap;
            }}
            
            .both_bold {{
                font-weight: 600;
                color: #222 !important; /* Consistent dark grey */
            }}
            
            /* Version info styling */
            .version-info {{
                position: absolute;
                top: 5px;
                right: 5px;
                font-size: 6pt !important;
                color: #999;
                font-family: Arial, sans-serif;
            }}
            
            .version-footer {{
                text-align: center;
                font-size: 6pt !important;
                color: #999;
                margin-top: 20px;
                font-family: Arial, sans-serif;
            }}
            """
            
            logger.info("Using clean CSS without external dependencies for PDF generation - SPACING FIX APPLIED")
            
            # Create HTML object with clean content
            html_doc = HTML(string=html_content_no_css, base_url=str(html_file.parent))
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to PDF
            html_doc.write_pdf(
                str(output_path),
                stylesheets=[CSS(string=clean_css)],
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
            
        except Exception as e:
            # Handle runtime errors during conversion
            if 'libgobject' in str(e) or 'cairo' in str(e) or 'pango' in str(e):
                return {
                    'success': False,
                    'error': f'WeasyPrint system dependencies missing. On macOS, install with: brew install cairo pango gdk-pixbuf libffi',
                    'file': str(html_file)
                }
            else:
                return {
                    'success': False,
                    'error': f'WeasyPrint conversion failed: {str(e)}',
                    'file': str(html_file)
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
from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.pdf_generator import generate_pdf, is_playwright_available
from src.events._db_helpers import get_job_id_from_path
from src.services.file_storage_service import FileStorageService


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Generate cover letter PDF from coverletter.html.
    
    The generated PDF is stored using FileStorageService in the database-centric
    file management system with file_purpose='coverletter_pdf' and file_source='generated'.
    """
    try:
        # Check Playwright is available
        if not is_playwright_available():
            return EventResult(
                ok=False,
                job_path=job_path,
                message="Playwright not installed",
                errors=[{"error": "Run: pip install playwright && playwright install chromium"}]
            )
        
        # Get job_id from job_path for database-centric storage
        job_id = get_job_id_from_path(job_path)
        
        # Determine HTML path - from FileStorageService if job_id available, else from job_path
        html_path = None
        file_service = None
        if job_id:
            try:
                file_service = FileStorageService()
                html_path = file_service.get_file_path(job_id, "coverletter_html")
            except Exception:
                # Database table may not exist, fall back to filesystem
                job_id = None
                html_path = None
        
        # Fallback to job_path if no database record found
        if not html_path:
            html_path = job_path / "coverletter.html"
        
        # Check that coverletter.html exists
        if not html_path.exists():
            return EventResult(
                ok=False,
                job_path=job_path,
                message="coverletter.html not found",
                errors=[{"error": "coverletter.html missing - run gen_coverletter_html first"}]
            )
        
        if job_id:
            # Database-centric storage: generate PDF to temp location, then store via FileStorageService
            import tempfile
            
            # Generate PDF to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                temp_pdf_path = Path(tmp_file.name)
            
            try:
                success, error = await generate_pdf(html_path, temp_pdf_path)
                
                if not success:
                    # Clean up temp file on failure
                    if temp_pdf_path.exists():
                        temp_pdf_path.unlink()
                    return EventResult(
                        ok=False,
                        job_path=job_path,
                        message=error,
                        errors=[{"error": error}]
                    )
                
                # Read the generated PDF content
                pdf_content = temp_pdf_path.read_bytes()
                
                # Store using FileStorageService
                if file_service is None:
                    file_service = FileStorageService()
                job_file = file_service.store_file(
                    job_id=job_id,
                    content=pdf_content,
                    file_purpose="coverletter_pdf",
                    file_source="generated",
                    extension="pdf"
                )
                
                return EventResult(
                    ok=True,
                    job_path=job_path,
                    message=f"Generated coverletter.pdf, stored at {job_file.file_path}",
                    artifacts=[job_file.file_path]
                )
            finally:
                # Clean up temp file
                if temp_pdf_path.exists():
                    temp_pdf_path.unlink()
        else:
            # Fallback: Legacy behavior when DB not enabled
            pdf_path = job_path / "coverletter.pdf"
            success, error = await generate_pdf(html_path, pdf_path)
            
            if not success:
                return EventResult(
                    ok=False,
                    job_path=job_path,
                    message=error,
                    errors=[{"error": error}]
                )
            
            return EventResult(
                ok=True,
                job_path=job_path,
                message="Generated coverletter.pdf",
                artifacts=[str(pdf_path)]
            )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to generate cover letter PDF: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not is_playwright_available():
        return EventResult(ok=False, job_path=job_path, message="Playwright not installed")
    
    # Get job_id from job_path for database-centric storage
    job_id = get_job_id_from_path(job_path)
    
    # Determine HTML path - from FileStorageService if job_id available, else from job_path
    html_path = None
    if job_id:
        try:
            file_service = FileStorageService()
            html_path = file_service.get_file_path(job_id, "coverletter_html")
        except Exception:
            # Database table may not exist, fall back to filesystem
            html_path = None
    
    # Fallback to job_path if no database record found
    if not html_path:
        html_path = job_path / "coverletter.html"
    
    if not html_path.exists():
        return EventResult(ok=False, job_path=job_path, message="coverletter.html not found")
    
    return EventResult(ok=True, job_path=job_path, message="Test: would generate coverletter.pdf")

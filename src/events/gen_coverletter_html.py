from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.html_generator import generate_coverletter_html
from src.lib.shared_css import ensure_shared_css_exists
from src.events._db_helpers import get_job_id_from_path
from src.services.file_storage_service import FileStorageService


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Generate cover letter HTML from subcontent.coverletter.yaml.
    
    CSS files are stored in a shared location (src/templates/css/) to avoid duplication.
    
    The generated HTML is stored using FileStorageService in the database-centric
    file management system with file_purpose='coverletter_html' and file_source='generated'.
    """
    try:
        # Check that coverletter subcontent exists
        coverletter_file = job_path / "subcontent.coverletter.yaml"
        if not coverletter_file.exists():
            return EventResult(
                ok=False,
                job_path=job_path,
                message="subcontent.coverletter.yaml not found",
                errors=[{"error": "coverletter subcontent missing"}]
            )
        
        # Ensure shared CSS directory exists
        css_dir = ensure_shared_css_exists()
        
        # Generate HTML (references shared CSS)
        html_content = generate_coverletter_html(job_path)
        
        # Get job_id from job_path for database-centric storage
        job_id = get_job_id_from_path(job_path)
        
        if job_id:
            # Store using FileStorageService for database-centric file management
            file_service = FileStorageService()
            job_file = file_service.store_file(
                job_id=job_id,
                content=html_content,
                file_purpose="coverletter_html",
                file_source="generated",
                extension="html"
            )
            
            return EventResult(
                ok=True,
                job_path=job_path,
                message=f"Generated coverletter.html (using shared CSS at {css_dir}), stored at {job_file.file_path}",
                artifacts=[job_file.file_path]
            )
        else:
            # Fallback: Write HTML file to job_path (legacy behavior when DB not enabled)
            html_path = job_path / "coverletter.html"
            html_path.write_text(html_content)
            
            return EventResult(
                ok=True,
                job_path=job_path,
                message=f"Generated coverletter.html (using shared CSS at {css_dir})",
                artifacts=[str(html_path)]
            )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to generate cover letter HTML: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate coverletter subcontent file exists."""
    coverletter_file = job_path / "subcontent.coverletter.yaml"
    if not coverletter_file.exists():
        return EventResult(ok=False, job_path=job_path, message="subcontent.coverletter.yaml not found")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate coverletter.html")

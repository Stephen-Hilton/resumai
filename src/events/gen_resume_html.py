from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.html_generator import generate_resume_html
from src.lib.shared_css import ensure_shared_css_exists
from src.events._db_helpers import get_job_id_from_path
from src.services.file_storage_service import FileStorageService


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Generate resume HTML from subcontent files.
    
    Validates all subcontent files exist and creates resume.html.
    CSS files are stored in a shared location (src/templates/css/) to avoid duplication.
    
    The generated HTML is stored using FileStorageService in the database-centric
    file management system with file_purpose='resume_html' and file_source='generated'.
    """
    try:
        # Check that all required subcontent files exist
        required_sections = ["contacts", "summary", "skills", "experience", "education"]
        missing_sections = []
        
        for section in required_sections:
            subcontent_file = job_path / f"subcontent.{section}.yaml"
            if not subcontent_file.exists():
                missing_sections.append(section)
        
        if missing_sections:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Missing required subcontent files: {', '.join(missing_sections)}",
                errors=[{"missing_sections": missing_sections}]
            )
        
        # Ensure shared CSS directory exists (creates CSS files if needed)
        css_dir = ensure_shared_css_exists()
        
        # Generate HTML (references shared CSS)
        html_content = generate_resume_html(job_path)
        
        # Get job_id from job_path for database-centric storage
        job_id = get_job_id_from_path(job_path)
        
        if job_id:
            # Store using FileStorageService for database-centric file management
            file_service = FileStorageService()
            job_file = file_service.store_file(
                job_id=job_id,
                content=html_content,
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            return EventResult(
                ok=True,
                job_path=job_path,
                message=f"Generated resume.html (using shared CSS at {css_dir}), stored at {job_file.file_path}",
                artifacts=[job_file.file_path]
            )
        else:
            # Fallback: Write HTML file to job_path (legacy behavior when DB not enabled)
            html_path = job_path / "resume.html"
            html_path.write_text(html_content)
            
            return EventResult(
                ok=True,
                job_path=job_path,
                message=f"Generated resume.html (using shared CSS at {css_dir})",
                artifacts=[str(html_path)]
            )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to generate resume HTML: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate subcontent files exist."""
    required_sections = ["contacts", "summary", "skills", "experience", "education"]
    missing_sections = []
    
    for section in required_sections:
        subcontent_file = job_path / f"subcontent.{section}.yaml"
        if not subcontent_file.exists():
            missing_sections.append(section)
    
    if missing_sections:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Missing subcontent files: {', '.join(missing_sections)}"
        )
    
    return EventResult(ok=True, job_path=job_path, message="Test: would generate resume.html")

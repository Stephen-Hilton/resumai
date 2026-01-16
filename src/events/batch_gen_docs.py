from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events.event_bus import run_event
from src.events._helpers import move_job_to_phase


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Batch generate all documents (HTML and PDF) for a job.
    
    Executes in sequence:
    1. gen_resume_html
    2. gen_coverletter_html
    3. gen_resume_pdf
    4. gen_coverletter_pdf
    
    On success, moves job to 3_Docs_Generated.
    """
    try:
        artifacts = []
        
        # Step 1: Generate resume HTML
        result = await run_event("gen_resume_html", job_path, ctx)
        if not result.ok:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Failed to generate resume HTML: {result.message}",
                errors=result.errors
            )
        artifacts.extend(result.artifacts)
        
        # Step 2: Generate cover letter HTML
        result = await run_event("gen_coverletter_html", job_path, ctx)
        if not result.ok:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Failed to generate cover letter HTML: {result.message}",
                errors=result.errors
            )
        artifacts.extend(result.artifacts)
        
        # Step 3: Generate resume PDF
        result = await run_event("gen_resume_pdf", job_path, ctx)
        if not result.ok:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Failed to generate resume PDF: {result.message}",
                errors=result.errors
            )
        artifacts.extend(result.artifacts)
        
        # Step 4: Generate cover letter PDF
        result = await run_event("gen_coverletter_pdf", job_path, ctx)
        if not result.ok:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Failed to generate cover letter PDF: {result.message}",
                errors=result.errors
            )
        artifacts.extend(result.artifacts)
        
        # All documents generated successfully - move to 3_Docs_Generated
        try:
            new_path = move_job_to_phase(job_path, ctx.jobs_root, "3_Docs_Generated")
            
            return EventResult(
                ok=True,
                job_path=new_path,
                message="Successfully generated all documents (HTML and PDF)",
                artifacts=artifacts
            )
        except Exception as e:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Documents generated but couldn't move to 3_Docs_Generated: {str(e)}",
                errors=[{"move_error": str(e)}],
                artifacts=artifacts
            )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Batch document generation failed: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate subcontent files exist."""
    required_files = [
        "subcontent.contacts.yaml",
        "subcontent.summary.yaml",
        "subcontent.skills.yaml",
        "subcontent.experience.yaml",
        "subcontent.education.yaml",
        "subcontent.coverletter.yaml"
    ]
    
    missing_files = []
    for filename in required_files:
        if not (job_path / filename).exists():
            missing_files.append(filename)
    
    if missing_files:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Missing files: {', '.join(missing_files)}"
        )
    
    return EventResult(ok=True, job_path=job_path, message="Test: would generate all documents")

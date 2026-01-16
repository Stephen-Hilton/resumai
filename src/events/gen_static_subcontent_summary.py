from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Generate static summary subcontent from resume.yaml.
    
    Copies the summary section from resume.yaml verbatim to subcontent.summary.yaml.
    """
    try:
        # Load resume.yaml
        resume_path = ctx.resumes_root / ctx.default_resume
        if not resume_path.exists():
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Resume file not found: {resume_path}",
                errors=[{"error": f"Resume file not found: {resume_path}"}]
            )
        
        resume_data = load_yaml(resume_path)
        
        # Extract summary section
        summary = resume_data.get("summary", "")
        
        if not summary:
            # Create a template if summary doesn't exist
            summary = "Professional summary to be added."
        
        # Write to subcontent.summary.yaml
        output_path = job_path / "subcontent.summary.yaml"
        dump_yaml(output_path, {"summary": summary})
        
        return EventResult(
            ok=True,
            job_path=job_path,
            message="Generated static summary subcontent",
            artifacts=[str(output_path)]
        )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to generate summary subcontent: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate resume exists."""
    resume_path = ctx.resumes_root / ctx.default_resume
    if not resume_path.exists():
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Resume file not found: {resume_path}"
        )
    
    return EventResult(
        ok=True,
        job_path=job_path,
        message="Test: would generate summary"
    )

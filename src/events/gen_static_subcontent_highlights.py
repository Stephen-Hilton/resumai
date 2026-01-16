from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate static highlights subcontent from resume.yaml."""
    try:
        resume_path = ctx.resumes_root / ctx.default_resume
        if not resume_path.exists():
            return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {resume_path}", errors=[{"error": f"Resume file not found: {resume_path}"}])
        
        resume_data = load_yaml(resume_path)
        highlights = resume_data.get("highlights", [])
        
        if not highlights:
            # Create template highlights
            highlights = [
                "Key achievement or highlight",
                "Another significant accomplishment",
                "Notable contribution or result"
            ]
        
        output_path = job_path / "subcontent.highlights.yaml"
        dump_yaml(output_path, highlights)
        
        return EventResult(ok=True, job_path=job_path, message=f"Generated static highlights subcontent ({len(highlights)} highlights)", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed to generate highlights subcontent: {str(e)}", errors=[{"exception": str(e)}])


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    resume_path = ctx.resumes_root / ctx.default_resume
    if not resume_path.exists():
        return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {resume_path}")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate highlights")

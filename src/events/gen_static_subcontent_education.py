from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate static education subcontent from resume.yaml."""
    try:
        resume_path = ctx.resumes_root / ctx.default_resume
        if not resume_path.exists():
            return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {resume_path}", errors=[{"error": f"Resume file not found: {resume_path}"}])
        
        resume_data = load_yaml(resume_path)
        education = resume_data.get("education", [])
        
        if not education:
            education = [{"course": "Degree", "school": "University", "dates": "2020"}]
        
        output_path = job_path / "subcontent.education.yaml"
        dump_yaml(output_path, education)
        
        return EventResult(ok=True, job_path=job_path, message=f"Generated static education subcontent ({len(education)} entries)", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed to generate education subcontent: {str(e)}", errors=[{"exception": str(e)}])


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    resume_path = ctx.resumes_root / ctx.default_resume
    if not resume_path.exists():
        return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {resume_path}")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate education")

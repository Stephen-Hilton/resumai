from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import dump_yaml
from src.events._db_helpers import load_resume_data, save_subcontent_to_db


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate static awards subcontent from resume.yaml."""
    try:
        # Load resume data (from DB or filesystem)
        resume_data = load_resume_data(ctx.resumes_root, ctx.default_resume)

        if not resume_data:
            return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {ctx.default_resume}", errors=[{"error": f"Resume file not found: {ctx.default_resume}"}])

        awards = resume_data.get("awards_and_keynotes", [])

        if not awards:
            awards = [{"award": "Award Name", "dates": "2020"}]

        output_path = job_path / "subcontent.awards.yaml"
        dump_yaml(output_path, awards)

        # Sync to database if enabled
        save_subcontent_to_db(job_path, "awards", awards)

        return EventResult(ok=True, job_path=job_path, message=f"Generated static awards subcontent ({len(awards)} awards)", artifacts=[str(output_path)])

    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed to generate awards subcontent: {str(e)}", errors=[{"exception": str(e)}])


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    resume_path = ctx.resumes_root / ctx.default_resume
    if not resume_path.exists():
        return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {resume_path}")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate awards")

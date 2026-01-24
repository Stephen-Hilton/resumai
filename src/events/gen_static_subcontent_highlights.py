from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import dump_yaml
from src.events._db_helpers import load_resume_data, save_subcontent_to_db


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate static highlights subcontent from resume.yaml."""
    try:
        # Load resume data (from DB or filesystem)
        resume_data = load_resume_data(ctx.resumes_root, ctx.default_resume)

        if not resume_data:
            return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {ctx.default_resume}", errors=[{"error": f"Resume file not found: {ctx.default_resume}"}])

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

        # Sync to database if enabled
        save_subcontent_to_db(job_path, "highlights", highlights)

        return EventResult(ok=True, job_path=job_path, message=f"Generated static highlights subcontent ({len(highlights)} highlights)", artifacts=[str(output_path)])

    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed to generate highlights subcontent: {str(e)}", errors=[{"exception": str(e)}])


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    resume_path = ctx.resumes_root / ctx.default_resume
    if not resume_path.exists():
        return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {resume_path}")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate highlights")

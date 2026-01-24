from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import dump_yaml
from src.events._db_helpers import load_resume_data, save_subcontent_to_db


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Generate static contacts subcontent from resume.yaml.

    Copies the contacts section from resume.yaml verbatim to subcontent.contacts.yaml.
    """
    try:
        # Load resume data (from DB or filesystem)
        resume_data = load_resume_data(ctx.resumes_root, ctx.default_resume)

        if not resume_data:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Resume file not found: {ctx.default_resume}",
                errors=[{"error": f"Resume file not found: {ctx.default_resume}"}]
            )

        # Extract contacts section
        contacts = resume_data.get("contacts", [])

        if not contacts:
            return EventResult(
                ok=False,
                job_path=job_path,
                message="No contacts section found in resume.yaml",
                errors=[{"error": "contacts section missing from resume"}]
            )

        # Write to subcontent.contacts.yaml
        output_path = job_path / "subcontent.contacts.yaml"
        dump_yaml(output_path, contacts)

        # Sync to database if enabled
        save_subcontent_to_db(job_path, "contacts", contacts)

        return EventResult(
            ok=True,
            job_path=job_path,
            message=f"Generated static contacts subcontent ({len(contacts)} contacts)",
            artifacts=[str(output_path)]
        )

    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to generate contacts subcontent: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate resume exists and has contacts."""
    resume_path = ctx.resumes_root / ctx.default_resume
    if not resume_path.exists():
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Resume file not found: {resume_path}"
        )
    
    try:
        resume_data = load_yaml(resume_path)
        contacts = resume_data.get("contacts", [])
        
        if not contacts:
            return EventResult(
                ok=False,
                job_path=job_path,
                message="No contacts section found in resume.yaml"
            )
        
        return EventResult(
            ok=True,
            job_path=job_path,
            message=f"Test: would generate {len(contacts)} contacts"
        )
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Test failed: {str(e)}"
        )

from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events._helpers import move_job_to_phase, append

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    # Safety check: prevent moving the jobs root directory
    if job_path == ctx.jobs_root or job_path.name == "jobs":
        return EventResult(
            ok=False,
            job_path=job_path,
            message="Cannot move jobs root directory - invalid job path provided"
        )

    # Safety check: ensure job_path is actually a job folder (should be inside a phase folder)
    if not job_path.parent.parent == ctx.jobs_root:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Invalid job path structure: {job_path}"
        )

    # Skip if already in Errored phase (prevents infinite loop)
    current_phase = job_path.parent.name
    if current_phase == "Errored":
        return EventResult(ok=True, job_path=job_path, message="already in Errored phase")

    new_path = move_job_to_phase(job_path, ctx.jobs_root, "Errored")
    append(new_path, "move_errored: moved to Errored")
    return EventResult(ok=True, job_path=new_path, message="moved")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

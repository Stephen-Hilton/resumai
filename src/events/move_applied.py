from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events._helpers import move_job_to_phase, append

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    new_path = move_job_to_phase(job_path, ctx.jobs_root, "4_Applied")
    append(new_path, "move_applied: moved to 4_Applied")
    return EventResult(ok=True, job_path=new_path, message="moved")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

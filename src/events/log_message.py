from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.logging_utils import append_job_log

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    message = ctx.state.get("message", "")
    append_job_log(job_path, message)
    return EventResult(ok=True, job_path=job_path, message="logged")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    # Non-destructive: do not write
    return EventResult(ok=True, job_path=job_path, message="test ok")

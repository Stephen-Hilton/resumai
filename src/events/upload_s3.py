from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=False, job_path=job_path, message="upload_s3 not implemented (future)")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

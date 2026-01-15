from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events.log_message import execute as log_execute

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    # UI reads app notifications from ctx.state['notifications'] list
    message = ctx.state.get("message", "")
    ctx.state.setdefault("notifications", []).append({"job": job_path.name, "message": message})
    await log_execute(job_path, ctx)
    return EventResult(ok=True, job_path=job_path, message="notified")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

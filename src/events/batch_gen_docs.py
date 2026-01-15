from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events.event_bus import run_event
from src.lib.logging_utils import append_job_log

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    append_job_log(job_path, "batch_gen_docs: starting")
    for step in ["gen_resume_html","gen_coverletter_html","gen_resume_pdf","gen_coverletter_pdf"]:
        res = await run_event(step, job_path, ctx)
        if not res.ok:
            await run_event("move_errored", job_path, ctx)
            return EventResult(ok=False, job_path=job_path, message=f"failed at {step}", errors=res.errors)
    moved = await run_event("move_docs_gen", job_path, ctx)
    return EventResult(ok=moved.ok, job_path=moved.job_path, message="docs generated")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

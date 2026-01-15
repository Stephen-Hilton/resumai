from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events.event_bus import run_event
from src.lib.logging_utils import append_job_log

SECTIONS = [
  "gen_truthful_summary",
  "gen_truthful_skills",
  "gen_truthful_highlights",
  "gen_truthful_experience",
  "gen_static_subcontent_education",
  "gen_static_subcontent_awards",
]

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    append_job_log(job_path, "batch_gen_data_truthful: starting")
    for ev in SECTIONS:
        res = await run_event(ev, job_path, ctx)
        if not res.ok:
            append_job_log(job_path, f"batch_gen_data_truthful: stopped at {ev}")
            return EventResult(ok=False, job_path=job_path, message=f"stopped at {ev}", errors=res.errors)
    moved = await run_event("move_data_gen", job_path, ctx)
    return EventResult(ok=moved.ok, job_path=moved.job_path, message="data generated")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

from __future__ import annotations

import asyncio
from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events.event_bus import run_events_parallel, run_event
from src.lib.logging_utils import append_job_log

LLM_EVENTS = [
    "gen_llm_subcontent_summary",
    "gen_llm_subcontent_skills",
    "gen_llm_subcontent_highlights",
    "gen_llm_subcontent_experience",
    "gen_static_subcontent_education",
    "gen_static_subcontent_awards",
    "gen_llm_subcontent_coverletter",
]

STATIC_EVENTS = [
    "gen_static_subcontent_summary",
    "gen_static_subcontent_skills",
    "gen_static_subcontent_highlights",
    "gen_static_subcontent_experience",
    "gen_static_subcontent_education",
    "gen_static_subcontent_awards",
    "gen_static_subcontent_coverletter",
]

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    mode = ctx.state.get("mode","llm")  # llm|static
    events = LLM_EVENTS if mode == "llm" else STATIC_EVENTS
    append_job_log(job_path, f"batch_gen_data: starting mode={mode} events={len(events)}")
    results = await run_events_parallel(events, job_path, ctx)
    if not all(r.ok for r in results):
        # move to errored
        ctx2 = ctx
        ctx2.state = {**ctx.state, "message": "batch_gen_data failed; moving to Errored"}
        await run_event("move_errored", job_path, ctx2)
        return EventResult(ok=False, job_path=job_path, message="batch_gen_data failed", errors=[{"event": r.message} for r in results if not r.ok])
    # move to data generated
    moved = await run_event("move_data_gen", job_path, ctx)
    return EventResult(ok=moved.ok, job_path=moved.job_path, message="data generated")

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

from __future__ import annotations

import asyncio
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Optional, Tuple

from src.lib.types import EventContext, EventResult, EventHandler
from src.lib.logging_utils import append_app_log

EVENTS_PACKAGE = "src.events"

def discover_events() -> Dict[str, str]:
    """Return mapping event_name -> module_path."""
    mapping: Dict[str, str] = {}
    pkg = importlib.import_module(EVENTS_PACKAGE)
    for m in pkgutil.iter_modules(pkg.__path__):
        if m.ispkg:
            continue
        name = m.name
        if name in ("event_bus",):
            continue
        mapping[name] = f"{EVENTS_PACKAGE}.{name}"
    return mapping

async def run_event(event_name: str, job_path: Path, ctx: EventContext) -> EventResult:
    mapping = discover_events()
    if event_name not in mapping:
        return EventResult(ok=False, job_path=job_path, message=f"Unknown event: {event_name}")
    module = importlib.import_module(mapping[event_name])
    fn_name = "test" if ctx.test_mode else "execute"
    fn: Optional[EventHandler] = getattr(module, fn_name, None)
    if fn is None:
        return EventResult(ok=False, job_path=job_path, message=f"Event {event_name} missing {fn_name}()")

    try:
        res = await fn(job_path, ctx)
        return res
    except Exception as e:
        append_app_log(Path('src/logs'), f"ERROR event={event_name} job={job_path} err={e}")
        return EventResult(ok=False, job_path=job_path, message=str(e), errors=[{"exception": repr(e)}])

async def run_events_parallel(event_names: list[str], job_path: Path, ctx: EventContext) -> list[EventResult]:
    tasks = [asyncio.create_task(run_event(name, job_path, ctx)) for name in event_names]
    return await asyncio.gather(*tasks)

def run_event_sync(event_name: str, job_path: Path, ctx: EventContext) -> EventResult:
    return asyncio.run(run_event(event_name, job_path, ctx))

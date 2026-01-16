from __future__ import annotations

import asyncio
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Optional, Tuple
import traceback as tb

from src.lib.types import EventContext, EventResult, EventHandler
from src.lib.logging_utils import append_app_log
from src.lib.error_utils import generate_error_md, should_move_to_errored

EVENTS_PACKAGE = "src.events"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2  # Exponential backoff base

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

async def run_event(event_name: str, job_path: Path, ctx: EventContext, retry_count: int = 0) -> EventResult:
    """
    Execute an event with optional retry logic.
    
    Args:
        event_name: Name of the event to execute
        job_path: Path to the job folder
        ctx: Event context
        retry_count: Current retry attempt (0 = first attempt)
        
    Returns:
        EventResult with execution status
    """
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
        if not res.ok and retry_count < MAX_RETRIES:
            # Event failed, attempt retry
            delay = RETRY_DELAY_SECONDS * (2 ** retry_count)  # Exponential backoff
            append_app_log(Path('src/logs'), f"RETRY event={event_name} job={job_path} attempt={retry_count + 1}/{MAX_RETRIES} delay={delay}s")
            await asyncio.sleep(delay)
            return await run_event(event_name, job_path, ctx, retry_count + 1)
        elif not res.ok and retry_count >= MAX_RETRIES:
            # Max retries exhausted, generate error.md and potentially move to Errored
            append_app_log(Path('src/logs'), f"FAILED event={event_name} job={job_path} - all retry attempts exhausted")
            
            # Log to job.log as well
            from src.lib.logging_utils import append_job_log
            append_job_log(job_path, f"FAILED event={event_name} - {res.message}")
            
            if should_move_to_errored(event_name, retry_count + 1, MAX_RETRIES, res.message):
                # Generate error.md
                error_details = {
                    "Attempts": retry_count + 1,
                    "Max Retries": MAX_RETRIES,
                    "Event": event_name
                }
                if res.errors:
                    error_details.update(res.errors[0] if isinstance(res.errors[0], dict) else {"Error": str(res.errors[0])})
                
                generate_error_md(
                    job_path=job_path,
                    event_name=event_name,
                    error_message=res.message,
                    error_details=error_details,
                    originating_phase=job_path.parent.name
                )
                
                # Move to Errored phase (skip retries by passing high retry_count)
                try:
                    move_result = await run_event("move_errored", job_path, ctx, retry_count=999)  # Skip retries for move
                    if move_result.ok:
                        res.job_path = move_result.job_path
                        append_job_log(res.job_path, f"Moved to Errored phase due to repeated failures")
                except Exception as move_error:
                    append_app_log(Path('src/logs'), f"ERROR moving job to Errored phase: {move_error}")
            else:
                # Systemic failure detected - don't move to Errored
                append_app_log(Path('src/logs'), f"SYSTEMIC_FAILURE detected for event={event_name} - job remains in current phase")
                append_job_log(job_path, f"SYSTEMIC_FAILURE: {res.message} - job not moved to Errored (likely configuration issue)")
        
        return res
    except Exception as e:
        error_traceback = tb.format_exc()
        error_message = str(e)
        append_app_log(Path('src/logs'), f"ERROR event={event_name} job={job_path} err={e} attempt={retry_count + 1}/{MAX_RETRIES + 1}")
        
        # Log to job.log as well
        from src.lib.logging_utils import append_job_log
        append_job_log(job_path, f"ERROR event={event_name} attempt={retry_count + 1}: {error_message}")
        
        if retry_count < MAX_RETRIES:
            # Exception occurred, attempt retry
            delay = RETRY_DELAY_SECONDS * (2 ** retry_count)  # Exponential backoff
            append_app_log(Path('src/logs'), f"RETRY event={event_name} job={job_path} attempt={retry_count + 1}/{MAX_RETRIES} delay={delay}s")
            await asyncio.sleep(delay)
            return await run_event(event_name, job_path, ctx, retry_count + 1)
        
        # Max retries exhausted
        append_app_log(Path('src/logs'), f"FAILED event={event_name} job={job_path} - all retry attempts exhausted")
        append_job_log(job_path, f"FAILED event={event_name} - all retry attempts exhausted: {error_message}")
        
        if should_move_to_errored(event_name, retry_count + 1, MAX_RETRIES, error_message):
            # Generate error.md
            error_details = {
                "Exception Type": type(e).__name__,
                "Attempts": retry_count + 1,
                "Max Retries": MAX_RETRIES,
                "Event": event_name
            }
            
            generate_error_md(
                job_path=job_path,
                event_name=event_name,
                error_message=f"Event failed after {MAX_RETRIES + 1} attempts: {error_message}",
                error_details=error_details,
                originating_phase=job_path.parent.name,
                traceback=error_traceback
            )
            
            # Move to Errored phase (skip retries by passing high retry_count)
            try:
                move_result = await run_event("move_errored", job_path, ctx, retry_count=999)  # Skip retries for move
                if move_result.ok:
                    job_path = move_result.job_path
                    append_job_log(job_path, f"Moved to Errored phase due to repeated failures")
            except Exception as move_error:
                append_app_log(Path('src/logs'), f"ERROR moving job to Errored phase: {move_error}")
        else:
            # Systemic failure detected - don't move to Errored
            append_app_log(Path('src/logs'), f"SYSTEMIC_FAILURE detected for event={event_name} - job remains in current phase")
            append_job_log(job_path, f"SYSTEMIC_FAILURE: {error_message} - job not moved to Errored (likely configuration issue)")
        
        return EventResult(
            ok=False, 
            job_path=job_path, 
            message=f"Event failed after {MAX_RETRIES + 1} attempts: {str(e)}", 
            errors=[{
                "exception": repr(e),
                "attempts": retry_count + 1,
                "max_retries": MAX_RETRIES,
                "traceback": error_traceback
            }]
        )

async def run_events_parallel(event_names: list[str], job_path: Path, ctx: EventContext) -> list[EventResult]:
    tasks = [asyncio.create_task(run_event(name, job_path, ctx)) for name in event_names]
    return await asyncio.gather(*tasks)

def run_event_sync(event_name: str, job_path: Path, ctx: EventContext) -> EventResult:
    return asyncio.run(run_event(event_name, job_path, ctx))

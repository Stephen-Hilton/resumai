from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.logging_utils import append_job_log


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Log a message to the job's log file.
    
    Expected state:
        - message: str - The message to log
        - context: str (optional) - Additional context for the log entry
    
    Format: {YYYY-MM-DD HH:MM:SS} - {job_name} - {context} - {message}
    """
    message = ctx.state.get("message", "")
    context = ctx.state.get("context", "")
    
    if not message:
        return EventResult(
            ok=False,
            job_path=job_path,
            message="No message provided to log",
            errors=[{"error": "message field is required in state"}]
        )
    
    # Sanitize message and context - remove newlines and extra whitespace
    message = " ".join(message.split())
    context = " ".join(context.split())
    
    # Format the log entry with optional context
    if context:
        log_entry = f"{context} - {message}"
    else:
        log_entry = message
    
    try:
        append_job_log(job_path, log_entry)
        return EventResult(
            ok=True,
            job_path=job_path,
            message=f"Logged: {log_entry}"
        )
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to log message: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate message exists but don't write."""
    message = ctx.state.get("message", "")
    
    if not message:
        return EventResult(
            ok=False,
            job_path=job_path,
            message="No message provided to log"
        )
    
    return EventResult(
        ok=True,
        job_path=job_path,
        message="Test: would log message"
    )

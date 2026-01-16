from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.events.event_bus import run_event


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Send a notification to the user via WebSocket and log the message.
    
    Expected state:
        - message: str - The notification message
        - context: str (optional) - Additional context
        - notification_type: str (optional) - Type of notification (info, success, warning, error)
    
    This event:
    1. Sends a WebSocket message to the UI (if WebSocket is available)
    2. Calls log_message to also log the notification
    """
    message = ctx.state.get("message", "")
    context = ctx.state.get("context", "notify_user")
    notification_type = ctx.state.get("notification_type", "info")
    
    if not message:
        return EventResult(
            ok=False,
            job_path=job_path,
            message="No message provided for notification",
            errors=[{"error": "message field is required in state"}]
        )
    
    # TODO: Send WebSocket message when WebSocket manager is implemented
    # For now, we'll just log it
    # Expected WebSocket payload:
    # {
    #     "type": "notification",
    #     "notification_type": notification_type,
    #     "job_folder_name": job_path.name,
    #     "message": message,
    #     "context": context
    # }
    
    # Call log_message to also log this notification
    log_ctx = EventContext(
        jobs_root=ctx.jobs_root,
        resumes_root=ctx.resumes_root,
        default_resume=ctx.default_resume,
        test_mode=ctx.test_mode,
        state={
            "message": message,
            "context": context
        }
    )
    
    log_result = await run_event("log_message", job_path, log_ctx)
    
    if not log_result.ok:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to log notification: {log_result.message}",
            errors=log_result.errors
        )
    
    return EventResult(
        ok=True,
        job_path=job_path,
        message=f"Notification sent: {message}"
    )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate message exists but don't send notification."""
    message = ctx.state.get("message", "")
    
    if not message:
        return EventResult(
            ok=False,
            job_path=job_path,
            message="No message provided for notification"
        )
    
    return EventResult(
        ok=True,
        job_path=job_path,
        message="Test: would send notification"
    )

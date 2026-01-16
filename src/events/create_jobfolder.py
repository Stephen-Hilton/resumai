from __future__ import annotations

from pathlib import Path
from datetime import datetime
from src.lib.types import EventContext, EventResult
from src.lib.job_folders import JobIdentity, folder_name, phase_path
from src.lib.yaml_utils import dump_job_yaml
from src.lib.logging_utils import append_job_log

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    # job_path may be a placeholder path; we create folder in 1_Queued based on ctx.state['job']
    job = ctx.state.get("job")
    if not job:
        return EventResult(ok=False, job_path=job_path, message="ctx.state['job'] missing")
    
    # Generate unique job ID if not provided
    if not job.get("id"):
        import uuid
        job["id"] = str(uuid.uuid4().hex[:12])
    
    identity = JobIdentity(
        company=job.get("company","Unknown"),
        title=job.get("title","Unknown"),
        posted_at=datetime.strptime(job.get("date_posted","1970-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S") if job.get("date_posted") else datetime.now(),
        job_id=str(job.get("id")),
    )
    name = folder_name(identity)
    dest = phase_path(ctx.jobs_root, "1_Queued") / name
    if dest.exists():
        return EventResult(ok=False, job_path=dest, message="job folder exists already")
    dest.mkdir(parents=True, exist_ok=False)
    dump_job_yaml(dest / "job.yaml", job)
    append_job_log(dest, "create_jobfolder: created")
    return EventResult(ok=True, job_path=dest, message="created", artifacts=["job.yaml"])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

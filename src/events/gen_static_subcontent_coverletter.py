from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.logging_utils import append_job_log

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    job = load_yaml(job_path / "job.yaml")
    resume_path = ctx.resumes_root / ctx.default_resume
    resume = load_yaml(resume_path)
    out = {"section": "coverletter", "mode": "static", "content": resume.get("coverletter") or resume.get("Coverletter")}
    out_path = job_path / f"subcontent.coverletter.yaml"
    dump_yaml(out_path, out)
    append_job_log(job_path, f"gen_static_subcontent_coverletter: wrote {out_path.name}")
    return EventResult(ok=True, job_path=job_path, message="ok", artifacts=[out_path.name])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

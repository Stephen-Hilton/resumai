from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.logging_utils import append_job_log
from src.lib.llm import get_llm

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    llm = get_llm()
    job = load_yaml(job_path / "job.yaml")
    resume = load_yaml(ctx.resumes_root / ctx.default_resume)
    prompt = f"""Generate subcontent.highlights.yaml for this job application.

Job:
{job}

Resume:
{resume}

Return YAML with keys: section, mode, content.
Truth-only: do not invent facts; only use resume content.
"""
    resp = await llm.complete(prompt)
    # For now, expect YAML string and save as text; a real implementation should parse and validate.
    out_path = job_path / f"subcontent.highlights.yaml"
    out_path.write_text(resp.text, encoding="utf-8")
    append_job_log(job_path, f"gen_llm_subcontent_highlights: wrote {out_path.name}")
    return EventResult(ok=True, job_path=job_path, message="ok", artifacts=[out_path.name])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

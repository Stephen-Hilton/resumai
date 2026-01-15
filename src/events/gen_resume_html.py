from __future__ import annotations

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml
from src.lib.logging_utils import append_job_log

SECTIONS = ["summary","skills","highlights","experience","education","awards"]

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    resume = load_yaml(ctx.resumes_root / ctx.default_resume)
    job = load_yaml(job_path / "job.yaml")

    sub = {}
    for name in SECTIONS:
        p = job_path / f"subcontent.{name}.yaml"
        sub[name] = load_yaml(p) if p.exists() else None

    env = Environment(
        loader=FileSystemLoader(str(Path("src/ui/templates"))),
        autoescape=select_autoescape(["html"])
    )
    tpl = env.get_template("resume.html")
    html = tpl.render(resume=resume, job=job, sub=sub)
    out = job_path / "resume.html"
    out.write_text(html, encoding="utf-8")
    append_job_log(job_path, "gen_resume_html: wrote resume.html")
    return EventResult(ok=True, job_path=job_path, message="ok", artifacts=["resume.html"])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

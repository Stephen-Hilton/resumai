from __future__ import annotations

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml
from src.lib.logging_utils import append_job_log
from datetime import date

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    resume = load_yaml(ctx.resumes_root / ctx.default_resume)
    job = load_yaml(job_path / "job.yaml")
    cover = load_yaml(job_path / "subcontent.coverletter.yaml").get("content") if (job_path / "subcontent.coverletter.yaml").exists() else ""
    env = Environment(
        loader=FileSystemLoader(str(Path("src/ui/templates"))),
        autoescape=select_autoescape(["html"])
    )
    tpl = env.get_template("coverletter.html")
    html = tpl.render(resume=resume, job=job, cover=cover, today=str(date.today()))
    out = job_path / "coverletter.html"
    out.write_text(html, encoding="utf-8")
    append_job_log(job_path, "gen_coverletter_html: wrote coverletter.html")
    return EventResult(ok=True, job_path=job_path, message="ok", artifacts=["coverletter.html"])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

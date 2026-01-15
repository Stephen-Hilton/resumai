from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.truthful_gen import generate_with_repair, make_validators
from src.lib import prompts
from src.lib.logging_utils import append_job_log

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    job = load_yaml(job_path / "job.yaml")
    resume = load_yaml(ctx.resumes_root / ctx.default_resume)
    verbatim = bool(ctx.state.get("verbatim_mode", False))
    validator = make_validators("skills", resume)

    prompt_builder = lambda inp: getattr(prompts, "skills_prompt")(inp["job"], inp["resume"], verbatim)
    fix_prompt_builder = lambda prev, errs: getattr(prompts, "skills_fix_prompt")(prev, errs)

    ok, payload, errors = await generate_with_repair(
        section="skills",
        job=job,
        resume=resume,
        verbatim_mode=verbatim,
        validator=validator,
        prompt_builder=prompt_builder,
        fix_prompt_builder=fix_prompt_builder,
        job_path=job_path,
    )
    # Persist output
    if ok:
        dump_yaml(job_path / "subcontent.skills.yaml", payload)
        append_job_log(job_path, "gen_truthful_skills: ok")
        return EventResult(ok=True, job_path=job_path, message="ok", artifacts=["subcontent.skills.yaml"])
    else:
        append_job_log(job_path, "gen_truthful_skills: failed validation after repair")
        return EventResult(ok=False, job_path=job_path, message="validation failed", errors=errors)

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.llm import get_llm_interface


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate LLM-based awards subcontent tailored to the job."""
    try:
        job_data = load_yaml(job_path / "job.yaml")
        resume_data = load_yaml(ctx.resumes_root / ctx.default_resume)
        
        title = job_data.get("title", "the position")
        awards = resume_data.get("awards_and_keynotes", [])
        
        system_prompt = """You are an expert resume writer. Prioritize awards and keynotes for a job application.
- Reorder entries by relevance to the target job
- Keep all entries
- Maintain the original YAML structure

Return in the exact same YAML format as provided."""

        user_prompt = f"""Prioritize these awards/keynotes for: {title}

ORIGINAL AWARDS (YAML format):
{_format_awards_yaml(awards)}

Reorder by relevance, keeping all entries."""

        llm = get_llm_interface()
        success, content, error = await llm.generate_content(system_prompt, user_prompt, temperature=0.4)
        
        if not success:
            output_path = job_path / "subcontent.awards.yaml"
            dump_yaml(output_path, awards)
            return EventResult(ok=True, job_path=job_path, message=f"LLM failed, using original: {error}", artifacts=[str(output_path)])
        
        try:
            import yaml
            tailored_awards = yaml.safe_load(content)
            if not isinstance(tailored_awards, list):
                tailored_awards = awards
        except:
            tailored_awards = awards
        
        output_path = job_path / "subcontent.awards.yaml"
        dump_yaml(output_path, tailored_awards)
        
        return EventResult(ok=True, job_path=job_path, message="Generated LLM awards subcontent", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed: {str(e)}", errors=[{"exception": str(e)}])


def _format_awards_yaml(awards_list):
    """Format awards as YAML string."""
    import yaml
    return yaml.dump(awards_list, default_flow_style=False, allow_unicode=True)


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not (job_path / "job.yaml").exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    if not (ctx.resumes_root / ctx.default_resume).exists():
        return EventResult(ok=False, job_path=job_path, message="Resume not found")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate LLM awards")

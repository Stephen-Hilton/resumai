from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.llm import get_llm_interface


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate LLM-based education subcontent tailored to the job."""
    try:
        job_data = load_yaml(job_path / "job.yaml")
        resume_data = load_yaml(ctx.resumes_root / ctx.default_resume)
        
        title = job_data.get("title", "the position")
        description = job_data.get("description", "")
        education = resume_data.get("education", [])
        
        system_prompt = """You are an expert resume writer. Prioritize and format education/certifications for a job application.
- Reorder entries by relevance to the target job (most relevant first)
- Keep all entries but prioritize the most relevant
- Maintain the original YAML structure
- Include all degrees, certifications, and courses

Return the education in the exact same YAML format as provided."""

        user_prompt = f"""Prioritize this education/certifications for the target job:

TARGET JOB: {title}

JOB REQUIREMENTS:
{description[:1500] if description else "Not provided"}

ORIGINAL EDUCATION (YAML format):
{_format_education_yaml(education)}

Reorder by relevance to this role, keeping all entries."""

        llm = get_llm_interface()
        success, content, error = await llm.generate_content(system_prompt, user_prompt, temperature=0.4)
        
        if not success:
            # Fallback to original
            output_path = job_path / "subcontent.education.yaml"
            dump_yaml(output_path, education)
            return EventResult(ok=True, job_path=job_path, message=f"LLM failed, using original: {error}", artifacts=[str(output_path)])
        
        try:
            import yaml
            tailored_education = yaml.safe_load(content)
            if not isinstance(tailored_education, list):
                tailored_education = education
        except:
            tailored_education = education
        
        output_path = job_path / "subcontent.education.yaml"
        dump_yaml(output_path, tailored_education)
        
        return EventResult(ok=True, job_path=job_path, message="Generated LLM education subcontent", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed: {str(e)}", errors=[{"exception": str(e)}])


def _format_education_yaml(education_list):
    """Format education as YAML string."""
    import yaml
    return yaml.dump(education_list, default_flow_style=False, allow_unicode=True)


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not (job_path / "job.yaml").exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    if not (ctx.resumes_root / ctx.default_resume).exists():
        return EventResult(ok=False, job_path=job_path, message="Resume not found")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate LLM education")

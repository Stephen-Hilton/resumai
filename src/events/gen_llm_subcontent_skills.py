from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.llm import get_llm_interface


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate LLM-based skills subcontent tailored to the job."""
    try:
        # Load job and resume data
        job_data = load_yaml(job_path / "job.yaml")
        resume_data = load_yaml(ctx.resumes_root / ctx.default_resume)
        
        company = job_data.get("company", "the company")
        title = job_data.get("title", "the position")
        description = job_data.get("description", "")
        original_skills = resume_data.get("skills", [])
        
        system_prompt = """You are an expert resume writer. Create a tailored skills list for a job application.
- Select and prioritize 10-15 most relevant skills from the candidate's full skill set
- Add any critical skills from the job description that the candidate likely has
- Order skills by relevance to the job (most relevant first)
- Use industry-standard terminology
- Return as a YAML list format, one skill per line starting with '- '"""

        user_prompt = f"""Create a tailored skills list for this job:

JOB: {title} at {company}

JOB DESCRIPTION:
{description[:2000] if description else "Not provided"}

CANDIDATE'S FULL SKILL SET:
{chr(10).join(f'- {skill}' for skill in original_skills)}

Generate a prioritized list of 10-15 most relevant skills."""

        llm = get_llm_interface()
        success, content, error = await llm.generate_content(system_prompt, user_prompt, temperature=0.5)
        
        if not success:
            return EventResult(ok=False, job_path=job_path, message=f"LLM generation failed: {error}", errors=[{"error": error}])
        
        # Parse skills from LLM response
        skills = [line.strip('- ').strip() for line in content.strip().split('\n') if line.strip().startswith('-')]
        
        output_path = job_path / "subcontent.skills.yaml"
        dump_yaml(output_path, skills)
        
        return EventResult(ok=True, job_path=job_path, message=f"Generated LLM skills subcontent ({len(skills)} skills)", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed: {str(e)}", errors=[{"exception": str(e)}])


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not (job_path / "job.yaml").exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    if not (ctx.resumes_root / ctx.default_resume).exists():
        return EventResult(ok=False, job_path=job_path, message="Resume not found")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate LLM skills")

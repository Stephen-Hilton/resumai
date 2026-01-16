from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.llm import get_llm_interface


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate LLM-based highlights subcontent tailored to the job."""
    try:
        job_data = load_yaml(job_path / "job.yaml")
        resume_data = load_yaml(ctx.resumes_root / ctx.default_resume)
        
        title = job_data.get("title", "the position")
        description = job_data.get("description", "")
        experience = resume_data.get("experience", [])
        
        system_prompt = """You are an expert resume writer. Create 4-6 compelling career highlights for a job application.
Each highlight should:
- Be one concise sentence
- Include quantifiable achievements when possible
- Be relevant to the target job
- Use strong action verbs
- Demonstrate impact and results
- Be written in THIRD PERSON ONLY (no "I", "my", "me" - use past tense action verbs)

Return as a YAML list format, one highlight per line starting with '- '"""

        user_prompt = f"""Create career highlights for this job application:

TARGET JOB: {title}

JOB REQUIREMENTS:
{description[:2000] if description else "Not provided"}

CANDIDATE'S EXPERIENCE:
{_format_experience(experience[:3])}

Generate 4-6 impactful career highlights most relevant to this role."""

        llm = get_llm_interface()
        success, content, error = await llm.generate_content(system_prompt, user_prompt, temperature=0.7)
        
        if not success:
            return EventResult(ok=False, job_path=job_path, message=f"LLM generation failed: {error}", errors=[{"error": error}])
        
        highlights = [line.strip('- ').strip() for line in content.strip().split('\n') if line.strip().startswith('-')]
        
        output_path = job_path / "subcontent.highlights.yaml"
        dump_yaml(output_path, highlights)
        
        return EventResult(ok=True, job_path=job_path, message=f"Generated LLM highlights ({len(highlights)} items)", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed: {str(e)}", errors=[{"exception": str(e)}])


def _format_experience(experience_list):
    """Format experience for LLM prompt."""
    if not experience_list:
        return "Not provided"
    formatted = []
    for exp in experience_list:
        company = exp.get("company_name", "Company")
        roles = exp.get("roles", [])
        for role in roles[:1]:
            role_title = role.get("role", "Position")
            bullets = role.get("bullets", [])
            formatted.append(f"\n{role_title} at {company}:")
            for bullet in bullets[:3]:
                formatted.append(f"  - {bullet.get('text', '')}")
    return "\n".join(formatted)


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not (job_path / "job.yaml").exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    if not (ctx.resumes_root / ctx.default_resume).exists():
        return EventResult(ok=False, job_path=job_path, message="Resume not found")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate LLM highlights")

from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.llm import get_llm_interface


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate LLM-based experience subcontent tailored to the job."""
    try:
        job_data = load_yaml(job_path / "job.yaml")
        resume_data = load_yaml(ctx.resumes_root / ctx.default_resume)
        
        title = job_data.get("title", "the position")
        description = job_data.get("description", "not provided")
        experience = resume_data.get("experience", [])
        
        system_prompt = """You are an expert resume writer. Tailor the candidate's work experience for a specific job.
- Keep the same companies and roles
- Rewrite bullet points to emphasize relevant achievements
- Each bullet MUST be either 90-115 characters (1 line) OR 180-240 characters (2 lines) including spaces
- Prioritize bullets most relevant to the target job
- Use strong action verbs and quantify results
- Write in THIRD PERSON ONLY (no "I", "my", "me" - use past tense action verbs like "Led", "Developed", "Managed")
- Maintain the original YAML structure

Return the experience in the exact same YAML format as provided."""

        user_prompt = f"""Tailor this work experience for the target job:

TARGET JOB: {title}

JOB DESCRIPTION:
{description}

ORIGINAL EXPERIENCE (YAML format):
{_format_experience_yaml(experience)}

Rewrite the experience to emphasize relevance to this role. 
Keep the same structure but lightly reword bullet points to better align with the job description.
IMPORTANT: Do NOT fabricate new ideas or experience. All bullets must adhere to real-world experience found in the Resume."""

        llm = get_llm_interface()
        success, content, error = await llm.generate_content(system_prompt, user_prompt, temperature=0.6)
        
        if not success:
            # Fallback to original experience
            output_path = job_path / "subcontent.experience.yaml"
            dump_yaml(output_path, experience)
            return EventResult(ok=True, job_path=job_path, message=f"LLM failed, using original experience: {error}", artifacts=[str(output_path)])
        
        # Try to parse the LLM response as YAML, fallback to original if it fails
        try:
            import yaml
            tailored_experience = yaml.safe_load(content)
            if not isinstance(tailored_experience, list):
                tailored_experience = experience
        except:
            tailored_experience = experience
        
        output_path = job_path / "subcontent.experience.yaml"
        dump_yaml(output_path, tailored_experience)
        
        return EventResult(ok=True, job_path=job_path, message="Generated LLM experience subcontent", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed: {str(e)}", errors=[{"exception": str(e)}])


def _format_experience_yaml(experience_list):
    """Format experience as YAML string for LLM."""
    import yaml
    return yaml.dump(experience_list[:3], default_flow_style=False, allow_unicode=True)


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not (job_path / "job.yaml").exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    if not (ctx.resumes_root / ctx.default_resume).exists():
        return EventResult(ok=False, job_path=job_path, message="Resume not found")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate LLM experience")

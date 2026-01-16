from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.llm import get_llm_interface


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate LLM-based cover letter subcontent tailored to the job."""
    try:
        job_data = load_yaml(job_path / "job.yaml")
        resume_data = load_yaml(ctx.resumes_root / ctx.default_resume)
        
        company = job_data.get("company", "the company")
        title = job_data.get("title", "the position")
        description = job_data.get("description", "")
        name = resume_data.get("name", "Candidate")
        summary = resume_data.get("summary", "")
        experience = resume_data.get("experience", [])
        
        system_prompt = """You are an expert cover letter writer. Create a compelling, personalized cover letter.
The cover letter should:
- Be professional but authentic
- Show genuine interest in the role and company
- Highlight 2-3 most relevant achievements
- Be 3-4 paragraphs
- Use a confident, enthusiastic tone
- Be written in THIRD PERSON ONLY (no "I", "my", "me" - refer to candidate by name or as "the candidate")

Return as YAML with these keys: greeting, opening, body (list of paragraphs), closing, signature"""

        user_prompt = f"""Create a cover letter for this job application:

CANDIDATE: {name}
TARGET JOB: {title} at {company}

JOB DESCRIPTION:
{description[:2500] if description else "Not provided"}

CANDIDATE SUMMARY:
{summary}

KEY EXPERIENCE:
{_format_experience(experience[:2])}

Generate a compelling cover letter in YAML format."""

        llm = get_llm_interface()
        success, content, error = await llm.generate_content(system_prompt, user_prompt, temperature=0.7)
        
        if not success:
            # Fallback to template
            coverletter = {
                "greeting": f"Dear Hiring Manager at {company},",
                "opening": f"I am writing to express my interest in the {title} position.",
                "body": [
                    "With my experience and skills, I believe I would be a strong fit for this role.",
                    "I am excited about the opportunity to contribute to your team."
                ],
                "closing": "Thank you for your consideration.",
                "signature": "Sincerely,"
            }
            output_path = job_path / "subcontent.coverletter.yaml"
            dump_yaml(output_path, coverletter)
            return EventResult(ok=True, job_path=job_path, message=f"LLM failed, using template: {error}", artifacts=[str(output_path)])
        
        try:
            import yaml
            coverletter = yaml.safe_load(content)
            if not isinstance(coverletter, dict):
                raise ValueError("Invalid format")
        except:
            coverletter = {
                "greeting": f"Dear Hiring Manager at {company},",
                "opening": content[:200],
                "body": [content[200:600], content[600:1000]],
                "closing": "Thank you for your consideration.",
                "signature": "Sincerely,"
            }
        
        output_path = job_path / "subcontent.coverletter.yaml"
        dump_yaml(output_path, coverletter)
        
        return EventResult(ok=True, job_path=job_path, message="Generated LLM cover letter", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed: {str(e)}", errors=[{"exception": str(e)}])


def _format_experience(experience_list):
    """Format experience for prompt."""
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
            for bullet in bullets[:2]:
                formatted.append(f"  - {bullet.get('text', '')}")
    return "\n".join(formatted)


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not (job_path / "job.yaml").exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    if not (ctx.resumes_root / ctx.default_resume).exists():
        return EventResult(ok=False, job_path=job_path, message="Resume not found")
    return EventResult(ok=True, job_path=job_path, message="Test: would generate LLM cover letter")

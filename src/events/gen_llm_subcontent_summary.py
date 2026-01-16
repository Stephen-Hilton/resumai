from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml
from src.lib.llm import get_llm_interface


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Generate LLM-based summary subcontent tailored to the job.
    
    Reads job.yaml and resume.yaml, uses LLM to generate a tailored summary,
    and writes to subcontent.summary.yaml.
    """
    try:
        # Load job data
        job_yaml_path = job_path / "job.yaml"
        if not job_yaml_path.exists():
            return EventResult(
                ok=False,
                job_path=job_path,
                message="job.yaml not found",
                errors=[{"error": "job.yaml not found"}]
            )
        
        job_data = load_yaml(job_yaml_path)
        company = job_data.get("company", "the company")
        title = job_data.get("title", "the position")
        description = job_data.get("description", "")
        
        # Load resume data
        resume_path = ctx.resumes_root / ctx.default_resume
        if not resume_path.exists():
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"Resume file not found: {resume_path}",
                errors=[{"error": f"Resume file not found: {resume_path}"}]
            )
        
        resume_data = load_yaml(resume_path)
        original_summary = resume_data.get("summary", "")
        experience = resume_data.get("experience", [])
        skills = resume_data.get("skills", [])
        
        # Build context for LLM
        system_prompt = """You are an expert resume writer. Your task is to create a compelling professional summary 
tailored to a specific job posting. The summary should:
- Be 3-4 sentences long
- Highlight relevant experience and skills that match the job requirements
- Use strong action words and quantifiable achievements when possible
- Be written in THIRD PERSON ONLY (no "I", "my", "me" - use candidate's name or professional titles)
- Sound professional but authentic

Return ONLY the summary text, no additional commentary."""

        user_prompt = f"""Create a professional summary for this job application:

JOB TITLE: {title}
COMPANY: {company}

JOB DESCRIPTION:
{description[:2000] if description else "Not provided"}

ORIGINAL SUMMARY:
{original_summary}

KEY SKILLS:
{', '.join(skills[:15]) if skills else "Not provided"}

RECENT EXPERIENCE:
{_format_experience(experience[:2])}

Generate a tailored professional summary that emphasizes the most relevant qualifications for this specific role.
IMPORTANT: Do NOT fabricate new ideas or experience. All ideas must map to existing skills, experience, education, or awards."""

        # Call LLM
        llm = get_llm_interface()
        success, content, error = await llm.generate_content(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7
        )
        
        if not success:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=f"LLM generation failed: {error}",
                errors=[{"error": error}]
            )
        
        # Write to subcontent.summary.yaml
        output_path = job_path / "subcontent.summary.yaml"
        dump_yaml(output_path, {"summary": content.strip()})
        
        return EventResult(
            ok=True,
            job_path=job_path,
            message=f"Generated LLM summary subcontent (cost: ${llm.get_total_cost():.6f})",
            artifacts=[str(output_path)]
        )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to generate summary subcontent: {str(e)}",
            errors=[{"exception": str(e)}]
        )


def _format_experience(experience_list):
    """Format experience for LLM prompt."""
    if not experience_list:
        return "Not provided"
    
    formatted = []
    for exp in experience_list:
        company = exp.get("company_name", "Company")
        roles = exp.get("roles", [])
        if roles:
            role = roles[0].get("role", "Position")
            dates = roles[0].get("dates", "")
            formatted.append(f"- {role} at {company} ({dates})")
    
    return "\n".join(formatted) if formatted else "Not provided"


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - validate files exist but don't call LLM."""
    job_yaml_path = job_path / "job.yaml"
    if not job_yaml_path.exists():
        return EventResult(ok=False, job_path=job_path, message="job.yaml not found")
    
    resume_path = ctx.resumes_root / ctx.default_resume
    if not resume_path.exists():
        return EventResult(ok=False, job_path=job_path, message=f"Resume file not found: {resume_path}")
    
    return EventResult(ok=True, job_path=job_path, message="Test: would generate LLM summary")

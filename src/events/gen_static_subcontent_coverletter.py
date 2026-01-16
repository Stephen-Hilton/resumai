from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.yaml_utils import load_yaml, dump_yaml


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate static coverletter subcontent - creates a template."""
    try:
        # Load job data to get company and title
        job_yaml_path = job_path / "job.yaml"
        if job_yaml_path.exists():
            job_data = load_yaml(job_yaml_path)
            company = job_data.get("company", "Company")
            title = job_data.get("title", "Position")
        else:
            company = "Company"
            title = "Position"
        
        # Create template cover letter
        coverletter = {
            "greeting": f"Dear Hiring Manager at {company},",
            "opening": f"I am writing to express my strong interest in the {title} position at {company}.",
            "body": [
                "With my extensive experience and proven track record, I am confident I would be a valuable addition to your team.",
                "My background aligns well with the requirements of this role, and I am excited about the opportunity to contribute to your organization's success."
            ],
            "closing": "Thank you for considering my application. I look forward to the opportunity to discuss how my skills and experience can benefit your team.",
            "signature": "Sincerely,"
        }
        
        output_path = job_path / "subcontent.coverletter.yaml"
        dump_yaml(output_path, coverletter)
        
        return EventResult(ok=True, job_path=job_path, message="Generated static coverletter subcontent (template)", artifacts=[str(output_path)])
        
    except Exception as e:
        return EventResult(ok=False, job_path=job_path, message=f"Failed to generate coverletter subcontent: {str(e)}", errors=[{"exception": str(e)}])


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    return EventResult(ok=True, job_path=job_path, message="Test: would generate coverletter template")

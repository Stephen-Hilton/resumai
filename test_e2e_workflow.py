"""
End-to-end workflow test for job application automation.

This demonstrates the complete workflow from job creation to document generation.
"""

import asyncio
import pytest
from pathlib import Path
from src.lib.types import EventContext
from src.events.event_bus import run_event
from src.lib.yaml_utils import dump_yaml
import shutil


@pytest.mark.asyncio
async def test_complete_workflow():
    """Test the complete workflow: create job -> generate data -> generate docs."""
    
    print("=" * 60)
    print("Job Application Automation - End-to-End Test")
    print("=" * 60)
    
    # Setup
    jobs_root = Path("jobs")
    test_job_name = "TestCorp.SeniorEngineer.20260114-120000.e2etest"
    
    # Clean up any existing test job
    for phase_dir in jobs_root.glob("*"):
        if phase_dir.is_dir():
            test_job = phase_dir / test_job_name
            if test_job.exists():
                shutil.rmtree(test_job)
    
    ctx = EventContext(
        jobs_root=jobs_root,
        resumes_root=Path("resumes"),
        default_resume="Stephen_Hilton.yaml",
        test_mode=False
    )
    
    # Step 1: Create job folder
    print("\n[Step 1] Creating job folder...")
    job_data = {
        "id": "e2etest",
        "company": "TestCorp",
        "title": "Senior Software Engineer",
        "date": "2026-01-14 12:00:00",
        "location": "Remote",
        "salary": "$150K-$200K",
        "description": """
We are seeking a Senior Software Engineer with expertise in Python, cloud architecture,
and distributed systems. The ideal candidate will have 5+ years of experience building
scalable applications and leading technical teams.

Key Responsibilities:
- Design and implement scalable backend systems
- Lead technical architecture decisions
- Mentor junior engineers
- Collaborate with product teams

Requirements:
- 5+ years of software engineering experience
- Strong Python and cloud platform knowledge
- Experience with AWS, Docker, Kubernetes
- Excellent communication skills
        """,
        "subcontent_events": [
            {"contacts": "gen_static_subcontent_contacts"},
            {"summary": "gen_static_subcontent_summary"},
            {"skills": "gen_static_subcontent_skills"},
            {"experience": "gen_static_subcontent_experience"},
            {"education": "gen_static_subcontent_education"},
            {"awards": "gen_static_subcontent_awards"},
            {"coverletter": "gen_static_subcontent_coverletter"}
        ]
    }
    
    ctx.state = {"job": job_data}
    result = await run_event("create_jobfolder", Path("placeholder"), ctx)
    
    if not result.ok:
        print(f"❌ Failed to create job folder: {result.message}")
        return False
    
    job_path = result.job_path
    print(f"✅ Job folder created: {job_path}")
    
    # Step 2: Generate all subcontent data
    print("\n[Step 2] Generating subcontent data...")
    result = await run_event("batch_gen_data", job_path, ctx)
    
    if not result.ok:
        print(f"❌ Failed to generate data: {result.message}")
        return False
    
    job_path = result.job_path
    print(f"✅ Data generated, job moved to: {job_path}")
    
    # List generated subcontent files
    subcontent_files = list(job_path.glob("subcontent.*.yaml"))
    print(f"   Generated {len(subcontent_files)} subcontent files:")
    for f in subcontent_files:
        print(f"   - {f.name}")
    
    # Step 3: Generate all documents
    print("\n[Step 3] Generating documents (HTML and PDF)...")
    result = await run_event("batch_gen_docs", job_path, ctx)
    
    if not result.ok:
        print(f"❌ Failed to generate documents: {result.message}")
        return False
    
    job_path = result.job_path
    print(f"✅ Documents generated, job moved to: {job_path}")
    
    # List generated documents
    html_files = list(job_path.glob("*.html"))
    pdf_files = list(job_path.glob("*.pdf"))
    css_files = list(job_path.glob("*.css"))
    
    print(f"   Generated {len(html_files)} HTML files:")
    for f in html_files:
        print(f"   - {f.name} ({f.stat().st_size:,} bytes)")
    
    print(f"   Generated {len(pdf_files)} PDF files:")
    for f in pdf_files:
        print(f"   - {f.name} ({f.stat().st_size:,} bytes)")
    
    print(f"   Generated {len(css_files)} CSS files")
    
    # Step 4: Verify final state
    print("\n[Step 4] Verifying final state...")
    
    # Check job is in correct phase
    expected_phase = "3_Docs_Generated"
    if job_path.parent.name == expected_phase:
        print(f"✅ Job is in correct phase: {expected_phase}")
    else:
        print(f"❌ Job is in wrong phase: {job_path.parent.name} (expected {expected_phase})")
        return False
    
    # Check all required files exist
    required_files = [
        "job.yaml",
        "job.log",
        "resume.html",
        "resume.pdf",
        "coverletter.html",
        "coverletter.pdf"
    ]
    
    missing_files = []
    for filename in required_files:
        if not (job_path / filename).exists():
            missing_files.append(filename)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print(f"✅ All required files present")
    
    # Read job log
    log_file = job_path / "job.log"
    log_content = log_file.read_text()
    log_lines = log_content.strip().split('\n')
    print(f"\n[Job Log] {len(log_lines)} entries:")
    for line in log_lines[-5:]:  # Show last 5 entries
        print(f"   {line}")
    
    print("\n" + "=" * 60)
    print("✅ END-TO-END TEST PASSED!")
    print("=" * 60)
    print(f"\nGenerated files are in: {job_path}")
    print(f"You can view the resume at: {job_path / 'resume.html'}")
    print(f"You can view the PDF at: {job_path / 'resume.pdf'}")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_complete_workflow())
    exit(0 if success else 1)

from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.pdf_generator import generate_pdf, is_playwright_available


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """Generate cover letter PDF from coverletter.html."""
    try:
        # Check Playwright is available
        if not is_playwright_available():
            return EventResult(
                ok=False,
                job_path=job_path,
                message="Playwright not installed",
                errors=[{"error": "Run: pip install playwright && playwright install chromium"}]
            )
        
        # Check that coverletter.html exists
        html_path = job_path / "coverletter.html"
        if not html_path.exists():
            return EventResult(
                ok=False,
                job_path=job_path,
                message="coverletter.html not found",
                errors=[{"error": "coverletter.html missing - run gen_coverletter_html first"}]
            )
        
        # Generate PDF (overwrite if exists)
        pdf_path = job_path / "coverletter.pdf"
        success, error = await generate_pdf(html_path, pdf_path)
        
        if not success:
            return EventResult(
                ok=False,
                job_path=job_path,
                message=error,
                errors=[{"error": error}]
            )
        
        return EventResult(
            ok=True,
            job_path=job_path,
            message="Generated coverletter.pdf",
            artifacts=[str(pdf_path)]
        )
        
    except Exception as e:
        return EventResult(
            ok=False,
            job_path=job_path,
            message=f"Failed to generate cover letter PDF: {str(e)}",
            errors=[{"exception": str(e)}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode."""
    if not is_playwright_available():
        return EventResult(ok=False, job_path=job_path, message="Playwright not installed")
    
    html_path = job_path / "coverletter.html"
    if not html_path.exists():
        return EventResult(ok=False, job_path=job_path, message="coverletter.html not found")
    
    return EventResult(ok=True, job_path=job_path, message="Test: would generate coverletter.pdf")

from __future__ import annotations

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.logging_utils import append_job_log
from playwright.async_api import async_playwright

async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    html_path = job_path / "coverletter.html"
    if not html_path.exists():
        return EventResult(ok=False, job_path=job_path, message="coverletter.html missing")
    pdf_path = job_path / "coverletter.pdf"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(html_path.resolve().as_uri())
        await page.pdf(path=str(pdf_path), format="Letter", print_background=True)
        await browser.close()
    append_job_log(job_path, "gen_coverletter_pdf: wrote coverletter.pdf")
    return EventResult(ok=True, job_path=job_path, message="ok", artifacts=["coverletter.pdf"])

async def test(job_path: Path, ctx: EventContext) -> EventResult:
    return EventResult(ok=True, job_path=job_path, message="test ok")

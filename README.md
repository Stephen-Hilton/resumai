# Resumai2 — Job Application Automation (local-first)

This project implements the event-driven job application pipeline described in `PROJECT_DESIGN.md`.

## Quick start

1. Create and activate a venv (recommended name `.venv_resumai`):
   ```bash
   python -m venv .venv_resumai
   source .venv_resumai/bin/activate
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

2. Copy env file:
   ```bash
   cp .env.example .env
   ```

3. Run the web UI:
   ```bash
   ./run_webserver.sh
   ```

Open http://127.0.0.1:5000

## Key concepts

- Jobs are stored on disk under `jobs/<phase>/<company>.<title>.<date>.<id>/`
- Each job folder contains:
  - `job.yaml` (required)
  - `job.html` (optional; raw captured posting)
  - `subcontent.*.yaml` (generated in 2_Data Generated)
  - `resume.html/pdf` + `coverletter.html/pdf` (generated in 3_Docs Generated)
- Work is performed via **events** under `src/events/*.py`.
  - Each event implements `async def execute(job_path: Path, ctx: EventContext) -> EventResult`
  - And `async def test(...)` for non-destructive tests.

## Notes

- LLM integration is stubbed behind an interface in `src/lib/llm.py`.
- Gmail IMAP ingestion is implemented as a starter in `get_gmail_linkedin`.
- Playwright is used for PDF rendering for better fidelity than WeasyPrint.
